#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_blf_detail.py — Détail d'un BLF + validation + annulation
===================================================================
Utilise Interface_blf_detail.py (généré depuis Setting_blf_detail.ui)
"""

import logging
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import get_api, is_client_mode
from Database import db
from Interface_blf_detail import Ui_Dialog
from Ui_helpers import setup_blf_detail_table

logger = logging.getLogger(__name__)


class Setting_blf_detail(QtWidgets.QDialog, Ui_Dialog):

    blf_updated = QtCore.Signal(str)  # blf_id

    def __init__(self, parent=None, blf_id: str = None,
                 user_id: str = None, user_name: str = "",
                 role: str = "ADMIN"):
        super().__init__(parent)
        self.setupUi(self)
        
        setup_blf_detail_table(self.table_lignes)

        self.blf_id = blf_id
        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.role = (role or "UTILISATEUR").upper()

        self._blf = None
        self._lignes = []

        # Signaux
        self.btn_close.clicked.connect(self.reject)
        self.btn_validate_blf.clicked.connect(self._on_validate_blf)
        self.btn_cancel_blf.clicked.connect(self._on_cancel_blf)

        # Charge et affiche
        self._load_data()
        self._refresh()

    # ══════════════════════════════════════════════════════════════
    def _load_data(self):
        try:
            if is_client_mode():
                api = get_api()
                if api is None:
                    self._blf = None
                    return
                data = api.get_blf(self.blf_id)
                self._blf = data
                self._lignes = data.get("lignes", []) or []
                return
            # ─── Mode local ───
            row = db.query_one(
                "SELECT * FROM BonLivraison WHERE id = ? LIMIT 1",
                (self.blf_id,))
            self._blf = dict(row) if row else None

            if self._blf:
                rows = db.query(
                    """SELECT * FROM LigneBonLivraison
                       WHERE blf_id = ? ORDER BY rowid ASC""",
                    (self.blf_id,))
                self._lignes = [dict(r) for r in rows]
        except Exception:
            logger.exception("Erreur chargement BLF")

    def _refresh(self):
        if not self._blf:
            self.header_numero.setText("BLF introuvable")
            self.header_sub.setText("—")
            self.btn_validate_blf.setEnabled(False)
            self.btn_cancel_blf.setEnabled(False)
            return

        blf = self._blf

        # Header
        self.header_numero.setText(f"BLF {blf['numero_blf']}")
        four = blf.get("fournisseur_nom") or "Sans fournisseur"
        self.header_sub.setText(
            f"{four} · {blf.get('date_livraison', '—')}")

        # Statut badge
        statut = blf["statut"]
        if statut == "VALIDEE":
            self.statut_badge.setText("✓ VALIDÉE")
            self.statut_badge.setStyleSheet("""
                background-color: #dcfce7;
                color: #15803d;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1px;
                border-radius: 10px;
                padding: 8px 16px;
            """)
        elif statut == "ANNULEE":
            self.statut_badge.setText("✗ ANNULÉE")
            self.statut_badge.setStyleSheet("""
                background-color: #fee2e2;
                color: #991b1b;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1px;
                border-radius: 10px;
                padding: 8px 16px;
            """)
        else:
            self.statut_badge.setText("● BROUILLON")
            self.statut_badge.setStyleSheet("""
                background-color: #fef3c7;
                color: #92400e;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1px;
                border-radius: 10px;
                padding: 8px 16px;
            """)

        # Métadonnées
        self.val_fournisseur.setText(four)
        self.val_ref_ext.setText(blf.get("reference_externe") or "—")
        self.val_date.setText(blf.get("date_livraison") or "—")
        self.val_created.setText(
            f"{blf.get('created_by_name') or '—'} · "
            f"{blf.get('created_at') or '—'}")
        self.val_validated.setText(
            f"{blf.get('validated_by_name') or '—'} · "
            f"{blf.get('validated_at') or '—'}"
            if blf.get('validated_at') else "—")
        self.val_cancelled.setText(
            f"{blf.get('cancelled_by_name') or '—'} · "
            f"{blf.get('cancelled_at') or '—'}"
            if blf.get('cancelled_at') else "—")

        # Lignes
        self._populate_lignes()

        # Totaux
        self.val_nb_articles.setText(f"{blf['nb_articles']} article(s)")
        self.val_nb_unites.setText(f"{blf['nb_unites']} unité(s)")
        self.total_value.setText(
            f"{blf['total_achat']:,.0f} FC".replace(",", " "))

        # Notes
        if blf.get("notes"):
            self.notes_text.setText(blf["notes"])
            self.notes_wrap.setVisible(True)
        else:
            self.notes_wrap.setVisible(False)

        # Motif annulation
        if blf.get("motif_annulation"):
            self.motif_text.setText(blf["motif_annulation"])
            self.motif_wrap.setVisible(True)
        else:
            self.motif_wrap.setVisible(False)

        # Boutons selon statut + rôle
        can_validate = (statut == "BROUILLON" and self.role == "ADMIN")
        can_cancel = (statut == "VALIDEE" and self.role == "ADMIN")

        self.btn_validate_blf.setVisible(can_validate)
        self.btn_cancel_blf.setVisible(can_cancel)

    def _populate_lignes(self):
        t = self.table_lignes
        t.setRowCount(0)
        t.setRowCount(len(self._lignes))

        font_bold = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        font_mono = QtGui.QFont("Courier New", 9)

        for i, l in enumerate(self._lignes):
            # Code
            item0 = QtWidgets.QTableWidgetItem(l["produit_id"] or "—")
            item0.setFont(font_mono)
            item0.setForeground(QtGui.QColor("#94a3b8"))
            t.setItem(i, 0, item0)

            # Nom
            item1 = QtWidgets.QTableWidgetItem(l["produit_nom"])
            item1.setFont(font_bold)
            t.setItem(i, 1, item1)

            # Qté
            item2 = QtWidgets.QTableWidgetItem(str(l["quantite"]))
            item2.setForeground(QtGui.QColor("#0077B6"))
            item2.setFont(font_bold)
            item2.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, 2, item2)

            # Prix achat
            item3 = QtWidgets.QTableWidgetItem(
                f"{float(l['prix_achat_unitaire'] or 0):.2f} FC")
            item3.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, 3, item3)

            # Prix vente
            item4 = QtWidgets.QTableWidgetItem(
                f"{float(l['prix_vente_unitaire'] or 0):.2f} FC")
            item4.setForeground(QtGui.QColor("#16A34A"))
            item4.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, 4, item4)

            # Total
            item5 = QtWidgets.QTableWidgetItem(
                f"{float(l['total_ligne'] or 0):,.2f} FC".replace(",", " "))
            item5.setForeground(QtGui.QColor("#023E8A"))
            item5.setFont(font_bold)
            item5.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, 5, item5)

            # Stock avant → après
            sa = l.get("stock_avant")
            sp = l.get("stock_apres")
            if sa is not None and sp is not None and sa != sp:
                txt = f"{sa} → {sp}"
                color = "#16A34A" if sp > sa else "#DC2626"
            else:
                txt = "—"
                color = "#94a3b8"
            item6 = QtWidgets.QTableWidgetItem(txt)
            item6.setForeground(QtGui.QColor(color))
            item6.setFont(font_bold)
            item6.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, 6, item6)

        setup_blf_detail_table(t)

    # ══════════════════════════════════════════════════════════════
    def _on_validate_blf(self):
        """Valide un BLF en brouillon."""
        if not self._blf:
            return

        rep = QtWidgets.QMessageBox.question(
            self, "Validation du BLF",
            f"Valider le BLF <b>{self._blf['numero_blf']}</b> ?<br><br>"
            f"Cette action va <b>ajouter</b> {self._blf['nb_unites']} "
            "unité(s) au stock.<br>"
            "<b>Action réversible</b> (annulation possible).",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)

        if rep != QtWidgets.QMessageBox.Yes:
            return

        # ═══════════════════════════════════════════════════════════
        # MODE CLIENT → API
        # ═══════════════════════════════════════════════════════════
        if is_client_mode():
            try:
                api = get_api()
                if api is None:
                    raise RuntimeError("API non initialisée")

                api.valider_blf(self.blf_id)
                logger.info(
                    "BLF validé (API) : %s",
                    self._blf["numero_blf"])
                QtWidgets.QMessageBox.information(
                    self, "BLF validé",
                    "Le BLF a été validé et le stock mis à jour.")
                self.blf_updated.emit(self.blf_id)
                self._load_data()
                self._refresh()
                return
            except Exception as e:
                logger.exception("Erreur validation BLF (API)")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible de valider le BLF :\n{e}")
                return

        # ═══ MODE AUTONOME / SERVEUR → DB locale ═══
        from Database import audit
        try:
            # ─── Snapshot avant validation ───
            avant_blf = audit.snapshot(
                "BonLivraison", "id", self.blf_id)

            with db.transaction():
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                db.execute("""
                    UPDATE BonLivraison
                    SET statut = 'VALIDEE',
                        validated_by = ?,
                        validated_by_name = ?,
                        validated_at = ?
                    WHERE id = ? AND statut = 'BROUILLON'
                """, (self.user_id, self.user_name, now, self.blf_id))

                # Récupère les lignes
                lignes_db = db.query(
                    """SELECT * FROM LigneBonLivraison
                       WHERE blf_id = ?""",
                    (self.blf_id,))

                for l in lignes_db:
                    code_ref = l["produit_id"]
                    if not code_ref:
                        continue

                    row_p = db.query_one(
                        "SELECT Quantite FROM produits "
                        "WHERE Code_reference = ? LIMIT 1",
                        (code_ref,))
                    if not row_p:
                        continue

                    stock_avant = int(row_p["Quantite"] or 0)
                    stock_apres = stock_avant + l["quantite"]

                    db.execute("""
                        UPDATE LigneBonLivraison
                        SET stock_avant = ?, stock_apres = ?
                        WHERE id = ?
                    """, (stock_avant, stock_apres, l["id"]))

                    db.execute("""
                        UPDATE produits
                        SET Quantite = ?, Prix_achat = ?,
                            Prix_vente = ?, Prix_unitaire = ?
                        WHERE Code_reference = ?
                    """, (stock_apres,
                          float(l["prix_achat_unitaire"] or 0),
                          float(l["prix_vente_unitaire"] or 0),
                          float(l["prix_vente_unitaire"] or 0),
                          code_ref))

                    uid_valide = None
                    if self.user_id:
                        try:
                            if db.query_one(
                                    "SELECT 1 FROM Utilisateur "
                                    "WHERE id = ? LIMIT 1",
                                    (self.user_id,)
                            ):
                                uid_valide = self.user_id
                        except Exception:
                            pass

                    db.execute("""
                        INSERT INTO MouvementStock
                        (id, produit_id, type, quantite,
                         stock_avant, stock_apres, motif, utilisateur_id)
                        VALUES (?,?,?,?,?,?,?,?)
                    """, (db.new_id(), code_ref, "ENTREE",
                          l["quantite"], stock_avant, stock_apres,
                          f"BLF {self._blf['numero_blf']} (validation)",
                          uid_valide))

            # ═══ AUDIT VALIDATION ═══
            try:
                apres_blf = audit.snapshot(
                    "BonLivraison", "id", self.blf_id)

                audit.log(
                    audit.ACTION_VALIDATION_BLF,
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="BonLivraison",
                    cible_id=self.blf_id,
                    cible_nom=self._blf["numero_blf"],
                    details={
                        "nb_articles": self._blf.get("nb_articles", 0),
                        "nb_unites": self._blf.get("nb_unites", 0),
                        "total_achat": self._blf.get("total_achat", 0),
                    },
                    avant=avant_blf,
                    apres=apres_blf,
                )
            except Exception:
                logger.exception("Erreur audit validation BLF")

            logger.info("BLF validé : %s", self._blf["numero_blf"])
            QtWidgets.QMessageBox.information(
                self, "BLF validé",
                "Le BLF a été validé et le stock mis à jour.")

            self.blf_updated.emit(self.blf_id)
            self._load_data()
            self._refresh()

        except Exception as e:
            logger.exception("Erreur validation BLF")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible de valider le BLF :\n{e}")

    def _on_cancel_blf(self):
        """Annule un BLF validé → rollback stock."""
        if not self._blf:
            return

        motif, ok = QtWidgets.QInputDialog.getText(
            self, "Annulation du BLF",
            "Motif de l'annulation (obligatoire) :",
            QtWidgets.QLineEdit.Normal,
            "")

        if not ok or not motif.strip():
            if ok:
                QtWidgets.QMessageBox.warning(
                    self, "Motif requis",
                    "Le motif d'annulation est obligatoire.")
            return

        motif = motif.strip()

        msg = (
            f"<b>Annuler le BLF {self._blf['numero_blf']} ?</b><br><br>"
            f"Cette action va <b>retirer</b> "
            f"{self._blf['nb_unites']} unité(s) du stock.<br><br>"
            f"<b>Motif :</b> {motif}<br><br>"
            "⚠ Cette action est <b>définitive</b>."
        )
        rep = QtWidgets.QMessageBox.question(
            self, "Confirmation", msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)

        if rep != QtWidgets.QMessageBox.Yes:
            return

        # ═══════════════════════════════════════════════════════════
        # MODE CLIENT → API
        # ═══════════════════════════════════════════════════════════
        if is_client_mode():
            try:
                api = get_api()
                if api is None:
                    raise RuntimeError("API non initialisée")

                api.annuler_blf(self.blf_id, motif)
                logger.info(
                    "BLF annulé (API) : %s — motif : %s",
                    self._blf["numero_blf"], motif)
                QtWidgets.QMessageBox.information(
                    self, "BLF annulé",
                    "Le BLF a été annulé et le stock a été restauré.")
                self.blf_updated.emit(self.blf_id)
                self._load_data()
                self._refresh()
                return
            except Exception as e:
                logger.exception("Erreur annulation BLF (API)")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible d'annuler le BLF :\n{e}")
                return

        # ═══ MODE AUTONOME / SERVEUR → DB locale ═══
        from Database import audit
        try:
            # ─── Snapshot avant annulation ───
            avant_blf = audit.snapshot(
                "BonLivraison", "id", self.blf_id)

            with db.transaction():
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                db.execute("""
                    UPDATE BonLivraison
                    SET statut = 'ANNULEE',
                        cancelled_by = ?,
                        cancelled_by_name = ?,
                        cancelled_at = ?,
                        motif_annulation = ?
                    WHERE id = ? AND statut = 'VALIDEE'
                """, (self.user_id, self.user_name, now, motif,
                      self.blf_id))

                lignes_db = db.query(
                    """SELECT * FROM LigneBonLivraison
                       WHERE blf_id = ?""",
                    (self.blf_id,))

                for l in lignes_db:
                    code_ref = l["produit_id"]
                    if not code_ref:
                        continue

                    row_p = db.query_one(
                        "SELECT Quantite FROM produits "
                        "WHERE Code_reference = ? LIMIT 1",
                        (code_ref,))
                    if not row_p:
                        continue

                    stock_avant = int(row_p["Quantite"] or 0)
                    stock_apres = max(
                        0, stock_avant - l["quantite"])

                    db.execute("""
                        UPDATE produits SET Quantite = ?
                        WHERE Code_reference = ?
                    """, (stock_apres, code_ref))

                    uid_valide = None
                    if self.user_id:
                        try:
                            if db.query_one(
                                    "SELECT 1 FROM Utilisateur "
                                    "WHERE id = ? LIMIT 1",
                                    (self.user_id,)
                            ):
                                uid_valide = self.user_id
                        except Exception:
                            pass

                    db.execute("""
                        INSERT INTO MouvementStock
                        (id, produit_id, type, quantite,
                         stock_avant, stock_apres, motif, utilisateur_id)
                        VALUES (?,?,?,?,?,?,?,?)
                    """, (db.new_id(), code_ref, "ANNULATION",
                          -l["quantite"], stock_avant, stock_apres,
                          f"Annulation BLF {self._blf['numero_blf']} — "
                          f"{motif}",
                          uid_valide))

                    db.execute("""
                        INSERT INTO AjustementStock
                        (id, Code_reference, Nom_produit,
                         stock_avant, stock_apres, difference,
                         motif, utilisateur_id)
                        VALUES (?,?,?,?,?,?,?,?)
                    """, (db.new_id(), code_ref, l["produit_nom"],
                          stock_avant, stock_apres, -l["quantite"],
                          f"Annulation BLF {self._blf['numero_blf']}",
                          uid_valide))

            # ═══ AUDIT ANNULATION ═══
            try:
                apres_blf = audit.snapshot(
                    "BonLivraison", "id", self.blf_id)

                audit.log(
                    audit.ACTION_ANNULATION_BLF,
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="BonLivraison",
                    cible_id=self.blf_id,
                    cible_nom=self._blf["numero_blf"],
                    details={
                        "motif": motif,
                        "stock_retire": self._blf.get("nb_unites", 0),
                    },
                    avant=avant_blf,
                    apres=apres_blf,
                )
            except Exception:
                logger.exception("Erreur audit annulation BLF")

            logger.info("BLF annulé : %s (motif: %s)",
                        self._blf["numero_blf"], motif)
            QtWidgets.QMessageBox.information(
                self, "BLF annulé",
                "Le BLF a été annulé et le stock a été restauré.")

            self.blf_updated.emit(self.blf_id)
            self._load_data()
            self._refresh()

        except Exception as e:
            logger.exception("Erreur annulation BLF")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'annuler le BLF :\n{e}")