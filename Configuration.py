#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration.py — Wizard de première configuration.
======================================================
Flux :
  1. Choix du type (Serveur / Client)         → page_type
  2a. SERVEUR → Wizard complet (6 pages .ui)
  2b. CLIENT  → Mini wizard (config + récap .ui)
"""

import os
import logging
import re
import socket
from datetime import date

import httpx
import bcrypt
from PySide6 import QtWidgets, QtGui, QtCore

from Database import db, seed, NATIONALITY_LIST
from Interface_configuration import Ui_Wizard
from Ui_helpers import fix_all_spinboxes



# ══════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════
PWD_MIN_LENGTH   = 8
PHONE_REGEX      = re.compile(r"(?:\+243\d{9}|0\d{9})")
EMAIL_REGEX      = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_REGEX       = re.compile(r"^[A-Za-zÀ-ÿ\-' ]{2,50}$")
ADDRESS_MIN_LEN  = 5

PHARMACY_TYPE_MAP = {
    "Petite":  "PETITE",
    "Moyenne": "MOYENNE",
    "Grande":  "GRANDE",
}



# ══════════════════════════════════════════════════════════════════
# Dialogue consentements
# ══════════════════════════════════════════════════════════════════
class ConsentementDialog(QtWidgets.QDialog):
    """Dialogue de consentements avec textes complets."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Consentements — Nova Pharma")
        self.setMinimumSize(720, 640)
        self.setModal(True)
        self._build_ui()


    def _build_ui(self):
        self.setStyleSheet("""
            QDialog { background: #f0f4f8; }
            QLabel { color: #334155; background: transparent; }
            QLabel#title {
                color: #023E8A; font-size: 18px; font-weight: 800;
            }
            QLabel#sub {
                color: #64748b; font-size: 12px;
            }
            QFrame#card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QFrame#card QLabel { background: transparent; }
            QTextEdit {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                color: #1e293b;
                font-size: 12px;
            }
            QCheckBox {
                font-size: 13px; font-weight: 600;
                color: #0f172a; spacing: 10px;
            }
            QPushButton {
                background: #0077B6; color: white;
                border: none; border-radius: 10px;
                padding: 10px 24px; font-weight: 700;
                font-size: 12px; min-width: 140px;
            }
            QPushButton:hover { background: #023E8A; }
            QPushButton#btn_cancel {
                background: transparent; color: #64748b;
                border: 1.5px solid #e2e8f0;
            }
        """)

        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(14)

        # Header
        t = QtWidgets.QLabel("Consentements & Conditions")
        t.setObjectName("title")
        v.addWidget(t)

        s = QtWidgets.QLabel(
            "Lisez attentivement chaque section ci-dessous. "
            "Les deux premiers consentements sont indépendants "
            "et facultatifs. Les CGU sont obligatoires.")
        s.setObjectName("sub")
        s.setWordWrap(True)
        v.addWidget(s)

        # Scroll
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        content = QtWidgets.QWidget()
        content.setStyleSheet("background: transparent;")
        cv = QtWidgets.QVBoxLayout(content)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(14)

        # ─── 1. CGU (obligatoire) ───
        self.check_cgu = self._make_section(
            cv, "1. Conditions Générales d'Utilisation (obligatoire)",
            CGU_TEXT, "J'ai lu et j'accepte les CGU de Nova Pharma.",
            checked=True)

        # ─── 2. Sauvegarde (indépendant) ───
        self.check_sauvegarde = self._make_section(
            cv, "2. Sauvegarde automatique des données",
            SAUVEGARDE_TEXT,
            "J'accepte la sauvegarde automatique de mes données.",
            checked=True)

        # ─── 3. IA anonymisée (facultatif) ───
        self.check_ia = self._make_section(
            cv, "3. Utilisation anonymisée pour amélioration (facultatif)",
            IA_TEXT,
            "J'accepte l'utilisation anonymisée de mes données de vente "
            "pour améliorer Nova Pharma.",
            checked=False)

        cv.addStretch()
        scroll.setWidget(content)
        v.addWidget(scroll, 1)

        # Footer
        hf = QtWidgets.QHBoxLayout()
        hf.addStretch()
        btn_cancel = QtWidgets.QPushButton("Annuler")
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.clicked.connect(self.reject)
        hf.addWidget(btn_cancel)

        btn_ok = QtWidgets.QPushButton("J'accepte et je continue")
        btn_ok.clicked.connect(self._on_accept)
        hf.addWidget(btn_ok)
        v.addLayout(hf)

    def _make_section(self, layout, titre, texte, checkbox_text,
                      checked=False):
        """Crée une section avec texte détaillé + checkbox."""
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        cv = QtWidgets.QVBoxLayout(card)
        cv.setContentsMargins(20, 16, 20, 16)
        cv.setSpacing(10)

        tl = QtWidgets.QLabel(titre)
        tl.setStyleSheet(
            "color: #023E8A; font-size: 13px; font-weight: 800;")
        cv.addWidget(tl)

        txt = QtWidgets.QTextEdit()
        txt.setPlainText(texte)
        txt.setReadOnly(True)
        txt.setMinimumHeight(130)
        txt.setMaximumHeight(180)
        cv.addWidget(txt)

        chk = QtWidgets.QCheckBox(checkbox_text)
        chk.setChecked(checked)
        cv.addWidget(chk)

        layout.addWidget(card)
        return chk

    def _on_accept(self):
        if not self.check_cgu.isChecked():
            QtWidgets.QMessageBox.warning(
                self, "CGU obligatoires",
                "Vous devez accepter les Conditions Générales "
                "d'Utilisation pour continuer.")
            return
        self.accept()

    def resultats(self):
        return (
            self.check_sauvegarde.isChecked(),
            self.check_ia.isChecked(),
            self.check_cgu.isChecked(),
        )


# ══════════════════════════════════════════════════════════════════
# Textes détaillés v2.0
# ══════════════════════════════════════════════════════════════════
CGU_TEXT = """CONDITIONS GÉNÉRALES D'UTILISATION — NOVA PHARMA v2.0

1. OBJET
Nova Pharma est un logiciel de gestion pharmaceutique destiné aux
officines. Il permet la gestion des ventes, du stock, des clients,
des fournisseurs, des rapports et de la traçabilité des actions.

2. LICENCE D'UTILISATION
L'utilisation de Nova Pharma est accordée sous licence propriétaire
non transférable. Vous ne pouvez pas copier, distribuer, revendre,
modifier, décompiler ou contourner les mécanismes de sécurité.

3. RESPONSABILITÉ DE L'UTILISATEUR
L'utilisateur est seul responsable :
  • De la véracité des données saisies
  • Du respect des réglementations pharmaceutiques locales
  • De la sauvegarde régulière de ses données
  • De la confidentialité de ses identifiants
  • De la protection physique de son matériel

4. EXONÉRATION DE RESPONSABILITÉ
TEAM NOVA fournit Nova Pharma "en l'état". TEAM NOVA ne saurait
être tenu responsable :
  • Des pertes de données (panne, vol, virus, ransomware)
  • Des erreurs de saisie ou de manipulation
  • Des conséquences commerciales ou financières
  • Des dommages indirects, matériels ou immatériels
  • D'une interruption d'activité, quelle qu'en soit la cause
  • D'une mauvaise utilisation du logiciel
  • D'un défaut de sauvegarde par l'utilisateur

L'utilisateur utilise Nova Pharma sous sa seule responsabilité.

5. MAINTENANCE & SUPPORT
Les conditions de maintenance et de support sont définies par un
contrat séparé entre l'utilisateur et TEAM NOVA. Les interventions
de maintenance gratuite peuvent être limitées dans le temps (ex:
3 mois après l'installation). Au-delà, toute intervention est
facturée selon les tarifs en vigueur de TEAM NOVA.

6. DONNÉES PERSONNELLES
Les données des clients (nom, téléphone, adresse, etc.) sont stockées
localement sur votre serveur. Vous vous engagez à respecter la
confidentialité de ces informations conformément aux lois en vigueur.

7. SUPPORT & MISES À JOUR
Le support technique est disponible via teamnovaoff@gmail.com.
Les mises à jour sont fournies à la discrétion de TEAM NOVA.

8. RÉSILIATION
La licence peut être révoquée en cas de non-respect de ces conditions.

9. DROIT APPLICABLE
Ces conditions sont régies par les lois de la République
Démocratique du Congo.

En acceptant, vous reconnaissez avoir lu et compris l'intégralité
de ces conditions."""


SAUVEGARDE_TEXT = """SAUVEGARDE AUTOMATIQUE DES DONNÉES

Nova Pharma peut sauvegarder automatiquement vos données selon
une politique de rétention configurable :
  • Quotidienne : 7 dernières archives
  • Hebdomadaire : 4 dernières archives
  • Mensuelle : 12 dernières archives
  • Annuelle : 5 dernières archives

CE QUE ÇA FAIT :
  • Création d'archives ZIP chiffrées (AES-256)
  • Stockage local ou sur USB/NAS/réseau
  • Détection automatique des besoins de sauvegarde
  • Mot de passe dérivé de l'empreinte machine

CE QUE ÇA NE FAIT PAS :
  • Aucune donnée n'est transmise sur Internet
  • Aucune donnée n'est lue par un tiers

RISQUES SANS SAUVEGARDE :
  • Perte totale en cas de panne disque
  • Aucun recours en cas de ransomware
  • Perte de l'historique comptable

Cette option est INDÉPENDANTE et FACULTATIVE. Vous pouvez
activer/désactiver la sauvegarde à tout moment dans les Paramètres."""


IA_TEXT = """UTILISATION ANONYMISÉE POUR ÉTUDE DE MARCHÉ (FACULTATIF)

En acceptant cette option, vous autorisez TEAM NOVA à extraire
périodiquement de votre base des données ANONYMISÉES pour :

  1. ÉTUDIER LE MARCHÉ PHARMACEUTIQUE
     Comprendre les tendances de consommation, les produits les
     plus vendus par région, les variations saisonnières.

  2. AMÉLIORER NOS MODÈLES D'INTELLIGENCE ARTIFICIELLE
     Développer des outils d'aide à la décision pour les pharmacies
     (prévision de stock, suggestions de réapprovisionnement).

DONNÉES EXTRAITES (ANONYMISÉES) :
  ✓ Noms de produits vendus
  ✓ Catégories de produits
  ✓ Quantités vendues
  ✓ Prix de vente (agrégés, sans lien avec des clients)
  ✓ Statistiques journalières et horaires
  ✓ Nombre de ventes par jour

DONNÉES JAMAIS EXTRAITES :
  ✗ Noms des clients
  ✗ Téléphones, emails, adresses des clients
  ✗ Noms des utilisateurs (caissiers, admins)
  ✗ Nom de votre pharmacie
  ✗ Adresse IP, identifiants machine
  ✗ Toute information permettant de vous identifier

CONFIDENTIALITÉ :
  • Un identifiant unique et irréversible (hash) remplace
    le nom de votre pharmacie
  • Impossible de relier les données à votre établissement
  • Aucune transmission automatique : les extractions sont
    faites manuellement par le développeur avec votre accord

DROIT DE RETRAIT :
Vous pouvez retirer votre consentement à tout moment en modifiant
cette option dans les Paramètres. Les extractions futures seront
alors refusées.

Cette option est TOTALEMENT FACULTATIVE. Refuser n'a AUCUNE
conséquence sur l'utilisation de Nova Pharma. Conformément aux
lois sur la protection des données, votre refus est libre et
sans justification."""


# ══════════════════════════════════════════════════════════════════
# Wizard principal
# ══════════════════════════════════════════════════════════════════
class Configuration(QtWidgets.QWizard, Ui_Wizard):

    # IDs des pages (ordre imposé par la .ui)
    PAGE_TYPE           = 0
    PAGE_WELCOME        = 1
    PAGE_IDENTITY       = 2
    PAGE_CONTACT        = 3
    PAGE_PHARMACY       = 4
    PAGE_SETTINGS       = 5
    PAGE_SUMMARY        = 6
    PAGE_CLIENT_CONFIG  = 7
    PAGE_CLIENT_SUMMARY = 8

    def __init__(self):
        super().__init__()

        # Images
        self.path_picture = None
        self.path_logo = None

        # Choix du type d'installation
        self._type_choice = None   # "serveur" | "client"

        # État du test de connexion client
        self._client_test_ok = False

        # Installe l'UI de base
        self.setupUi(self)
        fix_all_spinboxes(self)

        # Corrections valeurs par défaut
        self.input_profit_margin.setMinimum(0.0)
        self.input_profit_margin.setMaximum(100.0)
        self.input_profit_margin.setValue(30.0)
        self.input_profit_margin.setSuffix(" %")

        # Initialisation DB
        self._init_database()

        # Connexions
        self._connect_base_signals()
        self._connect_type_page()

        # État initial
        self._update_password_hint()
        self._update_age_from_dob()

        self.input_nationality.addItems(NATIONALITY_LIST)

    # ------------------------------------------------------------------
    # DB
    # ------------------------------------------------------------------
    def _init_database(self):
        try:
            db.get_conn()
            seed.run()
        except Exception as e:
            logging.exception("Erreur initialisation DB")
            QtWidgets.QMessageBox.critical(
                self, "Erreur fatale",
                f"Impossible d'initialiser la base :\n{e}")
            raise

    # ------------------------------------------------------------------
    # Page "Type" — cartes cliquables
    # ------------------------------------------------------------------
    def _connect_type_page(self):
        """Connecte les cartes et radios de la page Type."""
        # Cartes cliquables (filtre d'événement)
        self.type_card_server.installEventFilter(self)
        self.type_card_client.installEventFilter(self)

        # Radios
        self.radio_type_server.toggled.connect(
            lambda checked: checked and self._on_type_selected("serveur"))
        self.radio_type_client.toggled.connect(
            lambda checked: checked and self._on_type_selected("client"))

    def eventFilter(self, obj, event):
        """Rend les cartes cliquables (n'importe où dans le cadre)."""
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if obj is self.type_card_server:
                self.radio_type_server.setChecked(True)
                return True
            if obj is self.type_card_client:
                self.radio_type_client.setChecked(True)
                return True
        return super().eventFilter(obj, event)

    def _on_type_selected(self, choice: str):
        self._type_choice = choice

        # Met à jour le property CSS des cartes
        for card, name in (
                (self.type_card_server, "serveur"),
                (self.type_card_client, "client"),
        ):
            card.setProperty(
                "selected",
                "true" if name == choice else "false")
            card.style().unpolish(card)
            card.style().polish(card)

    # ------------------------------------------------------------------
    # Connexions de base
    # ------------------------------------------------------------------
    def _connect_base_signals(self):
        # Photo & logo
        self.btn_upload_photo.clicked.connect(self.Load_picture)
        self.btn_upload_logo.clicked.connect(self.Load_logo)

        # Mot de passe
        self.input_password.textChanged.connect(self._update_password_hint)
        self.input_password_confirm.textChanged.connect(
            self._update_password_hint)

        # Âge auto
        self.input_date_of_birth.dateChanged.connect(
            self._update_age_from_dob)

        # Récap dynamique
        for w in (self.input_first_name, self.input_name,
                  self.input_last_name, self.input_email,
                  self.input_phone, self.input_name_pharmacy,
                  self.input_adress):
            w.textChanged.connect(self._refresh_summary)
        self.input_type_pharmacy.currentIndexChanged.connect(
            self._refresh_summary)
        self.input_profit_margin.valueChanged.connect(self._refresh_summary)

        # Page client config
        self.btn_client_test.clicked.connect(self._on_client_test)
        self.input_client_host.textChanged.connect(self._on_client_input_changed)

        # Finish
        self.button(self.WizardButton.FinishButton).clicked.connect(
            self._on_finish)

    def _on_client_input_changed(self):
        self._client_test_ok = False
        self._set_client_test_result(
            "Saisissez l'adresse IP puis cliquez sur "
            "« Tester la connexion ».", "info")

    # ------------------------------------------------------------------
    # Navigation dynamique
    # ------------------------------------------------------------------
    def nextId(self) -> int:
        current = self.currentId()

        # Page 0 → choix du flux
        if current == self.PAGE_TYPE:
            if self._type_choice == "serveur":
                return self.PAGE_WELCOME
            if self._type_choice == "client":
                return self.PAGE_CLIENT_CONFIG
            return self.PAGE_TYPE

        # Fin du wizard serveur
        if current == self.PAGE_SUMMARY:
            return -1

        # Config client → Résumé client
        if current == self.PAGE_CLIENT_CONFIG:
            return self.PAGE_CLIENT_SUMMARY

        # Fin du wizard client
        if current == self.PAGE_CLIENT_SUMMARY:
            return -1

        # Navigation séquentielle par défaut
        pid_list = self.pageIds()
        try:
            idx = pid_list.index(current)
            if idx + 1 < len(pid_list):
                return pid_list[idx + 1]
        except ValueError:
            pass
        return -1

    # ------------------------------------------------------------------
    # Âge auto
    # ------------------------------------------------------------------
    def _update_age_from_dob(self):
        dob = self.input_date_of_birth.date()
        today = date.today()
        age = today.year - dob.year() - (
            (today.month, today.day) < (dob.month(), dob.day()))
        self.input_age.setValue(max(0, min(age, 120)))

    # ------------------------------------------------------------------
    # Mot de passe
    # ------------------------------------------------------------------
    def _password_status(self):
        pwd = self.input_password.text()
        confirm = self.input_password_confirm.text()

        if not pwd and not confirm:
            return False, ""
        if len(pwd) < PWD_MIN_LENGTH:
            return False, (
                f"Minimum {PWD_MIN_LENGTH} caractères "
                f"({len(pwd)}/{PWD_MIN_LENGTH}).")
        if not confirm:
            return False, "Confirmez le mot de passe."
        if pwd != confirm:
            return False, "Les mots de passe ne correspondent pas."
        return True, "Mot de passe valide"

    def _update_password_hint(self):
        valide, msg = self._password_status()
        self.label_pwd_error.setText(msg)
        self.label_pwd_error.setProperty(
            "valid", "true" if valide else "false")
        self.label_pwd_error.style().unpolish(self.label_pwd_error)
        self.label_pwd_error.style().polish(self.label_pwd_error)

    # ------------------------------------------------------------------
    # Validation par page
    # ------------------------------------------------------------------
    def validateCurrentPage(self) -> bool:
        pid = self.currentId()

        # Page type
        if pid == self.PAGE_TYPE:
            if self._type_choice not in ("serveur", "client"):
                QtWidgets.QMessageBox.warning(
                    self, "Type d'installation",
                    "Choisissez 'Serveur' ou 'Client'.")
                return False
            return True

        # Page welcome (carte Pharmacien)
        if pid == self.PAGE_WELCOME:
            return True

        # Pages serveur
        if pid == self.PAGE_IDENTITY:
            return self._validate_identity_page()
        if pid == self.PAGE_CONTACT:
            return self._validate_contact_page()
        if pid == self.PAGE_PHARMACY:
            return self._validate_pharmacy_page()
        if pid == self.PAGE_SETTINGS:
            return self._validate_settings_page()
        if pid == self.PAGE_SUMMARY:
            return self._validate_summary_page()

        # Page client config
        if pid == self.PAGE_CLIENT_CONFIG:
            return self._validate_client_config_page()

        return True

    def _validate_identity_page(self):
        erreurs = []
        prenom = self.input_first_name.text().strip()
        nom = self.input_name.text().strip()
        post_nom = self.input_last_name.text().strip()

        if not NAME_REGEX.match(prenom):
            erreurs.append("• Prénom invalide (2 à 50 lettres).")
        if not NAME_REGEX.match(nom):
            erreurs.append("• Nom invalide (2 à 50 lettres).")
        if not NAME_REGEX.match(post_nom):
            erreurs.append("• Post-nom invalide (2 à 50 lettres).")

        dob = self.input_date_of_birth.date()
        if dob > QtCore.QDate.currentDate():
            erreurs.append("• Date de naissance future interdite.")
        elif self.input_age.value() < 10:
            erreurs.append("• Âge minimum : 10 ans.")

        if self.input_nationality.currentIndex() < 0:
            erreurs.append("• Sélectionnez une nationalité.")
        if not self.path_picture:
            erreurs.append("• Photo de profil requise.")

        if erreurs:
            QtWidgets.QMessageBox.warning(
                self, "Champs invalides", "\n".join(erreurs))
            return False
        return True

    def _validate_contact_page(self):
        erreurs = []
        email = self.input_email.text().strip()
        if not EMAIL_REGEX.match(email):
            erreurs.append("• Email invalide.")

        numero = self.input_phone.text().strip().replace(" ", "")
        if not PHONE_REGEX.fullmatch(numero):
            erreurs.append(
                "• Numéro invalide (+243XXXXXXXXX ou 0XXXXXXXXX).")

        valide_pwd, msg_pwd = self._password_status()
        if not valide_pwd:
            erreurs.append(f"• {msg_pwd or 'Mot de passe requis.'}")

        if erreurs:
            QtWidgets.QMessageBox.warning(
                self, "Champs invalides", "\n".join(erreurs))
            return False
        return True

    def _validate_pharmacy_page(self):
        erreurs = []
        if len(self.input_name_pharmacy.text().strip()) < 2:
            erreurs.append("• Nom pharmacie obligatoire.")
        if self.input_type_pharmacy.currentIndex() < 0:
            erreurs.append("• Type d'officine requis.")

        email = self.input_email_pharmacy.text().strip()
        if not email:
            erreurs.append("• Email officine obligatoire.")
        elif not EMAIL_REGEX.match(email):
            erreurs.append("• Email officine invalide.")

        numero = self.input_phone_pharmacy.text().strip().replace(" ", "")
        if not PHONE_REGEX.fullmatch(numero):
            erreurs.append("• Téléphone officine invalide.")

        if len(self.input_adress.text().strip()) < ADDRESS_MIN_LEN:
            erreurs.append("• Adresse requise.")

        if erreurs:
            QtWidgets.QMessageBox.warning(
                self, "Champs invalides", "\n".join(erreurs))
            return False
        return True

    def _validate_settings_page(self):
        erreurs = []
        if self.input_low_stock_threshold.value() <= 0:
            erreurs.append("• Seuil stock > 0.")
        if self.input_profit_margin.value() <= 0:
            erreurs.append("• Marge > 0.")
        if erreurs:
            QtWidgets.QMessageBox.warning(
                self, "Champs invalides", "\n".join(erreurs))
            return False
        return True

    def _validate_summary_page(self):
        checkbox = getattr(self, "checkbox_cgu", None)
        if checkbox is None:
            return True
        if not checkbox.isChecked():
            QtWidgets.QMessageBox.warning(
                self, "Conditions requises",
                "Acceptez les conditions d'utilisation.")
            return False
        return True

    def _validate_client_config_page(self):
        if not self._client_test_ok:
            QtWidgets.QMessageBox.warning(
                self, "Test requis",
                "Testez la connexion au serveur avant de continuer.")
            return False

        # Persiste la config client
        host = self.input_client_host.text().strip()
        port = self.input_client_port.value()
        try:
            with db.transaction():
                db.set_config("server_mode", "client", type_="str")
                db.set_config("server_host", host, type_="str")
                db.set_config("server_port", port, type_="int")
                db.set_config("client_configured", "1", type_="str")
                db.set_config("first_time", False, type_="bool")
            logging.info("Config client enregistrée : %s:%d", host, port)
            return True
        except Exception:
            logging.exception("Erreur sauvegarde config client")
            return False

    # ------------------------------------------------------------------
    # Récap
    # ------------------------------------------------------------------
    def _refresh_summary(self):
        parties = [
            self.input_first_name.text().strip(),
            self.input_name.text().strip(),
            self.input_last_name.text().strip(),
        ]
        nom_complet = " ".join(p for p in parties if p) or "—"
        self.sc_name_value.setText(nom_complet)
        self.sc_email_value.setText(self.input_email.text().strip() or "—")
        self.sc_phone_value.setText(self.input_phone.text().strip() or "—")
        self.sc_pname_value.setText(
            self.input_name_pharmacy.text().strip() or "—")
        self.sc_ptype_value.setText(
            self.input_type_pharmacy.currentText() or "—")
        self.sc_addr_value.setText(
            self.input_adress.text().strip() or "—")
        self.sc_margin_value.setText(
            f"{self.input_profit_margin.value():.1f} %")

    # ------------------------------------------------------------------
    # Photo & Logo
    # ------------------------------------------------------------------
    def Load_picture(self):
        chemin, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Sélectionner une photo",
            os.path.expanduser("~"),
            filter="Images (*.jpg *.jpeg *.png)")
        if not chemin:
            return
        self.path_picture = chemin
        self.View_picture()

    def View_picture(self):
        if not self.path_picture:
            return
        pixmap = QtGui.QPixmap(self.path_picture)
        if pixmap.isNull():
            QtWidgets.QMessageBox.warning(
                self, "Image invalide", "Fichier invalide.")
            self.path_picture = None
            return
        if pixmap.width() > 800:
            pixmap = pixmap.scaledToWidth(
                800, QtCore.Qt.SmoothTransformation)
        os.makedirs("Img", exist_ok=True)
        pixmap.save(os.path.join(
            "Img", os.path.basename(self.path_picture)))
        self.photo_label.setPixmap(pixmap)

    def Load_logo(self):
        chemin, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Sélectionner un logo",
            os.path.expanduser("~"),
            filter="Images (*.jpg *.jpeg *.png)")
        if not chemin:
            return
        self.path_logo = chemin
        self.View_logo()

    def View_logo(self):
        if not self.path_logo:
            return
        pixmap = QtGui.QPixmap(self.path_logo)
        if pixmap.isNull():
            QtWidgets.QMessageBox.warning(
                self, "Image invalide", "Fichier invalide.")
            self.path_logo = None
            return
        if pixmap.width() > 600:
            pixmap = pixmap.scaledToWidth(
                600, QtCore.Qt.SmoothTransformation)
        os.makedirs("Img", exist_ok=True)
        pixmap.save(os.path.join(
            "Img", os.path.basename(self.path_logo)))
        self.logo_label.setPixmap(pixmap)

    # ------------------------------------------------------------------
    # Test connexion client
    # ------------------------------------------------------------------
    def _on_client_test(self):
        host = self.input_client_host.text().strip()
        port = self.input_client_port.value()

        if not host:
            self._set_client_test_result(
                "Adresse IP manquante.", "error")
            return

        self._set_client_test_result(
            "Test de connexion en cours…", "pending")
        QtWidgets.QApplication.processEvents()

        try:
            url = f"http://{host}:{port}/api/sante"
            r = httpx.get(url, timeout=5.0)

            if r.status_code == 200:
                data = r.json()
                version = data.get("version", "?")
                users = data.get("utilisateurs_actifs", "?")
                self._set_client_test_result(
                    f"Serveur joignable — Version {version} — "
                    f"{users} utilisateur(s) actif(s)",
                    "success")
                self._client_test_ok = True
            else:
                self._set_client_test_result(
                    f"Réponse inattendue (HTTP {r.status_code})",
                    "error")
                self._client_test_ok = False

        except httpx.ConnectError:
            self._set_client_test_result(
                "Connexion refusée. Vérifiez que le serveur est allumé "
                "et que vous êtes sur le même réseau.",
                "error")
            self._client_test_ok = False

        except httpx.TimeoutException:
            self._set_client_test_result(
                "Délai dépassé (5 s). Le serveur ne répond pas.",
                "error")
            self._client_test_ok = False

        except Exception as e:
            self._set_client_test_result(f"Erreur : {e}", "error")
            self._client_test_ok = False

    def _set_client_test_result(self, msg: str, status: str):
        lbl = self.label_client_test_result
        lbl.setText(msg)
        lbl.setProperty("status", status)
        lbl.style().unpolish(lbl)
        lbl.style().polish(lbl)

    # ------------------------------------------------------------------
    # Initialisation de la page client summary
    # ------------------------------------------------------------------
    def _fill_client_summary(self):
        try:
            host = db.get_config("server_host", "?")
            port = db.get_config("server_port", 5001)
            self.client_summary_details.setText(
                f"Serveur : {host}:{port}")
        except Exception:
            pass

    # ------------------------------------------------------------------
    # FINISH
    # ------------------------------------------------------------------
    def _on_finish(self):
        if self._type_choice == "client":
            self._fill_client_summary()
            QtWidgets.QMessageBox.information(
                self, "Client configuré",
                "Ce poste est maintenant configuré comme client.\n\n"
                "Connectez-vous avec vos identifiants.")
            return

        # Serveur : consentements + persistance
        dialog = ConsentementDialog(self)
        if dialog.exec() != QtWidgets.QDialog.Accepted:
            return
        accepte_sauvegarde, accepte_ia, accepte_cgu = dialog.resultats()

        try:
            self._persist_serveur(accepte_sauvegarde, accepte_ia)
        except Exception as e:
            logging.exception("Échec enregistrement config serveur")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'enregistrer :\n{e}")
            return

        QtWidgets.QMessageBox.information(
            self, "Configuration terminée",
            "NovaPharma est prêt (mode Serveur).")

    def _persist_serveur(self, accepte_sauvegarde: bool,
                          accepte_ia: bool):
        prenom = self.input_first_name.text().strip()
        nom = self.input_name.text().strip().upper()
        post_nom = self.input_last_name.text().strip().upper()
        sexe = "M" if self.radio_homme.isChecked() else "F"
        dob = self.input_date_of_birth.date().toString("yyyy-MM-dd")
        nationalite = self.input_nationality.currentText()

        email = self.input_email.text().strip().lower()
        numero = self.input_phone.text().strip().replace(" ", "")
        mdp = self.input_password.text()

        nom_pharmacie = self.input_name_pharmacy.text().strip().upper()
        type_pharmacie = PHARMACY_TYPE_MAP.get(
            self.input_type_pharmacy.currentText(), "MOYENNE")
        email_pharmacie = self.input_email_pharmacy.text().strip().lower()
        numero_pharmacie = self.input_phone_pharmacy.text().strip().replace(
            " ", "")
        adresse = self.input_adress.text().strip()

        seuil_stock = self.input_low_stock_threshold.value()
        marge = self.input_profit_margin.value()

        path_image_rel = (
            os.path.join("Img", os.path.basename(self.path_picture))
            if self.path_picture else None)
        path_logo_rel = (
            os.path.join("Img", os.path.basename(self.path_logo))
            if self.path_logo else None)

        with db.transaction():
            user_id = db.new_id()

            db.execute(
                """INSERT INTO Utilisateur
                (id, identifiant, prenom, nom, post_nom, sexe,
                    date_naissance, nationalite, email, numero,
                    numero_caisse, role, pswd_hash, path_image, actif)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
                (user_id, email, prenom, nom, post_nom, sexe,
                 dob, nationalite, email, numero, "A", "ADMIN",
                 bcrypt.hashpw(mdp.encode("utf-8"),
                               bcrypt.gensalt()).decode("utf-8"),
                 path_image_rel))

            db.execute(
                """INSERT INTO Pharmacie
                (id, nom, type, email, numero, adresse,
                    path_logo, seuil_stock, marge_benefice)
                VALUES (1,?,?,?,?,?,?,?,?)""",
                (nom_pharmacie, type_pharmacie, email_pharmacie,
                 numero_pharmacie, adresse, path_logo_rel,
                 seuil_stock, marge))

            db.set_config("nom_entreprise", nom_pharmacie)
            db.set_config("indice_vente", marge / 100.0)
            db.set_config("chiffre_affaire_periode", "Mois")
            db.set_config("qrcode_actif", False)
            db.set_config("impression_facture_auto", False)
            db.set_config("pc_name", socket.gethostname())
            db.set_config("server_mode", "serveur", type_="str")

            db.record_consent(
                user_id, "SAUVEGARDE",
                seed.VERSION_SAUVEGARDE,
                accepte_sauvegarde,
                seed.CONSENTEMENT_SAUVEGARDE_V1)

            db.record_consent(
                user_id, "IA_ANONYMISEE",
                seed.VERSION_IA,
                accepte_ia,
                seed.CONSENTEMENT_IA_V1)

            cgu_texte = getattr(seed, "CONSENTEMENT_CGU_V1",
                                 "CGU NovaPharma v1")
            db.record_consent(
                user_id, "CGU",
                getattr(seed, "VERSION_CGU", "1.0"),
                True, cgu_texte)

            db.set_config("sauvegarde_active", accepte_sauvegarde)
            db.set_config("ia_consentement", accepte_ia)

            if accepte_sauvegarde:
                db.set_config("consentement_sauvegarde_version",
                              seed.VERSION_SAUVEGARDE)
            if accepte_ia:
                db.set_config("ia_consentement_version", seed.VERSION_IA)

            db.set_config("first_time", False)

    # ------------------------------------------------------------------
    def closeEvent(self, event):
        try:
            db.close()
        finally:
            super().closeEvent(event)


class ConsentementDialog(QtWidgets.QDialog):
    """Dialogue de consentements v2.0 avec 3 sections séparées."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Consentements — Nova Pharma v2.0")
        self.setMinimumSize(800, 720)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("""
            QDialog { background: #f0f4f8; }
            QLabel { color: #334155; background: transparent; }
            QLabel#title {
                color: #023E8A; font-size: 20px; font-weight: 800;
            }
            QLabel#sub {
                color: #64748b; font-size: 12px;
            }
            QFrame#card {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QFrame#card_mandatory {
                background: #ffffff;
                border: 2px solid #dc2626;
                border-radius: 12px;
            }
            QFrame#card_optional {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QFrame#card QLabel { background: transparent; }
            QTextEdit {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                color: #1e293b;
                font-size: 12px;
            }
            QCheckBox {
                font-size: 13px; font-weight: 600;
                color: #0f172a; spacing: 10px;
            }
            QCheckBox#cb_mandatory {
                color: #dc2626; font-weight: 700;
            }
            QLabel#badge_mandatory {
                background: #fef2f2; color: #b91c1c;
                border: 1px solid #fecaca; border-radius: 6px;
                padding: 3px 10px; font-size: 10px; font-weight: 800;
            }
            QLabel#badge_optional {
                background: #f0fdf4; color: #15803d;
                border: 1px solid #bbf7d0; border-radius: 6px;
                padding: 3px 10px; font-size: 10px; font-weight: 800;
            }
            QLabel#badge_disabled {
                background: #f8fafc; color: #64748b;
                border: 1px solid #e2e8f0; border-radius: 6px;
                padding: 3px 10px; font-size: 10px; font-weight: 800;
            }
            QPushButton {
                background: #0077B6; color: white;
                border: none; border-radius: 10px;
                padding: 10px 24px; font-weight: 700;
                font-size: 12px; min-width: 140px;
            }
            QPushButton:hover { background: #023E8A; }
            QPushButton#btn_cancel {
                background: transparent; color: #64748b;
                border: 1.5px solid #e2e8f0;
            }
            QPushButton#btn_cancel:hover {
                background: #fef2f2; color: #dc2626;
                border-color: #fecaca;
            }
        """)

        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(12)

        # Header
        t = QtWidgets.QLabel("Consentements & Conditions")
        t.setObjectName("title")
        v.addWidget(t)

        s = QtWidgets.QLabel(
            "Lisez chaque section. Les CGU sont OBLIGATOIRES. Les 2 autres "
            "sont FACULTATIVES et indépendantes. Vous pouvez les refuser "
            "sans aucune conséquence sur l'utilisation de Nova Pharma.")
        s.setObjectName("sub")
        s.setWordWrap(True)
        v.addWidget(s)

        # Scroll
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        content = QtWidgets.QWidget()
        content.setStyleSheet("background: transparent;")
        cv = QtWidgets.QVBoxLayout(content)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(14)

        # ─── 1. CGU (OBLIGATOIRE) ───
        self.check_cgu = self._make_section(
            cv, "1. Conditions Générales d'Utilisation",
            CGU_TEXT,
            "J'ai lu et j'accepte les CGU de Nova Pharma. "
            "(OBLIGATOIRE)",
            checked=True,
            mandatory=True,
            badge_text="OBLIGATOIRE")

        # ─── 2. Sauvegarde (FACULTATIF, coché) ───
        self.check_sauvegarde = self._make_section(
            cv, "2. Sauvegarde automatique des données",
            SAUVEGARDE_TEXT,
            "J'accepte la sauvegarde automatique de mes données. "
            "(FACULTATIF - recommandé)",
            checked=True,
            mandatory=False,
            badge_text="FACULTATIF")

        # ─── 3. IA anonymisée (FACULTATIF, DÉCOCHÉ) ───
        self.check_ia = self._make_section(
            cv, "3. Extraction anonymisée pour étude de marché",
            IA_TEXT,
            "J'autorise l'extraction de données ANONYMISÉES pour "
            "l'étude de marché et l'amélioration des modèles IA. "
            "(FACULTATIF - décoché par défaut)",
            checked=False,
            mandatory=False,
            badge_text="FACULTATIF - NON COCHÉ")

        cv.addStretch()
        scroll.setWidget(content)
        v.addWidget(scroll, 1)

        # Footer
        hf = QtWidgets.QHBoxLayout()
        hf.addStretch()

        btn_cancel = QtWidgets.QPushButton("Annuler")
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.clicked.connect(self.reject)
        hf.addWidget(btn_cancel)

        btn_ok = QtWidgets.QPushButton("Valider mes choix")
        btn_ok.clicked.connect(self._on_accept)
        hf.addWidget(btn_ok)
        v.addLayout(hf)

    def _make_section(self, layout, titre, texte, checkbox_text,
                      checked=False, mandatory=False, badge_text=""):
        """Crée une section avec texte détaillé + checkbox."""
        card = QtWidgets.QFrame()
        card.setObjectName("card_mandatory" if mandatory else "card_optional")
        cv = QtWidgets.QVBoxLayout(card)
        cv.setContentsMargins(20, 16, 20, 16)
        cv.setSpacing(10)

        # Titre + badge
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(10)

        tl = QtWidgets.QLabel(titre)
        tl.setStyleSheet(
            "color: #023E8A; font-size: 13px; font-weight: 800;")
        h.addWidget(tl)
        h.addStretch()

        if badge_text:
            badge = QtWidgets.QLabel(badge_text)
            if mandatory:
                badge.setObjectName("badge_mandatory")
            elif "NON COCHÉ" in badge_text:
                badge.setObjectName("badge_disabled")
            else:
                badge.setObjectName("badge_optional")
            h.addWidget(badge)

        cv.addLayout(h)

        # Texte
        txt = QtWidgets.QTextEdit()
        txt.setPlainText(texte)
        txt.setReadOnly(True)
        txt.setMinimumHeight(140)
        txt.setMaximumHeight(200)
        cv.addWidget(txt)

        # Checkbox
        chk = QtWidgets.QCheckBox(checkbox_text)
        chk.setChecked(checked)
        if mandatory:
            chk.setObjectName("cb_mandatory")
        cv.addWidget(chk)

        layout.addWidget(card)
        return chk

    def _on_accept(self):
        if not self.check_cgu.isChecked():
            QtWidgets.QMessageBox.warning(
                self, "CGU obligatoires",
                "Vous devez accepter les Conditions Générales "
                "d'Utilisation pour continuer.\n\n"
                "Les 2 autres options sont facultatives.")
            return
        self.accept()

    def resultats(self):
        return (
            self.check_sauvegarde.isChecked(),
            self.check_ia.isChecked(),
            self.check_cgu.isChecked(),
        )