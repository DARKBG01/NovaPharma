#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_doc.py — Générateur du guide utilisateur PDF Nova Pharma.
===================================================================
Génère un guide complet de ~40 pages couvrant les 21 modules.

Usage :
    python docs/generer_doc.py
    python docs/generer_doc.py -o mon_guide.pdf
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    PageBreak, Table, TableStyle, Image, KeepTogether,
    NextPageTemplate,
)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Palette Nova Pharma
# ══════════════════════════════════════════════════════════════════
PRIMARY    = colors.HexColor("#023E8A")
BLUE       = colors.HexColor("#0077B6")
CYAN       = colors.HexColor("#00B4D8")
LIGHT      = colors.HexColor("#CAF0F8")
SUCCESS    = colors.HexColor("#16A34A")
DANGER     = colors.HexColor("#DC2626")
WARNING    = colors.HexColor("#F4A261")
DARK       = colors.HexColor("#0f172a")
GREY       = colors.HexColor("#64748b")
LIGHTGREY  = colors.HexColor("#f8fafc")
BORDER     = colors.HexColor("#e2e8f0")

# Couleurs de boxes
INFO_BG    = colors.HexColor("#dbeafe")
INFO_FG    = colors.HexColor("#1e40af")
WARN_BG    = colors.HexColor("#fef3c7")
WARN_FG    = colors.HexColor("#92400e")
OK_BG      = colors.HexColor("#dcfce7")
OK_FG      = colors.HexColor("#15803d")
DANGER_BG  = colors.HexColor("#fee2e2")
DANGER_FG  = colors.HexColor("#b91c1c")

APP_VERSION = "2.0.0"


# ══════════════════════════════════════════════════════════════════
# Styles
# ══════════════════════════════════════════════════════════════════
def _make_styles() -> dict:
    base = getSampleStyleSheet()

    return {
        "cover_title": ParagraphStyle(
            "cover_title", parent=base["Title"],
            fontSize=38, leading=44, textColor=colors.white,
            alignment=TA_CENTER, spaceAfter=20,
            fontName="Helvetica-Bold"),

        "cover_sub": ParagraphStyle(
            "cover_sub", parent=base["Normal"],
            fontSize=16, leading=22, textColor=colors.white,
            alignment=TA_CENTER, spaceAfter=10),

        "cover_meta": ParagraphStyle(
            "cover_meta", parent=base["Normal"],
            fontSize=10, textColor=colors.white,
            alignment=TA_CENTER),

        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"],
            fontSize=22, leading=28, textColor=PRIMARY,
            spaceBefore=24, spaceAfter=14,
            fontName="Helvetica-Bold"),

        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"],
            fontSize=15, leading=20, textColor=BLUE,
            spaceBefore=14, spaceAfter=8,
            fontName="Helvetica-Bold"),

        "h3": ParagraphStyle(
            "h3", parent=base["Heading3"],
            fontSize=12.5, leading=17, textColor=DARK,
            spaceBefore=10, spaceAfter=6,
            fontName="Helvetica-Bold"),

        "body": ParagraphStyle(
            "body", parent=base["BodyText"],
            fontSize=10.5, leading=15.5, textColor=DARK,
            alignment=TA_JUSTIFY, spaceAfter=8),

        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"],
            fontSize=10.5, leading=15, textColor=DARK,
            leftIndent=22, bulletIndent=10, spaceAfter=3),

        "info": ParagraphStyle(
            "info", parent=base["Normal"],
            fontSize=10, leading=14.5, textColor=DARK,
            alignment=TA_LEFT),

        "code": ParagraphStyle(
            "code", parent=base["Code"],
            fontSize=9, leading=12, textColor=DARK,
            fontName="Courier", backColor=LIGHTGREY,
            leftIndent=12, rightIndent=12,
            borderColor=BORDER, borderWidth=0.5,
            borderPadding=8),
    }


# ══════════════════════════════════════════════════════════════════
# Helpers de contenu
# ══════════════════════════════════════════════════════════════════
def _box(text: str, styles: dict,
         bg: colors.Color = INFO_BG,
         border: colors.Color = INFO_FG) -> Table:
    """Encadré coloré pour info / alerte."""
    p = Paragraph(text, styles["info"])
    t = Table([[p]], colWidths=[16 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 1, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


def _table(headers: list, rows: list,
           col_widths: list = None) -> Table:
    """Tableau propre avec header bleu."""
    data = [headers] + rows
    if col_widths is None:
        col_widths = [16 * cm / len(headers)] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, LIGHTGREY]),
    ]))
    return t


def _p(text: str, styles: dict) -> Paragraph:
    return Paragraph(text, styles["body"])


def _b(text: str, styles: dict) -> Paragraph:
    """Bullet point."""
    return Paragraph(text, styles["bullet"], bulletText="•")


# ══════════════════════════════════════════════════════════════════
# COUVERTURE & SOMMAIRE
# ══════════════════════════════════════════════════════════════════
def _build_cover(styles: dict, nom_pharmacie: str) -> list:
    elements = [Spacer(1, 3.5 * cm)]
    elements.append(Paragraph("NOVA PHARMA", styles["cover_title"]))
    elements.append(Paragraph("Guide utilisateur", styles["cover_sub"]))
    elements.append(Spacer(1, 1.5 * cm))

    if nom_pharmacie:
        elements.append(Paragraph(
            f"<b>{nom_pharmacie}</b>", styles["cover_sub"]))

    elements.append(Spacer(1, 3 * cm))
    elements.append(Paragraph(
        f"Version {APP_VERSION}  •  "
        f"{datetime.now().strftime('%B %Y')}",
        styles["cover_meta"]))
    elements.append(Spacer(1, 7 * cm))
    elements.append(Paragraph(
        "Développé par TEAM NOVA", styles["cover_meta"]))
    elements.append(Paragraph(
        "teamnovaoff@gmail.com", styles["cover_meta"]))
    return elements


def _build_sommaire(styles: dict) -> list:
    elements = [Paragraph("Sommaire", styles["h1"]), Spacer(1, 0.4 * cm)]

    toc = [
        ("1",  "Présentation générale"),
        ("2",  "Démarrage et connexion"),
        ("3",  "Rôles et permissions"),
        ("4",  "Page d'accueil"),
        ("5",  "Tableau de bord et graphiques"),
        ("6",  "Gestion des articles (produits)"),
        ("7",  "Gestion des clients"),
        ("8",  "Facturation"),
        ("9",  "Bons de livraison fournisseur (BLF)"),
        ("10", "Historique des ventes et commandes"),
        ("11", "Alertes"),
        ("12", "Rapports et exports"),
        ("13", "Journal d'audit"),
        ("14", "Gestion des utilisateurs"),
        ("15", "Paramètres"),
        ("16", "Surveillance (OWNER / DEVELOPER)"),
        ("17", "Modes d'installation"),
        ("18", "Sauvegardes et restauration"),
        ("19", "Questions fréquentes"),
        ("20", "Dépannage"),
        ("21", "Support et contact"),
    ]

    data = [[f"{n}.", title] for n, title in toc]
    t = Table(data, colWidths=[1.5 * cm, 14.5 * cm])
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), BLUE),
        ("TEXTCOLOR", (1, 0), (1, -1), DARK),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, BORDER),
    ]))
    elements.append(t)
    elements.append(PageBreak())
    return elements


# ══════════════════════════════════════════════════════════════════
# SECTION 1 — Présentation générale
# ══════════════════════════════════════════════════════════════════
def _build_s1(styles: dict) -> list:
    return [
        Paragraph("1. Présentation générale", styles["h1"]),
        _p("<b>Nova Pharma</b> est un logiciel de gestion complet conçu "
           "pour les pharmacies (petites, moyennes et grandes). Il "
           "centralise dans une seule application :", styles),
        _b("La <b>vente au comptoir</b> (facturation, impression)", styles),
        _b("La <b>gestion du stock</b> (entrées, sorties, ajustements)", styles),
        _b("Le <b>suivi client</b> (historique, fidélité)", styles),
        _b("Les <b>commandes fournisseurs</b> (BLF)", styles),
        _b("Les <b>rapports</b> d'activité", styles),
        _b("La <b>traçabilité complète</b> (audit anti-falsification)", styles),

        Paragraph("Points forts", styles["h2"]),
        _b("✅ <b>Hors ligne</b> par défaut — fonctionne sans internet", styles),
        _b("✅ <b>Multi-postes</b> possible (serveur / client réseau local)",
           styles),
        _b("✅ <b>Traçabilité totale</b> — chaque action est enregistrée",
           styles),
        _b("✅ <b>Sécurité</b> — bcrypt + backups AES-256", styles),
        _b("✅ <b>Permissions granulaires</b> par utilisateur", styles),

        Paragraph("Configuration minimale", styles["h2"]),
        _table(
            ["Élément", "Recommandation"],
            [
                ["Système",    "Windows 10/11, Linux, macOS"],
                ["RAM",        "2 Go minimum (4 Go recommandé)"],
                ["Disque",     "500 Mo + espace pour les factures"],
                ["Écran",      "1366 × 768 min (1920 × 1080 recommandé)"],
                ["Imprimante", "Thermique 80 mm ou A4"],
            ],
            col_widths=[4 * cm, 12 * cm],
        ),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 2 — Démarrage et connexion
# ══════════════════════════════════════════════════════════════════
def _build_s2(styles: dict) -> list:
    return [
        Paragraph("2. Démarrage et connexion", styles["h1"]),

        Paragraph("Premier lancement", styles["h2"]),
        _p("Au tout premier démarrage, un <b>assistant de configuration</b> "
           "(wizard) s'ouvre et vous demande :", styles),
        _b("<b>Nom de la pharmacie</b>", styles),
        _b("<b>Type</b> (Petite / Moyenne / Grande)", styles),
        _b("<b>Coordonnées</b> (téléphone, email, adresse)", styles),
        _b("<b>Logo</b> (facultatif — PNG ou JPG)", styles),
        _b("<b>Compte propriétaire</b> (nom, identifiant, mot de passe)",
           styles),
        _p("Une fois terminé, l'application bascule sur l'écran de "
           "connexion.", styles),

        Paragraph("Écran de connexion", styles["h2"]),
        _p("Saisissez votre <b>identifiant ou email</b>, puis votre "
           "<b>mot de passe</b>.", styles),
        _b("👁 <b>Afficher/masquer le mot de passe</b> (icône œil)", styles),
        _b("☑ <b>Se souvenir de moi</b> — pré-remplit l'identifiant", styles),
        _b("🔗 <b>Mot de passe oublié</b> — instructions de réinitialisation",
           styles),

        Paragraph("Sécurité anti-bruteforce", styles["h2"]),
        _box("⚠️ Après <b>5 tentatives échouées</b>, l'accès est verrouillé "
             "pendant <b>5 minutes</b>. Ce compteur est propre à chaque "
             "poste.", styles, bg=WARN_BG, border=WARN_FG),

        Paragraph("Changement de mot de passe forcé", styles["h2"]),
        _p("Si un administrateur a réinitialisé votre mot de passe, un "
           "dialogue de <b>changement obligatoire</b> apparaît à la "
           "première connexion. Vous devez :", styles),
        _b("Choisir un mot de passe de <b>8 caractères minimum</b>", styles),
        _b("Différent du mot de passe temporaire", styles),
        _b("Le confirmer", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 3 — Rôles et permissions
# ══════════════════════════════════════════════════════════════════
def _build_s3(styles: dict) -> list:
    return [
        Paragraph("3. Rôles et permissions", styles["h1"]),
        _p("Nova Pharma utilise <b>5 niveaux d'accès</b> :", styles),
        _table(
            ["Rôle", "Accès"],
            [
                ["DEVELOPER",   "Accès technique complet (console SQL, logs)"],
                ["OWNER",       "Propriétaire — tout sauf fonctions dev"],
                ["ADMIN",       "Administrateur — gestion complète"],
                ["UTILISATEUR", "Droits définis individuellement"],
                ["CAISSIER",    "Encaissement uniquement"],
            ],
            col_widths=[3.5 * cm, 12.5 * cm],
        ),

        Paragraph("Visibilité des pages par rôle", styles["h2"]),
        _table(
            ["Page", "ADMIN", "UTIL.", "CAISSIER"],
            [
                ["Accueil",       "✅", "❌", "❌"],
                ["Dashboard",     "✅", "❌", "❌"],
                ["Articles",      "✅", "❌", "❌"],
                ["Clients",       "✅", "❌", "❌"],
                ["Facturation",   "✅", "✅", "✅"],
                ["BLF",           "✅", "❌", "❌"],
                ["Historique",    "✅", "❌", "❌"],
                ["Alertes",       "✅", "❌", "❌"],
                ["Rapports",      "✅", "❌", "❌"],
                ["Audit",         "OWNER/DEV", "❌", "❌"],
                ["Utilisateurs",  "✅", "❌", "❌"],
                ["Paramètres",    "✅", "❌", "❌"],
                ["Surveillance",  "OWNER/DEV", "❌", "❌"],
            ],
            col_widths=[6 * cm, 3.5 * cm, 3 * cm, 3.5 * cm],
        ),

        Paragraph("Permissions granulaires", styles["h2"]),
        _p("En plus du rôle, chaque utilisateur dispose de <b>permissions "
           "précises</b> organisées par catégorie : Dashboard, Produits, "
           "Clients, Facturation, BLF, Fournisseurs, Rapports, "
           "Utilisateurs, Système.", styles),
        _p("Un utilisateur avec le rôle <b>UTILISATEUR</b> peut donc avoir :",
           styles),
        _b("✅ Voir les produits et les clients", styles),
        _b("✅ Faire des ventes", styles),
        _b("❌ Modifier le stock", styles),
        _b("❌ Supprimer un produit", styles),
        _p("Les permissions sont gérées par le propriétaire ou un admin "
           "depuis la page <b>Utilisateurs</b>.", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 4 — Page d'accueil
# ══════════════════════════════════════════════════════════════════
def _build_s4(styles: dict) -> list:
    return [
        Paragraph("4. Page d'accueil", styles["h1"]),
        _p("La page d'accueil donne un <b>aperçu instantané</b> de "
           "l'activité.", styles),

        Paragraph("Hero — Chiffre d'affaires", styles["h2"]),
        _b("CA total sur la période sélectionnée (grand format)", styles),
        _b("Tendance vs même période N-1 (↑ / ↓ %)", styles),

        Paragraph("Sélecteur de période", styles["h2"]),
        _p("3 boutons : <b>Semaine / Mois / Année</b>", styles),

        Paragraph("4 KPI cards", styles["h2"]),
        _table(
            ["KPI", "Description"],
            [
                ["Ventes",       "Nombre de factures distinctes"],
                ["Panier moyen", "CA ÷ nombre de ventes"],
                ["Clients",      "Clients distincts servis"],
                ["Ruptures",     "Produits avec stock ≤ seuil"],
            ],
            col_widths=[5 * cm, 11 * cm],
        ),

        Paragraph("Top 5 produits", styles["h2"]),
        _p("Classement par CA avec barres de progression.", styles),

        Paragraph("Alertes", styles["h2"]),
        _b("🔴 Ruptures de stock", styles),
        _b("🟠 Ventes annulées récentes", styles),
        _b("🟠 Sauvegardes manquantes ou anciennes", styles),

        Paragraph("Bandeau secondaire", styles["h2"]),
        _b("Valeur totale du stock", styles),
        _b("Marge globale de la période", styles),
        _b("Nombre d'annulations", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 5 — Dashboard
# ══════════════════════════════════════════════════════════════════
def _build_s5(styles: dict) -> list:
    return [
        Paragraph("5. Tableau de bord et graphiques", styles["h1"]),
        _p("Le <b>Dashboard</b> affiche une série de graphiques interactifs :",
           styles),
        _b("📈 <b>Revenus 7 derniers jours</b> (courbe)", styles),
        _b("📊 <b>CA mensuel</b> (12 derniers mois)", styles),
        _b("🥧 <b>Répartition anonymes vs identifiés</b>", styles),
        _b("🏆 <b>Top 10 médicaments</b> (par quantité vendue)", styles),
        _b("🍩 <b>Répartition par catégorie</b> (donut)", styles),
        _b("📅 <b>Comparaison annuelle</b> (N vs N-1)", styles),
        _b("⏰ <b>Activité horaire</b> (CA par heure)", styles),
        _b("📉 <b>Ventes quotidiennes</b> (30 derniers jours)", styles),
        _b("👥 <b>Top 10 clients</b> (CA cumulé)", styles),
        _b("🆕 <b>Nouveaux clients</b> (6 derniers mois)", styles),
        _b("⚠️ <b>Produits en rupture</b>", styles),
        _p("Un bouton <b>« Voir tous les graphiques »</b> ouvre une vue "
           "plein écran.", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 6 — Articles
# ══════════════════════════════════════════════════════════════════
def _build_s6(styles: dict) -> list:
    return [
        Paragraph("6. Gestion des articles (produits)", styles["h1"]),

        Paragraph("Ajouter un produit", styles["h2"]),
        _p("<b>Articles → Ajouter un article</b>", styles),
        _p("Le formulaire guide la saisie avec :", styles),
        _b("<b>Code référence</b> auto-généré (<code>MED-00001</code>)", styles),
        _b("<b>Nom</b> (compteur de caractères)", styles),
        _b("<b>Code-barre</b> (aperçu visuel instantané)", styles),
        _b("<b>Catégorie</b> (liste déroulante)", styles),
        _b("<b>Unité</b> (pièce, boîte, flacon, sachet…)", styles),
        _b("<b>Quantité initiale</b>", styles),
        _b("<b>Prix d'achat</b> et <b>prix de vente</b>", styles),
        _p("Une <b>checklist latérale</b> affiche la progression (0–100 %). "
           "Le calcul auto du prix de vente utilise la marge configurée "
           "(30 % par défaut), désactivable.", styles),

        Paragraph("Modifier un produit", styles["h2"]),
        _p("Sélectionnez un produit → bouton <b>Modifier</b> (ou double-clic).",
           styles),
        _b("Nom, code-barre, catégorie, unité, description", styles),
        _b("Prix d'achat / prix de vente (recalcul de la marge)", styles),
        _b("<b>Quantité en stock</b> — avec <b>motif obligatoire</b>",
           styles),
        _p("L'historique des <b>10 derniers ajustements</b> est affiché en "
           "bas du dialogue.", styles),

        Paragraph("Rechercher un produit", styles["h2"]),
        _b("<b>Barre rapide</b> dans le header (nom ou code)", styles),
        _b("<b>Barre dédiée</b> sur la page Articles", styles),
        _b("Filtre <b>« Voir ruptures »</b> (produits sous le seuil)", styles),

        Paragraph("Codes couleur stock", styles["h2"]),
        _table(
            ["Couleur", "Signification"],
            [
                ["🟢 Vert",   "Stock > 50 unités"],
                ["🟠 Orange", "Stock entre 21 et 50"],
                ["🔴 Rouge",  "Stock ≤ 20 (rupture)"],
            ],
            col_widths=[4 * cm, 12 * cm],
        ),

        Paragraph("Supprimer un produit", styles["h2"]),
        _p("Sélectionnez → <b>Supprimer</b>. Le produit est <b>masqué</b> "
           "(soft delete) mais reste dans l'historique des ventes. Action "
           "réversible par un admin.", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 7 — Clients
# ══════════════════════════════════════════════════════════════════
def _build_s7(styles: dict) -> list:
    return [
        Paragraph("7. Gestion des clients", styles["h1"]),

        Paragraph("Créer un client", styles["h2"]),
        _p("<b>Clients → Nouveau client</b>", styles),
        _b("<b>Nom</b> (2 à 120 caractères)", styles),
        _b("<b>Numéro</b> — format <code>+243XXXXXXXXX</code> ou "
           "<code>0XXXXXXXXX</code>", styles),
        _b("<b>Email</b> (facultatif)", styles),
        _b("<b>Adresse</b> (facultatif)", styles),
        _b("<b>Notes</b> (facultatif)", styles),
        _box("<b>Mode client anonyme</b> — cochez la case pour masquer les "
             "champs nom/numéro. Identifiant auto : "
             "<code>ANON-YYYYMMDD-XXXX</code>.", styles),

        Paragraph("Fiche client", styles["h2"]),
        _p("Double-cliquez sur un client pour ouvrir sa fiche complète :",
           styles),
        _b("<b>Avatar</b> (initiales ou photo)", styles),
        _b("<b>Badge de statut</b> (ACTIF / INACTIF / ANONYME)", styles),
        _b("<b>3 cartes stats</b> : Total acheté / Visites / Dernière visite",
           styles),
        _b("<b>Coordonnées complètes</b>", styles),
        _b("<b>Historique des achats</b> (tableau complet)", styles),

        Paragraph("Modifier / Supprimer", styles["h2"]),
        _b("<b>Modifier</b> → formulaire pré-rempli", styles),
        _b("<b>Supprimer</b> : sans achat → suppression définitive ; "
           "avec achats → désactivation (soft delete)", styles),
        _box("⚠️ Seul un <b>ADMIN</b> peut supprimer un client.",
             styles, bg=WARN_BG, border=WARN_FG),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 8 — Facturation
# ══════════════════════════════════════════════════════════════════
def _build_s8(styles: dict) -> list:
    return [
        Paragraph("8. Facturation", styles["h1"]),
        _p("C'est le cœur de l'application — la page la plus utilisée au "
           "comptoir.", styles),

        Paragraph("Créer une facture", styles["h2"]),

        Paragraph("1. Client (facultatif)", styles["h3"]),
        _b("Saisissez le <b>numéro de téléphone</b>", styles),
        _b("🟢 <b>Client identifié</b> → nom affiché automatiquement", styles),
        _b("🟠 <b>Numéro inconnu</b> → bouton « Créer ce client » proposé",
           styles),
        _b("🔴 <b>Format invalide</b> → message d'aide", styles),
        _b("Champ <b>vide</b> → vente anonyme", styles),

        Paragraph("2. Ajouter des articles", styles["h3"]),
        _b("Saisissez le nom dans la barre de recherche", styles),
        _b("Sélectionnez la quantité", styles),
        _b("Cliquez sur <b>Ajouter au panier</b>", styles),
        _b("Ajustez les quantités dans le tableau si besoin", styles),

        Paragraph("3. Vérification", styles["h3"]),
        _b("Total général affiché en temps réel", styles),
        _b("Nombre total d'articles", styles),

        Paragraph("4. Impression", styles["h3"]),
        _b("Cliquez sur <b>Imprimer la facture</b>", styles),
        _b("PDF généré dans <code>Factures/&lt;nom_client&gt;/</code>", styles),
        _b("Si impression auto activée → envoi direct à l'imprimante", styles),

        Paragraph("Détail du calcul", styles["h2"]),
        _b("Chaque ligne : <code>Quantité × Prix_unitaire</code>", styles),
        _b("Le <b>stock est décrémenté automatiquement</b>", styles),
        _b("Un <b>mouvement de stock</b> est tracé (SORTIE)", styles),
        _b("Le <b>montant total du client</b> est mis à jour", styles),

        Paragraph("Annuler une vente", styles["h2"]),
        _p("Réservé aux <b>ADMIN / OWNER / DEVELOPER</b>.", styles),
        _p("<b>Historique → double-clic → Annuler la vente</b>", styles),
        _b("Choisir un <b>motif</b> obligatoire", styles),
        _b("Confirmer", styles),
        _b("Effets : vente annulée + <b>stock restitué</b> + "
           "<b>montant client diminué</b> + audit", styles),

        Paragraph("Réimprimer une facture", styles["h2"]),
        _p("<b>Historique → clic droit → Réimprimer (PDF)</b>", styles),
        _p("La mention <b>« VENTE ANNULÉE »</b> apparaît sur les factures "
           "annulées.", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 9 — BLF
# ══════════════════════════════════════════════════════════════════
def _build_s9(styles: dict) -> list:
    return [
        Paragraph("9. Bons de livraison fournisseur (BLF)", styles["h1"]),
        _p("Le BLF enregistre une <b>réception de marchandises</b> d'un "
           "fournisseur.", styles),

        Paragraph("Cycle de vie", styles["h2"]),
        _p("<b>BROUILLON</b> ──[valider]──> <b>VALIDÉE</b> ──[annuler]──> "
           "<b>ANNULÉE</b>", styles),
        _p("Un brouillon peut être supprimé définitivement.", styles),

        Paragraph("Créer un BLF", styles["h2"]),
        _p("<b>BLF → Nouveau BLF</b>", styles),
        _b("<b>Fournisseur</b> (facultatif — « Sans fournisseur »)", styles),
        _b("<b>Notes</b> et <b>référence externe</b> (facultatif)", styles),
        _b("<b>Produits reçus</b> — ajustez Qté, Prix achat, Prix vente",
           styles),
        _b("<b>Total</b> calculé en direct", styles),
        _b("Deux boutons : <b>Enregistrer en brouillon</b> ou "
           "<b>Valider immédiatement</b>", styles),

        Paragraph("Valider un brouillon", styles["h2"]),
        _p("Ouvrez le BLF → bouton <b>Valider</b>. Le stock est <b>augmenté</b> "
           "pour chaque produit. Les prix sont mis à jour.", styles),

        Paragraph("Annuler un BLF validé", styles["h2"]),
        _p("Ouvrez le BLF → <b>Annuler</b>. Un <b>motif est obligatoire</b>. "
           "Le stock est <b>restitué</b> et un ajustement est tracé.", styles),

        Paragraph("Numérotation automatique", styles["h2"]),
        _p("Format : <code>BLF-YYYY-NNNNNNNNN</code>", styles),

        Paragraph("Créer un nouveau fournisseur", styles["h2"]),
        _p("<b>BLF → Nouveau fournisseur</b> — renseignez :", styles),
        _b("Raison sociale, catégorie", styles),
        _b("Responsable", styles),
        _b("Téléphone, email, adresse", styles),
        _p("L'identifiant est généré au format <code>FOU-0001</code>.", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 10 — Historique
# ══════════════════════════════════════════════════════════════════
def _build_s10(styles: dict) -> list:
    return [
        Paragraph("10. Historique des ventes et commandes", styles["h1"]),
        _p("<b>Historique</b> propose deux onglets :", styles),
        _b("<b>Ventes</b> (table <code>Historique</code>)", styles),
        _b("<b>Commandes fournisseurs</b> (table <code>Historique_commande</code>)",
           styles),

        Paragraph("Filtres disponibles", styles["h2"]),
        _b("<b>Période</b> : Aujourd'hui / 7j / 30j / 3 mois / Année / "
           "Personnalisé", styles),
        _b("<b>Recherche</b> : N° facture, article, client, code réf.", styles),
        _b("<b>Statut</b> : Toutes / Validées / Annulées", styles),

        Paragraph("Actions", styles["h2"]),
        _b("<b>Double-clic</b> → ouvre le détail de la facture", styles),
        _b("<b>Clic droit</b> → menu contextuel :", styles),
        _b("&nbsp;&nbsp;&nbsp;&nbsp;• Voir la facture", styles),
        _b("&nbsp;&nbsp;&nbsp;&nbsp;• Réimprimer (PDF)", styles),
        _b("&nbsp;&nbsp;&nbsp;&nbsp;• Annuler la vente (ADMIN/OWNER/DEV)",
           styles),
        _b("<b>Export CSV</b> — exporte toutes les lignes filtrées", styles),

        Paragraph("Détail d'une facture", styles["h2"]),
        _b("N° facture, date, client, caissier, statut", styles),
        _b("Tableau des lignes (article, quantité, PU, total)", styles),
        _b("<b>Total général</b>", styles),
        _b("Bouton <b>Réimprimer</b> (PDF)", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 11 — Alertes
# ══════════════════════════════════════════════════════════════════
def _build_s11(styles: dict) -> list:
    return [
        Paragraph("11. Alertes", styles["h1"]),
        _p("<b>Alertes</b> centralise tous les points d'attention :", styles),
        _table(
            ["Type", "Condition"],
            [
                ["🔴 Ruptures",        "Produits avec stock ≤ seuil"],
                ["🟠 Ventes annulées", "Annulations récentes (7 jours)"],
                ["🟠 Sauvegardes",     "Aucune ou > 7 jours"],
                ["🔵 Info",            "Notifications diverses"],
            ],
            col_widths=[4 * cm, 12 * cm],
        ),
        _p("Chaque alerte est une <b>carte colorée cliquable</b> qui renvoie "
           "vers la page concernée.", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 12 — Rapports
# ══════════════════════════════════════════════════════════════════
def _build_s12(styles: dict) -> list:
    return [
        Paragraph("12. Rapports et exports", styles["h1"]),
        _p("Trois rapports complets disponibles sur la page <b>Rapports</b>.",
           styles),

        Paragraph("Rapport Ventes", styles["h2"]),
        _b("CA total, nombre de ventes, panier moyen, clients, articles",
           styles),
        _b("<b>Comparaison automatique N-1</b>", styles),
        _b("<b>Top N produits</b> (par défaut 10)", styles),
        _b("<b>Répartition par catégorie</b> (donut)", styles),
        _b("<b>Évolution CA</b> (courbe)", styles),

        Paragraph("Rapport Équipe", styles["h2"]),
        _b("<b>Performance par vendeur</b> : ventes, CA, panier, part %",
           styles),
        _b("<b>Taux d'annulation par vendeur</b> (alerte si > 5 %)", styles),

        Paragraph("Rapport Opérations", styles["h2"]),
        _b("<b>Marges</b> : CA, coût, marge, taux par produit", styles),
        _b("<b>État du stock</b> : valeur totale, ruptures", styles),
        _b("<b>BLF</b> : nombre par statut", styles),
        _b("<b>Ajustements de stock</b>", styles),
        _b("<b>Annulations</b> (ventes + BLF)", styles),

        Paragraph("Périodes disponibles", styles["h2"]),
        _b("Aujourd'hui / Semaine / Mois / Année", styles),
        _b("30 derniers jours / 90 derniers jours", styles),
        _b("<b>Personnalisé</b> (dates au choix)", styles),

        Paragraph("Exports", styles["h2"]),
        _table(
            ["Format", "Contenu"],
            [
                ["PDF",   "Document structuré, KPIs + tableaux"],
                ["Excel", "Plusieurs feuilles : KPI, Top, Équipe, Marges"],
                ["CSV",   "Données brutes pour analyse externe"],
            ],
            col_widths=[3.5 * cm, 12.5 * cm],
        ),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 13 — Audit
# ══════════════════════════════════════════════════════════════════
def _build_s13(styles: dict) -> list:
    return [
        Paragraph("13. Journal d'audit", styles["h1"]),
        _box("Accès réservé aux <b>OWNER</b> et <b>DEVELOPER</b>.",
             styles, bg=WARN_BG, border=WARN_FG),
        _p("Chaque action importante est enregistrée avec :", styles),
        _b("Date et heure précises", styles),
        _b("Utilisateur (nom + identifiant)", styles),
        _b("Action (ex : <code>CREATION_VENTE</code>)", styles),
        _b("Cible (type + ID + nom)", styles),
        _b("<b>Détails</b> (JSON)", styles),
        _b("<b>État avant / après</b> (snapshot)", styles),
        _b("<b>Machine</b> et <b>adresse IP</b>", styles),
        _b("<b>Sévérité</b> (info / warning / danger)", styles),

        Paragraph("Chaîne anti-falsification", styles["h2"]),
        _p("Chaque entrée contient un <b>hash SHA-256</b> calculé à partir "
           "de l'entrée précédente + contenu. Toute modification manuelle "
           "de la base rompt la chaîne → <b>détection garantie de fraude</b>.",
           styles),

        Paragraph("Filtres disponibles", styles["h2"]),
        _b("Recherche libre", styles),
        _b("Action spécifique", styles),
        _b("Plage de dates", styles),
        _b("Pagination (50 entrées par page)", styles),

        Paragraph("Export & détail", styles["h2"]),
        _b("<b>Export CSV</b> de toutes les entrées filtrées", styles),
        _b("<b>Double-clic</b> → fiche complète avec détails JSON, "
           "avant / après", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 14 — Utilisateurs
# ══════════════════════════════════════════════════════════════════
def _build_s14(styles: dict) -> list:
    return [
        Paragraph("14. Gestion des utilisateurs", styles["h1"]),
        _p("Accès <b>ADMIN / OWNER / DEVELOPER</b>.", styles),

        Paragraph("Liste des utilisateurs", styles["h2"]),
        _p("Colonnes : Utilisateur, Email, Téléphone, Rôle, Statut, "
           "Dernière connexion.", styles),
        _p("Une <b>icône couronne 👑</b> signale le propriétaire, une "
           "<b>icône clé 🔧</b> le développeur.", styles),

        Paragraph("Créer un utilisateur", styles["h2"]),
        _p("<b>Nouvel utilisateur</b> — renseignez :", styles),
        _b("Prénom, Nom, Post-nom", styles),
        _b("Sexe, Date de naissance, Nationalité", styles),
        _b("Email, Téléphone", styles),
        _b("<b>Rôle</b> (UTILISATEUR / CAISSIER / ADMIN)", styles),
        _b("<b>Permissions granulaires</b> par catégorie", styles),
        _b("<b>Mot de passe</b> (génération auto possible)", styles),
        _b("Option <b>« Doit changer le mot de passe »</b>", styles),

        Paragraph("Fiche utilisateur", styles["h2"]),
        _b("Avatar + nom + email", styles),
        _b("Badges rôle et statut", styles),
        _b("Coordonnées complètes", styles),
        _b("<b>Permissions actives</b> (icônes ✓/✗)", styles),
        _b("<b>Historique des actions</b> (50 dernières)", styles),

        Paragraph("Actions", styles["h2"]),
        _b("<b>Modifier</b> → formulaire pré-rempli", styles),
        _b("<b>Réinitialiser le mot de passe</b> → mot de passe temporaire "
           "+ <b>QR code</b>", styles),
        _b("<b>Activer / Désactiver</b>", styles),

        Paragraph("Restrictions", styles["h2"]),
        _b("❌ On ne peut <b>pas modifier</b> le compte PROPRIÉTAIRE sans droits",
           styles),
        _b("❌ Impossible de désactiver un compte propriétaire sans droits",
           styles),
        _b("✅ <b>Un seul OWNER</b> et <b>un seul DEVELOPER</b> autorisés",
           styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 15 — Paramètres
# ══════════════════════════════════════════════════════════════════
def _build_s15(styles: dict) -> list:
    return [
        Paragraph("15. Paramètres", styles["h1"]),
        _p("<b>6 onglets + 1 onglet dynamique Réseau.</b>", styles),

        Paragraph("🏢 Entreprise", styles["h2"]),
        _b("Nom, type, téléphone, email, adresse", styles),
        _b("<b>Logo</b> (upload/suppression)", styles),

        Paragraph("💰 Vente", styles["h2"]),
        _b("Devise (FC, USD, EUR…)", styles),
        _b("Période du chiffre d'affaires (Mois / Semaine)", styles),
        _b("Marge bénéfice par défaut (%)", styles),
        _b("Numéro de caisse", styles),

        Paragraph("🧾 Facturation", styles["h2"]),
        _b("Impression automatique (oui/non)", styles),
        _b("QR code sur les factures", styles),
        _b("<b>Mentions du ticket</b> (une par ligne)", styles),

        Paragraph("💾 Sauvegarde", styles["h2"]),
        _b("Sauvegarde automatique (oui/non)", styles),
        _b("Fréquence (jours) + nombre d'archives", styles),
        _b("<b>Dossier principal</b> de sauvegarde", styles),
        _b("<b>Dossier secondaire</b> (USB / NAS / réseau)", styles),
        _b("Bouton <b>Gestionnaire des archives</b>", styles),

        Paragraph("🔒 Sécurité", styles["h2"]),
        _b("Longueur minimum du mot de passe", styles),
        _b("Expiration (jours)", styles),
        _b("Exigences : chiffre, majuscule, caractère spécial", styles),
        _b("<b>Seuil d'alerte stock</b>", styles),

        Paragraph("🖨 Impression", styles["h2"]),
        _b("Liste des imprimantes détectées", styles),
        _b("Imprimante par défaut", styles),
        _b("Impression auto + Ouverture PDF auto", styles),
        _b("Bouton <b>Tester l'impression</b>", styles),

        Paragraph("🌐 Réseau (dynamique)", styles["h2"]),
        _p("Voir la section 17 — Modes d'installation.", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 16 — Surveillance
# ══════════════════════════════════════════════════════════════════
def _build_s16(styles: dict) -> list:
    return [
        Paragraph("16. Surveillance (OWNER / DEVELOPER)", styles["h1"]),
        _box("Accès réservé — page spéciale de contrôle.",
             styles, bg=WARN_BG, border=WARN_FG),

        Paragraph("KPIs affichés", styles["h2"]),
        _table(
            ["KPI", "Description"],
            [
                ["Total actions (24h)", "Nombre d'entrées d'audit"],
                ["Alertes",             "Nombre de warning + danger"],
                ["Critiques",           "Nombre de danger uniquement"],
                ["État de la chaîne",   "✓ OK / ✗ RUPTURE"],
            ],
            col_widths=[5 * cm, 11 * cm],
        ),

        Paragraph("Vérification de la chaîne d'audit", styles["h2"]),
        _p("Bouton <b>🔒 Vérifier l'intégrité</b> — calcule tous les hashs "
           "et détecte toute falsification.", styles),
        _b("✅ Si OK → message de confirmation", styles),
        _b("🚨 Si rupture → <b>ALERTE FRAUDE</b> avec entrée corrompue",
           styles),

        Paragraph("Liste temps réel", styles["h2"]),
        _p("Table des dernières actions : date, utilisateur, sévérité, "
           "action, cible, IP. Double-clic → détail complet.", styles),

        Paragraph("Mode Développeur", styles["h2"]),
        _p("Accessible uniquement au <b>DEVELOPER</b> :", styles),
        _b("Infos système (DB, version, machine ID)", styles),
        _b("<b>Logs récents</b>", styles),
        _b("<b>Console SQL en lecture seule</b> (SELECT uniquement)", styles),
        _b("Statistiques par table", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 17 — Modes d'installation
# ══════════════════════════════════════════════════════════════════
def _build_s17(styles: dict) -> list:
    return [
        Paragraph("17. Modes d'installation", styles["h1"]),
        _p("Nova Pharma peut fonctionner selon <b>3 modes</b> :", styles),

        Paragraph("🖥 Mode Autonome (par défaut)", styles["h2"]),
        _b("1 seul poste", styles),
        _b("Base de données locale", styles),
        _b("Aucun partage réseau", styles),
        _p("<b>Usage :</b> petite pharmacie avec une seule caisse.", styles),

        Paragraph("🌐 Mode Serveur", styles["h2"]),
        _b("Un poste héberge la base <b>et</b> lance le serveur FastAPI", styles),
        _b("Les autres postes se connectent en réseau local", styles),
        _b("<b>Le serveur doit être allumé</b> pour les clients", styles),
        _p("<b>Commande :</b> <code>python run_server.py</code>", styles),
        _b("Écoute par défaut sur <code>0.0.0.0:5001</code>", styles),
        _b("Plage horaire paramétrable (refus hors plage)", styles),
        _b("Authentification par <b>token HMAC</b> (365 jours)", styles),

        Paragraph("💻 Mode Client", styles["h2"]),
        _b("Se connecte à un serveur distant", styles),
        _b("Saisissez l'<b>IP</b> et le <b>port</b>", styles),
        _b("Bouton <b>Tester la connexion</b>", styles),
        _p("<b>Usage :</b> plusieurs caisses dans une pharmacie.", styles),

        Paragraph("Configuration du mode", styles["h2"]),
        _p("<b>Paramètres → onglet Réseau → Configurer le réseau</b>", styles),
        _b("<b>Rôle</b> : Serveur principal / Client", styles),
        _b("<b>IP</b> + <b>Port</b> du serveur (si mode client)", styles),
        _b("<b>Plage horaire</b> d'ouverture", styles),
        _box("⚠️ Un <b>redémarrage de l'application</b> est requis après "
             "tout changement de mode.", styles, bg=WARN_BG, border=WARN_FG),

        Paragraph("Badge d'état serveur", styles["h2"]),
        _b("🟢 <b>Serveur connecté</b>", styles),
        _b("🔴 <b>Serveur injoignable</b> (vérifié toutes les 30 s)", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 18 — Sauvegardes
# ══════════════════════════════════════════════════════════════════
def _build_s18(styles: dict) -> list:
    return [
        Paragraph("18. Sauvegardes et restauration", styles["h1"]),

        Paragraph("Sauvegardes automatiques", styles["h2"]),
        _p("Si activées, sauvegarde selon la politique de rétention :", styles),
        _table(
            ["Type", "Fréquence", "Conservées"],
            [
                ["Quotidienne",  "1×/jour",    "7 dernières"],
                ["Hebdomadaire", "1×/semaine", "4 dernières"],
                ["Mensuelle",    "1×/mois",    "12 dernières"],
                ["Annuelle",     "1×/an",      "5 dernières"],
            ],
            col_widths=[4 * cm, 4 * cm, 8 * cm],
        ),

        Paragraph("Sauvegarde manuelle", styles["h2"]),
        _p("<b>Fichier → Sauvegarder maintenant</b> ou <b>Gestionnaire des "
           "archives → Nouvelle sauvegarde</b>", styles),
        _p("Format : archive <b>ZIP chiffrée AES-256</b> avec :", styles),
        _b("Mot de passe <b>dérivé de l'empreinte machine</b>", styles),
        _b("Hash SHA-256 de vérification", styles),
        _b("Enregistrement dans la table <code>Sauvegarde</code>", styles),

        Paragraph("Gestionnaire d'archives", styles["h2"]),
        _p("<b>Paramètres → Sauvegarde → Gestionnaire des archives</b>",
           styles),
        _b("📦 Créer une sauvegarde manuelle", styles),
        _b("👁 Ouvrir une archive en lecture seule", styles),
        _b("🗑 Supprimer une archive (avec confirmation)", styles),

        Paragraph("Restauration", styles["h2"]),
        _p("<b>Fichier → Restaurer une sauvegarde</b>", styles),
        _b("Sélectionner l'archive ZIP", styles),
        _b("Saisir le mot de passe (pré-rempli si même machine)", styles),
        _b("<b>Double confirmation</b> : cocher + taper <code>RESTAURER</code>",
           styles),
        _b("<b>Sauvegarde de sécurité</b> créée avant remplacement", styles),
        _b("L'application se ferme → redémarrage manuel requis", styles),
        _box("⚠️ Le mot de passe est dérivé de la machine. Une archive ne "
             "peut être restaurée que sur la machine qui l'a créée "
             "(protection anti-vol).", styles, bg=DANGER_BG, border=DANGER_FG),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 19 — FAQ
# ══════════════════════════════════════════════════════════════════
def _build_s19(styles: dict) -> list:
    return [
        Paragraph("19. Questions fréquentes", styles["h1"]),

        Paragraph("J'ai oublié mon mot de passe", styles["h3"]),
        _p("Contactez un <b>administrateur</b> ou le <b>propriétaire</b>. "
           "Il peut réinitialiser votre mot de passe depuis "
           "<b>Utilisateurs → Réinitialiser</b>, ce qui génère un mot de "
           "passe temporaire (avec QR code) à changer à la prochaine "
           "connexion.", styles),

        Paragraph("Le stock est faux", styles["h3"]),
        _p("Consultez <b>Articles → double-clic sur le produit</b> pour voir "
           "l'historique des 10 derniers ajustements.", styles),

        Paragraph("Comment sauvegarder mes données ?", styles["h3"]),
        _p("Sauvegardes automatiques si activées. Manuel : "
           "<b>Fichier → Sauvegarder maintenant</b>.", styles),

        Paragraph("L'imprimante ne fonctionne pas", styles["h3"]),
        _b("Vérifiez qu'elle est connectée et par défaut", styles),
        _b("<b>Paramètres → Impression → Tester l'impression</b>", styles),
        _b("Vérifiez la sélection dans la liste déroulante", styles),

        Paragraph("Je vois des alertes mais je ne les comprends pas",
                  styles["h3"]),
        _p("Les alertes sont documentées dans la section 11. Cliquez sur "
           "une carte pour accéder directement au problème.", styles),

        Paragraph("Comment ajouter un nouveau caissier ?", styles["h3"]),
        _p("<b>Utilisateurs → Nouvel utilisateur</b> → rôle = "
           "<b>CAISSIER</b>.", styles),

        Paragraph("Un client a un mauvais numéro", styles["h3"]),
        _p("<b>Clients → double-clic → Modifier</b>. Le changement est tracé.",
           styles),

        Paragraph("Comment annuler une vente ?", styles["h3"]),
        _p("<b>Historique → double-clic → Annuler</b>. Réservé "
           "ADMIN/OWNER/DEV. Motif obligatoire.", styles),

        Paragraph("Puis-je utiliser Nova Pharma sur plusieurs postes ?",
                  styles["h3"]),
        _p("Oui, en <b>mode serveur/client</b>. Voir la section 17.", styles),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 20 — Dépannage
# ══════════════════════════════════════════════════════════════════
def _build_s20(styles: dict) -> list:
    return [
        Paragraph("20. Dépannage", styles["h1"]),

        Paragraph("L'application ne démarre pas", styles["h3"]),
        _b("Vérifiez que la base existe : <code>Database/NovaPharma.db</code>",
           styles),
        _b("Consultez les logs dans le terminal", styles),
        _b("En cas de corruption, restaurez une sauvegarde récente", styles),

        Paragraph("« Serveur injoignable » en mode client", styles["h3"]),
        _b("Vérifiez que le serveur est allumé", styles),
        _b("Testez la connexion depuis <b>Paramètres → Réseau</b>", styles),
        _b("Vérifiez que le port <b>5001</b> n'est pas bloqué par le pare-feu",
           styles),
        _b("Vérifiez la <b>plage horaire</b> configurée sur le serveur", styles),

        Paragraph("Un produit n'apparaît pas dans la facturation",
                  styles["h3"]),
        _b("Vérifiez qu'il est <b>actif</b> (<code>actif = 1</code>)", styles),
        _b("Vérifiez l'orthographe exacte du nom", styles),

        Paragraph("« Mot de passe incorrect » alors que je suis sûr",
                  styles["h3"]),
        _b("Vérifiez que <b>Verr. Maj</b> n'est pas activé", styles),
        _b("L'identifiant est insensible à la casse, "
           "<b>mais pas le mot de passe</b>", styles),
        _b("Après 5 échecs, attendez 5 minutes", styles),

        Paragraph("Le chiffre d'affaires semble faux", styles["h3"]),
        _b("Vérifiez que les ventes <b>annulées</b> ne sont pas comptées",
           styles),
        _b("Vérifiez la <b>période sélectionnée</b>", styles),
        _b("Vérifiez le <b>format des dates</b> (DD/MM/YYYY)", styles),

        Paragraph("La chaîne d'audit est rompue", styles["h3"]),
        _box("🚨 <b>Ne touchez plus à rien.</b> Une rupture signifie qu'une "
             "entrée a été modifiée manuellement dans la base. Contactez "
             "immédiatement le <b>développeur</b> avec le message d'erreur "
             "exact (numéro d'entrée et ID fournis).",
             styles, bg=DANGER_BG, border=DANGER_FG),
        PageBreak(),
    ]


# ══════════════════════════════════════════════════════════════════
# SECTION 21 — Contact
# ══════════════════════════════════════════════════════════════════
def _build_s21(styles: dict) -> list:
    return [
        Paragraph("21. Support et contact", styles["h1"]),
        _p("<b>Support technique Nova Pharma</b>", styles),
        _table(
            ["Canal", "Coordonnées"],
            [
                ["📧 Email",     "teamnovaoff@gmail.com"],
                ["📞 Téléphone", "08 XX XX XX XX"],
                ["🕐 Horaires",  "Lun – Ven, 08h00 – 18h00 (GMT+1)"],
                ["🌐 Site",      "www.novapharma.cd"],
            ],
            col_widths=[4 * cm, 12 * cm],
        ),
        Spacer(1, 0.8 * cm),
        _box("<b>Éditeur :</b> TEAM NOVA<br/>"
             f"<b>Version :</b> {APP_VERSION}<br/>"
             "<b>Licence :</b> Propriétaire — © 2026 TEAM NOVA.<br/>"
             "Tous droits réservés.", styles),
        Spacer(1, 1.5 * cm),
        _p(f"<i>Document généré le "
           f"{datetime.now().strftime('%d/%m/%Y à %H:%M')} — "
           f"Version {APP_VERSION}</i>", styles),
    ]


# ══════════════════════════════════════════════════════════════════
# Rendu des pages (header / footer / cover)
# ══════════════════════════════════════════════════════════════════
def _make_cover_painter():
    def _draw(canvas, document):
        canvas.saveState()
        canvas.setFillColor(PRIMARY)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setFillColor(CYAN)
        canvas.rect(0, 0, A4[0], 6 * cm, fill=1, stroke=0)
        canvas.restoreState()
    return _draw


def _make_page_painter():
    def _draw(canvas, document):
        canvas.saveState()

        # Header
        canvas.setFillColor(PRIMARY)
        canvas.rect(0, A4[1] - 1 * cm, A4[0], 1 * cm, fill=1, stroke=0)

        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(2 * cm, A4[1] - 0.7 * cm, "NOVA PHARMA")

        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(
            A4[0] - 2 * cm, A4[1] - 0.7 * cm,
            "Guide utilisateur")

        # Footer
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)

        canvas.setFillColor(GREY)
        canvas.setFont("Helvetica", 8)
        canvas.drawString(2 * cm, 1 * cm, f"Version {APP_VERSION}")
        canvas.drawRightString(
            A4[0] - 2 * cm, 1 * cm,
            f"Page {document.page}")

        canvas.restoreState()
    return _draw


# ══════════════════════════════════════════════════════════════════
# Générateur principal
# ══════════════════════════════════════════════════════════════════
def generer_guide(output_path: str = "Guide_utilisateur_NovaPharma.pdf"):
    """Génère le guide utilisateur PDF complet (~40 pages)."""
    logger.info("Génération du guide complet")
    styles = _make_styles()

    # ─── Nom de la pharmacie ───
    nom_pharmacie = "NOVA PHARMA"
    try:
        from Database import db
        db.get_conn()
        row = db.query_one(
            "SELECT nom FROM Pharmacie WHERE id = 1 LIMIT 1")
        if row and row["nom"]:
            nom_pharmacie = row["nom"]
    except Exception:
        pass

    # ─── Document ───
    doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=2.5 * cm,
        rightMargin=2.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Guide utilisateur — Nova Pharma",
        author="TEAM NOVA",
        subject="Documentation utilisateur",
    )

    frame_cover = Frame(
        0, 0, A4[0], A4[1],
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0, id="cover")

    frame_page = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0, id="page")

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame_cover],
                     onPage=_make_cover_painter()),
        PageTemplate(id="page", frames=[frame_page],
                     onPage=_make_page_painter()),
    ])

    # ─── Contenu ───
    elements = []

    # Couverture
    elements += _build_cover(styles, nom_pharmacie)
    elements.append(NextPageTemplate("page"))
    elements.append(PageBreak())

    # Sommaire
    elements += _build_sommaire(styles)

    # Sections 1 à 21
    elements += _build_s1(styles)
    elements += _build_s2(styles)
    elements += _build_s3(styles)
    elements += _build_s4(styles)
    elements += _build_s5(styles)
    elements += _build_s6(styles)
    elements += _build_s7(styles)
    elements += _build_s8(styles)
    elements += _build_s9(styles)
    elements += _build_s10(styles)
    elements += _build_s11(styles)
    elements += _build_s12(styles)
    elements += _build_s13(styles)
    elements += _build_s14(styles)
    elements += _build_s15(styles)
    elements += _build_s16(styles)
    elements += _build_s17(styles)
    elements += _build_s18(styles)
    elements += _build_s19(styles)
    elements += _build_s20(styles)
    elements += _build_s21(styles)

    # ─── Build ───
    doc.build(elements)
    logger.info("Guide généré : %s", output_path)
    print(f"✅ Guide complet généré : {output_path}")
    return output_path


# ══════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Génère le guide utilisateur PDF Nova Pharma")
    parser.add_argument(
        "--output", "-o",
        default="Guide_utilisateur_NovaPharma.pdf",
        help="Chemin de sortie du PDF")
    args = parser.parse_args()

    generer_guide(args.output)