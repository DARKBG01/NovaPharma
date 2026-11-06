#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_surveillance.py — Page Surveillance (OWNER/DEVELOPER).
================================================================
Vue temps réel des actions suspectes + intégrité de l'audit.
"""

import logging
from datetime import datetime, timedelta

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db, audit
from Client.api_singleton import get_api, is_client_mode
from Interface_page_surveillance import Ui_PageSurveillance

logger = logging.getLogger(__name__)

PAGE_SIZE = 200

COL_DATE = 0
COL_USER = 1
COL_SEV = 2
COL_ACTION = 3
COL_CIBLE = 4
COL_IP = 5
COL_DETAILS = 6


# Couleurs par sévérité
SEV_STYLE = {
    "danger":  ("🔴 CRITIQUE", "#b91c1c", "#fee2e2"),
    "warning": ("🟠 ATTENTION", "#b45309", "#fef3c7"),
    "info":    ("🔵 INFO", "#1e40af", "#dbeafe"),
}


class PageSurveillance(QtWidgets.QWidget, Ui_PageSurveillance):

    def __init__(self, parent=None, user_id=None,
                 role="ADMIN", user_name="",
                 is_owner=False, is_developer=False):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.role = (role or "UTILISATEUR").upper()
        self.user_name = user_name or "Utilisateur"
        self.is_owner = is_owner
        self.is_developer = is_developer

        # ─── Vérif permission ───
        if not (self.is_owner or self.is_developer):
            logger.warning(
                "PageSurveillance installée sans permissions OWNER/DEV")
            QtWidgets.QMessageBox.warning(
                self, "Accès refusé",
                "Cette page est réservée au propriétaire ou développeur.")

        self._setup_icons()
        self._setup_dates()
        self._setup_table()
        self._setup_clients_tab()
        self._connect_signals()
        self._load_all()

    # ══════════════════════════════════════════════════════════════
    def _setup_icons(self):
        try:
            pix = QtGui.QPixmap(":/Icon/Icons/shield-alert_white.svg")
            if not pix.isNull():
                self.ico_surv.setPixmap(pix.scaled(
                    30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.ico_surv.setAlignment(Qt.AlignCenter)
        except Exception:
            logger.exception("Erreur setup icônes surveillance")

    def _setup_dates(self):
        today = QtCore.QDate.currentDate()
        self.date_surv_debut.setDate(today.addDays(-7))
        self.date_surv_fin.setDate(today)

    def _setup_table(self):
        h = self.table_surv.horizontalHeader()
        h.setSectionResizeMode(COL_DATE,    QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_USER,    QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_SEV,     QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_ACTION,  QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_CIBLE,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_IP,      QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_DETAILS, QtWidgets.QHeaderView.Stretch)

    def _setup_clients_tab(self):
        """Ajoute un panneau 'Postes connectés' visible sous la table actuelle."""
        try:

            # Évite double installation
            if hasattr(self, "table_clients"):
                return

            main_layout = self.layout()
            if main_layout is None:
                logger.warning("Pas de layout principal")
                return

            # ═══════════════════════════════════════════════════════════
            # 1. Conteneur "Postes connectés"
            # ═══════════════════════════════════════════════════════════
            container = QtWidgets.QFrame()
            container.setMinimumHeight(260)
            container.setStyleSheet(
                "QFrame { background: #ffffff; "
                "border: 1px solid #e2e8f0; border-radius: 12px; }")
            cv = QtWidgets.QVBoxLayout(container)
            cv.setContentsMargins(16, 14, 16, 14)
            cv.setSpacing(10)

            # Header
            h = QtWidgets.QHBoxLayout()
            h.setSpacing(10)

            icon = QtWidgets.QLabel("🖥")
            icon.setStyleSheet(
                "font-size: 20px; background: transparent; border: none;")
            h.addWidget(icon)

            title = QtWidgets.QLabel("Postes connectés au réseau")
            title.setStyleSheet(
                "color: #023E8A; font-size: 14px; font-weight: 800; "
                "background: transparent; border: none;")
            h.addWidget(title)

            h.addStretch()

            self._lbl_clients_count = QtWidgets.QLabel("—")
            self._lbl_clients_count.setStyleSheet(
                "color: #64748b; font-size: 11px; font-weight: 700; "
                "background: transparent; border: none;")
            h.addWidget(self._lbl_clients_count)

            btn_refresh = QtWidgets.QPushButton("Actualiser")
            btn_refresh.setCursor(QtCore.Qt.PointingHandCursor)
            btn_refresh.setStyleSheet("""
                QPushButton {
                    background: #eff6ff; color: #023E8A;
                    border: 1.5px solid #bfdbfe; border-radius: 10px;
                    padding: 6px 14px; font-size: 11px; font-weight: 700;
                }
                QPushButton:hover { background: #dbeafe; }
            """)
            btn_refresh.clicked.connect(self._load_clients_sessions)
            h.addWidget(btn_refresh)

            cv.addLayout(h)

            # Table
            self.table_clients = QtWidgets.QTableWidget()
            self.table_clients.setColumnCount(7)
            self.table_clients.setHorizontalHeaderLabels([
                "Statut", "Hostname", "IP", "Utilisateur",
                "Rôle", "Imprimante", "Dernière vue",
            ])
            self.table_clients.verticalHeader().setVisible(False)
            self.table_clients.verticalHeader().setDefaultSectionSize(38)
            self.table_clients.setAlternatingRowColors(True)
            self.table_clients.setSelectionBehavior(
                QtWidgets.QAbstractItemView.SelectRows)
            self.table_clients.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)
            self.table_clients.setStyleSheet("""
                QTableWidget {
                    background: #ffffff; border: none;
                    gridline-color: #f1f5f9;
                }
                QTableWidget::item {
                    padding: 6px; color: #334155;
                }
                QHeaderView::section {
                    background: #f8fafc; color: #64748b;
                    padding: 8px; border: none;
                    border-bottom: 1px solid #e2e8f0;
                    font-size: 10px; font-weight: 800;
                    letter-spacing: 1px;
                }
            """)

            hh = self.table_clients.horizontalHeader()
            hh.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            hh.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            hh.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            hh.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
            hh.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            hh.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            hh.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)

            self.table_clients.setContextMenuPolicy(
                QtCore.Qt.CustomContextMenu)
            self.table_clients.customContextMenuRequested.connect(
                self._on_client_context)

            cv.addWidget(self.table_clients)

            # ═══════════════════════════════════════════════════════════
            # 2. Insère dans le layout principal (au-dessus de la table logs)
            # ═══════════════════════════════════════════════════════════
            # Trouve l'index de la table existante pour insérer avant
            insert_idx = main_layout.count()  # par défaut = à la fin

            for i in range(main_layout.count()):
                w = main_layout.itemAt(i).widget()
                if w is self.table_surv:
                    insert_idx = i
                    break

            main_layout.insertWidget(insert_idx, container)

            logger.info("Panneau 'Postes connectés' ajouté à l'index %d",
                        insert_idx)

            # ═══════════════════════════════════════════════════════════
            # 3. Premier chargement
            # ═══════════════════════════════════════════════════════════
            self._load_clients_sessions()

            # ═══════════════════════════════════════════════════════════
            # 4. Timer toutes les 15 s
            # ═══════════════════════════════════════════════════════════
            self._timer_clients = QtCore.QTimer(self)
            self._timer_clients.timeout.connect(self._load_clients_sessions)
            self._timer_clients.start(15000)

        except Exception:
            logger.exception("Erreur _setup_clients_tab")

    def _load_clients_sessions(self):
        """Charge les sessions clients — DB locale (serveur) ou API (client)."""
        try:
            from Client.api_singleton import get_api, is_client_mode

            items = []

            # ═══════════════════════════════════════════════════════════
            # MODE SERVEUR / AUTONOME → lit la DB locale directement
            # ═══════════════════════════════════════════════════════════
            if not is_client_mode():
                logger.info("Sessions clients : lecture DB locale (serveur)")
                try:
                    from Database import db
                    # Marque comme déconnecté les sessions inactives (> 2 min)
                    from datetime import datetime, timedelta
                    threshold = (datetime.now() - timedelta(minutes=2)
                                 ).strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        db.execute("""
                            UPDATE ClientSession SET statut = 'DECONNECTE'
                            WHERE derniere_vue < ?
                              AND statut = 'CONNECTE'
                              AND bloque = 0
                        """, (threshold,))
                    except Exception:
                        pass

                    rows = db.query("""
                        SELECT * FROM ClientSession
                        ORDER BY bloque DESC, derniere_vue DESC
                    """)
                    items = [dict(r) for r in rows]
                    logger.info("Sessions DB locale : %d", len(items))
                except Exception:
                    logger.exception("Erreur lecture DB ClientSession")

            # ═══════════════════════════════════════════════════════════
            # MODE CLIENT → API
            # ═══════════════════════════════════════════════════════════
            else:
                api = get_api()
                if api is None:
                    logger.warning("Sessions clients : API non initialisée")
                    if hasattr(self, "_lbl_clients_count"):
                        self._lbl_clients_count.setText("API non prête")
                    return

                try:
                    data = api._request("GET", "/api/sessions")
                    items = data.get("items", [])
                    logger.info("Sessions API : %d", len(items))
                except Exception as e:
                    logger.warning("Erreur API sessions : %s", e)
                    if hasattr(self, "_lbl_clients_count"):
                        self._lbl_clients_count.setText("Erreur API")
                    return

            # ═══════════════════════════════════════════════════════════
            # Peuple la table (commun aux 2 modes)
            # ═══════════════════════════════════════════════════════════
            if not hasattr(self, "table_clients"):
                logger.warning("table_clients absent")
                return

            t = self.table_clients
            t.setRowCount(len(items))

            if not items:
                # Vide → message
                t.setRowCount(1)
                empty = QtWidgets.QTableWidgetItem(
                    "Aucun poste client connecté "
                    "(les heartbeats arrivent toutes les 30 s)")
                empty.setTextAlignment(Qt.AlignCenter)
                empty.setForeground(QtGui.QColor("#94a3b8"))
                f = QtGui.QFont("Segoe UI", 10)
                f.setItalic(True)
                empty.setFont(f)
                t.setItem(0, 0, empty)
                t.setSpan(0, 0, 1, t.columnCount())
                if hasattr(self, "_lbl_clients_count"):
                    self._lbl_clients_count.setText("0 connecté")
                return

            for i, s in enumerate(items):
                bloque = int(s.get("bloque") or 0) == 1
                statut = s.get("statut", "")

                if bloque:
                    badge, fg, bg = "🔒 BLOQUÉ", "#b91c1c", "#fee2e2"
                elif statut == "CONNECTE":
                    badge, fg, bg = "🟢 Connecté", "#15803d", "#dcfce7"
                else:
                    badge, fg, bg = "⚪ Déconnecté", "#64748b", "#f1f5f9"

                it0 = QtWidgets.QTableWidgetItem(badge)
                it0.setTextAlignment(Qt.AlignCenter)
                it0.setForeground(QtGui.QColor(fg))
                it0.setBackground(QtGui.QColor(bg))
                it0.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
                it0.setData(Qt.UserRole, s.get("id"))
                t.setItem(i, 0, it0)

                t.setItem(i, 1, QtWidgets.QTableWidgetItem(
                    s.get("hostname") or "—"))
                t.setItem(i, 2, QtWidgets.QTableWidgetItem(
                    s.get("ip_address") or "—"))
                t.setItem(i, 3, QtWidgets.QTableWidgetItem(
                    s.get("user_name") or "—"))

                role = s.get("role") or "—"
                it_role = QtWidgets.QTableWidgetItem(role)
                it_role.setTextAlignment(Qt.AlignCenter)
                if role == "CAISSIER":
                    it_role.setForeground(QtGui.QColor("#15803d"))
                elif role == "ADMIN":
                    it_role.setForeground(QtGui.QColor("#1e40af"))
                t.setItem(i, 4, it_role)

                t.setItem(i, 5, QtWidgets.QTableWidgetItem(
                    s.get("imprimante") or "—"))

                dv = str(s.get("derniere_vue") or "—")
                if len(dv) > 16:
                    dv = dv[11:16]
                it_dv = QtWidgets.QTableWidgetItem(dv)
                it_dv.setTextAlignment(Qt.AlignCenter)
                it_dv.setForeground(QtGui.QColor("#64748b"))
                t.setItem(i, 6, it_dv)

            if hasattr(self, "_lbl_clients_count"):
                n_connectes = sum(
                    1 for s in items if s.get("statut") == "CONNECTE")
                self._lbl_clients_count.setText(
                    f"{n_connectes} connecté(s) / {len(items)} total")

        except Exception:
            logger.exception("Erreur _load_clients_sessions")

    def _on_client_context(self, pos):
        """Menu contextuel sur un poste client."""
        row = self.table_clients.rowAt(pos.y())
        if row < 0:
            return
        self.table_clients.selectRow(row)

        it = self.table_clients.item(row, 0)
        if not it:
            return
        session_id = it.data(Qt.UserRole)
        if not session_id:
            return

        menu = QtWidgets.QMenu(self)
        act_block = menu.addAction("🔒 Bloquer ce poste")
        act_unblock = menu.addAction("🔓 Débloquer")
        menu.addSeparator()
        act_delete = menu.addAction("🚪 Forcer la déconnexion")

        action = menu.exec(self.table_clients.viewport().mapToGlobal(pos))
        if action == act_block:
            self._block_client(session_id)
        elif action == act_unblock:
            self._unblock_client(session_id)
        elif action == act_delete:
            self._delete_client_session(session_id)

    def _block_client(self, session_id):
        try:
            reason, ok = QtWidgets.QInputDialog.getText(
                self, "Bloquer le poste",
                "Raison du blocage :", QtWidgets.QLineEdit.Normal,
                "Bloqué par administrateur")
            if not ok or not reason.strip():
                return
            reason = reason.strip()

            if is_client_mode():
                # ═══ MODE CLIENT → API ═══
                from Client.api_singleton import get_api
                api = get_api()
                if api is None:
                    QtWidgets.QMessageBox.warning(
                        self, "Serveur injoignable",
                        "Impossible de bloquer : API non initialisée.")
                    return
                api._request("POST", f"/api/sessions/{session_id}/block",
                             json={"reason": reason})
            else:
                # ═══ MODE SERVEUR / AUTONOME → DB locale ═══
                db.execute("""
                    UPDATE ClientSession SET
                        bloque = 1, statut = 'BLOQUE',
                        bloque_raison = ?
                    WHERE id = ?
                """, (reason, session_id))
                logger.info(
                    "Poste bloqué localement : %s (%s)", session_id, reason)

            self._load_clients_sessions()
        except Exception:
            logger.exception("Erreur blocage poste")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "Impossible de bloquer le poste.")

    def _unblock_client(self, session_id):
        try:
            if is_client_mode():
                # ═══ MODE CLIENT → API ═══
                from Client.api_singleton import get_api
                api = get_api()
                if api is None:
                    return
                api._request(
                    "POST", f"/api/sessions/{session_id}/unblock")
            else:
                # ═══ MODE SERVEUR / AUTONOME → DB locale ═══
                db.execute("""
                    UPDATE ClientSession SET
                        bloque = 0, bloque_raison = NULL,
                        statut = 'CONNECTE'
                    WHERE id = ?
                """, (session_id,))
                logger.info("Poste débloqué localement : %s", session_id)

            self._load_clients_sessions()
        except Exception:
            logger.exception("Erreur déblocage poste")

    def _delete_client_session(self, session_id):
        try:
            rep = QtWidgets.QMessageBox.question(
                self, "Confirmer",
                "Forcer la déconnexion de ce poste ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)
            if rep != QtWidgets.QMessageBox.Yes:
                return

            if is_client_mode():
                # ═══ MODE CLIENT → API ═══
                from Client.api_singleton import get_api
                api = get_api()
                if api is None:
                    return
                api._request("DELETE", f"/api/sessions/{session_id}")
            else:
                # ═══ MODE SERVEUR / AUTONOME → DB locale ═══
                db.execute(
                    "DELETE FROM ClientSession WHERE id = ?",
                    (session_id,))
                logger.info("Session supprimée localement : %s", session_id)

            self._load_clients_sessions()
        except Exception:
            logger.exception("Erreur suppression session")

    def _connect_signals(self):
        self.btn_surv_refresh.clicked.connect(self._load_all)
        self.btn_surv_chain.clicked.connect(self._on_verify_chain)
        self.combo_surv_sev.currentTextChanged.connect(self._load_logs)
        self.inp_surv_search.textChanged.connect(self._load_logs)
        self.date_surv_debut.dateChanged.connect(self._load_logs)
        self.date_surv_fin.dateChanged.connect(self._load_logs)
        self.table_surv.doubleClicked.connect(self._on_row_clicked)

    # ══════════════════════════════════════════════════════════════
    def _load_all(self):
        self._load_kpis()
        self._load_logs()

    # ══════════════════════════════════════════════════════════════
    def _load_kpis(self):
        """Charge les 4 KPIs du header."""
        try:
            today_start = datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            ).strftime("%Y-%m-%d %H:%M:%S")

            if is_client_mode():
                # Récupère via API
                api = get_api()
                data = api.list_audit(
                    page=1, per_page=1,
                    date_debut=today_start[:10], date_fin="")
                total = int(data.get("total", 0))
                # Estimation warning+danger : requête séparée
                # (à optimiser plus tard)

                # Fallback : on fait 3 requêtes rapides
                data_w = api.list_audit(
                    page=1, per_page=1,
                    date_debut=today_start[:10], date_fin="")
                # Note : l'API ne filtre pas par sévérité pour l'instant
                self.kpi_surv_total.setText(str(total))
                self.kpi_surv_alertes.setText("—")
                self.kpi_surv_critiques.setText("—")
            else:
                # Local
                row = db.query_one(
                    "SELECT COUNT(*) AS n FROM AuditLog "
                    "WHERE date_action >= ?", (today_start,))
                total = int(row["n"] or 0) if row else 0

                row = db.query_one(
                    "SELECT COUNT(*) AS n FROM AuditLog "
                    "WHERE date_action >= ? AND severite IN ('warning','danger')",
                    (today_start,))
                alertes = int(row["n"] or 0) if row else 0

                row = db.query_one(
                    "SELECT COUNT(*) AS n FROM AuditLog "
                    "WHERE date_action >= ? AND severite = 'danger'",
                    (today_start,))
                critiques = int(row["n"] or 0) if row else 0

                self.kpi_surv_total.setText(str(total))
                self.kpi_surv_alertes.setText(str(alertes))
                self.kpi_surv_critiques.setText(str(critiques))

            # État de la chaîne (rapide, non bloquant)
            self.kpi_surv_chain.setText("✓")
            self.kpi_surv_chain.setObjectName("kpi_surv_value_ok")
        except Exception:
            logger.exception("Erreur chargement KPIs surveillance")

    # ══════════════════════════════════════════════════════════════
    def _load_logs(self):
        """Charge la liste des logs filtrés."""
        try:
            sev_filter = self._resolve_sev_filter()
            search = self.inp_surv_search.text().strip()
            d_debut = self.date_surv_debut.date().toString("yyyy-MM-dd")
            d_fin = self.date_surv_fin.date().toString("yyyy-MM-dd")

            if is_client_mode():
                api = get_api()
                data = api.list_audit(
                    page=1, per_page=PAGE_SIZE,
                    action="",
                    date_debut=d_debut, date_fin=d_fin)
                items = data.get("items", [])
                # Filtre local par sévérité et recherche
                items = self._filter_items(items, sev_filter, search)
            else:
                where, params = ["1=1"], []

                if sev_filter:
                    where.append("severite = ?")
                    params.append(sev_filter)

                if search:
                    where.append(
                        "(utilisateur_name LIKE ? OR action LIKE ? "
                        "OR cible_nom LIKE ? OR details LIKE ?)")
                    like = f"%{search}%"
                    params.extend([like, like, like, like])

                if d_debut:
                    where.append("date_action >= ?")
                    params.append(f"{d_debut} 00:00:00")
                if d_fin:
                    where.append("date_action <= ?")
                    params.append(f"{d_fin} 23:59:59")

                wc = " AND ".join(where)
                rows = db.query(
                    f"""SELECT id, date_action, utilisateur_name,
                              severite, action, cible_type, cible_nom,
                              ip_address, details
                       FROM AuditLog
                       WHERE {wc}
                       ORDER BY date_action DESC
                       LIMIT ?""",
                    tuple(params + [PAGE_SIZE]))

                items = [dict(r) for r in rows]

            self._populate(items)
        except Exception:
            logger.exception("Erreur chargement logs surveillance")

    def _resolve_sev_filter(self) -> str:
        """Retourne 'danger', 'warning', 'info' ou ''."""
        txt = self.combo_surv_sev.currentText()
        if "Danger" in txt:
            return "danger"
        if "Warning" in txt:
            return "warning"
        if "Info" in txt:
            return "info"
        return ""

    def _filter_items(self, items, sev, search):
        """Filtre côté client (mode API)."""
        out = []
        search_low = search.lower() if search else ""
        for it in items:
            if sev and it.get("severite") != sev:
                continue
            if search_low:
                haystack = " ".join([
                    str(it.get("utilisateur_name") or ""),
                    str(it.get("action") or ""),
                    str(it.get("cible_nom") or ""),
                    str(it.get("details") or ""),
                ]).lower()
                if search_low not in haystack:
                    continue
            out.append(it)
        return out

    # ══════════════════════════════════════════════════════════════
    def _populate(self, items):
        """Remplit la table."""
        t = self.table_surv
        t.blockSignals(True)
        t.setRowCount(0)
        t.clearSpans()

        if not items:
            t.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem(
                "Aucune action pour les filtres actuels")
            empty.setTextAlignment(Qt.AlignCenter)
            empty.setForeground(QtGui.QColor("#94a3b8"))
            f = QtGui.QFont("Segoe UI", 11)
            f.setItalic(True)
            empty.setFont(f)
            t.setItem(0, 0, empty)
            t.setSpan(0, 0, 1, t.columnCount())
            t.blockSignals(False)
            return

        t.setRowCount(len(items))
        fn = QtGui.QFont("Segoe UI", 10)
        fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        fm = QtGui.QFont("Courier New", 9)

        for i, r in enumerate(items):
            sev = (r.get("severite") or "info").lower()
            label, fg, bg = SEV_STYLE.get(sev, SEV_STYLE["info"])

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

            # Sévérité (badge)
            it2 = QtWidgets.QTableWidgetItem(label)
            it2.setFont(fb)
            it2.setForeground(QtGui.QColor(fg))
            it2.setBackground(QtGui.QColor(bg))
            it2.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_SEV, it2)

            # Action
            it3 = QtWidgets.QTableWidgetItem(r.get("action") or "—")
            it3.setFont(fb)
            it3.setForeground(QtGui.QColor("#1e40af"))
            t.setItem(i, COL_ACTION, it3)

            # Cible
            parts = []
            if r.get("cible_type"):
                parts.append(r["cible_type"])
            if r.get("cible_nom"):
                parts.append(r["cible_nom"])
            cible = " — ".join(parts) or "—"
            it4 = QtWidgets.QTableWidgetItem(cible)
            it4.setFont(fn)
            it4.setForeground(QtGui.QColor("#475569"))
            t.setItem(i, COL_CIBLE, it4)

            # IP
            it5 = QtWidgets.QTableWidgetItem(r.get("ip_address") or "—")
            it5.setFont(fm)
            it5.setForeground(QtGui.QColor("#94a3b8"))
            it5.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_IP, it5)

            # Détails (tronqué)
            details = str(r.get("details") or "")
            if len(details) > 80:
                details = details[:77] + "..."
            it6 = QtWidgets.QTableWidgetItem(details)
            it6.setFont(fn)
            it6.setForeground(QtGui.QColor("#64748b"))
            t.setItem(i, COL_DETAILS, it6)

        t.blockSignals(False)

    # ══════════════════════════════════════════════════════════════
    def _on_verify_chain(self):
        """Vérifie l'intégrité de la chaîne d'audit."""
        try:
            self.btn_surv_chain.setEnabled(False)
            self.btn_surv_chain.setText("Vérification…")
            QtWidgets.QApplication.processEvents()

            result = audit.verify_chain(limit=5000)

            if result["ok"]:
                self.kpi_surv_chain.setText("✓ OK")
                self.kpi_surv_chain.setObjectName("kpi_surv_value_ok")
                QtWidgets.QMessageBox.information(
                    self, "Intégrité vérifiée",
                    f"✅ {result['message']}\n\n"
                    f"Aucune falsification détectée.")
            else:
                self.kpi_surv_chain.setText("✗ RUPTURE")
                self.kpi_surv_chain.setObjectName("kpi_surv_value_danger")
                QtWidgets.QMessageBox.critical(
                    self, "🚨 ALERTE FRAUDE",
                    f"❌ {result['message']}\n\n"
                    f"Entrée #: {result.get('rupture_index')}\n"
                    f"ID: {result.get('rupture_id')}\n\n"
                    "Contactez immédiatement le développeur.")

            # Force style refresh
            self.kpi_surv_chain.style().unpolish(self.kpi_surv_chain)
            self.kpi_surv_chain.style().polish(self.kpi_surv_chain)
        except Exception as e:
            logger.exception("Erreur vérif chaîne")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", f"Impossible de vérifier : {e}")
        finally:
            self.btn_surv_chain.setEnabled(True)
            self.btn_surv_chain.setText("🔒  Vérifier l'intégrité")

    # ══════════════════════════════════════════════════════════════
    def _on_row_clicked(self, index):
        """Ouvre le détail d'une entrée."""
        try:
            row = index.row()
            it = self.table_surv.item(row, COL_DATE)
            if not it:
                return
            entry_id = it.data(Qt.UserRole)
            if not entry_id:
                return

            from Setting_audit_detail import Setting_audit_detail
            dlg = Setting_audit_detail(parent=self, entry_id=entry_id)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture détail")