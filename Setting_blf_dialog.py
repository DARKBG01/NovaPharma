#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_blf_dialog.py — Création d'un Bon de Livraison Fournisseur
====================================================================
Utilise Interface_blf_dialog.py (généré depuis Setting_blf_dialog.ui)

- Sélection fournisseur (ou "Sans fournisseur")
- Ajout de produits + quantités
- Prix achat / vente modifiables
- Aperçu du total
- Enregistrement en BROUILLON ou VALIDATION directe
"""

import logging
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import get_api, is_client_mode
from Database import db
from Interface_blf_dialog import Ui_Dialog
from Ui_helpers import setup_blf_dialog_table

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Widget ligne produit (widget custom inséré dynamiquement)
# ══════════════════════════════════════════════════════════════════
class LigneBLFWidget(QtWidgets.QFrame):
    """Une ligne de produit dans le BLF."""

    removed = QtCore.Signal(str)  # code_ref

    def __init__(self, produit_nom: str, code_ref: str,
                 prix_achat: float, prix_vente: float, parent=None):
        super().__init__(parent)
        self.produit_nom = produit_nom
        self.code_ref = code_ref

        self.setObjectName("ligne_blf")
        self.setFixedHeight(60)
        self.setStyleSheet("""
            QFrame#ligne_blf {
                background-color: #f8fafc;
                border: 1px solid #e6ebf2;
                border-radius: 12px;
            }
            QFrame#ligne_blf:hover { border-color: #bae6fd; }
        """)

        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(14, 8, 14, 8)
        h.setSpacing(12)

        # Nom + code
        v = QtWidgets.QVBoxLayout()
        v.setSpacing(0)

        lbl_nom = QtWidgets.QLabel(produit_nom)
        lbl_nom.setStyleSheet(
            "color: #0f172a; font-size: 13px; font-weight: 700; "
            "background: transparent;")
        v.addWidget(lbl_nom)

        lbl_ref = QtWidgets.QLabel(code_ref)
        lbl_ref.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-weight: 600; "
            "background: transparent; font-family: Courier New;")
        v.addWidget(lbl_ref)

        h.addLayout(v, 1)

        # Quantité
        v_q = QtWidgets.QVBoxLayout()
        v_q.setSpacing(2)
        lbl_q = QtWidgets.QLabel("Qté")
        lbl_q.setStyleSheet(
            "color: #64748b; font-size: 10px; font-weight: 700; "
            "background: transparent;")
        lbl_q.setAlignment(Qt.AlignCenter)
        v_q.addWidget(lbl_q)

        self.spin_qte = QtWidgets.QSpinBox()
        self.spin_qte.setRange(1, 1000000)
        self.spin_qte.setValue(1)
        self.spin_qte.setFixedWidth(80)
        self.spin_qte.setAlignment(Qt.AlignCenter)
        self.spin_qte.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.spin_qte.setStyleSheet("""
            QSpinBox {
                background-color: #ffffff;
                border: 1.5px solid #dbe3ec;
                border-radius: 8px;
                padding: 6px;
                color: #0077B6;
                font-size: 13px;
                font-weight: 800;
            }
            QSpinBox:focus { border-color: #0077B6; }
        """)
        v_q.addWidget(self.spin_qte)
        h.addLayout(v_q)

        # Prix achat
        v_pa = QtWidgets.QVBoxLayout()
        v_pa.setSpacing(2)
        lbl_pa = QtWidgets.QLabel("Prix achat")
        lbl_pa.setStyleSheet(
            "color: #64748b; font-size: 10px; font-weight: 700; "
            "background: transparent;")
        lbl_pa.setAlignment(Qt.AlignCenter)
        v_pa.addWidget(lbl_pa)

        self.spin_pa = QtWidgets.QDoubleSpinBox()
        self.spin_pa.setRange(0, 999999999.99)
        self.spin_pa.setDecimals(2)
        self.spin_pa.setValue(prix_achat)
        self.spin_pa.setFixedWidth(110)
        self.spin_pa.setAlignment(Qt.AlignCenter)
        self.spin_pa.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.spin_pa.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #ffffff;
                border: 1.5px solid #dbe3ec;
                border-radius: 8px;
                padding: 6px;
                color: #0f172a;
                font-size: 12px;
                font-weight: 700;
            }
            QDoubleSpinBox:focus { border-color: #0077B6; }
        """)
        v_pa.addWidget(self.spin_pa)
        h.addLayout(v_pa)

        # Prix vente
        v_pv = QtWidgets.QVBoxLayout()
        v_pv.setSpacing(2)
        lbl_pv = QtWidgets.QLabel("Prix vente")
        lbl_pv.setStyleSheet(
            "color: #64748b; font-size: 10px; font-weight: 700; "
            "background: transparent;")
        lbl_pv.setAlignment(Qt.AlignCenter)
        v_pv.addWidget(lbl_pv)

        self.spin_pv = QtWidgets.QDoubleSpinBox()
        self.spin_pv.setRange(0, 999999999.99)
        self.spin_pv.setDecimals(2)
        self.spin_pv.setValue(prix_vente)
        self.spin_pv.setFixedWidth(110)
        self.spin_pv.setAlignment(Qt.AlignCenter)
        self.spin_pv.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.spin_pv.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #ffffff;
                border: 1.5px solid #dbe3ec;
                border-radius: 8px;
                padding: 6px;
                color: #16A34A;
                font-size: 12px;
                font-weight: 700;
            }
            QDoubleSpinBox:focus { border-color: #16A34A; }
        """)
        v_pv.addWidget(self.spin_pv)
        h.addLayout(v_pv)

        # Total
        v_t = QtWidgets.QVBoxLayout()
        v_t.setSpacing(2)
        lbl_t = QtWidgets.QLabel("Total")
        lbl_t.setStyleSheet(
            "color: #64748b; font-size: 10px; font-weight: 700; "
            "background: transparent;")
        lbl_t.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        v_t.addWidget(lbl_t)

        self.lbl_total = QtWidgets.QLabel("0 FC")
        self.lbl_total.setStyleSheet(
            "color: #0077B6; font-size: 13px; font-weight: 800; "
            "background: transparent;")
        self.lbl_total.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_total.setFixedWidth(100)
        v_t.addWidget(self.lbl_total)
        h.addLayout(v_t)

        # Bouton supprimer
        self.btn_del = QtWidgets.QPushButton()
        self.btn_del.setFixedSize(32, 32)
        self.btn_del.setCursor(Qt.PointingHandCursor)
        self.btn_del.setIcon(QtGui.QIcon(":/Icon/Icons/trash.svg"))
        self.btn_del.setIconSize(QtCore.QSize(16, 16))
        self.btn_del.setStyleSheet("""
            QPushButton {
                background-color: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #fee2e2; }
        """)
        self.btn_del.clicked.connect(
            lambda: self.removed.emit(self.code_ref))
        h.addWidget(self.btn_del)

        # Recalcul
        self.spin_qte.valueChanged.connect(self._recalc_total)
        self.spin_pa.valueChanged.connect(self._recalc_total)
        self._recalc_total()

    def _recalc_total(self):
        total = self.spin_qte.value() * self.spin_pa.value()
        self.lbl_total.setText(f"{total:,.0f} FC".replace(",", " "))

    def get_data(self) -> dict:
        return {
            "produit_nom": self.produit_nom,
            "code_ref": self.code_ref,
            "quantite": self.spin_qte.value(),
            "prix_achat": self.spin_pa.value(),
            "prix_vente": self.spin_pv.value(),
            "total_ligne": self.spin_qte.value() * self.spin_pa.value(),
        }


# ══════════════════════════════════════════════════════════════════
# Dialogue principal
# ══════════════════════════════════════════════════════════════════
class Setting_blf_dialog(QtWidgets.QDialog, Ui_Dialog):

    blf_created = QtCore.Signal(str)  # blf_id

    def __init__(self, parent=None, user_id: str = None,
                 user_name: str = "", fournisseur_id: str = None):
        super().__init__(parent)
        self.setupUi(self)
        setup_blf_dialog_table(self.table_produits)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.fournisseur_id = fournisseur_id

        self._lignes = {}          # {code_ref: LigneBLFWidget}
        self._produits_cache = []  # Liste des produits

        # Layout des lignes — pointe vers celui du .ui
        self.scroll_layout = self.verticalLayout_lignes

        # Init
        self._load_produits()
        self._load_fournisseurs()
        self._connect_signals()
        self._update_header()

        if self.fournisseur_id:
            self._preselect_fournisseur()

        self._recalc_total()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        self.search_produit.textChanged.connect(self._filter_produits)
        self.table_produits.cellDoubleClicked.connect(self._add_ligne)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_draft.clicked.connect(lambda: self._save(validate=False))
        self.btn_validate.clicked.connect(lambda: self._save(validate=True))

    def _update_header(self):
        """Met à jour le sous-titre du header."""
        self.blf_header_subtitle.setText(
            f"Créé par {self.user_name} — "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # ══════════════════════════════════════════════════════════════
    def _load_produits(self):
        try:
            rows = db.query("""
                SELECT Code_reference, Nom, Quantite, Prix_achat, Prix_vente
                FROM produits WHERE actif = 1 ORDER BY Nom ASC
            """)
            self._produits_cache = [dict(r) for r in rows]

            self.table_produits.setRowCount(len(self._produits_cache))
            for i, p in enumerate(self._produits_cache):
                item0 = QtWidgets.QTableWidgetItem(p["Code_reference"])
                item0.setFont(QtGui.QFont("Courier New", 9))
                item0.setForeground(QtGui.QColor("#94a3b8"))
                self.table_produits.setItem(i, 0, item0)

                item1 = QtWidgets.QTableWidgetItem(p["Nom"])
                item1.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                self.table_produits.setItem(i, 1, item1)

                q = int(p["Quantite"] or 0)
                item2 = QtWidgets.QTableWidgetItem(str(q))
                color = "#16A34A" if q > 50 else "#F4A261" if q > 20 else "#DC2626"
                item2.setForeground(QtGui.QColor(color))
                item2.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                item2.setTextAlignment(Qt.AlignCenter)
                self.table_produits.setItem(i, 2, item2)

                item3 = QtWidgets.QTableWidgetItem(
                    f"{float(p['Prix_achat'] or 0):.0f} FC")
                item3.setForeground(QtGui.QColor("#0f172a"))
                item3.setTextAlignment(Qt.AlignCenter)
                self.table_produits.setItem(i, 3, item3)

            setup_blf_dialog_table(self.table_produits)

        except Exception:
            logger.exception("Erreur chargement produits")

    def _load_fournisseurs(self):
        try:
            self.combo_fournisseur.clear()
            self.combo_fournisseur.addItem("Sans fournisseur", None)

            rows = db.query("""
                SELECT Id_fournisseur, Entreprise
                FROM Fournisseur ORDER BY Entreprise ASC
            """)
            for r in rows:
                self.combo_fournisseur.addItem(
                    r["Entreprise"], r["Id_fournisseur"])
        except Exception:
            logger.exception("Erreur chargement fournisseurs")

    def _preselect_fournisseur(self):
        for i in range(self.combo_fournisseur.count()):
            if self.combo_fournisseur.itemData(i) == self.fournisseur_id:
                self.combo_fournisseur.setCurrentIndex(i)
                break

    def _filter_produits(self, text):
        text = text.lower().strip()
        for i in range(self.table_produits.rowCount()):
            match = False
            for c in (0, 1):
                item = self.table_produits.item(i, c)
                if item and text in item.text().lower():
                    match = True
                    break
            self.table_produits.setRowHidden(i, not match)

    # ══════════════════════════════════════════════════════════════
    def _add_ligne(self, row, col):
        try:
            code_ref = self.table_produits.item(row, 0).text()
            nom = self.table_produits.item(row, 1).text()

            # Déjà présent → incrémente la quantité
            if code_ref in self._lignes:
                self._lignes[code_ref].spin_qte.setValue(
                    self._lignes[code_ref].spin_qte.value() + 1)
                return

            p = next((x for x in self._produits_cache
                      if x["Code_reference"] == code_ref), None)
            if not p:
                return

            ligne = LigneBLFWidget(
                nom, code_ref,
                float(p["Prix_achat"] or 0),
                float(p["Prix_vente"] or 0))
            ligne.removed.connect(self._remove_ligne)
            ligne.spin_qte.valueChanged.connect(self._recalc_total)
            ligne.spin_pa.valueChanged.connect(self._recalc_total)

            # Insère AVANT le stretch final
            idx = self.scroll_layout.count() - 1
            self.scroll_layout.insertWidget(idx, ligne)

            self._lignes[code_ref] = ligne
            self._recalc_total()

        except Exception:
            logger.exception("Erreur ajout ligne")

    def _remove_ligne(self, code_ref):
        if code_ref not in self._lignes:
            return
        widget = self._lignes.pop(code_ref)
        widget.setParent(None)
        widget.deleteLater()
        self._recalc_total()

    def _recalc_total(self):
        total = 0.0
        for ligne in self._lignes.values():
            total += ligne.spin_qte.value() * ligne.spin_pa.value()

        nb = len(self._lignes)
        self.label_nb_articles.setText(f"{nb} article(s)")
        self.label_total_value.setText(
            f"{total:,.0f} FC".replace(",", " "))

        self.label_empty.setVisible(nb == 0)

    # ══════════════════════════════════════════════════════════════
    def _save(self, validate: bool = False):
        if not self._lignes:
            QtWidgets.QMessageBox.warning(
                self, "BLF vide",
                "Ajoutez au moins un produit au BLF.")
            return

        fournisseur_id = self.combo_fournisseur.currentData()
        fournisseur_nom = self.combo_fournisseur.currentText()
        lignes = [w.get_data() for w in self._lignes.values()]

        # ═══ MODE CLIENT → API ═══
        if is_client_mode():
            try:
                api = get_api()
                payload = {
                    "lignes": [
                        {
                            "code_ref": l["code_ref"],
                            "quantite": l["quantite"],
                            "prix_achat": l["prix_achat"],
                            "prix_vente": l["prix_vente"],
                        }
                        for l in lignes
                    ],
                    "fournisseur_id": fournisseur_id,
                    "notes": self.edit_notes.text().strip() or None,
                    "reference_externe":
                        self.edit_ref_externe.text().strip() or None,
                    "valider_immediatement": bool(validate),
                }
                result = api.create_blf(payload)
                blf_id = result.get("id")
                numero_blf = result.get("numero_blf", "")

                logger.info("BLF créé (API) : %s", numero_blf)
                self.blf_created.emit(blf_id)

                if validate:
                    QtWidgets.QMessageBox.information(
                        self, "BLF validé",
                        f"Le BLF {numero_blf} a été validé.")
                else:
                    QtWidgets.QMessageBox.information(
                        self, "BLF enregistré",
                        f"Le BLF {numero_blf} a été enregistré "
                        "en brouillon.")
                self.accept()
                return
            except Exception as e:
                logger.exception("Échec sauvegarde BLF (API)")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible d'enregistrer le BLF :\n{e}")
                return

        # ═══ MODE AUTONOME / SERVEUR → DB locale ═══
        try:
            compteur = int(db.get_config("blf_compteur", 1))
        except Exception:
            compteur = 1

        numero_blf = f"BLF-{datetime.now().year}-{compteur:09d}"
        total_achat = sum(l["total_ligne"] for l in lignes)
        nb_articles = len(lignes)
        nb_unites = sum(l["quantite"] for l in lignes)

        notes = self.edit_notes.text().strip() or None
        ref_ext = self.edit_ref_externe.text().strip() or None

        from Database import audit

        try:
            with db.transaction():
                blf_id = db.new_id()
                statut = "VALIDEE" if validate else "BROUILLON"
                validated_by = self.user_id if validate else None
                validated_by_name = self.user_name if validate else None
                validated_at = (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if validate else None
                )

                db.execute("""
                    INSERT INTO BonLivraison
                    (id, numero_blf, fournisseur_id, fournisseur_nom,
                     statut, total_achat, nb_articles, nb_unites,
                     notes, reference_externe,
                     created_by, created_by_name,
                     validated_by, validated_by_name, validated_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (blf_id, numero_blf, fournisseur_id, fournisseur_nom,
                      statut, total_achat, nb_articles, nb_unites,
                      notes, ref_ext,
                      self.user_id, self.user_name,
                      validated_by, validated_by_name, validated_at))

                for l in lignes:
                    code_ref = l["code_ref"]
                    row_p = db.query_one(
                        "SELECT Quantite FROM produits "
                        "WHERE Code_reference = ? LIMIT 1",
                        (code_ref,))
                    stock_avant = int(row_p["Quantite"] or 0) if row_p else 0
                    stock_apres = (stock_avant + l["quantite"]
                                   if validate else stock_avant)

                    db.execute("""
                        INSERT INTO LigneBonLivraison
                        (id, blf_id, produit_id, produit_nom,
                         quantite, prix_achat_unitaire, prix_vente_unitaire,
                         total_ligne, stock_avant, stock_apres)
                        VALUES (?,?,?,?,?,?,?,?,?,?)
                    """, (db.new_id(), blf_id, code_ref, l["produit_nom"],
                          l["quantite"], l["prix_achat"], l["prix_vente"],
                          l["total_ligne"],
                          stock_avant if validate else None,
                          stock_apres if validate else None))

                    if validate:
                        db.execute("""
                            UPDATE produits
                            SET Quantite = ?, Prix_achat = ?,
                                Prix_vente = ?, Prix_unitaire = ?
                            WHERE Code_reference = ?
                        """, (stock_apres, l["prix_achat"],
                              l["prix_vente"], l["prix_vente"], code_ref))

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
                              f"BLF {numero_blf} — {fournisseur_nom}",
                              uid_valide))

                db.set_config("blf_compteur", compteur + 1, type_="int")

            # ═══ AUDIT BLF ═══
            try:
                apres = audit.snapshot("BonLivraison", "id", blf_id)
                audit.log(
                    audit.ACTION_CREATION_BLF,
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="BonLivraison",
                    cible_id=blf_id,
                    cible_nom=numero_blf,
                    details={
                        "statut": statut,
                        "fournisseur_id": fournisseur_id,
                        "fournisseur_nom": fournisseur_nom,
                        "total_achat": total_achat,
                        "nb_articles": nb_articles,
                        "nb_unites": nb_unites,
                        "lignes": [
                            {"code_ref": l["code_ref"],
                             "produit": l["produit_nom"],
                             "qte": l["quantite"],
                             "prix_achat": l["prix_achat"],
                             "prix_vente": l["prix_vente"]}
                            for l in lignes
                        ],
                    },
                    apres=apres,
                )

                if validate:
                    audit.log(
                        audit.ACTION_VALIDATION_BLF,
                        utilisateur_id=self.user_id,
                        utilisateur_name=self.user_name,
                        cible_type="BonLivraison",
                        cible_id=blf_id,
                        cible_nom=numero_blf,
                        details={
                            "stock_impacte": nb_unites,
                            "validation_directe": True,
                        })
            except Exception:
                logger.exception("Erreur audit BLF")

            self.blf_created.emit(blf_id)
            QtWidgets.QMessageBox.information(
                self, "BLF enregistré",
                f"Le BLF {numero_blf} a été enregistré.")
            self.accept()

        except Exception as e:
            logger.exception("Erreur sauvegarde BLF")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'enregistrer le BLF :\n{e}")