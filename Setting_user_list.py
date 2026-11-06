#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_users_list.py — Page liste des utilisateurs.
=====================================================
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db
from Interface_page_users import Ui_PageUsers

logger = logging.getLogger(__name__)

PAGE_SIZE = 30

COL_USER   = 0
COL_EMAIL  = 1
COL_NUM    = 2
COL_ROLE   = 3
COL_STATUS = 4
COL_LAST   = 5

FILTERS = {
    "Tous les utilisateurs": ("1=1", ()),
    "Actifs":                ("actif = 1", ()),
    "Inactifs":              ("actif = 0", ()),
    "Rôle : ADMIN":          ("role = ?", ("ADMIN",)),
    "Rôle : UTILISATEUR":    ("role = ?", ("UTILISATEUR",)),
    "Rôle : CAISSIER":       ("role = ?", ("CAISSIER",)),
}

ROLE_BADGES = {
    "ADMIN":       ("ADMIN",       "#1e40af", "#dbeafe"),
    "UTILISATEUR": ("UTILISATEUR", "#334155", "#e2e8f0"),
    "CAISSIER":    ("CAISSIER",    "#15803d", "#dcfce7"),
}


class PageUsers(QtWidgets.QWidget, Ui_PageUsers):

    def __init__(self, parent=None, user_id=None, role="ADMIN",
                 is_owner=False, is_developer=False):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.role = (role or "UTILISATEUR").upper()
        self.is_owner = is_owner
        self.is_developer = is_developer

        self._page = 1
        self._total_pages = 1
        self._total_count = 0
        self._search = ""
        self._filter = "Tous les utilisateurs"

        self._connect_signals()
        self._setup_table()
        self._apply_permissions()
        self.refresh()

    def _apply_permissions(self):
        can_add = (self.is_owner or self.is_developer
                   or self.role == "ADMIN")
        self.btn_new.setVisible(can_add)

    def _setup_table(self):
        h = self.users_table.horizontalHeader()
        h.setSectionResizeMode(COL_USER,   QtWidgets.QHeaderView.Stretch)
        h.setSectionResizeMode(COL_EMAIL,  QtWidgets.QHeaderView.Stretch)
        h.setSectionResizeMode(COL_NUM,    QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_ROLE,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_STATUS, QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_LAST,   QtWidgets.QHeaderView.ResizeToContents)
        self.users_table.verticalHeader().setVisible(False)
        self.users_table.verticalHeader().setDefaultSectionSize(56)

    def _connect_signals(self):
        self.btn_new.clicked.connect(self._on_new)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_prev.clicked.connect(self._on_prev)
        self.btn_next.clicked.connect(self._on_next)
        self.inp_search.textChanged.connect(self._on_search)
        self.combo_filter.currentTextChanged.connect(self._on_filter)
        self.users_table.doubleClicked.connect(self._on_view)
        self.users_table.customContextMenuRequested.connect(self._on_context)

    # ══════════════════════════════════════════════════════════════
    def refresh(self):
        self._load_page(self._page)

    def _load_page(self, page):
        try:
            clause, params = FILTERS.get(self._filter, ("1=1", ()))
            where = [clause]
            p = list(params)

            if self._search:
                where.append("(prenom LIKE ? OR nom LIKE ? OR "
                             "email LIKE ? OR numero LIKE ?)")
                like = f"%{self._search}%"
                p.extend([like, like, like, like])

            wc = " AND ".join(where)
            row = db.query_one(
                f"SELECT COUNT(*) AS n FROM Utilisateur WHERE {wc}",
                tuple(p))
            self._total_count = int(row["n"] or 0) if row else 0
            self._total_pages = max(
                1, (self._total_count + PAGE_SIZE - 1) // PAGE_SIZE)
            self._page = max(1, min(page, self._total_pages))

            offset = (self._page - 1) * PAGE_SIZE
            rows = db.query(
                f"""SELECT id, identifiant, prenom, nom, email, numero,
                          role, actif, derniere_connexion,
                          is_owner, is_developer
                    FROM Utilisateur
                    WHERE {wc}
                    ORDER BY is_owner DESC, is_developer DESC,
                             created_at ASC
                    LIMIT ? OFFSET ?""",
                tuple(p + [PAGE_SIZE, offset]))

            self._populate(rows)
            self._update_pagination()
        except Exception:
            logger.exception("Erreur chargement utilisateurs")

    def _populate(self, rows):
        t = self.users_table
        t.blockSignals(True)
        t.setRowCount(0)
        t.clearSpans()

        if not rows:
            t.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem("Aucun utilisateur à afficher")
            empty.setTextAlignment(Qt.AlignCenter)
            empty.setForeground(QtGui.QColor("#94a3b8"))
            f = QtGui.QFont("Segoe UI", 11)
            f.setItalic(True)
            empty.setFont(f)
            t.setItem(0, 0, empty)
            t.setSpan(0, 0, 1, t.columnCount())
            t.blockSignals(False)
            return

        t.setRowCount(len(rows))
        fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        fn = QtGui.QFont("Segoe UI", 10)
        fm = QtGui.QFont("Courier New", 9)

        for i, r in enumerate(rows):
            prenom = r["prenom"] or ""
            nom = r["nom"] or ""
            full = f"{prenom} {nom}".strip()

            it0 = QtWidgets.QTableWidgetItem(full)
            it0.setFont(fb)
            it0.setForeground(QtGui.QColor("#0f172a"))
            it0.setData(Qt.UserRole, r["id"])
            if r["is_owner"]:
                it0.setIcon(QtGui.QIcon(":/Icon/Icons/crown.svg"))
            elif r["is_developer"]:
                it0.setIcon(QtGui.QIcon(":/Icon/Icons/wrench.svg"))
            t.setItem(i, COL_USER, it0)

            it1 = QtWidgets.QTableWidgetItem(r["email"] or "—")
            it1.setFont(fn)
            it1.setForeground(QtGui.QColor("#475569"))
            t.setItem(i, COL_EMAIL, it1)

            it2 = QtWidgets.QTableWidgetItem(r["numero"] or "—")
            it2.setFont(fm)
            it2.setForeground(QtGui.QColor("#64748b"))
            it2.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_NUM, it2)

            role = r["role"] or "UTILISATEUR"
            label, fg, bg = ROLE_BADGES.get(role, (role, "#334155", "#e2e8f0"))
            if r["is_owner"]:
                label, fg, bg = "PROPRIÉTAIRE", "#92400e", "#fef3c7"
            elif r["is_developer"]:
                label, fg, bg = "DÉVELOPPEUR", "#4338ca", "#e0e7ff"

            it3 = QtWidgets.QTableWidgetItem(label)
            it3.setFont(fb)
            it3.setForeground(QtGui.QColor(fg))
            it3.setBackground(QtGui.QColor(bg))
            it3.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_ROLE, it3)

            actif = int(r["actif"] or 0)
            txt, c = ("Actif", "#15803d") if actif else ("Inactif", "#64748b")
            it4 = QtWidgets.QTableWidgetItem(txt)
            it4.setFont(fb)
            it4.setForeground(QtGui.QColor(c))
            it4.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_STATUS, it4)

            last = r["derniere_connexion"] or "—"
            if last and len(str(last)) > 16:
                last = str(last)[:16]
            it5 = QtWidgets.QTableWidgetItem(str(last))
            it5.setFont(fn)
            it5.setForeground(QtGui.QColor("#94a3b8"))
            it5.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_LAST, it5)

        t.blockSignals(False)

    def _update_pagination(self):
        self.lbl_page_info.setText(
            f"Page {self._page} / {self._total_pages}")
        self.btn_prev.setEnabled(self._page > 1)
        self.btn_next.setEnabled(self._page < self._total_pages)

        label = "utilisateur" if self._total_count <= 1 else "utilisateurs"
        self.lbl_total_info.setText(f"{self._total_count} {label}")
        self.lbl_count_badge.setText(f"{self._total_count} {label}")

    def _on_prev(self):
        if self._page > 1:
            self._load_page(self._page - 1)

    def _on_next(self):
        if self._page < self._total_pages:
            self._load_page(self._page + 1)

    def _on_search(self, text):
        self._search = text.strip()
        self._page = 1
        self._load_page(1)

    def _on_filter(self, text):
        self._filter = text
        self._page = 1
        self._load_page(1)

    def _selected_id(self):
        row = self.users_table.currentRow()
        if row < 0:
            return None
        it = self.users_table.item(row, COL_USER)
        return it.data(Qt.UserRole) if it else None

    def _on_new(self):
        try:
            from Setting_user_dialog import Setting_user_dialog
            dlg = Setting_user_dialog(
                parent=self, current_user_id=self.user_id,
                current_is_owner=self.is_owner,
                current_is_developer=self.is_developer)
            dlg.user_saved.connect(lambda _: self.refresh())
            dlg.exec()
        except Exception:
            logger.exception("Erreur dialogue nouvel utilisateur")

    def _on_view(self):
        uid = self._selected_id()
        if not uid:
            return
        try:
            from Setting_user_info import Setting_user_info
            dlg = Setting_user_info(
                parent=self, user_id=uid,
                current_user_id=self.user_id,
                current_role=self.role,
                current_is_owner=self.is_owner,
                current_is_developer=self.is_developer)
            dlg.user_changed.connect(lambda _: self.refresh())
            dlg.exec()
        except Exception:
            logger.exception("Erreur fiche utilisateur")

    def _on_context(self, pos):
        row = self.users_table.rowAt(pos.y())
        if row < 0:
            return
        self.users_table.selectRow(row)

        menu = QtWidgets.QMenu(self)
        act_view = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/eye.svg"), "Voir la fiche")
        act_edit = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/edit.svg"), "Modifier")
        menu.addSeparator()
        act_reset = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/key.svg"), "Réinitialiser mot de passe")

        can_act = (self.is_owner or self.is_developer
                   or self.role == "ADMIN")
        act_edit.setEnabled(can_act)
        act_reset.setEnabled(can_act)

        action = menu.exec(self.users_table.viewport().mapToGlobal(pos))
        if action == act_view:
            self._on_view()
        elif action == act_edit:
            self._open_edit()
        elif action == act_reset:
            self._open_reset()

    def _open_edit(self):
        uid = self._selected_id()
        if not uid:
            return
        try:
            from Setting_user_dialog import Setting_user_dialog
            dlg = Setting_user_dialog(
                parent=self, user_id=uid,
                current_user_id=self.user_id,
                current_is_owner=self.is_owner,
                current_is_developer=self.is_developer)
            dlg.user_saved.connect(lambda _: self.refresh())
            dlg.exec()
        except Exception:
            logger.exception("Erreur édition utilisateur")

    def _open_reset(self):
        uid = self._selected_id()
        if not uid:
            return
        try:
            from Setting_reset_password import Setting_reset_password
            dlg = Setting_reset_password(
                parent=self, user_id=uid,
                current_user_id=self.user_id)
            dlg.password_reset.connect(lambda _: self.refresh())
            dlg.exec()
        except Exception:
            logger.exception("Erreur reset mot de passe")