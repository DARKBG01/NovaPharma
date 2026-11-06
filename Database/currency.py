#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
currency.py — Gestion des devises FC/USD avec taux manuel.
=============================================================
Format principal : FC (Franc Congolais)
Format secondaire : USD ($)
"""

import logging

from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════════════════════════
def get_config_devises() -> dict:
    """Retourne la config devises actuelle."""
    try:
        return {
            "primaire": db.get_config("devise", "FC") or "FC",
            "secondaire": "USD",
            "taux": float(db.get_config("taux_change", 2250.0)),
            "dual": bool(db.get_config("afficher_dual", True)),
        }
    except Exception:
        logger.exception("Erreur get_config_devises")
        return {"primaire": "FC", "secondaire": "USD",
                "taux": 2250.0, "dual": True}


def set_taux(nouveau_taux: float, user_id: str = None,
             user_name: str = None) -> bool:
    """Met à jour le taux + audit."""
    try:
        if nouveau_taux <= 0:
            return False

        ancien = float(db.get_config("taux_change", 2250.0))

        with db.transaction():
            db.set_config("taux_change", float(nouveau_taux),
                          type_="float")

        try:
            from Database import audit
            audit.log(
                "MODIF_TAUX_CHANGE",
                utilisateur_id=user_id,
                utilisateur_name=user_name,
                cible_type="Configuration",
                cible_id="taux_change",
                cible_nom="Taux de change FC/USD",
                details={
                    "ancien_taux": ancien,
                    "nouveau_taux": float(nouveau_taux),
                },
                severite="warning")
        except Exception:
            logger.exception("Erreur audit taux change")

        logger.info("Taux change : %s → %s FC/USD", ancien, nouveau_taux)
        return True
    except Exception:
        logger.exception("Erreur set_taux")
        return False


# ══════════════════════════════════════════════════════════════════
# Conversion
# ══════════════════════════════════════════════════════════════════
def to_usd(montant_fc: float, taux: float = None) -> float:
    """Convertit FC → USD."""
    if taux is None:
        taux = get_config_devises()["taux"]
    if taux <= 0:
        return 0.0
    return float(montant_fc) / taux


def to_fc(montant_usd: float, taux: float = None) -> float:
    """Convertit USD → FC."""
    if taux is None:
        taux = get_config_devises()["taux"]
    return float(montant_usd) * taux


# ══════════════════════════════════════════════════════════════════
# Formatage
# ══════════════════════════════════════════════════════════════════
def format_money(montant: float, devise: str = "FC",
                 dual: bool = None) -> str:
    """
    Formate un montant.
    Si dual=True : "45 000 FC (~$20.00)"
    """
    try:
        cfg = get_config_devises()
        montant = float(montant or 0)

        if dual is None:
            dual = cfg["dual"]

        # Format principal
        if devise.upper() == "USD":
            principal = f"$ {montant:,.2f}".replace(",", " ")
        else:
            principal = f"{montant:,.0f} FC".replace(",", " ")

        if not dual:
            return principal

        # Ajoute équivalent
        if devise.upper() == "USD":
            eq = to_fc(montant, cfg["taux"])
            equivalent = f"({eq:,.0f} FC)".replace(",", " ")
        else:
            eq = to_usd(montant, cfg["taux"])
            equivalent = f"(~$ {eq:,.2f})".replace(",", " ")

        return f"{principal} {equivalent}"
    except Exception:
        return f"{montant:,.0f}"


def format_dual(montant_fc: float) -> str:
    """Raccourci : formate un montant FC en dual."""
    return format_money(montant_fc, "FC", dual=True)


def format_simple_fc(montant_fc: float) -> str:
    """Format FC sans équivalent."""
    return format_money(montant_fc, "FC", dual=False)