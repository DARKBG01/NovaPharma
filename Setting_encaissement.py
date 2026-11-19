#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_encaissement.py — Dialogue de paiement (reçu / rendu).
==============================================================
S'ouvre AVANT la création de la facture.
Retourne un dict {devise, montant_recu, result} si Accepté.
"""

import logging

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from Database import db, encaissement

logger = logging.getLogger(__name__)


class Setting_encaissement(QtWidgets.QDialog):
    """Dialogue de paiement."""

    def __init__(self, parent=None,
                 montant_facture: float = 0,
                 devise: str = "FC"):
        super().__init__(parent)

        self.montant_facture = float(montant_facture or 0)
        self.devise = devise or "FC"
        self.taux = float(db.get_config("taux_change", 2800.0))

        self._result = None

        self.setWindowTitle("Encaissement")
        from Ui_helpers import make_dialog_responsive
        #make_dialog_responsive(self, 560, 520)
        self.setModal(True)
        self._build_ui()
        self._recalc()

    # ══════════════════════════════════════════════════════════════
    def _build_ui(self):
        self.setStyleSheet("""
            QDialog { background: #f0f4f8; }
            QLabel { color: #334155; background: transparent; font-size: 13px; }
            QLabel#lbl_big {
                color: #0f172a; font-size: 24px; font-weight: 800;
            }
            QLabel#lbl_rendu {
                color: #16A34A; font-size: 22px; font-weight: 800;
            }
            QLabel#lbl_manque {
                color: #DC2626; font-size: 16px; font-weight: 700;
            }
            QFrame#card {
                background: #ffffff; border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QFrame#rendu_card_ok {
                background: #dcfce7; border: 1px solid #86efac;
                border-radius: 12px;
            }
            QFrame#rendu_card_err {
                background: #fee2e2; border: 1px solid #fecaca;
                border-radius: 12px;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background: #f8fafc; border: 1.5px solid #e2e8f0;
                border-radius: 10px; padding: 8px 12px;
                font-size: 14px; color: #0f172a; min-height: 24px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                background: #ffffff; border-color: #00B4D8;
            }
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #0077B6, stop:1 #023E8A);
                color: white; border: none; border-radius: 10px;
                padding: 10px 24px; font-weight: 700; font-size: 13px;
                min-width: 130px;
            }
            QPushButton:hover { background: #023E8A; }
            QPushButton:disabled { background: #cbd5e1; }
            QPushButton#btn_cancel {
                background: transparent; color: #64748b;
                border: 1.5px solid #e2e8f0;
            }
            QPushButton#btn_cancel:hover {
                background: #fef2f2; color: #dc2626; border-color: #fecaca;
            }
        """)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(14)

        # ─── Header ───
        h = QtWidgets.QHBoxLayout()
        ico = QtWidgets.QLabel("💰")
        ico.setStyleSheet("font-size: 32px;")
        h.addWidget(ico)

        v = QtWidgets.QVBoxLayout()
        t1 = QtWidgets.QLabel("Encaissement")
        t1.setStyleSheet(
            "font-size: 18px; font-weight: 800; color: #023E8A;")
        v.addWidget(t1)
        t2 = QtWidgets.QLabel("Saisissez le montant reçu du client")
        t2.setStyleSheet("color: #64748b; font-size: 11px;")
        v.addWidget(t2)
        h.addLayout(v)
        h.addStretch()
        root.addLayout(h)

        # ─── Carte total ───
        total_card = QtWidgets.QFrame()
        total_card.setObjectName("card")
        tv = QtWidgets.QVBoxLayout(total_card)
        tv.setContentsMargins(20, 16, 20, 16)
        tv.setSpacing(4)

        lbl_total_titre = QtWidgets.QLabel("MONTANT À PAYER")
        lbl_total_titre.setStyleSheet(
            "color: #94a3b8; font-size: 10px; font-weight: 700; "
            "letter-spacing: 1px;")
        tv.addWidget(lbl_total_titre)

        self.lbl_total = QtWidgets.QLabel("0 FC")
        self.lbl_total.setObjectName("lbl_big")
        tv.addWidget(self.lbl_total)

        self.lbl_total_usd = QtWidgets.QLabel("")
        self.lbl_total_usd.setStyleSheet(
            "color: #64748b; font-size: 12px; font-weight: 600;")
        tv.addWidget(self.lbl_total_usd)

        root.addWidget(total_card)

        # ─── Carte saisie ───
        saisie_card = QtWidgets.QFrame()
        saisie_card.setObjectName("card")
        sv = QtWidgets.QFormLayout(saisie_card)
        sv.setContentsMargins(20, 16, 20, 16)
        sv.setSpacing(12)

        # Devise
        self.combo_devise = QtWidgets.QComboBox()
        self.combo_devise.addItems(["FC", "USD"])
        self.combo_devise.currentTextChanged.connect(self._recalc)
        sv.addRow("Devise de paiement", self.combo_devise)

        # Montant reçu
        self.input_recu = QtWidgets.QDoubleSpinBox()
        self.input_recu.setRange(0, 999_999_999.99)
        self.input_recu.setDecimals(2)
        self.input_recu.setSuffix(" " + self.devise)
        self.input_recu.setValue(self.montant_facture)
        self.input_recu.valueChanged.connect(self._recalc)
        self.input_recu.editingFinished.connect(self._on_valider)  # ← AJOUT
        sv.addRow("Montant reçu", self.input_recu)

        # Équivalent FC (si USD)
        self.lbl_equiv = QtWidgets.QLabel("")
        self.lbl_equiv.setStyleSheet(
            "color: #64748b; font-size: 11px; font-weight: 600;")
        sv.addRow("", self.lbl_equiv)

        root.addWidget(saisie_card)

        # ─── Carte rendu ───
        self.rendu_card = QtWidgets.QFrame()
        self.rendu_card.setObjectName("rendu_card_ok")
        rv = QtWidgets.QVBoxLayout(self.rendu_card)
        rv.setContentsMargins(20, 16, 20, 16)
        rv.setSpacing(4)

        lbl_rendu_titre = QtWidgets.QLabel("RENDU À DONNER")
        lbl_rendu_titre.setStyleSheet(
            "color: #15803d; font-size: 10px; font-weight: 700; "
            "letter-spacing: 1px;")
        rv.addWidget(lbl_rendu_titre)

        self.lbl_rendu = QtWidgets.QLabel("0 FC")
        self.lbl_rendu.setObjectName("lbl_rendu")
        rv.addWidget(self.lbl_rendu)

        self.lbl_manque = QtWidgets.QLabel("")
        self.lbl_manque.setObjectName("lbl_manque")
        rv.addWidget(self.lbl_manque)

        root.addWidget(self.rendu_card)

        # ─── Footer ───
        hf = QtWidgets.QHBoxLayout()
        hf.addStretch()

        self.btn_cancel = QtWidgets.QPushButton("Annuler")
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.reject)
        hf.addWidget(self.btn_cancel)

        self.btn_valider = QtWidgets.QPushButton("  Valider la vente")
        self.btn_valider.clicked.connect(self._on_valider)
        self.btn_valider.setDefault(True)  # ← AJOUT
        self.btn_valider.setAutoDefault(True)  # ← AJOUT
        hf.addWidget(self.btn_valider)

        root.addLayout(hf)

    # ══════════════════════════════════════════════════════════════
    def _recalc(self):
        """Recalcule le rendu en temps réel."""
        devise = self.combo_devise.currentText()
        recu = self.input_recu.value()

        # Adapte le suffixe et la valeur par défaut selon la devise
        if devise == "USD":
            total_usd = self.montant_facture / self.taux
            self.input_recu.setSuffix(" $")
            # Si l'utilisateur change la devise, on remet le montant au total converti
            if self.input_recu.property("last_devise") != "USD":
                self.input_recu.blockSignals(True)
                self.input_recu.setValue(total_usd)
                self.input_recu.blockSignals(False)
            self.input_recu.setProperty("last_devise", "USD")
        else:
            self.input_recu.setSuffix(" FC")
            if self.input_recu.property("last_devise") != "FC":
                self.input_recu.blockSignals(True)
                self.input_recu.setValue(self.montant_facture)
                self.input_recu.blockSignals(False)
            self.input_recu.setProperty("last_devise", "FC")

        recu = self.input_recu.value()

        # Calcul
        result = encaissement.compute_rendu(
            self.montant_facture, devise, recu, self.taux)
        self._result = result

        # Affichage total
        self.lbl_total.setText(
            f"{self.montant_facture:,.0f} FC".replace(",", " "))
        total_usd = self.montant_facture / self.taux if self.taux > 0 else 0
        self.lbl_total_usd.setText(
            f"Équivalent : $ {total_usd:,.2f}".replace(",", " "))

        # Équivalent FC si paiement USD
        if devise == "USD":
            self.lbl_equiv.setText(
                f"Équivalent FC : {result['montant_recu_fc']:,.0f} FC"
                .replace(",", " "))
        else:
            self.lbl_equiv.setText("")

        # Rendu
        if result["suffisant"]:
            self.rendu_card.setObjectName("rendu_card_ok")
            self.lbl_rendu.setStyleSheet(
                "color: #16A34A; font-size: 22px; font-weight: 800;")
            self.lbl_rendu.setText(
                f"{result['montant_rendu']:,.0f} FC".replace(",", " "))
            self.lbl_manque.setText("")
            self.btn_valider.setEnabled(True)
        else:
            self.rendu_card.setObjectName("rendu_card_err")
            self.lbl_rendu.setStyleSheet(
                "color: #DC2626; font-size: 22px; font-weight: 800;")
            self.lbl_rendu.setText("Montant insuffisant")
            self.lbl_manque.setText(
                f"Manque : {result['manque']:,.0f} FC".replace(",", " "))
            self.btn_valider.setEnabled(False)

        self.rendu_card.style().unpolish(self.rendu_card)
        self.rendu_card.style().polish(self.rendu_card)

    # ══════════════════════════════════════════════════════════════
    def _on_valider(self):
        if not self._result or not self._result["suffisant"]:
            return

        # Confirmation
        rep = QtWidgets.QMessageBox.question(
            self, "Confirmer l'encaissement",
            f"<b>Valider la vente ?</b><br><br>"
            f"Total : <b>{self.montant_facture:,.0f} FC</b><br>"
            f"Reçu : <b>{self._result['montant_recu']:,.2f} "
            f"{self._result['devise_paiement']}</b><br>"
            f"Rendu : <b>{self._result['montant_rendu']:,.0f} FC</b>"
            .replace(",", " "),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)

        if rep != QtWidgets.QMessageBox.Yes:
            return

        self.accept()

    # ══════════════════════════════════════════════════════════════
    def get_result(self) -> dict:
        """Retourne le dict {devise, montant_recu, result}."""
        if not self._result:
            return None
        return {
            "devise": self._result["devise_paiement"],
            "montant_recu": self._result["montant_recu"],
            "result": self._result,
        }