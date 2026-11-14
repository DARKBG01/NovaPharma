#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_user_info.py — Fiche détail utilisateur.
==================================================
"""

import json
import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import is_client_mode, get_api
from Database import db, audit
from Database import permissions as perms
from Interface_user_info import Ui_Dialog
from Ui_helpers import setup_user_info_history_table

logger = logging.getLogger(__name__)

ROLE_BADGES = {
    "ADMIN":       ("ADMIN",       "#1e40af", "#dbeafe"),
    "UTILISATEUR": ("UTILISATEUR", "#334155", "#e2e8f0"),
    "CAISSIER":    ("CAISSIER",    "#15803d", "#dcfce7"),
}


class Setting_user_info(QtWidgets.QDialog, Ui_Dialog):

    user_changed = QtCore.Signal(str)

    def __init__(self, parent=None, user_id=None, current_user_id=None,
                 current_role="ADMIN", current_is_owner=False,
                 current_is_developer=False):
        super().__init__(parent)
        self.setupUi(self)
        setup_user_info_history_table(self.history_table)

        self.user_id = user_id
        self.current_user_id = current_user_id
        self.current_role = (current_role or "UTILISATEUR").upper()
        self.current_is_owner = current_is_owner
        self.current_is_developer = current_is_developer
        self._user_data = None

        self._connect_signals()
        self._apply_permissions()
        self._load_user()
        self._refresh_ui()
        self._load_history()

    def _connect_signals(self):
        self.btn_close.clicked.connect(self.reject)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_reset_pwd.clicked.connect(self._on_reset)

    def _apply_permissions(self):
        can_act = (self.current_is_owner or self.current_is_developer
                   or self.current_role == "ADMIN")
        self.btn_edit.setVisible(can_act)
        self.btn_delete.setVisible(
            can_act and self.user_id != self.current_user_id)
        self.btn_reset_pwd.setVisible(can_act)

    def _load_user(self):
        try:
            if is_client_mode():
                api = get_api()
                if api is None:
                    self._user_data = None
                    return
                self._user_data = api.get_user(self.user_id)
                return
            row = db.query_one(
                "SELECT * FROM Utilisateur WHERE id = ? LIMIT 1",
                (self.user_id,))
            self._user_data = dict(row) if row else None
        except Exception:
            logger.exception("Erreur chargement utilisateur")

    def _refresh_ui(self):
        if not self._user_data:
            self.lbl_name.setText("Utilisateur introuvable")
            return
        u = self._user_data

        prenom = u.get("prenom") or ""
        nom = u.get("nom") or ""
        full = f"{prenom} {nom}".strip() or "—"

        initials = ""
        if prenom: initials += prenom[0]
        if nom:    initials += nom[0]
        self.lbl_avatar.setText(initials.upper() or "?")
        self.lbl_name.setText(full)
        self.lbl_email.setText(u.get("email") or "—")

        role = u.get("role") or "UTILISATEUR"
        label, fg, bg = ROLE_BADGES.get(role, (role, "#334155", "#e2e8f0"))
        if u.get("is_owner"):
            label, fg, bg = "PROPRIÉTAIRE", "#92400e", "#fef3c7"
        elif u.get("is_developer"):
            label, fg, bg = "DÉVELOPPEUR", "#4338ca", "#e0e7ff"
        self.lbl_role_badge.setText(label)
        self.lbl_role_badge.setStyleSheet(
            f"background: {bg}; color: {fg}; padding: 4px 12px; "
            f"border-radius: 10px; font-size: 10px; font-weight: 800; "
            f"letter-spacing: 1px;")

        actif = int(u.get("actif", 0))
        if actif:
            self.lbl_status_badge.setText("ACTIF")
            self.lbl_status_badge.setStyleSheet(
                "background: #dcfce7; color: #15803d; padding: 4px 12px; "
                "border-radius: 10px; font-size: 10px; font-weight: 800; "
                "letter-spacing: 1px;")
        else:
            self.lbl_status_badge.setText("INACTIF")
            self.lbl_status_badge.setStyleSheet(
                "background: #f1f5f9; color: #64748b; padding: 4px 12px; "
                "border-radius: 10px; font-size: 10px; font-weight: 800; "
                "letter-spacing: 1px;")

        self.val_prenom.setText(prenom or "—")
        self.val_nom.setText(nom or "—")
        self.val_email.setText(u.get("email") or "—")
        self.val_numero.setText(u.get("numero") or "—")
        self.val_sexe.setText(
            "Masculin" if u.get("sexe") == "M" else "Féminin")
        self.val_ddn.setText(u.get("date_naissance") or "—")
        self.val_natio.setText(u.get("nationalite") or "—")
        self.val_created.setText(u.get("created_at") or "—")
        self.val_last.setText(u.get("derniere_connexion") or "—")

        self._load_permissions()

    def _load_permissions(self):
        while self.permsListLayout.count():
            item = self.permsListLayout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        u = self._user_data or {}
        is_owner = bool(u.get("is_owner"))
        is_dev = bool(u.get("is_developer"))

        if is_owner or is_dev:
            info = QtWidgets.QFrame()
            info.setStyleSheet(
                "QFrame { background: #fef3c7; border: 1px solid #fde68a; "
                "border-radius: 10px; }")
            h = QtWidgets.QHBoxLayout(info)
            h.setContentsMargins(12, 12, 12, 12)
            h.setSpacing(10)

            ico = QtWidgets.QLabel()
            ico.setPixmap(QtGui.QPixmap(
                ":/Icon/Icons/crown.svg" if is_owner
                else ":/Icon/Icons/wrench.svg").scaled(
                    20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            ico.setStyleSheet("background: transparent;")
            h.addWidget(ico)

            msg = QtWidgets.QLabel(
                "Cet utilisateur dispose de TOUTES les permissions "
                "(compte propriétaire ou développeur).")
            msg.setWordWrap(True)
            msg.setStyleSheet(
                "background: transparent; color: #92400e; font-size: 12px; "
                "font-weight: 700;")
            h.addWidget(msg, 1)

            self.permsListLayout.addWidget(info)
            self.permsListLayout.addStretch()
            return

        active = set()
        try:
            if is_client_mode():
                # Déjà dans _user_data["permissions"]
                active = set(
                    (self._user_data or {}).get("permissions", []) or [])
            else:
                rows = db.query(
                    "SELECT permission_key FROM UtilisateurPermission "
                    "WHERE utilisateur_id = ? AND actif = 1",
                    (self.user_id,))
                active = {r["permission_key"] for r in rows}
        except Exception:
            logger.exception("Erreur lecture permissions")

        for cat_name, cat_data in perms.PERMISSIONS_CATALOG.items():
            box = QtWidgets.QFrame()
            box.setStyleSheet(
                "QFrame { background: #ffffff; border: 1px solid #e2e8f0; "
                "border-radius: 10px; }")
            v = QtWidgets.QVBoxLayout(box)
            v.setContentsMargins(14, 10, 14, 10)
            v.setSpacing(4)

            lbl = QtWidgets.QLabel(cat_name)
            lbl.setStyleSheet(
                "color: #0f172a; font-size: 12px; font-weight: 800; "
                "background: transparent;")
            v.addWidget(lbl)

            for item in cat_data["items"]:
                key, label = item[0], item[1]
                ok = key in active

                row = QtWidgets.QWidget()
                row.setStyleSheet("background: transparent;")
                h = QtWidgets.QHBoxLayout(row)
                h.setContentsMargins(0, 2, 0, 2)
                h.setSpacing(8)

                icon = QtWidgets.QLabel()
                icon.setStyleSheet("background: transparent;")
                icon.setPixmap(QtGui.QPixmap(
                    ":/Icon/Icons/check-circle.svg" if ok
                    else ":/Icon/Icons/circle.svg").scaled(
                        14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                h.addWidget(icon)

                text = QtWidgets.QLabel(label)
                text.setStyleSheet(
                    f"color: {'#16A34A' if ok else '#cbd5e1'}; "
                    f"font-size: 11px; background: transparent;")
                h.addWidget(text, 1)

                v.addWidget(row)

            self.permsListLayout.addWidget(box)

        self.permsListLayout.addStretch()

    def _load_history(self):
        try:
            rows = []
            if is_client_mode():
                from Client.api_singleton import get_api
                api = get_api()
                if api:
                    # On filtre par utilisateur_id via l'API
                    data = api.list_audit(
                        page=1, per_page=50,
                        utilisateur_id=self.user_id)
                    rows = data.get("items", [])
            else:
                db_rows = db.query(
                    """SELECT date_action, action, details FROM AuditLog
                       WHERE cible_id = ? OR utilisateur_id = ?
                       ORDER BY date_action DESC LIMIT 50""",
                    (self.user_id, self.user_id))
                rows = [dict(r) for r in db_rows]

            self.history_table.setRowCount(len(rows))
            for i, r in enumerate(rows):
                d = QtWidgets.QTableWidgetItem(str(r.get("date_action", "")))
                d.setForeground(QtGui.QColor("#64748b"))
                self.history_table.setItem(i, 0, d)

                a = QtWidgets.QTableWidgetItem(str(r.get("action", "")))
                a.setForeground(QtGui.QColor("#023E8A"))
                a.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                self.history_table.setItem(i, 1, a)

                try:
                    det = r.get("details", "")
                    if isinstance(det, str) and det.startswith("{"):
                        import json
                        det_dict = json.loads(det)
                        det_str = ", ".join(f"{k}={v}" for k, v in det_dict.items())
                    else:
                        det_str = str(det or "")
                except Exception:
                    det_str = str(r.get("details") or "")

                self.history_table.setItem(i, 2, QtWidgets.QTableWidgetItem(det_str))

            setup_user_info_history_table(self.history_table)
        except Exception:
            logger.exception("Erreur chargement historique")

    def _on_edit(self):
        try:
            from Setting_user_dialog import Setting_user_dialog
            dlg = Setting_user_dialog(
                parent=self, user_id=self.user_id,
                current_user_id=self.current_user_id,
                current_is_owner=self.current_is_owner,
                current_is_developer=self.current_is_developer)
            dlg.user_saved.connect(self._on_saved)
            dlg.exec()
        except Exception:
            logger.exception("Erreur édition")

    def _on_saved(self, uid):
        self._load_user()
        self._refresh_ui()
        self._load_history()
        self.user_changed.emit(uid)

    def _on_reset(self):
        try:
            from Setting_reset_password import Setting_reset_password
            dlg = Setting_reset_password(
                parent=self, user_id=self.user_id,
                current_user_id=self.current_user_id)

            def _done(_):
                self._load_user()
                self._refresh_ui()
                self._load_history()
                self.user_changed.emit(self.user_id)

            dlg.password_reset.connect(_done)
            dlg.exec()
        except Exception:
            logger.exception("Erreur reset")

    def _on_delete(self):
        if not self._user_data:
            return
        u = self._user_data
        if u.get("is_owner") and not (self.current_is_owner
                                      or self.current_is_developer):
            QtWidgets.QMessageBox.warning(
                self, "Accès refusé",
                "Vous ne pouvez pas désactiver le compte PROPRIÉTAIRE.")
            return

        prenom = u.get("prenom") or ""
        nom = u.get("nom") or ""
        actif = int(u.get("actif", 0))
        action = "réactiver" if not actif else "désactiver"

        rep = QtWidgets.QMessageBox.question(
            self, "Confirmation",
            f"Voulez-vous vraiment {action} le compte "
            f"« {prenom} {nom} » ?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        # ─── MODE CLIENT → API ───
        if is_client_mode():
            try:
                api = get_api()
                if api is None:
                    return
                if not actif:
                    # Réactivation : PUT actif=1
                    api.update_user(self.user_id, {"actif": 1})
                else:
                    # Désactivation : DELETE (soft delete)
                    api.delete_user(self.user_id)

                self.user_changed.emit(self.user_id)
                self.accept()
                QtWidgets.QMessageBox.information(
                    self, "Succès",
                    f"Le compte a été "
                    f"{'réactivé' if not actif else 'désactivé'}.")
                return
            except Exception as e:
                logger.exception("Erreur changement statut (API)")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur", str(e))
                return

        # ─── MODE LOCAL (code existant) ───
        try:
            from Database import audit
            new_actif = 0 if actif else 1
            avant = audit.snapshot("Utilisateur", "id", self.user_id)

            with db.transaction():
                db.execute(
                    "UPDATE Utilisateur SET actif = ? WHERE id = ?",
                    (new_actif, self.user_id))

            try:
                apres = audit.snapshot("Utilisateur", "id", self.user_id)
                action_log = (audit.ACTION_ACTIVATION_USER
                              if new_actif
                              else audit.ACTION_DESACTIVATION_USER)
                audit.log(
                    action_log,
                    utilisateur_id=self.current_user_id,
                    cible_type="Utilisateur",
                    cible_id=self.user_id,
                    cible_nom=f"{prenom} {nom}",
                    details={
                        "actif_avant": actif,
                        "actif_apres": new_actif,
                    },
                    avant=avant,
                    apres=apres)
            except Exception:
                logger.exception("Erreur audit activation user")

            self.user_changed.emit(self.user_id)
            self._load_user()
            self._refresh_ui()
            QtWidgets.QMessageBox.information(
                self, "Succès",
                f"Le compte a été "
                f"{'réactivé' if new_actif else 'désactivé'}.")
        except Exception as e:
            logger.exception("Erreur changement statut")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))