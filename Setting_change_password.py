#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_change_password.py — Changement de mot de passe FORCÉ après reset.
==========================================================================
Ouvert depuis Login.py quand must_change_password = 1.

- Valide le nouveau mot de passe (8+ caractères)
- Vérifie la confirmation
- Interdit la réutilisation du mot de passe temporaire
- Met à jour pswd_hash + must_change_password = 0
- Log MODIF_MOT_DE_PASSE dans AuditLog
"""

import logging

import bcrypt
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db, audit
from Interface_change_password import Ui_Dialog

logger = logging.getLogger(__name__)


MIN_PASSWORD_LEN = 8

ICON_CHECK_DONE = ":/Icon/Icons/check-circle.svg"
ICON_CHECK_GRAY = ":/Icon/Icons/circle.svg"


class Setting_change_password(QtWidgets.QDialog, Ui_Dialog):

    password_changed = QtCore.Signal(str)  # user_id

    def __init__(self, parent=None,
                 user_id: str = None,
                 old_password_plain: str = "",
                 user_name: str = "",
                 api_mode: bool = False):  # ← nouveau paramètre
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.old_password_plain = old_password_plain or ""
        self.user_name = user_name or "Utilisateur"
        self.api_mode = api_mode  # ← nouveau

        self._pwd1_visible = False
        self._pwd2_visible = False

        self._connect_signals()
        self._update_progress()
        self.inp_pwd1.setFocus()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        self.btn_cancel.clicked.connect(self._on_cancel)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_toggle_pwd1.clicked.connect(self._toggle_pwd1)
        self.btn_toggle_pwd2.clicked.connect(self._toggle_pwd2)

        self.inp_pwd1.textChanged.connect(self._update_progress)
        self.inp_pwd2.textChanged.connect(self._update_progress)
        self.inp_pwd2.returnPressed.connect(self._on_save)

    # ══════════════════════════════════════════════════════════════
    def _toggle_pwd1(self):
        self._pwd1_visible = not self._pwd1_visible
        self.inp_pwd1.setEchoMode(
            QtWidgets.QLineEdit.Normal if self._pwd1_visible
            else QtWidgets.QLineEdit.Password)
        self.btn_toggle_pwd1.setIcon(QtGui.QIcon(
            ":/Icon/Icons/eye-off.svg" if self._pwd1_visible
            else ":/Icon/Icons/eye.svg"))

    def _toggle_pwd2(self):
        self._pwd2_visible = not self._pwd2_visible
        self.inp_pwd2.setEchoMode(
            QtWidgets.QLineEdit.Normal if self._pwd2_visible
            else QtWidgets.QLineEdit.Password)
        self.btn_toggle_pwd2.setIcon(QtGui.QIcon(
            ":/Icon/Icons/eye-off.svg" if self._pwd2_visible
            else ":/Icon/Icons/eye.svg"))

    # ══════════════════════════════════════════════════════════════
    def _update_progress(self):
        pwd1 = self.inp_pwd1.text()
        pwd2 = self.inp_pwd2.text()

        len_ok = len(pwd1) >= MIN_PASSWORD_LEN
        match_ok = bool(pwd1) and (pwd1 == pwd2)
        diff_ok = bool(pwd1) and (pwd1 != self.old_password_plain)

        self._set_check(self.ico_len,   len_ok)
        self._set_check(self.ico_match, match_ok)
        self._set_check(self.ico_diff,  diff_ok)

        # Barre de force
        score = self._compute_strength(pwd1)
        self.bar_strength.setValue(score)
        self._apply_strength_style(score)

        # Bouton
        self.btn_save.setEnabled(len_ok and match_ok and diff_ok)

    def _compute_strength(self, pwd: str) -> int:
        if not pwd:
            return 0
        score = 0
        if len(pwd) >= 8:  score += 25
        if len(pwd) >= 12: score += 15
        if any(c.islower() for c in pwd): score += 15
        if any(c.isupper() for c in pwd): score += 15
        if any(c.isdigit() for c in pwd): score += 15
        if any(not c.isalnum() for c in pwd): score += 15
        return min(score, 100)

    def _apply_strength_style(self, score: int):
        if score < 40:
            color, label = "#DC2626", "Faible"
        elif score < 70:
            color, label = "#F4A261", "Moyen"
        else:
            color, label = "#16A34A", "Fort"
        self.bar_strength.setStyleSheet(
            f"QProgressBar {{ background: #e2e8f0; border: none; "
            f"border-radius: 3px; }} "
            f"QProgressBar::chunk {{ background: {color}; "
            f"border-radius: 3px; }}")
        self.lbl_strength.setText(f"Force du mot de passe : {label}")
        self.lbl_strength.setStyleSheet(
            f"color: {color}; font-size: 10px; font-weight: 700; "
            f"background: transparent;")

    @staticmethod
    def _set_check(icon_label: QtWidgets.QLabel, done: bool):
        pix = QtGui.QPixmap(ICON_CHECK_DONE if done else ICON_CHECK_GRAY)
        icon_label.setPixmap(pix.scaled(
            14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # ══════════════════════════════════════════════════════════════
    def _show_error(self, msg: str):
        self.lbl_error.setText(msg)
        self.lbl_error.setVisible(True)

    def _hide_error(self):
        self.lbl_error.setVisible(False)
        self.lbl_error.setText("")

    # ══════════════════════════════════════════════════════════════
    def _on_cancel(self):
        rep = QtWidgets.QMessageBox.question(
            self, "Annuler ?",
            "Si vous annulez, vous serez déconnecté et devrez "
            "changer votre mot de passe à la prochaine connexion.\n\n"
            "Continuer ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep == QtWidgets.QMessageBox.Yes:
            self.reject()

    def _on_save(self):
        self._hide_error()

        pwd1 = self.inp_pwd1.text()
        pwd2 = self.inp_pwd2.text()

        if len(pwd1) < MIN_PASSWORD_LEN:
            self._show_error(
                f"Le mot de passe doit contenir au moins "
                f"{MIN_PASSWORD_LEN} caractères.")
            return
        if pwd1 != pwd2:
            self._show_error("Les deux mots de passe ne correspondent pas.")
            return
        if pwd1 == self.old_password_plain:
            self._show_error(
                "Le nouveau mot de passe doit être différent "
                "du mot de passe temporaire.")
            return

        try:
            if self.api_mode:
                # ═══ MODE API (client) ═══
                from Client.api_singleton import get_api
                api = get_api()
                if api is None:
                    raise RuntimeError("API non initialisée")

                api.change_password(
                    ancien_password=self.old_password_plain,
                    nouveau_password=pwd1)

                logger.info(
                    "Mot de passe changé via API : %s", self.user_id)
            else:
                # ═══ MODE LOCAL ═══
                new_hash = bcrypt.hashpw(
                    pwd1.encode("utf-8"),
                    bcrypt.gensalt()).decode("utf-8")

                with db.transaction():
                    db.execute(
                        """UPDATE Utilisateur
                           SET pswd_hash = ?, must_change_password = 0
                           WHERE id = ?""",
                        (new_hash, self.user_id))

                    audit.log(audit.ACTION_MODIF_MOT_DE_PASSE,
                              utilisateur_id=self.user_id,
                              utilisateur_name=self.user_name,
                              cible_type="user", cible_id=self.user_id,
                              cible_nom=self.user_name,
                              details={"method": "force_change_at_login"})

                logger.info(
                    "Mot de passe changé (local) : %s", self.user_id)

            self.password_changed.emit(self.user_id)
            QtWidgets.QMessageBox.information(
                self, "Mot de passe modifié",
                "Votre mot de passe a été modifié avec succès.\n\n"
                "Vous allez être redirigé vers l'application.")
            self.accept()

        except Exception as e:
            logger.exception("Erreur changement de mot de passe")
            msg = str(e)
            if "incorrect" in msg.lower():
                msg = "Ancien mot de passe incorrect."
            elif "8" in msg and "caractère" in msg.lower():
                msg = "Le mot de passe doit contenir 8 caractères min."
            self._show_error(f"Erreur : {msg}")


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)

    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()
    seed.run()

    dlg = Setting_change_password(
        user_id="TEST",
        old_password_plain="NOVA-2026-AAAA",
        user_name="Test User")
    dlg.password_changed.connect(lambda uid: print(f"→ Changé : {uid}"))
    sys.exit(dlg.exec())