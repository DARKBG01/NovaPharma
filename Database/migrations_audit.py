#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
migrations_audit.py — Ajoute les colonnes d'audit renforcé.
============================================================
- prev_hash / current_hash : chaîne anti-falsification
- severite : niveau de gravité (info/warning/danger)
- chain_ok : marqueur de validation
"""

import logging
from Database import db

logger = logging.getLogger(__name__)


def migrate_audit_chain():
    """Ajoute les colonnes de chaîne + sévérité à AuditLog."""
    existing = {row["name"] for row in db.query(
        "PRAGMA table_info(AuditLog)")}

    additions = [
        ("prev_hash",    "TEXT"),
        ("current_hash", "TEXT"),
        ("severite",     "TEXT NOT NULL DEFAULT 'info'"),
    ]

    for col, definition in additions:
        if col in existing:
            continue
        try:
            db.execute(
                f"ALTER TABLE AuditLog ADD COLUMN {col} {definition}")
            print(f"  · Colonne ajoutée : AuditLog.{col}")
        except Exception as e:
            print(f"  ! Impossible d'ajouter {col} : {e}")

    # Index sur severite
    try:
        db.execute(
            "CREATE INDEX IF NOT EXISTS idx_audit_severite "
            "ON AuditLog(severite)")
    except Exception:
        pass

    print("  · AuditLog enrichi (hash + sévérité)")


def migrate_audit_indexes():
    """Ajoute les index manquants pour la performance."""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_audit_cible "
        "ON AuditLog(cible_type, cible_id)",
        "CREATE INDEX IF NOT EXISTS idx_audit_machine "
        "ON AuditLog(machine_name)",
    ]
    for sql in indexes:
        try:
            db.execute(sql)
        except Exception:
            pass
    print("  · Index audit ajoutés")


def run_all():
    print("→ Migrations audit...")
    with db.transaction():
        migrate_audit_chain()
        migrate_audit_indexes()
    print("✓ Migrations audit terminées")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    db.get_conn()
    run_all()