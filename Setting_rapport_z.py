#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_rapport_z.py — Dialogue de clôture de caisse (Rapport Z).
"""

import logging
import os
from datetime import datetime

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from Database import db, rapport_z
from Interface_rapport_z import Ui_DialogRapportZ

logger = logging.getLogger(__name__)


class Setting_rapport_z(QtWidgets.QDialog, Ui_DialogRapportZ):

    rapport_z_genere = QtCore.Signal(str)

    def __init__(self, parent=None, user_id=None, user_name="",
                 role="ADMIN", is_owner=False, is_developer=False,
                 caisse_utilisateur=None):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.role = (role or "UTILISATEUR").upper()
        self.is_owner = is_owner
        self.is_developer = is_developer
        self.caisse_utilisateur = caisse_utilisateur

        self._data = {}
        self._caisses = []
        self._loading = False

        # Suffixe devise
        try:
            devise = db.get_config("devise", "FC")
            self.spin_compte.setSuffix(f" {devise}")
            self.spin_compte.setMinimum(0)
        except Exception:
            pass

        self._connect_signals()
        self._load_caisses()
        self._init_dates()
        self.refresh()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        self.btn_secondary.clicked.connect(self.reject)
        self.btn_generer.clicked.connect(self._on_generate)
        self.combo_periode.currentTextChanged.connect(self._on_periode_changed)
        self.date_debut.dateChanged.connect(self.refresh)
        self.date_fin.dateChanged.connect(self.refresh)
        self.combo_caisse.currentTextChanged.connect(self.refresh)
        self.spin_compte.valueChanged.connect(self._update_ecart)

    # ══════════════════════════════════════════════════════════════
    def _load_caisses(self):
        try:
            self._caisses = rapport_z.list_caisses_disponibles()
        except Exception:
            self._caisses = ["A"]

        est_caissier = (self.role == "CAISSIER"
                        and not (self.is_owner or self.is_developer))

        self.combo_caisse.blockSignals(True)
        self.combo_caisse.clear()

        if est_caissier and self.caisse_utilisateur:
            self.combo_caisse.addItem(self.caisse_utilisateur)
            self.combo_caisse.setEnabled(False)
        else:
            self.combo_caisse.addItem("Toutes les caisses")
            for c in self._caisses:
                self.combo_caisse.addItem(c)
            self.combo_caisse.setCurrentIndex(0)

        self.combo_caisse.blockSignals(False)

    def _init_dates(self):
        today = QtCore.QDate.currentDate()
        self.date_debut.setDate(today)
        self.date_fin.setDate(today)
        self.date_debut.setEnabled(False)
        self.date_fin.setEnabled(False)

    def _on_periode_changed(self, text: str):
        p = (text or "").lower()
        custom = "personnalis" in p
        self.date_debut.setEnabled(custom)
        self.date_fin.setEnabled(custom)
        self.refresh()

    # ══════════════════════════════════════════════════════════════
    def _selected_caisse(self) -> str:
        txt = self.combo_caisse.currentText()
        if "toutes" in txt.lower():
            return "*"
        return txt or "A"

    def _selected_periode(self) -> str:
        return self.combo_periode.currentText()

    # ══════════════════════════════════════════════════════════════
    def refresh(self):
        if self._loading:
            return
        self._loading = True
        try:
            from datetime import datetime as _dt
            from Client.api_singleton import is_client_mode, get_api

            qd_debut = self.date_debut.date().toPython()
            qd_fin = self.date_fin.date().toPython()

            d_debut = _dt(qd_debut.year, qd_debut.month, qd_debut.day)
            d_fin = _dt(qd_fin.year, qd_fin.month, qd_fin.day)

            caisse = self._selected_caisse()
            periode = self._selected_periode()

            # ═══════════════════════════════════════════════════════
            # MODE CLIENT → appel API PREVIEW
            # ═══════════════════════════════════════════════════════
            if is_client_mode():
                api = get_api()
                if api is not None:
                    try:
                        # Dates uniquement en mode "Personnalisé"
                        is_custom = "personnalis" in (periode or "").lower()
                        ds = d_debut.strftime("%Y-%m-%d") if is_custom else ""
                        df = d_fin.strftime("%Y-%m-%d") if is_custom else ""

                        logger.info(
                            "Rapport Z : preview API "
                            "(caisse=%s, periode=%r)",
                            caisse, periode)

                        self._data = api.preview_rapport_z(
                            caisse=caisse,
                            periode=periode,
                            date_debut=ds,
                            date_fin=df)

                        logger.info(
                            "Rapport Z preview : %d factures, CA=%.0f",
                            self._data.get("nb_factures", 0),
                            self._data.get("ca_total", 0))

                        self._render()
                        return
                    except Exception:
                        logger.exception("Erreur preview API")
                        # Continue en mode local (fallback)

            # ═══════════════════════════════════════════════════════
            # MODE AUTONOME / SERVEUR → DB locale
            # ═══════════════════════════════════════════════════════
            debut, fin = rapport_z.resolve_period(
                periode, date_debut=d_debut,
                date_fin=d_fin, caisse=caisse)

            self._data = rapport_z.compute_rapport_z(caisse, debut, fin)

            logger.info(
                "Rapport Z (local) : caisse=%s, periode=%r → "
                "%d factures, CA=%.0f",
                caisse, periode,
                self._data.get("nb_factures", 0),
                self._data.get("ca_total", 0))

            self._render()
        except Exception:
            logger.exception("Erreur refresh Rapport Z")
        finally:
            self._loading = False

    # ══════════════════════════════════════════════════════════════
    def _render(self):
        """Remplit tous les labels avec les VRAIS objectName."""
        devise = self._data.get("devise", "FC")
        d = self._data

        # ─── Compteurs (value_big*) ───
        self.value_big.setText(str(d.get("nb_factures", 0)))
        self.value_big1.setText(str(d.get("nb_articles", 0)))
        self.value_big2.setText(str(d.get("nb_clients_ident", 0)))
        self.value_big3.setText(str(d.get("nb_clients_anon", 0)))
        self.value_big4.setText(str(d.get("nb_annulations", 0)))

        # ─── Montants (value_money*) ───
        try:
            from Database.currency import format_dual
            self.value_money.setText(
                format_dual(d.get('ca_total', 0)))
        except Exception:
            self.value_money.setText(
                f"{d.get('ca_total', 0):,.0f} {devise}"
                .replace(",", " "))
        self.value_money1.setText(
            f"{d.get('panier_moyen', 0):,.0f} {devise}".replace(",", " "))
        self.value_money2.setText(
            f"{d.get('montant_annule', 0):,.0f} {devise}".replace(",", " "))

        # ─── Contrôle caisse ───
        self.value_money3.setText(
            f"{d.get('ca_total', 0):,.0f} {devise}".replace(",", " "))

        # ─── Pré-remplit le spin si vide ───
        if self.spin_compte.value() == 0 and d.get("ca_total", 0) > 0:
            self.spin_compte.blockSignals(True)
            self.spin_compte.setValue(d["ca_total"])
            self.spin_compte.blockSignals(False)

        self._update_ecart()

    # ══════════════════════════════════════════════════════════════
    def _update_ecart(self):
        """Met à jour le label d'écart (change d'objectName pour le style)."""
        ca = self._data.get("ca_total", 0)
        compte = self.spin_compte.value()
        ecart = compte - ca
        devise = self._data.get("devise", "FC")

        if abs(ecart) < 1:
            txt = f"Écart : 0 {devise} — ✓ Aucun écart"
            obj = "ecart_ok"
        elif ecart < 0:
            txt = f"Écart : {ecart:+,.0f} {devise} — MANQUE".replace(",", " ")
            obj = "ecart_danger"
        else:
            txt = f"Écart : {ecart:+,.0f} {devise} — EXCÉDENT".replace(",", " ")
            obj = "ecart_warn"

        self.ecart_ok.setText(txt)
        self.ecart_ok.setObjectName(obj)
        self.ecart_ok.style().unpolish(self.ecart_ok)
        self.ecart_ok.style().polish(self.ecart_ok)

    # ══════════════════════════════════════════════════════════════
    def _on_generate(self):
        if self._data.get("nb_factures", 0) == 0:
            rep = QtWidgets.QMessageBox.question(
                self, "Aucune vente",
                "Aucune vente sur cette période.\n\nGénérer quand même ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return

        # ═══ MODE CLIENT → API ═══
        from Client.api_singleton import is_client_mode, get_api
        if is_client_mode():
            try:
                api = get_api()
                caisse = self._selected_caisse()
                # ⚠️ NE PAS convertir "*" en "TOUTES"
                # Le serveur normalise déjà

                # Dates custom
                is_custom = "personnalis" in self._selected_periode().lower()
                qd = self.date_debut.date().toPython()
                qf = self.date_fin.date().toPython()
                ds = qd.strftime("%Y-%m-%d") if is_custom else ""
                df = qf.strftime("%Y-%m-%d") if is_custom else ""

                result = api.create_rapport_z(
                    caisse=caisse,  # ← "*" ou "A" etc.
                    periode=self._selected_periode(),
                    montant_compte=self.spin_compte.value(),
                    format_pdf=("a4" if "a4" in
                                        self.combo_format.currentText().lower()
                                else "ticket"),
                    date_debut=ds,
                    date_fin=df,
                )

                QtWidgets.QMessageBox.information(
                    self, "Rapport Z généré",
                    f"Le rapport <b>{result['numero_z']}</b> "
                    f"a été généré sur le serveur.\n\n"
                    f"PDF : {result.get('chemin_pdf', '—')}")

                self.rapport_z_genere.emit(result.get("chemin_pdf", ""))
                self.spin_compte.setValue(0)
                self.refresh()
                return
            except Exception as e:
                logger.exception("Erreur Rapport Z via API")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible de générer sur le serveur :\n{e}")
                return

            except Exception as e:
                logger.exception("Erreur Rapport Z via API")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible de générer le rapport sur le serveur :\n{e}")
                return

        # ═══ MODE LOCAL (ci-dessous inchangé) ═══
        format_pdf = "a4" if "a4" in self.combo_format.currentText().lower() else "ticket"
        caisse = self._selected_caisse()
        if caisse == "*":
            caisse = "TOUTES"
        numero_z = rapport_z.next_numero_z(caisse)

        dossier = os.path.join("Rapports", "RapportZ",
                               datetime.now().strftime("%Y-%m"))
        os.makedirs(dossier, exist_ok=True)
        path_pdf = os.path.join(dossier, f"{numero_z}.pdf")

        try:
            rapport_z.generate_pdf(
                self._data, self.spin_compte.value(), numero_z,
                path_pdf, format_pdf=format_pdf)
            logger.info("PDF Rapport Z : %s", path_pdf)
        except Exception:
            logger.exception("Erreur PDF Rapport Z")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "Impossible de générer le PDF.")
            return

        try:
            rapport_z.save_rapport_z(
                self._data, user_id=self.user_id,
                user_name=self.user_name,
                montant_compte=self.spin_compte.value(),
                format_pdf=format_pdf, chemin_pdf=path_pdf)
        except Exception:
            logger.exception("Erreur enregistrement Rapport Z")

        if self.chk_print_auto.isChecked():
            try:
                from Database import printer_manager
                # Ticket → imprimante ticket, A4 → imprimante rapport
                kind = "ticket" if format_pdf == "ticket" else "report"
                printer_manager.print_pdf_silent(path_pdf, kind=kind)
                logger.info("Rapport Z envoyé (%s)", kind)
            except Exception:
                logger.exception("Erreur impression")

        self.rapport_z_genere.emit(path_pdf)

        QtWidgets.QMessageBox.information(
            self, "Rapport Z généré",
            f"Le rapport <b>{numero_z}</b> a été généré.\n\n"
            f"PDF : {os.path.basename(path_pdf)}")

        self.spin_compte.setValue(0)
        self.refresh()