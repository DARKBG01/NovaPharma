#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/auth.py — Authentification.
===================================
POST /api/auth/login   → { token, user }
POST /api/auth/logout  → invalide le token
GET  /api/auth/me      → infos utilisateur courant (enrichi)
"""

import logging

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from Database import db
from Server import server_auth as auth
from Server import server_config as cfg

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])


# ══════════════════════════════════════════════════════════════════
class LoginRequest(BaseModel):
    identifiant: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: dict


# ══════════════════════════════════════════════════════════════════
@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, request: Request):   # ← AJOUT request
    """Authentifie un utilisateur et retourne un token."""
    user = auth.verify_login(req.identifiant, req.password)
    if user is None:
        try:
            from Database import audit
            audit.log(
                audit.ACTION_ECHEC_CONNEXION,
                utilisateur_name=req.identifiant,
                details={"source": "server",
                         "reason": "invalid_credentials"})
        except Exception:
            pass
        raise HTTPException(401, "Identifiant ou mot de passe incorrect")

    # ─── Mise à jour derniere_connexion ───
    try:
        db.execute(
            "UPDATE Utilisateur "
            "SET derniere_connexion = datetime('now') "
            "WHERE id = ?",
            (user["id"],))
    except Exception:
        logger.exception("Erreur maj derniere_connexion")

    # ─── Détection fiable client / serveur ───
    client_kind = request.headers.get("X-Client-Kind", "").lower()
    is_remote = (client_kind == "client")

    if is_remote:
        role = (user.get("role") or "").upper()
        is_privileged = (user.get("is_owner")
                         or user.get("is_developer")
                         or role == "ADMIN")

        if is_privileged:
            allow = bool(db.get_config("allow_admin_on_client", True))
            if not allow:
                try:
                    from Database import audit
                    audit.log(
                        "CONNEXION_ADMIN_REFUSEE",
                        utilisateur_name=user["identifiant"],
                        cible_type="user",
                        cible_id=user["id"],
                        details={
                            "ip": request.client.host if request.client else None,
                            "hostname": request.headers.get("X-Client-Hostname", "—"),
                            "role": role,
                            "reason": "admin_on_client_disabled",
                        },
                        severite="warning")
                except Exception:
                    pass
                raise HTTPException(
                    403,
                    "Les connexions ADMIN/OWNER/DEVELOPER sont "
                    "désactivées sur les postes clients. "
                    "Contactez l'administrateur réseau.")

    duree = cfg.get("token_duree_jours") or 365
    token = auth.create_token(user, duree_jours=int(duree))

    # ─── Audit enrichi ───
    try:
        from Database import audit
        audit.log(
            audit.ACTION_CONNEXION,
            utilisateur_id=user["id"],
            utilisateur_name=user["identifiant"],
            cible_type="user", cible_id=user["id"],
            details={
                "source": "client" if is_remote else "serveur",
                "role": user["role"],
                "ip": request.client.host if request.client else None,
                "hostname": request.headers.get("X-Client-Hostname", "—"),
            },
            ip_address=request.client.host if request.client else None,
            machine_name=request.headers.get("X-Client-Hostname"),
            severite=(
                "warning"
                if (is_remote and (user.get("is_owner")
                                   or user.get("is_developer")))
                else "info"),
        )
    except Exception:
        pass

    logger.info("Login réussi : %s (%s)",
                user["identifiant"],
                "client" if is_remote else "serveur")
    return {"token": token, "user": user}


# ══════════════════════════════════════════════════════════════════
@router.post("/logout")
def logout(request: Request):
    """Invalide le token courant."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
        auth.invalidate_token(token)

    user = getattr(request.state, "user", {})
    if user:
        try:
            from Database import audit
            audit.log(
                audit.ACTION_DECONNEXION,
                utilisateur_id=user.get("uid"),
                utilisateur_name=user.get("ident"),
                details={"source": "server"})
        except Exception:
            pass

    return {"status": "ok", "message": "Déconnecté"}


# ══════════════════════════════════════════════════════════════════
@router.get("/me")
def me(request: Request):
    """
    Retourne les infos COMPLÈTES de l'utilisateur connecté (point 12).
    Utilisé par Setting_main_window._setup_user_profile côté client.
    """
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")

    try:
        row = db.query_one(
            """SELECT id, identifiant, prenom, nom, post_nom, sexe,
                      email, numero, role, path_image, actif,
                      is_owner, is_developer, derniere_connexion,
                      created_at
               FROM Utilisateur WHERE id = ? LIMIT 1""",
            (user["uid"],))

        if not row:
            raise HTTPException(404, "Utilisateur introuvable")

        return {
            "id": row["id"],
            "identifiant": row["identifiant"],
            "prenom": row["prenom"] or "",
            "nom": row["nom"] or "",
            "post_nom": row["post_nom"] or "",
            "sexe": row["sexe"] or "M",
            "email": row["email"] or "",
            "numero": row["numero"] or "",
            "role": row["role"],
            "path_image": row["path_image"],
            "actif": int(row["actif"] or 0),
            "is_owner": bool(row["is_owner"]),
            "is_developer": bool(row["is_developer"]),
            "derniere_connexion": row["derniere_connexion"],
            "created_at": row["created_at"],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur /api/auth/me")
        raise HTTPException(500, str(e))


# ══════════════════════════════════════════════════════════════════
# POST — Changement de mot de passe (self-service)
# ══════════════════════════════════════════════════════════════════
class ChangePasswordRequest(BaseModel):
    ancien_password: str
    nouveau_password: str


@router.post("/change-password")
def change_password(payload: ChangePasswordRequest, request: Request):
    """
    Change le mot de passe de l'utilisateur connecté.
    Vérifie l'ancien mot de passe (obligatoire).
    """
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")

    try:
        # ─── Vérifie ancien mot de passe ───
        row = db.query_one(
            "SELECT pswd_hash FROM Utilisateur WHERE id = ? LIMIT 1",
            (user["uid"],))
        if not row:
            raise HTTPException(404, "Utilisateur introuvable")

        import bcrypt
        try:
            ok = bcrypt.checkpw(
                payload.ancien_password.encode("utf-8"),
                row["pswd_hash"].encode("utf-8"))
        except Exception:
            ok = False

        if not ok:
            raise HTTPException(400, "Ancien mot de passe incorrect")

        # ─── Valide nouveau ───
        if len(payload.nouveau_password) < 8:
            raise HTTPException(
                400, "Le nouveau mot de passe doit contenir au moins "
                     "8 caractères")
        if payload.nouveau_password == payload.ancien_password:
            raise HTTPException(
                400, "Le nouveau mot de passe doit être différent de "
                     "l'ancien")

        # ─── Hash + UPDATE ───
        new_hash = bcrypt.hashpw(
            payload.nouveau_password.encode("utf-8"),
            bcrypt.gensalt()).decode("utf-8")

        with db.transaction():
            db.execute(
                "UPDATE Utilisateur SET "
                "pswd_hash = ?, must_change_password = 0 "
                "WHERE id = ?",
                (new_hash, user["uid"]))

        # ─── Audit ───
        try:
            from Database import audit
            audit.log(
                audit.ACTION_MODIF_MOT_DE_PASSE,
                utilisateur_id=user["uid"],
                utilisateur_name=user.get("ident"),
                cible_type="user",
                cible_id=user["uid"],
                cible_nom=user.get("ident"),
                details={"method": "self_change_client",
                         "ip": request.client.host
                         if request.client else None})
        except Exception:
            logger.exception("Erreur audit mdp")

        logger.info("Mdp changé via API : %s", user.get("ident"))
        return {"status": "ok", "message": "Mot de passe modifié"}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur change-password")
        raise HTTPException(500, str(e))