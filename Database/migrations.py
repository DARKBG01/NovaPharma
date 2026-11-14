"""
Migration — ajoute les nouvelles colonnes si elles n'existent pas.
Idempotent : peut être exécuté plusieurs fois sans danger.
"""

import logging

from Database import db

logger = logging.getLogger(__name__)


def migrate_produits():
    """Ajoute les colonnes V3 à `produits` si absentes."""
    existing = {row["name"] for row in db.query("PRAGMA table_info(produits)")}

    additions = [
        ("Code_barre",       "TEXT"),
        ("Description",      "TEXT"),
        ("Unite",            "TEXT NOT NULL DEFAULT 'pièce'"),
        ("Quantite_initiale","INTEGER NOT NULL DEFAULT 0"),
        ("Cree_par",         "TEXT"),
    ]

    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(f"ALTER TABLE produits ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : produits.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")


def migrate_produits_actif():
    """Ajoute la colonne `actif` à `produits` si absente."""
    existing = {row["name"] for row in db.query("PRAGMA table_info(produits)")}
    if "actif" in existing:
        return
    try:
        db.execute("ALTER TABLE produits ADD COLUMN actif INTEGER NOT NULL DEFAULT 1")
        print("  · Colonne ajoutée : produits.actif")
    except Exception as e:
        print(f"  ! Impossible d'ajouter actif : {e}")


def migrate_client():
    """Ajoute les colonnes manquantes à Client."""
    existing = {row["name"] for row in db.query("PRAGMA table_info(Client)")}
    additions = [
        ("C_name",        "TEXT"),
        ("Montant_total", "REAL NOT NULL DEFAULT 0"),
        ("Id_client",     "TEXT"),
        ("email",         "TEXT"),
        ("notes",         "TEXT"),
        ("actif",         "INTEGER NOT NULL DEFAULT 1"),
    ]
    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(f"ALTER TABLE Client ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : Client.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")


def migrate_facturation_config():
    """Ajoute les clés de configuration pour la facturation."""
    defaults = [
        ("facture_numero_caisse", "01", "str",
         "Code de la caisse utilisée pour les factures"),
        ("facture_numero_temoin", "1", "int",
         "Compteur séquentiel des factures"),
    ]
    for cle, valeur, type_, desc in defaults:
        existing = db.query_one(
            "SELECT 1 FROM Configuration WHERE cle = ? LIMIT 1", (cle,))
        if existing:
            continue
        db.set_config(cle, valeur, type_=type_, description=desc)
        print(f"  · Clé de config ajoutée : {cle} = {valeur}")

    # ─── MIGRATION : ancien "A" → "01" ───
    try:
        val = db.get_config("facture_numero_caisse", None)
        if val == "A":
            db.set_config("facture_numero_caisse", "01", type_="str")
            print("  · Migration caisse : 'A' → '01'")
    except Exception:
        pass


def migrate_blf():
    """Crée les tables BonLivraison + LigneBonLivraison."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS BonLivraison (
            id                  TEXT PRIMARY KEY,
            numero_blf          TEXT NOT NULL UNIQUE,
            fournisseur_id      TEXT,
            fournisseur_nom     TEXT,
            date_livraison      TEXT NOT NULL DEFAULT (datetime('now')),
            statut              TEXT NOT NULL DEFAULT 'BROUILLON'
                                CHECK(statut IN ('BROUILLON','VALIDEE','ANNULEE')),
            total_achat         REAL NOT NULL DEFAULT 0,
            nb_articles         INTEGER NOT NULL DEFAULT 0,
            nb_unites           INTEGER NOT NULL DEFAULT 0,
            notes               TEXT,
            reference_externe   TEXT,
            created_by          TEXT,
            created_by_name     TEXT,
            created_at          TEXT NOT NULL DEFAULT (datetime('now')),
            validated_by        TEXT,
            validated_by_name   TEXT,
            validated_at        TEXT,
            cancelled_by        TEXT,
            cancelled_by_name   TEXT,
            cancelled_at        TEXT,
            motif_annulation    TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS LigneBonLivraison (
            id                  TEXT PRIMARY KEY,
            blf_id              TEXT NOT NULL,
            produit_id          TEXT,
            produit_nom         TEXT NOT NULL,
            quantite            INTEGER NOT NULL CHECK(quantite > 0),
            prix_achat_unitaire REAL NOT NULL DEFAULT 0,
            prix_vente_unitaire REAL NOT NULL DEFAULT 0,
            total_ligne         REAL NOT NULL DEFAULT 0,
            stock_avant         INTEGER,
            stock_apres         INTEGER,
            FOREIGN KEY (blf_id)    REFERENCES BonLivraison(id) ON DELETE CASCADE,
            FOREIGN KEY (produit_id) REFERENCES produits(Code_reference)
                ON DELETE SET NULL
        )
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_blf_numero ON BonLivraison(numero_blf)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_blf_statut ON BonLivraison(statut)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_blf_date ON BonLivraison(date_livraison)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_blf_fourn ON BonLivraison(fournisseur_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_blf_ligne_blf ON LigneBonLivraison(blf_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_blf_ligne_produit ON LigneBonLivraison(produit_id)")


def migrate_blf_compteur():
    """Ajoute la clé de config pour le compteur BLF."""
    existing = db.query_one(
        "SELECT 1 FROM Configuration WHERE cle = 'blf_compteur' LIMIT 1")
    if existing:
        return
    db.set_config("blf_compteur", "1", type_="int",
                  description="Compteur séquentiel des BLF")


# ══════════════════════════════════════════════════════════════════
# PHASE 2 — Encaissement
# ══════════════════════════════════════════════════════════════════
def _apply_encaissement():
    """Crée la table Encaissement si absente."""
    try:
        if db.query("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='Encaissement'"):
            return

        db.execute("""
            CREATE TABLE IF NOT EXISTS Encaissement (
                id TEXT PRIMARY KEY,
                num_fact TEXT NOT NULL,
                montant_facture REAL NOT NULL,
                devise_paiement TEXT NOT NULL
                    CHECK(devise_paiement IN ('FC','USD')),
                taux_change REAL NOT NULL DEFAULT 2800.0,
                montant_recu REAL NOT NULL,
                montant_recu_fc REAL NOT NULL,
                montant_rendu REAL NOT NULL,
                devise_rendu TEXT NOT NULL DEFAULT 'FC'
                    CHECK(devise_rendu IN ('FC','USD')),
                utilisateur_id TEXT,
                utilisateur_name TEXT,
                date_encaissement TEXT NOT NULL DEFAULT (datetime('now')),
                notes TEXT,
                FOREIGN KEY (num_fact) REFERENCES Historique(Num_fact)
                    ON DELETE RESTRICT
            )""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_encaisse_facture "
                   "ON Encaissement(num_fact)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_encaisse_date "
                   "ON Encaissement(date_encaissement)")
        logger.info("Table Encaissement créée")
        print("  · Table Encaissement créée")
    except Exception:
        logger.exception("Erreur création Encaissement")


# ══════════════════════════════════════════════════════════════════
# PHASE C — Rapport Z
# ══════════════════════════════════════════════════════════════════
def _apply_rapport_z():
    """Crée la table RapportZ si absente."""
    try:
        if db.query("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='RapportZ'"):
            return

        db.execute("""
            CREATE TABLE IF NOT EXISTS RapportZ (
                id                TEXT PRIMARY KEY,
                numero_z          TEXT NOT NULL UNIQUE,
                caisse            TEXT NOT NULL,
                date_debut        TEXT NOT NULL,
                date_fin          TEXT NOT NULL,
                utilisateur_id    TEXT,
                utilisateur_name  TEXT,
                nb_factures       INTEGER NOT NULL DEFAULT 0,
                nb_articles       INTEGER NOT NULL DEFAULT 0,
                ca_total          REAL    NOT NULL DEFAULT 0,
                panier_moyen      REAL    NOT NULL DEFAULT 0,
                nb_clients_ident  INTEGER NOT NULL DEFAULT 0,
                nb_clients_anon   INTEGER NOT NULL DEFAULT 0,
                nb_annulations    INTEGER NOT NULL DEFAULT 0,
                montant_annule    REAL    NOT NULL DEFAULT 0,
                montant_compte    REAL    NOT NULL DEFAULT 0,
                ecart             REAL    NOT NULL DEFAULT 0,
                top_produits      TEXT,
                detail_heure      TEXT,
                format_pdf        TEXT NOT NULL DEFAULT 'ticket',
                chemin_pdf        TEXT,
                notes             TEXT,
                created_at        TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
                    ON DELETE SET NULL
            )""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_rapportz_caisse "
                   "ON RapportZ(caisse)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_rapportz_date "
                   "ON RapportZ(date_debut)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_rapportz_numero "
                   "ON RapportZ(numero_z)")
        logger.info("Table RapportZ créée")
        print("  · Table RapportZ créée")
    except Exception:
        logger.exception("Erreur création RapportZ")


# ══════════════════════════════════════════════════════════════════
# PHASE D — Retours
# ══════════════════════════════════════════════════════════════════
def _apply_retours():
    """Crée les tables RetourVente + LigneRetour si absentes."""
    try:
        if db.query("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='RetourVente'"):
            return

        db.execute("""
            CREATE TABLE IF NOT EXISTS RetourVente (
                id                TEXT PRIMARY KEY,
                numero_retour     TEXT NOT NULL UNIQUE,
                num_fact_origine  TEXT NOT NULL,
                utilisateur_id    TEXT,
                utilisateur_name  TEXT,
                client_name       TEXT,
                client_numero     TEXT,
                motif             TEXT NOT NULL,
                montant_total     REAL NOT NULL DEFAULT 0,
                statut            TEXT NOT NULL DEFAULT 'VALIDE'
                                  CHECK(statut IN ('BROUILLON','VALIDE','ANNULE')),
                notes             TEXT,
                date_retour       TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (num_fact_origine)
                    REFERENCES Historique(Num_fact)
                    ON DELETE RESTRICT
            )""")

        db.execute("""
            CREATE TABLE IF NOT EXISTS LigneRetour (
                id              TEXT PRIMARY KEY,
                retour_id       TEXT NOT NULL,
                code_reference  TEXT NOT NULL,
                article         TEXT NOT NULL,
                quantite        INTEGER NOT NULL CHECK(quantite > 0),
                prix_unitaire   REAL NOT NULL,
                total           REAL NOT NULL,
                reconditionne   INTEGER NOT NULL DEFAULT 1
                                CHECK(reconditionne IN (0,1)),
                FOREIGN KEY (retour_id) REFERENCES RetourVente(id)
                    ON DELETE CASCADE
            )""")

        db.execute("CREATE INDEX IF NOT EXISTS idx_retour_numero "
                   "ON RetourVente(numero_retour)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_retour_facture "
                   "ON RetourVente(num_fact_origine)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_retour_date "
                   "ON RetourVente(date_retour)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_retour_statut "
                   "ON RetourVente(statut)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_ligne_retour "
                   "ON LigneRetour(retour_id)")

        logger.info("Tables RetourVente + LigneRetour créées")
        print("  · Tables RetourVente + LigneRetour créées")
    except Exception:
        logger.exception("Erreur création Retours")

def _fix_encaissement_fk():
    """Recrée Encaissement sans FK vers Historique (Num_fact non-unique)."""
    try:
        # Vérifie si la table existe
        rows = db.query(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='Encaissement'")
        if not rows:
            return

        # Vérifie si la FK pose problème
        schema = db.query_one(
            "SELECT sql FROM sqlite_master "
            "WHERE type='table' AND name='Encaissement'")
        if not schema:
            return
        sql = schema["sql"] or ""
        if "FOREIGN KEY (num_fact)" not in sql:
            return  # déjà corrigée

        logger.info("Fix Encaissement : suppression FK cassée…")

        # a) Renomme l'ancienne
        db.execute("ALTER TABLE Encaissement RENAME TO Encaissement_old")

        # b) Recrée sans FK
        db.execute("""
            CREATE TABLE Encaissement (
                id TEXT PRIMARY KEY,
                num_fact TEXT NOT NULL,
                montant_facture REAL NOT NULL,
                devise_paiement TEXT NOT NULL
                    CHECK(devise_paiement IN ('FC','USD')),
                taux_change REAL NOT NULL DEFAULT 2800.0,
                montant_recu REAL NOT NULL,
                montant_recu_fc REAL NOT NULL,
                montant_rendu REAL NOT NULL,
                devise_rendu TEXT NOT NULL DEFAULT 'FC'
                    CHECK(devise_rendu IN ('FC','USD')),
                utilisateur_id TEXT,
                utilisateur_name TEXT,
                date_encaissement TEXT NOT NULL DEFAULT (datetime('now')),
                notes TEXT
            )""")

        # c) Copie les données existantes
        db.execute("""
            INSERT INTO Encaissement
            SELECT * FROM Encaissement_old
        """)

        # d) Drop l'ancienne
        db.execute("DROP TABLE Encaissement_old")

        # e) Recrée les index
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_encaisse_facture "
            "ON Encaissement(num_fact)")
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_encaisse_date "
            "ON Encaissement(date_encaissement)")

        logger.info("✅ Encaissement FK corrigée")
        print("  · Encaissement : FK cassée supprimée")

    except Exception:
        logger.exception("Erreur fix FK Encaissement")


def _fix_retour_fk():
    """Idem pour RetourVente → Historique."""
    try:
        schema = db.query_one(
            "SELECT sql FROM sqlite_master "
            "WHERE type='table' AND name='RetourVente'")
        if not schema:
            return
        sql = schema["sql"] or ""
        if "FOREIGN KEY (num_fact_origine)" not in sql:
            return

        logger.info("Fix RetourVente : suppression FK cassée…")

        db.execute("PRAGMA foreign_keys = OFF")
        db.execute("ALTER TABLE RetourVente RENAME TO RetourVente_old")

        db.execute("""
            CREATE TABLE RetourVente (
                id TEXT PRIMARY KEY,
                numero_retour TEXT NOT NULL UNIQUE,
                num_fact_origine TEXT NOT NULL,
                utilisateur_id TEXT,
                utilisateur_name TEXT,
                client_name TEXT,
                client_numero TEXT,
                motif TEXT NOT NULL,
                montant_total REAL NOT NULL DEFAULT 0,
                statut TEXT NOT NULL DEFAULT 'VALIDE'
                    CHECK(statut IN ('BROUILLON','VALIDE','ANNULE')),
                notes TEXT,
                date_retour TEXT NOT NULL DEFAULT (datetime('now'))
            )""")

        db.execute("""
            INSERT INTO RetourVente
            SELECT id, numero_retour, num_fact_origine,
                   utilisateur_id, utilisateur_name,
                   client_name, client_numero, motif,
                   montant_total, statut, notes, date_retour
            FROM RetourVente_old
        """)

        db.execute("DROP TABLE RetourVente_old")
        db.execute("PRAGMA foreign_keys = ON")

        logger.info("✅ RetourVente FK corrigée")
        print("  · RetourVente : FK cassée supprimée")

    except Exception:
        logger.exception("Erreur fix FK RetourVente")

def migrate_client_sexe():
    """Ajoute la colonne sexe à Client."""
    existing = {row["name"] for row in db.query("PRAGMA table_info(Client)")}
    if "sexe" in existing:
        return
    try:
        db.execute(
            "ALTER TABLE Client ADD COLUMN sexe TEXT "
            "CHECK(sexe IN ('M','F')) DEFAULT 'M'")
        logger.info("Colonne Client.sexe ajoutée")
        print("  · Colonne ajoutée : Client.sexe")
    except Exception as e:
        print(f"  ! Impossible d'ajouter Client.sexe : {e}")


def _apply_client_sexe_index():
    """Crée un index sur sexe (rapide pour stats)."""
    try:
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_client_sexe "
            "ON Client(sexe)")
    except Exception:
        pass

def _apply_client_sessions():
    """Table des sessions clients pour surveillance."""
    try:
        if db.query("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='ClientSession'"):
            return

        db.execute("""
            CREATE TABLE IF NOT EXISTS ClientSession (
                id              TEXT PRIMARY KEY,
                machine_id      TEXT NOT NULL UNIQUE,
                hostname        TEXT,
                ip_address      TEXT,
                mac_address     TEXT,
                user_id         TEXT,
                user_name       TEXT,
                role            TEXT,
                imprimante      TEXT,
                version_app     TEXT,
                statut          TEXT NOT NULL DEFAULT 'CONNECTE'
                                CHECK(statut IN ('CONNECTE','DECONNECTE','BLOQUE')),
                derniere_vue    TEXT NOT NULL DEFAULT (datetime('now')),
                created_at      TEXT NOT NULL DEFAULT (datetime('now')),
                bloque          INTEGER NOT NULL DEFAULT 0,
                bloque_raison   TEXT
            )""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_cs_machine "
                   "ON ClientSession(machine_id)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_cs_statut "
                   "ON ClientSession(statut)")
        logger.info("Table ClientSession créée")
    except Exception:
        logger.exception("Erreur création ClientSession")

def migrate_currency():
    """Ajoute les configs devises si absentes."""
    defaults = [
        ("devise", "FC", "str", "Devise principale"),
        ("taux_change", "2250.0", "float",
         "Taux de change (1 USD = X FC)"),
        ("afficher_dual", "true", "bool",
         "Afficher l'équivalent USD sous les montants FC"),
    ]
    for cle, valeur, type_, desc in defaults:
        existing = db.query_one(
            "SELECT 1 FROM Configuration WHERE cle = ? LIMIT 1", (cle,))
        if existing:
            continue
        db.set_config(cle, valeur, type_=type_, description=desc)
        print(f"  · Clé ajoutée : {cle} = {valeur}")


def _apply_monitoring_machine():
    """Crée la table MonitoringMachine si absente (whitelist PC monitoring)."""
    try:
        if db.query("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='MonitoringMachine'"):
            return

        db.execute("""
            CREATE TABLE IF NOT EXISTS MonitoringMachine (
                id              TEXT PRIMARY KEY,
                machine_id      TEXT NOT NULL UNIQUE,
                hostname        TEXT,
                role_autorise   TEXT NOT NULL DEFAULT 'ALL'
                                CHECK(role_autorise IN ('OWNER','ADMIN','DEV','ALL')),
                ajoute_par      TEXT,
                ajoute_par_name TEXT,
                ajoute_le       TEXT NOT NULL DEFAULT (datetime('now')),
                actif           INTEGER NOT NULL DEFAULT 1
            )
        """)
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_monitoring_machine "
            "ON MonitoringMachine(machine_id)")
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_monitoring_actif "
            "ON MonitoringMachine(actif)")
        logger.info("Table MonitoringMachine créée")
        print("  · Table MonitoringMachine créée")
    except Exception:
        logger.exception("Erreur création MonitoringMachine")


def _apply_notifications():
    """Crée la table Notification pour le centre de notifications."""
    try:
        if db.query("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='Notification'"):
            return

        db.execute("""
            CREATE TABLE IF NOT EXISTS Notification (
                id              TEXT PRIMARY KEY,
                type            TEXT NOT NULL
                                CHECK(type IN ('success','info','warning','danger')),
                title           TEXT NOT NULL,
                message         TEXT,
                lu              INTEGER NOT NULL DEFAULT 0,
                action_url      TEXT,
                created_at      TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_notif_lu "
            "ON Notification(lu)")
        logger.info("Table Notification créée")
        print("  · Table Notification créée")
    except Exception:
        logger.exception("Erreur création Notification")

# ══════════════════════════════════════════════════════════════════
# RUN ALL
# ══════════════════════════════════════════════════════════════════
def run_all():
    migrate_produits()
    migrate_produits_actif()
    migrate_client()
    migrate_facturation_config()
    migrate_blf()
    migrate_blf_compteur()

    # ─── Nouvelles tables (Phases C, D, 2) ───
    _apply_rapport_z()
    _apply_retours()
    _apply_encaissement()

    # ─── Fix FK ───
    _fix_encaissement_fk()
    _fix_retour_fk()

    # Migrations utilisateurs (flags, triggers, audit)
    from Database import migrations_users
    migrations_users.run_all()

    # Migrations audit renforcé
    from Database import migrations_audit
    migrations_audit.run_all()

    migrate_client_sexe()
    _apply_client_sexe_index()

    _apply_client_sessions()
    _apply_monitoring_machine()          # ← AJOUT ICI
    _apply_notifications()
    migrate_currency()



# ─── Point d'entrée CLI uniquement ───
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db.get_conn()
    run_all()