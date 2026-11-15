#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Login.py — Portail de connexion Nova Pharma
============================================
"""

import logging
from datetime import datetime, timedelta

from PySide6 import QtWidgets, QtGui, QtCore
import bcrypt

from Database import db, audit
from Client.api_singleton import get_api, is_client_mode
from Interface_login import Ui_LoginDialog
from Ui_helpers import fix_all_spinboxes


# ══════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════
MAX_FAILED_ATTEMPTS = 5
LOCK_DURATION_MIN   = 5

SETTINGS_ORG        = "NovaPharma"
SETTINGS_APP        = "Login"
KEY_LAST_USER       = "login/last_user"
KEY_REMEMBER        = "login/remember"
KEY_FAILED_COUNT    = "login/failed_count"
KEY_LOCK_UNTIL      = "login/lock_until"

ICON_APP            = ":/Icon/Icons/1758107223736.png"
ICON_EYE_OPEN       = ":/Icon/Icons/eye.svg"
ICON_EYE_CLOSED     = ":/Icon/Icons/eye-off.svg"


class LoginDialog(QtWidgets.QDialog, Ui_LoginDialog):

    login_success = QtCore.Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        fix_all_spinboxes(self)
        self.setWindowIcon(QtGui.QIcon(ICON_APP))
        self._center_on_screen()

        self.settings = QtCore.QSettings(SETTINGS_ORG, SETTINGS_APP)
        self._pwd_visible = False
        self.last_user_id = None
        self.last_role = None
        self.last_identifiant = None

        self._connect_signals()
        self._restore_settings()
        self._install_focus_effects()
        self._adapt_to_mode()

        if self.lineEdit_username.text():
            self.lineEdit_password.setFocus()
        else:
            self.lineEdit_username.setFocus()

    def _center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width()  - size.width())  // 2,
            (screen.height() - size.height()) // 2,
        )

    def _connect_signals(self):
        self.pushButton_login.clicked.connect(self._on_login_clicked)
        self.lineEdit_username.returnPressed.connect(self._on_login_clicked)
        self.lineEdit_password.returnPressed.connect(self._on_login_clicked)
        self.btn_toggle_pwd.clicked.connect(self._toggle_password)
        self.labelForgot.mousePressEvent = self._on_forgot_password
        self.labelHelp.linkActivated.connect(self._on_contact_support)

    def _adapt_to_mode(self):
        try:
            if is_client_mode():
                api = get_api()
                if api is not None:
                    self.setWindowTitle(
                        f"Nova Pharma — Client ({api.base_url})")
        except Exception:
            pass

    def _install_focus_effects(self):
        for line, frame in (
            (self.lineEdit_username, self.frameUsernameField),
            (self.lineEdit_password, self.framePasswordField),
        ):
            orig_in  = line.focusInEvent
            orig_out = line.focusOutEvent

            def make_in(f, orig):
                def handler(ev):
                    f.setProperty("focused", "true")
                    f.style().unpolish(f)
                    f.style().polish(f)
                    orig(ev)
                return handler

            def make_out(f, orig):
                def handler(ev):
                    f.setProperty("focused", "false")
                    f.style().unpolish(f)
                    f.style().polish(f)
                    orig(ev)
                return handler

            line.focusInEvent  = make_in(frame, orig_in)
            line.focusOutEvent = make_out(frame, orig_out)

    def _toggle_password(self):
        self._pwd_visible = not self._pwd_visible
        if self._pwd_visible:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.btn_toggle_pwd.setIcon(QtGui.QIcon(ICON_EYE_CLOSED))
        else:
            self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.btn_toggle_pwd.setIcon(QtGui.QIcon(ICON_EYE_OPEN))

    def _restore_settings(self):
        remember = self.settings.value(KEY_REMEMBER, True, type=bool)
        self.checkBox_remember.setChecked(remember)
        if remember:
            last_user = self.settings.value(KEY_LAST_USER, "", type=str)
            if last_user:
                self.lineEdit_username.setText(last_user)

    def _save_settings(self, identifiant: str):
        remember = self.checkBox_remember.isChecked()
        self.settings.setValue(KEY_REMEMBER, remember)
        if remember:
            self.settings.setValue(KEY_LAST_USER, identifiant)
        else:
            self.settings.remove(KEY_LAST_USER)

    def _get_failed_count(self) -> int:
        return self.settings.value(KEY_FAILED_COUNT, 0, type=int)

    def _register_failure(self):
        count = self._get_failed_count() + 1
        self.settings.setValue(KEY_FAILED_COUNT, count)
        if count >= MAX_FAILED_ATTEMPTS:
            until = datetime.now() + timedelta(minutes=LOCK_DURATION_MIN)
            self.settings.setValue(KEY_LOCK_UNTIL, until.isoformat())
            self.settings.setValue(KEY_FAILED_COUNT, 0)
            logging.warning("Login verrouillé jusqu'à %s", until)

    def _reset_failures(self):
        self.settings.setValue(KEY_FAILED_COUNT, 0)
        self.settings.remove(KEY_LOCK_UNTIL)

    def _check_locked(self) -> tuple[bool, int]:
        iso = self.settings.value(KEY_LOCK_UNTIL, "", type=str)
        if not iso:
            return False, 0
        try:
            until = datetime.fromisoformat(iso)
        except ValueError:
            return False, 0
        delta = (until - datetime.now()).total_seconds()
        if delta <= 0:
            self._reset_failures()
            return False, 0
        return True, int(delta // 60) + 1

    def _show_error(self, message: str):
        self.labelErrorText.setText(message)
        self.frameError.setVisible(True)
        self.frameError.style().unpolish(self.frameError)
        self.frameError.style().polish(self.frameError)

    def _hide_error(self):
        self.frameError.setVisible(False)
        self.labelErrorText.setText("")

    def _set_loading(self, loading: bool):
        self.pushButton_login.setEnabled(not loading)
        self.lineEdit_username.setEnabled(not loading)
        self.lineEdit_password.setEnabled(not loading)
        self.btn_toggle_pwd.setEnabled(not loading)

        if loading:
            self.pushButton_login.setText("  Connexion en cours…")
            self.setCursor(QtCore.Qt.WaitCursor)
            QtWidgets.QApplication.processEvents()
        else:
            self.pushButton_login.setText("  Se connecter au portail")
            self.unsetCursor()

    def _on_login_clicked(self):
        self._hide_error()

        locked, minutes = self._check_locked()
        if locked:
            self._show_error(
                f"Trop de tentatives échouées. "
                f"Réessayez dans {minutes} minute(s).")
            return

        identifiant = self.lineEdit_username.text().strip().lower()
        password    = self.lineEdit_password.text()

        if not identifiant:
            self._show_error("Veuillez saisir votre identifiant ou email.")
            self.lineEdit_username.setFocus()
            return

        if not password:
            self._show_error("Veuillez saisir votre mot de passe.")
            self.lineEdit_password.setFocus()
            return

        if is_client_mode():
            self._login_via_api(identifiant, password)
        else:
            self._login_local(identifiant, password)

    def _login_via_api(self, identifiant: str, password: str):
        api = get_api()
        if api is None:
            self._show_error("Mode client configuré mais API non initialisée.")
            return

        self._set_loading(True)
        try:
            data = api.login(identifiant, password)
            user_api = data.get("user", {})

            self._set_loading(False)
            self._reset_failures()
            self._save_settings(identifiant)

            self.last_user_id = user_api.get("id")
            self.last_role = user_api.get("role")
            self.last_identifiant = user_api.get("identifiant")

            if user_api.get("must_change_password"):
                logging.info("Changement de mdp forcé pour %s", user_api.get("identifiant"))
                self._log_success(user_api, note="force_password_change")

                if not self._force_change_password_api(user_api, password):
                    self.lineEdit_password.clear()
                    self.lineEdit_password.setFocus()
                    return

            logging.info("Connexion (client) réussie : %s (%s)", identifiant, user_api.get("role"))

            self._log_success(user_api)
            self.login_success.emit(
                user_api.get("id"),
                user_api.get("role"),
                user_api.get("identifiant"))
            self.accept()


        except Exception as e:

            self._set_loading(False)

            msg = str(e)

            low = msg.lower()

            # ═══ 402 : LICENCE SERVEUR EXPIRÉE ═══

            if "402" in msg or "licence" in low or "license" in low:
                self._show_error(

                    "⚠ La licence du serveur a expiré.\n\n"

                    "Contactez l'administrateur ou TEAM NOVA pour "

                    "la renouveler.\n\n"

                    "WhatsApp : +243 808 775 085\n"

                    "Email : teamnovaoff@gmail.com")

                self.lineEdit_password.clear()

                self.lineEdit_password.setFocus()

                return

            # ═══ 403 : poste non autorisé ═══

            if "403" in msg or "autorisé" in low or "forbidden" in low:
                self._show_error(

                    "Ce poste n'est pas autorisé pour ce rôle.\n"

                    "Contactez l'administrateur réseau.")

                self.lineEdit_password.clear()

                self.lineEdit_password.setFocus()

                return


            self._register_failure()

            if "401" in msg or "incorrect" in low:
                self._show_error("Identifiant ou mot de passe incorrect.")
            elif "indisponible" in low or "connect" in low or "refusée" in low:
                self._show_error("Serveur injoignable. Vérifiez que le serveur est allumé et que vous êtes connecté au réseau.")
            elif "fermé" in low or "503" in msg or "horaires" in low:
                self._show_error("Serveur fermé (hors horaires d'ouverture).")
            else:
                self._show_error(f"Erreur de connexion : {msg}")

            self.lineEdit_password.clear()
            self.lineEdit_password.setFocus()

    def _force_change_password_api(self, user: dict, old_plain: str) -> bool:
        try:
            from Client.api_singleton import get_api
            api_check = get_api()
            logging.info(
                "→ _force_change_password_api | api=%s | token=%s",
                "OK" if api_check else "None",
                "PRÉSENT" if (api_check and api_check.token) else "❌ ABSENT")

            from Setting_change_password import Setting_change_password
            dlg = Setting_change_password(
                parent=self,
                user_id=user["id"],
                old_password_plain=old_plain,
                user_name=user.get("identifiant") or "",
                api_mode=True)
            dlg.exec()
            return dlg.result() == QtWidgets.QDialog.Accepted
        except Exception:
            logging.exception("Erreur changement mdp API")
            return False

    def _login_local(self, identifiant: str, password: str):
        self._set_loading(True)
        try:
            user = self._fetch_user(identifiant)
        except Exception as e:
            logging.exception("Erreur accès DB lors du login")
            self._set_loading(False)
            self._show_error(f"Erreur interne : {e}")
            return

        if user is None:
            self._set_loading(False)
            self._register_failure()
            self._log_failure(identifiant, reason="user_not_found")
            self._show_error("Identifiant ou mot de passe incorrect.")
            self.lineEdit_password.clear()
            self.lineEdit_password.setFocus()
            return

        if not self._verify_password(password, user["pswd_hash"]):
            self._set_loading(False)
            self._register_failure()
            self._log_failure(identifiant, reason="wrong_password",
                              user_id=user.get("id"),
                              user_name=user.get("identifiant"))
            self._show_error("Identifiant ou mot de passe incorrect.")
            self.lineEdit_password.clear()
            self.lineEdit_password.setFocus()
            return

        if not user["actif"]:
            self._set_loading(False)
            self._log_failure(identifiant, reason="inactive",
                              user_id=user.get("id"),
                              user_name=user.get("identifiant"))
            self._show_error("Votre compte n'est pas encore activé. Contactez l'administrateur.")
            return

        if user.get("must_change_password"):
            self._set_loading(False)
            self._log_success(user, note="force_password_change")
            if not self._force_change_password(user, password):
                self.lineEdit_password.clear()
                self.lineEdit_password.setFocus()
                return

        self._reset_failures()
        self._save_settings(identifiant)
        self._update_last_login(user["id"])
        self._set_loading(False)

        self.last_user_id = user["id"]
        self.last_role = user["role"]
        self.last_identifiant = user["identifiant"]

        logging.info("Connexion réussie : %s (%s)", identifiant, user["role"])
        self._log_success(user)
        self.login_success.emit(user["id"], user["role"], user["identifiant"])
        self.accept()

    def _force_change_password(self, user: dict, old_plain: str) -> bool:
        try:
            from Setting_change_password import Setting_change_password
            dlg = Setting_change_password(
                parent=self,
                user_id=user["id"],
                old_password_plain=old_plain,
                user_name=user.get("identifiant") or "")
            dlg.exec()
            return dlg.result() == QtWidgets.QDialog.Accepted
        except Exception:
            logging.exception("Erreur changement forcé de mot de passe")
            return False

    @staticmethod
    def _log_success(user: dict, note: str = ""):
        audit.log(
            audit.ACTION_CONNEXION,
            utilisateur_id=user.get("id"),
            utilisateur_name=user.get("identifiant"),
            cible_type="user",
            cible_id=user.get("id"),
            cible_nom=user.get("identifiant"),
            details={"role": user.get("role"), "note": note} if note else
                    {"role": user.get("role")})

    @staticmethod
    def _log_failure(identifiant: str, reason: str,
                     user_id: str | None = None,
                     user_name: str | None = None):
        audit.log(
            audit.ACTION_ECHEC_CONNEXION,
            utilisateur_id=user_id,
            utilisateur_name=user_name or identifiant,
            cible_type="user",
            cible_id=user_id,
            cible_nom=identifiant,
            details={"reason": reason})

    def _fetch_user(self, identifiant: str):
        conn = db.get_conn()
        cur = conn.execute(
            """SELECT id, identifiant, email, role, pswd_hash, actif,
                      must_change_password
               FROM Utilisateur
               WHERE LOWER(identifiant) = ? OR LOWER(email) = ?
               LIMIT 1""",
            (identifiant, identifiant),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return dict(zip(
            ("id", "identifiant", "email", "role", "pswd_hash", "actif",
             "must_change_password"),
            row,
        ))

    @staticmethod
    def _verify_password(plain: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(
                plain.encode("utf-8"), hashed.encode("utf-8"))
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _update_last_login(user_id: str):
        try:
            db.execute(
                "UPDATE Utilisateur "
                "SET derniere_connexion = datetime('now') "
                "WHERE id = ?",
                (user_id,))
        except Exception as e:
            logging.warning("Impossible de mettre à jour derniere_connexion : %s", e)

    def _on_forgot_password(self, event):
        identifiant = self.lineEdit_username.text().strip().lower()
        if not identifiant:
            QtWidgets.QMessageBox.information(
                self, "Mot de passe oublié",
                "Saisissez d'abord votre identifiant ou email dans le premier champ, puis cliquez à nouveau sur « Mot de passe oublié ? ».")
            self.lineEdit_username.setFocus()
            return

        QtWidgets.QMessageBox.information(
            self, "Réinitialisation",
            f"Si un compte est associé à <b>{identifiant}</b>, contactez un administrateur pour réinitialiser votre mot de passe.<br><br>Aucune dépendance internet : la réinitialisation se fait directement depuis l'application.")

    def _on_contact_support(self, link: str):
        QtWidgets.QMessageBox.information(
            self, "Support TEAM NOVA",
            "<b>Contact support Nova Pharma</b><br><br><b>Équipe :</b> TEAM NOVA<br><b>Email :</b> teamnovaoff@gmail.com<br><b>Tél.  :</b> 08 XX XX XX XX<br><br>Horaires : Lun–Ven, 08h00 – 18h00 (GMT+1)")

    def closeEvent(self, event):
        super().closeEvent(event)

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    dlg = LoginDialog()
    dlg.login_success.connect(
        lambda uid, role, ident: print(f"→ OK : {ident} ({role})"))
    if dlg.exec() == QtWidgets.QDialog.Accepted:
        print("Connexion validée → on peut ouvrir le MainWindow")
    else:
        print("Fenêtre fermée")
    sys.exit(0)