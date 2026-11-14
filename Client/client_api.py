#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
client_api.py — Client HTTP pour l'app Nova Pharma.
====================================================
Utilisé par l'UI PySide pour communiquer avec le serveur.
Gère le token (stockage QSettings) et les erreurs.
"""

import logging
import socket
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
class NovaApiError(Exception):
    """Exception levée en cas d'erreur API."""
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


# ══════════════════════════════════════════════════════════════════
class NovaApiClient:
    """Client HTTP pour l'API Nova Pharma."""

    def __init__(self, base_url: str = "http://127.0.0.1:5001",
                 timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token: Optional[str] = None
        self.user: Optional[dict] = None

    # ══════════════════════════════════════════════════════════════

    # ✅ APRÈS
    def _headers(self) -> dict:
        h = {
            "Content-Type": "application/json",
            "X-Client-Kind": "client",
            "X-Client-Hostname": socket.gethostname(),
        }
        # ─── Identité machine (requis par Phase 1 monitoring) ───
        try:
            from Database import machine_id
            h["X-Client-Machine-ID"] = machine_id.get_machine_id()
        except Exception:
            h["X-Client-Machine-ID"] = "unknown"

        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _request(self, method: str, path: str, **kwargs) -> dict:
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                r = client.request(
                    method, url, headers=self._headers(), **kwargs)

            if r.status_code == 401:
                raise NovaApiError("Non authentifié", 401)
            if r.status_code == 403:
                raise NovaApiError("Accès refusé", 403)
            if r.status_code == 503:
                detail = r.json().get("detail", "Serveur fermé")
                raise NovaApiError(detail, 503)
            if r.status_code >= 400:
                try:
                    msg = r.json().get("detail") or r.json().get("error")
                except Exception:
                    msg = r.text
                raise NovaApiError(msg or "Erreur serveur", r.status_code)

            return r.json()

        except httpx.ConnectError:
            raise NovaApiError("Serveur indisponible", 0)
        except httpx.TimeoutException:
            raise NovaApiError("Délai dépassé", 0)
        except NovaApiError:
            raise
        except Exception as e:
            logger.exception("Erreur API")
            raise NovaApiError(str(e))

    # ══════════════════════════════════════════════════════════════
    # Health
    # ══════════════════════════════════════════════════════════════
    def sante(self) -> dict:
        """Ping du serveur."""
        return self._request("GET", "/api/sante")

    def is_available(self) -> bool:
        """Vrai si le serveur répond."""
        try:
            self.sante()
            return True
        except Exception:
            return False

    # ══════════════════════════════════════════════════════════════
    # Auth
    # ══════════════════════════════════════════════════════════════
    def login(self, identifiant: str, password: str) -> dict:
        data = self._request(
            "POST", "/api/auth/login",
            json={"identifiant": identifiant, "password": password})
        self.token = data["token"]
        self.user = data["user"]

        # ─── Persiste le token (au cas où) ───
        try:
            from PySide6 import QtCore
            s = QtCore.QSettings("NovaPharma", "Client")
            s.setValue("auth/token", self.token)
        except Exception:
            pass

        return data

    def logout(self) -> dict:
        """Déconnecte et efface le token."""
        try:
            r = self._request("POST", "/api/auth/logout")
        finally:
            self.token = None
            self.user = None
        return r

    def change_password(self, ancien_password: str,
                        nouveau_password: str) -> dict:
        """Change le mot de passe de l'utilisateur connecté."""
        if not self.token:
            logger.warning(
                "change_password : token absent, tentative de rechargement")
            # Optionnel : recharge depuis les settings si stocké
            try:
                from PySide6 import QtCore
                s = QtCore.QSettings("NovaPharma", "Client")
                tok = s.value("auth/token", "", type=str)
                if tok:
                    self.token = tok
                    logger.info("Token rechargé depuis QSettings")
            except Exception:
                pass

        if not self.token:
            raise NovaApiError(
                "Session expirée — reconnectez-vous", 401)

        return self._request(
            "POST", "/api/auth/change-password",
            json={
                "ancien_password": ancien_password,
                "nouveau_password": nouveau_password,
            })

    def me(self) -> dict:
        """Infos du token courant."""
        return self._request("GET", "/api/auth/me")
    
    # ══════════════════════════════════════════════════════════════
    # Produits
    # ══════════════════════════════════════════════════════════════
    def list_produits(self, page: int = 1, per_page: int = 50,
                      search: str = "", categorie: str = "",
                      actif: int = 1, rupture: bool = False) -> dict:
        """Liste paginée des produits."""
        params = {"page": page, "per_page": per_page, "actif": actif}
        if search:
            params["search"] = search
        if categorie:
            params["categorie"] = categorie
        if rupture:
            params["rupture"] = "true"
        return self._request("GET", "/api/produits", params=params)

    def get_produit(self, code_ref: str) -> dict:
        """Détail d'un produit."""
        return self._request("GET", f"/api/produits/{code_ref}")

    def create_produit(self, data: dict) -> dict:
        """Crée un produit."""
        return self._request("POST", "/api/produits", json=data)

    def update_produit(self, code_ref: str, data: dict) -> dict:
        """Modifie un produit."""
        return self._request("PUT", f"/api/produits/{code_ref}", json=data)

    def delete_produit(self, code_ref: str) -> dict:
        """Soft delete."""
        return self._request("DELETE", f"/api/produits/{code_ref}")

    def ajuster_stock(self, code_ref: str, nouvelle_quantite: int,
                      motif: str) -> dict:
        """Ajuste le stock d'un produit."""
        return self._request(
            "POST", f"/api/produits/{code_ref}/stock",
            json={"nouvelle_quantite": nouvelle_quantite, "motif": motif})
    
    # ══════════════════════════════════════════════════════════════
    # Clients
    # ══════════════════════════════════════════════════════════════
    def list_clients(self, page: int = 1, per_page: int = 50,
                     search: str = "", filtre: str = "tous",
                     actif: int = 1) -> dict:
        """Liste paginée des clients."""
        params = {"page": page, "per_page": per_page,
                  "actif": actif, "filtre": filtre}
        if search:
            params["search"] = search
        return self._request("GET", "/api/clients", params=params)

    def get_client(self, client_id: str) -> dict:
        """Fiche détaillée d'un client."""
        return self._request("GET", f"/api/clients/{client_id}")

    def find_client_by_numero(self, numero: str) -> dict:
        """Recherche un client par numéro."""
        num = numero.replace(" ", "").replace("-", "").replace(".", "")
        return self._request("GET", f"/api/clients/numero/{num}")

    def create_client(self, data: dict) -> dict:
        """Crée un client."""
        return self._request("POST", "/api/clients", json=data)

    def update_client(self, client_id: str, data: dict) -> dict:
        """Modifie un client."""
        return self._request("PUT", f"/api/clients/{client_id}", json=data)

    def delete_client(self, client_id: str) -> dict:
        """Désactive un client."""
        return self._request("DELETE", f"/api/clients/{client_id}")

    def reactiver_client(self, client_id: str) -> dict:
        """Réactive un client."""
        return self._request("POST", f"/api/clients/{client_id}/reactiver")

    # ══════════════════════════════════════════════════════════════
    # Ventes
    # ══════════════════════════════════════════════════════════════
    def list_ventes(self, page: int = 1, per_page: int = 50,
                    search: str = "", date_debut: str = "",
                    date_fin: str = "", annule: int = -1) -> dict:
        """Liste paginée des factures."""
        params = {"page": page, "per_page": per_page, "annule": annule}
        if search:      params["search"] = search
        if date_debut:  params["date_debut"] = date_debut
        if date_fin:    params["date_fin"] = date_fin
        return self._request("GET", "/api/ventes", params=params)

    def get_vente(self, num_fact: str) -> dict:
        """Détail d'une facture."""
        return self._request("GET", f"/api/ventes/{num_fact}")

    def create_vente(self, lignes: list, client_id: str = None,
                     client_numero: str = None, caisse: str = None,
                     remise: float = 0,
                     devise_paiement: str = None,
                     montant_recu: float = None) -> dict:
        """Crée une vente + encaissement optionnel."""
        data = {"lignes": lignes, "remise": remise}
        if client_id:      data["client_id"] = client_id
        if client_numero:  data["client_numero"] = client_numero
        if caisse:         data["caisse"] = caisse
        if devise_paiement: data["devise_paiement"] = devise_paiement
        if montant_recu is not None:
            data["montant_recu"] = float(montant_recu)
        return self._request("POST", "/api/ventes", json=data)

    def get_encaissement(self, num_fact: str) -> dict:
        """Récupère l'encaissement d'une facture."""
        return self._request("GET", f"/api/ventes/{num_fact}/encaissement")

    def annuler_vente(self, num_fact: str, motif: str) -> dict:
        """Annule une vente (restitue le stock)."""
        return self._request(
            "POST", f"/api/ventes/{num_fact}/annuler",
            json={"motif": motif})

    def stats_ventes_jour(self) -> dict:
        """Stats des ventes du jour."""
        return self._request("GET", "/api/ventes/stats/jour")
    
    # ══════════════════════════════════════════════════════════════
    # BLF
    # ══════════════════════════════════════════════════════════════
    def list_blf(self, page: int = 1, per_page: int = 30,
                 search: str = "", statut: str = "") -> dict:
        params = {"page": page, "per_page": per_page}
        if search:  params["search"] = search
        if statut:  params["statut"] = statut
        return self._request("GET", "/api/blf", params=params)

    def get_blf(self, blf_id: str) -> dict:
        return self._request("GET", f"/api/blf/{blf_id}")

    def create_blf(self, data: dict) -> dict:
        return self._request("POST", "/api/blf", json=data)

    def valider_blf(self, blf_id: str) -> dict:
        return self._request("POST", f"/api/blf/{blf_id}/valider")

    def annuler_blf(self, blf_id: str, motif: str) -> dict:
        return self._request(
            "POST", f"/api/blf/{blf_id}/annuler", json={"motif": motif})

    def delete_blf(self, blf_id: str) -> dict:
        return self._request("DELETE", f"/api/blf/{blf_id}")

    # ══════════════════════════════════════════════════════════════
    # Rapports
    # ══════════════════════════════════════════════════════════════
    def rapport_ventes(self, periode: str = "Ce mois",
                       date_debut: str = "", date_fin: str = "",
                       topn: int = 10) -> dict:
        params = {"periode": periode, "topn": topn}
        if date_debut: params["date_debut"] = date_debut
        if date_fin:   params["date_fin"] = date_fin
        return self._request("GET", "/api/rapports/ventes", params=params)

    def rapport_equipe(self, periode: str = "Ce mois",
                       date_debut: str = "", date_fin: str = "") -> dict:
        params = {"periode": periode}
        if date_debut: params["date_debut"] = date_debut
        if date_fin:   params["date_fin"] = date_fin
        return self._request("GET", "/api/rapports/equipe", params=params)

    def rapport_operations(self, periode: str = "Ce mois",
                           date_debut: str = "", date_fin: str = "") -> dict:
        params = {"periode": periode}
        if date_debut: params["date_debut"] = date_debut
        if date_fin:   params["date_fin"] = date_fin
        return self._request(
            "GET", "/api/rapports/operations", params=params)

    # ══════════════════════════════════════════════════════════════
    # Audit
    # ══════════════════════════════════════════════════════════════
    def list_audit(self, page: int = 1, per_page: int = 50,
                   action: str = "", utilisateur_id: str = "",
                   date_debut: str = "", date_fin: str = "") -> dict:
        params = {"page": page, "per_page": per_page}
        if action:          params["action"] = action
        if utilisateur_id:  params["utilisateur_id"] = utilisateur_id
        if date_debut:      params["date_debut"] = date_debut
        if date_fin:        params["date_fin"] = date_fin
        return self._request("GET", "/api/audit", params=params)

    def get_audit(self, entry_id: str) -> dict:
        return self._request("GET", f"/api/audit/{entry_id}")

    def audit_actions(self) -> dict:
        return self._request("GET", "/api/audit/actions/liste")

    def create_rapport_z(self, caisse: str, periode: str,
                         montant_compte: float, format_pdf: str = "ticket",
                         date_debut: str = "", date_fin: str = "") -> dict:
        """Crée un Rapport Z côté serveur."""
        payload = {
            "caisse": caisse,  # ← garder "*" tel quel
            "periode": periode,
            "montant_compte": montant_compte,
            "format_pdf": format_pdf,
        }
        if date_debut: payload["date_debut"] = date_debut
        if date_fin:   payload["date_fin"] = date_fin
        return self._request("POST", "/api/rapports/z", json=payload)

    def preview_rapport_z(self, caisse: str = "A",
                          periode: str = "Aujourd'hui",
                          date_debut: str = "",
                          date_fin: str = "") -> dict:
        """Calcule un Rapport Z sans générer le PDF (prévisualisation)."""
        params = {"caisse": caisse, "periode": periode}
        if date_debut:
            params["date_debut"] = date_debut
        if date_fin:
            params["date_fin"] = date_fin
        return self._request("GET", "/api/rapports/z/preview",
                             params=params)

    # ══════════════════════════════════════════════════════════════════
    # Retours
    # ══════════════════════════════════════════════════════════════════
    def list_retours(self, page: int = 1, per_page: int = 30,
                     search: str = "", statut: str = "") -> dict:
        params = {"page": page, "per_page": per_page}
        if search:  params["search"] = search
        if statut:  params["statut"] = statut
        return self._request("GET", "/api/retours", params=params)

    def get_retour(self, retour_id: str) -> dict:
        return self._request("GET", f"/api/retours/{retour_id}")

    def create_retour(self, data: dict) -> dict:
        return self._request("POST", "/api/retours", json=data)

    def get_public_config(self) -> dict:
        """Récupère les paramètres publics du serveur."""
        return self._request("GET", "/api/config/public")

    # ✅ APRÈS
    def heartbeat(self, imprimante: str = "", version: str = "2.0.0") -> dict:
        """Envoie un heartbeat pour signaler que ce poste est actif."""
        try:
            from Database import machine_id
            mid = machine_id.get_machine_id()
            hostname = socket.gethostname()
        except Exception:
            mid = "unknown"
            hostname = "unknown"

        return self._request(
            "POST", "/api/sessions/heartbeat",
            json={
                "machine_id": mid,
                "hostname": hostname,
                "imprimante": imprimante,
                "version": version,
            })


    # ══════════════════════════════════════════════════════════════
    # Monitoring — Whitelist PC (Phase 1)
    # ══════════════════════════════════════════════════════════════
    def validate_machine(self, machine_id: str, hostname: str = "",
                         role_attempt: str = "ADMIN") -> dict:
        """
        Vérifie si cette machine peut se connecter avec ce rôle.
        Public (pas besoin de token).
        Retourne : {allowed: bool, reason: str}
        """
        return self._request(
            "POST", "/api/auth/validate-machine",
            json={
                "machine_id": machine_id,
                "hostname": hostname,
                "role_attempt": role_attempt,
            })

    def list_monitoring_machines(self) -> dict:
        """
        Liste les machines whitelistées.
        Retourne : {total: int, max_allowed: int, items: [...]}
        """
        return self._request("GET", "/api/monitoring/machines")

    # ══════════════════════════════════════════════════════════════
    # Users (Phase 2)
    # ══════════════════════════════════════════════════════════════
    def list_users(self, page: int = 1, per_page: int = 30,
                   search: str = "", role: str = "",
                   actif: int = -1) -> dict:
        """Liste paginée des utilisateurs."""
        params = {"page": page, "per_page": per_page, "actif": actif}
        if search:
            params["search"] = search
        if role:
            params["role"] = role
        return self._request("GET", "/api/users", params=params)

    def get_user(self, user_id: str) -> dict:
        """Détail d'un utilisateur (+ permissions)."""
        return self._request("GET", f"/api/users/{user_id}")

    def create_user(self, data: dict) -> dict:
        """Crée un utilisateur."""
        return self._request("POST", "/api/users", json=data)

    def update_user(self, user_id: str, data: dict) -> dict:
        """Modifie un utilisateur."""
        return self._request("PUT", f"/api/users/{user_id}", json=data)

    def reset_user_password(self, user_id: str) -> dict:
        """Génère un mot de passe temporaire NOVA-YYYY-XXXX."""
        return self._request(
            "POST", f"/api/users/{user_id}/reset-password")

    def delete_user(self, user_id: str) -> dict:
        """Désactive un utilisateur (soft delete)."""
        return self._request("DELETE", f"/api/users/{user_id}")

    # ══════════════════════════════════════════════════════════════
    # Config / Paramètres (Phase 2)
    # ══════════════════════════════════════════════════════════════
    def get_full_config(self) -> dict:
        """Retourne toutes les configs admin."""
        return self._request("GET", "/api/config/full")

    def save_config(self, data: dict) -> dict:
        """Sauvegarde une ou plusieurs configs."""
        return self._request("PUT", "/api/config", json=data)

    def get_pharmacie(self) -> dict:
        """Retourne les infos pharmacie."""
        return self._request("GET", "/api/pharmacie")

    def save_pharmacie(self, data: dict) -> dict:
        """Modifie les infos pharmacie."""
        return self._request("PUT", "/api/pharmacie", json=data)

    # ══════════════════════════════════════════════════════════════
    # Fournisseurs (Phase 2)
    # ══════════════════════════════════════════════════════════════
    def list_fournisseurs(self, page: int = 1, per_page: int = 50,
                          search: str = "", actif: int = -1) -> dict:
        """Liste paginée des fournisseurs."""
        params = {"page": page, "per_page": per_page, "actif": actif}
        if search:
            params["search"] = search
        return self._request(
            "GET", "/api/fournisseurs", params=params)

    def get_fournisseur(self, fournisseur_id: str) -> dict:
        return self._request(
            "GET", f"/api/fournisseurs/{fournisseur_id}")

    def create_fournisseur(self, data: dict) -> dict:
        return self._request(
            "POST", "/api/fournisseurs", json=data)

    def update_fournisseur(self, fournisseur_id: str,
                           data: dict) -> dict:
        return self._request(
            "PUT", f"/api/fournisseurs/{fournisseur_id}", json=data)

    # ══════════════════════════════════════════════════════════════
    # Catégories (Phase 2)
    # ══════════════════════════════════════════════════════════════
    def list_categories(self, actif: int = 1) -> dict:
        """Liste des catégories (actives par défaut)."""
        return self._request(
            "GET", "/api/categories", params={"actif": actif})

    def create_categorie(self, nom: str,
                         description: str = None) -> dict:
        """Crée une catégorie."""
        return self._request(
            "POST", "/api/categories",
            json={"nom": nom, "description": description})

    def update_categorie(self, categorie_id: str,
                         data: dict) -> dict:
        return self._request(
            "PUT", f"/api/categories/{categorie_id}", json=data)

    def delete_categorie(self, categorie_id: str) -> dict:
        """Soft delete (actif = 0)."""
        return self._request(
            "DELETE", f"/api/categories/{categorie_id}")

    # ══════════════════════════════════════════════════════════════
    # Charts (Phase 2+)
    # ══════════════════════════════════════════════════════════════
    def get_dashboard_charts(self) -> dict:
        """Retourne toutes les données des 4 graphiques dashboard."""
        return self._request("GET", "/api/charts/dashboard")


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)

    api = NovaApiClient("http://127.0.0.1:5001")
    print("→ Test de connexion au serveur…")
    try:
        info = api.sante()
        print(f"✅ Serveur vivant : {info}")
    except NovaApiError as e:
        print(f"❌ Serveur indisponible : {e}")
        sys.exit(1)