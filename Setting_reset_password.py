#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_reset_password.py — Reset du mot de passe (admin → user).
==================================================================
"""

import io
import logging
import secrets
from datetime import datetime

import bcrypt
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import get_api, is_client_mode
from Database import db, audit
from Interface_reset_password import Ui_Dialog

logger = logging.getLogger(__name__)


def generate_temp_password() -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    suffix = "".join(secrets.choice(alphabet) for _ in range(4))
    return f"NOVA-{datetime.now().year}-{suffix}"


class Setting_reset_password(QtWidgets.QDialog, Ui_Dialog):

    password_reset = QtCore.Signal(str)

    def __init__(self, parent=None, user_id=None, current_user_id=None):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.current_user_id = current_user_id
        self._temp_password = generate_temp_password()

        self._connect_signals()
        self._apply_reset()
        self._render_qr()

    def _connect_signals(self):
        self.btn_close.clicked.connect(self.accept)
        self.btn_copy.clicked.connect(self._copy_to_clipboard)

    def _apply_reset(self):
        # ─── MODE CLIENT → API ───
        if is_client_mode():
            try:
                api = get_api()
                if api is None:
                    raise RuntimeError("API non initialisée")

                result = api.reset_user_password(self.user_id)
                self._temp_password = result.get(
                    "temp_password", self._temp_password)
                self.lbl_pwd.setText(self._temp_password)
                return
            except Exception as e:
                logger.exception("Erreur reset password (API)")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible de réinitialiser :\n{e}")
                self._temp_password = "ERREUR"
                self.lbl_pwd.setText("Échec de la réinitialisation")
                return

        # ─── MODE LOCAL (code existant) ───
        try:
            pwd_hash = bcrypt.hashpw(
                self._temp_password.encode("utf-8"),
                bcrypt.gensalt()).decode("utf-8")

            avant = audit.snapshot("Utilisateur", "id", self.user_id)

            cible_nom = "Utilisateur"
            try:
                r = db.query_one(
                    "SELECT COALESCE(prenom,'') || ' ' || "
                    "COALESCE(nom,'') AS nom FROM Utilisateur "
                    "WHERE id = ? LIMIT 1",
                    (self.user_id,))
                if r and r["nom"].strip():
                    cible_nom = r["nom"].strip()
            except Exception:
                pass

            with db.transaction():
                db.execute(
                    "UPDATE Utilisateur SET pswd_hash = ?, "
                    "must_change_password = 1 WHERE id = ?",
                    (pwd_hash, self.user_id))

            try:
                audit.log(
                    audit.ACTION_RESET_MOT_DE_PASSE,
                    utilisateur_id=self.current_user_id,
                    cible_type="Utilisateur",
                    cible_id=self.user_id,
                    cible_nom=cible_nom,
                    details={
                        "method": "admin_reset",
                        "temp_password_generated": True,
                        "force_change_at_login": True,
                    },
                    avant={"must_change_password":
                               avant.get("must_change_password")
                               if avant else None})
            except Exception:
                logger.exception("Erreur audit reset mdp")

            self.lbl_pwd.setText(self._temp_password)
        except Exception as e:
            logger.exception("Erreur reset mot de passe")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible de réinitialiser le mot de passe :\n{e}")

    def _render_qr(self):
        try:
            import qrcode
            data = f"NOVA-PWD|user_id={self.user_id}|pwd={self._temp_password}"
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#023E8A", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            qimg = QtGui.QImage.fromData(buf.getvalue())
            pix = QtGui.QPixmap.fromImage(qimg).scaled(
                200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_qrcode.setPixmap(pix)
        except Exception:
            logger.exception("Erreur génération QR")
            self.lbl_qrcode.setText("QR indisponible")

    def _copy_to_clipboard(self):
        QtWidgets.QApplication.clipboard().setText(self._temp_password)
        self.btn_copy.setIcon(QtGui.QIcon(":/Icon/Icons/check-circle.svg"))
        self.btn_copy.setText("Copié !")

        def _restore():
            self.btn_copy.setIcon(QtGui.QIcon(":/Icon/Icons/copy.svg"))
            self.btn_copy.setText("Copier dans le presse-papier")

        QtCore.QTimer.singleShot(2000, _restore)