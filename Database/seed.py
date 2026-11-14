"""
NovaPharma — Initialisation des données de base.

À exécuter UNE SEULE FOIS au premier lancement (ou si la table
Configuration est vide). Idempotent : ne réécrase rien.
"""

import secrets
import socket
from Database import db


# ==================================================================
# Textes de consentement (v1.0)
# ==================================================================
CONSENTEMENT_SAUVEGARDE_V1 = """
CONSENTEMENT À LA SAUVEGARDE DES DONNÉES

En cochant cette case, vous autorisez NovaPharma à sauvegarder
régulièrement les données de votre pharmacie (ventes, stocks,
utilisateurs, configuration) sur un support de votre choix.

Ces sauvegardes ont pour unique but :
  - de protéger vos données contre une perte accidentelle
  - de permettre leur restauration en cas d'incident

Vous restez propriétaire de vos données. Vous pouvez à tout
moment désactiver la sauvegarde automatique depuis les paramètres.
""".strip()

CONSENTEMENT_IA_V1 = """
CONSENTEMENT À L'UTILISATION ANONYMISÉE DES DONNÉES

En cochant cette case, vous autorisez l'utilisation de vos données
de vente, APRÈS ANONYMISATION COMPLÈTE, pour améliorer les modèles
d'aide à la décision de NovaPharma.

Anonymisation garantie :
  - Nom, téléphone et adresse des clients   : SUPPRIMÉS
  - Noms des utilisateurs                   : SUPPRIMÉS
  - Nom de votre pharmacie                  : SUPPRIMÉ
  - Localisation, adresse IP, identifiants  : SUPPRIMÉS
  - Heures et minutes des ventes            : ARRONDIES AU JOUR

Conservés après anonymisation :
  - Noms de produits vendus
  - Quantités, prix, dates (jour)
  - Catégories de produits

Cette autorisation est FACULTATIVE. Refuser n'empêche pas
l'utilisation normale de NovaPharma.

Vous pouvez retirer votre consentement à tout moment.
""".strip()

VERSION_SAUVEGARDE = "v2.0"
VERSION_IA         = "v2.0"
VERSION_CGU        = "v2.0"


# ==================================================================
# Valeurs par défaut de Configuration
# ==================================================================
DEFAULTS = [
    # Entreprise
    ("nom_entreprise",          "",           "str",   "Nom commercial de la pharmacie"),
    ("adresse_entreprise",      "",           "str",   "Adresse postale"),
    ("telephone_entreprise",    "",           "str",   "Téléphone de contact"),
    ("devise",                  "FC",         "str",   "Devise utilisée"),

    # Vente
    ("indice_vente",            "1.0",        "float", "Multiplicateur appliqué aux prix"),
    ("chiffre_affaire_periode", "Mois",       "str",   "Mois ou Semaine"),
    ("qrcode_actif",            "1",          "bool",  "Afficher un QR sur le ticket"),
    ("impression_facture_auto", "1",          "bool",  "Imprimer la facture automatiquement"),
    ("mentions_ticket",         "[]",         "json",  "Liste de mentions sur le ticket"),

    # Sécurité
    ("unique_key",              "",           "str",   "Clé HMAC pour signer les tickets"),

    # Installation
    ("first_time",              "1",          "bool",  "Wizard pas encore exécuté"),
    ("pc_name",                 "",           "str",   "Nom de la machine de configuration"),

    # Sauvegarde
    ("sauvegarde_active",              "0",  "bool", "Accord du client pour la sauvegarde"),
    ("sauvegarde_auto",                "1",  "bool", "Sauvegarde automatique activée"),
    ("sauvegarde_intervalle_jours",    "7",  "int",  "Fréquence en jours"),
    ("sauvegarde_max_conservees",      "10", "int",  "Nombre de sauvegardes à conserver"),
    ("sauvegarde_dossier",             "",   "str",  "Dossier de destination"),
    ("consentement_sauvegarde_version", VERSION_SAUVEGARDE, "str", "Version du texte accepté"),

    # IA anonymisée
    ("ia_consentement",         "0",   "bool", "Accord pour usage IA anonymisé"),
    ("ia_consentement_version", "",    "str",  "Version du texte accepté"),
    ("ia_derniere_export",      "",    "str",  "Date du dernier export"),
    ("consentement_ia_version", VERSION_IA, "str", "Version actuelle du texte IA"),
]


def run() -> None:
    """Initialise les données de base si nécessaire."""
    print("→ Initialisation de la base...")

    _seed_caisse()
    _seed_config()
    _seed_categories_par_defaut()

    print("✓ Base prête.")


def _seed_caisse() -> None:
    row = db.query_one("SELECT id FROM Caisse WHERE code = 'A'")
    if row:
        return
    db.execute(
        "INSERT INTO Caisse (id, code, libelle, active) VALUES (?,?,?,1)",
        (db.new_id(), "A", "Caisse principale")
    )
    print("  · Caisse 'A' créée")


def _seed_config() -> None:
    for cle, valeur, type_, description in DEFAULTS:
        # On ne réécrase PAS une valeur déjà présente
        existing = db.query_one("SELECT cle FROM Configuration WHERE cle = ?", (cle,))
        if existing:
            continue

        # Génération de la clé HMAC unique
        if cle == "unique_key" and not valeur:
            valeur = secrets.token_urlsafe(32)

        # Nom de la machine
        if cle == "pc_name" and not valeur:
            valeur = socket.gethostname()

        db.set_config(cle, valeur, type_=type_, description=description)

    print("  · Configuration initialisée")


def _seed_categories_par_defaut() -> None:
    """Catégories de départ — l'utilisateur pourra les modifier."""
    categories = [
        ("Antalgiques",       "Douleurs et fièvre"),
        ("Antibiotiques",     "Infections bactériennes"),
        ("Antipaludéens",     "Traitement du paludisme"),
        ("Vitamines",         "Compléments et vitamines"),
        ("Antiseptiques",     "Désinfection et plaies"),
        ("Matériel médical",  "Pansements, seringues, etc."),
        ("Divers",            "Non classé"),
    ]
    for nom, description in categories:
        existing = db.query_one("SELECT id FROM Categorie WHERE nom = ?", (nom,))
        if existing:
            continue
        db.execute(
            "INSERT INTO Categorie (id, nom, description) VALUES (?,?,?)",
            (db.new_id(), nom, description)
        )
    print("  · Catégories par défaut créées")


if __name__ == "__main__":
    run()