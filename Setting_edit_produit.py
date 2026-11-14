#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_edit_produit.py — Dialogue de modification de produit
==============================================================
Fonctionnalités :
  - Charge les infos du produit sélectionné
  - Code référence en lecture seule (PK)
  - Modification : Nom, Code-barre, Catégorie, Unité, Description
  - Modification des prix avec recalcul auto
  - Ajustement du stock tracé dans `AjustementStock`
  - Historique des 10 derniers ajustements
"""

import logging
import re

from PySide6 import QtWidgets, QtGui, QtCore

from Client.api_singleton import is_client_mode, get_api
from Database import db
from Interface_edit_produit import Ui_Dialog

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════
NAME_MIN_LEN   = 2
NAME_MAX_LEN   = 120
CODE_REF_REGEX = re.compile(r"^[A-Z0-9\-_]{3,20}$")

ICON_CHECK_GRAY = ":/Icon/Icons/circle_white.svg"
ICON_CHECK_DONE = ":/Icon/Icons/check-circle_white.svg"

BARCODE_HINT = "L'aperçu du code-barre s'affichera ici…"

MOTIFS_FIXES = {
    "Réception fournisseur",
    "Retour client",
    "Correction inventaire",
    "Casse / Périmé",
    "Don / Échantillon",
    "Autre",
}


# ══════════════════════════════════════════════════════════════════
# Dialogue
# ══════════════════════════════════════════════════════════════════
class Edit_produit(QtWidgets.QDialog, Ui_Dialog):

    product_updated = QtCore.Signal(str)  # Code_reference

    def __init__(self, parent=None, code_reference: str = None, user_id: str = None):
        super().__init__(parent)
        self.setupUi(self)

        self.code_reference = code_reference
        self.user_id = user_id

        # État
        self._produit = None
        self._stock_initial = 0
        self._marge = 30.0

        # Init
        self._load_config_defaults()
        self._load_categories()
        self._load_produit()
        self._connect_signals()
        self._load_historique_ajustements()

        self._refresh_ui()
        self._update_progress()

        # Focus sur le nom
        self.input_nom.setFocus()

    # ------------------------------------------------------------------
    # Chargement
    # ------------------------------------------------------------------
    def _load_config_defaults(self):
        try:
            indice = db.get_config("indice_vente", 0.30)
            marge = float(indice) * 100 if float(indice) <= 1 else float(indice)
        except Exception:
            marge = 30.0
            logger.exception("Impossible de charger la marge par défaut")
        self._marge = marge
        self.auto_hint.setText(f"Marge : {marge:.1f} %")

    def _load_categories(self):
        try:
            cats = []
            if is_client_mode():
                api = get_api()
                if api is not None:
                    data = api.list_categories()
                    cats = [r["nom"] for r in data.get("items", [])]
            else:
                rows = db.query(
                    "SELECT nom FROM Categorie WHERE actif = 1 "
                    "ORDER BY nom ASC")
                cats = [r["nom"] for r in rows]

            self.input_categorie.clear()
            if cats:
                self.input_categorie.addItems(cats)
            else:
                self.input_categorie.addItem("(aucune catégorie)")
        except Exception:
            logger.exception("Impossible de charger les catégories")
            self.input_categorie.addItem("(erreur)")

    def _load_produit(self):
        if not self.code_reference:
            self._produit = None
            return
        try:
            if is_client_mode():
                api = get_api()
                if api is None:
                    self._produit = None
                    return
                data = api.get_produit(self.code_reference)
                self._produit = data
            else:
                row = db.query_one(
                    """SELECT Code_reference, Nom, Code_barre, Categorie,
                              Description, Unite, Quantite, Quantite_initiale,
                              Prix_achat, Prix_vente, Prix_unitaire, Date_ajout
                       FROM produits WHERE Code_reference = ? LIMIT 1""",
                    (self.code_reference,))
                self._produit = dict(row) if row else None

            if self._produit:
                self._stock_initial = int(
                    self._produit.get("Quantite") or 0)
        except Exception:
            logger.exception("Erreur chargement produit")
            self._produit = None

    def _load_historique_ajustements(self):
        """Charge les 10 derniers ajustements (API non disponible)."""
        # ─── Mode client : pas d'API dédiée ───
        if is_client_mode():
            self.table_ajustements.setRowCount(1)
            it = QtWidgets.QTableWidgetItem(
                "Historique non disponible en mode client")
            it.setTextAlignment(QtCore.Qt.AlignCenter)
            it.setForeground(QtGui.QColor("#94a3b8"))
            f = QtGui.QFont("Segoe UI", 10)
            f.setItalic(True)
            it.setFont(f)
            self.table_ajustements.setItem(0, 0, it)
            self.table_ajustements.setSpan(
                0, 0, 1, self.table_ajustements.columnCount())
            return

        # ─── Mode local ───
        try:
            rows = db.query(
                """SELECT date_ajustement, difference, motif, stock_apres
                   FROM AjustementStock
                   WHERE Code_reference = ?
                   ORDER BY date_ajustement DESC
                   LIMIT 10""",
                (self.code_reference,))
            self.table_ajustements.setRowCount(len(rows))
            for i, r in enumerate(rows):
                diff = int(r["difference"])
                if diff > 0:
                    diff_str = f"+{diff}"
                    color = "#16a34a"
                elif diff < 0:
                    diff_str = str(diff)
                    color = "#dc2626"
                else:
                    diff_str = "0"
                    color = "#64748b"

                items = [
                    QtWidgets.QTableWidgetItem(str(r["date_ajustement"])),
                    QtWidgets.QTableWidgetItem(diff_str),
                    QtWidgets.QTableWidgetItem(str(r["motif"] or "")),
                    QtWidgets.QTableWidgetItem(str(r["stock_apres"])),
                ]
                items[1].setForeground(QtGui.QColor(color))
                for c, item in enumerate(items):
                    self.table_ajustements.setItem(i, c, item)
        except Exception:
            logger.exception("Erreur chargement historique ajustements")

    # ------------------------------------------------------------------
    # Signaux
    # ------------------------------------------------------------------
    def _connect_signals(self):
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_quick_add.clicked.connect(self._on_quick_add)
        self.btn_quick_sub.clicked.connect(self._on_quick_sub)

        self.input_code_barre.textChanged.connect(self._on_barcode_changed)
        self.input_nom.textChanged.connect(self._on_nom_changed)
        self.input_categorie.currentIndexChanged.connect(self._update_progress)
        self.input_unite.currentIndexChanged.connect(self._update_progress)

        self.input_prix_achat.valueChanged.connect(self._recalc_prix_vente)
        self.input_prix_vente.valueChanged.connect(self._recalc_prix_vente)
        self.auto_check.toggled.connect(self._on_auto_toggled)

        self.input_new_quantite.valueChanged.connect(self._on_quantite_changed)

        self.input_nom.returnPressed.connect(self._on_save)

    # ------------------------------------------------------------------
    # Remplissage des champs
    # ------------------------------------------------------------------
    def _refresh_ui(self):
        """Remplit l'UI avec les données du produit."""
        if not self._produit:
            self.info_value.setText("—")
            self.info_code.setText("—")
            return

        p = self._produit
        self.info_value.setText(p.get("Nom", "—"))
        self.info_code.setText(p.get("Code_reference", "—"))

        # Code référence (lecture seule)
        self.input_code_ref.setText(p.get("Code_reference", ""))
        self.input_code_barre.setText(p.get("Code_barre") or "")
        self.input_nom.setText(p.get("Nom") or "")
        self.input_description.setText(p.get("Description") or "")

        # Catégorie
        cat = p.get("Categorie") or ""
        idx = self.input_categorie.findText(cat)
        if idx >= 0:
            self.input_categorie.setCurrentIndex(idx)

        # Unité
        unite = p.get("Unite") or "pièce"
        idx_u = self.input_unite.findText(unite)
        if idx_u >= 0:
            self.input_unite.setCurrentIndex(idx_u)

        # Prix
        self.input_prix_achat.setValue(float(p.get("Prix_achat") or 0))
        self.input_prix_vente.setValue(float(p.get("Prix_vente") or 0))

        # Stock
        stock = int(p.get("Quantite") or 0)
        self.stock_current_value.setText(str(stock))
        self.input_new_quantite.setValue(stock)
        self.stock_new_value.setText(str(stock))
        self._update_diff_display(stock - stock)

        # Compteur nom
        self.name_counter.setText(f"{len(self.input_nom.text())}/{NAME_MAX_LEN}")

        # Aperçu code-barre
        self._render_barcode(self.input_code_barre.text())

        # Prix vente (recalcul si auto)
        self._recalc_prix_vente()

    # ------------------------------------------------------------------
    # Code-barre
    # ------------------------------------------------------------------
    def _on_barcode_changed(self, text):
        self._render_barcode(text)

    def _render_barcode(self, text: str):
        layout = self.barcode_preview_layout
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        text = (text or "").strip()
        if not text:
            hint = QtWidgets.QLabel(BARCODE_HINT)
            hint.setObjectName("barcode_hint")
            hint.setAlignment(QtCore.Qt.AlignCenter)
            hint.setStyleSheet(
                "color: #94a3b8; font-size: 11px; background: transparent;")
            layout.addWidget(hint)
            return

        for ch in text[:48]:
            width = (ord(ch) % 4) + 1
            bar = QtWidgets.QFrame()
            bar.setFixedWidth(width)
            bar.setFixedHeight(26)
            bar.setStyleSheet(
                "background-color: #023E8A; border: none; border-radius: 0;")
            layout.addWidget(bar)
        layout.addStretch()

    # ------------------------------------------------------------------
    # Nom
    # ------------------------------------------------------------------
    def _on_nom_changed(self, text):
        self.name_counter.setText(f"{len(text)}/{NAME_MAX_LEN}")
        self._update_progress()

    # ------------------------------------------------------------------
    # Quantité
    # ------------------------------------------------------------------
    def _on_quick_add(self):
        self.input_new_quantite.setValue(self.input_new_quantite.value() + 1)

    def _on_quick_sub(self):
        self.input_new_quantite.setValue(max(0, self.input_new_quantite.value() - 1))

    def _on_quantite_changed(self, val):
        self.stock_new_value.setText(str(val))
        self._update_diff_display(val - self._stock_initial)
        self._update_progress()

    def _update_diff_display(self, diff: int):
        self.stock_diff_value.setText(f"{diff:+d}" if diff != 0 else "0")
        if diff > 0:
            direction = "up"
        elif diff < 0:
            direction = "down"
        else:
            direction = "same"
        self.stock_diff_value.setProperty("direction", direction)
        self.stock_diff_value.style().unpolish(self.stock_diff_value)
        self.stock_diff_value.style().polish(self.stock_diff_value)

    # ------------------------------------------------------------------
    # Calcul auto
    # ------------------------------------------------------------------
    def _on_auto_toggled(self, checked):
        self.auto_box.setProperty("on", "true" if checked else "false")
        self.auto_box.style().unpolish(self.auto_box)
        self.auto_box.style().polish(self.auto_box)

        self.input_prix_vente.setReadOnly(checked)
        if checked:
            self._recalc_prix_vente()

    def _recalc_prix_vente(self):
        try:
            achat = float(self.input_prix_achat.value())
            if self.auto_check.isChecked():
                vente = round(achat * (1 + self._marge / 100.0), 2)
                self.input_prix_vente.blockSignals(True)
                self.input_prix_vente.setValue(vente)
                self.input_prix_vente.blockSignals(False)

            vente = float(self.input_prix_vente.value())

            if achat > 0 and vente > 0:
                marge_reelle = (vente - achat) / achat * 100
                self.margin_value.setText(f"{marge_reelle:.2f} %")
            else:
                self.margin_value.setText("—")

            if achat > 0 and vente > 0:
                benefice = vente - achat
                self.profit_value.setText(f"{benefice:,.2f} FC".replace(",", " "))
            else:
                self.profit_value.setText("—")

            self._update_progress()
        except Exception:
            logger.exception("Erreur calcul")

    # ------------------------------------------------------------------
    # Progression
    # ------------------------------------------------------------------
    def _update_progress(self):
        has_name  = len(self.input_nom.text().strip()) >= NAME_MIN_LEN
        has_cat   = (self.input_categorie.currentIndex() >= 0
                     and not self.input_categorie.currentText().startswith("("))
        has_prix  = (self.input_prix_achat.value() > 0
                     and self.input_prix_vente.value() > 0
                     and self.input_prix_vente.value() >= self.input_prix_achat.value())
        has_stock = self.input_new_quantite.value() >= 0

        self._set_check(self.check_row_name,  self.check_name_icon,  has_name)
        self._set_check(self.check_row_cat,   self.check_cat_icon,   has_cat)
        self._set_check(self.check_row_prix,  self.check_prix_icon,  has_prix)
        self._set_check(self.check_row_stock, self.check_stock_icon, has_stock)

        score = (25 if has_name else 0) + (25 if has_cat else 0) \
              + (25 if has_prix else 0) + (25 if has_stock else 0)
        self.progress_bar.setValue(score)
        self.progress_label.setText(f"{score} %")

    @staticmethod
    def _set_check(row: QtWidgets.QFrame,
                   icon: QtWidgets.QLabel,
                   done: bool):
        row.setProperty("done", "true" if done else "false")
        row.style().unpolish(row)
        row.style().polish(row)
        icon.setPixmap(QtGui.QPixmap(ICON_CHECK_DONE if done else ICON_CHECK_GRAY))

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def _validate(self):
        if not self._produit:
            return False, "Produit introuvable."

        nom = self.input_nom.text().strip()
        if len(nom) < NAME_MIN_LEN:
            return False, "Le nom du produit est trop court."
        if len(nom) > NAME_MAX_LEN:
            return False, f"Le nom ne doit pas dépasser {NAME_MAX_LEN} caractères."

        # Unicité (sauf ce produit)
        try:
            if db.query_one(
                """SELECT 1 FROM produits
                   WHERE LOWER(Nom) = LOWER(?)
                     AND Code_reference <> ? LIMIT 1""",
                (nom, self.code_reference)
            ):
                return False, f"Un autre produit s'appelle déjà '{nom}'."
        except Exception:
            logger.exception("Erreur verif nom")

        cat = self.input_categorie.currentText().strip()
        if not cat or cat.startswith("("):
            return False, "Sélectionnez une catégorie."

        unite = self.input_unite.currentText().strip()
        if not unite:
            return False, "Sélectionnez une unité."

        if self.input_prix_achat.value() <= 0:
            return False, "Le prix d'achat doit être supérieur à 0."
        if self.input_prix_vente.value() <= 0:
            return False, "Le prix de vente doit être supérieur à 0."
        if self.input_prix_vente.value() < self.input_prix_achat.value():
            return False, "Le prix de vente doit être ≥ au prix d'achat."

        return True, ""

    def _show_error(self, msg: str):
        self.label_error.setText(f"⚠  {msg}")
        self.label_error.setVisible(True)

    def _hide_error(self):
        self.label_error.setVisible(False)
        self.label_error.setText("")

    # ------------------------------------------------------------------
    # Enregistrement
    # ------------------------------------------------------------------
    def _on_save(self):
        self._hide_error()

        valide, msg = self._validate()
        if not valide:
            self._show_error(msg)
            return

        nom          = self.input_nom.text().strip()
        code_barre   = self.input_code_barre.text().strip() or None
        categorie    = self.input_categorie.currentText().strip()
        unite        = self.input_unite.currentText().strip()
        description  = self.input_description.text().strip() or None
        prix_achat   = float(self.input_prix_achat.value())
        prix_vente   = float(self.input_prix_vente.value())
        new_quantite = int(self.input_new_quantite.value())
        motif        = self.input_motif.currentText().strip()

        diff_qte = new_quantite - self._stock_initial

        # ═══════════════════════════════════════════════════════════
        # MODE CLIENT → API
        # ═══════════════════════════════════════════════════════════
        if is_client_mode():
            try:
                api = get_api()
                if api is None:
                    raise RuntimeError("API non initialisée")

                data = {
                    "Nom": nom,
                    "Code_barre": code_barre,
                    "Categorie": categorie,
                    "Description": description,
                    "Unite": unite,
                    "Quantite": new_quantite,
                    "Prix_achat": prix_achat,
                    "Prix_vente": prix_vente,
                    "Prix_unitaire": prix_vente,
                }
                api.update_produit(self.code_reference, data)

                logger.info(
                    "Produit modifié (API) : %s (diff stock: %+d)",
                    self.code_reference, diff_qte)
                self.product_updated.emit(self.code_reference)
                QtWidgets.QMessageBox.information(
                    self, "Produit modifié",
                    f"Les modifications du produit « {nom} » ont été "
                    "enregistrées.")
                self.accept()
                return
            except Exception as e:
                logger.exception("Échec modification produit (API)")
                self._show_error(f"Erreur d'enregistrement : {e}")
                return

        # ═══════════════════════════════════════════════════════════
        # MODE LOCAL (code existant)
        # ═══════════════════════════════════════════════════════════
        try:
            from Database import audit
            avant = audit.snapshot(
                "produits", "Code_reference", self.code_reference)

            with db.transaction():
                db.execute(
                    """UPDATE produits
                       SET Nom = ?, Code_barre = ?, Categorie = ?,
                           Description = ?, Unite = ?,
                           Quantite = ?, Prix_achat = ?, Prix_vente = ?,
                           Prix_unitaire = ?
                       WHERE Code_reference = ?""",
                    (nom, code_barre, categorie,
                     description, unite,
                     new_quantite, prix_achat, prix_vente,
                     prix_vente, self.code_reference))

                if diff_qte != 0:
                    db.execute(
                        """INSERT INTO AjustementStock
                           (id, Code_reference, Nom_produit,
                            stock_avant, stock_apres, difference,
                            motif, utilisateur_id)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (db.new_id(), self.code_reference, nom,
                         self._stock_initial, new_quantite, diff_qte,
                         motif, self.user_id))

                    db.execute(
                        """INSERT INTO MouvementStock
                           (id, produit_id, type, quantite,
                            stock_avant, stock_apres, motif, utilisateur_id)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (db.new_id(), self.code_reference, "AJUSTEMENT",
                         diff_qte, self._stock_initial, new_quantite,
                         motif, self.user_id))

            # ═══ AUDIT COMPLET (avec diff auto) ═══
            try:
                audit.trace_modif(
                    audit.ACTION_MODIF_PRODUIT,
                    table="produits",
                    id_column="Code_reference",
                    id_value=self.code_reference,
                    avant_snapshot=avant,
                    utilisateur_id=self.user_id,
                    cible_nom=nom,
                    details={"motif_stock": motif} if diff_qte else None,
                )

                # Trace spécifique prix changé (sensible)
                if avant:
                    old_pv = avant.get("Prix_vente") or 0
                    if float(old_pv) != float(prix_vente):
                        audit.log(
                            audit.ACTION_MODIF_PRIX,
                            utilisateur_id=self.user_id,
                            cible_type="produits",
                            cible_id=self.code_reference,
                            cible_nom=nom,
                            details={
                                "ancien_prix": old_pv,
                                "nouveau_prix": prix_vente,
                            })

                    old_pa = avant.get("Prix_achat") or 0
                    if float(old_pa) != float(prix_achat):
                        audit.log(
                            audit.ACTION_MODIF_PRIX_ACHAT,
                            utilisateur_id=self.user_id,
                            cible_type="produits",
                            cible_id=self.code_reference,
                            cible_nom=nom,
                            details={
                                "ancien_prix_achat": old_pa,
                                "nouveau_prix_achat": prix_achat,
                            })

                # Ajustement de stock manuel
                if diff_qte != 0:
                    audit.log(
                        audit.ACTION_MODIF_STOCK_MANUEL,
                        utilisateur_id=self.user_id,
                        cible_type="produits",
                        cible_id=self.code_reference,
                        cible_nom=nom,
                        details={
                            "stock_avant": self._stock_initial,
                            "stock_apres": new_quantite,
                            "difference": diff_qte,
                            "motif": motif,
                        })
            except Exception:
                logger.exception("Erreur audit modification produit")

            logger.info("Produit modifié : %s (diff stock: %+d)",
                        self.code_reference, diff_qte)
            self.product_updated.emit(self.code_reference)
            QtWidgets.QMessageBox.information(
                self, "Produit modifié",
                f"Les modifications du produit « {nom} » ont été "
                "enregistrées.")
            self.accept()
        except Exception as e:
            logger.exception("Échec modification produit")
            self._show_error(f"Erreur d'enregistrement : {e}")


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

    # Récupère le premier produit existant pour le test
    row = db.query_one("SELECT Code_reference FROM produits LIMIT 1")
    if not row:
        print("⚠ Aucun produit à éditer. Créez-en un d'abord.")
        sys.exit(0)

    dlg = Edit_produit(code_reference=row["Code_reference"], user_id="TEST")
    dlg.product_updated.connect(lambda c: print(f"→ Modifié : {c}"))
    sys.exit(dlg.exec())