#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alertes_dashboard.py — Widget panneau d'alertes du dashboard.
===============================================================
Regroupe toutes les anomalies :
  - Produits en rupture de stock
  - Ventes annulées récemment
  - Backups manquants
  - Échecs de connexion suspects
  - Produits à rotation lente

Chaque alerte est cliquable → navigue vers la page concernée.

CORRECTIF v4.8.1 :
  - Comparaison des dates `Historique.Date_vent` corrigée.
    La colonne est stockée en "DD/MM/YYYY HH:MM:SS", donc la
    comparaison string directe est fausse. On convertit en ISO
    via `_iso_expr()` (substr SQL) pour comparer correctement.
"""

import logging
from datetime import datetime, timedelta

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt, Signal

from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Helpers dates — Historique stocke en "DD/MM/YYYY HH:MM:SS"
# ══════════════════════════════════════════════════════════════════
def _to_iso(fr_date: str) -> str:
    """Convertit 'DD/MM/YYYY HH:MM:SS' → 'YYYY-MM-DD HH:MM:SS'."""
    try:
        d, rest = fr_date.split(" ", 1)
        day, month, year = d.split("/")
        return f"{year}-{month}-{day} {rest}"
    except Exception:
        return fr_date


def _iso_expr(col: str) -> str:
    """
    Expression SQL qui convertit une colonne FR en ISO à la volée.

    'DD/MM/YYYY HH:MM:SS'
        ↓
    substr(col, 7, 4)  → 'YYYY'
    substr(col, 4, 2)  → 'MM'
    substr(col, 1, 2)  → 'DD'
    substr(col, 11)    → ' HH:MM:SS'
        ↓
    'YYYY-MM-DD HH:MM:SS'
    """
    return (
        f"(substr({col}, 7, 4) || '-' || "
        f"substr({col}, 4, 2) || '-' || "
        f"substr({col}, 1, 2) || "
        f"substr({col}, 11))"
    )


# ══════════════════════════════════════════════════════════════════
# Types d'alertes
# ══════════════════════════════════════════════════════════════════
LEVEL_INFO    = "info"
LEVEL_WARNING = "warning"
LEVEL_DANGER  = "danger"

LEVEL_STYLES = {
    LEVEL_INFO: {
        "bg": "#eff6ff",
        "border": "#bfdbfe",
        "fg": "#1e40af",
        "icon": "info",
    },
    LEVEL_WARNING: {
        "bg": "#fef3c7",
        "border": "#fde68a",
        "fg": "#b45309",
        "icon": "alert-triangle",
    },
    LEVEL_DANGER: {
        "bg": "#fef2f2",
        "border": "#fecaca",
        "fg": "#b91c1c",
        "icon": "x-circle",
    },
}


# ══════════════════════════════════════════════════════════════════
# Widget ligne d'alerte
# ══════════════════════════════════════════════════════════════════
class AlertRow(QtWidgets.QFrame):
    """Une ligne d'alerte cliquable."""

    clicked = Signal(dict)   # payload

    def __init__(self, payload: dict, parent=None):
        super().__init__(parent)
        self.payload = payload
        self.setCursor(Qt.PointingHandCursor)
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        self.setObjectName("alert_row")
        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(14, 12, 14, 12)
        h.setSpacing(12)

        # Icône
        self.icon = QtWidgets.QLabel()
        self.icon.setFixedSize(24, 24)
        h.addWidget(self.icon)

        # Textes
        v = QtWidgets.QVBoxLayout()
        v.setSpacing(2)

        self.title = QtWidgets.QLabel(self.payload.get("title", ""))
        self.title.setStyleSheet(
            "background: transparent; font-size: 12px; font-weight: 800;")
        v.addWidget(self.title)

        self.subtitle = QtWidgets.QLabel(self.payload.get("subtitle", ""))
        self.subtitle.setStyleSheet(
            "background: transparent; font-size: 11px; font-weight: 500;")
        self.subtitle.setWordWrap(True)
        v.addWidget(self.subtitle)

        h.addLayout(v, 1)

        # Badge (compteur)
        badge_text = self.payload.get("badge", "")
        if badge_text:
            self.badge = QtWidgets.QLabel(str(badge_text))
            self.badge.setFixedSize(28, 28)
            self.badge.setAlignment(Qt.AlignCenter)
            self.badge.setStyleSheet(
                "background: rgba(0,0,0,0.08); border-radius: 14px; "
                "font-size: 12px; font-weight: 800;")
            h.addWidget(self.badge)

        # Flèche
        arrow = QtWidgets.QLabel()
        arrow.setFixedSize(16, 16)
        pix = QtGui.QPixmap(":/Icon/Icons/chevron-right.svg")
        if not pix.isNull():
            arrow.setPixmap(pix.scaled(
                14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(arrow)

    def _apply_style(self):
        style = LEVEL_STYLES.get(
            self.payload.get("level", LEVEL_INFO), LEVEL_STYLES[LEVEL_INFO])

        self.setStyleSheet(f"""
            QFrame#alert_row {{
                background: {style['bg']};
                border: 1px solid {style['border']};
                border-radius: 10px;
            }}
            QFrame#alert_row:hover {{
                border-color: {style['fg']};
            }}
            QFrame#alert_row QLabel {{
                color: {style['fg']};
            }}
        """)

        self.title.setStyleSheet(
            f"color: {style['fg']}; font-size: 12px; font-weight: 800; "
            f"background: transparent;")
        self.subtitle.setStyleSheet(
            f"color: {style['fg']}; font-size: 11px; font-weight: 500; "
            f"background: transparent;")

        pix = QtGui.QPixmap(f":/Icon/Icons/{style['icon']}.svg")
        if not pix.isNull():
            self.icon.setPixmap(pix.scaled(
                22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.payload)
        super().mousePressEvent(event)


# ══════════════════════════════════════════════════════════════════
# Détecteurs d'alertes (statiques — réutilisables)
# ══════════════════════════════════════════════════════════════════
def _detect_rupture_stock() -> list:
    """Produits en rupture (≤ seuil configurable)."""
    try:
        seuil = int(db.get_config("seuil_stock", 20))
    except Exception:
        seuil = 20

    try:
        row = db.query_one(
            "SELECT COUNT(*) AS n FROM produits "
            "WHERE actif = 1 AND Quantite <= ?",
            (seuil,))
        n = int(row["n"] or 0) if row else 0
    except Exception:
        logger.exception("Erreur détection rupture")
        return []

    if n == 0:
        return []

    level = LEVEL_DANGER if n >= 5 else LEVEL_WARNING
    return [{
        "id": "rupture_stock",
        "level": level,
        "icon": "alert-triangle",
        "title": "Produits en rupture de stock",
        "subtitle": f"{n} produit(s) avec moins de {seuil} unités",
        "badge": n,
        "action": "goto_products_filter_rupture",
    }]


def _detect_ventes_annulees() -> list:
    """
    Ventes annulées dans les 7 derniers jours.
    ⚠️ CORRECTIF : comparaison ISO car Historique.Date_vent est en FR.
    """
    try:
        seuil_fr = (datetime.now() - timedelta(days=7)
                    ).strftime("%d/%m/%Y %H:%M:%S")
        seuil_iso = _to_iso(seuil_fr)
    except Exception:
        return []

    try:
        row = db.query_one(
            f"""SELECT COUNT(*) AS n FROM Historique
                WHERE annule = 1
                  AND {_iso_expr('Date_vent')} >= ?""",
            (seuil_iso,))
        n = int(row["n"] or 0) if row else 0
    except Exception:
        logger.exception("Erreur détection ventes annulées")
        return []

    if n == 0:
        return []

    level = LEVEL_DANGER if n >= 10 else LEVEL_WARNING
    return [{
        "id": "ventes_annulees",
        "level": level,
        "icon": "x-circle",
        "title": "Ventes annulées récemment",
        "subtitle": f"{n} vente(s) annulée(s) ces 7 derniers jours",
        "badge": n,
        "action": "goto_historique_filter_annulees",
    }]


def _detect_backup() -> list:
    """Backup manquant (> 7 jours)."""
    last = db.get_config("backup_last_daily", "")
    if not last:
        return [{
            "id": "backup_missing",
            "level": LEVEL_WARNING,
            "icon": "save",
            "title": "Aucune sauvegarde effectuée",
            "subtitle": "Pensez à vérifier les paramètres de backup",
            "badge": "!",
            "action": "goto_parametres_backup",
        }]

    try:
        dt = datetime.fromisoformat(last)
        jours = (datetime.now() - dt).days
        if jours <= 7:
            return []
    except Exception:
        return []

    return [{
        "id": "backup_old",
        "level": LEVEL_WARNING,
        "icon": "save",
        "title": "Sauvegarde ancienne",
        "subtitle": f"Dernière sauvegarde il y a {jours} jour(s)",
        "badge": jours,
        "action": "goto_parametres_backup",
    }]


def _detect_echecs_connexion() -> list:
    """
    Échecs de connexion dans les dernières 24h.
    Note : AuditLog.date_action est déjà en format ISO (datetime('now') SQL)
          donc pas besoin de conversion ici.
    """
    try:
        seuil_iso = (datetime.now() - timedelta(hours=24)
                     ).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return []

    try:
        row = db.query_one(
            """SELECT COUNT(*) AS n FROM AuditLog
               WHERE action = 'ECHEC_CONNEXION' AND date_action >= ?""",
            (seuil_iso,))
        n = int(row["n"] or 0) if row else 0
    except Exception:
        return []

    if n < 3:
        return []

    level = LEVEL_DANGER if n >= 10 else LEVEL_WARNING
    return [{
        "id": "echecs_connexion",
        "level": level,
        "icon": "shield-alert",
        "title": "Tentatives de connexion suspectes",
        "subtitle": f"{n} échec(s) de connexion dans les 24 h",
        "badge": n,
        "action": "goto_audit_filter_echecs",
    }]


def collect_alerts() -> list:
    """Collecte toutes les alertes (utilitaire réutilisable)."""
    alerts = []
    for fn in (_detect_rupture_stock, _detect_ventes_annulees,
               _detect_backup, _detect_echecs_connexion):
        try:
            alerts += fn()
        except Exception:
            logger.exception("Erreur détecteur %s", fn.__name__)
    return alerts


# ══════════════════════════════════════════════════════════════════
# Panneau complet
# ══════════════════════════════════════════════════════════════════
class AlertesDashboard(QtWidgets.QFrame):
    """
    Panneau des alertes centralisées du dashboard.
    À appeler via `refresh()` pour recharger les alertes.
    """

    alert_clicked = Signal(dict)   # payload de l'alerte cliquée

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window

        self.setObjectName("alertes_dashboard")
        self._build_ui()

        # Charge initialement
        self.refresh()

    def _build_ui(self):
        self.setStyleSheet("""
            QFrame#alertes_dashboard {
                background: #ffffff;
                border: 1px solid #e6ebf2;
                border-radius: 18px;
            }
            QFrame#alertes_dashboard QLabel {
                background: transparent;
            }
        """)

        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(20, 18, 20, 18)
        v.setSpacing(12)

        # ─── Header ───
        h = QtWidgets.QHBoxLayout()
        h.setSpacing(10)

        icon = QtWidgets.QLabel()
        icon.setFixedSize(28, 28)
        pix = QtGui.QPixmap(":/Icon/Icons/alert-triangle.svg")
        if not pix.isNull():
            icon.setPixmap(pix.scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(icon)

        title = QtWidgets.QLabel("Alertes")
        title.setStyleSheet(
            "color: #0f172a; font-size: 15px; font-weight: 800; "
            "background: transparent;")
        h.addWidget(title)

        h.addStretch()

        self.count_badge = QtWidgets.QLabel("0")
        self.count_badge.setFixedHeight(24)
        self.count_badge.setStyleSheet("""
            background: #fef2f2;
            color: #b91c1c;
            border: 1px solid #fecaca;
            border-radius: 12px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.5px;
        """)
        h.addWidget(self.count_badge)

        self.btn_refresh = QtWidgets.QPushButton()
        self.btn_refresh.setFixedSize(28, 28)
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.setIcon(QtGui.QIcon(":/Icon/Icons/refresh.svg"))
        self.btn_refresh.setIconSize(QtCore.QSize(14, 14))
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            QPushButton:hover { background: #e2e8f0; }
        """)
        self.btn_refresh.clicked.connect(self.refresh)
        h.addWidget(self.btn_refresh)

        v.addLayout(h)

        # ─── Conteneur des alertes ───
        self.alerts_container = QtWidgets.QWidget()
        self.alerts_container.setStyleSheet("background: transparent;")
        self.alerts_layout = QtWidgets.QVBoxLayout(self.alerts_container)
        self.alerts_layout.setContentsMargins(0, 0, 0, 0)
        self.alerts_layout.setSpacing(8)
        v.addWidget(self.alerts_container)

        # ─── État vide (caché par défaut) ───
        self.empty_label = QtWidgets.QLabel(
            "✓ Aucune alerte active — tout va bien !")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            color: #15803d;
            font-size: 12px;
            font-weight: 700;
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-radius: 10px;
            padding: 18px;
        """)
        self.empty_label.setVisible(False)
        v.addWidget(self.empty_label)

    # ══════════════════════════════════════════════════════════════
    # Rafraîchissement
    # ══════════════════════════════════════════════════════════════
    def refresh(self):
        """Recharge toutes les alertes."""
        # Vide le layout
        while self.alerts_layout.count():
            item = self.alerts_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        # Collecte les alertes
        alerts = collect_alerts()

        # Trie par niveau : danger > warning > info
        order = {LEVEL_DANGER: 0, LEVEL_WARNING: 1, LEVEL_INFO: 2}
        alerts.sort(key=lambda a: order.get(a.get("level"), 3))

        # Affiche
        if not alerts:
            self.empty_label.setVisible(True)
            self.count_badge.setText("0")
            self.count_badge.setStyleSheet("""
                background: #f0fdf4;
                color: #15803d;
                border: 1px solid #bbf7d0;
                border-radius: 12px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 0.5px;
            """)
            return

        self.empty_label.setVisible(False)
        self.count_badge.setText(str(len(alerts)))

        for alert in alerts:
            row = AlertRow(alert, parent=self.alerts_container)
            row.clicked.connect(self._on_alert_clicked)
            self.alerts_layout.addWidget(row)

    def _on_alert_clicked(self, payload: dict):
        """Émet le signal vers le MainWindow."""
        self.alert_clicked.emit(payload)

    # ══════════════════════════════════════════════════════════════
    # Compat : anciens appels `_alert_*` (utilisés par AlertesPage)
    # ══════════════════════════════════════════════════════════════
    def _alert_rupture_stock(self) -> list:
        return _detect_rupture_stock()

    def _alert_ventes_annulees(self) -> list:
        return _detect_ventes_annulees()

    def _alert_backup(self) -> list:
        return _detect_backup()

    def _alert_echecs_connexion(self) -> list:
        return _detect_echecs_connexion()


# ══════════════════════════════════════════════════════════════════
# Installation dans le dashboard
# ══════════════════════════════════════════════════════════════════
def install_alerts_dashboard(main_window) -> None:
    """
    Installe le panneau d'alertes dans le dashboard (page_2).
    À appeler après install_dashboard_charts.
    """
    try:
        page_2 = getattr(main_window, "page_2", None)
        if page_2 is None:
            logger.warning("page_2 introuvable")
            return

        # Cherche le layout principal de page_2
        layout = page_2.layout()
        if layout is None:
            layout = QtWidgets.QVBoxLayout(page_2)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

        # Évite les doublons
        if getattr(main_window, "_alerts_dashboard", None) is not None:
            main_window._alerts_dashboard.refresh()
            return

        # Crée le panneau
        alerts_panel = AlertesDashboard(parent=page_2, main_window=main_window)
        alerts_panel.setMinimumHeight(200)

        # Connexion
        alerts_panel.alert_clicked.connect(
            lambda p: _on_alert_action(main_window, p))

        # Insère AU DÉBUT du layout (avant les graphiques)
        layout.insertWidget(0, alerts_panel)

        main_window._alerts_dashboard = alerts_panel
        logger.info("Panneau d'alertes installé dans page_2")

    except Exception:
        logger.exception("Erreur installation panneau d'alertes")


def _on_alert_action(main_window, payload: dict):
    """Dispatch une action selon le type d'alerte."""
    action = payload.get("action", "")
    logger.info("Alerte cliquée : %s", action)

    try:
        # ─── Produits en rupture → page Articles filtrée ───
        if action == "goto_products_filter_rupture":
            try:
                main_window._goto(2)   # page_3
                main_window.View_rupture_stock()
            except Exception:
                pass

        # ─── Ventes annulées → Historique ───
        elif action == "goto_historique_filter_annulees":
            try:
                main_window._goto(6)   # page_6
                if hasattr(main_window, "page_historique"):
                    # Pas de filtre dédié, on laisse l'utilisateur
                    pass
            except Exception:
                pass

        # ─── Backup → page Paramètres onglet Sauvegarde ───
        elif action == "goto_parametres_backup":
            try:
                main_window._goto(10)   # page_12
                if hasattr(main_window, "page_parametres"):
                    main_window.page_parametres.tabs.setCurrentIndex(3)
            except Exception:
                pass

        # ─── Échecs connexion → Audit ───
        elif action == "goto_audit_filter_echecs":
            try:
                main_window._goto(8)   # page_13
            except Exception:
                pass

    except Exception:
        logger.exception("Erreur dispatch alerte")


# ══════════════════════════════════════════════════════════════════
# Page Alertes (dédiée)
# ══════════════════════════════════════════════════════════════════
class AlertesPage(QtWidgets.QWidget):
    """Page dédiée aux alertes (remplace le panneau du dashboard)."""

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        self.setStyleSheet("""
            QWidget { background: #f0f4f8; }
            QLabel { background: transparent; }
        """)

        v = QtWidgets.QVBoxLayout(self)
        v.setContentsMargins(24, 24, 24, 24)
        v.setSpacing(16)

        # Header
        header = QtWidgets.QFrame()
        header.setStyleSheet("""
            QFrame { background: #ffffff; border: 1px solid #e6ebf2;
                     border-radius: 18px; }
        """)
        h = QtWidgets.QHBoxLayout(header)
        h.setContentsMargins(28, 22, 28, 22)
        h.setSpacing(16)

        icon = QtWidgets.QLabel()
        icon.setFixedSize(48, 48)
        icon.setStyleSheet(
            "background: #fef3c7; border-radius: 14px; padding: 12px;")
        pix = QtGui.QPixmap(":/Icon/Icons/alert-triangle.svg")
        if not pix.isNull():
            icon.setPixmap(pix.scaled(
                24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.setAlignment(Qt.AlignCenter)
        h.addWidget(icon)

        titles = QtWidgets.QVBoxLayout()
        titles.setSpacing(2)
        t1 = QtWidgets.QLabel("Centre d'alertes")
        t1.setStyleSheet(
            "color: #0f172a; font-size: 20px; font-weight: 800; "
            "background: transparent;")
        titles.addWidget(t1)
        t2 = QtWidgets.QLabel(
            "Toutes les anomalies et points d'attention")
        t2.setStyleSheet(
            "color: #64748b; font-size: 12px; background: transparent;")
        titles.addWidget(t2)
        h.addLayout(titles)

        h.addStretch()

        self.count_badge = QtWidgets.QLabel("0")
        self.count_badge.setStyleSheet("""
            background: #fef2f2; color: #b91c1c;
            border: 1px solid #fecaca; border-radius: 14px;
            padding: 6px 16px; font-size: 12px;
            font-weight: 800; letter-spacing: 1px;
        """)
        h.addWidget(self.count_badge)

        btn_refresh = QtWidgets.QPushButton("Actualiser")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setMinimumHeight(40)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background: #ffffff; color: #475569;
                border: 1.5px solid #dbe3ec; border-radius: 10px;
                padding: 0 20px; font-size: 12px; font-weight: 700;
            }
            QPushButton:hover { background: #f8fafc; }
        """)
        btn_refresh.clicked.connect(self.refresh)
        h.addWidget(btn_refresh)

        v.addWidget(header)

        # Conteneur des alertes
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }")

        content = QtWidgets.QWidget()
        content.setStyleSheet("background: transparent;")
        self.list_layout = QtWidgets.QVBoxLayout(content)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)

        self.empty_label = QtWidgets.QLabel(
            "✓ Aucune alerte active — tout va bien !")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            color: #15803d; font-size: 14px; font-weight: 700;
            background: #f0fdf4; border: 1px solid #bbf7d0;
            border-radius: 14px; padding: 40px;
        """)
        self.empty_label.setVisible(False)
        self.list_layout.addWidget(self.empty_label)

        scroll.setWidget(content)
        v.addWidget(scroll, 1)

    def refresh(self):
        """Recharge les alertes."""
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            w = item.widget()
            if w is not None and w is not self.empty_label:
                w.setParent(None)
                w.deleteLater()

        # Réintègre le label vide au début
        if self.empty_label.parent() is None:
            self.list_layout.addWidget(self.empty_label)

        # ─── Collecte via les fonctions statiques (plus de widget jetable) ───
        alerts = collect_alerts()

        order = {LEVEL_DANGER: 0, LEVEL_WARNING: 1, LEVEL_INFO: 2}
        alerts.sort(key=lambda a: order.get(a.get("level"), 3))

        if not alerts:
            self.empty_label.setVisible(True)
            self.count_badge.setText("0 alerte")
            self.count_badge.setStyleSheet("""
                background: #f0fdf4; color: #15803d;
                border: 1px solid #bbf7d0; border-radius: 14px;
                padding: 6px 16px; font-size: 12px;
                font-weight: 800; letter-spacing: 1px;
            """)
            return

        self.empty_label.setVisible(False)
        self.count_badge.setText(f"{len(alerts)} alerte(s)")

        for alert in alerts:
            row = AlertRow(alert, parent=self)
            row.clicked.connect(self._on_alert_clicked)
            self.list_layout.addWidget(row)

        self.list_layout.addStretch()

    def _on_alert_clicked(self, payload):
        if self.main_window is not None:
            _on_alert_action(self.main_window, payload)


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()

    w = QtWidgets.QWidget()
    w.resize(600, 400)
    w.setStyleSheet("background: #f0f4f8;")
    layout = QtWidgets.QVBoxLayout(w)
    layout.setContentsMargins(20, 20, 20, 20)

    panel = AlertesDashboard()
    layout.addWidget(panel)
    layout.addStretch()

    w.show()
    sys.exit(app.exec())