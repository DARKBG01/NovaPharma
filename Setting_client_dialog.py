#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_client_dialog.py — Dialogue d'ajout / modification de client
=====================================================================
- Mode ajout        : client_id = None  → INSERT
- Mode modification : client_id = "..." → UPDATE
- Toggle "client anonyme" → génère ANON-YYYYMMDD-XXXX
"""

import logging
import re
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore

from Client.api_singleton import get_api, is_client_mode
from Database import db
from Interface_client_dialog import Ui_Dialog

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════
PHONE_REGEX = re.compile(r"^(?:\+243\d{9}|0\d{9})$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_REGEX  = re.compile(r"^[A-Za-zÀ-ÿ\-' ]{2,120}$")

ICON_CHECK_GRAY = ":/Icon/Icons/circle_white.svg"
ICON_CHECK_DONE = ":/Icon/Icons/check-circle_white.svg"


# ══════════════════════════════════════════════════════════════════
# Dialogue
# ══════════════════════════════════════════════════════════════════
class Setting_client_dialog(QtWidgets.QDialog, Ui_Dialog):

    client_saved = QtCore.Signal(str)   # id_client

    def __init__(self, parent=None, client_id: str = None, user_id: str = None):
        super().__init__(parent)
        self.setupUi(self)

        # Session
        self.client_id = client_id
        self.user_id = user_id
        self._client_data = None

        # Titre selon mode
        if self.client_id:
            self.setWindowTitle("Modifier client — Nova Pharma")
            self.sidebar_title.setText("Modifier le client")
            self.sidebar_lead.setText(
                "Mettez à jour les coordonnées du client.")
            self.brand_badge_text.setText("MODIFICATION CLIENT")
            self.panel_title.setText("Fiche client")
            self.btn_save.setText("Enregistrer les modifications")
            # En mode édition : on cache le toggle anonymat
            self.anon_box.setVisible(False)
        else:
            self.setWindowTitle("Nouveau client — Nova Pharma")

        # Connexions
        self._connect_signals()

        # Charge le client si mode edit
        if self.client_id:
            self._load_client()
            self._refresh_ui()

        self._update_progress()
        self.input_nom.setFocus()

    # ------------------------------------------------------------------
    # Signaux
    # ------------------------------------------------------------------
    def _connect_signals(self):
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self._on_save)

        self.input_nom.textChanged.connect(self._update_progress)
        self.input_numero.textChanged.connect(self._update_progress)

        self.anon_check.toggled.connect(self._on_anon_toggled)

        self.input_nom.returnPressed.connect(self._on_save)
        self.input_numero.returnPressed.connect(self._on_save)

    # ------------------------------------------------------------------
    # Toggle anonymat
    # ------------------------------------------------------------------
    def _on_anon_toggled(self, checked: bool):
        # Style du toggle
        self.anon_box.setProperty("on", "true" if checked else "false")
        self.anon_box.style().unpolish(self.anon_box)
        self.anon_box.style().polish(self.anon_box)

        # Bandeau d'information
        self.anon_banner.setVisible(checked)

        # Champs nom + numéro
        if checked:
            self.input_nom.clear()
            self.input_numero.clear()
            self.input_nom.setEnabled(False)
            self.input_numero.setEnabled(False)
            self.input_nom.setPlaceholderText("Non communiqué")
            self.input_numero.setPlaceholderText("Non communiqué")
            self.req_nom.setVisible(False)
            self.req_numero.setVisible(False)
        else:
            self.input_nom.setEnabled(True)
            self.input_numero.setEnabled(True)
            self.input_nom.setPlaceholderText("Ex : Jean Kabila")
            self.input_numero.setPlaceholderText("Ex : +243 800 000 000")
            self.req_nom.setVisible(True)
            self.req_numero.setVisible(True)

        self._update_progress()

    # ------------------------------------------------------------------
    # Génération identifiant anonyme
    # ------------------------------------------------------------------
    def _generate_anonymous_data(self) -> tuple[str, str]:
        """
        Génère (nom_anonyme, numero_anonyme) unique.
        Format : ANON-YYYYMMDD-XXXX (X = hex)
        """
        today = datetime.now().strftime("%Y%m%d")

        for _ in range(20):
            suffix = db.new_id().replace("-", "")[:4].upper()
            numero = f"ANON-{today}-{suffix}"
            try:
                exists = db.query_one(
                    "SELECT 1 FROM Client WHERE numero = ? LIMIT 1", (numero,))
                if not exists:
                    nom = f"Anonyme #{suffix}"
                    return nom, numero
            except Exception:
                logger.exception("Erreur vérification numéro anonyme")
                continue

        # Fallback
        import time
        numero = f"ANON-{today}-{int(time.time()) % 10000:04d}"
        return f"Anonyme #{numero[-4:]}", numero

    # ------------------------------------------------------------------
    # Chargement (mode edit)
    # ------------------------------------------------------------------
    def _load_client(self):
        try:
            row = db.query_one(
                """SELECT id, COALESCE(C_name, nom) AS nom,
                          numero, adresse, email, notes, sexe
                   FROM Client WHERE id = ? LIMIT 1""",
                (self.client_id,))
            self._client_data = dict(row) if row else None
        except Exception:
            logger.exception("Erreur chargement client")
            self._client_data = None

    def _refresh_ui(self):
        if not self._client_data:
            return
        c = self._client_data
        self.input_nom.setText(c.get("nom") or "")
        self.input_numero.setText(c.get("numero") or "")
        self.input_email.setText(c.get("email") or "")
        self.input_adresse.setText(c.get("adresse") or "")
        self.input_notes.setPlainText(c.get("notes") or "")

        # ─── Sexe ───
        sexe = (c.get("sexe") or "M").upper()
        if hasattr(self, "input_sexe"):
            self.input_sexe.setCurrentIndex(0 if sexe == "M" else 1)

    # ------------------------------------------------------------------
    # Progression
    # ------------------------------------------------------------------
    def _update_progress(self):
        is_anon = self.anon_check.isChecked()

        if is_anon:
            self._set_check(self.check_row_name, self.check_name_icon, True)
            self._set_check(self.check_row_phone, self.check_phone_icon, True)
            self.progress_bar.setValue(100)
            self.progress_label.setText("100 %")
            return

        nom_ok = len(self.input_nom.text().strip()) >= 2
        numero_ok = bool(PHONE_REGEX.match(
            self.input_numero.text().strip().replace(" ", "")))

        self._set_check(self.check_row_name, self.check_name_icon, nom_ok)
        self._set_check(self.check_row_phone, self.check_phone_icon, numero_ok)

        score = (50 if nom_ok else 0) + (50 if numero_ok else 0)
        self.progress_bar.setValue(score)
        self.progress_label.setText(f"{score} %")

    @staticmethod
    def _set_check(row, icon, done: bool):
        row.setProperty("done", "true" if done else "false")
        row.style().unpolish(row)
        row.style().polish(row)
        icon.setPixmap(QtGui.QPixmap(ICON_CHECK_DONE if done else ICON_CHECK_GRAY))

    # ------------------------------------------------------------------
    # Erreur
    # ------------------------------------------------------------------
    def _show_error(self, msg: str):
        self.label_error.setText(msg)
        self.error_box.setVisible(True)

    def _hide_error(self):
        self.error_box.setVisible(False)
        self.label_error.setText("")

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def _validate(self):
        is_anon = self.anon_check.isChecked()

        # Mode anonyme : pas de validation nom/numéro
        if is_anon:
            email = self.input_email.text().strip().lower()
            if email and not EMAIL_REGEX.match(email):
                return False, "Adresse email invalide."
            return True, ""

        # Mode normal
        nom = self.input_nom.text().strip()
        if not NAME_REGEX.match(nom):
            return False, "Nom invalide (2 à 120 caractères)."

        numero = self.input_numero.text().strip().replace(" ", "")
        if not PHONE_REGEX.match(numero):
            return False, "Numéro invalide. Format : +243XXXXXXXXX ou 0XXXXXXXXX."

        email = self.input_email.text().strip().lower()
        if email and not EMAIL_REGEX.match(email):
            return False, "Adresse email invalide."

        # Unicité du numéro
        try:
            q = "SELECT 1 FROM Client WHERE numero = ?"
            p = (numero,)
            if self.client_id:
                q += " AND id <> ?"
                p = (numero, self.client_id)
            if db.query_one(q + " LIMIT 1", p):
                return False, f"Un autre client a déjà le numéro {numero}."
        except Exception:
            logger.exception("Erreur vérification numéro")

        return True, ""

    # ------------------------------------------------------------------
    # Enregistrement
    # ------------------------------------------------------------------
    def _on_save(self):
        self._hide_error()
        valide, msg = self._validate()
        if not valide:
            self._show_error(msg)
            QtWidgets.QMessageBox.warning(self, "Champs invalides", msg)
            return

        is_anon = self.anon_check.isChecked()

        # ─── Récupère le sexe ───
        sexe = "M"
        if hasattr(self, "input_sexe"):
            sexe = "M" if self.input_sexe.currentIndex() == 0 else "F"

        # ═══ MODE CLIENT → API ═══
        if is_client_mode():
            try:
                api = get_api()
                if self.client_id:
                    data = {
                        "nom": self.input_nom.text().strip() or None,
                        "numero": self.input_numero.text().strip()
                                  .replace(" ", "") or None,
                        "email": self.input_email.text().strip().lower() or None,
                        "adresse": self.input_adresse.text().strip() or None,
                        "notes": self.input_notes.toPlainText().strip() or None,
                        "sexe": sexe,  # ← AJOUT
                    }
                    result = api.update_client(self.client_id, data)
                    new_id = result.get("id", self.client_id)
                else:
                    data = {
                        "anonyme": is_anon,
                        "nom": self.input_nom.text().strip() or None,
                        "numero": self.input_numero.text().strip()
                                  .replace(" ", "") or None,
                        "email": self.input_email.text().strip().lower() or None,
                        "adresse": self.input_adresse.text().strip() or None,
                        "notes": self.input_notes.toPlainText().strip() or None,
                        "sexe": sexe,  # ← AJOUT
                    }
                    result = api.create_client(data)
                    new_id = result.get("id")

                self.client_saved.emit(new_id)

                if is_anon and not self.client_id:
                    QtWidgets.QMessageBox.information(
                        self, "Client anonyme ajouté",
                        "Un client anonyme a été créé avec succès.")
                elif self.client_id:
                    QtWidgets.QMessageBox.information(
                        self, "Client modifié",
                        "Les informations ont été mises à jour.")
                else:
                    QtWidgets.QMessageBox.information(
                        self, "Client ajouté",
                        "Le client a été créé avec succès.")
                self.accept()
                return
            except Exception as e:
                logger.exception("Échec enregistrement client (API)")
                self._show_error(f"Erreur d'enregistrement : {e}")
                return

        # ═══ MODE AUTONOME / SERVEUR → DB locale ═══
        from Database import audit

        if is_anon:
            nom, numero = self._generate_anonymous_data()
            email = self.input_email.text().strip().lower() or None
            adresse = self.input_adresse.text().strip() or None
            notes = self.input_notes.toPlainText().strip() or None
        else:
            nom = self.input_nom.text().strip()
            numero = self.input_numero.text().strip().replace(" ", "")
            email = self.input_email.text().strip().lower() or None
            adresse = self.input_adresse.text().strip() or None
            notes = self.input_notes.toPlainText().strip() or None

        try:
            # ─── Snapshot AVANT si modification ───
            avant = None
            if self.client_id:
                avant = audit.snapshot(
                    "Client", "id", self.client_id)

            with db.transaction():
                if self.client_id:
                    db.execute(
                        """UPDATE Client
                           SET nom = ?, C_name = ?, numero = ?,
                               email = ?, adresse = ?, notes = ?, sexe = ?
                           WHERE id = ?""",
                        (nom, nom, numero, email, adresse, notes,
                         sexe, self.client_id))
                    new_id = self.client_id
                else:
                    new_id = db.new_id()
                    db.execute(
                        """INSERT INTO Client
                           (id, nom, numero, adresse, Id_client, C_name,
                            Montant_total, email, notes, sexe, actif)
                           VALUES (?,?,?,?,?,?,0,?,?,?,1)""",
                        (new_id, nom, numero, adresse, new_id, nom,
                         email, notes, sexe))

            # ═══ AUDIT ═══
            try:
                if self.client_id and avant:
                    # Modification
                    audit.trace_modif(
                        audit.ACTION_MODIF_CLIENT,
                        table="Client",
                        id_column="id",
                        id_value=self.client_id,
                        avant_snapshot=avant,
                        utilisateur_id=self.user_id,
                        cible_nom=nom,
                    )

                    # Trace spécifique si numéro change
                    old_num = (avant.get("numero") or "").replace(" ", "")
                    new_num = numero.replace(" ", "")
                    if old_num and old_num != new_num:
                        audit.log(
                            audit.ACTION_MODIF_CLIENT_NUMERO,
                            utilisateur_id=self.user_id,
                            cible_type="Client",
                            cible_id=self.client_id,
                            cible_nom=nom,
                            details={
                                "ancien_numero": old_num,
                                "nouveau_numero": new_num,
                            })
                else:
                    # Création
                    apres = audit.snapshot("Client", "id", new_id)
                    audit.log(
                        audit.ACTION_CREATION_CLIENT,
                        utilisateur_id=self.user_id,
                        cible_type="Client",
                        cible_id=new_id,
                        cible_nom=nom,
                        details={
                            "anonyme": is_anon,
                            "numero": numero,
                        },
                        apres=apres,
                    )
            except Exception:
                logger.exception("Erreur audit client")

            self.client_saved.emit(new_id)
            QtWidgets.QMessageBox.information(
                self, "Client enregistré",
                f"Client « {nom} » enregistré avec succès.")
            self.accept()
        except Exception as e:
            logger.exception("Échec enregistrement client")
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

    dlg = Setting_client_dialog(user_id="TEST")
    dlg.client_saved.connect(lambda cid: print(f"→ Enregistré : {cid}"))
    sys.exit(dlg.exec())