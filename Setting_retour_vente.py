#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_retour_vente.py — Dialogue de retour de vente.
=======================================================
Permet de retourner partiellement une facture.
"""

import logging
import os
from datetime import datetime

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from Client.api_singleton import get_api, is_client_mode
from Database import db, retour_engine
from Database import printer_manager
from Interface_retour_vente import Ui_DialogRetourVente

logger = logging.getLogger(__name__)


COL_CHECK  = 0
COL_ARTICLE = 1
COL_QTE_F  = 2
COL_QTE_R  = 3
COL_PU     = 4
COL_TOTAL  = 5


class Setting_retour_vente(QtWidgets.QDialog, Ui_DialogRetourVente):

    retour_valide = QtCore.Signal(str)   # num_fact_origine

    def __init__(self, parent=None,
                 num_fact: str = None,
                 user_id: str = None,
                 user_name: str = "",
                 role: str = "ADMIN"):
        super().__init__(parent)
        self.setupUi(self)

        self.num_fact = num_fact
        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.role = (role or "UTILISATEUR").upper()

        self._lignes = []       # cache des lignes de la facture

        self._setup_icons()
        self._setup_table()
        self._connect_signals()
        self._load_facture()

    # ══════════════════════════════════════════════════════════════
    def _setup_icons(self):
        try:
            pix = QtGui.QPixmap(":/Icon/Icons/arrow-left_white.svg")
            if not pix.isNull():
                self.header_icon.setPixmap(pix.scaled(
                    32, 32, Qt.KeepAspectRatio,
                    Qt.SmoothTransformation))
        except Exception:
            pass

    def _setup_table(self):
        h = self.table_lignes.horizontalHeader()
        h.setSectionResizeMode(COL_CHECK,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_ARTICLE, QtWidgets.QHeaderView.Stretch)
        h.setSectionResizeMode(COL_QTE_F,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_QTE_R,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_PU,      QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_TOTAL,   QtWidgets.QHeaderView.ResizeToContents)
        self.table_lignes.verticalHeader().setVisible(False)
        self.table_lignes.verticalHeader().setDefaultSectionSize(46)

    def _connect_signals(self):
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_valider.clicked.connect(self._on_valider)

    # ══════════════════════════════════════════════════════════════
    def _load_facture(self):
        """Charge les lignes de la facture (API ou DB)."""
        try:
            if is_client_mode():
                api = get_api()
                data = api.get_vente(self.num_fact)
                self._lignes = data.get("lignes", [])
                # Enrichit avec les infos de la vente
                self._client_name = data.get("Client_name")
                self._date_vent = data.get("Date_vent")
                self._total_fact = float(data.get("total") or 0)
            else:
                self._lignes = retour_engine.get_lignes_facture(self.num_fact)
                if self._lignes:
                    first = self._lignes[0]
                    self._client_name = first.get("Client_name")
                    self._date_vent = first.get("Date_vent")
                    self._total_fact = sum(
                        float(l["Total"] or 0) for l in self._lignes)

            self._render_info()
            self._render_table()
        except Exception:
            logger.exception("Erreur chargement facture")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible de charger la facture.")
            self.reject()

    def _render_info(self):
        self.header_sub.setText(f"Facture d'origine : {self.num_fact}")
        self.lbl_num_fact.setText(str(self.num_fact))

        # Date formatée
        date_str = str(self._date_vent or "—")
        if len(date_str) > 16:
            date_str = date_str[:16]
        self.lbl_date.setText(date_str)

        self.lbl_client.setText(self._client_name or "Client anonyme")

        devise = db.get_config("devise", "FC")
        self.lbl_montant_initial.setText(
            f"{self._total_fact:,.0f} {devise}".replace(",", " "))

    def _render_table(self):
        t = self.table_lignes
        t.blockSignals(True)
        t.setRowCount(0)
        t.setRowCount(len(self._lignes))

        for i, l in enumerate(self._lignes):
            # Colonne 0 : checkbox
            chk = QtWidgets.QCheckBox()
            chk.setChecked(True)
            chk.stateChanged.connect(self._recalc_total)
            w = QtWidgets.QWidget()
            lay = QtWidgets.QHBoxLayout(w)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setAlignment(Qt.AlignCenter)
            lay.addWidget(chk)
            t.setCellWidget(i, COL_CHECK, w)

            # Colonne 1 : article
            art = QtWidgets.QTableWidgetItem(l.get("Article") or "—")
            art.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            t.setItem(i, COL_ARTICLE, art)

            # Colonne 2 : qté facturée
            qte_f = int(l.get("Quantite") or 0)
            it = QtWidgets.QTableWidgetItem(str(qte_f))
            it.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_QTE_F, it)

            # Colonne 3 : spin qté retour (calcul du max possible)
            code_ref = l.get("Code_reference")
            deja_retourne = 0
            if not is_client_mode() and code_ref:
                deja_retourne = retour_engine.get_quantite_deja_retournee(
                    self.num_fact, code_ref)
            max_q = max(0, qte_f - deja_retourne)

            spin = QtWidgets.QSpinBox()
            spin.setRange(0, max_q)
            spin.setValue(max_q)
            spin.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
            spin.setAlignment(Qt.AlignCenter)
            spin.setEnabled(max_q > 0)
            spin.valueChanged.connect(self._recalc_total)
            t.setCellWidget(i, COL_QTE_R, spin)

            # Colonne 4 : PU
            pu = float(l.get("Prix_uni") or 0)
            it_pu = QtWidgets.QTableWidgetItem(
                f"{pu:,.0f}".replace(",", " "))
            it_pu.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_PU, it_pu)

            # Colonne 5 : total (recalculé)
            it_tot = QtWidgets.QTableWidgetItem("0")
            it_tot.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_TOTAL, it_tot)

        t.blockSignals(False)
        self._recalc_total()

    def _recalc_total(self):
        """Recalcule le total à rembourser."""
        total = 0.0
        devise = db.get_config("devise", "FC")

        for i, l in enumerate(self._lignes):
            w_check = self.table_lignes.cellWidget(i, COL_CHECK)
            spin = self.table_lignes.cellWidget(i, COL_QTE_R)
            if not w_check or not spin:
                continue

            chk = w_check.findChild(QtWidgets.QCheckBox)
            if not chk or not chk.isChecked():
                self.table_lignes.item(i, COL_TOTAL).setText("0")
                continue

            qte = spin.value()
            pu = float(l.get("Prix_uni") or 0)
            ligne_total = qte * pu
            total += ligne_total

            self.table_lignes.item(i, COL_TOTAL).setText(
                f"{ligne_total:,.0f}".replace(",", " "))

        self.lbl_total.setText(
            f"{total:,.0f} {devise}".replace(",", " "))

    # ══════════════════════════════════════════════════════════════
    def _on_valider(self):
        # Construction des lignes à retourner
        lignes = []
        for i, l in enumerate(self._lignes):
            w_check = self.table_lignes.cellWidget(i, COL_CHECK)
            spin = self.table_lignes.cellWidget(i, COL_QTE_R)
            if not w_check or not spin:
                continue

            chk = w_check.findChild(QtWidgets.QCheckBox)
            if not chk or not chk.isChecked():
                continue
            qte = spin.value()
            if qte <= 0:
                continue

            pu = float(l.get("Prix_uni") or 0)
            lignes.append({
                "code_reference": l.get("Code_reference"),
                "article": l.get("Article"),
                "quantite": qte,
                "prix_unitaire": pu,
                "total": qte * pu,
                "reconditionne": True,   # TODO: ajouter checkbox par ligne
            })

        if not lignes:
            QtWidgets.QMessageBox.warning(
                self, "Aucun article",
                "Sélectionnez au moins un article à retourner.")
            return

        motif = self.combo_motif.currentText().strip()
        if motif == "Autre":
            motif, ok = QtWidgets.QInputDialog.getText(
                self, "Motif personnalisé",
                "Précisez le motif :")
            if not ok or not motif.strip():
                return
            motif = motif.strip()

        totaux = retour_engine.compute_totaux_retour(lignes)
        devise = db.get_config("devise", "FC")

        # Confirmation
        msg = (
            f"<b>Confirmer le retour ?</b><br><br>"
            f"Facture : <code>{self.num_fact}</code><br>"
            f"Motif : {motif}<br>"
            f"Articles : <b>{totaux['nb_articles']}</b> "
            f"({totaux['nb_lignes']} ligne(s))<br>"
            f"Montant à rembourser : <b>"
            f"{totaux['montant_total']:,.0f} {devise}</b>"
            .replace(",", " ") + "<br><br>"
            f"Le stock sera <b>restauré</b> et un "
            f"<b>avoir PDF</b> sera généré."
        )
        rep = QtWidgets.QMessageBox.question(
            self, "Confirmation", msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        # Sauvegarde
        data = {
            "num_fact_origine": self.num_fact,
            "client_name": self._client_name,
            "client_numero": self._extract_client_numero(),
            "motif": motif,
            "notes": self.txt_notes.toPlainText().strip() or None,
            "lignes": lignes,
            "montant_total": totaux["montant_total"],
            "nb_articles": totaux["nb_articles"],
        }

        try:
            if is_client_mode():
                api = get_api()
                result = api.create_retour(data)
                rid = result["id"]
                numero_retour = result.get("numero_retour", "")
            else:
                rid = retour_engine.save_retour(
                    data, self.user_id, self.user_name)
                numero_retour = retour_engine.next_numero_retour()

            # Génère PDF avoir
            self._generate_avoir(data, numero_retour, rid)

            self.retour_valide.emit(self.num_fact)

            QtWidgets.QMessageBox.information(
                self, "Retour validé",
                f"Le retour <b>{numero_retour}</b> a été enregistré.\n\n"
                f"Montant remboursé : "
                f"{totaux['montant_total']:,.0f} {devise}"
                .replace(",", " "))
            self.accept()

        except Exception as e:
            logger.exception("Erreur validation retour")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible de valider le retour :\n{e}")

    def _extract_client_numero(self):
        """Extrait le numéro client depuis son nom."""
        if not self._client_name:
            return None
        parts = str(self._client_name).strip().split(" ")
        if parts and (parts[-1].startswith("0")
                      or parts[-1].startswith("+243")):
            return parts[-1]
        return None

    def _generate_avoir(self, data: dict, numero_retour: str,
                        rid: str) -> None:
        """Génère le PDF de l'avoir."""
        try:
            # Infos pharmacie
            ph = db.query_one(
                "SELECT nom, adresse, numero FROM Pharmacie "
                "WHERE id = 1 LIMIT 1")
            data["nom_pharmacie"] = ph["nom"] if ph else "NOVA PHARMA"
            data["adresse_pharmacie"] = ph["adresse"] if ph else ""
            data["telephone_pharmacie"] = ph["numero"] if ph else ""

            data["numero_retour"] = numero_retour
            data["date_retour"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")

            dossier = os.path.join(
                "Factures", "Avoirs",
                datetime.now().strftime("%Y-%m"))
            os.makedirs(dossier, exist_ok=True)
            path = os.path.join(dossier, f"{numero_retour}.pdf")

            retour_engine.generate_pdf_avoir(data, path)
            logger.info("Avoir PDF généré : %s", path)

            # Impression auto si configurée
            try:
                auto = bool(db.get_config("printer_auto_print", False))
                if auto:
                    printer_manager.print_pdf_silent(path)
            except Exception:
                pass

        except Exception:
            logger.exception("Erreur génération avoir")