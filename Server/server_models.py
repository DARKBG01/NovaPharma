#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_models.py — Schémas Pydantic pour l'API.
================================================
"""

from typing import Optional, List
from pydantic import BaseModel, Field


# ══════════════════════════════════════════════════════════════════
# PRODUITS
# ══════════════════════════════════════════════════════════════════
class ProduitBase(BaseModel):
    Nom: str = Field(..., min_length=2, max_length=120)
    Code_barre: Optional[str] = None
    Categorie: Optional[str] = None
    Description: Optional[str] = None
    Unite: str = "pièce"
    Quantite: int = Field(0, ge=0)
    Prix_achat: float = Field(0, ge=0)
    Prix_vente: float = Field(0, ge=0)
    Prix_unitaire: Optional[float] = None


class ProduitCreate(ProduitBase):
    """Création : code généré automatiquement si absent."""
    Code_reference: Optional[str] = None


class ProduitUpdate(BaseModel):
    """Modification : tous les champs optionnels."""
    Nom: Optional[str] = None
    Code_barre: Optional[str] = None
    Categorie: Optional[str] = None
    Description: Optional[str] = None
    Unite: Optional[str] = None
    Quantite: Optional[int] = Field(None, ge=0)
    Prix_achat: Optional[float] = Field(None, ge=0)
    Prix_vente: Optional[float] = Field(None, ge=0)
    Prix_unitaire: Optional[float] = None


class ProduitResponse(BaseModel):
    Code_reference: str
    Nom: str
    Code_barre: Optional[str] = None
    Categorie: Optional[str] = None
    Description: Optional[str] = None
    Unite: str = "pièce"
    Quantite: int = 0
    Prix_achat: float = 0
    Prix_vente: float = 0
    Prix_unitaire: float = 0
    actif: int = 1
    Date_ajout: Optional[str] = None


class ProduitListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int
    items: List[ProduitResponse]


class StockAdjustRequest(BaseModel):
    """Ajustement manuel de stock."""
    nouvelle_quantite: int = Field(..., ge=0)
    motif: str = Field(..., min_length=2, max_length=200)


# ══════════════════════════════════════════════════════════════════
# RÉPONSES GÉNÉRIQUES
# ══════════════════════════════════════════════════════════════════
class SimpleResponse(BaseModel):
    status: str
    message: Optional[str] = None
    
    
    

# ══════════════════════════════════════════════════════════════════
# CLIENTS
# ══════════════════════════════════════════════════════════════════
class ClientBase(BaseModel):
    nom: Optional[str] = None
    numero: Optional[str] = None
    adresse: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None
    anonyme: bool = False
    sexe: Optional[str] = "M"   # ← AJOUT


class ClientCreate(ClientBase):
    """Création. Si anonyme=True → nom et numero générés auto."""
    pass


class ClientUpdate(BaseModel):
    nom: Optional[str] = None
    numero: Optional[str] = None
    adresse: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None
    sexe: Optional[str] = None


class ClientResponse(BaseModel):
    id: str
    nom: str
    numero: Optional[str] = None
    adresse: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None
    sexe: Optional[str] = "M"
    Montant_total: float = 0
    actif: int = 1
    created_at: Optional[str] = None


class ClientListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int
    items: List[ClientResponse]


class ClientDetailResponse(ClientResponse):
    """Fiche détaillée avec stats + historique."""
    nb_visites: int = 0
    derniere_visite: Optional[str] = None
    historique: List[dict] = []
    

# ══════════════════════════════════════════════════════════════════
# VENTES
# ══════════════════════════════════════════════════════════════════
class LigneVenteInput(BaseModel):
    """Une ligne du panier."""
    code_ref: str
    quantite: int = Field(..., ge=1)
    prix_unitaire: Optional[float] = None  # si None → utilise Prix_unitaire du produit


class VenteCreate(BaseModel):
    lignes: List[LigneVenteInput] = Field(..., min_length=1)
    client_id: Optional[str] = None
    client_numero: Optional[str] = None
    caisse: Optional[str] = None
    remise: float = Field(0, ge=0)

    # ─── NOUVEAU : encaissement ───
    devise_paiement: Optional[str] = "FC"
    montant_recu: Optional[float] = None   # None = pas d'encaissement


class AnnulationRequest(BaseModel):
    motif: str = Field(..., min_length=3, max_length=200)


class LigneVenteResponse(BaseModel):
    Article: str
    Code_reference: Optional[str] = None
    Quantite: int
    Prix_uni: float
    Total: float


class VenteResponse(BaseModel):
    Num_fact: str
    Date_vent: str
    Client_name: Optional[str] = None
    Caisse: Optional[str] = None
    utilisateur_id: Optional[str] = None
    utilisateur_name: Optional[str] = None
    annule: int = 0
    motif_annulation: Optional[str] = None
    total: float = 0
    nb_articles: int = 0
    lignes: List[LigneVenteResponse] = []


class VenteListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int
    items: List[dict]

class VenteCreateResponse(BaseModel):
    status: str
    Num_fact: str
    total: float
    nb_articles: int
    chemin_pdf: Optional[str] = None

    # ─── Retour encaissement ───
    montant_rendu: float = 0
    devise_rendu: str = "FC"
    
# ══════════════════════════════════════════════════════════════════
# BLF (Bon de Livraison Fournisseur)
# ══════════════════════════════════════════════════════════════════
class LigneBLFInput(BaseModel):
    code_ref: str
    quantite: int = Field(..., ge=1)
    prix_achat: Optional[float] = None
    prix_vente: Optional[float] = None


class BLFCreate(BaseModel):
    lignes: list[LigneBLFInput] = Field(..., min_length=1)
    fournisseur_id: Optional[str] = None
    notes: Optional[str] = None
    reference_externe: Optional[str] = None
    valider_immediatement: bool = False


class BLFAnnulationRequest(BaseModel):
    motif: str = Field(..., min_length=3, max_length=200)


class BLFResponse(BaseModel):
    id: str
    numero_blf: str
    fournisseur_id: Optional[str] = None
    fournisseur_nom: Optional[str] = None
    date_livraison: Optional[str] = None
    statut: str
    total_achat: float = 0
    nb_articles: int = 0
    nb_unites: int = 0
    notes: Optional[str] = None
    reference_externe: Optional[str] = None
    created_by_name: Optional[str] = None
    created_at: Optional[str] = None
    validated_by_name: Optional[str] = None
    validated_at: Optional[str] = None
    cancelled_by_name: Optional[str] = None
    cancelled_at: Optional[str] = None
    motif_annulation: Optional[str] = None


class BLFDetailResponse(BLFResponse):
    lignes: list = []


class BLFListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int
    items: list


# ══════════════════════════════════════════════════════════════════
# RAPPORTS
# ══════════════════════════════════════════════════════════════════
class RapportParams(BaseModel):
    periode: str = "Ce mois"
    date_debut: Optional[str] = None
    date_fin: Optional[str] = None
    topn: int = 10


# ══════════════════════════════════════════════════════════════════
# AUDIT
# ══════════════════════════════════════════════════════════════════
class AuditListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int
    items: list




# ══════════════════════════════════════════════════════════════════
# MONITORING — Whitelist PC monitoring (Phase 1)
# ══════════════════════════════════════════════════════════════════
class MachineCreate(BaseModel):
    """Ajout d'une machine à la whitelist monitoring."""
    machine_id: str = Field(..., min_length=8, max_length=128)
    hostname: Optional[str] = Field(None, max_length=120)
    role_autorise: str = Field("ALL", pattern="^(OWNER|ADMIN|DEV|ALL)$")


class MachineResponse(BaseModel):
    id: str
    machine_id: str
    hostname: Optional[str] = None
    role_autorise: str
    ajoute_par: Optional[str] = None
    ajoute_par_name: Optional[str] = None
    ajoute_le: Optional[str] = None
    actif: int = 1


class MachinesListResponse(BaseModel):
    total: int
    max_allowed: int = 3
    items: List[MachineResponse]


class ValidateMachineRequest(BaseModel):
    """Vérification d'une machine lors du login (mode client)."""
    machine_id: str = Field(..., min_length=8, max_length=128)
    hostname: Optional[str] = None
    role_attempt: str = Field(..., pattern="^(ADMIN|OWNER|UTILISATEUR|CAISSIER|DEV)$")


class ValidateMachineResponse(BaseModel):
    allowed: bool
    reason: str


# ══════════════════════════════════════════════════════════════════
# UTILISATEURS (Phase 2)
# ══════════════════════════════════════════════════════════════════
class UserCreate(BaseModel):
    prenom: str = Field(..., min_length=2, max_length=80)
    nom: str = Field(..., min_length=2, max_length=80)
    post_nom: Optional[str] = None
    sexe: str = Field("M", pattern="^[MF]$")
    date_naissance: Optional[str] = None
    nationalite: Optional[str] = None
    email: str = Field(..., min_length=5, max_length=120)
    numero: str = Field(..., min_length=6, max_length=20)
    role: str = Field(..., pattern="^(ADMIN|UTILISATEUR|CAISSIER)$")
    password: Optional[str] = None
    must_change_password: bool = False
    permissions: list[str] = []


class UserUpdate(BaseModel):
    prenom: Optional[str] = None
    nom: Optional[str] = None
    post_nom: Optional[str] = None
    sexe: Optional[str] = None
    date_naissance: Optional[str] = None
    nationalite: Optional[str] = None
    email: Optional[str] = None
    numero: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None
    actif: Optional[int] = None
    must_change_password: Optional[int] = None
    permissions: Optional[list[str]] = None


class UserResponse(BaseModel):
    id: str
    identifiant: str
    prenom: str
    nom: str
    post_nom: Optional[str] = None
    sexe: Optional[str] = "M"
    date_naissance: Optional[str] = None
    nationalite: Optional[str] = None
    email: Optional[str] = None
    numero: Optional[str] = None
    role: str
    actif: int = 1
    is_owner: int = 0
    is_developer: int = 0
    must_change_password: int = 0
    derniere_connexion: Optional[str] = None
    created_at: Optional[str] = None
    path_image: Optional[str] = None


class UserListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int
    items: List[UserResponse]


class ResetPasswordResponse(BaseModel):
    user_id: str
    temp_password: str
    message: str = "Mot de passe réinitialisé"


# ══════════════════════════════════════════════════════════════════
# CONFIG / PARAMÈTRES (Phase 2)
# ══════════════════════════════════════════════════════════════════
class ConfigFullResponse(BaseModel):
    """Toutes les configs en un seul objet."""
    # Entreprise
    nom_entreprise: Optional[str] = ""
    adresse_entreprise: Optional[str] = ""
    telephone_entreprise: Optional[str] = ""
    # Vente
    devise: str = "FC"
    taux_change: float = 2250.0
    afficher_dual: bool = True
    chiffre_affaire_periode: str = "Mois"
    marge_benefice: float = 30.0
    facture_numero_caisse: str = "01"
    max_postes: int = 100
    # Facturation
    impression_facture_auto: bool = True
    qrcode_actif: bool = True
    mentions_ticket: list = []
    # Sauvegarde
    sauvegarde_auto: bool = False
    sauvegarde_intervalle_jours: int = 7
    sauvegarde_max_conservees: int = 10
    backup_dir: str = ""
    backup_secondary_enabled: bool = False
    backup_secondary_dir: str = ""
    # Sécurité
    pwd_min_length: int = 8
    pwd_expiration_days: int = 0
    pwd_require_digit: bool = False
    pwd_require_upper: bool = False
    pwd_require_special: bool = False
    require_password_critical: bool = False
    backup_urgence_auto: bool = True
    seuil_stock: int = 20
    allow_admin_on_client: bool = True
    # Impression
    printer_auto_print: bool = False
    printer_auto_print_report: bool = False
    printer_auto_open: bool = True


class ConfigUpdate(BaseModel):
    """Update partiel : seuls les champs présents sont modifiés."""
    nom_entreprise: Optional[str] = None
    adresse_entreprise: Optional[str] = None
    telephone_entreprise: Optional[str] = None
    devise: Optional[str] = None
    taux_change: Optional[float] = None
    afficher_dual: Optional[bool] = None
    chiffre_affaire_periode: Optional[str] = None
    marge_benefice: Optional[float] = None
    facture_numero_caisse: Optional[str] = None
    max_postes: Optional[int] = None
    impression_facture_auto: Optional[bool] = None
    qrcode_actif: Optional[bool] = None
    mentions_ticket: Optional[list] = None
    sauvegarde_auto: Optional[bool] = None
    sauvegarde_intervalle_jours: Optional[int] = None
    sauvegarde_max_conservees: Optional[int] = None
    backup_dir: Optional[str] = None
    backup_secondary_enabled: Optional[bool] = None
    backup_secondary_dir: Optional[str] = None
    pwd_min_length: Optional[int] = None
    pwd_expiration_days: Optional[int] = None
    pwd_require_digit: Optional[bool] = None
    pwd_require_upper: Optional[bool] = None
    pwd_require_special: Optional[bool] = None
    require_password_critical: Optional[bool] = None
    backup_urgence_auto: Optional[bool] = None
    seuil_stock: Optional[int] = None
    allow_admin_on_client: Optional[bool] = None
    printer_auto_print: Optional[bool] = None
    printer_auto_print_report: Optional[bool] = None
    printer_auto_open: Optional[bool] = None


# ══════════════════════════════════════════════════════════════════
# PHARMACIE (Phase 2)
# ══════════════════════════════════════════════════════════════════
class PharmacieResponse(BaseModel):
    nom: str = ""
    type: Optional[str] = "MOYENNE"
    email: Optional[str] = ""
    numero: Optional[str] = ""
    adresse: Optional[str] = ""
    path_logo: Optional[str] = None
    seuil_stock: int = 25
    marge_benefice: float = 30.0


class PharmacieUpdate(BaseModel):
    nom: Optional[str] = None
    type: Optional[str] = None
    email: Optional[str] = None
    numero: Optional[str] = None
    adresse: Optional[str] = None
    path_logo: Optional[str] = None
    seuil_stock: Optional[int] = None
    marge_benefice: Optional[float] = None


# ══════════════════════════════════════════════════════════════════
# FOURNISSEURS (Phase 2)
# ══════════════════════════════════════════════════════════════════
class FournisseurCreate(BaseModel):
    Entreprise: str = Field(..., min_length=2, max_length=120)
    Categorie: Optional[str] = None
    Responsable: Optional[str] = None
    Numero: Optional[str] = None
    Email: Optional[str] = None
    Adresse: Optional[str] = None


class FournisseurUpdate(BaseModel):
    Entreprise: Optional[str] = None
    Categorie: Optional[str] = None
    Responsable: Optional[str] = None
    Numero: Optional[str] = None
    Email: Optional[str] = None
    Adresse: Optional[str] = None
    actif: Optional[int] = None


class FournisseurResponse(BaseModel):
    Id_fournisseur: str
    Entreprise: str
    Categorie: Optional[str] = None
    Responsable: Optional[str] = None
    Numero: Optional[str] = None
    Email: Optional[str] = None
    Adresse: Optional[str] = None
    actif: int = 1
    created_at: Optional[str] = None


class FournisseurListResponse(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int
    items: List[FournisseurResponse]


# ══════════════════════════════════════════════════════════════════
# CATÉGORIES (Phase 2)
# ══════════════════════════════════════════════════════════════════
class CategorieCreate(BaseModel):
    nom: str = Field(..., min_length=2, max_length=80)
    description: Optional[str] = None


class CategorieUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    actif: Optional[int] = None


class CategorieResponse(BaseModel):
    id: str
    nom: str
    description: Optional[str] = None
    actif: int = 1
    created_at: Optional[str] = None


class CategorieListResponse(BaseModel):
    total: int
    items: List[CategorieResponse]
