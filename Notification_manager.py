#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notification_manager.py — Système de notifications global.
===========================================================
- Toasts flottants (coins haut-droit) avec icônes SVG
- Centre de notifications (historique DB)
"""

import logging
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt, QTimer

from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Toast (Popup animé)
# ══════════════════════════════════════════════════════════════════
class Toast(QtWidgets.QFrame):
    def __init__(self, message: str, type_: str, parent, duration=4000):
        super().__init__(parent)
        self.setObjectName("toast")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Style et icônes par type
        configs = {
            "success": ("#dcfce7", "#15803d", "#bbf7d0", "check-circle"),
            "danger": ("#fee2e2", "#b91c1c", "#fecaca", "x-circle"),
            "warning": ("#fef3c7", "#b45309", "#fde68a", "alert-triangle"),
            "info": ("#dbeafe", "#1e40af", "#bfdbfe", "info")
        }
        bg, fg, border, icon_name = configs.get(type_, configs["info"])

        self.setStyleSheet(f"""
            QFrame#toast {{
                background: {bg};
                border: 1px solid {border};
                border-radius: 10px;
            }}
            QLabel {{ background: transparent; color: {fg}; font-weight: 600; }}
        """)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        # Icône SVG (au lieu du caractère)
        icon_lbl = QtWidgets.QLabel()
        icon_lbl.setFixedSize(20, 20)
        pix = QtGui.QPixmap(f":/Icon/Icons/{icon_name}.svg")
        if not pix.isNull():
            # On colorie le pixmap avec la couleur du texte (fg)
            colored_pix = QtGui.QPixmap(pix.size())
            colored_pix.fill(Qt.transparent)
            painter = QtGui.QPainter(colored_pix)
            painter.drawPixmap(0, 0, pix)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
            painter.fillRect(colored_pix.rect(), QtGui.QColor(fg))
            painter.end()

            icon_lbl.setPixmap(colored_pix.scaled(
                20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        layout.addWidget(icon_lbl)

        # Message
        lbl = QtWidgets.QLabel(message)
        lbl.setWordWrap(True)
        layout.addWidget(lbl, 1)

        # Auto-delete
        QTimer.singleShot(duration, self.close)


# ══════════════════════════════════════════════════════════════════
# Manager
# ══════════════════════════════════════════════════════════════════
class NotificationManager:
    def __init__(self):
        self._main_window = None
        self._toasts = []

    def attach_to_main(self, main_window):
        self._main_window = main_window

    def _save_to_db(self, type_: str, title: str, message: str, action_url: str = None):
        try:
            with db.transaction():
                db.execute("""
                    INSERT INTO Notification (id, type, title, message, action_url)
                    VALUES (?, ?, ?, ?, ?)
                """, (db.new_id(), type_, title, message, action_url))
        except Exception:
            logger.exception("Erreur sauvegarde notification")

    def _show_toast(self, message: str, type_: str, duration: int):
        if not self._main_window:
            return

        toast = Toast(message, type_, self._main_window)
        toast.adjustSize()

        # Placement (haut-droit)
        x = self._main_window.width() - toast.width() - 20
        y = 80 + (len(self._toasts) * (toast.height() + 10))
        toast.move(x, y)
        toast.show()

        self._toasts.append(toast)

        # Nettoyage de la liste quand le toast se ferme
        def _cleanup():
            if toast in self._toasts:
                self._toasts.remove(toast)
            toast.deleteLater()

        QTimer.singleShot(duration, _cleanup)

    # ─── API publique ───
    def success(self, message: str, duration=3000):
        self._show_toast(message, "success", duration)

    def error(self, message: str, duration=5000):
        self._show_toast(message, "danger", duration)
        self._save_to_db("danger", "Erreur", message)

    def warning(self, message: str, duration=5000):
        self._show_toast(message, "warning", duration)
        self._save_to_db("warning", "Attention", message)

    def info(self, message: str, duration=3000):
        self._show_toast(message, "info", duration)
        self._save_to_db("info", "Information", message)


# Singleton
notify = NotificationManager()