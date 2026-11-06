#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_audit_log.py — Page liste du journal d'audit.
======================================================
"""

import csv
import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import is_client_mode, get_api
from Database import db, audit
from Interface_page_audit import Ui_PageAudit

logger = logging.getLogger(__name__)

PAGE_SIZE = 50

COL_DATE   = 0
COL_USER   = 1
COL_ACTION = 2
COL_CIBLE  = 3
COL_MACHINE = 4

# Actions connues (pour le filtre)
ACTIONS = [
    "CREATION_USER", "MODIF_INFO_USER", "MODIF_PERMISSIONS",
    "MODIF_MOT_DE_PASSE", "RESET_MOT_DE_PASSE",
    "ACTIVATION_USER", "DESACTIVATION_USER",
    "CONNEXION", "DECONNEXION", "ECHEC_CONNEXION",
    "ANNULATION_VENTE", "VALIDATION_BLF", "ANNULATION_BLF",
    "MODIF_STOCK_MANUEL", "EXPORT_RAPPORT", "MODIF_CONFIG",
    "CONNEXION_DEVELOPER", "ACCES_MODE_TECHNIQUE",
]

# Couleurs par famille d'action
ACTION_COLORS = {
    "CREATION_USER":        ("#15803d", "#dcfce7"),
    "MODIF_INFO_USER":      ("#1e40af", "#dbeafe"),
    "MODIF_PERMISSIONS":    ("#b45309", "#fef3c7"),
    "MODIF_MOT_DE_PASSE":   ("#b45309", "#fef3c7"),
    "RESET_MOT_DE_PASSE":   ("#b45309", "#fef3c7"),
    "ACTIVATION_USER":      ("#15803d", "#dcfce7"),
    "DESACTIVATION_USER":   ("#b91c1c", "#fee2e2"),
    "CONNEXION":            ("#1e40af", "#dbeafe"),
    "DECONNEXION":          ("#64748b", "#f1f5f9"),
    "ECHEC_CONNEXION":      ("#b91c1c", "#fee2e2"),
    "ANNULATION_VENTE":     ("#b91c1c", "#fee2e2"),
    "VALIDATION_BLF":       ("#15803d", "#dcfce7"),
    "ANNULATION_BLF":       ("#b91c1c", "#fee2e2"),
    "MODIF_STOCK_MANUEL":   ("#b45309", "#fef3c7"),
    "EXPORT_RAPPORT":       ("#1e40af", "#dbeafe"),
    "MODIF_CONFIG":         ("#b45309", "#fef3c7"),
    "CONNEXION_DEVELOPER":  ("#4338ca", "#e0e7ff"),
    "ACCES_MODE_TECHNIQUE": ("#4338ca", "#e0e7ff"),
}


class PageAudit(QtWidgets.QWidget, Ui_PageAudit):

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

        # Filtres
        self._search = ""
        self._action = ""
        self._date_debut = None
        self._date_fin = None

        self._setup_table()
        self._setup_filters()
        self._connect_signals()
        self.refresh()

    # ══════════════════════════════════════════════════════════════
    def _setup_table(self):
        h = self.audit_table.horizontalHeader()
        h.setSectionResizeMode(COL_DATE,    QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_USER,    QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_ACTION,  QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_CIBLE,   QtWidgets.QHeaderView.Stretch)
        h.setSectionResizeMode(COL_MACHINE, QtWidgets.QHeaderView.ResizeToContents)
        self.audit_table.verticalHeader().setVisible(False)
        self.audit_table.verticalHeader().setDefaultSectionSize(46)

    def _setup_filters(self):
        for act in ACTIONS:
            self.combo_action.addItem(act)
        # Dates : 30 derniers jours par défaut
        today = QtCore.QDate.currentDate()
        self.date_fin.setDate(today)
        self.date_debut.setDate(today.addDays(-30))
        self._date_debut = self.date_debut.date().toString("yyyy-MM-dd")
        self._date_fin = self.date_fin.date().toString("yyyy-MM-dd 23:59:59")

    def _connect_signals(self):
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_export_csv.clicked.connect(self._on_export_csv)
        self.btn_reset_filters.clicked.connect(self._on_reset_filters)
        self.btn_prev.clicked.connect(self._on_prev)
        self.btn_next.clicked.connect(self._on_next)

        self.inp_search.textChanged.connect(self._on_search)
        self.combo_action.currentTextChanged.connect(self._on_action_changed)
        self.date_debut.dateChanged.connect(self._on_date_changed)
        self.date_fin.dateChanged.connect(self._on_date_changed)

        self.audit_table.doubleClicked.connect(self._on_view_detail)
        self.audit_table.customContextMenuRequested.connect(self._on_context)

    # ══════════════════════════════════════════════════════════════
    def refresh(self):
        self._load_page(self._page)

    def _load_page(self, page):
        """Charge une page — API ou DB."""
        try:
            if is_client_mode():
                self._load_page_api(page)
            else:
                self._load_page_local(page)
            self._update_pagination()
        except Exception:
            logger.exception("Erreur chargement audit")

    def _load_page_local(self, page):
        """Charge depuis la DB locale (code existant)."""
        where, params = ["1=1"], []

        if self._search:
            where.append(
                "(utilisateur_name LIKE ? OR cible_nom LIKE ? "
                "OR action LIKE ? OR cible_id LIKE ?)")
            like = f"%{self._search}%"
            params.extend([like, like, like, like])

        if self._action:
            where.append("action = ?")
            params.append(self._action)

        if self._date_debut:
            where.append("date_action >= ?")
            params.append(self._date_debut)

        if self._date_fin:
            where.append("date_action <= ?")
            params.append(self._date_fin)

        wc = " AND ".join(where)

        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM AuditLog WHERE {wc}",
            tuple(params))
        self._total_count = int(row["n"] or 0) if row else 0
        self._total_pages = max(
            1, (self._total_count + PAGE_SIZE - 1) // PAGE_SIZE)
        self._page = max(1, min(page, self._total_pages))

        offset = (self._page - 1) * PAGE_SIZE
        rows = db.query(
            f"""SELECT id, date_action, utilisateur_name,
                      action, cible_type, cible_id, cible_nom,
                      machine_name
                FROM AuditLog
                WHERE {wc}
                ORDER BY date_action DESC
                LIMIT ? OFFSET ?""",
            tuple(params + [PAGE_SIZE, offset]))

        items = [dict(r) for r in rows]
        self._populate(items)

    def _load_page_api(self, page):
        """Charge via l'API."""
        api = get_api()
        if api is None:
            raise RuntimeError("API non initialisée")

        data = api.list_audit(
            page=page, per_page=PAGE_SIZE,
            action=self._action or "",
            utilisateur_id="",
            date_debut=self._date_debut or "",
            date_fin=self._date_fin or "",
        )

        self._total_count = int(data.get("total", 0))
        self._total_pages = int(data.get("pages", 1))
        self._page = int(data.get("page", 1))

        items = data.get("items", [])
        self._populate(items)

    def _populate(self, rows):
        """Remplit la table (universel : Row ou dict)."""
        t = self.audit_table
        t.blockSignals(True)
        t.setRowCount(0)
        t.clearSpans()

        if not rows:
            t.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem(
                "Aucune entrée d'audit pour les filtres actuels")
            empty.setTextAlignment(Qt.AlignCenter)
            empty.setForeground(QtGui.QColor("#94a3b8"))
            f = QtGui.QFont("Segoe UI", 11)
            f.setItalic(True)
            empty.setFont(f)
            t.setItem(0, 0, empty)
            t.setSpan(0, 0, 1, t.columnCount())
            t.blockSignals(False)
            return

        # ─── Normalise ───
        items = []
        for r in rows:
            try:
                if isinstance(r, dict):
                    items.append(r)
                else:
                    items.append({k: r[k] for k in r.keys()})
            except Exception:
                continue

        t.setRowCount(len(items))
        fn = QtGui.QFont("Segoe UI", 10)
        fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        fm = QtGui.QFont("Courier New", 9)

        for i, r in enumerate(items):
            # Date
            it0 = QtWidgets.QTableWidgetItem(str(r.get("date_action") or ""))
            it0.setFont(fm)
            it0.setForeground(QtGui.QColor("#64748b"))
            it0.setData(Qt.UserRole, r.get("id"))
            t.setItem(i, COL_DATE, it0)

            # Utilisateur
            it1 = QtWidgets.QTableWidgetItem(
                r.get("utilisateur_name") or "—")
            it1.setFont(fb)
            it1.setForeground(QtGui.QColor("#0f172a"))
            t.setItem(i, COL_USER, it1)

            # Action
            action = r.get("action") or "—"
            fg, bg = ACTION_COLORS.get(action, ("#334155", "#f1f5f9"))
            it2 = QtWidgets.QTableWidgetItem(action)
            it2.setFont(fb)
            it2.setForeground(QtGui.QColor(fg))
            it2.setBackground(QtGui.QColor(bg))
            it2.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_ACTION, it2)

            # Cible
            parts = []
            if r.get("cible_type"):
                parts.append(r["cible_type"])
            if r.get("cible_nom"):
                parts.append(r["cible_nom"])
            cible = " — ".join(parts) or "—"
            it3 = QtWidgets.QTableWidgetItem(cible)
            it3.setFont(fn)
            it3.setForeground(QtGui.QColor("#475569"))
            t.setItem(i, COL_CIBLE, it3)

            # Machine
            it4 = QtWidgets.QTableWidgetItem(r.get("machine_name") or "—")
            it4.setFont(fm)
            it4.setForeground(QtGui.QColor("#94a3b8"))
            it4.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_MACHINE, it4)

        t.blockSignals(False)

    def _update_pagination(self):
        self.lbl_page_info.setText(
            f"Page {self._page} / {self._total_pages}")
        self.btn_prev.setEnabled(self._page > 1)
        self.btn_next.setEnabled(self._page < self._total_pages)

        label = "entrée" if self._total_count <= 1 else "entrées"
        self.lbl_total_info.setText(f"{self._total_count} {label}")
        self.lbl_count_badge.setText(f"{self._total_count} {label}")

    # ══════════════════════════════════════════════════════════════
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

    def _on_action_changed(self, text):
        self._action = "" if text == "Toutes les actions" else text
        self._page = 1
        self._load_page(1)

    def _on_date_changed(self, _):
        self._date_debut = self.date_debut.date().toString("yyyy-MM-dd")
        self._date_fin = self.date_fin.date().toString("yyyy-MM-dd 23:59:59")
        self._page = 1
        self._load_page(1)

    def _on_reset_filters(self):
        self.inp_search.clear()
        self.combo_action.setCurrentIndex(0)
        today = QtCore.QDate.currentDate()
        self.date_debut.setDate(today.addDays(-30))
        self.date_fin.setDate(today)
        self._search = ""
        self._action = ""
        self._date_debut = self.date_debut.date().toString("yyyy-MM-dd")
        self._date_fin = self.date_fin.date().toString("yyyy-MM-dd 23:59:59")
        self._page = 1
        self._load_page(1)

    def _selected_id(self):
        row = self.audit_table.currentRow()
        if row < 0:
            return None
        it = self.audit_table.item(row, COL_DATE)
        return it.data(Qt.UserRole) if it else None

    # ══════════════════════════════════════════════════════════════
    def _on_view_detail(self):
        entry_id = self._selected_id()
        if not entry_id:
            return
        try:
            from Setting_audit_detail import Setting_audit_detail
            dlg = Setting_audit_detail(parent=self, entry_id=entry_id)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture détail audit")

    def _on_context(self, pos):
        row = self.audit_table.rowAt(pos.y())
        if row < 0:
            return
        self.audit_table.selectRow(row)

        menu = QtWidgets.QMenu(self)
        act_view = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/eye.svg"), "Voir le détail")
        action = menu.exec(self.audit_table.viewport().mapToGlobal(pos))
        if action == act_view:
            self._on_view_detail()

    # ══════════════════════════════════════════════════════════════
    def _on_export_csv(self):
        if self._total_count == 0:
            QtWidgets.QMessageBox.information(
                self, "Export", "Aucune entrée à exporter.")
            return

        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exporter le journal",
            f"audit_log_{QtCore.QDate.currentDate().toString('yyyyMMdd')}.csv",
            "Fichier CSV (*.csv)")
        if not path:
            return

        try:
            # Récupère TOUTES les entrées filtrées (pas seulement la page)
            # ═══ RÉCUPÉRATION (API ou DB) ═══
            if is_client_mode():
                api = get_api()
                # Récupère par pages successives (jusqu'à 1000 lignes max)
                all_items = []
                p = 1
                while p <= 20:   # 20 * 50 = 1000 max
                    data = api.list_audit(
                        page=p, per_page=50,
                        action=self._action or "",
                        date_debut=self._date_debut or "",
                        date_fin=self._date_fin or "",
                    )
                    items = data.get("items", [])
                    all_items.extend(items)
                    if len(items) < 50:
                        break
                    p += 1
                rows = all_items
            else:
                where, params = ["1=1"], []
                if self._search:
                    where.append(
                        "(utilisateur_name LIKE ? OR cible_nom LIKE ? "
                        "OR action LIKE ? OR cible_id LIKE ?)")
                    like = f"%{self._search}%"
                    params.extend([like, like, like, like])
                if self._action:
                    where.append("action = ?"); params.append(self._action)
                if self._date_debut:
                    where.append("date_action >= ?"); params.append(self._date_debut)
                if self._date_fin:
                    where.append("date_action <= ?"); params.append(self._date_fin)
                wc = " AND ".join(where)

                rows = db.query(
                    f"""SELECT date_action, utilisateur_name, action,
                              cible_type, cible_id, cible_nom,
                              details, avant, apres, machine_name
                        FROM AuditLog
                        WHERE {wc}
                        ORDER BY date_action DESC""",
                    tuple(params))

            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f, delimiter=";")
                w.writerow([
                    "Date", "Utilisateur", "Action",
                    "Type cible", "ID cible", "Nom cible",
                    "Détails", "Avant", "Après", "Machine"])
                for r in rows:
                    def _get(r, key):
                        if isinstance(r, dict):
                            return r.get(key) or ""
                        return r[key] or ""

                    w.writerow([
                        _get(r, "date_action"), _get(r, "utilisateur_name"),
                        _get(r, "action"), _get(r, "cible_type"),
                        _get(r, "cible_id"), _get(r, "cible_nom"),
                        _get(r, "details"), _get(r, "avant"),
                        _get(r, "apres"), _get(r, "machine_name")])

            QtWidgets.QMessageBox.information(
                self, "Export réussi",
                f"{len(rows)} entrée(s) exportée(s) vers :\n{path}")

            # Log de l'export
            audit.log(audit.ACTION_EXPORT_RAPPORT,
                      utilisateur_id=self.user_id,
                      cible_type="audit", cible_nom="export_csv",
                      details={"count": len(rows), "path": path})

        except Exception as e:
            logger.exception("Erreur export CSV")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", f"Export impossible :\n{e}")