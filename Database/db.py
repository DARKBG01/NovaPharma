"""
NovaPharma — Couche d'accès à la base de données.
Connexion unique + gestion transactionnelle ROBUSTE + multi-thread.

⚠️  Le flag `check_same_thread=False` et le verrou `_db_lock` sont
    nécessaires pour le serveur FastAPI (multi-thread).
"""

import sqlite3
import uuid
import hashlib
import threading
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime

# ------------------------------------------------------------------
# Chemins
# ------------------------------------------------------------------
DB_DIR  = Path(__file__).parent
DB_PATH = DB_DIR / "NovaPharma.db"
SCHEMA  = DB_DIR / "schema.sql"

# ------------------------------------------------------------------
# Connexion globale
# ------------------------------------------------------------------
_conn: sqlite3.Connection | None = None
_tx_depth: int = 0   # profondeur de transaction (pour gérer les imbrications)

# ══════════════════════════════════════════════════════════════════
# Verrou multi-thread
# ══════════════════════════════════════════════════════════════════
# SQLite n'aime pas les accès concurrents, même avec WAL.
# Ce RLock sérialise tous les accès (query / execute / transaction).
# RLock = réentrant → permet d'appeler query() depuis transaction().
_db_lock = threading.RLock()


def get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        first_time = not DB_PATH.exists()
        # isolation_level=None  → mode autocommit explicite
        # check_same_thread=False → autorise plusieurs threads
        _conn = sqlite3.connect(
            DB_PATH,
            isolation_level=None,
            check_same_thread=False,
        )
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA foreign_keys = ON")
        _conn.execute("PRAGMA journal_mode = WAL")
        _conn.execute("PRAGMA busy_timeout = 5000")
        if first_time:
            _apply_schema(_conn)
    return _conn


def close() -> None:
    global _conn, _tx_depth
    with _db_lock:
        if _conn is not None:
            try:
                if _tx_depth > 0:
                    _conn.execute("ROLLBACK")
            except Exception:
                pass
            _conn.close()
            _conn = None
            _tx_depth = 0


def _apply_schema(conn: sqlite3.Connection) -> None:
    if not SCHEMA.exists():
        raise FileNotFoundError(f"Schéma introuvable : {SCHEMA}")
    with SCHEMA.open("r", encoding="utf-8") as f:
        conn.executescript(f.read())


# ------------------------------------------------------------------
# Requêtes
# ------------------------------------------------------------------
def query(sql: str, params: tuple = ()) -> list[sqlite3.Row]:
    with _db_lock:
        return get_conn().execute(sql, params).fetchall()


def query_one(sql: str, params: tuple = ()) -> sqlite3.Row | None:
    with _db_lock:
        return get_conn().execute(sql, params).fetchone()


def execute(sql: str, params: tuple = ()) -> sqlite3.Cursor:
    """Exécute une requête. Commit auto SI on n'est pas dans une transaction."""
    with _db_lock:
        conn = get_conn()
        cur = conn.execute(sql, params)
        if _tx_depth == 0:
            conn.commit()
        return cur


def executemany(sql: str, seq_params: list[tuple]) -> None:
    with _db_lock:
        conn = get_conn()
        conn.executemany(sql, seq_params)
        if _tx_depth == 0:
            conn.commit()


# ══════════════════════════════════════════════════════════════════
# Transaction robuste (support de l'imbrication + multi-thread)
# ══════════════════════════════════════════════════════════════════
@contextmanager
def transaction():
    """
    Utilisation :
        with db.transaction():
            db.execute(...)
            db.set_config(...)
            db.record_consent(...)
        # → COMMIT si pas d'erreur, ROLLBACK sinon
    """
    global _tx_depth
    with _db_lock:
        conn = get_conn()
        _tx_depth += 1

        if _tx_depth == 1:
            conn.execute("BEGIN")

        try:
            yield conn
        except Exception:
            _tx_depth -= 1
            if _tx_depth == 0:
                try:
                    conn.execute("ROLLBACK")
                except Exception:
                    pass
            raise
        else:
            _tx_depth -= 1
            if _tx_depth == 0:
                conn.execute("COMMIT")


# ------------------------------------------------------------------
# Configuration (clé/valeur typée)
# ------------------------------------------------------------------
def _cast(valeur: str, type_: str):
    if type_ == "int":   return int(valeur)
    if type_ == "float": return float(valeur)
    if type_ == "bool":  return valeur == "1"
    if type_ == "json":
        import json
        return json.loads(valeur)
    return valeur


def _uncast(valeur, type_: str) -> str:
    if type_ == "bool":  return "1" if valeur else "0"
    if type_ == "json":
        import json
        return json.dumps(valeur, ensure_ascii=False)
    return str(valeur)


def get_config(cle: str, default=None):
    row = query_one("SELECT valeur, type FROM Configuration WHERE cle = ?", (cle,))
    if row is None:
        return default
    return _cast(row["valeur"], row["type"])


def set_config(cle: str, valeur, type_: str | None = None,
               description: str | None = None) -> None:
    if type_ is None:
        if isinstance(valeur, bool):          type_ = "bool"
        elif isinstance(valeur, int):         type_ = "int"
        elif isinstance(valeur, float):       type_ = "float"
        elif isinstance(valeur, (dict, list)): type_ = "json"
        else:                                 type_ = "str"

    execute(
        """INSERT INTO Configuration (cle, valeur, type, description, updated_at)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(cle) DO UPDATE SET
               valeur = excluded.valeur,
               type = excluded.type,
               description = COALESCE(excluded.description, Configuration.description),
               updated_at = excluded.updated_at""",
        (cle, _uncast(valeur, type_), type_, description,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def all_config() -> dict:
    return {row["cle"]: _cast(row["valeur"], row["type"])
            for row in query("SELECT * FROM Configuration")}


# ------------------------------------------------------------------
# Utilitaires
# ------------------------------------------------------------------
def new_id() -> str:
    return str(uuid.uuid4())


def hash_sha256(texte: str) -> str:
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def record_consent(utilisateur_id: str, type_consentement: str,
                   version: str, accepte: bool, texte: str) -> None:
    execute(
        """INSERT INTO Consentement
           (id, utilisateur_id, type, version_texte, accepte, empreinte)
           VALUES (?,?,?,?,?,?)""",
        (new_id(), utilisateur_id, type_consentement,
         version, 1 if accepte else 0, hash_sha256(texte))
    )


def next_compteur(cle: str, annee: int | None = None) -> int:
    if annee is None:
        annee = datetime.now().year
    conn = get_conn()
    row = conn.execute(
        "SELECT valeur FROM Compteur WHERE cle = ? AND annee = ?",
        (cle, annee)
    ).fetchone()
    if row is None:
        execute("INSERT INTO Compteur (cle, annee, valeur) VALUES (?,?,1)",
                (cle, annee))
        return 1
    nouvelle = row["valeur"] + 1
    execute("UPDATE Compteur SET valeur = ? WHERE cle = ? AND annee = ?",
            (nouvelle, cle, annee))
    return nouvelle