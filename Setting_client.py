#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page_clients.py — Page de gestion des clients.
================================================
Compatible mode autonome (DB locale) et mode client (API).
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore

from Database import db
from Client.api_singleton import get_api, is_client_mode
from Interface_client import Ui_PageClients

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
PAGE_SIZE = 50

# Colonnes
COL_NAME    = 0
COL_SEXE    = 1   # ← AJOUT
COL_NUMERO  = 2
COL_TOTAL   = 3
COL_VISITS  = 4
COL_LAST    = 5
COL_STATUS  = 6


FILTERS_LOCAL = {
    "Tous les clients":   "1=1",
    "Clients actifs":     "actif = 1 AND numero NOT LIKE 'ANON-%'",
    "Clients anonymes":   "numero LIKE 'ANON-%'",
    "Clients inactifs":   "actif = 0",
}

FILTERS_API = {
    "Tous les clients":  "tous",
    "Clients actifs":    "actifs",
    "Clients anonymes":  "anonymes",
    "Clients inactifs":  "inactifs",
}


class PageClients(QtWidgets.QWidget, Ui_PageClients):

    def __init__(self, parent=None, user_id: str = None, role: str = "ADMIN"):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.role = (role or "UTILISATEUR").upper()

        self._page = 1
        self._total_pages = 1
        self._total_count = 0
        self._search_term = ""
        self._filter_label = "Tous les clients"

        self._connect_signals()
        self.refresh()

    # ------------------------------------------------------------------
    def _connect_signals(self):
        for btn_name, slot in (
            ("btn_new",     self._on_new),
            ("btn_new_clients", self._on_new),
            ("btn_refresh", self.refresh),
            ("btn_refresh_clients", self.refresh),
            ("btn_prev",    self._on_prev),
            ("btn_prev_clients", self._on_prev),
            ("btn_next",    self._on_next),
            ("btn_next_clients", self._on_next),
            ("btn_view",    self._on_view),
            ("btn_view_clients", self._on_view),
            ("btn_edit",    self._on_edit),
            ("btn_edit_clients", self._on_edit),
            ("btn_delete",  self._on_delete),
            ("btn_delete_clients", self._on_delete),
        ):
            w = getattr(self, btn_name, None)
            if w is not None:
                try:
                    w.clicked.connect(slot)
                except Exception:
                    pass

        for inp_name in ("search_input", "search_input_clients"):
            w = getattr(self, inp_name, None)
            if w is not None:
                w.textChanged.connect(self._on_search_changed)
                try:
                    w.returnPressed.connect(self._on_search_enter)
                except Exception:
                    pass

        for combo_name in ("filter_combo", "filter_combo_clients"):
            w = getattr(self, combo_name, None)
            if w is not None:
                w.currentTextChanged.connect(self._on_filter_changed)

        if hasattr(self, "clients_table"):
            self.clients_table.itemSelectionChanged.connect(
                self._on_selection_changed)
            self.clients_table.doubleClicked.connect(self._on_view)
            self.clients_table.setContextMenuPolicy(
                QtCore.Qt.CustomContextMenu)
            self.clients_table.customContextMenuRequested.connect(
                self._on_context_menu)

    # ------------------------------------------------------------------
    # Chargement des données — ROUTEUR API/DB
    # ------------------------------------------------------------------
    def refresh(self):
        self._load_page(self._page)

    def _load_page(self, page: int):
        """Charge une page — mode client ou autonome."""
        try:
            if is_client_mode():
                self._load_page_api(page)
            else:
                self._load_page_local(page)

            self._update_pagination()
            self._update_count_badge()

        except Exception:
            logger.exception("Erreur chargement page clients")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible de charger la liste des clients.")

    # ─── MODE CLIENT (via API) ───
    def _load_page_api(self, page: int):
        api = get_api()
        if api is None:
            raise RuntimeError("API non initialisée")

        data = api.list_clients(
            page=page,
            per_page=PAGE_SIZE,
            search=self._search_term,
            filtre=FILTERS_API.get(self._filter_label, "tous"),
        )

        self._total_count = int(data.get("total", 0))
        self._total_pages = int(data.get("pages", 1))
        self._page = int(data.get("page", 1))

        items = data.get("items", [])
        self._populate_table(items)

    # ─── MODE AUTONOME / SERVEUR (DB locale) ───
    def _load_page_local(self, page: int):
        where = [FILTERS_LOCAL.get(self._filter_label, "1=1")]
        params = []
        if self._search_term:
            where.append("(nom LIKE ? OR numero LIKE ? OR C_name LIKE ?)")
            like = f"%{self._search_term}%"
            params.extend([like, like, like])

        where_clause = " AND ".join(where)

        count_row = db.query_one(
            f"SELECT COUNT(*) AS n FROM Client WHERE {where_clause}",
            tuple(params))
        self._total_count = int(count_row["n"] or 0) if count_row else 0
        self._total_pages = max(
            1, (self._total_count + PAGE_SIZE - 1) // PAGE_SIZE)
        self._page = max(1, min(page, self._total_pages))

        offset = (self._page - 1) * PAGE_SIZE
        rows = db.query(
            f"""SELECT id,
                      COALESCE(C_name, nom) AS display_name,
                      COALESCE(numero, '') AS display_numero,
                      COALESCE(Montant_total, 0) AS montant,
                      COALESCE(sexe, 'M') AS sexe,
                      actif
               FROM Client
               WHERE {where_clause}
               ORDER BY display_name COLLATE NOCASE ASC
               LIMIT ? OFFSET ?""",
            tuple(params + [PAGE_SIZE, offset]))

        # Normalise pour la même structure que l'API
        items = []
        for r in rows:
            items.append({
                "id": r["id"],
                "nom": r["display_name"] or "—",
                "sexe": r["sexe"] or "M",
                "numero": r["display_numero"] or "—",
                "Montant_total": float(r["montant"] or 0),
                "actif": int(r["actif"] or 0),
            })
        # ═══ AJOUT : calcule les stats en batch ═══
        stats = self._load_client_stats_batch(items)

        self._populate_table(items, stats=stats)  # ← passer stats

    # ─── Rendu commun ───
    def _populate_table(self, items,stats : dict = None):
        """Remplit la table depuis une liste de dicts normalisés."""
        table = self.clients_table
        table.blockSignals(True)
        table.setRowCount(0)

        if not items:
            table.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem("Aucun client à afficher")
            empty.setTextAlignment(QtCore.Qt.AlignCenter)
            empty.setForeground(QtGui.QColor("#94a3b8"))
            font = QtGui.QFont("Segoe UI", 11)
            font.setItalic(True)
            empty.setFont(font)
            table.setItem(0, 0, empty)
            table.setSpan(0, 0, 1, table.columnCount())
            table.blockSignals(False)
            return

        table.setRowCount(len(items))

        font_normal = QtGui.QFont("Segoe UI", 10)
        font_bold   = QtGui.QFont("Segoe UI", 10)
        font_bold.setBold(True)
        font_mono   = QtGui.QFont("Courier New", 9)

        for i, r in enumerate(items):
            client_id    = r.get("id")
            display_name = r.get("nom") or "—"
            numero       = r.get("numero") or "—"
            montant      = float(r.get("Montant_total") or 0)
            actif        = int(r.get("actif") or 0)

            item_name = QtWidgets.QTableWidgetItem(display_name)
            item_name.setFont(font_bold)
            item_name.setForeground(QtGui.QColor("#0f172a"))
            item_name.setData(QtCore.Qt.UserRole, client_id)
            table.setItem(i, COL_NAME, item_name)

            item_num = QtWidgets.QTableWidgetItem(numero)
            item_num.setFont(font_mono)
            item_num.setForeground(QtGui.QColor("#64748b"))
            table.setItem(i, COL_NUMERO, item_num)

            # Sexe
            sexe = (r.get("sexe") or "M").upper()
            item_sexe = QtWidgets.QTableWidgetItem(
                "M" if sexe == "M" else "F")
            item_sexe.setTextAlignment(QtCore.Qt.AlignCenter)
            item_sexe.setFont(font_bold)
            if sexe == "M":
                item_sexe.setForeground(QtGui.QColor("#1e40af"))
                item_sexe.setBackground(QtGui.QColor("#dbeafe"))
            else:
                item_sexe.setForeground(QtGui.QColor("#be185d"))
                item_sexe.setBackground(QtGui.QColor("#fce7f3"))
            table.setItem(i, COL_SEXE, item_sexe)

            item_total = QtWidgets.QTableWidgetItem(
                f"{montant:,.2f} FC".replace(",", " "))
            item_total.setFont(font_bold)
            item_total.setForeground(QtGui.QColor("#16A34A"))
            item_total.setTextAlignment(
                QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            table.setItem(i, COL_TOTAL, item_total)

            item_visits = QtWidgets.QTableWidgetItem("—")
            item_visits.setFont(font_normal)
            item_visits.setForeground(QtGui.QColor("#94a3b8"))
            item_visits.setTextAlignment(QtCore.Qt.AlignCenter)
            table.setItem(i, COL_VISITS, item_visits)

            item_last = QtWidgets.QTableWidgetItem("—")
            item_last.setFont(font_normal)
            item_last.setForeground(QtGui.QColor("#94a3b8"))
            item_last.setTextAlignment(QtCore.Qt.AlignCenter)
            table.setItem(i, COL_LAST, item_last)

            if not actif:
                text, fg, bg = "Inactif", "#64748b", "#f1f5f9"
            elif str(numero).startswith("ANON-"):
                text, fg, bg = "Anonyme", "#92400e", "#fef3c7"
            else:
                text, fg, bg = "Actif", "#15803d", "#dcfce7"

            item_status = QtWidgets.QTableWidgetItem(text)
            item_status.setFont(font_bold)
            item_status.setForeground(QtGui.QColor(fg))
            item_status.setBackground(QtGui.QColor(bg))
            item_status.setTextAlignment(QtCore.Qt.AlignCenter)
            table.setItem(i, COL_STATUS, item_status)

            # ─── NOUVEAU : Visites + Dernière visite ───
            nom = r.get("nom") or ""
            num = r.get("numero") or ""
            exact_name = f"{nom} {num}".strip() if num else nom
            st = (stats or {}).get(exact_name, {})
            n_visits = st.get("n_visits", 0)
            last_visit = st.get("last_visit")

            item_visits = QtWidgets.QTableWidgetItem(
                str(n_visits) if n_visits else "—")
            item_visits.setFont(font_normal)
            item_visits.setForeground(QtGui.QColor(
                "#0f172a" if n_visits else "#94a3b8"))
            item_visits.setTextAlignment(QtCore.Qt.AlignCenter)
            table.setItem(i, COL_VISITS, item_visits)

            last_str = "—"
            if last_visit:
                last_str = str(last_visit).split(" ")[0]  # Date seule
            item_last = QtWidgets.QTableWidgetItem(last_str)
            item_last.setFont(font_normal)
            item_last.setForeground(QtGui.QColor(
                "#0f172a" if last_visit else "#94a3b8"))
            item_last.setTextAlignment(QtCore.Qt.AlignCenter)
            table.setItem(i, COL_LAST, item_last)

        table.blockSignals(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(COL_NAME,   QtWidgets.QHeaderView.Stretch)
        for c in (COL_NUMERO, COL_TOTAL, COL_VISITS, COL_LAST, COL_STATUS):
            header.setSectionResizeMode(
                c, QtWidgets.QHeaderView.ResizeToContents)

    # ------------------------------------------------------------------
    # Pagination
    # ------------------------------------------------------------------
    def _update_pagination(self):
        try:
            self.page_info.setText(f"Page {self._page} / {self._total_pages}")
            self.btn_prev.setEnabled(self._page > 1)
            self.btn_next.setEnabled(self._page < self._total_pages)

            total_label = "client" if self._total_count <= 1 else "clients"
            self.total_info.setText(f"{self._total_count} {total_label}")
        except Exception:
            pass

    def _update_count_badge(self):
        try:
            total = self._total_count
            label = "client" if total <= 1 else "clients"
            self.count_badge.setText(f"{total} {label}")
        except Exception:
            pass

    def _on_prev(self):
        if self._page > 1:
            self._load_page(self._page - 1)

    def _on_next(self):
        if self._page < self._total_pages:
            self._load_page(self._page + 1)

    def _on_search_changed(self, text: str):
        self._search_term = text.strip()
        self._page = 1
        self._load_page(1)

    def _on_search_enter(self):
        self._search_term = self.search_input.text().strip()
        self._page = 1
        self._load_page(1)

    def _on_filter_changed(self, text: str):
        self._filter_label = text
        self._page = 1
        self._load_page(1)

    # ------------------------------------------------------------------
    # Sélection
    # ------------------------------------------------------------------
    def _on_selection_changed(self):
        has_selection = self._selected_client_id() is not None
        try:
            self.btn_view.setEnabled(has_selection)
            self.btn_edit.setEnabled(has_selection)
            self.btn_delete.setEnabled(
                has_selection and self.role == "ADMIN")
        except Exception:
            pass

    def _selected_client_id(self):
        row = self.clients_table.currentRow()
        if row < 0:
            return None
        item = self.clients_table.item(row, COL_NAME)
        if not item:
            return None
        return item.data(QtCore.Qt.UserRole)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def _on_new(self):
        try:
            from Setting_client_dialog import Setting_client_dialog
            dlg = Setting_client_dialog(parent=self, user_id=self.user_id)
            dlg.client_saved.connect(self._on_client_saved)
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                self._load_page(1)
        except Exception:
            logger.exception("Erreur ouverture dialogue nouveau client")

    def _on_view(self):
        client_id = self._selected_client_id()
        if not client_id:
            return
        try:
            from Setting_client_information import ClientInfoDialog
            dlg = ClientInfoDialog(
                parent=self, client_id=client_id,
                user_id=self.user_id, role=self.role)
            dlg.client_deleted.connect(lambda _: self.refresh())
            dlg.client_edited.connect(lambda _: self.refresh())
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture fiche client")

    def _on_edit(self):
        client_id = self._selected_client_id()
        if not client_id:
            return
        try:
            from Setting_client_dialog import Setting_client_dialog
            dlg = Setting_client_dialog(
                parent=self, client_id=client_id, user_id=self.user_id)
            dlg.client_saved.connect(self._on_client_saved)
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                self.refresh()
        except Exception:
            logger.exception("Erreur édition client")

    def _on_delete(self):
        client_id = self._selected_client_id()
        if not client_id:
            return
        if self.role != "ADMIN":
            QtWidgets.QMessageBox.warning(
                self, "Accès refusé",
                "Seul un administrateur peut supprimer un client.")
            return
        try:
            from Setting_client_information import ClientInfoDialog
            dlg = ClientInfoDialog(
                parent=self, client_id=client_id,
                user_id=self.user_id, role=self.role)
            dlg.client_deleted.connect(lambda _: self.refresh())
            dlg.client_edited.connect(lambda _: self.refresh())
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture fiche pour suppression")

    def _on_context_menu(self, pos):
        row = self.clients_table.rowAt(pos.y())
        if row < 0:
            return
        self.clients_table.selectRow(row)

        menu = QtWidgets.QMenu(self)
        act_view = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/eye.svg"), "Voir la fiche")
        act_edit = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/edit.svg"), "Modifier")
        menu.addSeparator()
        act_del = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/trash.svg"), "Supprimer")
        act_del.setEnabled(self.role == "ADMIN")

        action = menu.exec(self.clients_table.viewport().mapToGlobal(pos))
        if action == act_view:
            self._on_view()
        elif action == act_edit:
            self._on_edit()
        elif action == act_del:
            self._on_delete()

    def _on_client_saved(self, client_id: str):
        logger.info("Client enregistré : %s", client_id)
        self.refresh()

    def _load_client_stats_batch(self, client_items: list) -> dict:
        """
        Calcule les stats (nb_visites, derniere_visite) pour tous les clients
        en une seule requête SQL.
        """
        if not client_items:
            return {}

        stats = {}
        try:
            exact_names = []
            for c in client_items:
                nom = c.get("nom") or ""
                num = c.get("numero") or ""
                if not nom:
                    continue
                exact_name = f"{nom} {num}".strip() if num else nom
                exact_names.append(exact_name)

            if not exact_names:
                return {}

            where = " OR ".join("Client_name = ?" for _ in exact_names)
            rows = db.query(
                f"""SELECT Client_name,
                                   COUNT(DISTINCT Num_fact) AS n_visits,
                                   MAX(Date_vent) AS last_visit
                            FROM Historique
                            WHERE {where}
                            GROUP BY Client_name""",
                tuple(exact_names))

            # Mapping direct Client_name → stats
            for r in rows:
                cn = r["Client_name"] or ""
                stats[cn] = {
                    "n_visits": int(r["n_visits"] or 0),
                    "last_visit": r["last_visit"],
                }
        except Exception:
            logger.exception("Erreur batch stats clients")

        return stats