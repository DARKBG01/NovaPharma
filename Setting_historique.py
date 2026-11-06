#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_historique.py — Page Historique (Ventes + Commandes).
==============================================================
"""

import csv
import logging
from datetime import datetime, timedelta

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import get_api, is_client_mode
from Database import db
from Interface_page_historique import Ui_PageHistorique

logger = logging.getLogger(__name__)

PAGE_SIZE = 100

# Colonnes Ventes
COL_V_FACT   = 0
COL_V_DATE   = 1
COL_V_ART    = 2
COL_V_QTE    = 3
COL_V_PU     = 4
COL_V_TOTAL  = 5
COL_V_CLIENT = 6
COL_V_CAISSE = 7
COL_V_STATUT = 8

# Colonnes Commandes
COL_C_NUM    = 0
COL_C_DATE   = 1
COL_C_ART    = 2
COL_C_CAT    = 3
COL_C_QTE    = 4
COL_C_PU     = 5
COL_C_TOTAL  = 6
COL_C_FOUR   = 7


class PageHistorique(QtWidgets.QWidget, Ui_PageHistorique):

    def __init__(self, parent=None, user_id=None, role="ADMIN",
                 user_name="", is_owner=False, is_developer=False):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.role = (role or "UTILISATEUR").upper()
        self.user_name = user_name or "Utilisateur"
        self.is_owner = is_owner
        self.is_developer = is_developer

        # État pagination
        self._page_v = 1
        self._total_pages_v = 1
        self._count_v = 0
        self._page_c = 1
        self._total_pages_c = 1
        self._count_c = 0

        # Filtres
        self._search = ""
        self._periode = "Tout"
        self._debut = None
        self._fin = None
        self._filtre_annule = "toutes"

        self._setup_tables()
        self._connect_signals()
        self._on_periode_changed("Tout")

    # ══════════════════════════════════════════════════════════════
    def _setup_tables(self):
        # Ventes
        h = self.table_ventes.horizontalHeader()
        h.setSectionResizeMode(COL_V_FACT,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_V_DATE,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_V_ART,    QtWidgets.QHeaderView.Stretch)
        h.setSectionResizeMode(COL_V_QTE,    QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_V_PU,     QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_V_TOTAL,  QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_V_CLIENT, QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_V_CAISSE, QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_V_STATUT, QtWidgets.QHeaderView.ResizeToContents)
        self.table_ventes.verticalHeader().setVisible(False)
        self.table_ventes.verticalHeader().setDefaultSectionSize(42)

        # Commandes
        h = self.table_commandes.horizontalHeader()
        h.setSectionResizeMode(COL_C_NUM,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_C_DATE,  QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_C_ART,   QtWidgets.QHeaderView.Stretch)
        h.setSectionResizeMode(COL_C_CAT,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_C_QTE,   QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_C_PU,    QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_C_TOTAL, QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_C_FOUR,  QtWidgets.QHeaderView.ResizeToContents)
        self.table_commandes.verticalHeader().setVisible(False)
        self.table_commandes.verticalHeader().setDefaultSectionSize(42)

    def _connect_signals(self):
        # Filtres
        self.inp_search.textChanged.connect(self._on_search_changed)
        self.combo_periode.currentTextChanged.connect(self._on_periode_changed)
        self.date_debut.dateChanged.connect(self._on_custom_date_changed)
        self.date_fin.dateChanged.connect(self._on_custom_date_changed)

        # Boutons
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_reset.clicked.connect(self._on_reset)
        self.btn_export_csv.clicked.connect(self._on_export_csv)

        # Pagination Ventes
        self.btn_prev_v.clicked.connect(self._on_prev_v)
        self.btn_next_v.clicked.connect(self._on_next_v)

        # Pagination Commandes
        self.btn_prev_c.clicked.connect(self._on_prev_c)
        self.btn_next_c.clicked.connect(self._on_next_c)

        # Table Ventes : menu contextuel + double-clic
        self.table_ventes.doubleClicked.connect(self._on_vente_double_click)
        self.table_ventes.customContextMenuRequested.connect(
            self._on_vente_context_menu)

        # Init dates
        today = QtCore.QDate.currentDate()
        self.date_debut.setDate(today.addDays(-30))
        self.date_fin.setDate(today)

    # ══════════════════════════════════════════════════════════════
    # Filtres
    # ══════════════════════════════════════════════════════════════
    def _on_search_changed(self, text):
        self._search = text.strip()
        self._page_v = 1
        self._load_ventes()

    def _on_periode_changed(self, label):
        self._periode = label
        custom = (label == "Personnalisé")
        self.date_debut.setVisible(custom)
        self.date_fin.setVisible(custom)
        self.lbl_au.setVisible(custom)

        today = datetime.now().replace(hour=23, minute=59, second=59)
        self._debut = None
        self._fin = None

        if label == "Aujourd'hui":
            self._debut = today.replace(hour=0, minute=0, second=0)
            self._fin = today
        elif label == "7 derniers jours":
            self._debut = (today - timedelta(days=7)).replace(
                hour=0, minute=0, second=0)
            self._fin = today
        elif label == "30 derniers jours":
            self._debut = (today - timedelta(days=30)).replace(
                hour=0, minute=0, second=0)
            self._fin = today
        elif label == "3 derniers mois":
            self._debut = (today - timedelta(days=90)).replace(
                hour=0, minute=0, second=0)
            self._fin = today
        elif label == "Cette année":
            self._debut = today.replace(month=1, day=1,
                                        hour=0, minute=0, second=0)
            self._fin = today
        elif label == "Personnalisé":
            self._update_custom_dates()

        self._page_v = 1
        self._load_ventes()
        self._load_commandes()

    def _on_custom_date_changed(self, _):
        if self.combo_periode.currentText() == "Personnalisé":
            self._update_custom_dates()
            self._page_v = 1
            self._load_ventes()
            self._load_commandes()

    def _update_custom_dates(self):
        d = self.date_debut.date().toPython()
        f = self.date_fin.date().toPython()
        self._debut = datetime(d.year, d.month, d.day, 0, 0, 0)
        self._fin = datetime(f.year, f.month, f.day, 23, 59, 59)

    def _on_reset(self):
        self.inp_search.clear()
        self.combo_periode.setCurrentIndex(0)
        self._search = ""
        self._page_v = 1
        self._page_c = 1
        self._load_ventes()
        self._load_commandes()

    # ══════════════════════════════════════════════════════════════
    # Filtres SQL (dates stockées en format FR)
    # ══════════════════════════════════════════════════════════════
    def _where_ventes(self):
        where = ["1=1"]
        params = []
        if self._search:
            where.append(
                "(Num_fact LIKE ? OR Article LIKE ? OR Client_name LIKE ? "
                "OR Code_reference LIKE ?)")
            like = f"%{self._search}%"
            params.extend([like, like, like, like])

        if self._debut and self._fin:
            # ⚠️ Historique.Date_vent est stocké en "DD/MM/YYYY HH:MM:SS"
            # Une comparaison string sur ce format est INCORRECTE
            # (ex : "31/12/2025" > "01/01/2026" en string).
            #
            # On convertit donc la date en ISO dans le SQL :
            # "DD/MM/YYYY HH:MM:SS" → "YYYY-MM-DD HH:MM:SS"
            #   substr(Date_vent, 7, 4) = "YYYY"      (pos 7, 4 chars)
            #   substr(Date_vent, 4, 2) = "MM"        (pos 4, 2 chars)
            #   substr(Date_vent, 1, 2) = "DD"        (pos 1, 2 chars)
            #   substr(Date_vent, 11)   = " HH:MM:SS" (pos 11 → fin)
            date_iso = (
                "substr(Date_vent, 7, 4) || '-' || "
                "substr(Date_vent, 4, 2) || '-' || "
                "substr(Date_vent, 1, 2) || "
                "substr(Date_vent, 11)"
            )
            where.append(f"({date_iso}) >= ? AND ({date_iso}) <= ?")
            params.append(self._debut.strftime("%Y-%m-%d %H:%M:%S"))
            params.append(self._fin.strftime("%Y-%m-%d %H:%M:%S"))

        return " AND ".join(where), params

    def _where_commandes(self):
        where = ["1=1"]
        params = []
        if self._search:
            where.append(
                "(Num_commande LIKE ? OR Article LIKE ? OR Entreprise LIKE ? "
                "OR Code_reference LIKE ?)")
            like = f"%{self._search}%"
            params.extend([like, like, like, like])
        if self._debut and self._fin:
            where.append("Date_commande >= ? AND Date_commande <= ?")
            params.append(self._debut.strftime("%Y-%m-%d %H:%M:%S"))
            params.append(self._fin.strftime("%Y-%m-%d %H:%M:%S"))
        return " AND ".join(where), params

    # ══════════════════════════════════════════════════════════════
    def refresh(self):
        self._load_ventes()
        self._load_commandes()

    # ══════════════════════════════════════════════════════════════
    # VENTES
    # ══════════════════════════════════════════════════════════════
    def _load_ventes(self):
        """Charge les ventes — API ou DB (avec debug)."""
        import traceback
        try:
            logger.info("=== _load_ventes démarré ===")
            logger.info("Mode client : %s", is_client_mode())

            if is_client_mode():
                logger.info("→ Appel _load_ventes_api")
                self._load_ventes_api()
            else:
                logger.info("→ Appel _load_ventes_local")
                self._load_ventes_local()

            logger.info("Après chargement : _count_v=%d, _total_pages_v=%d, _page_v=%d",
                        self._count_v, self._total_pages_v, self._page_v)

            self._update_pagination_ventes()
            self._update_stats_ventes()
            self._update_count_badge()
            logger.info("=== _load_ventes terminé ===")
        except Exception as e:
            logger.error("!!! ERREUR dans _load_ventes : %s", e)
            logger.error(traceback.format_exc())

    def _load_ventes_api(self):
        api = get_api()
        if api is None:
            raise RuntimeError("API non initialisée")

        # Filtre annulé
        annule_param = -1
        if self._filtre_annule == "validées":
            annule_param = 0
        elif self._filtre_annule == "annulées":
            annule_param = 1

        data = api.list_ventes(
            page=self._page_v, per_page=PAGE_SIZE,
            search=self._search,
            date_debut=self._debut.strftime("%Y-%m-%d") if self._debut else "",
            date_fin=self._fin.strftime("%Y-%m-%d") if self._fin else "",
            annule=annule_param,
        )

        self._count_v = int(data.get("total", 0))
        self._total_pages_v = int(data.get("pages", 1))
        self._page_v = int(data.get("page", 1))

        items = data.get("items", [])

        # Normalise pour la table
        rows = []
        for it in items:
            rows.append({
                "Num_fact": it.get("Num_fact"),
                "Date_vent": it.get("Date_vent"),
                "Article": f"{it.get('nb_articles', 0)} article(s)",
                "Quantite": it.get("nb_articles", 0),
                "Prix_uni": 0,
                "Total": it.get("total", 0),
                "Client_name": it.get("Client_name"),
                "Caisse": it.get("Caisse") or "A",
                "utilisateur_id": it.get("utilisateur_id"),
                "utilisateur_name": it.get("utilisateur_name") or "—",
                "annule": it.get("annule", 0),
                "motif_annulation": it.get("motif_annulation"),
            })
        self._populate_ventes_api(rows)
    
    def _load_ventes_local(self):
        """Charge les ventes depuis la DB (avec debug)."""
        logger.info(">>> _load_ventes_local : début")
        wc, params = self._where_ventes()
        logger.info(">>> _where_ventes → wc='%s' params=%s", wc, params)

        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM Historique WHERE {wc}",
            tuple(params))
        self._count_v = int(row["n"] or 0) if row else 0
        logger.info(">>> count = %d", self._count_v)

        self._total_pages_v = max(
            1, (self._count_v + PAGE_SIZE - 1) // PAGE_SIZE)
        self._page_v = max(1, min(self._page_v, self._total_pages_v))

        offset = (self._page_v - 1) * PAGE_SIZE
        logger.info(">>> SQL SELECT avec LIMIT=%d OFFSET=%d",
                    PAGE_SIZE, offset)

        rows = db.query(
            f"""SELECT Id, Num_fact, Date_vent, Article, Quantite,
                      Prix_uni, Total, Client_name, Caisse,
                      utilisateur_id, annule, motif_annulation,
                      Code_reference
                FROM Historique
                WHERE {wc}
                ORDER BY Id DESC
                LIMIT ? OFFSET ?""",
            tuple(params + [PAGE_SIZE, offset]))

        logger.info(">>> %d ligne(s) récupérée(s) depuis Historique", len(rows))
        if rows:
            logger.info(">>> Première ligne : %s | %s",
                        rows[0]["Num_fact"], rows[0]["Article"])

        self._populate_ventes(rows)
        logger.info(">>> _populate_ventes appelé")

    
    
    def _populate_ventes_api(self, rows):
        """Variante de _populate_ventes adaptée aux dicts API."""
        t = self.table_ventes
        t.blockSignals(True)
        t.setRowCount(0)
        t.clearSpans()

        if not rows:
            t.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem(
                "Aucune vente pour les filtres actuels")
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
        fn = QtGui.QFont("Segoe UI", 10)
        fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        fm = QtGui.QFont("Courier New", 9)
        devise = db.get_config("devise", "FC")

        for i, r in enumerate(rows):
            is_annule = int(r.get("annule") or 0) == 1

            it0 = QtWidgets.QTableWidgetItem(str(r.get("Num_fact") or ""))
            it0.setFont(fm)
            it0.setForeground(QtGui.QColor("#023E8A"))
            it0.setData(Qt.UserRole, r.get("Num_fact"))
            t.setItem(i, COL_V_FACT, it0)

            it1 = QtWidgets.QTableWidgetItem(str(r.get("Date_vent") or ""))
            it1.setFont(fn)
            it1.setForeground(QtGui.QColor("#64748b"))
            t.setItem(i, COL_V_DATE, it1)

            it2 = QtWidgets.QTableWidgetItem(r.get("Article") or "—")
            it2.setFont(fb)
            it2.setForeground(QtGui.QColor(
                "#94a3b8" if is_annule else "#0f172a"))
            t.setItem(i, COL_V_ART, it2)

            it3 = QtWidgets.QTableWidgetItem(str(int(r.get("Quantite") or 0)))
            it3.setFont(fb)
            it3.setForeground(QtGui.QColor("#0077B6"))
            it3.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_V_QTE, it3)

            it4 = QtWidgets.QTableWidgetItem("—")
            it4.setFont(fn)
            it4.setForeground(QtGui.QColor("#475569"))
            it4.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_V_PU, it4)

            it5 = QtWidgets.QTableWidgetItem(
                f"{float(r.get('Total') or 0):,.2f} {devise}".replace(",", " "))
            it5.setFont(fb)
            it5.setForeground(QtGui.QColor(
                "#94a3b8" if is_annule else "#16A34A"))
            it5.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_V_TOTAL, it5)

            it6 = QtWidgets.QTableWidgetItem(r.get("Client_name") or "—")
            it6.setFont(fn)
            it6.setForeground(QtGui.QColor("#475569"))
            t.setItem(i, COL_V_CLIENT, it6)

            it7 = QtWidgets.QTableWidgetItem(
                r.get("utilisateur_name") or "—")
            it7.setFont(fn)
            it7.setForeground(QtGui.QColor("#94a3b8"))
            t.setItem(i, COL_V_CAISSE, it7)

            if is_annule:
                txt, fg, bg = "Annulée", "#b91c1c", "#fee2e2"
            else:
                txt, fg, bg = "Validée", "#15803d", "#dcfce7"
            it8 = QtWidgets.QTableWidgetItem(txt)
            it8.setFont(fb)
            it8.setForeground(QtGui.QColor(fg))
            it8.setBackground(QtGui.QColor(bg))
            it8.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_V_STATUT, it8)

        t.blockSignals(False)

    def _populate_ventes(self, rows):
        """Remplit la table des ventes (universel : Row ou dict)."""
        t = self.table_ventes
        t.blockSignals(True)
        t.setRowCount(0)
        t.clearSpans()

        if not rows:
            t.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem(
                "Aucune vente pour les filtres actuels")
            empty.setTextAlignment(Qt.AlignCenter)
            empty.setForeground(QtGui.QColor("#94a3b8"))
            f = QtGui.QFont("Segoe UI", 11)
            f.setItalic(True)
            empty.setFont(f)
            t.setItem(0, 0, empty)
            t.setSpan(0, 0, 1, t.columnCount())
            t.blockSignals(False)
            return

        # ─── Normalise en dicts ───
        items = []
        for r in rows:
            try:
                if isinstance(r, dict):
                    items.append(r)
                else:
                    # sqlite3.Row → dict
                    items.append({k: r[k] for k in r.keys()})
            except Exception:
                continue

        # ─── Charge la map des caissiers ───
        caissier_ids = list({
            it.get("utilisateur_id")
            for it in items if it.get("utilisateur_id")
        })
        caissier_map = {}
        if caissier_ids:
            placeholders = ",".join("?" * len(caissier_ids))
            try:
                users = db.query(
                    f"""SELECT id, COALESCE(prenom, '') || ' ' ||
                               COALESCE(nom, '') AS nom
                        FROM Utilisateur
                        WHERE id IN ({placeholders})""",
                    tuple(caissier_ids))
                for u in users:
                    caissier_map[u["id"]] = u["nom"].strip() or "—"
            except Exception:
                pass

        t.setRowCount(len(items))
        fn = QtGui.QFont("Segoe UI", 10)
        fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        fm = QtGui.QFont("Courier New", 9)
        devise = db.get_config("devise", "FC")

        for i, r in enumerate(items):
            is_annule = int(r.get("annule") or 0) == 1

            # N° facture
            it0 = QtWidgets.QTableWidgetItem(str(r.get("Num_fact") or ""))
            it0.setFont(fm)
            it0.setForeground(QtGui.QColor("#023E8A"))
            it0.setData(Qt.UserRole, r.get("Num_fact"))
            t.setItem(i, COL_V_FACT, it0)

            # Date
            it1 = QtWidgets.QTableWidgetItem(str(r.get("Date_vent") or ""))
            it1.setFont(fn)
            it1.setForeground(QtGui.QColor("#64748b"))
            t.setItem(i, COL_V_DATE, it1)

            # Article (gère "nb_articles" pour mode API)
            article_txt = r.get("Article") or "—"
            if not article_txt or article_txt == "—":
                if r.get("nb_articles"):
                    article_txt = f"{r.get('nb_articles')} article(s)"
            it2 = QtWidgets.QTableWidgetItem(article_txt)
            it2.setFont(fb)
            it2.setForeground(QtGui.QColor(
                "#94a3b8" if is_annule else "#0f172a"))
            t.setItem(i, COL_V_ART, it2)

            # Quantité
            qte = int(r.get("Quantite") or r.get("nb_articles") or 0)
            it3 = QtWidgets.QTableWidgetItem(str(qte))
            it3.setFont(fb)
            it3.setForeground(QtGui.QColor("#0077B6"))
            it3.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_V_QTE, it3)

            # PU
            pu = float(r.get("Prix_uni") or 0)
            it4 = QtWidgets.QTableWidgetItem(
                f"{pu:,.2f}".replace(",", " ") if pu else "—")
            it4.setFont(fn)
            it4.setForeground(QtGui.QColor("#475569"))
            it4.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_V_PU, it4)

            # Total
            tot = float(r.get("Total") or r.get("total") or 0)
            it5 = QtWidgets.QTableWidgetItem(
                f"{tot:,.2f} {devise}".replace(",", " "))
            it5.setFont(fb)
            it5.setForeground(QtGui.QColor(
                "#94a3b8" if is_annule else "#16A34A"))
            it5.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_V_TOTAL, it5)

            # Client
            it6 = QtWidgets.QTableWidgetItem(r.get("Client_name") or "—")
            it6.setFont(fn)
            it6.setForeground(QtGui.QColor("#475569"))
            t.setItem(i, COL_V_CLIENT, it6)

            # Caissier
            nom_caissier = (r.get("utilisateur_name") or
                            caissier_map.get(r.get("utilisateur_id"), "—"))
            it7 = QtWidgets.QTableWidgetItem(nom_caissier)
            it7.setFont(fn)
            it7.setForeground(QtGui.QColor("#94a3b8"))
            t.setItem(i, COL_V_CAISSE, it7)

            # Statut
            if is_annule:
                txt, fg, bg = "Annulée", "#b91c1c", "#fee2e2"
            else:
                txt, fg, bg = "Validée", "#15803d", "#dcfce7"
            it8 = QtWidgets.QTableWidgetItem(txt)
            it8.setFont(fb)
            it8.setForeground(QtGui.QColor(fg))
            it8.setBackground(QtGui.QColor(bg))
            it8.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_V_STATUT, it8)

        t.blockSignals(False)

    def _update_stats_ventes(self):
        try:
            devise = db.get_config("devise", "FC")

            if is_client_mode():
                # En mode API, on utilise les données du serveur
                api = get_api()
                stats = api.stats_ventes_jour()
                ca = float(stats.get("ca", 0))
                n_fact = int(stats.get("nb_factures", 0))
                n_art = int(stats.get("nb_articles", 0))
                n_annul = 0  # à compléter si besoin
            else:
                wc, params = self._where_ventes()
                row = db.query_one(
                    f"""SELECT
                          COALESCE(SUM(CASE WHEN annule = 0 THEN Total ELSE 0 END), 0) AS ca,
                          COUNT(DISTINCT CASE WHEN annule = 0 THEN Num_fact END) AS n_fact,
                          COALESCE(SUM(CASE WHEN annule = 0 THEN Quantite ELSE 0 END), 0) AS n_art,
                          SUM(CASE WHEN annule = 1 THEN 1 ELSE 0 END) AS n_annul
                        FROM Historique WHERE {wc}""",
                    tuple(params))
                ca = float(row['ca'] or 0) if row else 0
                n_fact = int(row["n_fact"] or 0) if row else 0
                n_art = int(row["n_art"] or 0) if row else 0
                n_annul = int(row["n_annul"] or 0) if row else 0

            self.lbl_ca_valeur.setText(
                f"{ca:,.0f} {devise}".replace(",", " "))
            self.lbl_fact_valeur.setText(str(n_fact))
            self.lbl_articles_valeur.setText(str(n_art))
            self.lbl_annul_valeur.setText(str(n_annul))
        except Exception:
            logger.exception("Erreur stats ventes")

    def _update_pagination_ventes(self):
        self.lbl_page_v.setText(
            f"Page {self._page_v} / {self._total_pages_v}")
        self.btn_prev_v.setEnabled(self._page_v > 1)
        self.btn_next_v.setEnabled(self._page_v < self._total_pages_v)

        label = "entrée" if self._count_v <= 1 else "entrées"
        self.lbl_total_ventes.setText(f"{self._count_v} {label}")

    def _on_prev_v(self):
        if self._page_v > 1:
            self._page_v -= 1
            self._load_ventes()

    def _on_next_v(self):
        if self._page_v < self._total_pages_v:
            self._page_v += 1
            self._load_ventes()

    def _update_count_badge(self):
        total = self._count_v + self._count_c
        label = "entrée" if total <= 1 else "entrées"
        self.lbl_count_badge.setText(f"{total} {label}")

    # ══════════════════════════════════════════════════════════════
    # COMMANDES
    # ══════════════════════════════════════════════════════════════
    def _load_commandes(self):
        try:
            wc, params = self._where_commandes()

            row = db.query_one(
                f"SELECT COUNT(*) AS n FROM Historique_commande WHERE {wc}",
                tuple(params))
            self._count_c = int(row["n"] or 0) if row else 0
            self._total_pages_c = max(
                1, (self._count_c + PAGE_SIZE - 1) // PAGE_SIZE)
            self._page_c = max(1, min(self._page_c, self._total_pages_c))

            offset = (self._page_c - 1) * PAGE_SIZE
            rows = db.query(
                f"""SELECT Id, Num_commande, Date_commande, Article,
                          Categorie, Quantite, Prix_uni, Total, Entreprise
                    FROM Historique_commande
                    WHERE {wc}
                    ORDER BY Id DESC
                    LIMIT ? OFFSET ?""",
                tuple(params + [PAGE_SIZE, offset]))

            self._populate_commandes(rows)
            self._update_pagination_commandes()
            self._update_count_badge()

        except Exception:
            logger.exception("Erreur chargement commandes")

    def _populate_commandes(self, rows):
        t = self.table_commandes
        t.blockSignals(True)
        t.setRowCount(0)
        t.clearSpans()

        if not rows:
            t.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem(
                "Aucune commande pour les filtres actuels")
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
        fn = QtGui.QFont("Segoe UI", 10)
        fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        fm = QtGui.QFont("Courier New", 9)
        devise = db.get_config("devise", "FC")

        for i, r in enumerate(rows):
            # N°
            it0 = QtWidgets.QTableWidgetItem(str(r["Num_commande"] or "—"))
            it0.setFont(fm)
            it0.setForeground(QtGui.QColor("#023E8A"))
            t.setItem(i, COL_C_NUM, it0)

            # Date
            it1 = QtWidgets.QTableWidgetItem(str(r["Date_commande"]))
            it1.setFont(fn)
            it1.setForeground(QtGui.QColor("#64748b"))
            t.setItem(i, COL_C_DATE, it1)

            # Article
            it2 = QtWidgets.QTableWidgetItem(r["Article"] or "—")
            it2.setFont(fb)
            it2.setForeground(QtGui.QColor("#0f172a"))
            t.setItem(i, COL_C_ART, it2)

            # Catégorie
            it3 = QtWidgets.QTableWidgetItem(r["Categorie"] or "—")
            it3.setFont(fn)
            it3.setForeground(QtGui.QColor("#64748b"))
            it3.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_C_CAT, it3)

            # Qté
            it4 = QtWidgets.QTableWidgetItem(str(int(r["Quantite"] or 0)))
            it4.setFont(fb)
            it4.setForeground(QtGui.QColor("#0077B6"))
            it4.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_C_QTE, it4)

            # PU
            it5 = QtWidgets.QTableWidgetItem(
                f"{float(r['Prix_uni'] or 0):,.2f}".replace(",", " "))
            it5.setFont(fn)
            it5.setForeground(QtGui.QColor("#475569"))
            it5.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_C_PU, it5)

            # Total
            it6 = QtWidgets.QTableWidgetItem(
                f"{float(r['Total'] or 0):,.2f} {devise}".replace(",", " "))
            it6.setFont(fb)
            it6.setForeground(QtGui.QColor("#16A34A"))
            it6.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_C_TOTAL, it6)

            # Fournisseur
            it7 = QtWidgets.QTableWidgetItem(r["Entreprise"] or "—")
            it7.setFont(fn)
            it7.setForeground(QtGui.QColor("#475569"))
            t.setItem(i, COL_C_FOUR, it7)

        t.blockSignals(False)

    def _update_pagination_commandes(self):
        self.lbl_page_c.setText(
            f"Page {self._page_c} / {self._total_pages_c}")
        self.btn_prev_c.setEnabled(self._page_c > 1)
        self.btn_next_c.setEnabled(self._page_c < self._total_pages_c)

        label = "entrée" if self._count_c <= 1 else "entrées"
        self.lbl_total_commandes.setText(f"{self._count_c} {label}")

    def _on_prev_c(self):
        if self._page_c > 1:
            self._page_c -= 1
            self._load_commandes()

    def _on_next_c(self):
        if self._page_c < self._total_pages_c:
            self._page_c += 1
            self._load_commandes()

    # ══════════════════════════════════════════════════════════════
    # Détail facture
    # ══════════════════════════════════════════════════════════════
    def _selected_facture(self):
        row = self.table_ventes.currentRow()
        if row < 0:
            return None
        it = self.table_ventes.item(row, COL_V_FACT)
        return it.data(Qt.UserRole) if it else None

    def _on_vente_double_click(self, index):
        """Handler double-clic — utilise l'index reçu du signal."""
        try:
            row = index.row()
            it = self.table_ventes.item(row, COL_V_FACT)
            if it is None:
                return
            num_fact = it.data(Qt.UserRole)
            if num_fact:
                self._open_facture_detail(num_fact)
        except Exception:
            logger.exception("Erreur double-clic sur vente")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir le détail de la facture.")

    def _on_vente_context_menu(self, pos):
        row = self.table_ventes.rowAt(pos.y())
        if row < 0:
            return
        self.table_ventes.selectRow(row)

        num_fact = self._selected_facture()
        if not num_fact:
            return

        # Statut de la vente (pour le libellé)
        statut_libelle = ""
        try:
            it = self.table_ventes.item(row, COL_V_STATUT)
            if it:
                statut_libelle = it.text()
        except Exception:
            pass

        menu = QtWidgets.QMenu(self)
        act_view = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/eye.svg"), "Voir la facture")
        act_reprint = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/printer.svg"), "Réimprimer (PDF)")

        # ─── Retour / Avoir (ADMIN + CAISSIER, si non annulée) ───
        can_retour = (
                (self.is_owner or self.is_developer
                 or self.role in ("ADMIN", "CAISSIER"))
                and statut_libelle != "Annulée"
        )
        if can_retour:
            menu.addSeparator()
            act_retour = menu.addAction(
                QtGui.QIcon(":/Icon/Icons/arrow-left.svg"),
                "Retour / Avoir")
        else:
            act_retour = None

        # Actions admin (annulation)
        can_act = (self.is_owner or self.is_developer
                   or self.role == "ADMIN")
        if can_act and statut_libelle != "Annulée":
            menu.addSeparator()
            act_cancel = menu.addAction(
                QtGui.QIcon(":/Icon/Icons/x-circle.svg"),
                "Annuler la vente")
        else:
            act_cancel = None

        action = menu.exec(
            self.table_ventes.viewport().mapToGlobal(pos))

        if action == act_view:
            self._open_facture_detail(num_fact)
        elif action == act_reprint:
            self._reprint_from_list(num_fact)
        elif act_retour is not None and action == act_retour:
            self._on_retour_clicked(num_fact)
        elif act_cancel is not None and action == act_cancel:
            self._open_facture_detail(num_fact)  # ouvre puis annule

    def _reprint_from_list(self, num_fact: str):
        """Réimprime une facture sans ouvrir le dialogue."""
        try:
            from Setting_historique_detail import Setting_historique_detail
            dlg = Setting_historique_detail(
                parent=self,
                num_fact=num_fact,
                user_id=self.user_id,
                user_name=self.user_name,
                role=self.role,
                is_owner=self.is_owner,
                is_developer=self.is_developer)
            # Ouvre directement la réimpression
            dlg._on_reprint()
            dlg.accept()
        except Exception:
            logger.exception("Erreur réimpression rapide")

    def _open_facture_detail(self, num_fact):
        try:
            from Setting_historique_detail import Setting_historique_detail
            dlg = Setting_historique_detail(
                parent=self,
                num_fact=num_fact,
                user_id=self.user_id,
                user_name=getattr(self, "user_name", "Utilisateur"),
                role=self.role,
                is_owner=getattr(self, "is_owner", False),
                is_developer=getattr(self, "is_developer", False))
            dlg.exec()
            self.refresh()
        except ImportError as e:
            logger.exception("Module Setting_historique_detail introuvable")
            QtWidgets.QMessageBox.critical(
                self, "Module manquant",
                f"Le module 'Setting_historique_detail' est introuvable.\n\n"
                f"Vérifiez que :\n"
                f"• Setting_historique_detail.py existe\n"
                f"• Interface_historique_detail.py a été généré\n\n"
                f"Détails : {e}")
        except Exception as e:
            logger.exception("Erreur ouverture détail facture")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'ouvrir la facture :\n\n{e}")

    def _on_retour_clicked(self, num_fact: str) -> None:
        """Ouvre le dialogue de retour / avoir pour une facture."""
        try:
            from Setting_retour_vente import Setting_retour_vente
            dlg = Setting_retour_vente(
                parent=self,
                num_fact=num_fact,
                user_id=self.user_id,
                user_name=self.user_name,
                role=self.role)
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                self.refresh()
        except ImportError as e:
            logger.exception("Module Setting_retour_vente introuvable")
            QtWidgets.QMessageBox.critical(
                self, "Module manquant",
                f"Le module 'Setting_retour_vente' est introuvable.\n\n"
                f"Vérifiez que ces fichiers existent :\n"
                f"• Setting_retour_vente.py\n"
                f"• Interface_retour_vente.py (généré)\n\n"
                f"Détails : {e}")
        except Exception:
            logger.exception("Erreur ouverture dialogue retour")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir le formulaire de retour.")

    # ══════════════════════════════════════════════════════════════
    # Export CSV
    # ══════════════════════════════════════════════════════════════
    def _on_export_csv(self):
        current_tab = self.tabs.currentIndex()
        is_ventes = (current_tab == 0)

        if is_ventes and self._count_v == 0:
            QtWidgets.QMessageBox.information(
                self, "Export", "Aucune vente à exporter.")
            return
        if not is_ventes and self._count_c == 0:
            QtWidgets.QMessageBox.information(
                self, "Export", "Aucune commande à exporter.")
            return

        suffix = "ventes" if is_ventes else "commandes"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Exporter",
            f"historique_{suffix}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            "CSV (*.csv)")
        if not path:
            return

        try:
            if is_ventes:
                self._export_ventes_csv(path)
            else:
                self._export_commandes_csv(path)

            QtWidgets.QMessageBox.information(
                self, "Export réussi", f"Fichier enregistré :\n{path}")

        except Exception as e:
            logger.exception("Erreur export CSV")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _export_ventes_csv(self, path):
        wc, params = self._where_ventes()
        rows = db.query(
            f"""SELECT Num_fact, Date_vent, Article, Quantite,
                      Prix_uni, Total, Client_name, Caisse,
                      annule, motif_annulation
                FROM Historique WHERE {wc} ORDER BY Id DESC""",
            tuple(params))
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["N° Facture", "Date", "Article", "Qté",
                        "P.U", "Total", "Client", "Caisse",
                        "Statut", "Motif annulation"])
            for r in rows:
                w.writerow([
                    r["Num_fact"], r["Date_vent"], r["Article"],
                    r["Quantite"], r["Prix_uni"], r["Total"],
                    r["Client_name"], r["Caisse"],
                    "Annulée" if r["annule"] else "Validée",
                    r["motif_annulation"] or ""])

    def _export_commandes_csv(self, path):
        wc, params = self._where_commandes()
        rows = db.query(
            f"""SELECT Num_commande, Date_commande, Article, Categorie,
                      Quantite, Prix_uni, Total, Entreprise
                FROM Historique_commande WHERE {wc} ORDER BY Id DESC""",
            tuple(params))
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["N° Commande", "Date", "Article", "Catégorie",
                        "Qté", "P.U", "Total", "Fournisseur"])
            for r in rows:
                w.writerow([
                    r["Num_commande"], r["Date_commande"], r["Article"],
                    r["Categorie"], r["Quantite"], r["Prix_uni"],
                    r["Total"], r["Entreprise"]])