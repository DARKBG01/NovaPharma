#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_save.py — Dialogue de sauvegarde manuelle.
====================================================
- Archive ZIP AES-256 de la base NovaPharma.db
- Mot de passe hashé + log dans AuditLog
- Utilise Database/db.py (plus Config.json)
"""

import logging
import os
import shutil
import time
from datetime import datetime

import pyzipper
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db, audit
from Interface_sauvegarde import Ui_Setting_save

logger = logging.getLogger(__name__)


class Setting_save(QtWidgets.QDialog, Ui_Setting_save):

    sauvegarde_terminee = QtCore.Signal(str)   # chemin du ZIP

    def __init__(self, parent=None, user_id=None, user_name=""):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self._pwd_visible = False
        self._path_folder = ""

        self._connect_signals()
        self._load_defaults()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        self.btn_browse.clicked.connect(self._on_browse)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_toggle_pwd.clicked.connect(self._toggle_pwd)
        self.edit_dossier.textChanged.connect(self._on_folder_changed)
        self.edit_pwd.textChanged.connect(self._update_save_enabled)

    def _load_defaults(self):
        # Dossier par défaut depuis la config
        try:
            default_dir = db.get_config("sauvegarde_dossier", "") or ""
            if default_dir and os.path.isdir(default_dir):
                self.edit_dossier.setText(default_dir)
                self._path_folder = default_dir
        except Exception:
            pass

        # Nom par défaut
        nom = f"NovaPharma_backup_" \
              f"{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
        self.edit_nom.setText(nom)

    def _toggle_pwd(self):
        self._pwd_visible = not self._pwd_visible
        if self._pwd_visible:
            self.edit_pwd.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.btn_toggle_pwd.setIcon(
                QtGui.QIcon(":/Icon/Icons/eye-off.svg"))
        else:
            self.edit_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
            self.btn_toggle_pwd.setIcon(
                QtGui.QIcon(":/Icon/Icons/eye.svg"))

    def _on_folder_changed(self, text):
        self._path_folder = text.strip()
        self._update_save_enabled()

    def _on_browse(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choisir le dossier de sauvegarde",
            self._path_folder or os.path.expanduser("~"))
        if folder:
            self.edit_dossier.setText(folder)

    def _update_save_enabled(self):
        dossier_ok = (bool(self._path_folder)
                      and os.path.isdir(self._path_folder))
        pwd_ok = len(self.edit_pwd.text()) >= 4
        nom_ok = bool(self.edit_nom.text().strip())
        self.btn_save.setEnabled(dossier_ok and pwd_ok and nom_ok)

    # ══════════════════════════════════════════════════════════════
    def _show_error(self, msg: str):
        self.lbl_error.setText(msg)
        self.lbl_error.setVisible(True)

    def _hide_error(self):
        self.lbl_error.setVisible(False)
        self.lbl_error.setText("")

    # ══════════════════════════════════════════════════════════════
    def _on_save(self):
        self._hide_error()

        # ─── Validation ───
        dossier = self.edit_dossier.text().strip()
        if not dossier or not os.path.isdir(dossier):
            self._show_error("Dossier de destination invalide.")
            return

        pwd = self.edit_pwd.text()
        if len(pwd) < 4:
            self._show_error(
                "Le mot de passe doit contenir au moins 4 caractères.")
            return

        nom = self.edit_nom.text().strip()
        if not nom:
            nom = f"NovaPharma_backup_" \
                  f"{datetime.now().strftime('%Y%m%d_%H%M')}.zip"
        if not nom.lower().endswith(".zip"):
            nom += ".zip"

        target_zip = os.path.join(dossier, nom)

        # ─── Confirmation si existe déjà ───
        if os.path.exists(target_zip):
            rep = QtWidgets.QMessageBox.question(
                self, "Écraser ?",
                f"Le fichier existe déjà :\n{nom}\n\nL'écraser ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return

        # ─── Lancement ───
        self._set_loading(True)
        try:
            self._create_backup(target_zip, pwd)
            self.sauvegarde_terminee.emit(target_zip)
            QtWidgets.QMessageBox.information(
                self, "Sauvegarde réussie",
                f"La sauvegarde a été créée avec succès.\n\n"
                f"Fichier : {os.path.basename(target_zip)}\n"
                f"Dossier : {dossier}")
            self.accept()

        except Exception as e:
            logger.exception("Erreur sauvegarde")
            self._show_error(f"Erreur : {e}")
        finally:
            self._set_loading(False)

    def _set_loading(self, loading: bool):
        self.btn_save.setEnabled(not loading)
        self.btn_cancel.setEnabled(not loading)
        self.btn_browse.setEnabled(not loading)
        self.progress.setVisible(loading)
        if loading:
            self.progress.setRange(0, 0)   # mode indéterminé
            self.setCursor(Qt.WaitCursor)
            QtWidgets.QApplication.processEvents()
        else:
            self.progress.setVisible(False)
            self.unsetCursor()

    # ══════════════════════════════════════════════════════════════
    def _create_backup(self, target_zip, password):
        """Crée l'archive ZIP AES-256 de la base."""
        db_path = str(db.DB_PATH)

        if not os.path.exists(db_path):
            raise FileNotFoundError(
                f"Base introuvable : {db_path}")

        # Force un checkpoint WAL pour avoir un fichier cohérent
        try:
            db.get_conn().execute("PRAGMA wal_checkpoint(FULL)")
        except Exception:
            pass

        # Copie temporaire de la base (pour éviter les locks)
        tmp_dir = os.path.join(os.path.dirname(target_zip),
                               ".tmp_backup_nova")
        os.makedirs(tmp_dir, exist_ok=True)
        try:
            tmp_db = os.path.join(tmp_dir, "NovaPharma.db")
            shutil.copyfile(db_path, tmp_db)

            # Crée l'archive AES-256
            with pyzipper.AESZipFile(
                    target_zip, "w",
                    compression=pyzipper.ZIP_LZMA,
                    encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(password.encode("utf-8"))
                zf.setencryption(pyzipper.WZ_AES, nbits=256)
                zf.write(tmp_db, arcname="NovaPharma.db")

            # Calcule le hash SHA256
            import hashlib
            h = hashlib.sha256()
            with open(target_zip, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            file_hash = h.hexdigest()
            file_size = os.path.getsize(target_zip)

            # Enregistre dans la table Sauvegarde
            try:
                with db.transaction():
                    db.execute("""
                        INSERT INTO Sauvegarde
                        (id, chemin, taille_octets, hash_sha256,
                         type, statut, utilisateur_id, commentaire)
                        VALUES (?, ?, ?, ?, 'MANUELLE', 'OK', ?, ?)
                    """, (db.new_id(), target_zip, file_size,
                          file_hash, self.user_id,
                          f"Sauvegarde manuelle par {self.user_name}"))
            except Exception:
                logger.exception("Erreur insert Sauvegarde")

            # Audit
            # ═══ AUDIT ═══
            audit.log(
                audit.ACTION_BACKUP_CREATION,
                utilisateur_id=self.user_id,
                utilisateur_name=self.user_name,
                cible_type="backup",
                cible_id=os.path.basename(target_zip),
                cible_nom=os.path.basename(target_zip),
                details={
                    "path": target_zip,
                    "size": file_size,
                    "hash": file_hash,
                    "type": "MANUELLE",
                },
                severite="info")

            logger.info("Sauvegarde créée : %s", target_zip)

        finally:
            # Nettoyage
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception:
                pass


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()
    seed.run()

    dlg = Setting_save(user_id="TEST", user_name="Test")
    sys.exit(dlg.exec())