#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_rapports.py — Dialogue des 3 rapports.
================================================
"""

import logging
import os
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from reportlab.lib.units import cm

from Database import db, audit, printer_manager
from Database import rapport_engine as engine
from Database import rapport_export as export
from Client.api_singleton import get_api, is_client_mode
from Interface_page_rapports import Ui_PageRapports

logger = logging.getLogger(__name__)


class PageRapports(QtWidgets.QWidget, Ui_PageRapports):

    def __init__(self, parent=None, user_id=None, user_name=""):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"

        self._debut = None
        self._fin = None
        self._debut_n1 = None
        self._fin_n1 = None
        self._topn = 10
        self._current_data = {}   # cache pour les exports
        self._use_api_data = False

        self._connect_signals()
        self._apply_styles()
        self._setup_scroll_areas()
        self._generer()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        self.combo_periode.currentTextChanged.connect(self._on_periode_changed)
        self.date_debut.dateChanged.connect(self._on_date_changed)
        self.date_fin.dateChanged.connect(self._on_date_changed)
        self.combo_topn.currentTextChanged.connect(self._on_topn_changed)
        self.btn_generer.clicked.connect(self._generer)
        self.btn_export_csv.clicked.connect(self._export_csv)
        self.btn_export_excel.clicked.connect(self._export_excel)
        self.btn_export_pdf.clicked.connect(self._export_pdf)

    def _apply_styles(self):
        today = QtCore.QDate.currentDate()
        self.date_debut.setDate(today.addDays(-30))
        self.date_fin.setDate(today)

    # ══════════════════════════════════════════════════════════════
    def _on_periode_changed(self, label):
        custom = (label == "Personnalisé")
        self.date_debut.setVisible(custom)
        self.date_fin.setVisible(custom)
        self.lbl_au.setVisible(custom)
        self._generer()

    def _on_date_changed(self, _):
        if self.combo_periode.currentText() != "Personnalisé":
            return
        # Anti-rebond : ne régénère que 200 ms après le dernier clic
        if hasattr(self, "_date_timer"):
            self._date_timer.stop()
        else:
            self._date_timer = QtCore.QTimer(self)
            self._date_timer.setSingleShot(True)
            self._date_timer.timeout.connect(self._generer)
        self._date_timer.start(200)

    def _on_topn_changed(self, text):
        try:
            self._topn = int(text)
        except ValueError:
            self._topn = 10
        self._generer()

    # ══════════════════════════════════════════════════════════════
    def _generer(self):
        if getattr(self, "_generating", False):
            return
        self._generating = True
        try:
            self.lbl_status.setText("Génération…")
            QtWidgets.QApplication.processEvents()

            label = self.combo_periode.currentText()
            cs = self.date_debut.date().toPython() if \
                 label == "Personnalisé" else None
            ce = self.date_fin.date().toPython() if \
                 label == "Personnalisé" else None

            if cs:
                from datetime import datetime as dt
                cs = dt(cs.year, cs.month, cs.day)
            if ce:
                from datetime import datetime as dt
                ce = dt(ce.year, ce.month, ce.day)

            # ═══ RÉCUPÉRATION DES DONNÉES ═══
            if is_client_mode():
                self._fetch_data_api(label, cs, ce)
            else:
                self._fetch_data_local(label, cs, ce)

            self.lbl_periode_active.setText(
                f"Du {self._debut[:10]} au {self._fin[:10]}")

            # ═══ RENDU ═══
            self._render_ventes()
            self._render_equipe()
            self._render_operations()

            self.lbl_status.setText(
                f"Généré à {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            logger.exception("Erreur génération rapports")
            self.lbl_status.setText(f"Erreur : {e}")
        finally:
            self._generating = False

    def _fetch_data_local(self, label, cs, ce):
        """Récupère les données depuis la DB locale."""
        self._debut, self._fin, self._debut_n1, self._fin_n1 = \
            engine.resolve_period(label, cs, ce)
        self._use_api_data = False

    def _fetch_data_api(self, label, cs, ce):
        """Récupère les données via l'API."""
        api = get_api()
        if api is None:
            raise RuntimeError("API non initialisée")

        ds = cs.strftime("%Y-%m-%d") if cs else ""
        df = ce.strftime("%Y-%m-%d") if ce else ""

        data_v = api.rapport_ventes(
            periode=label, date_debut=ds, date_fin=df, topn=self._topn)
        data_e = api.rapport_equipe(
            periode=label, date_debut=ds, date_fin=df)
        data_o = api.rapport_operations(
            periode=label, date_debut=ds, date_fin=df)

        p = data_v.get("periode", {})
        self._debut = p.get("debut", "")
        self._fin = p.get("fin", "")
        self._debut_n1 = p.get("debut_n1", "")
        self._fin_n1 = p.get("fin_n1", "")

        self._current_data = {
            "ventes_kpi": data_v.get("kpi", {}),
            "ventes_kpi_n1": data_v.get("kpi_n1", {}),
            "ventes_var": data_v.get("variation", {}),
            "top_produits": data_v.get("top_produits", []),
            "categories": data_v.get("categories", []),
            "vendeurs": data_e.get("vendeurs", []),
            "annulations": data_e.get("annulations", []),
            "marges": data_o.get("marges", []),
            "stock": data_o.get("stock", {}),
            "clients": data_o.get("clients", {}),
            "operations": data_o.get("operations", {}),
        }
        self._use_api_data = True

    # ══════════════════════════════════════════════════════════════
    # ONGLET 1 : VENTES
    # ══════════════════════════════════════════════════════════════
    def _render_ventes(self):
        """Rendu Ventes — hybride."""
        devise = db.get_config("devise", "FC")

        # ═══ RÉCUPÉRATION ═══
        if is_client_mode() and getattr(self, "_use_api_data", False):
            kpi = self._current_data.get("ventes_kpi", {})
            kpi_n1 = self._current_data.get("ventes_kpi_n1", {})
            var = self._current_data.get("ventes_var", {})
            top = self._current_data.get("top_produits", [])
        else:
            kpi = engine.compute_kpis(self._debut, self._fin)
            kpi_n1 = engine.compute_kpis(self._debut_n1, self._fin_n1)
            var = engine.compare_n1(kpi, kpi_n1)
            top = engine.top_produits(self._debut, self._fin, self._topn)

            self._current_data["ventes_kpi"] = kpi
            self._current_data["ventes_kpi_n1"] = kpi_n1
            self._current_data["ventes_var"] = var
            self._current_data["top_produits"] = top

        # ═══ KPIs ═══
        self.kpi_ca_value.setText(
            f"{kpi.get('ca_total', 0):,.0f} {devise}".replace(",", " "))
        self.kpi_ventes_value.setText(str(kpi.get("nb_ventes", 0)))
        self.kpi_panier_value.setText(
            f"{kpi.get('panier_moyen', 0):,.0f} {devise}".replace(",", " "))
        self.kpi_clients_value.setText(str(kpi.get("nb_clients", 0)))
        self.kpi_articles_value.setText(str(kpi.get("nb_articles", 0)))

        self._set_var_label(self.kpi_ca_var, var.get("ca_total"))
        self._set_var_label(self.kpi_ventes_var, var.get("nb_ventes"))
        self._set_var_label(self.kpi_panier_var, var.get("panier_moyen"))
        self._set_var_label(self.kpi_clients_var, var.get("nb_clients"))
        self._set_var_label(self.kpi_articles_var, var.get("nb_articles"))

        # ═══ TOP PRODUITS ═══
        total_ca = sum(t.get("ca", 0) for t in top) or 1
        self.table_top_produits.setRowCount(len(top))
        for i, t in enumerate(top):
            part = (t.get("ca", 0) / total_ca) * 100
            items = [
                t.get("nom", "—"),
                t.get("categorie", "—"),
                str(int(t.get("qte", 0))),
                f"{t.get('ca', 0):,.0f} {devise}".replace(",", " "),
                f"{part:.1f} %",
            ]
            for j, v in enumerate(items):
                it = QtWidgets.QTableWidgetItem(str(v))
                if j == 0:
                    it.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                if j >= 2:
                    it.setTextAlignment(Qt.AlignCenter)
                self.table_top_produits.setItem(i, j, it)

        h = self.table_top_produits.horizontalHeader()
        h.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for j in (1, 2, 3, 4):
            h.setSectionResizeMode(j, QtWidgets.QHeaderView.ResizeToContents)

        # ═══ GRAPHIQUES ═══
        if is_client_mode() and getattr(self, "_use_api_data", False):
            self._render_charts_api_message()
        else:
            self._render_chart_ca()
            self._render_chart_cat()

    def _render_charts_api_message(self):
        """En mode API, on remplace les graphiques par un message."""
        for layout, title_obj in (
            (self.chart_ca.layout(), "chart_ca_title"),
            (self.chart_cat.layout(), "chart_cat_title"),
        ):
            try:
                self._clean_layout_keep_title(layout, title_obj)
                lbl = QtWidgets.QLabel(
                    "Graphique disponible uniquement en mode local.\n"
                    "Utilisez les tableaux ci-dessous pour l'analyse.")
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet(
                    "color: #94a3b8; font-size: 11px; "
                    "font-style: italic; background: transparent;")
                layout.addWidget(lbl)
            except Exception:
                logger.exception("Erreur remplacement graphique")

    def _render_chart_ca(self):
        try:
            from PySide6.QtCharts import (
                QChart, QChartView, QLineSeries, QValueAxis
            )
            from PySide6.QtCore import QPointF

            layout = self.chart_ca.layout()

            # ═══ Nettoyage : garde SEULEMENT le titre (chart_ca_title) ═══
            self._clean_layout_keep_title(layout, "chart_ca_title")

            # ═══ Récupère les données ═══
            serie = engine.serie_ca_journalier(self._debut, self._fin)

            if not serie:
                lbl = QtWidgets.QLabel("Aucune donnée sur la période")
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet(
                    "color: #94a3b8; font-size: 12px; "
                    "font-style: italic; background: transparent;")
                layout.addWidget(lbl)
                return

            # ═══ Crée le nouveau chart ═══
            chart = QChart()
            chart.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#ffffff")))
            chart.setPlotAreaBackgroundBrush(
                QtGui.QBrush(QtGui.QColor("#ffffff")))
            chart.setPlotAreaBackgroundVisible(True)
            chart.setMargins(QtCore.QMargins(8, 8, 8, 8))
            chart.legend().hide()

            series = QLineSeries()
            pen = QtGui.QPen(QtGui.QColor("#0077B6"))
            pen.setWidth(2)
            series.setPen(pen)

            max_y = 0.0
            for i, (_, ca) in enumerate(serie):
                series.append(float(i), float(ca))
                max_y = max(max_y, float(ca))

            chart.addSeries(series)

            # ─── Axe X ───
            axis_x = QValueAxis()
            axis_x.setLabelFormat("%d")
            axis_x.setLabelsColor(QtGui.QColor("#64748b"))
            axis_x.setLabelsFont(QtGui.QFont("Segoe UI", 8))
            axis_x.setGridLineVisible(False)
            axis_x.setLinePenColor(QtGui.QColor("#cbd5e1"))
            axis_x.setRange(0, max(len(serie) - 1, 1))
            axis_x.setTickCount(min(len(serie), 10))
            chart.addAxis(axis_x, Qt.AlignBottom)
            series.attachAxis(axis_x)

            # ─── Axe Y ───
            axis_y = QValueAxis()
            axis_y.setLabelFormat("%.0f")
            axis_y.setLabelsColor(QtGui.QColor("#64748b"))
            axis_y.setLabelsFont(QtGui.QFont("Segoe UI", 8))
            axis_y.setGridLineColor(QtGui.QColor("#e2e8f0"))
            axis_y.setLinePenColor(QtGui.QColor("#cbd5e1"))
            axis_y.setRange(0, max_y * 1.15 if max_y > 0 else 10)
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_y)

            view = QChartView(chart)
            view.setRenderHint(QtGui.QPainter.Antialiasing)
            view.setStyleSheet("background: transparent; border: none;")
            view.setMinimumHeight(220)
            layout.addWidget(view)

        except Exception:
            logger.exception("Erreur graphique CA")

    def _render_chart_cat(self):
        try:
            from PySide6.QtCharts import QChart, QChartView, QPieSeries

            layout = self.chart_cat.layout()

            # ═══ Nettoyage : garde SEULEMENT le titre (chart_cat_title) ═══
            self._clean_layout_keep_title(layout, "chart_cat_title")

            # ═══ Données ═══
            data = engine.repartition_categories(self._debut, self._fin)
            data = [(d["cat"], d["ca"]) for d in data if d["ca"] > 0]

            if not data:
                lbl = QtWidgets.QLabel("Aucune donnée")
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet(
                    "color: #94a3b8; font-size: 12px; "
                    "font-style: italic; background: transparent;")
                layout.addWidget(lbl)
                return

            # ═══ Chart ═══
            chart = QChart()
            chart.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#ffffff")))
            chart.setMargins(QtCore.QMargins(4, 4, 4, 4))

            series = QPieSeries()
            palette = ["#023E8A", "#0077B6", "#00B4D8", "#90E0EF",
                       "#F4A261", "#16A34A", "#DC2626", "#a855f7"]

            for i, (cat, ca) in enumerate(data[:8]):
                slice_ = series.append(str(cat), float(ca))
                slice_.setBrush(QtGui.QColor(palette[i % len(palette)]))
                slice_.setLabelVisible(False)

            chart.addSeries(series)
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)
            chart.legend().setLabelColor(QtGui.QColor("#475569"))
            chart.legend().setFont(QtGui.QFont("Segoe UI", 8))

            view = QChartView(chart)
            view.setRenderHint(QtGui.QPainter.Antialiasing)
            view.setStyleSheet("background: transparent; border: none;")
            view.setMinimumHeight(220)
            layout.addWidget(view)

        except Exception:
            logger.exception("Erreur graphique catégories")

    def _set_var_label(self, label, pct):
        if pct is None:
            label.setText("N-1 : —")
            label.setStyleSheet(
                "color: #94a3b8; font-size: 10px; font-weight: 700; "
                "background: transparent;")
            return
        arrow = "▲" if pct >= 0 else "▼"
        color = "#16A34A" if pct >= 0 else "#DC2626"
        label.setText(f"{arrow} {pct:+.1f} % vs N-1")
        label.setStyleSheet(
            f"color: {color}; font-size: 10px; font-weight: 700; "
            f"background: transparent;")

    # ══════════════════════════════════════════════════════════════
    # ONGLET 2 : ÉQUIPE
    # ══════════════════════════════════════════════════════════════
    def _render_equipe(self):
        """Rendu Équipe — hybride."""
        devise = db.get_config("devise", "FC")

        # ═══ RÉCUPÉRATION ═══
        if is_client_mode() and getattr(self, "_use_api_data", False):
            vendeurs = self._current_data.get("vendeurs", [])
            annul = self._current_data.get("annulations", [])
        else:
            vendeurs = engine.equipe_vendeurs(self._debut, self._fin)
            annul = engine.equipe_annulations(self._debut, self._fin)
            self._current_data["vendeurs"] = vendeurs
            self._current_data["annulations"] = annul

        # ═══ TABLEAU VENDEURS ═══
        self.table_vendeurs.setRowCount(len(vendeurs))
        for i, v in enumerate(vendeurs):
            items = [
                v.get("nom", "—"),
                str(v.get("n_ventes", 0)),
                f"{v.get('ca', 0):,.0f} {devise}".replace(",", " "),
                f"{v.get('panier', 0):,.0f} {devise}".replace(",", " "),
                str(v.get("n_clients", 0)),
                f"{v.get('part', 0):.1f} %",
            ]
            for j, val in enumerate(items):
                it = QtWidgets.QTableWidgetItem(str(val))
                if j == 0:
                    it.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                if j >= 1:
                    it.setTextAlignment(Qt.AlignCenter)
                self.table_vendeurs.setItem(i, j, it)

        h = self.table_vendeurs.horizontalHeader()
        h.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for j in (1, 2, 3, 4, 5):
            h.setSectionResizeMode(j, QtWidgets.QHeaderView.ResizeToContents)

        # ═══ TABLEAU ANNULATIONS ═══
        self.table_annulations.setRowCount(len(annul))
        for i, v in enumerate(annul):
            items = [
                v.get("nom", "—"),
                str(v.get("n_total", 0)),
                str(v.get("n_annul", 0)),
                f"{v.get('taux', 0):.2f} %",
                "ALERTE" if v.get("alerte") else "OK",
            ]
            for j, val in enumerate(items):
                it = QtWidgets.QTableWidgetItem(str(val))
                it.setTextAlignment(Qt.AlignCenter)
                if v.get("alerte"):
                    if j == 3:
                        it.setForeground(QtGui.QColor("#b91c1c"))
                        it.setFont(
                            QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                    elif j == 4:
                        it.setForeground(QtGui.QColor("#b91c1c"))
                        it.setBackground(QtGui.QColor("#fee2e2"))
                        it.setFont(
                            QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                elif j == 4:
                    it.setForeground(QtGui.QColor("#15803d"))
                    it.setBackground(QtGui.QColor("#dcfce7"))
                self.table_annulations.setItem(i, j, it)

        h = self.table_annulations.horizontalHeader()
        for j in range(5):
            h.setSectionResizeMode(j, QtWidgets.QHeaderView.Stretch)

    # ══════════════════════════════════════════════════════════════
    # ONGLET 3 : OPÉRATIONS
    # ══════════════════════════════════════════════════════════════
    def _render_operations(self):
        """Rendu Opérations — hybride."""
        devise = db.get_config("devise", "FC")

        # ═══ RÉCUPÉRATION ═══
        if is_client_mode() and getattr(self, "_use_api_data", False):
            marges = self._current_data.get("marges", [])
            stock = self._current_data.get("stock", {})
            ops = self._current_data.get("operations", {})
        else:
            marges = engine.marges(self._debut, self._fin)
            stock = engine.stock_et_blf(self._debut, self._fin)
            ops = engine.operations_resume(self._debut, self._fin)
            self._current_data["marges"] = marges
            self._current_data["stock"] = stock
            self._current_data["operations"] = ops

        # ═══ KPIs MARGES ═══
        total_ca = sum(m.get("ca", 0) for m in marges)
        total_marge = sum(m.get("marge", 0) for m in marges)
        taux = (total_marge / total_ca * 100) if total_ca else 0

        self.kpi_marge_value.setText(
            f"{total_marge:,.0f} {devise}".replace(",", " "))
        self.kpi_marge_pct_value.setText(f"{taux:.1f} %")

        # ═══ KPIs STOCK ═══
        valeur = float(stock.get("stock", {}).get("valeur", 0))
        self.kpi_stock_val_value.setText(
            f"{valeur:,.0f} {devise}".replace(",", " "))
        self.kpi_rupture_value.setText(str(stock.get("rupture", 0)))

        # ═══ TOP MARGES ═══
        top = sorted(marges, key=lambda x: -x.get("marge", 0))[:self._topn]
        self.table_top_marge.setRowCount(len(top))
        for i, m in enumerate(top):
            items = [
                m.get("nom", "—"),
                str(int(m.get("qte", 0))),
                f"{m.get('ca', 0):,.0f}".replace(",", " "),
                f"{m.get('cout', 0):,.0f}".replace(",", " "),
                f"{m.get('marge', 0):,.0f}".replace(",", " "),
                f"{m.get('marge_pct', 0):.1f} %",
            ]
            for j, v in enumerate(items):
                it = QtWidgets.QTableWidgetItem(str(v))
                if j == 0:
                    it.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                if j >= 1:
                    it.setTextAlignment(Qt.AlignCenter)
                if j == 4:
                    it.setForeground(
                        QtGui.QColor("#16A34A" if m.get("marge", 0) > 0
                                     else "#DC2626"))
                    it.setFont(
                        QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
                self.table_top_marge.setItem(i, j, it)

        h = self.table_top_marge.horizontalHeader()
        h.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for j in (1, 2, 3, 4, 5):
            h.setSectionResizeMode(j, QtWidgets.QHeaderView.ResizeToContents)

        # ═══ RUPTURE ═══
        low = stock.get("low_stock", [])
        self.table_rupture.setRowCount(len(low))
        for i, p in enumerate(low):
            code = QtWidgets.QTableWidgetItem(p.get("Code_reference", ""))
            code.setFont(QtGui.QFont("Courier New", 9))
            code.setForeground(QtGui.QColor("#94a3b8"))
            self.table_rupture.setItem(i, 0, code)

            nom = QtWidgets.QTableWidgetItem(p.get("Nom", "—"))
            nom.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            self.table_rupture.setItem(i, 1, nom)

            qte = int(p.get("Quantite", 0))
            q_item = QtWidgets.QTableWidgetItem(str(qte))
            q_item.setTextAlignment(Qt.AlignCenter)
            q_item.setForeground(QtGui.QColor(
                "#DC2626" if qte <= 5 else "#F4A261" if qte <= 20
                else "#16A34A"))
            q_item.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            self.table_rupture.setItem(i, 2, q_item)

        h = self.table_rupture.horizontalHeader()
        h.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        h.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        # ═══ RÉSUMÉ OPÉRATIONNEL ═══
        blfs = stock.get("blf", [])
        blfs_txt = ", ".join(
            f"{b.get('statut', '?')}: {b.get('n', 0)}"
            for b in blfs) or "aucun"

        ajust = ops.get("ajustements", {})
        if isinstance(ajust, dict):
            n_ajust = ajust.get("n", 0)
            q_ajust = ajust.get("qte", 0)
        else:
            n_ajust = 0
            q_ajust = 0

        txt = (
            f"Ventes annulées : <b>{ops.get('ventes_annulees', 0)}</b><br>"
            f"Ajustements de stock : <b>{n_ajust}</b> "
            f"({q_ajust} unités)<br>"
            f"BLF annulés : <b>{ops.get('blf_annules', 0)}</b><br>"
            f"BLF de la période : {blfs_txt}"
        )
        self.lbl_ops_text.setText(txt)

    # ══════════════════════════════════════════════════════════════
    # EXPORTS
    # ══════════════════════════════════════════════════════════════
    def _on_export_success(self, path):
        QtWidgets.QMessageBox.information(
            self, "Export réussi", f"Fichier enregistré :\n{path}")
        audit.log(audit.ACTION_EXPORT_RAPPORT,
                  utilisateur_id=self.user_id,
                  cible_type="rapport",
                  cible_nom=os.path.basename(path),
                  details={"periode": f"{self._debut} → {self._fin}"})

    def _export_csv(self):
        if not self._debut:
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export CSV",
            f"rapport_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            "CSV (*.csv)")
        if not path:
            return
        try:
            devise = db.get_config("devise", "FC")
            headers = ["Section", "Élément", "Valeur 1", "Valeur 2", "Valeur 3"]
            rows = []
            for i, t in enumerate(self._current_data.get("top_produits", [])):
                rows.append(["Top produits", t["nom"], int(t["qte"]),
                             f"{t['ca']:.0f}", t["categorie"]])
            for v in self._current_data.get("vendeurs", []):
                rows.append(["Vendeur", v["nom"], v["n_ventes"],
                             f"{v['ca']:.0f}", v["part"]])
            for m in self._current_data.get("marges", [])[:20]:
                rows.append(["Marge", m["nom"], int(m["qte"]),
                             f"{m['marge']:.0f}", f"{m['marge_pct']:.1f}"])
            ok = export.export_csv(path, headers, rows)
            if ok:
                self._on_export_success(path)
        except Exception as e:
            logger.exception("Erreur export CSV")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _export_excel(self):
        if not self._debut:
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Excel",
            f"rapport_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            "Excel (*.xlsx)")
        if not path:
            return
        try:
            devise = db.get_config("devise", "FC")
            sheets = {}

            kpi = self._current_data.get("ventes_kpi", {})
            sheets["Ventes KPI"] = {
                "headers": ["Indicateur", "Valeur"],
                "rows": [
                    ["CA total", f"{kpi.get('ca_total', 0):.0f} {devise}"],
                    ["Nombre de ventes", kpi.get("nb_ventes", 0)],
                    ["Panier moyen", f"{kpi.get('panier_moyen', 0):.0f} {devise}"],
                    ["Clients servis", kpi.get("nb_clients", 0)],
                    ["Articles vendus", kpi.get("nb_articles", 0)],
                ]}

            top = self._current_data.get("top_produits", [])
            sheets["Top produits"] = {
                "headers": ["Produit", "Catégorie", "Qté", "CA"],
                "rows": [[t["nom"], t["categorie"], int(t["qte"]), t["ca"]]
                         for t in top]}

            vendeurs = self._current_data.get("vendeurs", [])
            sheets["Équipe"] = {
                "headers": ["Vendeur", "Ventes", "CA", "Panier", "Clients", "Part %"],
                "rows": [[v["nom"], v["n_ventes"], v["ca"], v["panier"],
                          v["n_clients"], round(v["part"], 2)]
                         for v in vendeurs]}

            marges = self._current_data.get("marges", [])
            sheets["Marges"] = {
                "headers": ["Produit", "Qté", "CA", "Coût", "Marge", "Taux %"],
                "rows": [[m["nom"], int(m["qte"]), m["ca"], m["cout"],
                          m["marge"], round(m["marge_pct"], 2)]
                         for m in marges]}

            ok = export.export_excel(path, sheets)
            if ok:
                self._on_export_success(path)
        except Exception as e:
            logger.exception("Erreur export Excel")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _export_pdf(self):
        if not self._debut:
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export PDF",
            f"rapport_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            "PDF (*.pdf)")
        if not path:
            return
        try:
            devise = db.get_config("devise", "FC")
            kpi = self._current_data.get("ventes_kpi", {})

            def f(v):
                return f"{v:,.0f} {devise}".replace(",", " ")

            sections = [
                {"titre": "Indicateurs clés", "type": "kpis", "data": [
                    ("Chiffre d'affaires", f(kpi.get("ca_total", 0))),
                    ("Nombre de ventes", kpi.get("nb_ventes", 0)),
                    ("Panier moyen", f(kpi.get("panier_moyen", 0))),
                    ("Clients servis", kpi.get("nb_clients", 0)),
                    ("Articles vendus", kpi.get("nb_articles", 0)),
                ]},
                {"titre": f"Top {self._topn} produits", "type": "table",
                 "headers": ["Produit", "Catégorie", "Qté", "CA"],
                 "rows": [
                     [t["nom"], t.get("categorie", "—"),
                      int(t["qte"]), f(t["ca"])]
                     for t in self._current_data.get("top_produits", [])
                 ],
                 "col_widths": [7 * cm, 3.5 * cm, 2 * cm, 4 * cm]},
                {"titre": "Performance équipe", "type": "table",
                 "headers": ["Vendeur", "Ventes", "CA", "Part %"],
                 "rows": [
                     [v["nom"], v["n_ventes"], f(v["ca"]),
                      f"{v['part']:.1f}"]
                     for v in self._current_data.get("vendeurs", [])
                 ],
                 "col_widths": [7 * cm, 2.5 * cm, 4 * cm, 2.5 * cm]},
            ]

            from Database import rapport_export
            nom_ent = db.get_config("nom_entreprise", "NOVA PHARMA")
            ok = rapport_export.export_pdf(
                path, "Rapport d'activité",
                f"Période : {self._debut[:10]} → {self._fin[:10]}",
                sections, nom_entreprise=nom_ent)

            if ok:
                self._on_export_success(path)

                # ─── Impression auto (si activé) ───
                try:
                    auto = bool(db.get_config(
                        "printer_auto_print_report", False))
                    if auto:
                        printer_manager.print_pdf_silent(path, kind="report")
                        logger.info("Rapport PDF envoyé à l'imprimante A4")
                except Exception:
                    logger.exception("Erreur impression rapport")
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Erreur", "Impossible de générer le PDF.")
        except Exception as e:
            logger.exception("Erreur export PDF")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))
            
    # ══════════════════════════════════════════════════════════════
    # Scroll dans chaque onglet
    # ══════════════════════════════════════════════════════════════
    def _setup_scroll_areas(self) -> None:
        """Wrap le contenu de chaque onglet dans un QScrollArea."""
        for i in range(self.tabs.count()):
            tab_widget = self.tabs.widget(i)
            if tab_widget is None:
                continue
            try:
                self._wrap_widget_in_scroll(tab_widget)
            except Exception:
                logger.exception(
                    "Impossible d'ajouter un scroll à l'onglet %d", i)

    def _wrap_widget_in_scroll(self, widget: QtWidgets.QWidget) -> None:
        """
        Remplace le contenu d'un widget par :
            widget → QVBoxLayout(0 margin)
                        └── QScrollArea
                                └── container (avec l'ancien contenu)
        """
        old_layout = widget.layout()
        if old_layout is None:
            return

        # ─── Récupère les items AVANT de les déplacer ───
        items = []
        while old_layout.count():
            items.append(old_layout.takeAt(0))

        # Sauvegarde les propriétés de l'ancien layout
        m = old_layout.contentsMargins()
        spacing = old_layout.spacing()

        # ─── Container avec l'ancien contenu ───
        container = QtWidgets.QWidget()
        container.setStyleSheet("background: transparent;")
        inner = QtWidgets.QVBoxLayout(container)
        inner.setContentsMargins(m.left(), m.top(), m.right(), m.bottom())
        inner.setSpacing(spacing)

        for item in items:
            if item is None:
                continue
            if item.widget():
                inner.addWidget(item.widget())
            elif item.layout():
                inner.addLayout(item.layout())
            elif item.spacerItem():
                inner.addItem(item)

        # ─── QScrollArea ───
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 10px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                min-height: 32px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: transparent;
                border: none;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
        """)
        scroll.setWidget(container)

        # ─── Nouveau layout du widget original ───
        # On efface l'ancien layout en le "détachant"
        QtWidgets.QWidget().setLayout(old_layout)

        new_layout = QtWidgets.QVBoxLayout(widget)
        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(0)
        new_layout.addWidget(scroll)
    
    # ══════════════════════════════════════════════════════════════
    def _clean_layout_keep_title(self, layout, title_object_name: str) -> None:
        """
        Supprime TOUS les widgets d'un layout SAUF celui dont
        l'objectName est `title_object_name`.

        Détruit proprement les widgets : setParent(None) + deleteLater().
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item is None:
                continue
            w = item.widget()
            if w is None:
                continue
            # Garde le titre
            if w.objectName() == title_object_name:
                continue
            layout.removeWidget(w)
            w.setParent(None)
            w.deleteLater()
            # Force la suppression immédiate pour éviter l'accumulation
            w.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)