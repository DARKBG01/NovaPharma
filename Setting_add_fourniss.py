#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_add_fourniss.py — Dialogue d'ajout de fournisseur.
============================================================
- Utilise Database/db.py (plus de Users.db)
- Génère un Id_fournisseur automatique (FOU-XXXX)
- Renseigne Adresse, actif, created_at
- Audit CREATION_FOURNISSEUR
"""

import logging
import re

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db, audit
from Interface_add_fournisseur import Ui_DialogAddFournisseur

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_REGEX = re.compile(r"^[+0-9\s\-()]{6,20}$")


class Setting_add_fourniss(QtWidgets.QDialog, Ui_DialogAddFournisseur):

    fournisseur_created = QtCore.Signal(str)  # Id_fournisseur

    def __init__(self, parent=None, user_id=None, user_name=""):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"

        self._connect_signals()
        self._update_progress()

        self.edit_raison_sociale.setFocus()

    # ══════════════════════════════════════════════════════════════
    def _connect_signals(self):
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self._on_save)

        for w in (self.edit_raison_sociale, self.edit_nom_contact,
                  self.edit_tel_contact, self.edit_email_contact,
                  self.edit_adresse):
            w.textChanged.connect(self._update_progress)

        self.edit_raison_sociale.returnPressed.connect(self._on_save)
        self.edit_nom_contact.returnPressed.connect(self._on_save)
        self.edit_tel_contact.returnPressed.connect(self._on_save)
        self.edit_email_contact.returnPressed.connect(self._on_save)

    # ══════════════════════════════════════════════════════════════
    def _update_progress(self):
        entreprise = self.edit_raison_sociale.text().strip()
        self.btn_save.setEnabled(len(entreprise) >= 3)

    # ══════════════════════════════════════════════════════════════
    def _show_error(self, msg: str):
        self.lbl_error.setText(f"Erreur : {msg}")
        self.lbl_error.setVisible(True)

    def _hide_error(self):
        self.lbl_error.setVisible(False)
        self.lbl_error.setText("")

    # ══════════════════════════════════════════════════════════════
    def _validate(self):
        entreprise = self.edit_raison_sociale.text().strip()
        if len(entreprise) < 3:
            return False, "Le nom de l'entreprise est trop court."

        email = self.edit_email_contact.text().strip().lower()
        if email and not EMAIL_REGEX.match(email):
            return False, "Email invalide."

        tel = self.edit_tel_contact.text().strip()
        if tel and not PHONE_REGEX.match(tel):
            return False, "Téléphone invalide."

        # Unicité entreprise
        try:
            if db.query_one(
                "SELECT 1 FROM Fournisseur WHERE LOWER(Entreprise) = LOWER(?) LIMIT 1",
                (entreprise,)
            ):
                return False, f"Un fournisseur « {entreprise} » existe déjà."
        except Exception:
            logger.exception("Erreur vérif unicité")

        return True, ""

    # ══════════════════════════════════════════════════════════════
    def _next_id_fournisseur(self) -> str:
        """Génère FOU-0001, FOU-0002, etc."""
        try:
            row = db.query_one(
                """SELECT Id_fournisseur FROM Fournisseur
                   WHERE Id_fournisseur LIKE 'FOU-%'
                   ORDER BY Id_fournisseur DESC LIMIT 1""")
            if row and row["Id_fournisseur"]:
                try:
                    n = int(row["Id_fournisseur"].split("-")[1]) + 1
                except (ValueError, IndexError):
                    n = 1
            else:
                n = 1
            return f"FOU-{n:04d}"
        except Exception:
            logger.exception("Erreur génération Id_fournisseur")
            import time
            return f"FOU-{int(time.time()) % 10000:04d}"

    # ══════════════════════════════════════════════════════════════
    def _on_save(self):
        self._hide_error()

        valide, msg = self._validate()
        if not valide:
            self._show_error(msg)
            return

        entreprise  = self.edit_raison_sociale.text().strip().upper()
        categorie   = self.cmb_categorie.currentText().strip().upper()
        responsable = self.edit_nom_contact.text().strip().upper() or None
        numero      = self.edit_tel_contact.text().strip() or None
        email       = self.edit_email_contact.text().strip().lower() or None
        adresse     = self.edit_adresse.text().strip() or None

        id_four = self._next_id_fournisseur()

        try:
            with db.transaction():
                db.execute("""
                    INSERT INTO Fournisseur
                    (Id_fournisseur, Entreprise, Categorie, Responsable,
                     Numero, Email, Adresse, actif, created_at)
                    VALUES (?,?,?,?,?,?,?,1, datetime('now'))
                """, (id_four, entreprise, categorie, responsable,
                      numero, email, adresse))

                audit.log(
                    "CREATION_FOURNISSEUR",
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="fournisseur",
                    cible_id=id_four,
                    cible_nom=entreprise,
                    details={
                        "categorie": categorie,
                        "responsable": responsable,
                        "numero": numero,
                        "email": email,
                    })

            logger.info("Fournisseur créé : %s (%s)", entreprise, id_four)
            self.fournisseur_created.emit(id_four)

            QtWidgets.QMessageBox.information(
                self, "Fournisseur créé",
                f"Le fournisseur « {entreprise} » a été ajouté.\n\n"
                f"Identifiant : {id_four}")
            self.accept()

        except Exception as e:
            logger.exception("Échec création fournisseur")
            self._show_error(f"Impossible d'enregistrer : {e}")


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db, seed
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()
    seed.run()
    dlg = Setting_add_fourniss(user_id="TEST", user_name="Test")
    dlg.fournisseur_created.connect(
        lambda fid: print(f"→ Créé : {fid}"))
    sys.exit(dlg.exec())