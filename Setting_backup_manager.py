#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_backup_manager.py — Gestionnaire des sauvegardes.
============================================================
Liste les archives, permet de :
  - Créer une sauvegarde manuelle
  - Ouvrir une archive en lecture seule
  - Supprimer une archive
"""

import logging
from datetime import datetime

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db, backup_engine
from Interface_backup_manager import Ui_Dialog

logger = logging.getLogger(__name__)


COL_NAME = 0
COL_TYPE = 1
COL_DATE = 2
COL_SIZE = 3


class Setting_backup_manager(QtWidgets.QDialog, Ui_Dialog):

    backup_created = QtCore.Signal(str)

    def __init__(self, parent=None, user_id=None, user_name=""):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"

        self._backups = []
        self._temp_dir = None

        self._setup_table()
        self._connect_signals()
        self._refresh()

    # ══════════════════════════════════════════════════════════════
    def _setup_table(self):
        h = self.table_backups.horizontalHeader()
        h.setSectionResizeMode(COL_NAME, QtWidgets.QHeaderView.Stretch)
        h.setSectionResizeMode(COL_TYPE, QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_DATE, QtWidgets.QHeaderView.ResizeToContents)
        h.setSectionResizeMode(COL_SIZE, QtWidgets.QHeaderView.ResizeToContents)
        self.table_backups.verticalHeader().setVisible(False)
        self.table_backups.verticalHeader().setDefaultSectionSize(44)

    def _connect_signals(self):
        self.btn_close.clicked.connect(self.accept)
        self.btn_new_backup.clicked.connect(self._on_new_backup)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_view.clicked.connect(self._on_view)
        self.table_backups.itemSelectionChanged.connect(
            self._on_selection_changed)
        self.table_backups.doubleClicked.connect(self._on_view)

    # ══════════════════════════════════════════════════════════════
    def _refresh(self):
        self._backups = backup_engine.list_backups()
        self._populate()
        self._update_stats()
        self._on_selection_changed()

    def _populate(self):
        t = self.table_backups
        t.blockSignals(True)
        t.setRowCount(0)
        t.clearSpans()

        if not self._backups:
            t.setRowCount(1)
            item = QtWidgets.QTableWidgetItem(
                "Aucune sauvegarde disponible")
            item.setTextAlignment(Qt.AlignCenter)
            item.setForeground(QtGui.QColor("#94a3b8"))
            f = QtGui.QFont("Segoe UI", 11)
            f.setItalic(True)
            item.setFont(f)
            t.setItem(0, 0, item)
            t.setSpan(0, 0, 1, t.columnCount())
            t.blockSignals(False)
            return

        t.setRowCount(len(self._backups))
        fn = QtGui.QFont("Segoe UI", 10)
        fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)
        fm = QtGui.QFont("Courier New", 9)

        type_colors = {
            "daily":   ("#1e40af", "#dbeafe"),
            "weekly":  ("#15803d", "#dcfce7"),
            "monthly": ("#92400e", "#fef3c7"),
            "yearly":  ("#4338ca", "#e0e7ff"),
        }

        for i, b in enumerate(self._backups):
            # Nom
            it0 = QtWidgets.QTableWidgetItem(b["name"])
            it0.setFont(fm)
            it0.setForeground(QtGui.QColor("#0f172a"))
            it0.setData(Qt.UserRole, b["path"])
            t.setItem(i, COL_NAME, it0)

            # Type
            fg, bg = type_colors.get(b["type"], ("#334155", "#f1f5f9"))
            it1 = QtWidgets.QTableWidgetItem(b["type"].upper())
            it1.setFont(fb)
            it1.setForeground(QtGui.QColor(fg))
            it1.setBackground(QtGui.QColor(bg))
            it1.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, COL_TYPE, it1)

            # Date
            dt_str = b["date"].strftime("%d/%m/%Y %H:%M")
            it2 = QtWidgets.QTableWidgetItem(dt_str)
            it2.setFont(fn)
            it2.setForeground(QtGui.QColor("#475569"))
            t.setItem(i, COL_DATE, it2)

            # Taille
            size_mb = b["size"] / (1024 * 1024)
            it3 = QtWidgets.QTableWidgetItem(f"{size_mb:.1f} MB")
            it3.setFont(fn)
            it3.setForeground(QtGui.QColor("#64748b"))
            it3.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, COL_SIZE, it3)

        t.blockSignals(False)

    def _update_stats(self):
        if not self._backups:
            self.lbl_stats.setText("Aucune archive")
            return
        total = sum(b["size"] for b in self._backups)
        total_mb = total / (1024 * 1024)
        self.lbl_stats.setText(
            f"{len(self._backups)} archive(s) • "
            f"{total_mb:.1f} MB au total")

    def _selected(self):
        row = self.table_backups.currentRow()
        if row < 0 or row >= len(self._backups):
            return None
        return self._backups[row]

    def _on_selection_changed(self):
        b = self._selected()
        self.btn_view.setEnabled(b is not None)
        self.btn_delete.setEnabled(b is not None)

    # ══════════════════════════════════════════════════════════════
    def _on_new_backup(self):
        try:
            path = backup_engine.create_backup(
                "manual",
                user_id=self.user_id,
                user_name=self.user_name)
            if path:
                QtWidgets.QMessageBox.information(
                    self, "Sauvegarde créée",
                    f"L'archive a été créée :\n{path}")
                self.backup_created.emit(path)
                self._refresh()
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Échec",
                    "Impossible de créer la sauvegarde.")
        except Exception as e:
            logger.exception("Erreur création backup")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _on_delete(self):
        b = self._selected()
        if not b:
            return
        rep = QtWidgets.QMessageBox.question(
            self, "Supprimer l'archive",
            f"Supprimer cette sauvegarde ?\n\n{b['name']}\n\n"
            "Cette action est irréversible.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        try:
            from Database import audit

            # ─── Infos avant suppression ───
            taille = b.get("size", 0)
            path = b["path"]
            name = b["name"]

            if backup_engine.delete_backup(path):
                # ═══ AUDIT ═══
                try:
                    audit.log(
                        audit.ACTION_BACKUP_SUPPRESSION,
                        utilisateur_id=self.user_id,
                        utilisateur_name=self.user_name,
                        cible_type="backup",
                        cible_id=name,
                        cible_nom=name,
                        details={
                            "path": path,
                            "size": taille,
                        },
                        severite="warning")
                except Exception:
                    logger.exception("Erreur audit suppression backup")

                self._refresh()
        except Exception as e:
            logger.exception("Erreur suppression backup")
            QtWidgets.QMessageBox.critical(self, "Erreur", str(e))

    def _on_view(self):
        b = self._selected()
        if not b:
            return
        try:
            from Setting_backup_reader import Setting_backup_reader
            dlg = Setting_backup_reader(
                parent=self,
                archive_path=b["path"],
                archive_name=b["name"])
            dlg.exec()
        except Exception:
            logger.exception("Erreur ouverture lecture seule")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                "Impossible d'ouvrir l'archive.")


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()
    seed.run()
    dlg = Setting_backup_manager(user_id="TEST", user_name="Test")
    sys.exit(dlg.exec())