#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_backup_reader.py — Lecture seule d'une archive.
=========================================================
Déchiffre l'archive dans un dossier temp, ouvre la DB en READ-ONLY,
affiche un rapport simplifié (3 onglets), nettoie à la fermeture.
"""

import logging
import os
import sqlite3

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db, backup_engine
from Interface_backup_reader import Ui_Dialog

logger = logging.getLogger(__name__)


class Setting_backup_reader(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None, archive_path="", archive_name=""):
        super().__init__(parent)
        self.setupUi(self)

        self.archive_path = archive_path
        self.archive_name = archive_name or os.path.basename(archive_path)

        self._tmp_dir = ""
        self._db_path = ""
        self._conn = None
        self._cleaned_up = False

        self.lbl_header_title.setText(f"Archive : {self.archive_name}")
        self.lbl_header_sub.setText(
            "Consultation en lecture seule — aucune modification")

        self.btn_close.clicked.connect(self.accept)

        self._load_archive()

    # ══════════════════════════════════════════════════════════════
    def _load_archive(self):
        try:
            tmp_dir, db_path = backup_engine.extract_to_temp(
                self.archive_path)
            if not tmp_dir:
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    "Impossible d'ouvrir l'archive.\n\n"
                    "Le mot de passe est peut-être invalide, ou "
                    "l'archive a été créée sur une autre machine.")
                self.reject()
                return

            self._tmp_dir = tmp_dir
            self._db_path = db_path

            # Connexion lecture seule
            self._conn = sqlite3.connect(
                f"file:{db_path}?mode=ro", uri=True)
            self._conn.row_factory = sqlite3.Row

            self._render_ventes()
            self._render_clients()
            self._render_stocks()

        except Exception:
            logger.exception("Erreur lecture archive")
            QtWidgets.QMessageBox.critical(
                self, "Erreur", "Impossible de lire l'archive.")
            self.reject()

    def _q(self, sql, params=()):
        return self._conn.execute(sql, params).fetchall()

    def _q1(self, sql, params=()):
        return self._conn.execute(sql, params).fetchone()

    # ══════════════════════════════════════════════════════════════
    def _render_ventes(self):
        try:
            row = self._q1("""
                SELECT COALESCE(SUM(Total), 0) AS ca,
                       COUNT(DISTINCT Num_fact) AS n_ventes,
                       COALESCE(SUM(Quantite), 0) AS n_art
                FROM Historique
                WHERE COALESCE(annule, 0) = 0
            """)
            ca = float(row["ca"] or 0)
            n_v = int(row["n_ventes"] or 0)
            n_a = int(row["n_art"] or 0)
            panier = ca / n_v if n_v else 0
            devise = "FC"

            txt = (
                f"<b>Chiffre d'affaires total :</b> "
                f"{ca:,.0f} {devise}<br>"
                f"<b>Nombre de factures :</b> {n_v}<br>"
                f"<b>Articles vendus :</b> {n_a}<br>"
                f"<b>Panier moyen :</b> {panier:,.0f} {devise}"
            ).replace(",", " ")
            self.lbl_ventes_stats.setText(txt)

            # Top 10 produits
            rows = self._q("""
                SELECT Article, SUM(Quantite) AS q, SUM(Total) AS ca
                FROM Historique
                WHERE COALESCE(annule, 0) = 0
                GROUP BY Article
                ORDER BY ca DESC LIMIT 10
            """)
            t = self.table_top_produits
            t.setRowCount(len(rows))
            fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
            for i, r in enumerate(rows):
                it0 = QtWidgets.QTableWidgetItem(r["Article"] or "—")
                it0.setFont(fb)
                t.setItem(i, 0, it0)

                it1 = QtWidgets.QTableWidgetItem(str(int(r["q"] or 0)))
                it1.setTextAlignment(Qt.AlignCenter)
                it1.setForeground(QtGui.QColor("#0077B6"))
                it1.setFont(fb)
                t.setItem(i, 1, it1)

                ca_str = f"{float(r['ca'] or 0):,.0f} {devise}".replace(",", " ")
                it2 = QtWidgets.QTableWidgetItem(ca_str)
                it2.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                it2.setForeground(QtGui.QColor("#16A34A"))
                it2.setFont(fb)
                t.setItem(i, 2, it2)

            h = t.horizontalHeader()
            h.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            h.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            h.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        except Exception:
            logger.exception("Erreur rendu ventes")

    def _render_clients(self):
        try:
            row = self._q1("SELECT COUNT(*) AS n FROM Client")
            n = int(row["n"] or 0)

            row2 = self._q1("""
                SELECT COUNT(*) AS n FROM Client
                WHERE numero LIKE 'ANON-%'
            """)
            anon = int(row2["n"] or 0)
            identifies = n - anon

            txt = (
                f"<b>Clients enregistrés :</b> {n}<br>"
                f"<b>Identifiés :</b> {identifies}<br>"
                f"<b>Anonymes :</b> {anon}"
            )
            self.lbl_clients_stats.setText(txt)

            rows = self._q("""
                SELECT COALESCE(C_name, nom) AS nom, Montant_total
                FROM Client
                WHERE actif = 1
                ORDER BY Montant_total DESC LIMIT 10
            """)
            t = self.table_top_clients
            t.setRowCount(len(rows))
            fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
            for i, r in enumerate(rows):
                it0 = QtWidgets.QTableWidgetItem(r["nom"] or "—")
                it0.setFont(fb)
                t.setItem(i, 0, it0)

                ca_str = f"{float(r['Montant_total'] or 0):,.0f} FC".replace(",", " ")
                it1 = QtWidgets.QTableWidgetItem(ca_str)
                it1.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                it1.setForeground(QtGui.QColor("#16A34A"))
                it1.setFont(fb)
                t.setItem(i, 1, it1)

            h = t.horizontalHeader()
            h.setSectionHeaderItem if False else None
            h.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            h.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        except Exception:
            logger.exception("Erreur rendu clients")

    def _render_stocks(self):
        try:
            row = self._q1("""
                SELECT COUNT(*) AS n,
                       COALESCE(SUM(Quantite), 0) AS total
                FROM produits WHERE actif = 1
            """)
            n = int(row["n"] or 0)
            total = int(row["total"] or 0)

            row2 = self._q1("""
                SELECT COUNT(*) AS n FROM produits
                WHERE actif = 1 AND Quantite <= 5
            """)
            rupture = int(row2["n"] or 0)

            txt = (
                f"<b>Produits actifs :</b> {n}<br>"
                f"<b>Unités en stock :</b> {total}<br>"
                f"<b>Produits en rupture (≤ 5) :</b> {rupture}"
            )
            self.lbl_stocks_stats.setText(txt)

            rows = self._q("""
                SELECT Nom, Quantite FROM produits
                WHERE actif = 1 AND Quantite <= 20
                ORDER BY Quantite ASC LIMIT 20
            """)
            t = self.table_rupture
            t.setRowCount(len(rows))
            fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
            for i, r in enumerate(rows):
                it0 = QtWidgets.QTableWidgetItem(r["Nom"] or "—")
                it0.setFont(fb)
                t.setItem(i, 0, it0)

                q = int(r["Quantite"] or 0)
                it1 = QtWidgets.QTableWidgetItem(str(q))
                it1.setTextAlignment(Qt.AlignCenter)
                it1.setFont(fb)
                it1.setForeground(QtGui.QColor(
                    "#dc2626" if q <= 5 else "#f4a261"))
                t.setItem(i, 1, it1)

            h = t.horizontalHeader()
            h.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            h.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        except Exception:
            logger.exception("Erreur rendu stocks")

    # ══════════════════════════════════════════════════════════════
    def _cleanup(self):
        """Ferme la connexion + supprime le dossier temp. Idempotent."""
        if getattr(self, "_cleaned_up", False):
            return
        self._cleaned_up = True

        try:
            if self._conn:
                self._conn.close()
                self._conn = None
        except Exception:
            pass

        try:
            if self._tmp_dir:
                backup_engine.cleanup_temp(self._tmp_dir)
                self._tmp_dir = ""
        except Exception:
            pass

    def closeEvent(self, event):
        """Nettoyage simple, PAS de super().closeEvent() (évite la récursion)."""
        self._cleanup()
        event.accept()

    def accept(self):
        self._cleanup()
        super().accept()

    def reject(self):
        self._cleanup()
        super().reject()