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

