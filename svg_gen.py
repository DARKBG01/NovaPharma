#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
svg_gen.py — Générateur d'icônes SVG pour Nova Pharma
=====================================================
Génère des icônes SVG vectorielles pures (style Feather/Lucide, 24x24, stroke-based).
AUCUN EMOJI. Uniquement des chemins SVG professionnels et scalables.

Usage :
    python svg_gen.py

Sortie :
    Assets/Icons/*.svg          (variante couleur primaire)
    Assets/Icons/*_white.svg    (variante blanche, pour headers/boutons colorés)

Intégration Qt :
    1) Ajouter dans Icon.qrc :
        <qresource prefix="/Icon">
            <file>Icons/home.svg</file>
            <file>Icons/home_white.svg</file>
            ...
        </qresource>
    2) Compiler :
        pyside6-rcc Icon.qrc -o Icon_rc.py
"""

from pathlib import Path
from typing import Dict

# ─── Palette Nova Pharma ────────────────────────────────────────────
PRIMARY = "#023E8A"
BLUE = "#0077B6"
CYAN = "#00B4D8"
GOLD = "#F4A261"
GREEN = "#16A34A"
RED = "#DC2626"
SLATE = "#64748B"
WHITE = "#FFFFFF"

OUTPUT_DIR = Path(__file__).resolve().parent / "Assets" / "Icons"


# ─── Helpers ────────────────────────────────────────────────────────
def _svg(paths: str, color: str = PRIMARY, size: int = 24, stroke_width: float = 2.0) -> str:
    """Assemble un SVG stroke-based cohérent (24x24 viewBox)."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round">\n'
        f'{paths.strip()}\n'
        f'</svg>\n'
    )


def _write(name: str, content: str) -> None:
    (OUTPUT_DIR / f"{name}.svg").write_text(content, encoding="utf-8")


# ════════════════════════════════════════════════════════════════════
#   BIBLIOTHÈQUE D'ICÔNES (Pure SVG, aucun emoji)
# ════════════════════════════════════════════════════════════════════
ICONS: Dict[str, str] = {
    # ═══ 1. Navigation & UI ═══════════════════════════════════
    "home": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>',
    "menu": '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "list": '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevron-up": '<path d="m6 15 6-6 6 6"/>',
    "chevron-left": '<path d="m15 6-6 6 6 6"/>',
    "chevron-right": '<path d="m9 6 6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "close": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "sidebar": '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/>',

    # ═══ 2. Actions Principales ═══════════════════════════════
    "plus": '<path d="M12 5v14"/><path d="M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "check": '<path d="m5 13 4 4L19 7"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8.5 12.2 2.4 2.4 4.6-5"/>',
    "x-circle": '<circle cx="12" cy="12" r="9"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    "edit": '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "trash": '<path d="M3 6h18"/><path d="M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>',
    "save": '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8"/><path d="M7 3v5h8"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
    "refresh": '<path d="M23 4v6h-6"/><path d="M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10"/><path d="M20.49 15a9 9 0 0 1-14.85 3.36L1 14"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20.5 20.5-4-4"/>',
    "filter": '<path d="M22 3H2l8 9.46V19l4 2v-8.54z"/>',
    "printer": '<path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',

    # ═══ 3. Utilisateur & Profil ══════════════════════════════
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "user-check": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/>',
    "user-plus": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><line x1="19" y1="8" x2="19" y2="14"/><line x1="16" y1="11" x2="22" y2="11"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "shield-check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',

    # ═══ 4. Pharmacie & Médical ═══════════════════════════════
    "pharmacy": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M12 8v8"/><path d="M8 12h8"/>',
    "pill": '<path d="m10.5 20.5-7-7a5 5 0 0 1 7-7l7 7a5 5 0 0 1-7 7z"/><path d="m8.5 8.5 7 7"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "virus": '<circle cx="12" cy="12" r="6"/><path d="M12 1v3"/><path d="M12 20v3"/><path d="M4.2 4.2l2.1 2.1"/><path d="M17.7 17.7l2.1 2.1"/><path d="M1 12h3"/><path d="M20 12h3"/>',

    # ═══ 5. Commerce & Caisse (POS) ═══════════════════════════
    "shopping-cart": '<circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>',
    "shopping-bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    "credit-card": '<rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/>',
    "wallet": '<path d="M20 12V8a2 2 0 0 0-2-2H4a2 2 0 0 1 0-4h14a2 2 0 0 1 2 2v2"/><rect x="2" y="8" width="20" height="14" rx="2"/><circle cx="17" cy="15" r="1.5"/>',
    "dollar": '<line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "tag": '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>',
    "receipt": '<path d="M4 2v20l3-2 3 2 3-2 3 2 3-2 1 2V2l-3 2-3-2-3 2-3-2-3 2z"/><path d="M8 8h8"/><path d="M8 12h8"/><path d="M8 16h8"/>',
    "invoice": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 13h6"/><path d="M9 17h6"/>',
    "barcode": '<path d="M3 5v14"/><path d="M6 5v14"/><path d="M10 5v14"/><path d="M13 5v14"/><path d="M17 5v14"/><path d="M20 5v14"/>',
    "scan": '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" y1="12" x2="17" y2="12"/>',
    "calculator": '<rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="16" y2="10"/><line x1="8" y1="14" x2="16" y2="14"/><line x1="8" y1="18" x2="16" y2="18"/>',

    # ═══ 6. Fichiers & Documents ══════════════════════════════
    "file-text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "folder": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    "clipboard-check": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="m9 14 2 2 4-4"/>',

    # ═══ 7. Temps & Statut ════════════════════════════════════
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><line x1="16" y1="3" x2="16" y2="7"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="3" y1="11" x2="21" y2="11"/>',
    "calendar-check": '<rect x="3" y="5" width="18" height="16" rx="2"/><line x1="16" y1="3" x2="16" y2="7"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="3" y1="11" x2="21" y2="11"/><path d="m9 16 2 2 4-4"/>',
    "history": '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l3.5 2"/>',
    "alert-triangle": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 8h.01"/>',

    # ═══ 8. Graphiques & Système ══════════════════════════════
    "chart-pie": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "chart-line": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "log-out": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
}

# ════════════════════════════════════════════════════════════════════
#   VARIANTES BLANCHES
#   Icônes déclinées en #FFFFFF pour les headers sur dégradé et boutons.
# ════════════════════════════════════════════════════════════════════
WHITE_VARIANTS = {
    "home", "menu", "grid", "list", "chevron-down", "chevron-up", "close",
    "plus", "minus", "check", "check-circle", "x-circle", "edit", "trash",
    "save", "download", "upload", "refresh", "search", "filter", "printer",
    "user", "user-check", "user-plus", "users", "shield-check",
    "pharmacy", "pill", "activity", "virus",
    "shopping-cart", "shopping-bag", "credit-card", "wallet", "dollar",
    "tag", "receipt", "invoice", "barcode", "scan", "calculator",
    "file-text", "folder", "clipboard-check",
    "calendar", "calendar-check", "history", "alert-triangle", "info",
    "chart-pie", "chart-line", "settings", "log-out"
}


# ════════════════════════════════════════════════════════════════════
#   MAIN
# ════════════════════════════════════════════════════════════════════
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"→ Répertoire de sortie : {OUTPUT_DIR}\n")

    total = 0
    for name, paths in ICONS.items():
        _write(name, _svg(paths, color=PRIMARY))
        total += 1
        if name in WHITE_VARIANTS:
            _write(f"{name}_white", _svg(paths, color=WHITE))
            total += 1

    print(f"✅ {len(ICONS)} icônes de base générées.")
    print(f"✅ {len(WHITE_VARIANTS)} variantes blanches générées.")
    print(f"✅ {total} fichiers SVG au total dans {OUTPUT_DIR}")


# ─────────────────────────────────────────────────────────────────
#  ALIASES — Noms attendus par MainWindow.ui (Compatibilité totale)
#  Génère les mêmes SVG sous les anciens noms pour ne rien casser.
# ─────────────────────────────────────────────────────────────────
ALIASES = {
    # Navigation
    "home-svgrepo-com": "home",
    "home-svgrepo-com2": "home",
    "home-svgrepo-com3": "home",
    "pie-chart-1-svgrepo-com": "chart-pie",
    "pie-chart-1-svgrepo-com2": "chart-pie",

    # Médical & Articles
    "medical-medicine-health-11-svgrepo-com": "pill",
    "medical-medicine-health-11-svgrepo-com2": "pill",
    "pharmacy-icon-svgrepo-com2": "pharmacy",

    # Utilisateurs
    "users-group-svgrepo-com3": "users",
    "users-group-svgrepo-com4": "users",
    "user-plus-alt-1-svgrepo-com": "user-plus",
    "user-setting-svgrepo-com": "settings",
    "user-setting-svgrepo-com2": "settings",

    # Facturation & Caisse
    "invoice-dollar-svgrepo-com": "invoice",
    "invoice-dollar-svgrepo-com (Copie)": "invoice",
    "shopping-cart-free-5-svgrepo-com": "shopping-cart",
    "shopping-bag-svgrepo-com": "shopping-bag",
    "currency-dollar-circle-svgrepo-com": "dollar",

    # Actions & Divers
    "history-svgrepo-com": "history",
    "history-svgrepo-com2": "history",
    "history-svgrepo-com3": "history",
    "report-svgrepo-com": "chart-line",
    "report-svgrepo-com2": "chart-line",
    "biohazard-svgrepo-com": "virus",
    "exclamation-mark-triangle-f-svgrepo-com": "alert-triangle",
    "add-svgrepo-com": "plus",
    "edit-svgrepo-com (2)": "edit",
    "edit-svgrepo-com_2": "edit",
    "printer": "printer",
    "printer-svgrepo-com": "printer",
    "search-alt-2-svgrepo-com": "search",
}


def generate_aliases():
    """Copie chaque icône SVG sous ses noms alternatifs pour compatibilité UI."""
    generated = 0
    for alias, source in ALIASES.items():
        src = OUTPUT_DIR / f"{source}.svg"
        if not src.exists():
            continue

        # Générer la version normale
        (OUTPUT_DIR / f"{alias}.svg").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        generated += 1

        # Générer la version blanche si elle existe
        src_w = OUTPUT_DIR / f"{source}_white.svg"
        if src_w.exists():
            (OUTPUT_DIR / f"{alias}_white.svg").write_text(src_w.read_text(encoding="utf-8"), encoding="utf-8")
            generated += 1

    print(f"✅ {generated} alias SVG générés pour compatibilité avec l'ancienne UI.")


if __name__ == "__main__":
    main()
    generate_aliases()