#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nova Pharma — Point d'entrée principal
=======================================
Flux :
  1. Initialise la base (db + seed + migrations)
  2. Détecte le mode (autonome / serveur / client)
  3. Si first_time → Wizard Configuration
  4. Boucle : Login → MainWindow → (Logout → Login | Quitter)
"""

import sys
import logging

import pandas as pd
from PySide6 import QtWidgets, QtCore

from Database import db, seed
from Client import api_singleton


def setup_logging():
    import os
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                "logs/novapharma.log", encoding="utf-8"),
        ],
    )


def run_wizard() -> bool:
    """Ouvre le wizard. Retourne True si terminé, False si annulé."""
    from Configuration import Configuration
    wizard = Configuration()
    return wizard.exec() == QtWidgets.QDialog.Accepted


def apply_light_theme(app: QtWidgets.QApplication) -> None:
    """Force un thème clair indépendant du système."""
    from PySide6 import QtGui
    app.setStyle("Fusion")
    p = QtGui.QPalette()
    p.setColor(QtGui.QPalette.Window,          QtGui.QColor("#f0f4f8"))
    p.setColor(QtGui.QPalette.WindowText,      QtGui.QColor("#0f172a"))
    p.setColor(QtGui.QPalette.Base,            QtGui.QColor("#ffffff"))
    p.setColor(QtGui.QPalette.AlternateBase,   QtGui.QColor("#f8fafc"))
    p.setColor(QtGui.QPalette.Text,            QtGui.QColor("#0f172a"))
    p.setColor(QtGui.QPalette.Button,          QtGui.QColor("#ffffff"))
    p.setColor(QtGui.QPalette.ButtonText,      QtGui.QColor("#0f172a"))
    p.setColor(QtGui.QPalette.Highlight,       QtGui.QColor("#0077B6"))
    p.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#ffffff"))
    p.setColor(QtGui.QPalette.PlaceholderText, QtGui.QColor("#94a3b8"))
    app.setPalette(p)


def detect_and_init_mode() -> str:
    """
    Détecte le mode (autonome / serveur / client) et initialise l'API
    si nécessaire.

    - autonome : 1 seul PC, pas de serveur, DB locale
    - serveur  : PC hôte, DB locale + serveur FastAPI à part
    - client   : PC client, utilise l'API du serveur

    Retourne le mode.
    """
    logger = logging.getLogger("main")

    try:
        mode = db.get_config("server_mode", "autonome") or "autonome"
    except Exception:
        mode = "autonome"

    if mode == "client":
        host = db.get_config("server_host", "127.0.0.1") or "127.0.0.1"
        port = int(db.get_config("server_port", 5001) or 5001)

        logger.info("→ Mode CLIENT — serveur cible : %s:%d", host, port)
        api = api_singleton.init_api(
            base_url=f"http://{host}:{port}", mode="client")

        # Vérifie que le serveur est joignable
        try:
            info = api.sante()
            logger.info("✅ Serveur joignable — version %s",
                        info.get("version", "?"))
        except Exception as e:
            logger.warning(
                "⚠️  Serveur injoignable : %s — le Login affichera "
                "un message d'erreur", e)
    else:
        logger.info("→ Mode %s — base locale", mode.upper())
        api_singleton.init_api(mode=mode)

    return mode


def main() -> int:
    setup_logging()
    logger = logging.getLogger("main")

    # ═══ UN SEUL QApplication (jamais recréé) ═══
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("NovaPharma")
    apply_light_theme(app)

    # ═══ Timer : vérif backup auto toutes les heures ═══
    def _check_backup_timer():
        try:
            from Database import backup_engine
            backup_engine.check_and_run_auto_backup()
        except Exception:
            logger.exception("Erreur timer backup")

    backup_timer = QtCore.QTimer()
    backup_timer.timeout.connect(_check_backup_timer)
    backup_timer.start(3600 * 1000)  # 1 h
    app.backup_timer = backup_timer  # garde la référence

    # ═══ 1. Initialise la base ═══
    try:
        db.get_conn()
        seed.run()

        # ═══ Migrations (idempotentes) ═══
        from Database import migrations
        migrations.run_all()

        # ═══ NOUVEAU : backup auto en arrière-plan ═══
        try:
            from Database import backup_engine
            created, path = backup_engine.check_and_run_auto_backup()
            if created:
                logger.info("Backup auto créée au démarrage : %s", path)
        except Exception:
            logger.exception("Erreur backup auto au démarrage")

    except Exception as e:
        logger.exception("Impossible d'initialiser la base")
        QtWidgets.QMessageBox.critical(
            None, "Erreur fatale",
            f"Impossible d'initialiser la base de données :\n{e}")
        return 1

    # ═══ 1.5 Détecte le mode serveur/client ═══
    try:
        detect_and_init_mode()
    except Exception:
        logger.exception("Erreur détection mode serveur/client")
        # On continue en autonome par défaut

    # ═══ 2. Wizard si première fois ═══
    if db.get_config("first_time", True):
        logger.info("→ Ouverture du wizard d'inscription")
        if not run_wizard():
            logger.info("Wizard annulé par l'utilisateur")
            return 0
        logger.info("Wizard terminé avec succès")

    # ═══════════════════════════════════════════════════════════════
    # 3. BOUCLE : Login → MainWindow → (Logout → Login | Quitter)
    # ═══════════════════════════════════════════════════════════════
    from Login import LoginDialog
    from Setting_main_window import Setting_main_window

    # Référence globale pour éviter le garbage-collector
    app.main_window = None

    first_iteration = True

    while True:
        # ─── Login ───
        logger.info("→ Ouverture du login")
        login = LoginDialog()

        if login.exec() != QtWidgets.QDialog.Accepted:
            logger.info("Login annulé — fermeture de l'application")
            return 0

        user_id = getattr(login, "last_user_id", None)
        role = getattr(login, "last_role", None)
        identifiant = getattr(login, "last_identifiant", None)

        if not user_id:
            logger.error("Login validé sans user_id — arrêt")
            return 1

        logger.info("→ Login validé : %s (%s)", identifiant, role)

        # ─── Splash (uniquement 1ère fois) ───
        splash = None
        if first_iteration:
            try:
                from Loading_screen import LoadingScreen
                splash = LoadingScreen(
                    fullscreen=True,
                    title="Nova Pharma",
                    subtitle="Préparation de votre espace de travail…")
                splash.show()
                splash.set_step_count(6)
                QtWidgets.QApplication.processEvents()
            except Exception:
                logger.exception("Erreur création splash")
                splash = None

        # ─── MainWindow ───
        try:
            window = Setting_main_window(
                user_id=user_id,
                role=role,
                identifiant=identifiant,
                splash=splash,
            )
            app.main_window = window
        except Exception as e:
            logger.exception("Erreur chargement MainWindow")
            if splash:
                try:
                    splash.close()
                except Exception:
                    pass
            QtWidgets.QMessageBox.critical(
                None, "Erreur au démarrage",
                f"Impossible de charger l'application :\n{e}")
            return 1

        # ─── Flag de déconnexion (attribut global sur app) ───
        app.should_logout = False

        def _on_logout():
            app.should_logout = True

        try:
            window.logout_requested.connect(_on_logout)
        except Exception:
            logger.exception("Impossible de connecter logout_requested")

        # ─── Boucle d'événements locale (bloque jusqu'à fermeture) ───
        loop = QtCore.QEventLoop()

        def _on_window_closed():
            try:
                loop.quit()
            except Exception:
                pass

        try:
            window.window_closed.connect(_on_window_closed)
        except Exception:
            logger.exception("Impossible de connecter window_closed")

        window.showMaximized()

        # Ferme le splash après affichage
        if splash is not None:
            QtCore.QTimer.singleShot(400, splash.finish)

        logger.info("→ Entrée dans la boucle locale")
        loop.exec()

        # ─── Décision ───
        if not getattr(app, "should_logout", False):
            logger.info("→ Fermeture normale de l'application")
            return 0

        logger.info("→ Déconnexion — retour au login")
        first_iteration = False

    return 0


if __name__ == "__main__":
    sys.exit(main())