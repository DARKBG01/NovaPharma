#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/users.py — CRUD utilisateurs + permissions (Phase 2).
==============================================================
Réservé OWNER / DEVELOPER / ADMIN.

Règles :
  - Seul OWNER peut créer un ADMIN
  - Un OWNER ne peut être supprimé que par DEVELOPER
  - CAISSIER + UTILISATEUR : n'importe quel ADMIN peut créer
"""

import logging
import re
import secrets
from datetime import datetime
from typing import Optional

import bcrypt
from fastapi import APIRouter, Request, HTTPException, Query
from Database import db, audit
from Database import permissions as perms

from Server.server_models import (
    UserCreate, UserUpdate, UserResponse, UserListResponse,
    ResetPasswordResponse, SimpleResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["users"])

PAGE_SIZE_DEFAULT = 30
PHONE_REGEX = re.compile(r"^(?:\+243\d{9}|0\d{9})$")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ══════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════
def _row_to_dict(row) -> dict:
    return {k: row[k] for k in row.keys()}


def _require_admin(request: Request):
    """Vérifie OWNER / DEVELOPER / ADMIN."""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")
    is_privileged = (user.get("own") or user.get("dev")
                     or user.get("role", "").upper() == "ADMIN")
    if not is_privileged:
        raise HTTPException(403, "Réservé aux administrateurs")


def _require_owner_or_dev(request: Request):
    """Vérifie OWNER / DEVELOPER uniquement."""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")
    if not (user.get("own") or user.get("dev")):
        raise HTTPException(403, "Réservé au propriétaire ou développeur")


def _has_perm(user: dict, perm: str) -> bool:
    """Vérifie une permission granulaire (OWNER/DEV = toujours True)."""
    if user.get("own") or user.get("dev"):
        return True
    try:
        from Database import permissions as perms
        return perms.has_permission(user.get("uid"), perm)
    except Exception:
        return False


def _generate_temp_password() -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    suffix = "".join(secrets.choice(alphabet) for _ in range(4))
    return f"NOVA-{datetime.now().year}-{suffix}"


def _generate_identifiant(email: str) -> str:
    """Identifiant = email, avec suffixe .N si déjà pris."""
    base = email.lower()
    identifiant = base
    i = 1
    while db.query_one(
            "SELECT 1 FROM Utilisateur WHERE identifiant = ? LIMIT 1",
            (identifiant,)):
        i += 1
        identifiant = f"{base}.{i}"
    return identifiant


def _get_user_permissions(user_id: str) -> list:
    rows = db.query(
        "SELECT permission_key FROM UtilisateurPermission "
        "WHERE utilisateur_id = ? AND actif = 1",
        (user_id,))
    return [r["permission_key"] for r in rows]


def _set_user_permissions(user_id: str, permissions: list):
    """Remplace les permissions d'un utilisateur."""
    db.execute(
        "UPDATE UtilisateurPermission SET actif = 0 "
        "WHERE utilisateur_id = ?", (user_id,))
    for perm in permissions:
        db.execute(
            """INSERT INTO UtilisateurPermission
               (id, utilisateur_id, permission_key, actif, updated_at)
               VALUES (?, ?, ?, 1, datetime('now'))
               ON CONFLICT(utilisateur_id, permission_key) DO UPDATE
                 SET actif = 1, updated_at = datetime('now')""",
            (db.new_id(), user_id, perm))


def _preset_for_role(role: str) -> list:
    """Retourne le preset de permissions pour un rôle."""
    try:
        return perms.get_preset(role)
    except Exception:
        return []


# ══════════════════════════════════════════════════════════════════
# GET — Liste paginée
# ══════════════════════════════════════════════════════════════════
@router.get("", response_model=UserListResponse)
def list_users(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(PAGE_SIZE_DEFAULT, ge=1, le=200),
    search: str = Query(""),
    role: str = Query(""),
    actif: int = Query(-1),   # -1=tous, 0=inactifs, 1=actifs
):
    """Liste paginée des utilisateurs."""
    _require_admin(request)

    try:
        where, params = ["1=1"], []

        if search:
            where.append(
                "(prenom LIKE ? OR nom LIKE ? OR email LIKE ? "
                "OR numero LIKE ? OR identifiant LIKE ?)")
            like = f"%{search}%"
            params.extend([like, like, like, like, like])

        if role:
            where.append("role = ?")
            params.append(role)

        if actif in (0, 1):
            where.append("actif = ?")
            params.append(actif)

        wc = " AND ".join(where)

        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM Utilisateur WHERE {wc}",
            tuple(params))
        total = int(row["n"] or 0) if row else 0
        pages = max(1, (total + per_page - 1) // per_page)

        offset = (page - 1) * per_page
        rows = db.query(
            f"""SELECT id, identifiant, prenom, nom, post_nom, sexe,
                      date_naissance, nationalite, email, numero,
                      role, actif, is_owner, is_developer,
                      must_change_password, derniere_connexion,
                      created_at, path_image
                FROM Utilisateur
                WHERE {wc}
                ORDER BY is_owner DESC, is_developer DESC,
                         created_at ASC
                LIMIT ? OFFSET ?""",
            tuple(params + [per_page, offset]))

        items = [_row_to_dict(r) for r in rows]

        return {
            "total": total, "page": page,
            "per_page": per_page, "pages": pages,
            "items": items,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur list_users")
        raise HTTPException(500, f"Erreur : {e}")


# ══════════════════════════════════════════════════════════════════
# GET — Détail d'un utilisateur
# ══════════════════════════════════════════════════════════════════
@router.get("/{user_id}")
def get_user(user_id: str, request: Request):
    """Détail + permissions d'un utilisateur."""
    _require_admin(request)

    row = db.query_one(
        """SELECT id, identifiant, prenom, nom, post_nom, sexe,
                  date_naissance, nationalite, email, numero,
                  role, actif, is_owner, is_developer,
                  must_change_password, derniere_connexion,
                  created_at, path_image
           FROM Utilisateur WHERE id = ? LIMIT 1""",
        (user_id,))
    if not row:
        raise HTTPException(404, "Utilisateur introuvable")

    user = _row_to_dict(row)
    user["permissions"] = _get_user_permissions(user_id)
    return user


# ══════════════════════════════════════════════════════════════════
# POST — Créer un utilisateur
# ══════════════════════════════════════════════════════════════════
@router.post("", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, request: Request):
    """Crée un nouvel utilisateur + permissions."""
    _require_admin(request)
    current = request.state.user

    # ─── Restriction : permission `creer_admin` requise ───
    if payload.role == "ADMIN":
        if not _has_perm(current, "creer_admin"):
            raise HTTPException(
                403, "Vous n'avez pas la permission de créer "
                     "un administrateur.")

    # ─── Validation ───
    email = payload.email.strip().lower()
    numero = payload.numero.strip().replace(" ", "")

    if not EMAIL_REGEX.match(email):
        raise HTTPException(400, "Email invalide")
    if not PHONE_REGEX.match(numero):
        raise HTTPException(
            400, "Téléphone invalide (+243XXXXXXXXX ou 0XXXXXXXXX)")

    if db.query_one(
            "SELECT 1 FROM Utilisateur WHERE LOWER(email) = ? LIMIT 1",
            (email,)):
        raise HTTPException(409, f"Email déjà utilisé : {email}")
    if db.query_one(
            "SELECT 1 FROM Utilisateur WHERE numero = ? LIMIT 1",
            (numero,)):
        raise HTTPException(409, f"Numéro déjà utilisé : {numero}")

    # ─── Mot de passe ───
    pwd_plain = payload.password or _generate_temp_password()
    if len(pwd_plain) < 8:
        raise HTTPException(
            400, "Mot de passe : 8 caractères minimum")

    pwd_hash = bcrypt.hashpw(
        pwd_plain.encode("utf-8"),
        bcrypt.gensalt()).decode("utf-8")

    identifiant = _generate_identifiant(email)
    new_id = db.new_id()

    # ─── Permissions : fournies ou preset ───
    if payload.permissions:
        selected = list(payload.permissions)
    else:
        selected = _preset_for_role(payload.role)

    try:
        with db.transaction():
            db.execute(
                """INSERT INTO Utilisateur
                   (id, identifiant, prenom, nom, post_nom, sexe,
                    date_naissance, nationalite, email, numero,
                    role, pswd_hash, actif, must_change_password)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,1,?)""",
                (new_id, identifiant, payload.prenom, payload.nom,
                 payload.post_nom, payload.sexe,
                 payload.date_naissance, payload.nationalite,
                 email, numero, payload.role, pwd_hash,
                 1 if payload.must_change_password else 0))

            _set_user_permissions(new_id, selected)

            audit.log(
                audit.ACTION_CREATION_USER,
                utilisateur_id=current.get("uid"),
                utilisateur_name=current.get("ident"),
                cible_type="Utilisateur",
                cible_id=new_id,
                cible_nom=f"{payload.prenom} {payload.nom}",
                details={
                    "role": payload.role,
                    "email": email,
                    "permissions_count": len(selected),
                })

        logger.info(
            "Utilisateur créé via API : %s (%s)",
            identifiant, payload.role)

        row = db.query_one(
            """SELECT id, identifiant, prenom, nom, post_nom, sexe,
                      date_naissance, nationalite, email, numero,
                      role, actif, is_owner, is_developer,
                      must_change_password, derniere_connexion,
                      created_at, path_image
               FROM Utilisateur WHERE id = ? LIMIT 1""",
            (new_id,))
        return _row_to_dict(row)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur create_user")
        raise HTTPException(500, f"Erreur création : {e}")


# ══════════════════════════════════════════════════════════════════
# PUT — Modifier un utilisateur
# ══════════════════════════════════════════════════════════════════
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, payload: UserUpdate, request: Request):
    """Modifie un utilisateur + permissions."""
    _require_admin(request)
    current = request.state.user

    existing = db.query_one(
        "SELECT * FROM Utilisateur WHERE id = ? LIMIT 1", (user_id,))
    if not existing:
        raise HTTPException(404, "Utilisateur introuvable")

    # ─── Protection OWNER ───
    if existing["is_owner"]:
        if not (current.get("own") or current.get("dev")):
            raise HTTPException(
                403, "Seul un propriétaire ou développeur "
                     "peut modifier un OWNER.")

    # ─── Restriction : permission `creer_admin` requise pour promouvoir ───
    if payload.role and payload.role.upper() == "ADMIN":
        if not _has_perm(current, "creer_admin"):
            raise HTTPException(
                403, "Vous n'avez pas la permission de promouvoir "
                     "un administrateur.")

    # ─── Validation unicité (si modif email/numero) ───
    if payload.email:
        email_lower = payload.email.strip().lower()
        if not EMAIL_REGEX.match(email_lower):
            raise HTTPException(400, "Email invalide")
        dup = db.query_one(
            """SELECT 1 FROM Utilisateur
               WHERE LOWER(email) = ? AND id <> ? LIMIT 1""",
            (email_lower, user_id))
        if dup:
            raise HTTPException(409, "Email déjà utilisé")

    if payload.numero:
        numero_clean = payload.numero.strip().replace(" ", "")
        if not PHONE_REGEX.match(numero_clean):
            raise HTTPException(400, "Téléphone invalide")
        dup = db.query_one(
            """SELECT 1 FROM Utilisateur
               WHERE numero = ? AND id <> ? LIMIT 1""",
            (numero_clean, user_id))
        if dup:
            raise HTTPException(409, "Numéro déjà utilisé")

    try:
        # ─── Champs à modifier ───
        champs, params = [], []

        simple_map = {
            "prenom": payload.prenom,
            "nom": payload.nom,
            "post_nom": payload.post_nom,
            "sexe": payload.sexe,
            "date_naissance": payload.date_naissance,
            "nationalite": payload.nationalite,
            "role": payload.role,
            "actif": payload.actif,
            "must_change_password": payload.must_change_password,
        }
        for field, val in simple_map.items():
            if val is not None:
                champs.append(f"{field} = ?")
                params.append(val)

        if payload.email:
            champs.append("email = ?")
            params.append(payload.email.strip().lower())
        if payload.numero:
            champs.append("numero = ?")
            params.append(payload.numero.strip().replace(" ", ""))

        if payload.password:
            if len(payload.password) < 8:
                raise HTTPException(
                    400, "Mot de passe : 8 caractères minimum")
            pwd_hash = bcrypt.hashpw(
                payload.password.encode("utf-8"),
                bcrypt.gensalt()).decode("utf-8")
            champs.append("pswd_hash = ?")
            params.append(pwd_hash)

        if not champs and payload.permissions is None:
            raise HTTPException(400, "Aucun champ à modifier")

        with db.transaction():
            if champs:
                params.append(user_id)
                db.execute(
                    f"UPDATE Utilisateur SET {', '.join(champs)} "
                    f"WHERE id = ?",
                    tuple(params))

            # ─── Permissions ───
            if payload.permissions is not None:
                _set_user_permissions(user_id, payload.permissions)

            audit.log(
                audit.ACTION_MODIF_INFO_USER,
                utilisateur_id=current.get("uid"),
                utilisateur_name=current.get("ident"),
                cible_type="Utilisateur",
                cible_id=user_id,
                cible_nom=existing["identifiant"],
                details={
                    "champs_modifies": [c.split(" = ")[0]
                                        for c in champs],
                    "permissions_updated":
                        payload.permissions is not None,
                })

        logger.info("Utilisateur modifié : %s", user_id)

        row = db.query_one(
            """SELECT id, identifiant, prenom, nom, post_nom, sexe,
                      date_naissance, nationalite, email, numero,
                      role, actif, is_owner, is_developer,
                      must_change_password, derniere_connexion,
                      created_at, path_image
               FROM Utilisateur WHERE id = ? LIMIT 1""",
            (user_id,))
        return _row_to_dict(row)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur update_user")
        raise HTTPException(500, f"Erreur modification : {e}")


# ══════════════════════════════════════════════════════════════════
# POST — Reset du mot de passe
# ══════════════════════════════════════════════════════════════════
@router.post("/{user_id}/reset-password",
             response_model=ResetPasswordResponse)
def reset_password(user_id: str, request: Request):
    """Génère un mot de passe temporaire NOVA-YYYY-XXXX."""
    _require_admin(request)
    current = request.state.user

    existing = db.query_one(
        "SELECT is_owner, identifiant FROM Utilisateur WHERE id = ? LIMIT 1",
        (user_id,))
    if not existing:
        raise HTTPException(404, "Utilisateur introuvable")

    # ─── Protection OWNER ───
    if existing["is_owner"]:
        if not (current.get("own") or current.get("dev")):
            raise HTTPException(
                403, "Seul un propriétaire ou développeur "
                     "peut reset le mot de passe d'un OWNER.")

    try:
        temp_password = _generate_temp_password()
        pwd_hash = bcrypt.hashpw(
            temp_password.encode("utf-8"),
            bcrypt.gensalt()).decode("utf-8")

        with db.transaction():
            db.execute(
                "UPDATE Utilisateur SET pswd_hash = ?, "
                "must_change_password = 1 WHERE id = ?",
                (pwd_hash, user_id))

            audit.log(
                audit.ACTION_RESET_MOT_DE_PASSE,
                utilisateur_id=current.get("uid"),
                utilisateur_name=current.get("ident"),
                cible_type="Utilisateur",
                cible_id=user_id,
                cible_nom=existing["identifiant"],
                details={"method": "admin_reset_api"},
                severite="warning")

        logger.info("Mot de passe réinitialisé : %s", user_id)

        return {
            "user_id": user_id,
            "temp_password": temp_password,
            "message": "Mot de passe réinitialisé — "
                       "l'utilisateur devra le changer à la connexion.",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur reset_password")
        raise HTTPException(500, f"Erreur reset : {e}")


# ══════════════════════════════════════════════════════════════════
# DELETE — Désactiver un utilisateur (soft delete)
# ══════════════════════════════════════════════════════════════════
@router.delete("/{user_id}", response_model=SimpleResponse)
def delete_user(user_id: str, request: Request):
    """Désactive un utilisateur (actif = 0)."""
    _require_admin(request)
    current = request.state.user

    existing = db.query_one(
        "SELECT is_owner, identifiant, actif FROM Utilisateur "
        "WHERE id = ? LIMIT 1",
        (user_id,))
    if not existing:
        raise HTTPException(404, "Utilisateur introuvable")

    # ─── Protection OWNER : seul DEV peut désactiver ───
    if existing["is_owner"]:
        if not current.get("dev"):
            raise HTTPException(
                403, "Seul le développeur peut désactiver un OWNER.")

    # ─── On ne se désactive pas soi-même ───
    if user_id == current.get("uid"):
        raise HTTPException(
            400, "Vous ne pouvez pas désactiver votre propre compte.")

    if not existing["actif"]:
        raise HTTPException(400, "Utilisateur déjà inactif")

    try:
        with db.transaction():
            db.execute(
                "UPDATE Utilisateur SET actif = 0 WHERE id = ?",
                (user_id,))

            audit.log(
                audit.ACTION_DESACTIVATION_USER,
                utilisateur_id=current.get("uid"),
                utilisateur_name=current.get("ident"),
                cible_type="Utilisateur",
                cible_id=user_id,
                cible_nom=existing["identifiant"],
                severite="warning")

        logger.info("Utilisateur désactivé : %s", user_id)
        return {
            "status": "ok",
            "message": f"Utilisateur '{existing['identifiant']}' désactivé",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur delete_user")
        raise HTTPException(500, f"Erreur désactivation : {e}")