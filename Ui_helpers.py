#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ui_helpers.py — Helpers UI réutilisables Nova Pharma.
======================================================
Configure les QTableWidget de façon uniforme dans tous les dialogues.
"""

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt


# ══════════════════════════════════════════════════════════════════
# Configuration de tables
# ══════════════════════════════════════════════════════════════════
def setup_dialog_table(
        table: QtWidgets.QTableWidget,
        stretch_columns: list = None,
        resize_columns: list = None,
        row_height: int = 42,
        hide_vertical_header: bool = True,
        alternating: bool = True,
        show_grid: bool = False,
        font_family: str = "Segoe UI",
        font_size: int = 10) -> None:
    """
    Configure une QTableWidget pour un dialogue.

    Args:
        table: le QTableWidget à configurer
        stretch_columns: indexes des colonnes qui prennent l'espace restant
        resize_columns: indexes des colonnes ajustées au contenu
        row_height: hauteur par défaut des lignes
        hide_vertical_header: masque la colonne de numéros
        alternating: active les couleurs alternées
        show_grid: affiche la grille
        font_family, font_size: police du tableau
    """
    if table is None:
        return

    stretch_columns = stretch_columns or []
    resize_columns = resize_columns or []

    # ─── Font ───
    f = QtGui.QFont(font_family, font_size)
    table.setFont(f)

    # ─── Headers ───
    header = table.horizontalHeader()
    header.setFont(QtGui.QFont(font_family, 9, QtGui.QFont.Bold))
    header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    n_cols = table.columnCount()
    for i in range(n_cols):
        if i in stretch_columns:
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        elif i in resize_columns:
            header.setSectionResizeMode(
                i, QtWidgets.QHeaderView.ResizeToContents)
        else:
            # Par défaut : Stretch aussi (pour ne pas laisser de vide)
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

    # ─── Vertical header ───
    vh = table.verticalHeader()
    if hide_vertical_header:
        vh.setVisible(False)
    vh.setDefaultSectionSize(row_height)

    # ─── Table ───
    table.setAlternatingRowColors(alternating)
    table.setShowGrid(show_grid)
    table.setSelectionBehavior(
        QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
    table.setSelectionMode(
        QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    # ─── Style uniforme ───
    table.setStyleSheet("""
        QTableWidget {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            gridline-color: transparent;
            color: #0f172a;
            alternate-background-color: #f8fafc;
        }
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f1f5f9;
        }
        QTableWidget::item:selected {
            background: #e0f2fe;
            color: #0f172a;
        }
        QHeaderView::section {
            background: #f8fafc;
            color: #64748b;
            padding: 10px;
            border: none;
            border-bottom: 1px solid #e2e8f0;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
        }
    """)


# ══════════════════════════════════════════════════════════════════
# Adaptateurs par dialogue
# ══════════════════════════════════════════════════════════════════
def setup_blf_detail_table(table: QtWidgets.QTableWidget) -> None:
    """Table des lignes du détail BLF (7 colonnes)."""
    setup_dialog_table(
        table,
        stretch_columns=[1],       # Nom du produit
        resize_columns=[0, 2, 3, 4, 5, 6],
    )


def setup_user_info_history_table(table: QtWidgets.QTableWidget) -> None:
    """Table historique de la fiche utilisateur (3 colonnes)."""
    setup_dialog_table(
        table,
        stretch_columns=[2],       # Détails
        resize_columns=[0, 1],
    )


def setup_historique_detail_table(table: QtWidgets.QTableWidget) -> None:
    """Table détail facture (4 colonnes)."""
    setup_dialog_table(
        table,
        stretch_columns=[0],       # Article
        resize_columns=[1, 2, 3],
    )


def setup_audit_detail_table(table: QtWidgets.QTableWidget) -> None:
    """Table détail audit (si besoin)."""
    setup_dialog_table(table)


def setup_blf_dialog_table(table: QtWidgets.QTableWidget) -> None:
    """Table produits du BLF (4 colonnes)."""
    setup_dialog_table(
        table,
        stretch_columns=[1],       # Nom produit
        resize_columns=[0, 2, 3],
    )

class ProduitCompleter(QtWidgets.QCompleter):
    """
    QCompleter custom affichant :
        Nom — Code · Prix · Stock
    Stocke le dict complet du produit en UserRole.
    """

    def __init__(self, produits: list, parent=None):
        super().__init__(parent)
        self._produits = produits or []

        # Récupère la devise
        try:
            from Database import db
            devise = db.get_config("devise", "FC")
        except Exception:
            devise = "FC"

        model = QtGui.QStandardItemModel(self)

        for p in self._produits:
            nom = p.get("Nom") or "—"
            code = p.get("Code_reference") or "—"
            prix = float(p.get("Prix_vente")
                         or p.get("Prix_unitaire") or 0)
            stock = int(p.get("Quantite") or 0)

            display = (
                f"{nom}  —  {code}  ·  "
                f"{prix:,.0f} {devise}  ·  stock {stock}"
            ).replace(",", " ")

            item = QtGui.QStandardItem(display)
            item.setData(p, Qt.UserRole)
            model.appendRow(item)

        self.setModel(model)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.setMaxVisibleItems(15)

    # ------------------------------------------------------------------
    def get_produit_par_display(self, display: str) -> dict | None:
        """Retourne le dict produit depuis le texte affiché."""
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item and item.text() == display:
                return item.data(Qt.UserRole)
        return None

    def get_produit_par_nom(self, nom: str) -> dict | None:
        """Retourne le dict produit depuis son nom."""
        for p in self._produits:
            if p.get("Nom") == nom:
                return p
        return None