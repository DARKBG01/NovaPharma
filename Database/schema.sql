-- ============================================================
-- NovaPharma — Schéma unifié COMPLET v5.0
-- Base unique : Database/NovaPharma.db
-- Toutes les migrations intégrées — aucune migration requise
--
-- Nettoyage v5.0 :
--   • Supprimé : Compteur, Produit (v2), Vente (v2), LigneVente (v2),
--     Historique_commande, DeveloperKey, RapportSauvegarde
--   • Corrigé : FK Encaissement/RetourVente vers Historique (bug)
--   • Ajouté : Client.sexe, ClientSession
-- ============================================================

PRAGMA foreign_keys = ON;

-- ═══════════════════════════════════════════════════════════
--  1. NOYAU — Tables indépendantes
-- ═══════════════════════════════════════════════════════════

-- ─── Caisse ───
CREATE TABLE IF NOT EXISTS Caisse (
    id          TEXT PRIMARY KEY,
    code        TEXT NOT NULL UNIQUE,
    libelle     TEXT NOT NULL,
    active      INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ─── Pharmacie ───
CREATE TABLE IF NOT EXISTS Pharmacie (
    id              INTEGER PRIMARY KEY CHECK(id = 1),
    nom             TEXT NOT NULL,
    type            TEXT NOT NULL CHECK(type IN ('PETITE','MOYENNE','GRANDE')),
    email           TEXT,
    numero          TEXT,
    adresse         TEXT,
    path_logo       TEXT,
    seuil_stock     INTEGER NOT NULL DEFAULT 25,
    marge_benefice  REAL    NOT NULL DEFAULT 30.0,
    actif           INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ─── Configuration (clé/valeur) ───
-- Contient : devise, mentions_ticket, facture_numero_caisse,
--            facture_numero_temoin, max_postes, taux_change, etc.
CREATE TABLE IF NOT EXISTS Configuration (
    cle         TEXT PRIMARY KEY,
    valeur      TEXT NOT NULL,
    type        TEXT NOT NULL CHECK(type IN ('str','int','float','bool','json')),
    description TEXT,
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ─── Categorie ───
CREATE TABLE IF NOT EXISTS Categorie (
    id          TEXT PRIMARY KEY,
    nom         TEXT NOT NULL UNIQUE,
    description TEXT,
    actif       INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);


-- ═══════════════════════════════════════════════════════════
--  2. PRODUITS, CLIENTS, FOURNISSEURS
-- ═══════════════════════════════════════════════════════════

-- ─── produits (table active) ───
CREATE TABLE IF NOT EXISTS produits (
    Code_reference      TEXT PRIMARY KEY,
    Nom                 TEXT NOT NULL UNIQUE,
    Code_barre          TEXT UNIQUE,
    Categorie           TEXT,
    Description         TEXT,
    Unite               TEXT NOT NULL DEFAULT 'pièce',
    Quantite_initiale   INTEGER NOT NULL DEFAULT 0,
    Quantite            INTEGER NOT NULL DEFAULT 0,
    Prix_achat          REAL NOT NULL DEFAULT 0,
    Prix_vente          REAL NOT NULL DEFAULT 0,
    Prix_unitaire       REAL NOT NULL DEFAULT 0,
    Cree_par            TEXT,
    actif               INTEGER NOT NULL DEFAULT 1,
    Date_ajout          TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_produits_nom     ON produits(Nom);
CREATE INDEX IF NOT EXISTS idx_produits_cat     ON produits(Categorie);
CREATE INDEX IF NOT EXISTS idx_produits_stock   ON produits(Quantite);
CREATE INDEX IF NOT EXISTS idx_produits_barcode ON produits(Code_barre);
CREATE INDEX IF NOT EXISTS idx_produits_actif   ON produits(actif);

-- ─── Client ───
CREATE TABLE IF NOT EXISTS Client (
    id              TEXT PRIMARY KEY,
    nom             TEXT NOT NULL,
    numero          TEXT UNIQUE,
    adresse         TEXT,
    -- Legacy (compat)
    Id_client       TEXT,
    C_name          TEXT,
    Montant_total   REAL NOT NULL DEFAULT 0,
    -- v4+
    email           TEXT,
    notes           TEXT,
    sexe            TEXT CHECK(sexe IN ('M','F')) DEFAULT 'M',   -- NOUVEAU
    actif           INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_client_numero ON Client(numero);
CREATE INDEX IF NOT EXISTS idx_client_nom    ON Client(C_name);
CREATE INDEX IF NOT EXISTS idx_client_name2  ON Client(nom);
CREATE INDEX IF NOT EXISTS idx_client_actif  ON Client(actif);
CREATE INDEX IF NOT EXISTS idx_client_sexe   ON Client(sexe);

-- ─── Fournisseur ───
CREATE TABLE IF NOT EXISTS Fournisseur (
    Id_fournisseur  TEXT PRIMARY KEY,
    Entreprise      TEXT NOT NULL,
    Categorie       TEXT,
    Responsable     TEXT,
    Numero          TEXT,
    Email           TEXT,
    Adresse         TEXT,
    actif           INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_fournisseur_entreprise ON Fournisseur(Entreprise);
CREATE INDEX IF NOT EXISTS idx_fournisseur_actif      ON Fournisseur(actif);


-- ═══════════════════════════════════════════════════════════
--  3. UTILISATEURS & SÉCURITÉ
-- ═══════════════════════════════════════════════════════════

-- ─── Utilisateur ───
CREATE TABLE IF NOT EXISTS Utilisateur (
    id                    TEXT PRIMARY KEY,
    identifiant           TEXT NOT NULL UNIQUE,
    prenom                TEXT NOT NULL,
    nom                   TEXT NOT NULL,
    post_nom              TEXT,
    sexe                  TEXT NOT NULL CHECK(sexe IN ('M','F')),
    date_naissance        TEXT,
    nationalite           TEXT,
    email                 TEXT UNIQUE,
    numero                TEXT NOT NULL UNIQUE,
    numero_caisse         TEXT,
    role                  TEXT NOT NULL
                          CHECK(role IN ('ADMIN','UTILISATEUR','CAISSIER')),
    pswd_hash             TEXT NOT NULL,
    path_image            TEXT,
    actif                 INTEGER NOT NULL DEFAULT 1,
    derniere_connexion    TEXT,
    created_at            TEXT NOT NULL DEFAULT (datetime('now')),
    -- Flags spéciaux
    is_owner              INTEGER NOT NULL DEFAULT 0,
    is_developer          INTEGER NOT NULL DEFAULT 0,
    must_change_password  INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (numero_caisse) REFERENCES Caisse(code)
        ON UPDATE CASCADE ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_utilisateur_identifiant ON Utilisateur(identifiant);
CREATE INDEX IF NOT EXISTS idx_utilisateur_email       ON Utilisateur(email);
CREATE INDEX IF NOT EXISTS idx_utilisateur_role        ON Utilisateur(role);
CREATE INDEX IF NOT EXISTS idx_utilisateur_actif       ON Utilisateur(actif);
CREATE INDEX IF NOT EXISTS idx_utilisateur_owner       ON Utilisateur(is_owner);
CREATE INDEX IF NOT EXISTS idx_utilisateur_developer   ON Utilisateur(is_developer);

-- ─── UtilisateurPermission ───
CREATE TABLE IF NOT EXISTS UtilisateurPermission (
    id              TEXT PRIMARY KEY,
    utilisateur_id  TEXT NOT NULL,
    permission_key  TEXT NOT NULL,
    actif           INTEGER NOT NULL DEFAULT 1,
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(utilisateur_id, permission_key),
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
        ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_uperm_user ON UtilisateurPermission(utilisateur_id);
CREATE INDEX IF NOT EXISTS idx_uperm_key  ON UtilisateurPermission(permission_key);

-- ─── Consentement ───
CREATE TABLE IF NOT EXISTS Consentement (
    id              TEXT PRIMARY KEY,
    utilisateur_id  TEXT NOT NULL,
    type            TEXT NOT NULL
                    CHECK(type IN ('SAUVEGARDE','IA_ANONYMISEE','CGU')),
    version_texte   TEXT NOT NULL,
    accepte         INTEGER NOT NULL CHECK(accepte IN (0,1)),
    empreinte       TEXT NOT NULL,
    date_decision   TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
        ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_consentement_user ON Consentement(utilisateur_id);
CREATE INDEX IF NOT EXISTS idx_consentement_type ON Consentement(type, version_texte);

-- ─── AuditLog ───
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
    severite          TEXT NOT NULL DEFAULT 'info'
                      CHECK(severite IN ('info','warning','danger')),
    prev_hash         TEXT,
    current_hash      TEXT,
    date_action       TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_audit_action ON AuditLog(action);
CREATE INDEX IF NOT EXISTS idx_audit_user   ON AuditLog(utilisateur_id);
CREATE INDEX IF NOT EXISTS idx_audit_cible  ON AuditLog(cible_type, cible_id);
CREATE INDEX IF NOT EXISTS idx_audit_date   ON AuditLog(date_action);
CREATE INDEX IF NOT EXISTS idx_audit_sev    ON AuditLog(severite);

-- ─── Sauvegarde ───
CREATE TABLE IF NOT EXISTS Sauvegarde (
    id              TEXT PRIMARY KEY,
    chemin          TEXT NOT NULL,
    taille_octets   INTEGER NOT NULL,
    hash_sha256     TEXT NOT NULL,
    type            TEXT NOT NULL
                    CHECK(type IN ('MANUELLE','AUTO','PRE_MIGRATION')),
    statut          TEXT NOT NULL DEFAULT 'OK'
                    CHECK(statut IN ('OK','CORROMPUE','RESTAUREE')),
    date_creation   TEXT NOT NULL DEFAULT (datetime('now')),
    utilisateur_id  TEXT,
    commentaire     TEXT,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)
        ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_sauvegarde_date ON Sauvegarde(date_creation);


-- ═══════════════════════════════════════════════════════════
--  4. VENTES & MOUVEMENTS DE STOCK
-- ═══════════════════════════════════════════════════════════

-- ─── Historique (table active pour les ventes) ───
-- ⚠️ Num_fact N'EST PAS UNIQUE (une facture = plusieurs lignes)
CREATE TABLE IF NOT EXISTS Historique (
    Id               INTEGER PRIMARY KEY AUTOINCREMENT,
    Num_fact         TEXT NOT NULL,
    Code_reference   TEXT,
    Article          TEXT NOT NULL,
    Prix_uni         REAL NOT NULL,
    Quantite         INTEGER NOT NULL,
    Total            REAL NOT NULL,
    Expiration       TEXT,
    Client_name      TEXT,
    Caisse           TEXT,
    Date_vent        TEXT NOT NULL DEFAULT (datetime('now')),
    utilisateur_id   TEXT,
    annule           INTEGER NOT NULL DEFAULT 0,
    motif_annulation TEXT
);
CREATE INDEX IF NOT EXISTS idx_historique_fact ON Historique(Num_fact);
CREATE INDEX IF NOT EXISTS idx_historique_date ON Historique(Date_vent);
CREATE INDEX IF NOT EXISTS idx_historique_user ON Historique(utilisateur_id);
CREATE INDEX IF NOT EXISTS idx_historique_ann  ON Historique(annule);
CREATE INDEX IF NOT EXISTS idx_historique_caiss ON Historique(Caisse);

-- ─── MouvementStock ───
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
    date_mouvement  TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (produit_id)     REFERENCES produits(Code_reference) ON DELETE RESTRICT,
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id)          ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_mvt_produit ON MouvementStock(produit_id);
CREATE INDEX IF NOT EXISTS idx_mvt_date    ON MouvementStock(date_mouvement);
CREATE INDEX IF NOT EXISTS idx_mvt_type    ON MouvementStock(type);

-- ─── AjustementStock ───
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
);
CREATE INDEX IF NOT EXISTS idx_ajust_produit ON AjustementStock(Code_reference);
CREATE INDEX IF NOT EXISTS idx_ajust_date    ON AjustementStock(date_ajustement);
CREATE INDEX IF NOT EXISTS idx_ajust_user    ON AjustementStock(utilisateur_id);

-- ─── Encaissement (reçu client + rendu) ───
-- ⚠️ PAS DE FK vers Historique : Num_fact n'y est pas UNIQUE
CREATE TABLE IF NOT EXISTS Encaissement (
    id                TEXT PRIMARY KEY,
    num_fact          TEXT NOT NULL,
    montant_facture   REAL NOT NULL,
    devise_paiement   TEXT NOT NULL
                      CHECK(devise_paiement IN ('FC','USD')),
    taux_change       REAL NOT NULL DEFAULT 2800.0,
    montant_recu      REAL NOT NULL,
    montant_recu_fc   REAL NOT NULL,
    montant_rendu     REAL NOT NULL,
    devise_rendu      TEXT NOT NULL DEFAULT 'FC'
                      CHECK(devise_rendu IN ('FC','USD')),
    utilisateur_id    TEXT,
    utilisateur_name  TEXT,
    date_encaissement TEXT NOT NULL DEFAULT (datetime('now')),
    notes             TEXT
);
CREATE INDEX IF NOT EXISTS idx_encaisse_facture ON Encaissement(num_fact);
CREATE INDEX IF NOT EXISTS idx_encaisse_date    ON Encaissement(date_encaissement);
CREATE INDEX IF NOT EXISTS idx_encaisse_user    ON Encaissement(utilisateur_id);


-- ═══════════════════════════════════════════════════════════
--  5. BON DE LIVRAISON FOURNISSEUR (BLF)
-- ═══════════════════════════════════════════════════════════

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
    motif_annulation    TEXT,
    FOREIGN KEY (fournisseur_id) REFERENCES Fournisseur(Id_fournisseur)
        ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_blf_numero ON BonLivraison(numero_blf);
CREATE INDEX IF NOT EXISTS idx_blf_statut ON BonLivraison(statut);
CREATE INDEX IF NOT EXISTS idx_blf_date   ON BonLivraison(date_livraison);
CREATE INDEX IF NOT EXISTS idx_blf_fourn  ON BonLivraison(fournisseur_id);

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
    FOREIGN KEY (blf_id)     REFERENCES BonLivraison(id) ON DELETE CASCADE,
    FOREIGN KEY (produit_id) REFERENCES produits(Code_reference)
        ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_blf_ligne_blf     ON LigneBonLivraison(blf_id);
CREATE INDEX IF NOT EXISTS idx_blf_ligne_produit ON LigneBonLivraison(produit_id);


-- ═══════════════════════════════════════════════════════════
--  6. RAPPORTS & RETOURS
-- ═══════════════════════════════════════════════════════════

-- ─── Rapport Z (clôture de caisse) ───
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
);
CREATE INDEX IF NOT EXISTS idx_rapportz_caisse ON RapportZ(caisse);
CREATE INDEX IF NOT EXISTS idx_rapportz_date   ON RapportZ(date_debut);
CREATE INDEX IF NOT EXISTS idx_rapportz_numero ON RapportZ(numero_z);

-- ─── Retour de vente (avoir) ───
-- ⚠️ PAS DE FK vers Historique : Num_fact n'y est pas UNIQUE
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
    date_retour       TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_retour_numero   ON RetourVente(numero_retour);
CREATE INDEX IF NOT EXISTS idx_retour_facture  ON RetourVente(num_fact_origine);
CREATE INDEX IF NOT EXISTS idx_retour_date     ON RetourVente(date_retour);
CREATE INDEX IF NOT EXISTS idx_retour_statut   ON RetourVente(statut);

-- ─── Ligne de retour ───
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
);
CREATE INDEX IF NOT EXISTS idx_ligne_retour ON LigneRetour(retour_id);


-- ═══════════════════════════════════════════════════════════
--  7. SURVEILLANCE POSTES CLIENTS
-- ═══════════════════════════════════════════════════════════

-- ─── ClientSession (postes connectés) ───
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
);
CREATE INDEX IF NOT EXISTS idx_cs_machine ON ClientSession(machine_id);
CREATE INDEX IF NOT EXISTS idx_cs_statut  ON ClientSession(statut);
CREATE INDEX IF NOT EXISTS idx_cs_user    ON ClientSession(user_id);


-- ═══════════════════════════════════════════════════════════
--  8. TRIGGERS — contraintes spéciales
-- ═══════════════════════════════════════════════════════════

-- ─── 1 seul OWNER ───
DROP TRIGGER IF EXISTS trg_one_owner_update;
CREATE TRIGGER trg_one_owner_update
BEFORE UPDATE OF is_owner ON Utilisateur
WHEN NEW.is_owner = 1 AND OLD.is_owner = 0
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM Utilisateur WHERE is_owner = 1) >= 1
        THEN RAISE(ABORT, 'Un seul owner est autorise')
    END;
END;

DROP TRIGGER IF EXISTS trg_one_owner_insert;
CREATE TRIGGER trg_one_owner_insert
BEFORE INSERT ON Utilisateur
WHEN NEW.is_owner = 1
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM Utilisateur WHERE is_owner = 1) >= 1
        THEN RAISE(ABORT, 'Un seul owner est autorise')
    END;
END;

-- ─── 1 seul DEVELOPER ───
DROP TRIGGER IF EXISTS trg_one_developer_update;
CREATE TRIGGER trg_one_developer_update
BEFORE UPDATE OF is_developer ON Utilisateur
WHEN NEW.is_developer = 1 AND OLD.is_developer = 0
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM Utilisateur WHERE is_developer = 1) >= 1
        THEN RAISE(ABORT, 'Un seul developer est autorise')
    END;
END;

DROP TRIGGER IF EXISTS trg_one_developer_insert;
CREATE TRIGGER trg_one_developer_insert
BEFORE INSERT ON Utilisateur
WHEN NEW.is_developer = 1
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM Utilisateur WHERE is_developer = 1) >= 1
        THEN RAISE(ABORT, 'Un seul developer est autorise')
    END;
END;


-- Garde pour compat, jamais remplie
CREATE TABLE IF NOT EXISTS Historique_commande (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Num_commande TEXT NOT NULL,
    Code_reference TEXT, Article TEXT NOT NULL,
    Categorie TEXT, Prix_uni REAL NOT NULL,
    Quantite INTEGER NOT NULL, Total REAL NOT NULL,
    Expiration TEXT, Entreprise TEXT,
    Date_commande TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ─── MonitoringMachine (whitelist PC monitoring - Phase 1) ───
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
);
CREATE INDEX IF NOT EXISTS idx_monitoring_machine ON MonitoringMachine(machine_id);
CREATE INDEX IF NOT EXISTS idx_monitoring_actif   ON MonitoringMachine(actif);

-- ═══════════════════════════════════════════════════════════
--  FIN DU SCHÉMA v2.0.0
-- ═══════════════════════════════════════════════════════════