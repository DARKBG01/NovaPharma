#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notification_manager.py — Système de notifications internes.
=============================================================
Permet d'envoyer des notifications à l'utilisateur via un bandeau
en haut de la fenêtre principale.

Usage :
    from Notification_manager import notify
    notify.info("Produit ajouté")
    notify.warning("Stock faible pour Doliprane")
    notify.danger("Erreur d'enregistrement")
    notify.success("Vente enregistrée")
"""

import logging
from datetime import datetime, timedelta

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt, QTimer

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Types de notification
# ══════════════════════════════════════════════════════════════════
STYLE_INFO = {
    "bg": "#eff6ff", "border": "#bfdbfe",
    "fg": "#1e40af", "icon": "info",
}
STYLE_SUCCESS = {
    "bg": "#f0fdf4", "border": "#bbf7d0",
    "fg": "#15803d", "icon": "check-circle",
}
STYLE_WARNING = {
    "bg": "#fef3c7", "border": "#fde68a",
    "fg": "#b45309", "icon": "alert-triangle",
}
STYLE_DANGER = {
    "bg": "#fef2f2", "border": "#fecaca",
    "fg": "#b91c1c", "icon": "x-circle",
}

STYLES = {
    "info":    STYLE_INFO,
    "success": STYLE_SUCCESS,
    "warning": STYLE_WARNING,
    "danger":  STYLE_DANGER,
}


# ══════════════════════════════════════════════════════════════════
# Widget bandeau
# ══════════════════════════════════════════════════════════════════
class NotificationBanner(QtWidgets.QFrame):
    """Un bandeau de notification individuel."""

    closed = QtCore.Signal(object)  # self

    def __init__(self, message: str, level: str = "info",
                 duration_ms: int = 5000, parent=None):
        super().__init__(parent)
        self.level = level
        self.duration_ms = duration_ms
        self._build_ui(message)
        self._apply_style()
        self._start_timer()

    def _build_ui(self, message: str):
        self.setObjectName("notification_banner")
        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(14, 10, 10, 10)
        h.setSpacing(10)

        # Icône
        self.icon = QtWidgets.QLabel()
        self.icon.setFixedSize(18, 18)
        h.addWidget(self.icon)

        # Message
        self.label = QtWidgets.QLabel(message)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(
            "background: transparent; font-size: 12px; font-weight: 600;")
        h.addWidget(self.label, 1)

        # Bouton fermer
        self.btn_close = QtWidgets.QPushButton()
        self.btn_close.setFixedSize(24, 24)
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.setIcon(QtGui.QIcon(":/Icon/Icons/close.svg"))
        self.btn_close.setIconSize(QtCore.QSize(12, 12))
        self.btn_close.setStyleSheet(
            "QPushButton { background: transparent; border: none; }"
            "QPushButton:hover { background: rgba(0,0,0,0.06); "
            "border-radius: 6px; }")
        self.btn_close.clicked.connect(self._close)
        h.addWidget(self.btn_close)

    def _apply_style(self):
        style = STYLES.get(self.level, STYLE_INFO)
        self.setStyleSheet(f"""
            QFrame#notification_banner {{
                background: {style['bg']};
                border: 1px solid {style['border']};
                border-radius: 10px;
            }}
            QLabel {{ background: transparent; color: {style['fg']}; }}
        """)
        self.label.setStyleSheet(
            f"color: {style['fg']}; font-size: 12px; font-weight: 600; "
            f"background: transparent;")

        # Icône SVG
        pix = QtGui.QPixmap(f":/Icon/Icons/{style['icon']}.svg")
        if not pix.isNull():
            self.icon.setPixmap(pix.scaled(
                16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def _start_timer(self):
        if self.duration_ms > 0:
            QTimer.singleShot(self.duration_ms, self._close)

    def _close(self):
        self.closed.emit(self)
        try:
            self.setParent(None)
            self.deleteLater()
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════
# Gestionnaire
# ══════════════════════════════════════════════════════════════════
class NotificationManager(QtCore.QObject):

    def __init__(self):
        super().__init__()
        self._container = None
        self._max_visible = 3

    def attach(self, container: QtWidgets.QWidget):
        """
        Attache le gestionnaire à un conteneur (QVBoxLayout prêt à
        accueillir les bandeaux). Appelé par Setting_main_window.
        """
        self._container = container

    def _emit(self, message: str, level: str, duration_ms: int):
        if self._container is None:
            logger.debug(
                "[NOTIF %s] %s", level.upper(), message)
            return

        try:
            banner = NotificationBanner(
                message, level=level,
                duration_ms=duration_ms,
                parent=self._container)
            banner.closed.connect(self._on_banner_closed)

            layout = self._container.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(self._container)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(6)

            layout.addWidget(banner)
            self._trim()

        except Exception:
            logger.exception("Erreur affichage notification")

    def _trim(self):
        """Garde seulement N bandeaux visibles."""
        try:
            layout = self._container.layout()
            if layout is None:
                return
            # Compte les bandeaux
            banners = []
            for i in range(layout.count()):
                w = layout.itemAt(i).widget()
                if isinstance(w, NotificationBanner):
                    banners.append(w)
            while len(banners) > self._max_visible:
                old = banners.pop(0)
                old._close()
        except Exception:
            pass

    def _on_banner_closed(self, banner):
        pass

    # ── API publique ──
    def info(self, message: str, duration_ms: int = 5000):
        self._emit(message, "info", duration_ms)

    def success(self, message: str, duration_ms: int = 4000):
        self._emit(message, "success", duration_ms)

    def warning(self, message: str, duration_ms: int = 7000):
        self._emit(message, "warning", duration_ms)

    def danger(self, message: str, duration_ms: int = 9000):
        self._emit(message, "danger", duration_ms)
    
    def attach_to_main(self, main_window):
        """
        Attache les notifications à une fenêtre principale qui n'a
        pas de conteneur dédié. Crée un conteneur flottant en haut à droite.
        """
        try:
            self._container = QtWidgets.QWidget(main_window)
            self._container.setStyleSheet("background: transparent;")

            # ═══ CRUCIAL : le container ne doit PAS intercepter les clics ═══
            self._container.setAttribute(
                QtCore.Qt.WA_TransparentForMouseEvents, True)
            self._container.setAttribute(
                QtCore.Qt.WA_NoSystemBackground, True)

            layout = QtWidgets.QVBoxLayout(self._container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(6)

            # Positionne en haut à droite
            geo = main_window.geometry()
            self._container.setGeometry(
                geo.width() - 420, 100, 400, 300)

            # Repositionner si la fenêtre bouge
            def _reposition():
                try:
                    g = main_window.geometry()
                    self._container.setGeometry(
                        g.width() - 420, 100, 400, 300)
                    self._container.raise_()
                except Exception:
                    pass

            self._container.raise_()
            self._container.show()
        except Exception:
            logger.exception("Erreur attach_to_main")


# ══════════════════════════════════════════════════════════════════
# Singleton
# ══════════════════════════════════════════════════════════════════
notify = NotificationManager()