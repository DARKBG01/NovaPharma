#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
charts.py — Module de graphiques Nova Pharma
=============================================
Contient :
  - ChartData         : extraction de données SQL/Python
  - ChartCard         : widget carte (titre + chart)
  - 12 générateurs de graphiques

Chartes disponibles :
  1.  Flux de revenus (ligne - N jours)
  2.  CA par mois (bar - 12 mois)
  3.  CA par heure (bar - 24h)
  4.  Ventes par jour (ligne - 30 jours)
  5.  Top médicaments par quantité (bar horizontal)
  6.  Top médicaments par CA (bar horizontal)
  7.  Répartition par catégorie (donut)
  8.  Top clients par CA (bar horizontal)
  9.  Nouveaux clients par mois (ligne)
  10. Anonymes vs identifiés (donut)
  11. Produits en rupture de stock (bar horizontal)
  12. Comparaison année N vs N-1 (ligne double)
"""

import logging
from datetime import datetime, timedelta
from collections import defaultdict

from PySide6.QtCharts import (
    QChart, QChartView, QLineSeries, QPieSlice, QSplineSeries, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis, QPieSeries, QHorizontalBarSeries,
    QCategoryAxis, QStackedBarSeries,
)
from PySide6.QtCore import Qt, QMargins, QPointF, QSize
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QLinearGradient, QIcon, QPixmap,
)
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QSizePolicy,
    QPushButton, QGridLayout,
)

from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Palette
# ══════════════════════════════════════════════════════════════════
PRIMARY_COLOR   = "#0077B6"
SECONDARY_COLOR = "#00B4D8"
DARK_COLOR      = "#023E8A"
LIGHT_COLOR     = "#90E0EF"
SUCCESS_COLOR   = "#16A34A"
DANGER_COLOR    = "#DC2626"
WARNING_COLOR   = "#F4A261"
PURPLE_COLOR    = "#7c3aed"

CHART_PALETTE = [
    "#0077B6", "#00B4D8", "#023E8A", "#90E0EF",
    "#F4A261", "#16A34A", "#7c3aed", "#dc2626",
    "#0891b2", "#059669", "#d97706", "#9333ea",
]

GRID_COLOR      = "#e2e8f0"
TEXT_COLOR      = "#334155"
MUTED_COLOR     = "#94a3b8"

MOIS_FR = {
    1: "Jan", 2: "Fév", 3: "Mar", 4: "Avr", 5: "Mai", 6: "Juin",
    7: "Juil", 8: "Août", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Déc",
}

JOURS_FR = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]


# ══════════════════════════════════════════════════════════════════
# Extraction des données
# ══════════════════════════════════════════════════════════════════
class ChartData:
    """Extraction et agrégation des données pour les graphiques."""

    @staticmethod
    def _parse_date(date_str):
        """Parse une date au format DD/MM/YYYY [HH:MM:SS]."""
        try:
            parts = str(date_str).strip().split(" ")
            d, m, y = parts[0].split("/")
            h, mi, s = (0, 0, 0)
            if len(parts) > 1:
                hms = parts[1].split(":")
                h = int(hms[0]) if len(hms) > 0 else 0
                mi = int(hms[1]) if len(hms) > 1 else 0
                s = int(hms[2]) if len(hms) > 2 else 0
            return datetime(int(y), int(m), int(d), h, mi, s)
        except Exception:
            return None

    @staticmethod
    def _load_historique():
        """Charge tout l'historique des ventes (une seule fois)."""
        try:
            rows = db.query("SELECT * FROM Historique ORDER BY Id ASC")
            data = []
            for r in rows:
                dt = ChartData._parse_date(r["Date_vent"])
                if dt is None:
                    continue
                data.append({
                    "date": dt,
                    "total": float(r["Total"] or 0),
                    "quantite": int(r["Quantite"] or 0),
                    "article": str(r["Article"] or ""),
                    "num_fact": str(r["Num_fact"] or ""),
                    "client_name": str(r["Client_name"] or ""),
                })
            return data
        except Exception:
            logger.exception("Erreur chargement historique")
            return []

    # ─── 1. CA par jour (N derniers jours) ───
    @staticmethod
    def get_revenue_by_day(days: int = 7):
        """Retourne (labels, ca_list, ventes_list)."""
        data = ChartData._load_historique()
        today = datetime.now().date()
        start = today - timedelta(days=days - 1)

        daily_ca = defaultdict(float)
        daily_fact = defaultdict(set)

        for r in data:
            d = r["date"].date()
            if start <= d <= today:
                key = d.isoformat()
                daily_ca[key] += r["total"]
                daily_fact[key].add(r["num_fact"])

        labels, ca, ventes = [], [], []
        for i in range(days):
            d = start + timedelta(days=i)
            key = d.isoformat()
            labels.append(d.strftime("%d/%m"))
            ca.append(daily_ca.get(key, 0.0))
            ventes.append(len(daily_fact.get(key, set())))
        return labels, ca, ventes

    # ─── 2. CA par mois (N derniers mois) ───
    @staticmethod
    def get_revenue_by_month(months: int = 12):
        """Retourne (labels, ca_list)."""
        data = ChartData._load_historique()
        now = datetime.now()
        start = (now.replace(day=1) - timedelta(days=30 * (months - 1))).replace(day=1)

        monthly_ca = defaultdict(float)
        for r in data:
            d = r["date"]
            if d >= start:
                key = f"{d.year}-{d.month:02d}"
                monthly_ca[key] += r["total"]

        labels, ca = [], []
        cur = start
        for _ in range(months):
            key = f"{cur.year}-{cur.month:02d}"
            labels.append(f"{MOIS_FR[cur.month]} {cur.year % 100:02d}")
            ca.append(monthly_ca.get(key, 0.0))
            # Mois suivant
            if cur.month == 12:
                cur = cur.replace(year=cur.year + 1, month=1)
            else:
                cur = cur.replace(month=cur.month + 1)
        return labels, ca

    # ─── 3. CA par heure (24h) ───
    @staticmethod
    def get_revenue_by_hour():
        """Retourne (labels, ca_list)."""
        data = ChartData._load_historique()
        hourly = defaultdict(float)
        for r in data:
            hourly[r["date"].hour] += r["total"]

        labels = [f"{h:02d}h" for h in range(24)]
        ca = [hourly.get(h, 0.0) for h in range(24)]
        return labels, ca

    # ─── 4. Ventes par jour (30 derniers jours) ───
    @staticmethod
    def get_sales_count_by_day(days: int = 30):
        """Retourne (labels, count_list)."""
        data = ChartData._load_historique()
        today = datetime.now().date()
        start = today - timedelta(days=days - 1)

        daily_fact = defaultdict(set)
        for r in data:
            d = r["date"].date()
            if start <= d <= today:
                daily_fact[d.isoformat()].add(r["num_fact"])

        labels, counts = [], []
        for i in range(days):
            d = start + timedelta(days=i)
            labels.append(d.strftime("%d/%m"))
            counts.append(len(daily_fact.get(d.isoformat(), set())))
        return labels, counts

    # ─── 5/6. Top produits (par quantité OU CA) ───
    @staticmethod
    def get_top_products(limit: int = 10, mode: str = "quantity"):
        """mode = 'quantity' ou 'revenue'."""
        data = ChartData._load_historique()
        agg = defaultdict(lambda: {"qte": 0, "ca": 0.0})

        for r in data:
            art = r["article"]
            agg[art]["qte"] += r["quantite"]
            agg[art]["ca"] += r["total"]

        if mode == "revenue":
            sorted_items = sorted(agg.items(), key=lambda x: x[1]["ca"], reverse=True)
            return (
                [k for k, _ in sorted_items[:limit]],
                [v["ca"] for _, v in sorted_items[:limit]]
            )
        else:
            sorted_items = sorted(agg.items(), key=lambda x: x[1]["qte"], reverse=True)
            return (
                [k for k, _ in sorted_items[:limit]],
                [v["qte"] for _, v in sorted_items[:limit]]
            )

    # ─── 7. Répartition par catégorie ───
    @staticmethod
    def get_sales_by_category():
        """Retourne dict {categorie: ca_total}."""
        try:
            rows = db.query("""
                SELECT p.Categorie AS cat, SUM(h.Total) AS ca
                FROM Historique h
                LEFT JOIN produits p ON p.Code_reference = h.Code_reference
                GROUP BY p.Categorie
                ORDER BY ca DESC
            """)
            result = {}
            for r in rows:
                cat = r["cat"] or "Non classé"
                result[cat] = float(r["ca"] or 0)
            return result
        except Exception:
            logger.exception("Erreur répartition catégories")
            return {}

    # ─── 8. Top clients ───
    @staticmethod
    def get_top_clients(limit: int = 10):
        """Top clients par montant total acheté."""
        try:
            rows = db.query("""
                SELECT COALESCE(C_name, nom) AS nom,
                       COALESCE(Montant_total, 0) AS total
                FROM Client
                WHERE actif = 1
                ORDER BY total DESC
                LIMIT ?
            """, (limit,))
            return (
                [r["nom"] or "—" for r in rows],
                [float(r["total"] or 0) for r in rows]
            )
        except Exception:
            logger.exception("Erreur top clients")
            return [], []

    # ─── 9. Nouveaux clients par mois ───
    @staticmethod
    def get_new_clients_by_month(months: int = 6):
        """Retourne (labels, count)."""
        try:
            rows = db.query(
                "SELECT created_at FROM Client WHERE created_at IS NOT NULL")
        except Exception:
            return [], []

        now = datetime.now()
        start = (now.replace(day=1) - timedelta(days=30 * (months - 1))).replace(day=1)

        monthly = defaultdict(int)
        for r in rows:
            try:
                dt = datetime.fromisoformat(str(r["created_at"]).split(" ")[0])
                if dt >= start:
                    key = f"{dt.year}-{dt.month:02d}"
                    monthly[key] += 1
            except Exception:
                continue

        labels, counts = [], []
        cur = start
        for _ in range(months):
            key = f"{cur.year}-{cur.month:02d}"
            labels.append(f"{MOIS_FR[cur.month]} {cur.year % 100:02d}")
            counts.append(monthly.get(key, 0))
            if cur.month == 12:
                cur = cur.replace(year=cur.year + 1, month=1)
            else:
                cur = cur.replace(month=cur.month + 1)
        return labels, counts

    # ─── 10. Anonymes vs identifiés ───
    @staticmethod
    def get_anonyme_split():
        """Retourne dict {'Identifiés': count, 'Anonymes': count}."""
        try:
            total = db.query_one(
                "SELECT COUNT(DISTINCT Num_fact) AS n FROM Historique")["n"]
            anonymes = db.query_one(
                """SELECT COUNT(DISTINCT Num_fact) AS n FROM Historique
                   WHERE Client_name LIKE 'Client anonyme%'""")["n"]
            total = int(total or 0)
            anonymes = int(anonymes or 0)
            return {
                "Identifiés": max(0, total - anonymes),
                "Anonymes": anonymes,
            }
        except Exception:
            logger.exception("Erreur split anonymes")
            return {"Identifiés": 0, "Anonymes": 0}

    # ─── 11. Produits en rupture ───
    @staticmethod
    def get_low_stock_products(limit: int = 10):
        """Produits avec stock <= 20, triés par quantité croissante."""
        try:
            rows = db.query("""
                SELECT Nom, Quantite FROM produits
                WHERE actif = 1 AND Quantite <= 20
                ORDER BY Quantite ASC
                LIMIT ?
            """, (limit,))
            return (
                [r["Nom"] for r in rows],
                [int(r["Quantite"] or 0) for r in rows]
            )
        except Exception:
            logger.exception("Erreur produits rupture")
            return [], []

    # ─── 12. Comparaison N vs N-1 ───
    @staticmethod
    def get_year_comparison():
        """CA mensuel de l'année courante vs précédente."""
        data = ChartData._load_historique()
        now = datetime.now()
        cur_year = now.year
        prev_year = cur_year - 1

        cur_monthly = defaultdict(float)
        prev_monthly = defaultdict(float)
        for r in data:
            y = r["date"].year
            m = r["date"].month
            if y == cur_year:
                cur_monthly[m] += r["total"]
            elif y == prev_year:
                prev_monthly[m] += r["total"]

        labels = [MOIS_FR[m] for m in range(1, 13)]
        cur_data = [cur_monthly.get(m, 0.0) for m in range(1, 13)]
        prev_data = [prev_monthly.get(m, 0.0) for m in range(1, 13)]
        return labels, cur_data, prev_data, cur_year, prev_year


# ══════════════════════════════════════════════════════════════════
# Style global des charts
# ══════════════════════════════════════════════════════════════════
def _base_chart(title: str = "") -> QChart:
    """Retourne un QChart avec le style Nova Pharma de base."""
    chart = QChart()
    chart.setTitle("")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.setBackgroundRoundness(0)
    chart.setBackgroundBrush(QBrush(QColor("#ffffff")))
    chart.setPlotAreaBackgroundVisible(False)
    chart.setMargins(QMargins(8, 8, 8, 8))
    chart.legend().setVisible(False)
    chart.legend().setAlignment(Qt.AlignBottom)
    chart.legend().setLabelColor(QColor(TEXT_COLOR))
    chart.legend().setFont(QFont("Segoe UI", 9))

    # Cache le titre interne (le ChartCard a son propre titre)
    chart.setTitleBrush(QBrush(QColor(TEXT_COLOR)))
    return chart


def _style_axis_value(axis: QValueAxis, label_format: str = ""):
    """Applique le style à un axe de valeurs."""
    axis.setLabelsColor(QColor(TEXT_COLOR))
    axis.setLabelsFont(QFont("Segoe UI", 8))
    axis.setGridLineColor(QColor(GRID_COLOR))
    axis.setLinePenColor(QColor(GRID_COLOR))
    if label_format:
        axis.setLabelFormat(label_format)


def _style_axis_category(axis: QBarCategoryAxis):
    """Applique le style à un axe de catégories."""
    axis.setLabelsColor(QColor(TEXT_COLOR))
    axis.setLabelsFont(QFont("Segoe UI", 8))
    axis.setGridLineVisible(False)
    axis.setLinePenColor(QColor(GRID_COLOR))


def _make_chart_view(chart: QChart) -> QChartView:
    """Crée un QChartView avec antialiasing."""
    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)
    view.setStyleSheet("background: transparent; border: none;")
    return view


# ══════════════════════════════════════════════════════════════════
# ChartCard — Carte avec titre + chart
# ══════════════════════════════════════════════════════════════════
class ChartCard(QFrame):
    """Carte contenant un graphique avec titre."""

    def __init__(self, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("chart_card")
        self.setStyleSheet("""
            QFrame#chart_card {
                background-color: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 18px;
            }
        """)
        self.setMinimumHeight(320)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        # Titre
        title_row = QHBoxLayout()
        title_row.setSpacing(8)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(
            "color: #0f172a; font-size: 14px; font-weight: 800; "
            "background: transparent;")
        title_row.addWidget(lbl_title)

        if subtitle:
            lbl_sub = QLabel(f"—  {subtitle}")
            lbl_sub.setStyleSheet(
                "color: #94a3b8; font-size: 11px; font-weight: 600; "
                "background: transparent;")
            title_row.addWidget(lbl_sub)

        title_row.addStretch()
        layout.addLayout(title_row)

        # Conteneur pour le chart
        self.chart_container = QVBoxLayout()
        self.chart_container.setContentsMargins(0, 4, 0, 0)
        layout.addLayout(self.chart_container, 1)

        self._chart_view = None

    def set_chart(self, chart: QChart):
        """Remplace le graphique contenu."""
        # Retire l'ancien
        if self._chart_view is not None:
            self.chart_container.removeWidget(self._chart_view)
            self._chart_view.deleteLater()

        self._chart_view = _make_chart_view(chart)
        self.chart_container.addWidget(self._chart_view)

    def set_empty(self, message: str = "Aucune donnée disponible"):
        """Affiche un message vide."""
        lbl = QLabel(message)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(
            "color: #94a3b8; font-size: 13px; font-style: italic; "
            "background: transparent; padding: 40px;")
        # Retire l'ancien
        if self._chart_view is not None:
            self.chart_container.removeWidget(self._chart_view)
            self._chart_view.deleteLater()
            self._chart_view = None
        self.chart_container.addWidget(lbl)

    # ─── Localisation : après la classe ChartCard, AVANT chart_revenue_line ───



# ══════════════════════════════════════════════════════════════════
# Placeholder mode client (fonction module-level)
# ══════════════════════════════════════════════════════════════════
def _make_client_placeholder(title: str, sub: str = "") -> ChartCard:
    """Carte placeholder pour mode client (pas de graphiques locaux)."""
    card = ChartCard(title, sub)
    card.setMinimumHeight(260)
    card.setStyleSheet("""
        QFrame {
            background: #ffffff;
            border: 1px solid #e6ebf2;
            border-radius: 18px;
        }
    """)

    # ─── Conteneur interne ───
    container = QWidget()
    container.setStyleSheet("background: transparent;")
    v = QVBoxLayout(container)
    v.setContentsMargins(20, 20, 20, 20)
    v.setSpacing(12)
    v.setAlignment(Qt.AlignCenter)

    # ─── Icône (fallback sur plusieurs noms) ───
    icon = QLabel()
    icon.setFixedSize(56, 56)
    icon.setAlignment(Qt.AlignCenter)
    icon.setStyleSheet("""
        QLabel {
            background: #eff6ff;
            border: 1px solid #dbeafe;
            border-radius: 14px;
            padding: 14px;
        }
    """)
    for icon_name in ("chart-pie", "chart-line", "activity", "info"):
        pix = QPixmap(f":/Icon/Icons/{icon_name}.svg")
        if not pix.isNull():
            icon.setPixmap(pix.scaled(
                28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            break
    v.addWidget(icon, alignment=Qt.AlignCenter)

    # ─── Message ───
    msg = QLabel(
        "Les graphiques détaillés\n"
        "sont disponibles dans la page Rapports.")
    msg.setAlignment(Qt.AlignCenter)
    msg.setStyleSheet(
        "color: #64748b; font-size: 12px; font-weight: 600; "
        "background: transparent; line-height: 1.5;")
    v.addWidget(msg)

    # ─── Bouton ───
    btn = QPushButton("  Voir les rapports")
    btn.setCursor(Qt.PointingHandCursor)
    btn.setMinimumHeight(36)
    btn.setStyleSheet("""
        QPushButton {
            background: #0077B6;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 8px 20px;
            font-size: 12px;
            font-weight: 700;
        }
        QPushButton:hover { background: #023E8A; }
    """)

    def _go_to_reports():
        try:
            w = card.parent()
            while w is not None:
                if hasattr(w, "_goto_name"):
                    w._goto_name("btn_onglet_rapport")
                    return
                w = w.parent()
        except Exception:
            logger.exception("Erreur navigation vers Rapports")

    btn.clicked.connect(_go_to_reports)
    v.addWidget(btn, alignment=Qt.AlignCenter)

    # ─── Ajout au ChartCard ───
    card.chart_container.addWidget(container)
    return card


# ══════════════════════════════════════════════════════════════════
# Générateurs de graphiques
# ══════════════════════════════════════════════════════════════════

# ─── 1. Flux de revenus (ligne) ───
def chart_revenue_line(days: int = 7, data: dict = None) -> QChart:
    # ─── Données : API (data) ou DB (ChartData) ───
    if data is not None:
        labels = data.get("labels", [])
        ca = data.get("ca", [])
    else:
        labels, ca, _ = ChartData.get_revenue_by_day(days)

    chart = _base_chart("Revenus")
    if not ca or sum(ca) == 0:
        return chart

    series = QSplineSeries()
    series.setName("CA (FC)")
    pen = QPen(QColor(PRIMARY_COLOR))
    pen.setWidth(3)
    series.setPen(pen)

    max_val = max(ca) if ca else 0
    for i, v in enumerate(ca):
        series.append(i, v)

    chart.addSeries(series)

    axis_x = QBarCategoryAxis()
    axis_x.append(labels)
    _style_axis_category(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setRange(0, max_val * 1.15 if max_val > 0 else 10)
    axis_y.setLabelFormat("%.0f")
    _style_axis_value(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    # Gradient sous la courbe
    gradient = QLinearGradient(0, 0, 0, 1)
    gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
    gradient.setColorAt(0.0, QColor(0, 119, 182, 100))
    gradient.setColorAt(1.0, QColor(0, 119, 182, 0))
    series.setBrush(QBrush(gradient))

    return chart


# ─── 2. CA par mois (bar) ───
def chart_revenue_monthly(months: int = 12, data: dict = None) -> QChart:
    if data is not None:
        labels = data.get("labels", [])
        ca = data.get("ca", [])
    else:
        labels, ca = ChartData.get_revenue_by_month(months)

    chart = _base_chart("CA mensuel")
    if not ca or sum(ca) == 0:
        return chart

    bar_set = QBarSet("CA")
    bar_set.setColor(QColor(PRIMARY_COLOR))
    bar_set.append(ca)

    series = QBarSeries()
    series.append(bar_set)
    series.setBarWidth(0.7)
    chart.addSeries(series)

    axis_x = QBarCategoryAxis()
    axis_x.append(labels)
    _style_axis_category(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setRange(0, max(ca) * 1.15 if max(ca) > 0 else 10)
    axis_y.setLabelFormat("%.0f")
    _style_axis_value(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    return chart


# ─── 3. CA par heure (bar) ───
def chart_revenue_hourly() -> QChart:
    labels, ca = ChartData.get_revenue_by_hour()

    chart = _base_chart("CA par heure")
    if not ca or sum(ca) == 0:
        return chart

    bar_set = QBarSet("CA")
    bar_set.setColor(QColor(SECONDARY_COLOR))
    bar_set.append(ca)

    series = QBarSeries()
    series.append(bar_set)
    series.setBarWidth(0.8)
    chart.addSeries(series)

    axis_x = QBarCategoryAxis()
    axis_x.append(labels)
    _style_axis_category(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setRange(0, max(ca) * 1.15 if max(ca) > 0 else 10)
    axis_y.setLabelFormat("%.0f")
    _style_axis_value(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    return chart


# ─── 4. Ventes par jour (ligne) ───
def chart_sales_count_line(days: int = 30) -> QChart:
    labels, counts = ChartData.get_sales_count_by_day(days)

    chart = _base_chart("Nombre de ventes")
    if not counts or sum(counts) == 0:
        return chart

    series = QLineSeries()
    series.setName("Ventes")
    pen = QPen(QColor(SUCCESS_COLOR))
    pen.setWidth(2.5)
    series.setPen(pen)

    for i, v in enumerate(counts):
        series.append(i, v)

    chart.addSeries(series)

    axis_x = QBarCategoryAxis()
    axis_x.append(labels)
    _style_axis_category(axis_x)
    # Réduit les labels (affiche un sur 3)
    if len(labels) > 15:
        for i in range(len(labels)):
            if i % 3 != 0:
                axis_x.setLabelsVisible(False) if i > 0 else None
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setRange(0, max(counts) * 1.15 if max(counts) > 0 else 10)
    axis_y.setLabelFormat("%d")
    axis_y.setTickCount(min(6, max(counts) + 2))
    _style_axis_value(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    return chart


# ─── 5. Top médicaments (bar horizontal) ───
def chart_top_products(mode: str = "quantity", limit: int = 10,
                       data: list = None) -> QChart:
    if data is not None:
        # data = [{nom, qte, ca}, ...]
        key = "qte" if mode == "quantity" else "ca"
        sorted_items = sorted(
            data, key=lambda x: x.get(key, 0), reverse=True)[:limit]
        labels = [x.get("nom", "—") for x in sorted_items]
        values = [x.get(key, 0) for x in sorted_items]
    else:
        labels, values = ChartData.get_top_products(
            limit=limit, mode=mode)

    chart = _base_chart()
    if not values:
        return chart

    # Inverse pour afficher le top en haut
    labels = labels[::-1]
    values = values[::-1]

    bar_set = QBarSet(
        "Quantité" if mode == "quantity" else "CA (FC)")
    bar_set.setColor(QColor(
        PRIMARY_COLOR if mode == "quantity" else SUCCESS_COLOR))
    bar_set.append(values)

    series = QHorizontalBarSeries()
    series.append(bar_set)
    series.setBarWidth(0.7)
    chart.addSeries(series)

    axis_y = QBarCategoryAxis()
    axis_y.append(labels)
    _style_axis_category(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    axis_x = QValueAxis()
    axis_x.setRange(0, max(values) * 1.15 if max(values) > 0 else 10)
    axis_x.setLabelFormat("%.0f")
    _style_axis_value(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    return chart


# ─── 7. Répartition catégories (donut) ───
def chart_categories_donut(data: list = None) -> QChart:
    if data is not None:
        # data = [{cat, ca}, ...]
        cat_dict = {
            d.get("cat", "—"): float(d.get("ca", 0))
            for d in data if (d.get("ca") or 0) > 0
        }
    else:
        cat_dict = ChartData.get_sales_by_category()

    chart = _base_chart()
    if not cat_dict:
        return chart

    series = QPieSeries()
    series.setHoleSize(0.45)
    series.setPieSize(0.75)

    for i, (cat, ca) in enumerate(cat_dict.items()):
        slice_ = QPieSlice(cat, ca)
        color = QColor(CHART_PALETTE[i % len(CHART_PALETTE)])
        slice_.setBrush(QBrush(color))
        slice_.setPen(QPen(QColor("#ffffff"), 2))
        slice_.setLabelVisible(True)
        slice_.setLabelColor(QColor(TEXT_COLOR))
        slice_.setLabelFont(QFont("Segoe UI", 8, QFont.Bold))
        series.append(slice_)

    chart.addSeries(series)
    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignRight)

    total = sum(cat_dict.values())
    chart.setTitle(f"Total : {total:,.0f} FC".replace(",", " "))
    chart.setTitleFont(QFont("Segoe UI", 10, QFont.Bold))
    chart.setTitleBrush(QBrush(QColor(DARK_COLOR)))

    return chart


# ─── 8. Top clients (bar horizontal) ───
def chart_top_clients(limit: int = 10) -> QChart:
    labels, values = ChartData.get_top_clients(limit=limit)

    chart = _base_chart()
    if not values:
        return chart

    # Inverse
    labels = labels[::-1]
    values = values[::-1]

    bar_set = QBarSet("Total acheté (FC)")
    bar_set.setColor(QColor(PURPLE_COLOR))
    bar_set.append(values)

    series = QHorizontalBarSeries()
    series.append(bar_set)
    series.setBarWidth(0.7)
    chart.addSeries(series)

    axis_y = QBarCategoryAxis()
    # Tronque les noms longs
    short_labels = [
        (lbl[:18] + "…") if len(lbl) > 20 else lbl for lbl in labels
    ]
    axis_y.append(short_labels)
    _style_axis_category(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    axis_x = QValueAxis()
    axis_x.setRange(0, max(values) * 1.15 if max(values) > 0 else 10)
    axis_x.setLabelFormat("%.0f")
    _style_axis_value(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    return chart


# ─── 9. Nouveaux clients par mois (ligne) ───
def chart_new_clients(months: int = 6) -> QChart:
    labels, counts = ChartData.get_new_clients_by_month(months)

    chart = _base_chart()
    if not counts or sum(counts) == 0:
        return chart

    series = QSplineSeries()
    series.setName("Nouveaux clients")
    pen = QPen(QColor(WARNING_COLOR))
    pen.setWidth(3)
    series.setPen(pen)
    series.setPointsVisible(True)

    for i, v in enumerate(counts):
        series.append(i, v)

    chart.addSeries(series)

    axis_x = QBarCategoryAxis()
    axis_x.append(labels)
    _style_axis_category(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setRange(0, max(counts) * 1.2 if max(counts) > 0 else 5)
    axis_y.setLabelFormat("%d")
    _style_axis_value(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    return chart


# ─── 10. Anonymes vs Identifiés (donut) ───
def chart_anonyme_split() -> QChart:
    data = ChartData.get_anonyme_split()

    chart = _base_chart()
    total = sum(data.values())
    if total == 0:
        return chart

    series = QPieSeries()
    series.setHoleSize(0.45)
    series.setPieSize(0.75)

    colors = {
        "Identifiés": SUCCESS_COLOR,
        "Anonymes": WARNING_COLOR,
    }
    for label, val in data.items():
        slice_ = QPieSlice(label, val)
        color = QColor(colors.get(label, PRIMARY_COLOR))
        slice_.setBrush(QBrush(color))
        slice_.setPen(QPen(QColor("#ffffff"), 2))
        slice_.setLabelVisible(True)
        slice_.setLabelColor(QColor(TEXT_COLOR))
        slice_.setLabelFont(QFont("Segoe UI", 9, QFont.Bold))
        series.append(slice_)

    chart.addSeries(series)
    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignRight)

    chart.setTitle(f"Total : {total} factures")
    chart.setTitleFont(QFont("Segoe UI", 10, QFont.Bold))
    chart.setTitleBrush(QBrush(QColor(DARK_COLOR)))

    return chart


# ─── 11. Produits en rupture (bar horizontal) ───
def chart_low_stock(limit: int = 10) -> QChart:
    labels, values = ChartData.get_low_stock_products(limit=limit)

    chart = _base_chart()
    if not values:
        return chart

    labels = labels[::-1]
    values = values[::-1]

    bar_set = QBarSet("Stock")
    bar_set.setColor(QColor(DANGER_COLOR))
    bar_set.append(values)

    series = QHorizontalBarSeries()
    series.append(bar_set)
    series.setBarWidth(0.7)
    chart.addSeries(series)

    axis_y = QBarCategoryAxis()
    short_labels = [
        (lbl[:18] + "…") if len(lbl) > 20 else lbl for lbl in labels
    ]
    axis_y.append(short_labels)
    _style_axis_category(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    axis_x = QValueAxis()
    axis_x.setRange(0, max(values) * 1.3 if max(values) > 0 else 25)
    axis_x.setLabelFormat("%d")
    _style_axis_value(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    return chart


# ─── 12. Comparaison N vs N-1 (ligne double) ───
def chart_year_comparison() -> QChart:
    labels, cur, prev, cur_year, prev_year = ChartData.get_year_comparison()

    chart = _base_chart()
    if sum(cur) == 0 and sum(prev) == 0:
        return chart

    # Année précédente
    s_prev = QLineSeries()
    s_prev.setName(str(prev_year))
    pen_prev = QPen(QColor(MUTED_COLOR))
    pen_prev.setWidth(2)
    pen_prev.setStyle(Qt.DashLine)
    s_prev.setPen(pen_prev)
    for i, v in enumerate(prev):
        s_prev.append(i, v)

    # Année courante
    s_cur = QSplineSeries()
    s_cur.setName(str(cur_year))
    pen_cur = QPen(QColor(PRIMARY_COLOR))
    pen_cur.setWidth(3)
    s_cur.setPen(pen_cur)
    for i, v in enumerate(cur):
        s_cur.append(i, v)

    chart.addSeries(s_prev)
    chart.addSeries(s_cur)

    axis_x = QBarCategoryAxis()
    axis_x.append(labels)
    _style_axis_category(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    s_prev.attachAxis(axis_x)
    s_cur.attachAxis(axis_x)

    max_val = max(max(cur), max(prev)) if (cur or prev) else 0
    axis_y = QValueAxis()
    axis_y.setRange(0, max_val * 1.15 if max_val > 0 else 10)
    axis_y.setLabelFormat("%.0f")
    _style_axis_value(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    s_prev.attachAxis(axis_y)
    s_cur.attachAxis(axis_y)

    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignTop)

    return chart


# ══════════════════════════════════════════════════════════════════
# Header du dashboard (titre + bouton "Voir tous les graphiques")
# ══════════════════════════════════════════════════════════════════
def _make_dashboard_header(main_window) -> QFrame:
    frame = QFrame()
    frame.setObjectName("dashboard_header")
    frame.setStyleSheet(
        "QFrame#dashboard_header { background: transparent; border: none; }")
    h = QHBoxLayout(frame)
    h.setContentsMargins(0, 0, 0, 0)
    h.setSpacing(12)

    title = QLabel("Aperçu des performances")
    title.setStyleSheet(
        "color: #0f172a; font-size: 18px; font-weight: 800; "
        "background: transparent;")
    h.addWidget(title)
    h.addStretch()

    btn = QPushButton("  Voir tous les graphiques")
    btn.setMinimumHeight(40)
    btn.setCursor(Qt.PointingHandCursor)
    btn.setIcon(QIcon(":/Icon/Icons/add-svgrepo-com.svg"))
    btn.setIconSize(QSize(16, 16))
    btn.setStyleSheet("""
        QPushButton {
            background: #023E8A; color: #ffffff;
            border: none; border-radius: 10px;
            font-size: 12px; font-weight: 700; padding: 0 18px;
        }
        QPushButton:hover { background: #0077B6; }
    """)
    btn.clicked.connect(lambda: _open_all_charts(main_window))
    h.addWidget(btn)

    return frame


def _open_all_charts(main_window) -> None:
    try:
        from Setting_all_charts import Setting_all_charts
        dlg = Setting_all_charts(parent=main_window)
        dlg.exec()
    except Exception:
        logger.exception("Erreur ouverture tous les graphiques")


# ══════════════════════════════════════════════════════════════════
# Installation dashboard : 4 charts + bouton
# ══════════════════════════════════════════════════════════════════
def install_dashboard_charts(main_window) -> None:
    """
    Installe le dashboard dans `page_2` :
      - Header avec bouton "Voir tous les graphiques"
      - 2 x 2 cartes (graphiques en serveur, placeholders en client)
    Version robuste : chaque carte dans un try/except.
    """
    try:
        page_2 = getattr(main_window, "page_2", None)
        if page_2 is None:
            logger.warning("page_2 introuvable pour installer les graphiques")
            return

        # ─── Nettoie complètement l'ancien layout ───
        old = page_2.layout()
        if old is None:
            old = QVBoxLayout(page_2)
        else:
            while old.count():
                item = old.takeAt(0)
                w = item.widget()
                if w:
                    w.setParent(None)
                    w.deleteLater()
            old.setContentsMargins(0, 0, 0, 0)
            old.setSpacing(0)

        # ─── Conteneur racine ───
        container = QWidget()
        container.setObjectName("dashboard_container")
        container.setStyleSheet(
            "QWidget#dashboard_container { background: transparent; }")
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(20, 20, 20, 20)
        vbox.setSpacing(16)

        # ─── Header ───
        try:
            vbox.addWidget(_make_dashboard_header(main_window))
        except Exception:
            logger.exception("Erreur header dashboard")

        # ─── Détection mode ───
        is_client = False
        try:
            from Client.api_singleton import is_client_mode
            is_client = is_client_mode()
        except Exception:
            logger.exception("Erreur détection is_client_mode")

        logger.info(
            "install_dashboard_charts : is_client=%s", is_client)

        # ─── Grille 2x2 ───
        grid = QGridLayout()
        grid.setSpacing(16)

        # ═══ MODE CLIENT : graphiques via API ═══
        if is_client:
            try:
                from Client.api_singleton import get_api
                api = get_api()
                if api is None:
                    raise RuntimeError("API non initialisée")

                api_data = api.get_dashboard_charts()
                logger.info(
                    "Données dashboard chargées via API : "
                    "%d jours, %d mois, %d top, %d cat",
                    len(api_data.get("revenue_7days", {}).get("labels", [])),
                    len(api_data.get("revenue_12months", {}).get("labels", [])),
                    len(api_data.get("top_products", [])),
                    len(api_data.get("categories", []))
                )

                charts_def = [
                    ("Revenus des 7 derniers jours", "CA quotidien",
                     lambda: chart_revenue_line(
                         7, data=api_data.get("revenue_7days"))),
                    ("Chiffre d'affaires mensuel", "12 derniers mois",
                     lambda: chart_revenue_monthly(
                         12, data=api_data.get("revenue_12months"))),
                    ("Top 10 médicaments", "Par quantité vendue",
                     lambda: chart_top_products(
                         "quantity", 10,
                         data=api_data.get("top_products"))),
                    ("Répartition par catégorie", "CA par catégorie",
                     lambda: chart_categories_donut(
                         data=api_data.get("categories"))),
                ]

                for i, (title, sub, fn) in enumerate(charts_def):
                    try:
                        card = ChartCard(title, sub)
                        chart = fn()
                        if chart is not None and chart.series():
                            card.set_chart(chart)
                        else:
                            card.set_empty()
                        card.setMinimumHeight(260)
                        grid.addWidget(card, i // 2, i % 2)
                        logger.info(
                            "Carte graphique (API) ajoutée : %s", title)
                    except Exception:
                        logger.exception(
                            "Erreur carte graphique API %d (%s)", i, title)

            except Exception:
                logger.exception(
                    "Erreur fetch dashboard API → fallback placeholders")
                # ─── Fallback : placeholders ───
                charts_def = [
                    ("Revenus", "Serveur indisponible"),
                    ("Chiffre d'affaires mensuel", "Serveur indisponible"),
                    ("Top 10 médicaments", "Serveur indisponible"),
                    ("Répartition par catégorie", "Serveur indisponible"),
                ]
                for i, (title, sub) in enumerate(charts_def):
                    try:
                        card = _make_client_placeholder(title, sub)
                        card.setMinimumHeight(260)
                        grid.addWidget(card, i // 2, i % 2)
                    except Exception:
                        logger.exception(
                            "Erreur fallback placeholder %d", i)

        # ═══ MODE LOCAL : graphiques directs (inchangé) ═══
        else:
            charts_def = [
                ("Revenus des 7 derniers jours", "CA quotidien",
                 lambda: chart_revenue_line(7)),
                ("Chiffre d'affaires mensuel", "12 derniers mois",
                 lambda: chart_revenue_monthly(12)),
                ("Top 10 médicaments", "Par quantité vendue",
                 lambda: chart_top_products("quantity", 10)),
                ("Répartition par catégorie", "CA par catégorie",
                 chart_categories_donut),
            ]
            for i, (title, sub, fn) in enumerate(charts_def):
                try:
                    card = ChartCard(title, sub)
                    chart = fn()
                    if chart is not None and chart.series():
                        card.set_chart(chart)
                    else:
                        card.set_empty()
                    card.setMinimumHeight(260)
                    grid.addWidget(card, i // 2, i % 2)
                except Exception:
                    logger.exception(
                        "Erreur carte graphique %d (%s)", i, title)

        vbox.addLayout(grid, 1)
        old.addWidget(container)

        logger.info(
            "Dashboard installé (%s) — %d cartes",
            "client placeholders" if is_client else "graphiques locaux",
            len(charts_def))

    except Exception:
        logger.exception(
            "ERREUR FATALE install_dashboard_charts")
        # ─── Fallback visible ───
        try:
            page_2 = getattr(main_window, "page_2", None)
            if page_2 is not None:
                layout = page_2.layout()
                if layout is None:
                    layout = QVBoxLayout(page_2)
                err_lbl = QLabel(
                    "⚠️  Impossible d'installer le tableau de bord.\n\n"
                    "Vérifiez les logs pour plus de détails.")
                err_lbl.setAlignment(Qt.AlignCenter)
                err_lbl.setStyleSheet(
                    "color: #dc2626; font-size: 13px; "
                    "font-weight: 600; "
                    "padding: 40px; background: #fef2f2; "
                    "border: 1px solid #fecaca; border-radius: 12px;")
                layout.addWidget(err_lbl)
        except Exception:
            pass


def install_reports_charts(main_window) -> None:
    """
    Installe les graphiques de la page Rapports dans `page_7`.
    En mode client : placeholders (les graphiques sont déjà dans les
    3 onglets Rapports de la page).
    """
    try:
        page_7 = getattr(main_window, "page_7", None)
        if page_7 is None:
            logger.warning("page_7 introuvable pour installer les graphiques")
            return

        # Mode client : ne rien installer (page Rapports gère déjà)
        try:
            from Client.api_singleton import is_client_mode
            if is_client_mode():
                logger.info(
                    "Mode client : graphiques Rapports gérés par la page")
                return
        except Exception:
            pass

        layout = page_7.layout()
        if layout is None:
            layout = QVBoxLayout(page_7)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(16)

        # ─── CA mensuel ───
        card_month = ChartCard("Chiffre d'affaires mensuel",
                               "12 derniers mois")
        chart_month = chart_revenue_monthly(months=12)
        if chart_month.series():
            card_month.set_chart(chart_month)
        else:
            card_month.set_empty()
        layout.addWidget(card_month, 1)

        # ─── Comparaison N vs N-1 ───
        card_cmp = ChartCard("Comparaison annuelle",
                             "Année courante vs année précédente")
        chart_cmp = chart_year_comparison()
        if chart_cmp.series():
            card_cmp.set_chart(chart_cmp)
        else:
            card_cmp.set_empty()
        layout.addWidget(card_cmp, 1)

        # ─── CA par heure + Ventes par jour ───
        row = QHBoxLayout()
        row.setSpacing(16)

        card_hour = ChartCard("Activité horaire", "CA par heure")
        chart_hour = chart_revenue_hourly()
        if chart_hour.series():
            card_hour.set_chart(chart_hour)
        else:
            card_hour.set_empty()
        row.addWidget(card_hour, 1)

        card_day = ChartCard("Ventes quotidiennes", "30 derniers jours")
        chart_day = chart_sales_count_line(days=30)
        if chart_day.series():
            card_day.set_chart(chart_day)
        else:
            card_day.set_empty()
        row.addWidget(card_day, 1)

        layout.addLayout(row, 1)

        # ─── Top clients + Nouveaux clients ───
        row2 = QHBoxLayout()
        row2.setSpacing(16)

        card_clients = ChartCard("Top 10 clients", "Par CA cumulé")
        chart_clients = chart_top_clients(limit=10)
        if chart_clients.series():
            card_clients.set_chart(chart_clients)
        else:
            card_clients.set_empty()
        row2.addWidget(card_clients, 1)

        card_new = ChartCard("Nouveaux clients", "6 derniers mois")
        chart_new = chart_new_clients(months=6)
        if chart_new.series():
            card_new.set_chart(chart_new)
        else:
            card_new.set_empty()
        row2.addWidget(card_new, 1)

        layout.addLayout(row2, 1)

        # ─── Produits en rupture ───
        card_low = ChartCard("Produits en rupture",
                             "Stock ≤ 20 unités")
        chart_low = chart_low_stock(limit=10)
        if chart_low.series():
            card_low.set_chart(chart_low)
        else:
            card_low.set_empty()
        layout.addWidget(card_low, 1)

        logger.info("Graphiques rapports installés (mode local)")

    except Exception:
        logger.exception("Erreur installation graphiques rapports")


# ══════════════════════════════════════════════════════════════════
# Test autonome
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    from PySide6 import QtWidgets, QtGui

    logging.basicConfig(level=logging.INFO)
    db.get_conn()

    app = QtWidgets.QApplication(sys.argv)

    # Fenêtre de démo
    win = QtWidgets.QWidget()
    win.setWindowTitle("Nova Pharma — Graphiques")
    win.resize(1400, 900)
    win.setStyleSheet("background-color: #f0f4f8;")

    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("background: transparent; border: none;")

    content = QtWidgets.QWidget()
    content.setStyleSheet("background: transparent;")
    layout = QtWidgets.QVBoxLayout(content)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(16)

    # Demo : 4 charts
    for title, sub, chart_fn in [
        ("Revenus des 7 derniers jours", "CA quotidien", lambda: chart_revenue_line(7)),
        ("Chiffre d'affaires mensuel", "12 derniers mois", lambda: chart_revenue_monthly(12)),
        ("Top 10 médicaments", "Par quantité", lambda: chart_top_products("quantity", 10)),
        ("Répartition par catégorie", "CA", chart_categories_donut),
        ("Activité horaire", "24h", chart_revenue_hourly),
        ("Comparaison annuelle", "N vs N-1", chart_year_comparison),
        ("Top 10 clients", "CA cumulé", lambda: chart_top_clients(10)),
        ("Produits en rupture", "Stock ≤ 20", lambda: chart_low_stock(10)),
        ("Nouveaux clients", "6 mois", lambda: chart_new_clients(6)),
        ("Anonymes vs identifiés", "", chart_anonyme_split),
    ]:
        card = ChartCard(title, sub)
        chart = chart_fn()
        if chart.series():
            card.set_chart(chart)
        else:
            card.set_empty()
        card.setMinimumHeight(340)
        layout.addWidget(card, 1)

    scroll.setWidget(content)

    root = QtWidgets.QVBoxLayout(win)
    root.setContentsMargins(0, 0, 0, 0)
    root.addWidget(scroll)

    win.show()
    sys.exit(app.exec())