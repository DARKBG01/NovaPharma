#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrations_users.py — Migrations du module Utilisateurs
========================================================
- Ajoute is_owner, is_developer, must_change_password
- Crée AuditLog et UtilisateurPermission
- Triggers : 1 seul owner / 1 seul developer
- Migration auto du 1ᵉʳ user comme owner
"""

import logging
from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# 1. Colonnes à ajouter à Utilisateur
# ══════════════════════════════════════════════════════════════════
def migrate_utilisateur_flags():
    """Ajoute les colonnes is_owner, is_developer, must_change_password."""
    existing = {row["name"] for row in db.query(
        "PRAGMA table_info(Utilisateur)")}

    additions = [
        ("is_owner",             "INTEGER NOT NULL DEFAULT 0"),
        ("is_developer",         "INTEGER NOT NULL DEFAULT 0"),
        ("must_change_password", "INTEGER NOT NULL DEFAULT 0"),
    ]

    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(
                f"ALTER TABLE Utilisateur ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : Utilisateur.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")


# ══════════════════════════════════════════════════════════════════
# 2. Table AuditLog
# ══════════════════════════════════════════════════════════════════
def migrate_audit_log():
    """Crée la table AuditLog si absente."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS AuditLog (
            id                TEXT PRIMARY KEY,
            action            TEXT NOT NULL,
            utilisateur_id    TEXT,
            utilisateur_name  TEXT,
            cible_type        TEXT,
            cible_id          TEXT,
            cible_nom         TEXT,
            details           TEXT,
            avant             TEXT,
            apres             TEXT,
            ip_address        TEXT,
            machine_name      TEXT,
            date_action       TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_audit_action "
        "ON AuditLog(action)")
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_audit_user "
        "ON AuditLog(utilisateur_id)")
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_audit_date "
        "ON AuditLog(date_action)")
    print("  · Table AuditLog prête")


# ══════════════════════════════════════════════════════════════════
# 3. Table UtilisateurPermission
# ══════════════════════════════════════════════════════════════════
def migrate_utilisateur_permission():
    """Crée la table UtilisateurPermission si absente."""
    db.execute("""
        CREATE TABLE IF NOT EXISTS UtilisateurPermission (
            id              TEXT PRIMARY KEY,
            utilisateur_id  TEXT NOT NULL,
            permission_key  TEXT NOT NULL,
            actif           INTEGER NOT NULL DEFAULT 1,
            updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(utilisateur_id, permission_key),
            FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
                ON DELETE CASCADE
        )
    """)
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_uperm_user "
        "ON UtilisateurPermission(utilisateur_id)")
    print("  · Table UtilisateurPermission prête")


# ══════════════════════════════════════════════════════════════════
# 4. Triggers : 1 seul owner / 1 seul developer
# ══════════════════════════════════════════════════════════════════
def migrate_triggers():
    """Crée les triggers pour garantir 1 seul owner et 1 seul developer."""

    # Trigger owner
    db.execute("DROP TRIGGER IF EXISTS trg_one_owner_update")
    db.execute("""
        CREATE TRIGGER trg_one_owner_update
        BEFORE UPDATE OF is_owner ON Utilisateur
        WHEN NEW.is_owner = 1 AND OLD.is_owner = 0
        BEGIN
            SELECT CASE
                WHEN (SELECT COUNT(*) FROM Utilisateur
                      WHERE is_owner = 1) >= 1
                THEN RAISE(ABORT, 'Un seul owner est autorise')
            END;
        END
    """)

    db.execute("DROP TRIGGER IF EXISTS trg_one_owner_insert")
    db.execute("""
        CREATE TRIGGER trg_one_owner_insert
        BEFORE INSERT ON Utilisateur
        WHEN NEW.is_owner = 1
        BEGIN
            SELECT CASE
                WHEN (SELECT COUNT(*) FROM Utilisateur
                      WHERE is_owner = 1) >= 1
                THEN RAISE(ABORT, 'Un seul owner est autorise')
            END;
        END
    """)

    # Trigger developer
    db.execute("DROP TRIGGER IF EXISTS trg_one_developer_update")
    db.execute("""
        CREATE TRIGGER trg_one_developer_update
        BEFORE UPDATE OF is_developer ON Utilisateur
        WHEN NEW.is_developer = 1 AND OLD.is_developer = 0
        BEGIN
            SELECT CASE
                WHEN (SELECT COUNT(*) FROM Utilisateur
                      WHERE is_developer = 1) >= 1
                THEN RAISE(ABORT, 'Un seul developer est autorise')
            END;
        END
    """)

    db.execute("DROP TRIGGER IF EXISTS trg_one_developer_insert")
    db.execute("""
        CREATE TRIGGER trg_one_developer_insert
        BEFORE INSERT ON Utilisateur
        WHEN NEW.is_developer = 1
        BEGIN
            SELECT CASE
                WHEN (SELECT COUNT(*) FROM Utilisateur
                      WHERE is_developer = 1) >= 1
                THEN RAISE(ABORT, 'Un seul developer est autorise')
            END;
        END
    """)

    print("  · Triggers créés (1 owner, 1 developer)")


# ══════════════════════════════════════════════════════════════════
# 5. Migration auto : 1ᵉʳ user = owner
# ══════════════════════════════════════════════════════════════════
def migrate_first_user_as_owner():
    """
    Définit le 1ᵉʳ utilisateur comme OWNER (tout-puissant) si aucun
    n'existe.

    Actions :
      - is_owner = 1
      - Toutes les permissions granulaires activées
      - Log dans AuditLog
    """
    try:
        # ─── Y a-t-il déjà un OWNER ? ───
        row = db.query_one(
            "SELECT COUNT(*) AS n FROM Utilisateur WHERE is_owner = 1")
        if row and int(row["n"] or 0) > 0:
            return

        # ─── Y a-t-il des utilisateurs ? ───
        count = db.query_one("SELECT COUNT(*) AS n FROM Utilisateur")
        if not count or int(count["n"] or 0) == 0:
            return  # pas encore d'utilisateur (wizard pas passé)

        # ─── Cherche le 1ᵉʳ utilisateur créé (peu importe le rôle) ───
        first = db.query_one(
            """SELECT id, identifiant,
                      COALESCE(prenom, '') || ' ' ||
                      COALESCE(nom, '') AS nom,
                      role
               FROM Utilisateur
               ORDER BY created_at ASC, rowid ASC
               LIMIT 1""")

        if first is None:
            return

        # ─── Promotion en OWNER ───
        try:
            db.execute(
                "UPDATE Utilisateur SET is_owner = 1 WHERE id = ?",
                (first["id"],))
        except Exception as e:
            # Si le trigger bloque, c'est qu'un owner existe déjà
            logger.debug("Promotion owner bloquée : %s", e)
            return

        # ─── Attribution de TOUTES les permissions granulaires ───
        try:
            from Database import permissions as perms
            all_keys = perms.get_all_permissions()
            for key in all_keys:
                try:
                    db.execute(
                        """INSERT INTO UtilisateurPermission
                           (id, utilisateur_id, permission_key,
                            actif, updated_at)
                           VALUES (?, ?, ?, 1, datetime('now'))
                           ON CONFLICT(utilisateur_id, permission_key)
                           DO UPDATE SET actif = 1,
                                         updated_at = datetime('now')""",
                        (db.new_id(), first["id"], key))
                except Exception:
                    pass
        except Exception:
            logger.exception("Erreur attribution permissions owner")

        # ─── Audit ───
        try:
            from Database import audit
            audit.log(
                "PROMOTION_OWNER_AUTO",
                utilisateur_id=first["id"],
                utilisateur_name=first["identifiant"],
                cible_type="user",
                cible_id=first["id"],
                cible_nom=first["identifiant"],
                details={
                    "raison": "1ᵉʳ utilisateur créé dans la base",
                    "role_initial": first["role"],
                })
        except Exception:
            pass

        print(f"  · OWNER promu automatiquement : "
              f"{first['nom'].strip()} ({first['identifiant']})")

    except Exception as e:
        logger.debug("Migration owner ignorée : %s", e)

# ══════════════════════════════════════════════════════════════════
# 7. Migration : colonnes v4.4 dans Historique
# ══════════════════════════════════════════════════════════════════
def migrate_historique_v44():
    """Ajoute utilisateur_id, annule, motif_annulation à Historique."""
    existing = {row["name"] for row in db.query(
        "PRAGMA table_info(Historique)")}

    additions = [
        ("utilisateur_id",    "TEXT"),
        ("annule",            "INTEGER NOT NULL DEFAULT 0"),
        ("motif_annulation",  "TEXT"),
    ]

    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(
                f"ALTER TABLE Historique ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : Historique.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")


# ══════════════════════════════════════════════════════════════════
# 8. Migration : tables BLF + MouvementStock + AjustementStock
# ══════════════════════════════════════════════════════════════════
def migrate_blf_tables():
    """Crée/assure toutes les tables BLF et traçabilité."""
    # BonLivraison
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

    # LigneBonLivraison
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
            FOREIGN KEY (blf_id) REFERENCES BonLivraison(id)
                ON DELETE CASCADE
        )
    """)

    # MouvementStock (si absente)
    db.execute("""
        CREATE TABLE IF NOT EXISTS MouvementStock (
            id              TEXT PRIMARY KEY,
            produit_id      TEXT NOT NULL,
            type            TEXT NOT NULL
                            CHECK(type IN ('ENTREE','SORTIE','AJUSTEMENT','ANNULATION')),
            quantite        INTEGER NOT NULL,
            stock_avant     INTEGER NOT NULL,
            stock_apres     INTEGER NOT NULL,
            motif           TEXT,
            vente_id        TEXT,
            utilisateur_id  TEXT,
            date_mouvement  TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # AjustementStock (si absente)
    db.execute("""
        CREATE TABLE IF NOT EXISTS AjustementStock (
            id              TEXT PRIMARY KEY,
            Code_reference  TEXT NOT NULL,
            Nom_produit     TEXT NOT NULL,
            stock_avant     INTEGER NOT NULL,
            stock_apres     INTEGER NOT NULL,
            difference      INTEGER NOT NULL,
            motif           TEXT NOT NULL,
            utilisateur_id  TEXT,
            date_ajustement TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # Index
    for stmt in [
        "CREATE INDEX IF NOT EXISTS idx_blf_numero ON BonLivraison(numero_blf)",
        "CREATE INDEX IF NOT EXISTS idx_blf_statut ON BonLivraison(statut)",
        "CREATE INDEX IF NOT EXISTS idx_blf_ligne_blf ON LigneBonLivraison(blf_id)",
        "CREATE INDEX IF NOT EXISTS idx_mvt_produit ON MouvementStock(produit_id)",
        "CREATE INDEX IF NOT EXISTS idx_ajust_produit ON AjustementStock(Code_reference)",
    ]:
        try:
            db.execute(stmt)
        except Exception:
            pass

    print("  · Tables BLF + traçabilité prêtes")
    

# ══════════════════════════════════════════════════════════════════
# 9. Migration : colonnes manquantes dans Fournisseur
# ══════════════════════════════════════════════════════════════════
def migrate_fournisseur_v44():
    """Ajoute actif, Adresse, created_at à Fournisseur si absents."""
    existing = {row["name"] for row in db.query(
        "PRAGMA table_info(Fournisseur)")}

    additions = [
        ("Adresse",    "TEXT"),
        ("actif",      "INTEGER NOT NULL DEFAULT 1"),
        ("created_at", "TEXT"),
    ]

    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(
                f"ALTER TABLE Fournisseur ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : Fournisseur.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")

    # Remplit created_at pour les lignes existantes
    try:
        db.execute(
            "UPDATE Fournisseur SET created_at = datetime('now') "
            "WHERE created_at IS NULL")
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════
# 10. Migration : colonnes manquantes dans produits
# ══════════════════════════════════════════════════════════════════
def migrate_produits_v44():
    """Assure que produits a toutes les colonnes attendues."""
    existing = {row["name"] for row in db.query(
        "PRAGMA table_info(produits)")}

    additions = [
        ("Code_barre",        "TEXT"),
        ("Description",       "TEXT"),
        ("Unite",             "TEXT NOT NULL DEFAULT 'pièce'"),
        ("Quantite_initiale", "INTEGER NOT NULL DEFAULT 0"),
        ("Cree_par",          "TEXT"),
        ("actif",             "INTEGER NOT NULL DEFAULT 1"),
        ("Date_ajout",        "TEXT"),
    ]

    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(
                f"ALTER TABLE produits ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : produits.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")


# ══════════════════════════════════════════════════════════════════
# 11. Migration : colonnes manquantes dans Client
# ══════════════════════════════════════════════════════════════════
def migrate_client_v44():
    """Assure que Client a toutes les colonnes attendues."""
    existing = {row["name"] for row in db.query(
        "PRAGMA table_info(Client)")}

    additions = [
        ("C_name",        "TEXT"),
        ("Montant_total", "REAL NOT NULL DEFAULT 0"),
        ("Id_client",     "TEXT"),
        ("email",         "TEXT"),
        ("notes",         "TEXT"),
        ("actif",         "INTEGER NOT NULL DEFAULT 1"),
        ("created_at",    "TEXT"),
    ]

    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(
                f"ALTER TABLE Client ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : Client.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")

    # Remplit created_at pour les lignes existantes
    try:
        db.execute(
            "UPDATE Client SET created_at = datetime('now') "
            "WHERE created_at IS NULL")
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════
# 12. Migration : colonnes manquantes dans Historique_commande
# ══════════════════════════════════════════════════════════════════
def migrate_historique_commande_v44():
    """Assure que Historique_commande a toutes les colonnes."""
    existing = {r["name"] for r in db.query(
        "PRAGMA table_info(Historique_commande)")}
    if not existing:
        return  # table absente, sera créée par seed ou autre

    additions = [
        ("Num_commande",  "TEXT"),
        ("Categorie",     "TEXT"),
        ("Expiration",    "TEXT"),
        ("Entreprise",    "TEXT"),
        ("Date_commande", "TEXT"),
    ]

    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(
                f"ALTER TABLE Historique_commande "
                f"ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : Historique_commande.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")
            

# ══════════════════════════════════════════════════════════════════
# 13. Migration : corrige la FK de MouvementStock
# ══════════════════════════════════════════════════════════════════
def migrate_mouvement_stock_fix():
    """
    Recrée MouvementStock avec la bonne FK vers produits(Code_reference)
    au lieu de Produit(id) (table v2 vide).

    ⚠️ Perd les données existantes de MouvementStock.
    """
    # Vérifie si la table existe
    try:
        info = db.query("PRAGMA table_info(MouvementStock)")
        if not info:
            print("  · MouvementStock absente — skip")
            return
    except Exception:
        return

    # Vérifie si la FK est déjà correcte (SQLite ne l'expose pas directement,
    # donc on teste la cohérence en essayant un insert bidon puis rollback)
    try:
        with db.transaction():
            test_id = db.new_id()
            db.execute("""
                INSERT INTO MouvementStock
                (id, produit_id, type, quantite, stock_avant, stock_apres)
                VALUES (?,?,?,?,?,?)
            """, (test_id, "__TEST__", "ENTREE", 0, 0, 0))
            raise RuntimeError("rollback_test")
    except RuntimeError:
        # FK accepte la chaîne libre → OK, skip
        print("  · MouvementStock : FK déjà correcte")
        return
    except Exception:
        # FK refuse → il faut recréer
        pass

    # ─── Recréation de la table ───
    try:
        print("  · Recréation de MouvementStock avec la bonne FK...")

        # Désactive temporairement les FK pour permettre le DROP
        db.get_conn().execute("PRAGMA foreign_keys = OFF")

        try:
            # Sauvegarde des données (au cas où il y en aurait)
            try:
                old_data = db.query("SELECT * FROM MouvementStock")
            except Exception:
                old_data = []

            db.execute("DROP TABLE IF EXISTS MouvementStock")

            db.execute("""
                CREATE TABLE MouvementStock (
                    id              TEXT PRIMARY KEY,
                    produit_id      TEXT NOT NULL,
                    type            TEXT NOT NULL
                                    CHECK(type IN ('ENTREE','SORTIE','AJUSTEMENT','ANNULATION')),
                    quantite        INTEGER NOT NULL,
                    stock_avant     INTEGER NOT NULL,
                    stock_apres     INTEGER NOT NULL,
                    motif           TEXT,
                    vente_id        TEXT,
                    utilisateur_id  TEXT,
                    date_mouvement  TEXT NOT NULL DEFAULT (datetime('now')),
                    FOREIGN KEY (produit_id)     REFERENCES produits(Code_reference) ON DELETE RESTRICT,
                    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)          ON DELETE SET NULL
                )
            """)

            db.execute(
                "CREATE INDEX IF NOT EXISTS idx_mvt_produit "
                "ON MouvementStock(produit_id)")
            db.execute(
                "CREATE INDEX IF NOT EXISTS idx_mvt_date "
                "ON MouvementStock(date_mouvement)")

            # Réinsère les données valides (celles dont le produit existe)
            if old_data:
                for r in old_data:
                    try:
                        db.execute("""
                            INSERT INTO MouvementStock
                            (id, produit_id, type, quantite,
                             stock_avant, stock_apres, motif,
                             vente_id, utilisateur_id, date_mouvement)
                            VALUES (?,?,?,?,?,?,?,?,?,?)
                        """, (r["id"], r["produit_id"], r["type"],
                              r["quantite"], r["stock_avant"],
                              r["stock_apres"], r["motif"],
                              r["vente_id"], r["utilisateur_id"],
                              r["date_mouvement"]))
                    except Exception:
                        pass  # skip lignes orphelines
                print(f"  · {len(old_data)} ligne(s) conservée(s)")
        finally:
            db.get_conn().execute("PRAGMA foreign_keys = ON")

        print("  ✓ MouvementStock recréée correctement")

    except Exception as e:
        print(f"  ! Erreur migration MouvementStock : {e}")

# ══════════════════════════════════════════════════════════════════
# 6. Point d'entrée
# ══════════════════════════════════════════════════════════════════
def run_all():
    print("→ Migrations...")
    with db.transaction():
        migrate_utilisateur_flags()
        migrate_audit_log()
        migrate_utilisateur_permission()
        migrate_triggers()
        migrate_historique_v44()
        migrate_blf_tables()
        migrate_fournisseur_v44()
        migrate_produits_v44()
        migrate_client_v44()
        migrate_historique_commande_v44()
        migrate_first_user_as_owner()
    # FK fix : hors transaction (car on touche aux PRAGMA)
    migrate_mouvement_stock_fix()
    print("✓ Migrations terminées")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db.get_conn()
    run_all()