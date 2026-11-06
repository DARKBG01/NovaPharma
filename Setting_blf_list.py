#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_blf_list.py — Page liste des Bons de Livraison Fournisseur
====================================================================
Utilise Interface_page_blf.py (généré depuis Page_blf.ui)
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from Client.api_singleton import get_api, is_client_mode
from Database import db
from Interface_page_blf import Ui_PageBLF

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════════════════════════
PAGE_SIZE = 30

# Colonnes
COL_NUMERO      = 0
COL_FOURNISSEUR = 1
COL_DATE        = 2
COL_ARTICLES    = 3
COL_UNITES      = 4
COL_TOTAL       = 5
COL_STATUT      = 6
COL_CREATEUR    = 7

FILTERS = {
    "Tous les BLF": "1=1",
    "Brouillons":   "statut = 'BROUILLON'",
    "Validées":     "statut = 'VALIDEE'",
    "Annulées":     "statut = 'ANNULEE'",
}


# ══════════════════════════════════════════════════════════════════
# Page
# ══════════════════════════════════════════════════════════════════
class PageBLF(QtWidgets.QWidget, Ui_PageBLF):

    def __init__(self, parent=None, user_id: str = None,
                 user_name: str = "", role: str = "ADMIN"):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.role = (role or "UTILISATEUR").upper()

        # État pagination
        self._page = 1
        self._total_pages = 1
        self._total_count = 0

        # État recherche / filtre
        self._search = ""
        self._filter = "Tous les BLF"

        # Connexions
        self._connect_signals()

        # Bouton supplémentaire : Nouveau fournisseur
        self._setup_ui_extras()

        # Charge la première page
        self.refresh()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        # Boutons principaux
        self.btn_new.clicked.connect(self._on_new)
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_prev.clicked.connect(self._on_prev)
        self.btn_next.clicked.connect(self._on_next)
        self.btn_view.clicked.connect(self._on_view)

        # Recherche + filtre
        self.search_input.textChanged.connect(self._on_search_changed)
        self.filter_combo.currentTextChanged.connect(self._on_filter_changed)

        # Table
        self.blf_table.itemSelectionChanged.connect(self._on_selection_changed)
        self.blf_table.doubleClicked.connect(self._on_view)
        self.blf_table.customContextMenuRequested.connect(self._on_context_menu)

    # ══════════════════════════════════════════════════════════════
    # Chargement
    # ══════════════════════════════════════════════════════════════
    def refresh(self):
        self._load_page(self._page)

    def _load_page(self, page: int):
        """Charge une page — mode client (API) ou autonome (DB)."""
        try:
            if is_client_mode():
                self._load_page_api(page)
            else:
                self._load_page_local(page)

            self._update_pagination()
        except Exception:
            logger.exception("Erreur chargement BLF")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible de charger la liste des BLF.")

    def _load_page_api(self, page: int):
        """Charge via l'API."""
        api = get_api()
        if api is None:
            raise RuntimeError("API non initialisée")

        statut_map = {
            "Tous les BLF": "",
            "Brouillons":   "BROUILLON",
            "Validées":     "VALIDEE",
            "Annulées":     "ANNULEE",
        }

        data = api.list_blf(
            page=page, per_page=PAGE_SIZE,
            search=self._search,
            statut=statut_map.get(self._filter, ""))

        self._total_count = int(data.get("total", 0))
        self._total_pages = int(data.get("pages", 1))
        self._page = int(data.get("page", 1))

        items = data.get("items", [])
        self._populate_table(items)

    def _load_page_local(self, page: int):
        """Charge depuis la DB locale."""
        where = [FILTERS.get(self._filter, "1=1")]
        params = []

        if self._search:
            where.append("(numero_blf LIKE ? OR fournisseur_nom LIKE ?)")
            like = f"%{self._search}%"
            params.extend([like, like])

        wc = " AND ".join(where)

        row = db.query_one(
            f"SELECT COUNT(*) AS n FROM BonLivraison WHERE {wc}",
            tuple(params))
        self._total_count = int(row["n"] or 0) if row else 0
        self._total_pages = max(
            1, (self._total_count + PAGE_SIZE - 1) // PAGE_SIZE)
        self._page = max(1, min(page, self._total_pages))

        offset = (self._page - 1) * PAGE_SIZE
        rows = db.query(
            f"""SELECT * FROM BonLivraison
                WHERE {wc}
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?""",
            tuple(params + [PAGE_SIZE, offset]))

        items = [dict(r) for r in rows]
        self._populate_table(items)

    def _populate_table(self, items):
        """Remplit la table depuis une liste de dicts."""
        t = self.blf_table
        t.blockSignals(True)
        t.setRowCount(0)
        t.clearSpans()

        if not items:
            t.setRowCount(1)
            empty = QtWidgets.QTableWidgetItem(
                "Aucun BLF à afficher — cliquez sur « Nouveau BLF » "
                "pour commencer")
            empty.setTextAlignment(Qt.AlignCenter)
            empty.setForeground(QtGui.QColor("#94a3b8"))
            f = QtGui.QFont("Segoe UI", 11)
            f.setItalic(True)
            empty.setFont(f)
            t.setItem(0, 0, empty)
            t.setSpan(0, 0, 1, t.columnCount())
            t.blockSignals(False)
            return

        t.setRowCount(len(items))
        font_bold = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        font_mono = QtGui.QFont("Courier New", 9)
        font_normal = QtGui.QFont("Segoe UI", 10)

        for i, r in enumerate(items):
            # N° BLF
            it0 = QtWidgets.QTableWidgetItem(str(r.get("numero_blf", "")))
            it0.setFont(font_mono)
            it0.setForeground(QtGui.QColor("#023E8A"))
            it0.setData(Qt.UserRole, r.get("id"))
            t.setItem(i, COL_NUMERO, it0)

            # Fournisseur
            has_four = r.get("fournisseur_id") is not None
            it1 = QtWidgets.QTableWidgetItem(
                r.get("fournisseur_nom") or "Sans fournisseur")
            it1.setFont(font_bold if has_four else font_normal)
            it1.setForeground(QtGui.QColor(
                "#0f172a" if has_four else "#94a3b8"))
            t.setItem(i, COL_FOURNISSEUR, it1)

            # Date
            it2 = QtWidgets.QTableWidgetItem(
                str(r.get("date_livraison") or "—"))
            it2.setForeground(QtGui.QColor("#64748b"))
            t.setItem(i, COL_DATE, it2)

            # Articles
            it3 = QtWidgets.QTableWidgetItem(
                str(int(r.get("nb_articles") or 0)))
            it3.setTextAlignment(Qt.AlignCenter)
            it3.setForeground(QtGui.QColor("#475569"))
            t.setItem(i, COL_ARTICLES, it3)

            # Unités
            it4 = QtWidgets.QTableWidgetItem(
                str(int(r.get("nb_unites") or 0)))
            it4.setTextAlignment(Qt.AlignCenter)
            it4.setForeground(QtGui.QColor("#0077B6"))
            it4.setFont(font_bold)
            t.setItem(i, COL_UNITES, it4)

            # Total
            total = float(r.get("total_achat") or 0)
            it5 = QtWidgets.QTableWidgetItem(
                f"{total:,.0f} FC".replace(",", " "))
            it5.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            it5.setForeground(QtGui.QColor("#16A34A"))
            it5.setFont(font_bold)
            t.setItem(i, COL_TOTAL, it5)

            # Statut
            statut = r.get("statut", "")
            if statut == "VALIDEE":
                txt, fg, bg = "● Validée", "#15803d", "#dcfce7"
            elif statut == "ANNULEE":
                txt, fg, bg = "● Annulée", "#991b1b", "#fee2e2"
            else:
                txt, fg, bg = "● Brouillon", "#92400e", "#fef3c7"

            it6 = QtWidgets.QTableWidgetItem(txt)
            it6.setForeground(QtGui.QColor(fg))
            it6.setBackground(QtGui.QColor(bg))
            it6.setTextAlignment(Qt.AlignCenter)
            it6.setFont(font_bold)
            t.setItem(i, COL_STATUT, it6)

            # Créateur
            it7 = QtWidgets.QTableWidgetItem(
                str(r.get("created_by_name") or "—"))
            it7.setForeground(QtGui.QColor("#94a3b8"))
            t.setItem(i, COL_CREATEUR, it7)

        t.blockSignals(False)

        header = t.horizontalHeader()
        header.setSectionResizeMode(
            COL_NUMERO, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            COL_FOURNISSEUR, QtWidgets.QHeaderView.Stretch)
        for c in (COL_DATE, COL_ARTICLES, COL_UNITES, COL_TOTAL,
                  COL_STATUT, COL_CREATEUR):
            header.setSectionResizeMode(
                c, QtWidgets.QHeaderView.ResizeToContents)

    # ══════════════════════════════════════════════════════════════
    # Pagination
    # ══════════════════════════════════════════════════════════════
    def _update_pagination(self):
        self.page_info.setText(
            f"Page {self._page} / {self._total_pages}")
        self.btn_prev.setEnabled(self._page > 1)
        self.btn_next.setEnabled(self._page < self._total_pages)

        self.total_info.setText(f"{self._total_count} BLF au total")
        self.header_badge.setText(f"{self._total_count} BLF")

    def _on_prev(self):
        if self._page > 1:
            self._load_page(self._page - 1)

    def _on_next(self):
        if self._page < self._total_pages:
            self._load_page(self._page + 1)

    # ══════════════════════════════════════════════════════════════
    # Recherche / filtre
    # ══════════════════════════════════════════════════════════════
    def _on_search_changed(self, text: str):
        self._search = text.strip()
        self._page = 1
        self._load_page(1)

    def _on_filter_changed(self, text: str):
        self._filter = text
        self._page = 1
        self._load_page(1)

    # ══════════════════════════════════════════════════════════════
    # Sélection
    # ══════════════════════════════════════════════════════════════
    def _on_selection_changed(self):
        has = self._selected_blf_id() is not None
        self.btn_view.setEnabled(has)

        if has:
            self.hint_selection.setText("BLF sélectionné")
            self.hint_selection.setStyleSheet(
                "color: #0077B6; font-size: 11px; font-weight: 700; "
                "background: transparent;")
        else:
            self.hint_selection.setText(
                "Sélectionnez un BLF pour voir les détails")
            self.hint_selection.setStyleSheet(
                "color: #94a3b8; font-size: 11px; font-weight: 600; "
                "background: transparent;")

    def _selected_blf_id(self):
        row = self.blf_table.currentRow()
        if row < 0:
            return None
        item = self.blf_table.item(row, COL_NUMERO)
        if not item:
            return None
        return item.data(Qt.UserRole)

    # ══════════════════════════════════════════════════════════════
    # Actions
    # ══════════════════════════════════════════════════════════════
    def _on_new(self):
        try:
            from Setting_blf_dialog import Setting_blf_dialog
            dlg = Setting_blf_dialog(
                parent=self,
                user_id=self.user_id,
                user_name=self.user_name,
            )
            dlg.blf_created.connect(self._on_blf_created)
            if dlg.exec() == QtWidgets.QDialog.Accepted:
                self._page = 1
                self.refresh()
        except Exception:
            logger.exception("Erreur ouverture dialogue BLF")

    def _on_view(self):
        blf_id = self._selected_blf_id()
        if not blf_id:
            return
        try:
            from Setting_blf_detail import Setting_blf_detail
            dlg = Setting_blf_detail(
                parent=self,
                blf_id=blf_id,
                user_id=self.user_id,
                user_name=self.user_name,
                role=self.role,
            )
            dlg.blf_updated.connect(self._on_blf_updated)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture détail BLF")

    def _on_blf_created(self, blf_id: str):
        logger.info("BLF créé : %s", blf_id)
        self._page = 1
        self.refresh()

    def _on_blf_updated(self, blf_id: str):
        logger.info("BLF mis à jour : %s", blf_id)
        self.refresh()

    def _on_context_menu(self, pos):
        row = self.blf_table.rowAt(pos.y())
        if row < 0:
            return
        self.blf_table.selectRow(row)

        blf_id = self._selected_blf_id()
        if not blf_id:
            return

        # Récupère le statut
        try:
            row_data = db.query_one(
                "SELECT statut, numero_blf FROM BonLivraison "
                "WHERE id = ? LIMIT 1", (blf_id,))
            statut = row_data["statut"] if row_data else None
            numero = row_data["numero_blf"] if row_data else ""
        except Exception:
            statut = None
            numero = ""

        menu = QtWidgets.QMenu(self)

        # Voir détail
        act_view = menu.addAction(
            QtGui.QIcon(":/Icon/Icons/eye.svg"), "Voir le détail")
        act_view.triggered.connect(self._on_view)

        # Actions admin
        if self.role == "ADMIN":
            # Valider (si brouillon)
            if statut == "BROUILLON":
                menu.addSeparator()
                act_validate = menu.addAction(
                    QtGui.QIcon(":/Icon/Icons/check-circle.svg"),
                    "Valider ce BLF")
                act_validate.triggered.connect(self._on_view)

            # Annuler (si validée)
            if statut == "VALIDEE":
                menu.addSeparator()
                act_cancel = menu.addAction(
                    QtGui.QIcon(":/Icon/Icons/x-circle.svg"),
                    "Annuler ce BLF")
                act_cancel.triggered.connect(self._on_view)

            # Supprimer brouillon
            if statut == "BROUILLON":
                menu.addSeparator()
                act_del = menu.addAction(
                    QtGui.QIcon(":/Icon/Icons/trash.svg"),
                    "Supprimer le brouillon")
                act_del.triggered.connect(
                    lambda: self._on_delete_draft(blf_id, numero))

        menu.exec(self.blf_table.viewport().mapToGlobal(pos))

    def _on_delete_draft(self, blf_id: str, numero: str = ""):
        """Supprime un BLF en brouillon (hard delete)."""
        try:
            # Vérifie à nouveau le statut
            blf = db.query_one(
                "SELECT numero_blf, statut FROM BonLivraison "
                "WHERE id = ? LIMIT 1", (blf_id,))

            if not blf or blf["statut"] != "BROUILLON":
                QtWidgets.QMessageBox.warning(
                    self, "Action impossible",
                    "Seuls les brouillons peuvent être supprimés.")
                return

            numero = blf["numero_blf"]

            rep = QtWidgets.QMessageBox.question(
                self, "Suppression du brouillon",
                f"<b>Supprimer le brouillon {numero} ?</b><br><br>"
                "Le BLF sera définitivement supprimé.<br>"
                "Aucun impact sur le stock (brouillon non validé).<br><br>"
                "<b>Action irréversible.</b>",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)

            if rep != QtWidgets.QMessageBox.Yes:
                return

            with db.transaction():
                db.execute(
                    "DELETE FROM BonLivraison WHERE id = ?", (blf_id,))

            logger.info("Brouillon BLF supprimé : %s", numero)
            QtWidgets.QMessageBox.information(
                self, "Supprimé",
                f"Le brouillon {numero} a été supprimé.")

            self.refresh()

        except Exception as e:
            logger.exception("Erreur suppression brouillon")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible de supprimer le brouillon :\n{e}")
            
    # ══════════════════════════════════════════════════════════════
    # UI extras : bouton "Nouveau fournisseur"
    # ══════════════════════════════════════════════════════════════
    def _setup_ui_extras(self) -> None:
        """Connecte le bouton 'Nouveau fournisseur' du .ui."""
        try:
            if hasattr(self, "btn_new_supplier"):
                self.btn_new_supplier.clicked.connect(self._on_new_supplier)
                logger.info("Bouton 'Nouveau fournisseur' connecté")
            else:
                logger.warning(
                    "btn_new_supplier absent du .ui — bouton non connecté")
        except Exception:
            logger.exception("Erreur _setup_ui_extras")

    def _on_new_supplier(self) -> None:
        """Ouvre le dialogue d'ajout de fournisseur."""
        try:
            from Setting_add_fourniss import Setting_add_fourniss
            dlg = Setting_add_fourniss(
                parent=self,
                user_id=self.user_id,
                user_name=self.user_name)
            dlg.fournisseur_created.connect(self._on_supplier_created)
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture dialogue fournisseur")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir le formulaire fournisseur.")

    def _on_supplier_created(self, fid: str) -> None:
        logger.info("Fournisseur créé : %s", fid)
        QtWidgets.QMessageBox.information(
            self, "Fournisseur ajouté",
            f"Le fournisseur a été enregistré avec succès.\n\n"
            f"Vous pouvez maintenant l'utiliser pour créer un BLF.")


# ══════════════════════════════════════════════════════════════════
# Test autonome
# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)

    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)

    db.get_conn()
    seed.run()

    w = PageBLF(user_id="TEST", user_name="Test User", role="ADMIN")
    w.resize(1200, 800)
    w.show()
    sys.exit(app.exec())