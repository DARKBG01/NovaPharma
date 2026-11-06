#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_mes_ventes.py — Liste des ventes du caissier (jour).
==============================================================
Permet au CAISSIER de voir ses ventes du jour et d'annuler
celles qui sont encore annulables.
"""

import logging
from datetime import datetime

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from Client.api_singleton import get_api, is_client_mode
from Database import db, audit

logger = logging.getLogger(__name__)


class Setting_mes_ventes(QtWidgets.QDialog):

    vente_annulee = QtCore.Signal(str)  # num_fact

    def __init__(self, parent=None, user_id: str = None,
                 user_name: str = "", role: str = "CAISSIER",
                 is_owner: bool = False, is_developer: bool = False):
        super().__init__(parent)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.role = (role or "UTILISATEUR").upper()
        self.is_owner = is_owner
        self.is_developer = is_developer

        self._ventes = []

        self.setWindowTitle("Mes ventes du jour")
        self.setMinimumSize(800, 600)
        self.setModal(True)

        self._build_ui()
        self._load_ventes()

    # ══════════════════════════════════════════════════════════════
    def _build_ui(self):
        self.setStyleSheet("""
            QDialog { background: #f0f4f8; }
            QLabel { color: #334155; background: transparent; font-size: 13px; }
            QLabel#header_title {
                color: #023E8A; font-size: 18px; font-weight: 800;
            }
            QLabel#header_sub {
                color: #64748b; font-size: 11px; font-weight: 600;
            }
            QFrame#card {
                background: #ffffff; border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QTableWidget {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                gridline-color: #f1f5f9;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 10px; color: #0f172a;
            }
            QTableWidget::item:selected {
                background: #eff6ff; color: #023E8A;
            }
            QHeaderView::section {
                background: #f8fafc; color: #64748b;
                padding: 10px; border: none;
                border-bottom: 1px solid #e2e8f0;
                font-size: 11px; font-weight: 800;
            }
            QPushButton {
                background: #0077B6; color: white;
                border: none; border-radius: 10px;
                padding: 8px 18px; font-weight: 700;
                font-size: 12px; min-width: 90px;
            }
            QPushButton:hover { background: #023E8A; }
            QPushButton#btn_close {
                background: transparent; color: #64748b;
                border: 1.5px solid #e2e8f0;
            }
            QPushButton#btn_close:hover {
                background: #fef2f2; color: #dc2626;
                border-color: #fecaca;
            }
            QPushButton#btn_cancel_sale {
                background: #fef2f2; color: #dc2626;
                border: 1px solid #fecaca;
                padding: 6px 14px; font-size: 11px;
                min-width: 70px;
            }
            QPushButton#btn_cancel_sale:hover {
                background: #fee2e2;
                border-color: #f87171;
            }
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # ─── Header ───
        h = QtWidgets.QHBoxLayout()
        t = QtWidgets.QVBoxLayout()
        t1 = QtWidgets.QLabel("Mes ventes du jour")
        t1.setObjectName("header_title")
        t.addWidget(t1)
        self.lbl_sub = QtWidgets.QLabel("—")
        self.lbl_sub.setObjectName("header_sub")
        t.addWidget(self.lbl_sub)
        h.addLayout(t)
        h.addStretch()

        btn_refresh = QtWidgets.QPushButton("Actualiser")
        btn_refresh.clicked.connect(self._load_ventes)
        h.addWidget(btn_refresh)
        root.addLayout(h)

        # ─── Carte table ───
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(16, 16, 16, 16)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "N° Facture", "Heure", "Client", "Total", "Statut", ""
        ])
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(52)
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        h_t = self.table.horizontalHeader()
        h_t.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        h_t.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        h_t.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        h_t.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        h_t.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        h_t.setSectionResizeMode(5, QtWidgets.QHeaderView.Fixed)
        self.table.setColumnWidth(5, 100)

        v.addWidget(self.table)
        root.addWidget(card, 1)

        # ─── Footer ───
        hf = QtWidgets.QHBoxLayout()
        hf.addStretch()
        btn_close = QtWidgets.QPushButton("Fermer")
        btn_close.setObjectName("btn_close")
        btn_close.clicked.connect(self.accept)
        hf.addWidget(btn_close)
        root.addLayout(hf)

    # ══════════════════════════════════════════════════════════════
    def _load_ventes(self):
        """Charge les ventes du jour pour ce caissier."""
        try:
            if is_client_mode():
                self._load_ventes_api()
            else:
                self._load_ventes_local()
            self._populate()
        except Exception:
            logger.exception("Erreur chargement mes ventes")

    def _load_ventes_api(self):
        """Charge via l'API."""
        api = get_api()
        if api is None:
            raise RuntimeError("API non initialisée")

        today = datetime.now().strftime("%Y-%m-%d")
        data = api.list_ventes(
            page=1, per_page=100,
            date_debut=today, date_fin=today,
            annule=-1)

        items = data.get("items", [])
        # Filtre : uniquement les ventes de ce caissier
        self._ventes = [
            v for v in items
            if v.get("utilisateur_id") == self.user_id
        ]

    def _load_ventes_local(self):
        """Charge via DB locale."""
        today = datetime.now().strftime("%d/%m/%Y")
        rows = db.query(
            """SELECT Num_fact,
                      MIN(Date_vent) AS date_vent,
                      MAX(Client_name) AS client_name,
                      SUM(Total) AS total,
                      MAX(annule) AS annule,
                      MAX(motif_annulation) AS motif
               FROM Historique
               WHERE Date_vent LIKE ?
                 AND utilisateur_id = ?
               GROUP BY Num_fact
               ORDER BY date_vent DESC""",
            (f"{today}%", self.user_id))
        self._ventes = [dict(r) for r in rows]

    # ══════════════════════════════════════════════════════════════
    def _populate(self):
        t = self.table
        t.setRowCount(0)

        if not self._ventes:
            t.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem(
                "Aucune vente aujourd'hui")
            empty.setTextAlignment(Qt.AlignCenter)
            empty.setForeground(QtGui.QColor("#94a3b8"))
            f = QtGui.QFont("Segoe UI", 11)
            f.setItalic(True)
            empty.setFont(f)
            t.setItem(0, 0, empty)
            t.setSpan(0, 0, 1, t.columnCount())
            self.lbl_sub.setText("0 vente aujourd'hui")
            return

        t.setRowCount(len(self._ventes))
        devise = db.get_config("devise", "FC")

        for i, v in enumerate(self._ventes):
            num_fact = v.get("Num_fact") or "—"
            date_vent = str(v.get("date_vent") or v.get("Date_vent") or "")
            client = v.get("client_name") or v.get("Client_name") or "Anonyme"
            total = float(v.get("total") or v.get("Total") or 0)
            annule = int(v.get("annule") or 0) == 1

            # N° facture
            it0 = QtWidgets.QTableWidgetItem(num_fact)
            it0.setFont(QtGui.QFont("Courier New", 9))
            it0.setForeground(QtGui.QColor("#023E8A"))
            it0.setData(Qt.UserRole, num_fact)
            t.setItem(i, 0, it0)

            # Heure
            heure = date_vent[-8:] if len(date_vent) > 8 else date_vent
            it1 = QtWidgets.QTableWidgetItem(heure)
            it1.setTextAlignment(Qt.AlignCenter)
            it1.setForeground(QtGui.QColor("#64748b"))
            t.setItem(i, 1, it1)

            # Client
            it2 = QtWidgets.QTableWidgetItem(client)
            t.setItem(i, 2, it2)

            # Total
            it3 = QtWidgets.QTableWidgetItem(
                f"{total:,.0f} {devise}".replace(",", " "))
            it3.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            it3.setForeground(QtGui.QColor("#16A34A"))
            it3.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, 3, it3)

            # Statut
            if annule:
                it4 = QtWidgets.QTableWidgetItem("Annulée")
                it4.setForeground(QtGui.QColor("#b91c1c"))
                it4.setBackground(QtGui.QColor("#fee2e2"))
            else:
                it4 = QtWidgets.QTableWidgetItem("Validée")
                it4.setForeground(QtGui.QColor("#15803d"))
                it4.setBackground(QtGui.QColor("#dcfce7"))
            it4.setTextAlignment(Qt.AlignCenter)
            it4.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            t.setItem(i, 4, it4)

            # Bouton annuler
            if not annule:
                btn = QtWidgets.QPushButton("Annuler")
                btn.setObjectName("btn_cancel_sale")
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(
                    lambda _, nf=num_fact, tot=total:
                    self._on_cancel(nf, tot))

                wrap = QtWidgets.QWidget()
                lay = QtWidgets.QHBoxLayout(wrap)
                lay.setContentsMargins(2, 2, 2, 2)
                lay.addWidget(btn)
                t.setCellWidget(i, 5, wrap)

        self.lbl_sub.setText(
            f"{len(self._ventes)} vente(s) aujourd'hui")

    # ══════════════════════════════════════════════════════════════
    def _on_cancel(self, num_fact: str, total: float):
        """Annule une vente après confirmation + motif."""
        devise = db.get_config("devise", "FC")

        # Motif
        motifs = [
            "Client s'est ravisé",
            "Erreur de saisie",
            "Produit défectueux",
            "Doublon",
            "Prix incorrect",
            "Autre (préciser)",
        ]
        motif, ok = QtWidgets.QInputDialog.getItem(
            self, "Annulation de la vente",
            f"Annuler la facture {num_fact} ?\n\nMotif :",
            motifs, 0, False)
        if not ok or not motif:
            return

        if motif.startswith("Autre"):
            motif, ok2 = QtWidgets.QInputDialog.getText(
                self, "Motif personnalisé", "Précisez le motif :")
            if not ok2 or not motif.strip():
                return
            motif = motif.strip()

        # Confirmation
        msg = (
            f"<b>Annuler la facture {num_fact} ?</b><br><br>"
            f"Motif : {motif}<br>"
            f"Montant : <b>{total:,.0f} {devise}</b>"
            .replace(",", " ") + "<br><br>"
            "Le stock sera <b>restitué</b> automatiquement."
        )
        rep = QtWidgets.QMessageBox.question(
            self, "Confirmation", msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        try:
            if is_client_mode():
                api = get_api()
                api.annuler_vente(num_fact, motif)
            else:
                self._cancel_local(num_fact, motif)

            logger.info("Vente annulée : %s", num_fact)
            QtWidgets.QMessageBox.information(
                self, "Annulée",
                f"La facture {num_fact} a été annulée.")
            self.vente_annulee.emit(num_fact)
            self._load_ventes()

        except Exception as e:
            logger.exception("Erreur annulation vente")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'annuler :\n{e}")

    def _cancel_local(self, num_fact: str, motif: str):
        """Annulation locale (DB)."""
        # Récupère les lignes
        lignes = db.query(
            "SELECT Code_reference, Quantite FROM Historique "
            "WHERE Num_fact = ?", (num_fact,))

        with db.transaction():
            db.execute(
                "UPDATE Historique SET annule = 1, motif_annulation = ? "
                "WHERE Num_fact = ?", (motif, num_fact))

            for l in lignes:
                code_ref = l["Code_reference"]
                qte = int(l["Quantite"] or 0)
                if not code_ref:
                    continue

                row_p = db.query_one(
                    "SELECT Quantite, Nom FROM produits "
                    "WHERE Code_reference = ? LIMIT 1", (code_ref,))
                if not row_p:
                    continue

                avant = int(row_p["Quantite"] or 0)
                apres = avant + qte

                db.execute(
                    "UPDATE produits SET Quantite = ? "
                    "WHERE Code_reference = ?", (apres, code_ref))

                db.execute(
                    """INSERT INTO MouvementStock
                       (id, produit_id, type, quantite,
                        stock_avant, stock_apres, motif, utilisateur_id)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (db.new_id(), code_ref, "ANNULATION", qte,
                     avant, apres,
                     f"Annulation {num_fact} — {motif}",
                     self.user_id))

            try:
                audit.log(
                    "ANNULATION_VENTE",
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="vente",
                    cible_id=num_fact,
                    cible_nom=num_fact,
                    details={"motif": motif, "par": "caissier"})
            except Exception:
                pass