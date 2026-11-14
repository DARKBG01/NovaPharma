#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_client_info.py — Fiche client détaillée
=================================================
Affiche :
  - Le header (avatar, nom, numéro, badge statut)
  - 3 cartes stats : Total acheté / Visites / Dernière visite
  - Les coordonnées complètes
  - L'historique des achats (QTableWidget pur, aucune limite)

Signaux émis :
  - client_deleted(id) : après suppression
  - client_edited(id)  : après modification
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore

from Client.api_singleton import is_client_mode, get_api
from Database import db
from Interface_client_information import Ui_Dialog

logger = logging.getLogger(__name__)


# Limite d'affichage de l'historique (perf)
HISTORY_LIMIT = 500


class ClientInfoDialog(QtWidgets.QDialog, Ui_Dialog):

    client_deleted = QtCore.Signal(str)
    client_edited  = QtCore.Signal(str)

    def __init__(self, parent=None, client_id: str = None,
                 user_id: str = None, role: str = "ADMIN"):
        super().__init__(parent)
        self.setupUi(self)

        self.client_id = client_id
        self.user_id = user_id
        self.role = (role or "UTILISATEUR").upper()
        self._client = None

        # Cache pour éviter les recalculs
        self._cached_stats = None

        # Connexions
        self._connect_signals()

        # Bouton supprimer caché pour non-admin
        if self.role != "ADMIN":
            self.btn_delete.setVisible(False)

        # Charge et affiche
        self._load_client()
        self._refresh_ui()

    # ------------------------------------------------------------------
    def _connect_signals(self):
        self.btn_close.clicked.connect(self.reject)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)

    # ------------------------------------------------------------------
    # Chargement
    # ------------------------------------------------------------------
    def _load_client(self):
        """Charge les données du client (API ou DB locale)."""
        try:
            if is_client_mode():
                api = get_api()
                if api is None:
                    self._client = None
                    return
                data = api.get_client(self.client_id)
                # L'API renvoie déjà nb_visites / derniere_visite / historique
                self._client = {
                    "id": data.get("id"),
                    "nom": data.get("nom") or "—",
                    "numero": data.get("numero") or "",
                    "sexe": data.get("sexe") or "M",
                    "montant_total": float(data.get("Montant_total") or 0),
                    "adresse": data.get("adresse"),
                    "email": data.get("email"),
                    "notes": data.get("notes"),
                    "actif": int(data.get("actif") or 0),
                    "_api_nb_visites": int(data.get("nb_visites") or 0),
                    "_api_last_visit": data.get("derniere_visite"),
                    "_api_historique": data.get("historique", []),
                }
                return
            # ─── Mode local ───
            row = db.query_one(
                """SELECT id,
                          COALESCE(C_name, nom) AS nom,
                          numero, sexe,
                          COALESCE(Montant_total, 0) AS montant_total,
                          adresse, email, notes, actif
                   FROM Client WHERE id = ? LIMIT 1""",
                (self.client_id,))
            self._client = dict(row) if row else None
        except Exception:
            logger.exception("Erreur chargement client")
            self._client = None

    def _load_stats(self):
        if not self._client:
            return 0, None

        # ─── Mode client : déjà chargé via get_client() ───
        if "_api_nb_visites" in self._client:
            return (self._client["_api_nb_visites"],
                    self._client.get("_api_last_visit"))

        # ─── Mode local ───
        nom = self._client.get("nom") or ""
        numero = self._client.get("numero") or ""
        exact_name = f"{nom} {numero}".strip() if numero else nom

        try:
            row = db.query_one(
                """SELECT COUNT(DISTINCT Num_fact) AS n_visits,
                          MAX(Date_vent) AS last_visit
                   FROM Historique
                   WHERE Client_name = ?""",
                (exact_name,))
            n_visits = int(row["n_visits"] or 0) if row else 0
            last_visit = row["last_visit"] if row else None
        except Exception:
            logger.exception("Erreur calcul stats")
            n_visits = 0
            last_visit = None

        return n_visits, last_visit

    def _load_history(self):
        if not self._client:
            self._fill_empty_history()
            return

        # ─── Mode client : historique fourni par get_client() ───
        if "_api_historique" in self._client:
            hist = self._client["_api_historique"] or []
            # Normalise : les clés sont déjà Date_vent, Num_fact, etc.
            self._populate_history(hist)
            return

        # ─── Mode local ───
        nom = self._client.get("nom") or ""
        numero = self._client.get("numero") or ""
        exact_name = f"{nom} {numero}".strip() if numero else nom

        try:
            rows = db.query(
                """SELECT Date_vent, Num_fact, Article, Quantite, Total
                   FROM Historique
                   WHERE Client_name = ?
                   ORDER BY Date_vent DESC
                   LIMIT ?""",
                (exact_name, HISTORY_LIMIT))
        except Exception:
            logger.exception("Erreur chargement historique")
            rows = []

        self._populate_history(rows)

    def _fill_empty_history(self):
        table = self.history_table
        table.setRowCount(1)
        item = QtWidgets.QTableWidgetItem("Aucun achat enregistré")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setForeground(QtGui.QColor("#94a3b8"))
        font = QtGui.QFont("Segoe UI", 10)
        font.setItalic(True)
        item.setFont(font)
        table.setItem(0, 0, item)
        table.setSpan(0, 0, 1, table.columnCount())

    def _populate_history(self, rows):
        """Remplit la table d'historique (QTableWidgetItem uniquement)."""
        table = self.history_table
        table.blockSignals(True)
        table.setRowCount(0)
        table.clearSpans()

        if not rows:
            self._fill_empty_history()
            table.blockSignals(False)
            return

        table.setRowCount(len(rows))

        font_normal = QtGui.QFont("Segoe UI", 10)
        font_mono   = QtGui.QFont("Courier New", 9)
        font_bold   = QtGui.QFont("Segoe UI", 10)
        font_bold.setBold(True)

        align_c = QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        align_r = QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter

        for i, r in enumerate(rows):
            # Date
            date_str = str(r["Date_vent"])
            # Garde uniquement la date + heure courte
            if len(date_str) > 16:
                date_str = date_str[:16]
            item_date = QtWidgets.QTableWidgetItem(date_str)
            item_date.setFont(font_normal)
            item_date.setForeground(QtGui.QColor("#64748b"))
            table.setItem(i, 0, item_date)

            # N° facture
            item_fact = QtWidgets.QTableWidgetItem(str(r["Num_fact"]))
            item_fact.setFont(font_mono)
            item_fact.setForeground(QtGui.QColor("#94a3b8"))
            table.setItem(i, 1, item_fact)

            # Article
            item_art = QtWidgets.QTableWidgetItem(str(r["Article"]))
            item_art.setFont(font_bold)
            item_art.setForeground(QtGui.QColor("#0f172a"))
            table.setItem(i, 2, item_art)

            # Quantité
            item_qte = QtWidgets.QTableWidgetItem(str(r["Quantite"]))
            item_qte.setFont(font_bold)
            item_qte.setForeground(QtGui.QColor("#0077B6"))
            item_qte.setTextAlignment(align_c)
            table.setItem(i, 3, item_qte)

            # Total
            total = float(r["Total"] or 0)
            item_total = QtWidgets.QTableWidgetItem(
                f"{total:,.2f} FC".replace(",", " "))
            item_total.setFont(font_bold)
            item_total.setForeground(QtGui.QColor("#16A34A"))
            item_total.setTextAlignment(align_r)
            table.setItem(i, 4, item_total)

        table.blockSignals(False)

        # Largeurs
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

    # ------------------------------------------------------------------
    # Rafraîchissement UI
    # ------------------------------------------------------------------
    def _refresh_ui(self):
        if not self._client:
            self.header_name.setText("Client introuvable")
            self.header_numero.setText("—")
            self.header_badge.setVisible(False)
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
            self._fill_empty_history()
            return

        c = self._client
        nom = c.get("nom") or "—"
        numero = c.get("numero") or "—"
        actif = int(c.get("actif") or 0)
        is_anon = str(numero).startswith("ANON-")

        # Header
        sexe = (c.get("sexe") or "M").upper()
        sexe_label = "M" if sexe == "M" else "F"
        self.header_name.setText(nom)
        self.header_numero.setText(f"{numero}   ·   {sexe_label}")

        # Avatar (initiales)
        initiales = self._extract_initials(nom)
        self.avatar.setText(initiales)

        # Badge statut
        if not actif:
            text = "INACTIF"
            style = "QLabel { background-color: #f1f5f9; color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 1px; border-radius: 10px; padding: 5px 12px; }"
        elif is_anon:
            text = "ANONYME"
            style = "QLabel { background-color: #fef3c7; color: #92400e; font-size: 10px; font-weight: 800; letter-spacing: 1px; border-radius: 10px; padding: 5px 12px; }"
        else:
            text = "ACTIF"
            style = "QLabel { background-color: #dcfce7; color: #15803d; font-size: 10px; font-weight: 800; letter-spacing: 1px; border-radius: 10px; padding: 5px 12px; }"

        self.header_badge.setText(text)
        self.header_badge.setStyleSheet(style)

        # Coordonnées
        self._set_coord_value(self.coord_val_phone, numero)
        self._set_coord_value(self.coord_val_email, c.get("email"))
        self._set_coord_value(self.coord_val_adresse, c.get("adresse"))
        self._set_coord_value(self.coord_val_notes, c.get("notes"))

        # Stats
        n_visits, last_visit = self._load_stats()

        # Total acheté
        total = float(c.get("montant_total") or 0)
        self.stat_total_value.setText(
            f"{total:,.2f} FC".replace(",", " "))

        # Visites
        self.stat_visits_value.setText(str(n_visits))

        # Dernière visite
        if last_visit:
            date_part = str(last_visit).split(" ")[0]
            self.stat_last_value.setText(date_part)
        else:
            self.stat_last_value.setText("—")

        # Historique
        self._load_history()

    @staticmethod
    def _extract_initials(nom: str) -> str:
        if not nom:
            return "?"
        parts = nom.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()
        return nom[:2].upper()

    @staticmethod
    def _set_coord_value(label: QtWidgets.QLabel, value):
        """Affiche une valeur ou un placeholder grisé."""
        if value and str(value).strip():
            label.setText(str(value))
            label.setStyleSheet(
                "color: #1e293b; font-size: 13px; font-weight: 600; background: transparent;")
        else:
            label.setText("Non renseigné")
            label.setStyleSheet(
                "color: #cbd5e1; font-size: 13px; font-weight: 500; "
                "font-style: italic; background: transparent;")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def _on_edit(self):
        """Ouvre le dialogue de modification."""
        try:
            from Setting_client_dialog import Setting_client_dialog
            dlg = Setting_client_dialog(
                parent=self, client_id=self.client_id, user_id=self.user_id)
            dlg.client_saved.connect(self._on_client_saved)
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                self._load_client()
                self._refresh_ui()
                self.client_edited.emit(self.client_id)
        except Exception:
            logger.exception("Erreur ouverture dialogue modification")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir le dialogue de modification.")

    def _on_client_saved(self, client_id: str):
        logger.info("Client sauvegardé depuis la fiche : %s", client_id)

    def _on_delete(self):
        """Suppression avec confirmation."""
        if not self._client:
            return
        if self.role != "ADMIN":
            QtWidgets.QMessageBox.warning(
                self, "Accès refusé",
                "Seul un administrateur peut supprimer un client.")
            return

        nom = self._client.get("nom") or "—"
        numero = self._client.get("numero") or "—"

        # Vérifie si le client a des achats
        has_sales = False
        try:
            exact_name = f"{nom} {numero}".strip() if numero else nom
            row = db.query_one(
                "SELECT COUNT(*) AS n FROM Historique WHERE Client_name = ?",
                (exact_name,))
            has_sales = (row and int(row["n"]) > 0)
        except Exception:
            pass

        # Message adapté
        if has_sales:
            msg = (
                f"<b>Supprimer le client « {nom} » ?</b><br><br>"
                "⚠️ Ce client a <b>déjà effectué des achats</b>.<br><br>"
                "Il sera marqué comme <b>inactif</b> et ne pourra plus être "
                "sélectionné lors des nouvelles ventes, mais son historique "
                "sera conservé.<br><br>"
                "<b>Action réversible par un administrateur.</b>"
            )
        else:
            msg = (
                f"<b>Supprimer le client « {nom} » ?</b><br><br>"
                f"Numéro : <code>{numero}</code><br><br>"
                "Le client sera définitivement supprimé.<br><br>"
                "<b>Action irréversible.</b>"
            )

        rep = QtWidgets.QMessageBox.question(
            self, "Confirmation de suppression", msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)

        if rep != QtWidgets.QMessageBox.Yes:
            return

        # ─── MODE CLIENT → API ───
        if is_client_mode():
            try:
                api = get_api()
                if api is None:
                    return
                api.delete_client(self.client_id)
                logger.info("Client supprimé (API) : %s", self.client_id)
                QtWidgets.QMessageBox.information(
                    self, "Client désactivé",
                    f"Le client « {nom} » a été désactivé.")
                self.client_deleted.emit(self.client_id)
                self.accept()
                return
            except Exception as e:
                logger.exception("Erreur suppression client (API)")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible de désactiver le client :\n{e}")
                return

        # ─── MODE LOCAL (code existant) ───
        try:
            with db.transaction():
                if has_sales:
                    db.execute(
                        "UPDATE Client SET actif = 0 WHERE id = ?",
                        (self.client_id,))
                else:
                    db.execute(
                        "DELETE FROM Client WHERE id = ?",
                        (self.client_id,))

            logger.info(
                "Client supprimé : %s (%s) par %s",
                nom, self.client_id, self.user_id)

            QtWidgets.QMessageBox.information(
                self, "Client supprimé",
                f"Le client « {nom} » a été supprimé.")

            self.client_deleted.emit(self.client_id)
            self.accept()

        except Exception as e:
            logger.exception("Échec suppression client")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible de supprimer le client :\n{e}")


# ══════════════════════════════════════════════════════════════════
# Test autonome
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)

    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()
    seed.run()

    # Récupère un client existant
    row = db.query_one("SELECT id FROM Client LIMIT 1")
    if not row:
        print("⚠ Aucun client en base. Créez-en un d'abord.")
        sys.exit(0)

    dlg = ClientInfoDialog(
        client_id=row["id"], user_id="TEST", role="ADMIN")
    dlg.client_deleted.connect(lambda cid: print(f"→ Supprimé : {cid}"))
    dlg.client_edited.connect(lambda cid: print(f"→ Modifié : {cid}"))
    sys.exit(dlg.exec())