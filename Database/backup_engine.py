#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database/backup_engine.py — Moteur de sauvegarde / restauration.
=================================================================
Politique GFS (Grand-père / Père / Fils) :
  • daily   → 7 derniers
  • weekly  → 4 dernières
  • monthly → 12 derniers
  • yearly  → 5 derniers

- Exclusion sélective des secrets (Configuration.unique_key, pwd_*,
  DeveloperKey, AuditLog, UtilisateurPermission, pswd_hash)
- Mot de passe dérivé machine
- Backup secondaire (USB/NAS) optionnel
"""

import json
import logging
import os
import shutil
import sqlite3
import tempfile
import time
from datetime import datetime, timedelta

import pyzipper

from Database import db, audit, machine_id
from Database.backup_crypto import get_backup_password

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Constantes
# ══════════════════════════════════════════════════════════════════
DEFAULT_BACKUP_DIR = os.path.join(
    os.path.expanduser("~"), "Documents", "NovaPharma", "Backups")

RETENTION = {
    "daily":   7,
    "weekly":  4,
    "monthly": 12,
    "yearly":  5,
}

# Tables EXCLUES (jamais incluses dans le backup)
EXCLUDED_TABLES = {
    "AuditLog",            # journal volumineux
    "UtilisateurPermission",  # sera réinitialisé au restore
    "DeveloperKey",        # sécurité critique
    "Consentement",        # volumineux et reconstruisible
}

# Colonnes EXCLUES (remplacées par placeholder si NOT NULL)
EXCLUDED_COLUMNS = {
    "Utilisateur": {"pswd_hash"},
    "Configuration": None,
}

# Placeholder pour les colonnes NOT NULL qu'on doit vider
# (format bcrypt valide → checkpw échoue proprement sans crash)
PLACEHOLDER_PSWD_HASH = (
    "$2b$12$" + "0" * 22 + "x" * 31
)  # 60 caractères exactement

PLACEHOLDER_COLUMNS = {
    "Utilisateur": {
        "pswd_hash": PLACEHOLDER_PSWD_HASH,
    },
}

# Clés de Configuration à exclure
EXCLUDED_CONFIG_KEYS = {
    "unique_key",
    "pwd_min_length", "pwd_expiration_days",
    "pwd_require_digit", "pwd_require_upper", "pwd_require_special",
    "sauvegarde_dossier", "sauvegarde_auto",
    "sauvegarde_intervalle_jours", "sauvegarde_max_conservees",
    "backup_secondary_dir", "backup_secondary_enabled",
    "backup_last_daily", "backup_last_weekly",
    "backup_last_monthly", "backup_last_yearly",
    "backup_last_secondary",
}


# ══════════════════════════════════════════════════════════════════
# Utilitaires
# ══════════════════════════════════════════════════════════════════
def _ensure_dirs(base_dir):
    for sub in ("daily", "weekly", "monthly", "yearly"):
        os.makedirs(os.path.join(base_dir, sub), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "meta"), exist_ok=True)


def get_backup_dir() -> str:
    """Retourne le dossier de backup principal."""
    custom = db.get_config("backup_dir", "")
    return custom if custom and os.path.isdir(custom) else DEFAULT_BACKUP_DIR


def get_secondary_dir() -> str:
    """Retourne le dossier secondaire s'il est activé et valide."""
    if not db.get_config("backup_secondary_enabled", False):
        return ""
    d = db.get_config("backup_secondary_dir", "") or ""
    return d if os.path.isdir(d) else ""


def _now() -> datetime:
    return datetime.now()


def _fmt_ts(dt=None) -> str:
    dt = dt or _now()
    return dt.strftime("%Y-%m-%d_%H%M%S")


# ══════════════════════════════════════════════════════════════════
# Création d'une copie filtrée de la base
# ══════════════════════════════════════════════════════════════════
def _create_filtered_db(source_path: str, dest_path: str) -> None:
    """
    Copie la base en excluant les tables et colonnes sensibles.
    """
    # Checkpoint pour un fichier cohérent
    try:
        db.get_conn().execute("PRAGMA wal_checkpoint(FULL)")
    except Exception:
        pass

    # On attache la source et on reconstruit dans dest
    conn_dst = sqlite3.connect(dest_path)
    try:
        conn_dst.execute("ATTACH DATABASE ? AS src", (source_path,))

        # Liste des tables
        tables = [
            r[0] for r in conn_dst.execute(
                "SELECT name FROM src.sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            ).fetchall()
        ]

        for tbl in tables:
            if tbl in EXCLUDED_TABLES:
                logger.info("Backup : table exclue → %s", tbl)
                continue

            # Récupère le CREATE
            row = conn_dst.execute(
                "SELECT sql FROM src.sqlite_master "
                "WHERE type='table' AND name=?", (tbl,)).fetchone()
            if not row or not row[0]:
                continue
            create_sql = row[0]

            conn_dst.execute(create_sql)

            # Colonnes de la source
            src_cols = [r[1] for r in conn_dst.execute(
                f"PRAGMA src.table_info({tbl})").fetchall()]

            # Filtre les colonnes exclues
            excluded_cols = EXCLUDED_COLUMNS.get(tbl, set()) or set()
            cols_to_keep = [c for c in src_cols if c not in excluded_cols]

            if not cols_to_keep:
                continue

            # Placeholders pour les colonnes exclues mais NOT NULL
            replaced = PLACEHOLDER_COLUMNS.get(tbl, {})
            replaced_cols = [c for c in replaced if c in src_cols
                             and c in excluded_cols]
            all_cols = cols_to_keep + replaced_cols

            col_list = ", ".join(f'"{c}"' for c in all_cols)
            placeholders = ", ".join("?" for _ in all_cols)

            # Récupère les lignes (colonnes gardées)
            rows = conn_dst.execute(
                f"SELECT {col_list} FROM src.\"{tbl}\""
                if not replaced_cols else
                f"SELECT {', '.join(chr(34)+c+chr(34) for c in cols_to_keep)} "
                f"FROM src.\"{tbl}\""
            ).fetchall()

            # Ajoute les placeholders
            if replaced_cols:
                rows = [tuple(r) + tuple(replaced[c]
                                          for c in replaced_cols)
                        for r in rows]

            if rows:
                conn_dst.executemany(
                    f'INSERT INTO "{tbl}" ({col_list}) '
                    f"VALUES ({placeholders})",
                    rows)

        # Copie des index (CREATE INDEX)
        indexes = conn_dst.execute(
            "SELECT sql FROM src.sqlite_master "
            "WHERE type='index' AND sql IS NOT NULL").fetchall()
        for (sql,) in indexes:
            try:
                conn_dst.execute(sql)
            except Exception:
                pass

        # ─── Filtre Configuration ───
        try:
            placeholders = ", ".join("?" for _ in EXCLUDED_CONFIG_KEYS)
            conn_dst.execute(
                f"DELETE FROM Configuration "
                f"WHERE cle IN ({placeholders})",
                tuple(EXCLUDED_CONFIG_KEYS))
        except Exception:
            pass

        # ─── Force must_change_password sur tous les users ───
        try:
            conn_dst.execute(
                "UPDATE Utilisateur SET must_change_password = 1, "
                "is_owner = 0")
        except Exception:
            pass

        conn_dst.commit()
        conn_dst.execute("DETACH DATABASE src")
    finally:
        conn_dst.close()


# ══════════════════════════════════════════════════════════════════
# Création d'une archive ZIP
# ══════════════════════════════════════════════════════════════════
def create_backup(backup_type: str,
                  custom_path: str = None,
                  user_id: str = None,
                  user_name: str = "Système") -> str:
    """
    Crée une archive ZIP du type demandé.
    Retourne le chemin du ZIP ou "" en cas d'erreur.

    backup_type : "daily" | "weekly" | "monthly" | "yearly" | "manual"
    custom_path : chemin personnalisé (pour "manual")
    """
    try:
        backup_dir = get_backup_dir()
        _ensure_dirs(backup_dir)

        subdir = backup_type if backup_type in RETENTION else "daily"
        if custom_path:
            zip_path = custom_path
        else:
            if backup_type == "daily":
                name = f"NovaPharma_daily_{_now().strftime('%Y-%m-%d')}.zip"
            elif backup_type == "weekly":
                y, w, _ = _now().isocalendar()
                name = f"NovaPharma_weekly_{y}-W{w:02d}.zip"
            elif backup_type == "monthly":
                name = f"NovaPharma_monthly_{_now().strftime('%Y-%m')}.zip"
            elif backup_type == "yearly":
                name = f"NovaPharma_yearly_{_now().strftime('%Y')}.zip"
            else:
                name = f"NovaPharma_manual_{_fmt_ts()}.zip"

            zip_path = os.path.join(backup_dir, subdir, name)

        os.makedirs(os.path.dirname(zip_path), exist_ok=True)

        # ─── Crée la base filtrée dans un dossier temp ───
        tmp_dir = tempfile.mkdtemp(prefix="nova_backup_")
        try:
            tmp_db = os.path.join(tmp_dir, "NovaPharma.db")
            _create_filtered_db(str(db.DB_PATH), tmp_db)

            # ─── ZIP AES-256 ───
            pwd = get_backup_password()
            if not pwd:
                raise RuntimeError("Mot de passe backup vide")

            with pyzipper.AESZipFile(
                    zip_path, "w",
                    compression=pyzipper.ZIP_LZMA,
                    encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(pwd.encode("utf-8"))
                zf.setencryption(pyzipper.WZ_AES, nbits=256)

                # Ajoute la DB
                zf.write(tmp_db, arcname="NovaPharma.db")

                # Ajoute un manifest
                manifest = {
                    "type": backup_type,
                    "date": _now().isoformat(),
                    "machine_id": machine_id.get_machine_id(),
                    "machine_short_id": machine_id.get_machine_short_id(),
                    "user": user_name,
                    "app_version": "4.5",
                }
                zf.writestr("manifest.json",
                            json.dumps(manifest, indent=2, ensure_ascii=False))

            # ─── Stats ───
            file_size = os.path.getsize(zip_path)
            file_hash = _hash_file(zip_path)

            # ─── Sauvegarde secondaire ───
            _copy_to_secondary(zip_path)

            # ─── Enregistre en DB ───
            try:
                with db.transaction():
                    db.execute("""
                        INSERT INTO Sauvegarde
                        (id, chemin, taille_octets, hash_sha256,
                         type, statut, utilisateur_id, commentaire)
                        VALUES (?, ?, ?, ?, ?, 'OK', ?, ?)
                    """, (db.new_id(), zip_path, file_size, file_hash,
                          _type_to_db(backup_type), user_id,
                          f"Backup auto {backup_type}"))
            except Exception:
                logger.exception("Erreur insert Sauvegarde")

            # ─── Update meta ───
            _update_last_run(backup_type)

            # ─── Audit ───
            audit.log(f"BACKUP_{backup_type.upper()}",
                      utilisateur_id=user_id,
                      utilisateur_name=user_name,
                      cible_type="backup",
                      cible_nom=os.path.basename(zip_path),
                      details={"path": zip_path,
                               "size": file_size})

            logger.info("Backup %s créé : %s", backup_type, zip_path)
            return zip_path

        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)

    except Exception:
        logger.exception("Erreur création backup %s", backup_type)
        return ""


def _hash_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def _type_to_db(t):
    mapping = {"daily": "AUTO", "weekly": "AUTO",
               "monthly": "AUTO", "yearly": "AUTO",
               "manual": "MANUELLE"}
    return mapping.get(t, "AUTO")


def _update_last_run(backup_type: str) -> None:
    key = f"backup_last_{backup_type}"
    try:
        db.set_config(key, _now().isoformat(),
                      type_="str",
                      description=f"Dernier backup {backup_type}")
    except Exception:
        pass


def _copy_to_secondary(zip_path: str) -> None:
    """Copie le ZIP dans le dossier secondaire si activé."""
    sec = get_secondary_dir()
    if not sec:
        return
    try:
        dest = os.path.join(sec, os.path.basename(zip_path))
        shutil.copyfile(zip_path, dest)
        logger.info("Copie secondaire : %s", dest)
        try:
            db.set_config("backup_last_secondary",
                          _now().isoformat(), type_="str")
        except Exception:
            pass
    except Exception:
        logger.exception("Erreur copie secondaire vers %s", sec)


# ══════════════════════════════════════════════════════════════════
# Politique GFS
# ══════════════════════════════════════════════════════════════════
def should_run_daily() -> bool:
    last = db.get_config("backup_last_daily", "")
    if not last:
        return True
    try:
        dt = datetime.fromisoformat(last)
        return (_now() - dt) >= timedelta(hours=24)
    except Exception:
        return True


def should_run_weekly() -> bool:
    last = db.get_config("backup_last_weekly", "")
    if not last:
        return True
    try:
        dt = datetime.fromisoformat(last)
        return (_now() - dt) >= timedelta(days=7)
    except Exception:
        return True


def should_run_monthly() -> bool:
    last = db.get_config("backup_last_monthly", "")
    if not last:
        return True
    try:
        dt = datetime.fromisoformat(last)
        return (_now() - dt) >= timedelta(days=30)
    except Exception:
        return True


def should_run_yearly() -> bool:
    last = db.get_config("backup_last_yearly", "")
    if not last:
        return True
    try:
        dt = datetime.fromisoformat(last)
        return (_now() - dt) >= timedelta(days=365)
    except Exception:
        return True


def _rotate(backup_type: str) -> None:
    """Supprime les archives au-delà de la rétention."""
    max_keep = RETENTION.get(backup_type)
    if not max_keep:
        return
    try:
        base = os.path.join(get_backup_dir(), backup_type)
        if not os.path.isdir(base):
            return
        files = [os.path.join(base, f)
                 for f in os.listdir(base)
                 if f.endswith(".zip")]
        files.sort(key=os.path.getmtime, reverse=True)
        for old in files[max_keep:]:
            try:
                os.remove(old)
                # Supprime aussi du dossier secondaire
                sec = get_secondary_dir()
                if sec:
                    p = os.path.join(sec, os.path.basename(old))
                    if os.path.exists(p):
                        os.remove(p)
                logger.info("Backup supprimé (rotation) : %s", old)
            except Exception:
                pass
    except Exception:
        logger.exception("Erreur rotation %s", backup_type)


# ══════════════════════════════════════════════════════════════════
# Orchestrateur — appelé au lancement
# ══════════════════════════════════════════════════════════════════
def run_auto_backups(user_id: str = None,
                     user_name: str = "Système") -> list:
    """
    Lance les backups dus (daily/weekly/monthly/yearly).
    Retourne la liste des chemins créés.
    """
    created = []
    try:
        if should_run_daily():
            p = create_backup("daily", user_id=user_id,
                              user_name=user_name)
            if p:
                created.append(p)
                _rotate("daily")

        if should_run_weekly():
            p = create_backup("weekly", user_id=user_id,
                              user_name=user_name)
            if p:
                created.append(p)
                _rotate("weekly")

        if should_run_monthly():
            p = create_backup("monthly", user_id=user_id,
                              user_name=user_name)
            if p:
                created.append(p)
                _rotate("monthly")

        if should_run_yearly():
            p = create_backup("yearly", user_id=user_id,
                              user_name=user_name)
            if p:
                created.append(p)
                _rotate("yearly")

    except Exception:
        logger.exception("Erreur backups auto")

    return created


# ══════════════════════════════════════════════════════════════════
# Liste / suppression
# ══════════════════════════════════════════════════════════════════
def list_backups() -> list:
    """Retourne la liste de toutes les archives."""
    out = []
    try:
        base = get_backup_dir()
        for sub in RETENTION.keys():
            d = os.path.join(base, sub)
            if not os.path.isdir(d):
                continue
            for f in os.listdir(d):
                if not f.endswith(".zip"):
                    continue
                p = os.path.join(d, f)
                try:
                    st = os.stat(p)
                    out.append({
                        "path": p,
                        "name": f,
                        "type": sub,
                        "size": st.st_size,
                        "date": datetime.fromtimestamp(st.st_mtime),
                    })
                except Exception:
                    pass
        out.sort(key=lambda x: x["date"], reverse=True)
    except Exception:
        logger.exception("Erreur list_backups")
    return out


def delete_backup(path: str) -> bool:
    try:
        if os.path.exists(path):
            os.remove(path)
            # Supprime aussi du secondaire
            sec = get_secondary_dir()
            if sec:
                p = os.path.join(sec, os.path.basename(path))
                if os.path.exists(p):
                    os.remove(p)
            return True
    except Exception:
        logger.exception("Erreur suppression backup")
    return False


# ══════════════════════════════════════════════════════════════════
# Extraction en lecture seule
# ══════════════════════════════════════════════════════════════════
def extract_to_temp(zip_path: str) -> tuple:
    """
    Déchiffre l'archive dans un dossier temp.
    Retourne (tmp_dir, db_path). En cas d'erreur, retourne ("", "").
    """
    try:
        if not os.path.exists(zip_path):
            return "", ""

        tmp_dir = tempfile.mkdtemp(prefix="nova_reader_")
        pwd = get_backup_password()

        with pyzipper.AESZipFile(zip_path) as zf:
            zf.setpassword(pwd.encode("utf-8"))
            zf.extractall(tmp_dir)

        db_path = os.path.join(tmp_dir, "NovaPharma.db")
        if not os.path.exists(db_path):
            return "", ""
        return tmp_dir, db_path
    except Exception:
        logger.exception("Erreur extraction backup")
        return "", ""


def cleanup_temp(tmp_dir: str) -> None:
    try:
        if tmp_dir and os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
    except Exception:
        pass

def check_and_run_auto_backup():
    """
    Vérifie si une sauvegarde auto est due et la lance.
    Retourne (created: bool, path: str).
    """
    try:
        from Database import db
        from datetime import datetime, timedelta

        enabled = bool(db.get_config("sauvegarde_auto", False))
        if not enabled:
            return False, ""

        interval = int(db.get_config(
            "sauvegarde_intervalle_jours", 7))

        # Dernière sauvegarde AUTO
        last = db.get_config("sauvegarde_last_auto", "")
        if last:
            try:
                last_dt = datetime.fromisoformat(last)
            except ValueError:
                last_dt = None
        else:
            last_dt = None

        now = datetime.now()
        if last_dt and (now - last_dt).days < interval:
            logger.info(
                "Backup auto : pas encore due (dernière : %s, "
                "intervalle : %d j)", last, interval)
            return False, ""

        # Lance la sauvegarde
        logger.info("Lancement de la sauvegarde auto…")
        path = create_backup(
            "auto",
            user_id=None,
            user_name="Auto")
        if path:
            db.set_config("sauvegarde_last_auto",
                          now.isoformat(), type_="str")
            logger.info("✅ Backup auto créée : %s", path)
            return True, path

        return False, ""

    except Exception:
        logger.exception("Erreur check_and_run_auto_backup")
        return False, ""