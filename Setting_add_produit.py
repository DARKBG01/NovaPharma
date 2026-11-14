#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_add_produit.py — Dialogue d'ajout de produit
=====================================================
Design inspiré du HTML Nova Pharma :
  - Sidebar avec checklist dynamique + progression
  - Aperçu visuel du code-barre (dans le bon layout)
  - Compteur de caractères sur le nom
  - Calcul auto du prix de vente + totaux en direct
"""

import logging
import re

from PySide6 import QtWidgets, QtGui, QtCore

from Client.api_singleton import get_api, is_client_mode
from Database import db
from Interface_add_produit import Ui_Dialog
from Ui_helpers import fix_all_spinboxes

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════
NAME_MIN_LEN   = 2
NAME_MAX_LEN   = 120
CODE_REF_REGEX = re.compile(r"^[A-Z0-9\-_]{3,20}$")

ICON_CHECK_GRAY = ":/Icon/Icons/circle_white.svg"
ICON_CHECK_DONE = ":/Icon/Icons/check-circle_white.svg"

BARCODE_HINT_TEXT = "L'aperçu du code-barre s'affichera ici…"


# ══════════════════════════════════════════════════════════════════
# Dialogue
# ══════════════════════════════════════════════════════════════════
class Add_produit(QtWidgets.QDialog, Ui_Dialog):

    product_created = QtCore.Signal(str)

    def __init__(self, parent=None, user_id: str = None):
        super().__init__(parent)
        self.setupUi(self)
        fix_all_spinboxes(self)

        # Session
        self.user_id = user_id

        # Catégories
        self._categories = []

        # État
        self._auto_suggested_ref = True
        self._marge = 30.0

        # Init
        self._load_config_defaults()
        self._load_categories()
        self._connect_signals()

        # Code référence initial
        self._suggest_code_reference()
        self._recalc_prix_vente()
        self._update_progress()

        # Initialise l'aperçu code-barre (état vide)
        self._render_barcode("")

        # Focus
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
            rows = db.query(
                "SELECT nom FROM Categorie WHERE actif = 1 ORDER BY nom ASC")
            self._categories = [r["nom"] for r in rows]

            self.input_categorie.clear()
            self.input_categorie.setEditable(True)  # ← AJOUT
            self.input_categorie.setInsertPolicy(  # ← AJOUT
                QtWidgets.QComboBox.NoInsert)
            self.input_categorie.lineEdit().setPlaceholderText(
                "Choisir ou taper une nouvelle catégorie…")

            if self._categories:
                self.input_categorie.addItems(self._categories)
                self.input_categorie.setCurrentIndex(-1)
            else:
                self.input_categorie.addItem("")
                self.input_categorie.setCurrentIndex(0)

            logger.info("Catégories chargées : %d", len(self._categories))
        except Exception:
            logger.exception("Impossible de charger les catégories")
            self.input_categorie.setEditable(True)
            self.input_categorie.clear()
            self.input_categorie.addItem("")

    def _connect_signals(self):
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_gen_ref.clicked.connect(self._on_generate_ref)

        self.input_code_ref.textEdited.connect(self._on_ref_edited)
        self.input_code_barre.textChanged.connect(self._on_barcode_changed)

        self.input_prix_achat.valueChanged.connect(self._recalc_prix_vente)
        self.auto_check.toggled.connect(self._on_auto_toggled)

        self.input_nom.textChanged.connect(self._on_nom_changed)
        self.input_categorie.currentIndexChanged.connect(self._update_progress)
        self.input_quantite.valueChanged.connect(self._recalc_prix_vente)
        self.input_prix_vente.valueChanged.connect(self._recalc_prix_vente)

        self.input_nom.returnPressed.connect(self._on_save)

    def _ensure_categorie(self, nom: str) -> str:
        """
        Vérifie que la catégorie existe, sinon l'insère.
        Retourne le nom nettoyé.

        ⚠️ En mode client : pas d'écriture locale (la catégorie sera
        créée côté serveur quand l'API `create_produit` sera étendue).
        """
        nom = (nom or "").strip()
        if not nom:
            return ""

        # ─── MODE CLIENT → pas d'écriture locale ───
        if is_client_mode():
            return nom.upper()

        # ─── MODE AUTONOME / SERVEUR → DB locale ───
        try:
            row = db.query_one(
                "SELECT nom FROM Categorie "
                "WHERE LOWER(nom) = LOWER(?) AND actif = 1 LIMIT 1",
                (nom,))
            if row:
                return row["nom"]

            db.execute("""
                INSERT INTO Categorie (id, nom, actif, created_at)
                VALUES (?, ?, 1, datetime('now'))
            """, (db.new_id(), nom.upper()))

            logger.info("Nouvelle catégorie créée : %s", nom.upper())
            return nom.upper()
        except Exception:
            logger.exception("Erreur création catégorie %s", nom)
            return nom.upper()

    # ------------------------------------------------------------------
    # Code référence auto
    # ------------------------------------------------------------------
    def _suggest_code_reference(self) -> str:
        try:
            row = db.query_one(
                """SELECT Code_reference FROM produits
                   WHERE Code_reference LIKE 'MED-%'
                   ORDER BY Code_reference DESC LIMIT 1""")
            next_num = 1
            if row:
                try:
                    next_num = int(row["Code_reference"].split("-")[1]) + 1
                except (ValueError, IndexError):
                    next_num = 1
            code = f"MED-{next_num:05d}"
        except Exception:
            logger.exception("Erreur génération code ref")
            code = "MED-00001"

        self.input_code_ref.setText(code)
        return code

    def _on_generate_ref(self):
        self._suggest_code_reference()
        self._auto_suggested_ref = True
        self._update_progress()

    def _on_ref_edited(self, _text):
        self._auto_suggested_ref = False
        self._update_progress()

    # ------------------------------------------------------------------
    # Code-barre preview (CORRIGÉ)
    # ------------------------------------------------------------------
    def _on_barcode_changed(self, text):
        self._render_barcode(text)

    def _render_barcode(self, text: str):
        """
        Dessine l'aperçu du code-barre dans le QFrame `barcode_preview`.
        Utilise directement le layout QHBoxLayout nommé `barcode_preview_layout`.
        """
        layout = self.barcode_preview_layout

        # Vide le layout
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        text = (text or "").strip()

        # Cas vide → affiche un hint
        if not text:
            hint = QtWidgets.QLabel("L'aperçu du code-barre s'affichera ici…")
            hint.setObjectName("barcode_hint")
            hint.setAlignment(QtCore.Qt.AlignCenter)
            hint.setStyleSheet(
                "color: #94a3b8; font-size: 11px; background: transparent;")
            layout.addWidget(hint)
            return

        # Dessine les barres
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
    # Nom (compteur)
    # ------------------------------------------------------------------
    def _on_nom_changed(self, text):
        self.name_counter.setText(f"{len(text)}/{NAME_MAX_LEN}")
        self._update_progress()

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
            qte   = int(self.input_quantite.value())

            total_achat = qte * achat
            total_vente = qte * vente

            self.tot_buy_value.setText(
                f"{total_achat:,.2f} FC".replace(",", " "))
            self.tot_sell_value.setText(
                f"{total_vente:,.2f} FC".replace(",", " "))

            if achat > 0 and vente > 0:
                marge_reelle = (vente - achat) / achat * 100
                self.margin_value.setText(f"{marge_reelle:.2f} %")
            else:
                self.margin_value.setText("—")

            if qte > 0 and achat > 0 and vente > 0:
                benefice = qte * (vente - achat)
                self.profit_value.setText(
                    f"{benefice:,.2f} FC".replace(",", " "))
            else:
                self.profit_value.setText("—")

            self._update_progress()
        except Exception:
            logger.exception("Erreur calcul")

    # ------------------------------------------------------------------
    # Progression + checklist
    # ------------------------------------------------------------------
    def _update_progress(self):
        has_code  = bool(self.input_code_ref.text().strip())
        has_name  = len(self.input_nom.text().strip()) >= NAME_MIN_LEN
        has_cat   = (self.input_categorie.currentIndex() >= 0
                     and not self.input_categorie.currentText().startswith("("))
        has_stock = (self.input_quantite.value() > 0
                     and self.input_prix_achat.value() > 0
                     and self.input_prix_vente.value() > 0)

        self._set_check(self.check_row_code,  self.check_code_icon,  has_code)
        self._set_check(self.check_row_name,  self.check_name_icon,  has_name)
        self._set_check(self.check_row_cat,   self.check_cat_icon,   has_cat)
        self._set_check(self.check_row_stock, self.check_stock_icon, has_stock)

        score = (25 if has_code else 0) + (25 if has_name else 0) \
              + (20 if has_cat else 0) + (30 if has_stock else 0)
        self.progress_bar.setValue(score)
        self.progress_label.setText(f"{score} %")

    @staticmethod
    def _set_check(row: QtWidgets.QFrame,
                   icon: QtWidgets.QLabel,
                   done: bool):
        row.setProperty("done", "true" if done else "false")
        row.style().unpolish(row)
        row.style().polish(row)

        icon.setPixmap(
            QtGui.QPixmap(ICON_CHECK_DONE if done else ICON_CHECK_GRAY))

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def _validate(self):
        code = self.input_code_ref.text().strip().upper()
        if not code:
            return False, "Le code référence est obligatoire."
        if not CODE_REF_REGEX.match(code):
            return False, "Code référence invalide (3-20 car., A-Z 0-9 - _)."
        try:
            if db.query_one(
                "SELECT 1 FROM produits WHERE Code_reference = ? LIMIT 1",
                (code,)
            ):
                return False, f"Le code '{code}' existe déjà."
        except Exception:
            logger.exception("Erreur verif code")
            return False, "Erreur de vérification."

        nom = self.input_nom.text().strip()
        if len(nom) < NAME_MIN_LEN:
            return False, "Le nom du produit est trop court."
        try:
            if db.query_one(
                "SELECT 1 FROM produits WHERE LOWER(Nom) = LOWER(?) LIMIT 1",
                (nom,)
            ):
                return False, f"Un produit nommé '{nom}' existe déjà."
        except Exception:
            logger.exception("Erreur verif nom")

        cat = self.input_categorie.currentText().strip()
        if not cat:
            return False, "Choisissez ou saisissez une catégorie."
        if len(cat) < 2:
            return False, "Catégorie trop courte (2 caractères min)."

        unite = self.input_unite.currentText().strip()
        if not unite:
            return False, "Sélectionnez une unité."

        if self.input_quantite.value() <= 0:
            return False, "La quantité doit être supérieure à 0."
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

        code       = self.input_code_ref.text().strip().upper()
        nom        = self.input_nom.text().strip()
        code_barre = self.input_code_barre.text().strip() or None
        categorie  = self._ensure_categorie(self.input_categorie.currentText())
        unite      = self.input_unite.currentText().strip()
        quantite   = self.input_quantite.value()
        prix_achat = float(self.input_prix_achat.value())
        prix_vente = float(self.input_prix_vente.value())

        # ═══ MODE CLIENT → API ═══
        if is_client_mode():
            try:
                api = get_api()
                data = {
                    "Code_reference": code,
                    "Nom": nom,
                    "Code_barre": code_barre,
                    "Categorie": categorie,
                    "Unite": unite,
                    "Quantite": quantite,
                    "Prix_achat": prix_achat,
                    "Prix_vente": prix_vente,
                    "Prix_unitaire": prix_vente,
                }
                result = api.create_produit(data)
                new_code = result.get("Code_reference", code)

                logger.info("Produit créé (API) : %s (%s)", nom, new_code)
                self.product_created.emit(new_code)
                QtWidgets.QMessageBox.information(
                    self, "Produit ajouté",
                    f"Le produit « {nom} » a été créé avec succès.")
                self.accept()
                return
            except Exception as e:
                logger.exception("Échec création produit (API)")
                self._show_error(f"Erreur d'enregistrement : {e}")
                return

        # ═══ MODE AUTONOME / SERVEUR → DB locale ═══
        try:
            with db.transaction():
                db.execute(
                    """INSERT INTO produits
                       (Code_reference, Nom, Code_barre, Categorie,
                        Unite, Quantite_initiale, Quantite,
                        Prix_achat, Prix_vente, Prix_unitaire,
                        Cree_par, Date_ajout)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?, datetime('now'))""",
                    (code, nom, code_barre, categorie,
                     unite, quantite, quantite,
                     prix_achat, prix_vente, prix_vente,
                     self.user_id))

                if quantite > 0:
                    db.execute(
                        """INSERT INTO MouvementStock
                           (id, produit_id, type, quantite,
                            stock_avant, stock_apres, motif, utilisateur_id)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (db.new_id(), code, "ENTREE", quantite,
                         0, quantite, "Stock initial", self.user_id))

            # ═══ AUDIT COMPLET ═══
            try:
                from Database import audit
                apres = audit.snapshot(
                    "produits", "Code_reference", code)
                audit.log(
                    audit.ACTION_CREATION_PRODUIT,
                    utilisateur_id=self.user_id,
                    cible_type="produits",
                    cible_id=code,
                    cible_nom=nom,
                    details={
                        "categorie": categorie,
                        "quantite_initiale": quantite,
                        "prix_achat": prix_achat,
                        "prix_vente": prix_vente,
                    },
                    apres=apres,
                )
            except Exception:
                logger.exception("Erreur audit création produit")

            logger.info("Produit créé : %s (%s)", nom, code)
            self.product_created.emit(code)
            QtWidgets.QMessageBox.information(
                self, "Produit ajouté",
                f"Le produit « {nom} » a été créé avec succès.")
            self.accept()
        except Exception as e:
            logger.exception("Échec création produit")
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

    dlg = Add_produit(user_id="TEST")
    dlg.product_created.connect(lambda c: print(f"→ Créé : {c}"))
    sys.exit(dlg.exec())