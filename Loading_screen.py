#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loading_screen.py — Overlay de chargement Nova Pharma.
========================================================
Splash screen non-modal qui affiche une barre de progression
pendant le chargement des données (DB, pages, graphiques).

Utilisation :
    splash = LoadingScreen()
    splash.show()
    splash.set_status("Chargement des produits…")
    splash.set_progress(30)
    ...
    splash.close()
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

logger = logging.getLogger(__name__)

ICON_APP = ":/Icon/Icons/1758107223736.png"
LOGO_ICON = ":/Icon/Icons/1758107223736.png"


class LoadingScreen(QtWidgets.QWidget):
    """
    Overlay plein écran ou fenêtre popup (selon fullscreen).
    - Mode fullscreen=True  : occupe tout l'écran (parfait au boot)
    - Mode fullscreen=False : petite fenêtre centrée
    """

    def __init__(self, parent=None, fullscreen=False,
                 title="Nova Pharma",
                 subtitle="Chargement en cours…"):
        super().__init__(parent)

        self.fullscreen = fullscreen
        self._step_count = 0
        self._current_step = 0

        self._setup_window(title, subtitle)
        self._build_ui(title, subtitle)

        if fullscreen:
            self._cover_screen()

    # ══════════════════════════════════════════════════════════════
    def _setup_window(self, title, subtitle):
        self.setWindowTitle(title)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        if self.fullscreen:
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1:0, y1:0, x2:0.6, y2:1,
                        stop:0 #023E8A, stop:1 #0077B6);
                    color: #ffffff;
                }
                QLabel { background: transparent; color: #ffffff; }
            """)
        else:
            self.setFixedSize(480, 280)
            self.setStyleSheet("""
                QWidget {
                    background: #ffffff;
                    color: #0f172a;
                    border-radius: 16px;
                }
                QLabel { background: transparent; }
            """)

    def _cover_screen(self):
        screen = QtWidgets.QApplication.primaryScreen()
        if screen is None:
            return
        geo = screen.geometry()
        self.setGeometry(geo)

    # ══════════════════════════════════════════════════════════════
    def _build_ui(self, title, subtitle):
        # Layout racine
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Centre
        root.addStretch(1)

        center_wrap = QtWidgets.QHBoxLayout()
        center_wrap.addStretch(1)

        card = QtWidgets.QFrame()
        card.setObjectName("loading_card")
        if self.fullscreen:
            card.setFixedSize(520, 380)
            card.setStyleSheet("""
                QFrame#loading_card {
                    background: rgba(255,255,255,0.08);
                    border: 1px solid rgba(255,255,255,0.18);
                    border-radius: 24px;
                }
                QFrame#loading_card QLabel {
                    background: transparent;
                    color: #ffffff;
                }
            """)
        else:
            card.setFixedSize(440, 260)
            card.setStyleSheet("""
                QFrame#loading_card {
                    background: #ffffff;
                    border: 1px solid #e2e8f0;
                    border-radius: 24px;
                }
            """)

        v = QtWidgets.QVBoxLayout(card)
        v.setContentsMargins(40, 36, 40, 36)
        v.setSpacing(16)

        # ─── Logo ───
        logo = QtWidgets.QLabel()
        logo.setFixedSize(72, 72)
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            QLabel {
                background: rgba(255,255,255,0.15);
                border-radius: 20px;
                padding: 14px;
            }
        """)
        pix = QtGui.QPixmap(LOGO_ICON)
        if not pix.isNull():
            logo.setPixmap(pix.scaled(
                40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            logo.setText("Rx")
            logo.setStyleSheet("""
                QLabel {
                    background: rgba(255,255,255,0.15);
                    border-radius: 20px;
                    font-size: 24px;
                    font-weight: 800;
                    color: #ffffff;
                }
            """)
        v.addWidget(logo, 0, Qt.AlignHCenter)

        # ─── Titre ───
        lbl_title = QtWidgets.QLabel(title)
        lbl_title.setAlignment(Qt.AlignCenter)
        if self.fullscreen:
            lbl_title.setStyleSheet(
                "color: #ffffff; font-size: 22px; font-weight: 800; "
                "letter-spacing: 0.5px; background: transparent;")
        else:
            lbl_title.setStyleSheet(
                "color: #023E8A; font-size: 20px; font-weight: 800; "
                "background: transparent;")
        v.addWidget(lbl_title)

        # ─── Sous-titre dynamique ───
        self.lbl_status = QtWidgets.QLabel(subtitle)
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setWordWrap(True)
        if self.fullscreen:
            self.lbl_status.setStyleSheet(
                "color: rgba(255,255,255,0.8); font-size: 12px; "
                "font-weight: 500; background: transparent;")
        else:
            self.lbl_status.setStyleSheet(
                "color: #64748b; font-size: 12px; font-weight: 500; "
                "background: transparent;")
        v.addWidget(self.lbl_status)

        v.addSpacing(8)

        # ─── Barre de progression ───
        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        if self.fullscreen:
            self.progress.setStyleSheet("""
                QProgressBar {
                    background: rgba(255,255,255,0.15);
                    border: none;
                    border-radius: 4px;
                }
                QProgressBar::chunk {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #00B4D8, stop:1 #90E0EF);
                    border-radius: 4px;
                }
            """)
        else:
            self.progress.setStyleSheet("""
                QProgressBar {
                    background: #e2e8f0;
                    border: none;
                    border-radius: 4px;
                }
                QProgressBar::chunk {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #0077B6, stop:1 #00B4D8);
                    border-radius: 4px;
                }
            """)
        v.addWidget(self.progress)

        # ─── Pourcentage ───
        self.lbl_pct = QtWidgets.QLabel("0 %")
        self.lbl_pct.setAlignment(Qt.AlignCenter)
        if self.fullscreen:
            self.lbl_pct.setStyleSheet(
                "color: rgba(255,255,255,0.6); font-size: 11px; "
                "font-weight: 700; background: transparent;")
        else:
            self.lbl_pct.setStyleSheet(
                "color: #94a3b8; font-size: 11px; font-weight: 700; "
                "background: transparent;")
        v.addWidget(self.lbl_pct)

        center_wrap.addWidget(card, 0, Qt.AlignCenter)
        center_wrap.addStretch(1)
        root.addLayout(center_wrap)

        # Version en bas
        root.addStretch(1)

        lbl_version = QtWidgets.QLabel("Nova Pharma v4.5")
        lbl_version.setAlignment(Qt.AlignCenter)
        if self.fullscreen:
            lbl_version.setStyleSheet(
                "color: rgba(255,255,255,0.45); font-size: 10px; "
                "font-weight: 600; letter-spacing: 1px; "
                "background: transparent; padding-bottom: 24px;")
        else:
            lbl_version.setStyleSheet(
                "color: #94a3b8; font-size: 10px; font-weight: 600; "
                "background: transparent;")
        root.addWidget(lbl_version)

    # ══════════════════════════════════════════════════════════════
    # API publique
    # ══════════════════════════════════════════════════════════════
    def set_status(self, message: str) -> None:
        """Change le message affiché."""
        try:
            self.lbl_status.setText(message)
            QtWidgets.QApplication.processEvents()
        except Exception:
            pass

    def set_progress(self, value: int) -> None:
        """Définit la progression (0-100)."""
        try:
            value = max(0, min(100, int(value)))
            self.progress.setValue(value)
            self.lbl_pct.setText(f"{value} %")
            QtWidgets.QApplication.processEvents()
        except Exception:
            pass

    def step(self, message: str = None, weight: int = 1) -> None:
        """
        Avance d'une étape. Appelle d'abord set_step_count() pour définir
        le nombre total d'étapes.
        """
        self._current_step += 1
        if self._step_count > 0:
            pct = int((self._current_step / self._step_count) * 100)
            self.set_progress(pct)
        if message:
            self.set_status(message)

    def set_step_count(self, total: int) -> None:
        """Définit le nombre total d'étapes pour `step()`."""
        self._step_count = max(1, int(total))
        self._current_step = 0

    def finish(self) -> None:
        """Marque comme terminé et ferme."""
        self.set_progress(100)
        self.set_status("Prêt !")
        QtCore.QTimer.singleShot(300, self.close)


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys, time
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)

    splash = LoadingScreen(fullscreen=True)
    splash.show()
    splash.set_step_count(5)

    steps = [
        "Initialisation de la base…",
        "Chargement des produits…",
        "Chargement des clients…",
        "Préparation de l'interface…",
        "Installation des graphiques…",
    ]
    for s in steps:
        splash.step(s, 1)
        time.sleep(0.6)

    splash.finish()
    QtCore.QTimer.singleShot(1500, app.quit)
    sys.exit(app.exec())