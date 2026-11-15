#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routes/auth.py — Authentification.
===================================
POST /api/auth/login   → { token, user }
POST /api/auth/logout  → invalide le token
GET  /api/auth/me      → infos utilisateur courant (enrichi)
POST /api/auth/change-password → self-service
"""

import logging
import socket
import time

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from Database import db
from Server import server_auth as auth
from Server import server_config as cfg

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])

# ─── Anti-bruteforce serveur ───
_login_attempts = {}  # { "ip_identifiant": (count, last_attempt_time) }
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME_SEC = 300  # 5 minutes


# ══════════════════════════════════════════════════════════════════
class LoginRequest(BaseModel):
    identifiant: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: dict


# ══════════════════════════════════════════════════════════════════
# POST — Validation de machine (avant login, sans token)
# ══════════════════════════════════════════════════════════════════
class ValidateMachineRequest(BaseModel):
    machine_id: str
    hostname: str = ""
    role_attempt: str = "ADMIN"


class ValidateMachineResponse(BaseModel):
    allowed: bool
    reason: str


@router.post("/validate-machine", response_model=ValidateMachineResponse)
def validate_machine(payload: ValidateMachineRequest, request: Request):
    """Vérifie si cette machine peut se connecter avec le rôle demandé."""
    client_kind = request.headers.get("X-Client-Kind", "").lower()
    is_remote = (client_kind == "client")

    if not is_remote:
        return {"allowed": True, "reason": "physical_server"}

    role_upper = (payload.role_attempt or "").upper()
    if role_upper not in ("ADMIN", "OWNER", "DEV", "DEVELOPER"):
        return {"allowed": True, "reason": "non_privileged_role"}

    try:
        machine = db.query_one(
            """SELECT role_autorise FROM MonitoringMachine
               WHERE machine_id = ? AND actif = 1 LIMIT 1""",
            (payload.machine_id,))
    except Exception:
        logger.exception("Erreur lecture MonitoringMachine")
        return {"allowed": False, "reason": "db_error"}

    if machine:
        role_autorise = (machine["role_autorise"] or "ALL").upper()
        role_normalized = "DEV" if role_upper == "DEVELOPER" else role_upper

        if role_autorise == "ALL":
            return {"allowed": True, "reason": "whitelisted_all"}
        if role_autorise == role_normalized:
            return {"allowed": True, "reason": "whitelisted_role"}
        return {
            "allowed": False,
            "reason": f"role_mismatch ({role_autorise} ≠ {role_normalized})",
        }

    try:
        allow = bool(db.get_config("allow_admin_on_client", True))
    except Exception:
        allow = True

    if allow:
        return {"allowed": True, "reason": "degraded_mode"}
    return {"allowed": False, "reason": "not_whitelisted"}


# ══════════════════════════════════════════════════════════════════
# POST — Login
# ══════════════════════════════════════════════════════════════════
@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, request: Request):
    """Authentifie un utilisateur et retourne un token."""

    # ═══════════════════════════════════════════════════════════════
    # VÉRIFICATION LICENCE SERVEUR (avant tout)
    # Si la licence serveur est expirée, AUCUNE connexion n'est permise
    # ═══════════════════════════════════════════════════════════════
    try:
        from Core.license_manager import check_license_and_trial
        # On est sur le serveur → on force le check (pas de skip client)
        # (is_client_mode() retourne False ici car le serveur n'importe pas le client_api)
        ok, days, msg = check_license_and_trial()
        if not ok:
            logger.warning(
                "Login refusé — licence serveur expirée : %s", msg)
            raise HTTPException(402, msg)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Erreur vérification licence serveur")
        # Si l'erreur n'est pas bloquante (ex: import), on continue
        # mais on log l'incident

    # ─── 1. Vérification Anti-Bruteforce ───
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    key = f"{client_ip}_{req.identifiant.lower()}"

    if key in _login_attempts:
        count, last_time = _login_attempts[key]
        if count >= MAX_LOGIN_ATTEMPTS:
            if now - last_time < LOCKOUT_TIME_SEC:
                raise HTTPException(
                    429,
                    "Trop de tentatives échouées. Réessayez dans 5 minutes."
                )
            else:
                del _login_attempts[key]

    # ─── 2. Vérification des identifiants ───
    user = auth.verify_login(req.identifiant, req.password)

    if user is None:
        # Enregistrer l'échec
        count, _ = _login_attempts.get(key, (0, now))
        _login_attempts[key] = (count + 1, now)

        try:
            from Database import audit
            audit.log(
                audit.ACTION_ECHEC_CONNEXION,
                utilisateur_name=req.identifiant,
                details={"source": "server", "reason": "invalid_credentials"})
        except Exception:
            pass
        raise HTTPException(401, "Identifiant ou mot de passe incorrect")

    # ─── 3. Succès : Reset le compteur d'échecs ───
    if key in _login_attempts:
        del _login_attempts[key]

    # ─── 4. Mise à jour derniere_connexion ───
    try:
        db.execute(
            "UPDATE Utilisateur SET derniere_connexion = datetime('now') "
            "WHERE id = ?", (user["id"],))
    except Exception:
        logger.exception("Erreur maj derniere_connexion")

    # ═══════════════════════════════════════════════════════════════
    # 5. DÉTECTION CLIENT + VÉRIFICATION MONITORING
    # ═══════════════════════════════════════════════════════════════
    client_kind = request.headers.get("X-Client-Kind", "").lower()
    is_remote = (client_kind == "client")

    role_upper = (user.get("role") or "").upper()
    is_owner = bool(user.get("is_owner"))
    is_developer = bool(user.get("is_developer"))
    is_privileged = (is_owner or is_developer or role_upper == "ADMIN")

    machine_id = request.headers.get("X-Client-Machine-ID", "")
    hostname = request.headers.get("X-Client-Hostname", "") or socket.gethostname()
    ip_client = request.client.host if request.client else None

    if is_owner:
        role_type = "OWNER"
    elif is_developer:
        role_type = "DEV"
    elif role_upper == "ADMIN":
        role_type = "ADMIN"
    else:
        role_type = "NORMAL"

    # Si client ET rôle privilégié → vérif MonitoringMachine
    if is_remote and is_privileged:
        try:
            machine = db.query_one(
                """SELECT role_autorise FROM MonitoringMachine
                   WHERE machine_id = ? AND actif = 1 LIMIT 1""",
                (machine_id,))
        except Exception:
            machine = None
            logger.exception("Erreur lecture MonitoringMachine")

        machine_ok = False
        role_autorise = ""

        if machine:
            role_autorise = (machine["role_autorise"] or "ALL").upper()
            if role_autorise == "ALL" or role_autorise == role_type:
                machine_ok = True

        # Cas A : machine whitelistée et rôle OK
        if machine_ok:
            try:
                from Database import audit
                audit.log(
                    audit.ACTION_CONNEXION_ADMIN_MONITORING,
                    utilisateur_id=user["id"],
                    utilisateur_name=user["identifiant"],
                    cible_type="user",
                    cible_id=user["id"],
                    cible_nom=user["identifiant"],
                    details={
                        "role": role_type, "machine_id": machine_id,
                        "hostname": hostname, "role_autorise": role_autorise,
                        "ip": ip_client, "reason": "whitelisted",
                    },
                    ip_address=ip_client, machine_name=hostname, severite="warning")
            except Exception:
                pass

        # Cas B : pas whitelistée → fallback allow_admin_on_client
        else:
            try:
                allow = bool(db.get_config("allow_admin_on_client", True))
            except Exception:
                allow = True

            if not allow:
                try:
                    from Database import audit
                    audit.log(
                        audit.ACTION_CONNEXION_ADMIN_REFUSEE,
                        utilisateur_id=user["id"],
                        utilisateur_name=user["identifiant"],
                        cible_type="user", cible_id=user["id"],
                        cible_nom=user["identifiant"],
                        details={
                            "role": role_type, "machine_id": machine_id,
                            "hostname": hostname, "ip": ip_client,
                            "reason": "role_mismatch" if machine else "not_whitelisted",
                        },
                        ip_address=ip_client, machine_name=hostname, severite="danger")
                except Exception:
                    pass

                raise HTTPException(
                    403,
                    "Ce poste n'est pas autorisé pour ce rôle. "
                    "Contactez l'administrateur réseau.")

            # Autorisé en mode dégradé
            try:
                from Database import audit
                audit.log(
                    audit.ACTION_CONNEXION_ADMIN_NON_WHITELISTEE,
                    utilisateur_id=user["id"],
                    utilisateur_name=user["identifiant"],
                    cible_type="user", cible_id=user["id"],
                    cible_nom=user["identifiant"],
                    details={
                        "role": role_type, "machine_id": machine_id,
                        "hostname": hostname, "ip": ip_client,
                        "reason": "degraded_mode",
                    },
                    ip_address=ip_client, machine_name=hostname, severite="warning")
            except Exception:
                pass

    # ─── 6. Token ───
    duree = cfg.get("token_duree_jours") or 365
    token = auth.create_token(user, duree_jours=int(duree))

    # ─── 7. Audit CONNEXION standard ───
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
                "ip": ip_client,
                "hostname": hostname,
            },
            ip_address=ip_client,
            machine_name=hostname if is_remote else None,
            severite="warning" if (is_remote and is_privileged) else "info",
        )
    except Exception:
        pass

    logger.info("Login réussi : %s (%s)",
                user["identifiant"],
                "client" if is_remote else "serveur")

    return {"token": token, "user": user}


# ══════════════════════════════════════════════════════════════════
# POST — Logout
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
# GET — Me
# ══════════════════════════════════════════════════════════════════
@router.get("/me")
def me(request: Request):
    """Retourne les infos COMPLÈTES de l'utilisateur connecté."""
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
# POST — Change Password
# ══════════════════════════════════════════════════════════════════
class ChangePasswordRequest(BaseModel):
    ancien_password: str
    nouveau_password: str


@router.post("/change-password")
def change_password(payload: ChangePasswordRequest, request: Request):
    """Change le mot de passe de l'utilisateur connecté."""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Non authentifié")

    try:
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

        if len(payload.nouveau_password) < 8:
            raise HTTPException(
                400, "Le nouveau mot de passe doit contenir au moins 8 caractères")
        if payload.nouveau_password == payload.ancien_password:
            raise HTTPException(
                400, "Le nouveau mot de passe doit être différent de l'ancien")

        new_hash = bcrypt.hashpw(
            payload.nouveau_password.encode("utf-8"),
            bcrypt.gensalt()).decode("utf-8")

        with db.transaction():
            db.execute(
                "UPDATE Utilisateur SET pswd_hash = ?, must_change_password = 0 "
                "WHERE id = ?",
                (new_hash, user["uid"]))

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
                         "ip": request.client.host if request.client else None})
        except Exception:
            pass

        logger.info("Mdp changé via API : %s", user.get("ident"))
        return {"status": "ok", "message": "Mot de passe modifié"}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Erreur change-password")
        raise HTTPException(500, str(e))