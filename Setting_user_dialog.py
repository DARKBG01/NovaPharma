#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_user_dialog.py — Formulaire création / modification utilisateur.
========================================================================
"""

import logging
import re
import secrets
from datetime import datetime

import bcrypt
from PySide6 import QtWidgets, QtGui, QtCore

from Client.api_singleton import is_client_mode, get_api
from Database import db, audit, NATIONALITY_LIST
from Database import permissions as perms
from Interface_user_dialog import Ui_Dialog

logger = logging.getLogger(__name__)

PHONE_REGEX = re.compile(r"^(?:\+243\d{9}|0\d{9})$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_REGEX  = re.compile(r"^[A-Za-zÀ-ÿ\-' ]{2,80}$")

MIN_PASSWORD_LEN = 8
ROLE_LIST = ["UTILISATEUR", "CAISSIER", "ADMIN"]


def generate_temp_password() -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    suffix = "".join(secrets.choice(alphabet) for _ in range(4))
    return f"NOVA-{datetime.now().year}-{suffix}"


class Setting_user_dialog(QtWidgets.QDialog, Ui_Dialog):

    user_saved = QtCore.Signal(str)

    def __init__(self, parent=None, user_id=None,
                 current_user_id=None,
                 current_is_owner=False,
                 current_is_developer=False):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.current_user_id = current_user_id
        self.current_is_owner = current_is_owner
        self.current_is_developer = current_is_developer

        self._user_data = None
        self._perm_checkboxes = {}
        self._checks_rows = {
            "identity": self.check_identity,
            "contact":  self.check_contact,
            "role":     self.check_role,
            "password": self.check_password,
            "perms":    self.check_perms,
        }

        self._setup_title()
        self._build_permissions_ui()
        self._connect_signals()

        if self.user_id:
            self._load_user()
            self._refresh_ui()
        else:
            self._on_role_changed(self.combo_role.currentText())
        self.inp_natio.addItems(NATIONALITY_LIST)
        self._update_progress()

    # ══════════════════════════════════════════════════════════════
    def _setup_title(self):
        if self.user_id:
            self.setWindowTitle("Modifier utilisateur — Nova Pharma")
            self.lbl_header_title.setText("Modifier l'utilisateur")
            self.btn_save.setText("Enregistrer les modifications")
            self.inp_pwd.setPlaceholderText("Laisser vide pour conserver")

    # ══════════════════════════════════════════════════════════════
    def _build_permissions_ui(self):
        for cat_name, cat_data in perms.PERMISSIONS_CATALOG.items():
            items = cat_data["items"]

            box = QtWidgets.QFrame()
            box.setStyleSheet(
                "QFrame { background: #ffffff; border: 1px solid #e2e8f0; "
                "border-radius: 10px; }")
            v = QtWidgets.QVBoxLayout(box)
            v.setContentsMargins(16, 12, 16, 12)
            v.setSpacing(6)

            h = QtWidgets.QHBoxLayout()
            lbl_cat = QtWidgets.QLabel(cat_name)
            lbl_cat.setStyleSheet(
                "color: #0f172a; font-size: 12px; font-weight: 800; "
                "background: transparent;")
            h.addWidget(lbl_cat)
            h.addStretch()

            btn_all = QtWidgets.QPushButton("Tout")
            btn_off = QtWidgets.QPushButton("Rien")
            for b in (btn_all, btn_off):
                b.setFixedSize(46, 22)
                b.setCursor(QtCore.Qt.PointingHandCursor)
                b.setStyleSheet(
                    "QPushButton { background: #f1f5f9; color: #475569; "
                    "border: 1px solid #e2e8f0; border-radius: 6px; "
                    "font-size: 10px; font-weight: 700; }"
                    "QPushButton:hover { background: #e2e8f0; }")
            h.addWidget(btn_all)
            h.addWidget(btn_off)
            v.addLayout(h)

            for item in items:
                key, label = item[0], item[1]
                flag = item[2] if len(item) >= 3 else None

                chk = QtWidgets.QCheckBox(label)
                base_style = ("QCheckBox { color: #334155; font-size: 11px; "
                              "padding: 2px 0; background: transparent; }")
                if flag == "sensible":
                    base_style = ("QCheckBox { color: #b45309; font-size: 11px; "
                                  "font-weight: 600; padding: 2px 0; "
                                  "background: transparent; }")

                if flag in ("owner", "developer") and not (
                        self.current_is_owner or self.current_is_developer):
                    chk.setEnabled(False)
                    base_style = ("QCheckBox { color: #94a3b8; "
                                  "font-size: 11px; background: transparent; }")

                chk.setStyleSheet(base_style)
                self._perm_checkboxes[key] = chk
                v.addWidget(chk)
                chk.toggled.connect(self._update_progress)

            btn_all.clicked.connect(
                lambda _=False, its=items: self._set_cat_perms(its, True))
            btn_off.clicked.connect(
                lambda _=False, its=items: self._set_cat_perms(its, False))

            self.perms_container_layout.addWidget(box)

    def _set_cat_perms(self, items, state):
        for item in items:
            chk = self._perm_checkboxes.get(item[0])
            if chk and chk.isEnabled():
                chk.blockSignals(True)
                chk.setChecked(state)
                chk.blockSignals(False)
        self._update_progress()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_toggle_pwd.clicked.connect(self._toggle_pwd)
        self.btn_gen_pwd.clicked.connect(self._generate_pwd)
        self.combo_role.currentTextChanged.connect(self._on_role_changed)

        for w in (self.inp_prenom, self.inp_nom, self.inp_post,
                  self.inp_email, self.inp_numero, self.inp_pwd):
            w.textChanged.connect(self._update_progress)

        self.inp_natio.currentIndexChanged.connect(self._update_progress)

        self.chk_actif.toggled.connect(self._update_progress)
        self.chk_must_change.toggled.connect(self._update_progress)

        for w in (self.inp_prenom, self.inp_nom, self.inp_email,
                  self.inp_numero, self.inp_pwd):
            w.returnPressed.connect(self._on_save)

    # ══════════════════════════════════════════════════════════════
    def _on_role_changed(self, role):
        descriptions = {
            "CAISSIER":
                "Un CAISSIER peut uniquement effectuer des ventes "
                "et imprimer des factures.",
            "UTILISATEUR":
                "Un UTILISATEUR peut vendre, consulter les produits, "
                "les clients et l'historique des ventes.",
            "ADMIN":
                "Un ADMIN a accès à presque tout, sauf aux fonctionnalités "
                "réservées au propriétaire (configuration, sauvegarde, audit).",
        }
        self.lbl_role_desc.setText(descriptions.get(role, ""))

        if not self.user_id:
            preset = perms.get_preset(role)
            for key, chk in self._perm_checkboxes.items():
                if chk.isEnabled():
                    chk.blockSignals(True)
                    chk.setChecked(key in preset)
                    chk.blockSignals(False)
        self._update_progress()

    def _toggle_pwd(self):
        if self.inp_pwd.echoMode() == QtWidgets.QLineEdit.Password:
            self.inp_pwd.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.btn_toggle_pwd.setIcon(
                QtGui.QIcon(":/Icon/Icons/eye-off.svg"))
        else:
            self.inp_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
            self.btn_toggle_pwd.setIcon(
                QtGui.QIcon(":/Icon/Icons/eye.svg"))

    def _generate_pwd(self):
        pwd = generate_temp_password()
        self.inp_pwd.setText(pwd)
        self.inp_pwd.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.btn_toggle_pwd.setIcon(QtGui.QIcon(":/Icon/Icons/eye-off.svg"))
        self.chk_must_change.setChecked(True)

    # ══════════════════════════════════════════════════════════════
    def _update_progress(self):
        identity_ok = (len(self.inp_prenom.text().strip()) >= 2 and
                       len(self.inp_nom.text().strip()) >= 2)

        email = self.inp_email.text().strip().lower()
        numero = self.inp_numero.text().strip().replace(" ", "")
        contact_ok = (bool(EMAIL_REGEX.match(email)) and
                      bool(PHONE_REGEX.match(numero)))

        role_ok = self.combo_role.currentText() in ROLE_LIST
        pwd = self.inp_pwd.text()
        pwd_ok = (len(pwd) >= MIN_PASSWORD_LEN) or bool(self.user_id)
        perms_ok = any(c.isChecked() for c in self._perm_checkboxes.values()
                       if c.isEnabled())

        self._checks_rows["identity"].setChecked(identity_ok)
        self._checks_rows["contact"].setChecked(contact_ok)
        self._checks_rows["role"].setChecked(role_ok)
        self._checks_rows["password"].setChecked(pwd_ok)
        self._checks_rows["perms"].setChecked(perms_ok)

        initials = ""
        if self.inp_prenom.text().strip():
            initials += self.inp_prenom.text().strip()[0]
        if self.inp_nom.text().strip():
            initials += self.inp_nom.text().strip()[0]
        self.lbl_avatar.setText(initials.upper() or "?")

        nom_complet = (self.inp_prenom.text().strip() + " "
                       + self.inp_nom.text().strip()).strip()
        self.lbl_sidebar_name.setText(nom_complet or "Nouvel utilisateur")
        self.lbl_sidebar_role.setText(self.combo_role.currentText())

        self.btn_save.setEnabled(
            identity_ok and contact_ok and role_ok and pwd_ok and perms_ok)

    # ══════════════════════════════════════════════════════════════
    def _load_user(self):
        try:
            if is_client_mode():
                from Client.api_singleton import get_api
                api = get_api()
                if api is None:
                    self._user_data = None
                    return
                data = api.get_user(self.user_id)
                self._user_data = data
                # Met en cache les permissions pour l'UI
                self._api_permissions = set(data.get("permissions", []))
                return

            row = db.query_one(
                "SELECT * FROM Utilisateur WHERE id = ? LIMIT 1",
                (self.user_id,))
            self._user_data = dict(row) if row else None
        except Exception:
            logger.exception("Erreur chargement utilisateur")
            self._user_data = None

    def _refresh_ui(self):
        if not self._user_data:
            return
        u = self._user_data

        self.inp_prenom.setText(u.get("prenom") or "")
        self.inp_nom.setText(u.get("nom") or "")
        self.inp_post.setText(u.get("post_nom") or "")
        self.inp_natio.setCurrentIndex(-1)
        self.combo_sexe.setCurrentIndex(
            0 if (u.get("sexe") or "M") == "M" else 1)

        if u.get("date_naissance"):
            d = QtCore.QDate.fromString(u["date_naissance"], "yyyy-MM-dd")
            if d.isValid():
                self.inp_naissance.setDate(d)

        self.inp_email.setText(u.get("email") or "")
        self.inp_numero.setText(u.get("numero") or "")
        self.combo_role.setCurrentText(u.get("role") or "UTILISATEUR")
        self.chk_actif.setChecked(bool(u.get("actif", 1)))
        self.chk_must_change.setChecked(bool(u.get("must_change_password", 0)))

        if u.get("is_owner"):
            self.lbl_status_badge.setText("PROPRIÉTAIRE")
            self.lbl_status_badge.setVisible(True)
        elif u.get("is_developer"):
            self.lbl_status_badge.setText("DÉVELOPPEUR")
            self.lbl_status_badge.setVisible(True)

        current = self._get_user_permissions(self.user_id)
        for key, chk in self._perm_checkboxes.items():
            if chk.isEnabled():
                chk.blockSignals(True)
                chk.setChecked(key in current)
                chk.blockSignals(False)

        if u.get("is_owner") and not (self.current_is_owner
                                      or self.current_is_developer):
            self.chk_actif.setEnabled(False)
            self.combo_role.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.lbl_error.setText(
                "Vous ne pouvez pas modifier le compte PROPRIÉTAIRE.")
            self.lbl_error.setVisible(True)

    def _get_user_permissions(self, user_id):
        if is_client_mode():
            # Déjà chargé dans _load_user → cache
            return getattr(self, "_api_permissions", set())
        rows = db.query(
            "SELECT permission_key FROM UtilisateurPermission "
            "WHERE utilisateur_id = ? AND actif = 1",
            (user_id,))
        return {r["permission_key"] for r in rows}

    @staticmethod
    def _set_user_permissions(user_id, permissions):
        db.execute(
            "UPDATE UtilisateurPermission SET actif = 0 "
            "WHERE utilisateur_id = ?", (user_id,))
        for perm in permissions:
            db.execute(
                """INSERT INTO UtilisateurPermission
                   (id, utilisateur_id, permission_key, actif, updated_at)
                   VALUES (?, ?, ?, 1, datetime('now'))
                   ON CONFLICT(utilisateur_id, permission_key) DO UPDATE
                     SET actif = 1, updated_at = datetime('now')""",
                (db.new_id(), user_id, perm))

    # ══════════════════════════════════════════════════════════════
    def _show_error(self, msg):
        self.lbl_error.setText(f"Erreur : {msg}")
        self.lbl_error.setVisible(True)

    def _hide_error(self):
        self.lbl_error.setVisible(False)
        self.lbl_error.setText("")

    def _validate(self):
        prenom = self.inp_prenom.text().strip()
        nom = self.inp_nom.text().strip()
        if not NAME_REGEX.match(prenom):
            return False, "Prénom invalide."
        if not NAME_REGEX.match(nom):
            return False, "Nom invalide."

        email = self.inp_email.text().strip().lower()
        if not EMAIL_REGEX.match(email):
            return False, "Email invalide."

        numero = self.inp_numero.text().strip().replace(" ", "")
        if not PHONE_REGEX.match(numero):
            return False, "Téléphone invalide."

        pwd = self.inp_pwd.text()
        if (not self.user_id and len(pwd) < MIN_PASSWORD_LEN) or \
           (pwd and len(pwd) < MIN_PASSWORD_LEN):
            return False, f"Mot de passe : {MIN_PASSWORD_LEN} caractères min."

        q = "SELECT 1 FROM Utilisateur WHERE (email = ? OR numero = ?)"
        p = [email, numero]
        if self.user_id:
            q += " AND id <> ?"
            p.append(self.user_id)
        if db.query_one(q + " LIMIT 1", tuple(p)):
            return False, "Email ou téléphone déjà utilisé."
        return True, ""

    # ══════════════════════════════════════════════════════════════
    def _on_save(self):
        self._hide_error()
        valide, msg = self._validate()
        if not valide:
            self._show_error(msg)
            return

        prenom = self.inp_prenom.text().strip()
        nom = self.inp_nom.text().strip()
        post = self.inp_post.text().strip() or None
        natio = self.inp_natio.currentText().strip() or None
        sexe = "M" if self.combo_sexe.currentIndex() == 0 else "F"
        ddn = self.inp_naissance.date().toString("yyyy-MM-dd")
        email = self.inp_email.text().strip().lower()
        numero = self.inp_numero.text().strip().replace(" ", "")
        role = self.combo_role.currentText()
        actif = 1 if self.chk_actif.isChecked() else 0
        must_change = 1 if self.chk_must_change.isChecked() else 0

        pwd_plain = self.inp_pwd.text()

        selected = [k for k, c in self._perm_checkboxes.items()
                    if c.isChecked() and c.isEnabled()]

        # ═══════════════════════════════════════════════════════════
        # MODE CLIENT → API
        # ═══════════════════════════════════════════════════════════
        if is_client_mode():
            try:
                api = get_api()
                if api is None:
                    raise RuntimeError("API non initialisée")

                if self.user_id:
                    # ─── UPDATE ───
                    data = {
                        "prenom": prenom,
                        "nom": nom,
                        "post_nom": post,
                        "sexe": sexe,
                        "date_naissance": ddn,
                        "nationalite": natio,
                        "email": email,
                        "numero": numero,
                        "role": role,
                        "actif": actif,
                        "must_change_password": must_change,
                        "permissions": selected,
                    }
                    if pwd_plain:
                        data["password"] = pwd_plain

                    api.update_user(self.user_id, data)
                    new_id = self.user_id
                else:
                    # ─── CREATE ───
                    if not pwd_plain or len(pwd_plain) < 8:
                        self._show_error(
                            "Mot de passe requis (8 caractères min).")
                        return
                    data = {
                        "prenom": prenom,
                        "nom": nom,
                        "post_nom": post,
                        "sexe": sexe,
                        "date_naissance": ddn,
                        "nationalite": natio,
                        "email": email,
                        "numero": numero,
                        "role": role,
                        "password": pwd_plain,
                        "must_change_password": bool(must_change),
                        "permissions": selected,
                    }
                    result = api.create_user(data)
                    new_id = result.get("id")

                self.user_saved.emit(new_id)
                QtWidgets.QMessageBox.information(
                    self, "Succès",
                    f"L'utilisateur « {prenom} {nom} » a été "
                    f"{'modifié' if self.user_id else 'créé'}.")
                self.accept()
                return

            except Exception as e:
                logger.exception("Erreur enregistrement user (API)")
                self._show_error(str(e))
                return

        # ═══════════════════════════════════════════════════════════
        # MODE LOCAL (code existant)
        # ═══════════════════════════════════════════════════════════
        pwd_hash = None
        if pwd_plain:
            pwd_hash = bcrypt.hashpw(
                pwd_plain.encode("utf-8"),
                bcrypt.gensalt()).decode("utf-8")

        selected_set = set(selected)

        try:
            from Database import audit

            avant = None
            if self.user_id:
                avant = audit.snapshot("Utilisateur", "id", self.user_id)

            with db.transaction():
                if self.user_id:
                    # MODIFICATION
                    if pwd_hash:
                        db.execute(
                            """UPDATE Utilisateur SET
                               prenom=?, nom=?, post_nom=?, nationalite=?,
                               sexe=?, date_naissance=?, email=?, numero=?,
                               role=?, actif=?, must_change_password=?,
                               pswd_hash=? WHERE id=?""",
                            (prenom, nom, post, natio, sexe, ddn,
                             email, numero, role, actif, must_change,
                             pwd_hash, self.user_id))
                    else:
                        db.execute(
                            """UPDATE Utilisateur SET
                               prenom=?, nom=?, post_nom=?, nationalite=?,
                               sexe=?, date_naissance=?, email=?, numero=?,
                               role=?, actif=?, must_change_password=?
                               WHERE id=?""",
                            (prenom, nom, post, natio, sexe, ddn,
                             email, numero, role, actif, must_change,
                             self.user_id))

                    self._set_user_permissions(self.user_id, selected_set)
                    new_id = self.user_id
                else:
                    new_id = db.new_id()
                    identifiant = email
                    base, i = identifiant, 1
                    while db.query_one(
                            "SELECT 1 FROM Utilisateur WHERE identifiant=? LIMIT 1",
                            (identifiant,)):
                        i += 1
                        identifiant = f"{base}.{i}"

                    if not pwd_hash:
                        raise ValueError("Mot de passe obligatoire.")

                    db.execute(
                        """INSERT INTO Utilisateur
                           (id, identifiant, prenom, nom, post_nom, sexe,
                            date_naissance, nationalite, email, numero,
                            role, pswd_hash, actif, must_change_password)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (new_id, identifiant, prenom, nom, post, sexe,
                         ddn, natio, email, numero, role, pwd_hash,
                         actif, must_change))

                    self._set_user_permissions(new_id, selected_set)

            # AUDIT (code existant — garde tel quel)
            try:
                if self.user_id and avant:
                    apres = audit.snapshot("Utilisateur", "id", self.user_id)
                    audit.trace_modif(
                        audit.ACTION_MODIF_INFO_USER,
                        table="Utilisateur", id_column="id",
                        id_value=self.user_id, avant_snapshot=avant,
                        utilisateur_id=self.current_user_id,
                        cible_type="Utilisateur",
                        cible_nom=f"{prenom} {nom}",
                        details={"role_apres": role,
                                 "actif_apres": actif})
                else:
                    apres = audit.snapshot("Utilisateur", "id", new_id)
                    audit.log(
                        audit.ACTION_CREATION_USER,
                        utilisateur_id=self.current_user_id,
                        cible_type="Utilisateur", cible_id=new_id,
                        cible_nom=f"{prenom} {nom}",
                        details={"role": role, "email": email},
                        apres=apres)
            except Exception:
                logger.exception("Erreur audit user")

            self.user_saved.emit(new_id)
            QtWidgets.QMessageBox.information(
                self, "Succès",
                f"L'utilisateur « {prenom} {nom} » a été "
                f"{'modifié' if self.user_id else 'créé'}.")
            self.accept()

        except Exception as e:
            logger.exception("Échec enregistrement utilisateur")
            self._show_error(str(e))