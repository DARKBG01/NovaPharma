#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
printer_manager.py — Gestion imprimantes (ticket + rapport).
=============================================================
Configs par MACHINE (QSettings) : nom des imprimantes
Configs GLOBALES (DB) : auto-print, auto-open
"""

import logging
import os
import platform
import subprocess
import sys

from PySide6 import QtCore

logger = logging.getLogger(__name__)

# Clés QSettings (per-machine)
SETTINGS_ORG = "NovaPharma"
SETTINGS_APP = "Printers"
KEY_TICKET = "printer/ticket"
KEY_REPORT = "printer/report"


# ══════════════════════════════════════════════════════════════════
# Détection des imprimantes système
# ══════════════════════════════════════════════════════════════════
def list_printers() -> list[str]:
    """Liste les imprimantes disponibles sur le système."""
    system = platform.system()

    try:
        if system == "Windows":
            import win32print
            printers = [
                p[2] for p in win32print.EnumPrinters(
                    win32print.PRINTER_ENUM_LOCAL
                    | win32print.PRINTER_ENUM_CONNECTIONS)
            ]
            return sorted(printers)

        elif system == "Linux":
            result = subprocess.run(
                ["lpstat", "-a"], capture_output=True,
                text=True, timeout=5)
            if result.returncode == 0:
                printers = []
                for line in result.stdout.strip().split("\n"):
                    if line:
                        name = line.split()[0]
                        printers.append(name)
                return sorted(printers)

        elif system == "Darwin":  # macOS
            result = subprocess.run(
                ["lpstat", "-a"], capture_output=True,
                text=True, timeout=5)
            if result.returncode == 0:
                return sorted(
                    line.split()[0]
                    for line in result.stdout.strip().split("\n")
                    if line)

    except Exception:
        logger.exception("Erreur listing imprimantes")

    return []


# ══════════════════════════════════════════════════════════════════
# Gestion ticket / rapport (QSettings)
# ══════════════════════════════════════════════════════════════════
def _settings() -> QtCore.QSettings:
    return QtCore.QSettings(SETTINGS_ORG, SETTINGS_APP)


def get_ticket_printer() -> str:
    """Retourne l'imprimante configurée pour les tickets."""
    return _settings().value(KEY_TICKET, "", type=str) or ""


def set_ticket_printer(name: str) -> None:
    """Définit l'imprimante des tickets."""
    _settings().setValue(KEY_TICKET, name or "")


def get_report_printer() -> str:
    """Retourne l'imprimante configurée pour les rapports A4."""
    return _settings().value(KEY_REPORT, "", type=str) or ""


def set_report_printer(name: str) -> None:
    """Définit l'imprimante des rapports A4."""
    _settings().setValue(KEY_REPORT, name or "")



# ══════════════════════════════════════════════════════════════════
# Compat ancienne API (printer par défaut)
# ══════════════════════════════════════════════════════════════════
def get_default_printer() -> str:
    """Alias rétro-compat : retourne l'imprimante ticket."""
    return get_ticket_printer()


def set_default_printer(name: str) -> None:
    """Alias rétro-compat : définit l'imprimante ticket."""
    set_ticket_printer(name)


# ══════════════════════════════════════════════════════════════════
# Impression silencieuse (paramétrée)
# ══════════════════════════════════════════════════════════════════
def print_pdf_silent(path: str, printer: str = None,
                     kind: str = "ticket") -> bool:
    """
    Imprime un PDF sur l'imprimante spécifiée.

    Args:
        path   : chemin du PDF
        printer: nom de l'imprimante (None → utilise la config selon `kind`)
        kind   : "ticket" ou "report" (choisit l'imprimante par défaut)
    """
    if not os.path.isfile(path):
        logger.error("PDF introuvable : %s", path)
        return False

    # Résolution de l'imprimante
    if printer is None:
        printer = (get_ticket_printer()
                   if kind == "ticket"
                   else get_report_printer())

    system = platform.system()

    try:
        if system == "Windows":
            return _print_windows(path, printer)
        elif system in ("Linux", "Darwin"):
            return _print_linux(path, printer)
        else:
            logger.error("Système non supporté : %s", system)
            return False
    except Exception:
        logger.exception("Erreur impression %s", path)
        return False


def _print_windows(path: str, printer: str) -> bool:
    """Impression sur Windows."""
    try:
        import win32api

        if printer:
            win32api.ShellExecute(
                0, "printto", path,
                f'"{printer}"', ".", 0)
        else:
            win32api.ShellExecute(0, "print", path, None, ".", 0)

        logger.info("Impression Windows : %s → %s",
                    path, printer or "défaut système")
        return True
    except Exception:
        logger.exception("Erreur impression Windows")
        return False


def _print_linux(path: str, printer: str) -> bool:
    """Impression sur Linux / macOS via lp."""
    try:
        cmd = ["lp"]
        if printer:
            cmd += ["-d", printer]
        cmd.append(path)

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15)

        if result.returncode == 0:
            logger.info("Impression Linux : %s → %s",
                        path, printer or "défaut système")
            return True

        logger.error("Erreur lp : %s", result.stderr)
        return False
    except Exception:
        logger.exception("Erreur impression Linux")
        return False


# ══════════════════════════════════════════════════════════════════
# Test d'impression
# ══════════════════════════════════════════════════════════════════
def test_print(kind: str = "ticket") -> bool:
    """Imprime une page de test."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm

    path = os.path.join(
        os.path.expanduser("~"),
        f"nova_test_{kind}.pdf")

    try:
        if kind == "ticket":
            # Format ticket 80mm
            width = 80 * mm
            height = 120 * mm
            page_size = (width, height)
        else:
            page_size = A4

        c = canvas.Canvas(path, pagesize=page_size)
        c.setFont("Helvetica-Bold", 14)

        if kind == "ticket":
            c.drawCentredString(width / 2, height - 20, "NOVA PHARMA")
            c.setFont("Helvetica", 10)
            c.drawCentredString(width / 2, height - 40, "Test TICKET")
            c.drawCentredString(width / 2, 30, "OK")
        else:
            c.drawString(100, 750, "NOVA PHARMA")
            c.setFont("Helvetica", 12)
            c.drawString(100, 720, "Test impression A4")
            c.drawString(100, 700, "Page de test OK")

        c.save()
        return print_pdf_silent(path, kind=kind)
    except Exception:
        logger.exception("Erreur test impression")
        return False