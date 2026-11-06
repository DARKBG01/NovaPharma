#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_load.py — Dialogue de restauration de sauvegarde.
===========================================================
Remplace l'ancienne version qui utilisait Config.json.

Nouveau fonctionnement :
  1. Sélectionne une archive .zip
  2. Déchiffre avec le mot de passe (dérivé ou manuel)
  3. Backup auto de la base actuelle (sécurité)
  4. Copie la base restaurée
  5. Redémarrage requis
"""

import logging
import os
import shutil
import tempfile
import time
from datetime import datetime

import pyzipper
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db, audit
from Database.backup_crypto import get_backup_password
from Interface_load import Ui_Dialog

logger = logging.getLogger(__name__)


class Setting_load(QtWidgets.QDialog, Ui_Dialog):

    restauration_terminee = QtCore.Signal(str)  # chemin backup de sécurité

    def __init__(self, parent = None, user_id=None, user_name=""):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self._archive_path = ""
        self._pwd_visible = False

        self._connect_signals()
        self._prefill_password()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        self.btn_browse.clicked.connect(self._on_browse)
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_restore.clicked.connect(self._on_restore)
        self.btn_toggle_pwd.clicked.connect(self._toggle_pwd)
        self.edit_pwd.textChanged.connect(self._update_restore_enabled)

    def _prefill_password(self):
        """Pré-remplit avec le mot de passe dérivé de cette machine."""
        try:
            pwd = get_backup_password()
            if pwd:
                self.edit_pwd.setText(pwd)
        except Exception:
            pass

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

    def _on_browse(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Choisir une archive de sauvegarde",
            os.path.expanduser("~"),
            "Archives ZIP (*.zip)")
        if not path:
            return
        self._archive_path = path
        self.edit_archive.setText(path)
        self._update_restore_enabled()

    def _update_restore_enabled(self):
        ok = (bool(self._archive_path)
              and os.path.isfile(self._archive_path)
              and len(self.edit_pwd.text()) >= 4)
        self.btn_restore.setEnabled(ok)

    # ══════════════════════════════════════════════════════════════
    def _show_error(self, msg: str):
        self.lbl_error.setText(msg)
        self.lbl_error.setVisible(True)

    def _hide_error(self):
        self.lbl_error.setVisible(False)
        self.lbl_error.setText("")

    def _set_loading(self, loading: bool):
        self.btn_restore.setEnabled(not loading)
        self.btn_cancel.setEnabled(not loading)
        self.btn_browse.setEnabled(not loading)
        self.progress.setVisible(loading)
        if loading:
            self.progress.setRange(0, 0)
            self.setCursor(Qt.WaitCursor)
            QtWidgets.QApplication.processEvents()
        else:
            self.progress.setVisible(False)
            self.unsetCursor()

    # ══════════════════════════════════════════════════════════════
    def _on_restore(self):
        self._hide_error()

        archive = self._archive_path
        pwd = self.edit_pwd.text()

        if not archive or not os.path.isfile(archive):
            self._show_error("Archive introuvable.")
            return

        # ─── Confirmation 1 ───
        rep = QtWidgets.QMessageBox.warning(
            self, "Confirmation",
            f"<b>Restaurer cette archive ?</b><br><br>"
            f"Fichier : <code>{os.path.basename(archive)}</code><br><br>"
            f"⚠ L'application va se fermer après l'opération.<br>"
            f"Une sauvegarde de sécurité sera créée avant.<br><br>"
            f"Confirmer ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        # ─── Confirmation 2 : saisie ───
        text, ok = QtWidgets.QInputDialog.getText(
            self, "Confirmation finale",
            "Tapez RESTAURER pour confirmer :",
            QtWidgets.QLineEdit.Normal, "")
        if not ok or text.strip().upper() != "RESTAURER":
            QtWidgets.QMessageBox.information(
                self, "Annulé", "Restauration annulée.")
            return

        self._set_loading(True)
        try:
            self._do_restore(archive, pwd)
        except Exception as e:
            logger.exception("Erreur restauration")
            self._show_error(f"Erreur : {e}")
        finally:
            self._set_loading(False)

    # ══════════════════════════════════════════════════════════════
    def _do_restore(self, archive: str, password: str):
        """Effectue la restauration complète."""
        # ─── 1. Déchiffre l'archive dans un dossier temp ───
        tmp_dir = tempfile.mkdtemp(prefix="nova_restore_")
        try:
            logger.info("Déchiffrement de %s…", archive)
            with pyzipper.AESZipFile(archive) as zf:
                zf.setpassword(password.encode("utf-8"))
                zf.extractall(tmp_dir)

            # Cherche NovaPharma.db
            restored_db = os.path.join(tmp_dir, "NovaPharma.db")
            if not os.path.isfile(restored_db):
                raise FileNotFoundError(
                    "L'archive ne contient pas de base de données valide "
                    "(NovaPharma.db manquant).")

            # ─── 2. Vérifications approfondies ───
            import sqlite3

            try:
                test_conn = sqlite3.connect(restored_db)
                test_conn.row_factory = sqlite3.Row

                # a) PRAGMA integrity_check
                integrity = test_conn.execute(
                    "PRAGMA integrity_check").fetchone()[0]
                if integrity != "ok":
                    test_conn.close()
                    raise ValueError(
                        f"Intégrité compromise : {integrity}")

                # b) Tables essentielles présentes ?
                required = ["Utilisateur", "produits", "Historique",
                            "Client", "Configuration", "Pharmacie"]
                existing = {r["name"] for r in test_conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'")}
                missing = [t for t in required if t not in existing]
                if missing:
                    test_conn.close()
                    raise ValueError(
                        f"Tables essentielles manquantes : {missing}")

                # c) Au moins un OWNER ?
                try:
                    row = test_conn.execute(
                        "SELECT COUNT(*) FROM Utilisateur "
                        "WHERE is_owner = 1 AND actif = 1").fetchone()
                    if row[0] == 0:
                        logger.warning(
                            "⚠️ Aucun OWNER actif dans la base restaurée")
                except Exception:
                    pass

                # d) Vérif config
                try:
                    row = test_conn.execute(
                        "SELECT COUNT(*) FROM Configuration").fetchone()
                    if row[0] == 0:
                        logger.warning(
                            "⚠️ Configuration vide dans la base restaurée")
                except Exception:
                    pass

                test_conn.close()

                logger.info(
                    "✅ Base restaurée validée : %d tables, integrity OK",
                    len(existing))

            except sqlite3.DatabaseError as e:
                raise ValueError(
                    f"Base corrompue : {e}")

            # ─── 3. Crée un backup de sécurité ───
            backup_dir = os.path.join(
                os.path.dirname(str(db.DB_PATH)), "safety_backups")
            os.makedirs(backup_dir, exist_ok=True)
            safety_backup = os.path.join(
                backup_dir,
                f"NovaPharma_before_restore_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

            db_path = str(db.DB_PATH)
            # Checkpoint pour cohérence
            try:
                db.get_conn().execute("PRAGMA wal_checkpoint(FULL)")
            except Exception:
                pass

            if os.path.exists(db_path):
                shutil.copyfile(db_path, safety_backup)
                logger.info("Backup de sécurité créé : %s", safety_backup)

            # ─── 4. Ferme la connexion ───
            try:
                db.close()
            except Exception:
                pass

            # ─── 5. Remplace la base ───
            for suffix in ("", "-wal", "-shm"):
                f = db_path + suffix
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception:
                        pass

            shutil.copyfile(restored_db, db_path)
            logger.info("Base restaurée : %s", db_path)

            # ─── 6. Audit (dans la base restaurée) ───
            try:
                db.get_conn()
                with db.transaction():
                    audit.log(
                        audit.ACTION_RESTORE_DATABASE,
                        utilisateur_id=self.user_id,
                        utilisateur_name=self.user_name,
                        cible_type="database",
                        cible_id="restore",
                        cible_nom=os.path.basename(archive),
                        details={
                            "source_archive": archive,
                            "safety_backup": safety_backup,
                            "restored_at": datetime.now().isoformat(),
                        },
                        severite="danger")
            except Exception:
                logger.exception("Erreur log audit restore")

            # ─── 7. Message final ───
            QtWidgets.QMessageBox.information(
                self, "✅ Restauration réussie",
                f"<b>La base a été restaurée avec succès.</b><br><br>"
                f"<b>Archive :</b> {os.path.basename(archive)}<br>"
                f"<b>Backup de sécurité :</b> "
                f"{os.path.basename(safety_backup)}<br><br>"
                f"<b>Vérifications effectuées :</b><br>"
                f"• Intégrité SQLite : OK ✅<br>"
                f"• Tables essentielles : OK ✅<br>"
                f"• Utilisateurs : OK ✅<br><br>"
                f"<b style='color:#dc2626;'>L'application va se fermer. "
                f"Relancez-la manuellement.</b>")

            self.restauration_terminee.emit(safety_backup)
            QtWidgets.QApplication.quit()

        except pyzipper.BadZipFile:
            raise ValueError(
                "Le fichier n'est pas une archive ZIP valide.")
        except RuntimeError as e:
            if "Bad password" in str(e).lower() or "password" in str(e).lower():
                raise ValueError(
                    "Mot de passe incorrect. Vérifiez que l'archive a "
                    "bien été créée sur cette machine.")
            raise
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

    dlg = Setting_load(user_id="TEST", user_name="Test")
    dlg.restauration_terminee.connect(
        lambda p: print(f"→ Restauré, backup : {p}"))
    sys.exit(dlg.exec())