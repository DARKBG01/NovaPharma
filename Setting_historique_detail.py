#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_historique_detail.py — Détail d'une facture.
=====================================================
"""

import logging

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Client.api_singleton import get_api, is_client_mode
from Database import audit, db
from Database import encaissement as enc_engine
from Interface_historique_detail import Ui_Dialog
from Ui_helpers import setup_historique_detail_table

logger = logging.getLogger(__name__)


class Setting_historique_detail(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None, num_fact=None,
                 user_id=None, user_name="", role="UTILISATEUR",
                 is_owner=False, is_developer=False):
        super().__init__(parent)
        self.setupUi(self)

        self.num_fact = num_fact
        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.role = (role or "UTILISATEUR").upper()
        self.is_owner = is_owner
        self.is_developer = is_developer
        setup_historique_detail_table(self.table_lignes)

        self.btn_close.clicked.connect(self.accept)
        self.btn_cancel_sale.clicked.connect(self._on_cancel_sale)
        self.btn_reprint.clicked.connect(self._on_reprint)

        # ─── Bouton "Annuler la vente" : OWNER / DEV / ADMIN ───
        can_cancel = (self.is_owner or self.is_developer
                      or self.role == "ADMIN")
        self.btn_cancel_sale.setVisible(can_cancel)

        self._load()
        self._render()

    def _load(self):
        """Charge les lignes d'une facture — API ou DB."""
        try:
            if is_client_mode():
                api = get_api()
                data = api.get_vente(self.num_fact)
                self._lignes = []
                for l in data.get("lignes", []):
                    self._lignes.append({
                        "Article": l.get("Article"),
                        "Code_reference": l.get("Code_reference"),
                        "Quantite": l.get("Quantite"),
                        "Prix_uni": l.get("Prix_uni"),
                        "Total": l.get("Total"),
                        "Client_name": data.get("Client_name"),
                        "Caisse": data.get("Caisse"),
                        "Date_vent": data.get("Date_vent"),
                        "utilisateur_id": data.get("utilisateur_id"),
                        "annule": data.get("annule", 0),
                        "motif_annulation": data.get("motif_annulation"),
                    })
            else:
                rows = db.query(
                    """SELECT Article, Code_reference, Quantite, Prix_uni, Total,
                              Client_name, Caisse, Date_vent,
                              utilisateur_id, annule, motif_annulation
                       FROM Historique
                       WHERE Num_fact = ?
                       ORDER BY Id ASC""",
                    (self.num_fact,))
                self._lignes = [dict(r) for r in rows]
        except Exception:
            logger.exception("Erreur chargement facture")
            self._lignes = []

    def _render(self):
        if not self._lignes:
            self.val_fact.setText(self.num_fact or "—")
            self.val_date.setText("—")
            self.val_client.setText("—")
            self.val_caissier.setText("—")
            self.val_statut.setText("—")
            self.table_lignes.setRowCount(0)
            self.lbl_total_value.setText("0 FC")
            return

        first = self._lignes[0]
        is_annule = int(first.get("annule", 0)) == 1
        devise = db.get_config("devise", "FC")

        # Header
        self.lbl_header_title.setText(f"Facture {self.num_fact}")
        self.lbl_header_sub.setText(str(first.get("Date_vent") or "—"))

        # Info card
        self.val_fact.setText(str(self.num_fact or "—"))
        self.val_date.setText(str(first.get("Date_vent") or "—"))
        self.val_client.setText(first.get("Client_name") or "Client anonyme")
        self.val_caissier.setText(self._caissier_name(
            first.get("utilisateur_id")))

        if is_annule:
            self.val_statut.setText("ANNULÉE")
            self.val_statut.setStyleSheet(
                "color: #b91c1c; font-size: 13px; font-weight: 800;")
            self.lbl_motif_annul.setText(
                f"Motif d'annulation : "
                f"{first.get('motif_annulation') or '(non précisé)'}")
            self.lbl_motif_annul.setVisible(True)
        else:
            self.val_statut.setText("VALIDÉE")
            self.val_statut.setStyleSheet(
                "color: #15803d; font-size: 13px; font-weight: 800;")
            self.lbl_motif_annul.setVisible(False)

        setup_historique_detail_table(self.table_lignes)
        
        # Lignes
        t = self.table_lignes
        t.setRowCount(len(self._lignes))

        total_general = 0.0
        fn = QtGui.QFont("Segoe UI", 10)
        fb = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)

        for i, l in enumerate(self._lignes):
            art = QtWidgets.QTableWidgetItem(l["Article"] or "—")
            art.setFont(fb)
            art.setForeground(QtGui.QColor("#0f172a"))
            t.setItem(i, 0, art)

            qte = QtWidgets.QTableWidgetItem(str(int(l["Quantite"] or 0)))
            qte.setFont(fb)
            qte.setForeground(QtGui.QColor("#0077B6"))
            qte.setTextAlignment(Qt.AlignCenter)
            t.setItem(i, 1, qte)

            pu = QtWidgets.QTableWidgetItem(
                f"{float(l['Prix_uni'] or 0):,.2f} {devise}".replace(",", " "))
            pu.setFont(fn)
            pu.setForeground(QtGui.QColor("#475569"))
            pu.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, 2, pu)

            tot = QtWidgets.QTableWidgetItem(
                f"{float(l['Total'] or 0):,.2f} {devise}".replace(",", " "))
            tot.setFont(fb)
            tot.setForeground(QtGui.QColor("#16A34A"))
            tot.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            t.setItem(i, 3, tot)

            total_general += float(l["Total"] or 0)

        # Total (dual FC/USD)
        try:
            from Database.currency import format_dual
            self.lbl_total_value.setText(format_dual(total_general))
        except Exception:
            self.lbl_total_value.setText(
                f"{total_general:,.2f} {devise}".replace(",", " "))
        if is_annule:
            self.lbl_total_value.setStyleSheet(
                "color: #94a3b8; font-size: 22px; font-weight: 800; "
                "text-decoration: line-through; background: transparent;")

        # ─── Encaissement (reçu / rendu) ───
        self._render_encaissement(devise)

    def _render_encaissement(self, devise: str) -> None:
        """Affiche le montant reçu et rendu si disponible."""
        enc = None
        try:
            if is_client_mode():
                api = get_api()
                enc = api.get_encaissement(self.num_fact)
            else:
                enc = enc_engine.get_encaissement(self.num_fact)
        except Exception:
            enc = None

        # Crée le label une seule fois
        if not hasattr(self, "_lbl_encaissement"):
            self._lbl_encaissement = QtWidgets.QLabel()
            self._lbl_encaissement.setAlignment(Qt.AlignCenter)
            self._lbl_encaissement.setStyleSheet(
                "color: #15803d; font-size: 14px; font-weight: 800; "
                "background: #dcfce7; border-radius: 10px; padding: 10px;"
            )
            # Ajoute au bas du dialog
            if self.layout():
                self.layout().addWidget(self._lbl_encaissement)

        if enc:
            devise_p = enc.get("devise_paiement", "FC")
            m_recu = float(enc.get("montant_recu", 0))
            m_rendu = float(enc.get("montant_rendu", 0))

            txt = (
                f"Payé : {m_recu:,.2f} {devise_p}  ·  "
                f"Rendu : {m_rendu:,.2f} {devise}"
            ).replace(",", " ")
            self._lbl_encaissement.setText(txt)
            self._lbl_encaissement.show()
        else:
            self._lbl_encaissement.hide()

    # ══════════════════════════════════════════════════════════════
    # Annulation de la vente
    # ══════════════════════════════════════════════════════════════
    def _on_cancel_sale(self):
        """Annule la vente (marque comme annulée + restitue le stock)."""
        # ─── Vérifie qu'on a bien une vente ───
        if not self._lignes:
            QtWidgets.QMessageBox.warning(
                self, "Aucune vente",
                "Impossible d'annuler : aucune vente trouvée.")
            return

        first = self._lignes[0]
        is_annule = int(first.get("annule", 0)) == 1

        if is_annule:
            QtWidgets.QMessageBox.information(
                self, "Déjà annulée",
                "Cette vente a déjà été annulée.")
            return

        # ─── Vérif permissions ───
        if not (self.is_owner or self.is_developer
                or self.role == "ADMIN"):
            QtWidgets.QMessageBox.warning(
                self, "Accès refusé",
                "Seul un administrateur peut annuler une vente.")
            return

        # ─── Saisie du motif ───
        motifs = [
            "Erreur de saisie",
            "Client s'est ravisé",
            "Produit défectueux",
            "Doublon",
            "Prix incorrect",
            "Autre (préciser)",
        ]
        motif, ok = QtWidgets.QInputDialog.getItem(
            self, "Annulation de la vente",
            "Motif de l'annulation :",
            motifs, 0, False)
        if not ok or not motif:
            return

        if motif.startswith("Autre"):
            motif, ok2 = QtWidgets.QInputDialog.getText(
                self, "Motif personnalisé",
                "Précisez le motif :",
                QtWidgets.QLineEdit.Normal, "")
            if not ok2 or not motif.strip():
                QtWidgets.QMessageBox.warning(
                    self, "Motif obligatoire",
                    "Le motif est obligatoire pour annuler une vente.")
                return
            motif = motif.strip()

        # ─── Calcul du total et du nombre d'articles ───
        total_general = sum(float(l.get("Total") or 0)
                            for l in self._lignes)
        nb_articles = len(self._lignes)
        devise = db.get_config("devise", "FC")

        # ─── Confirmation finale ───
        msg = (
            f"<b>Annuler la vente {self.num_fact} ?</b><br><br>"
            f"<b>Motif :</b> {motif}<br>"
            f"<b>Articles :</b> {nb_articles}<br>"
            f"<b>Montant :</b> {total_general:,.0f} {devise}"
            .replace(",", " ") + "<br><br>"
            "<b>Cette action est définitive.</b><br>"
            "Le stock sera <b>restitué</b> automatiquement."
        )
        rep = QtWidgets.QMessageBox.question(
            self, "Confirmation finale", msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        if rep != QtWidgets.QMessageBox.Yes:
            return

        # ═══ MODE CLIENT → API ═══
        if is_client_mode():
            try:
                api = get_api()
                api.annuler_vente(self.num_fact, motif)
                logger.info("Vente annulée (API) : %s (motif: %s)",
                            self.num_fact, motif)
                QtWidgets.QMessageBox.information(
                    self, "Vente annulée",
                    f"La vente <b>{self.num_fact}</b> a été annulée.")
                self.accept()
                return
            except Exception as e:
                logger.exception("Erreur annulation vente (API)")
                QtWidgets.QMessageBox.critical(
                    self, "Erreur",
                    f"Impossible d'annuler la vente :\n{e}")
                return

        # ═══ MODE AUTONOME / SERVEUR → DB locale ═══
        try:
            with db.transaction():
                # 1. Marque la vente comme annulée
                db.execute(
                    """UPDATE Historique
                       SET annule = 1, motif_annulation = ?
                       WHERE Num_fact = ?""",
                    (motif, self.num_fact))

                # 2. Restitue le stock
                for l in self._lignes:
                    code_ref = l.get("Code_reference")
                    if not code_ref:
                        continue

                    qte = int(l.get("Quantite") or 0)

                    row_p = db.query_one(
                        "SELECT Quantite, Nom FROM produits "
                        "WHERE Code_reference = ? LIMIT 1",
                        (code_ref,))
                    if not row_p:
                        continue

                    stock_avant = int(row_p["Quantite"] or 0)
                    stock_apres = stock_avant + qte

                    db.execute(
                        """UPDATE produits
                           SET Quantite = ?
                           WHERE Code_reference = ?""",
                        (stock_apres, code_ref))

                    # Log du mouvement de stock
                    db.execute(
                        """INSERT INTO MouvementStock
                           (id, produit_id, type, quantite,
                            stock_avant, stock_apres, motif, utilisateur_id)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (db.new_id(), code_ref, "ANNULATION", qte,
                         stock_avant, stock_apres,
                         f"Annulation vente {self.num_fact} — {motif}",
                         self.user_id))

                # 3. Si client identifié → déduire le montant
                client_name = first.get("Client_name") or ""
                if client_name and "anonyme" not in client_name.lower():
                    # Extrait le numéro du client (dernier mot)
                    parts = client_name.strip().split(" ")
                    if parts:
                        num_client = parts[-1]
                        try:
                            row_c = db.query_one(
                                "SELECT Montant_total FROM Client "
                                "WHERE numero = ? LIMIT 1",
                                (num_client,))
                            if row_c:
                                total_actuel = float(
                                    row_c["Montant_total"] or 0)
                                nouveau = max(
                                    0.0, total_actuel - total_general)
                                db.execute(
                                    """UPDATE Client
                                       SET Montant_total = ?
                                       WHERE numero = ?""",
                                    (nouveau, num_client))
                        except Exception:
                            logger.exception(
                                "Erreur mise à jour client")

                # 4. Audit
                audit.log(
                    "ANNULATION_VENTE",
                    utilisateur_id=self.user_id,
                    utilisateur_name=self.user_name,
                    cible_type="vente",
                    cible_id=self.num_fact,
                    cible_nom=self.num_fact,
                    details={
                        "motif": motif,
                        "montant": total_general,
                        "nb_articles": nb_articles,
                    })

            logger.info("Vente annulée : %s (motif: %s)",
                        self.num_fact, motif)

            QtWidgets.QMessageBox.information(
                self, "Vente annulée",
                f"La vente <b>{self.num_fact}</b> a été annulée.\n\n"
                f"Le stock a été restitué automatiquement.\n"
                f"La référence client a été mise à jour.")

            self.accept()

        except Exception as e:
            logger.exception("Erreur annulation vente")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible d'annuler la vente :\n{e}")

    # ══════════════════════════════════════════════════════════════
    # Réimpression PDF
    # ══════════════════════════════════════════════════════════════
    def _on_reprint(self):
        """Régénère le PDF de cette facture."""
        if not self._lignes:
            QtWidgets.QMessageBox.warning(
                self, "Aucune donnée",
                "Impossible de réimprimer : aucune ligne trouvée.")
            return

        # ─── Demande où enregistrer ───
        import os
        from datetime import datetime

        default_name = f"{self.num_fact}.pdf"
        default_dir = os.path.join(
            "Factures", "Reimpressions")
        os.makedirs(default_dir, exist_ok=True)
        default_path = os.path.join(default_dir, default_name)

        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Enregistrer la facture",
            default_path,
            "Fichier PDF (*.pdf)")
        if not path:
            return

        # ─── Reconstruit les données ───
        try:
            if is_client_mode():
                data = self._build_facture_data_api()
            else:
                data = self._build_facture_data()

            # ─── Génère le PDF ───
            from Facture_gen import Generer_ticket_final
            Generer_ticket_final(data, path)

            # ─── Audit ───
            try:
                audit.log("REIMPRESSION_FACTURE",
                          utilisateur_id=self.user_id,
                          utilisateur_name=self.user_name,
                          cible_type="vente",
                          cible_id=self.num_fact,
                          cible_nom=self.num_fact,
                          details={"path": path})
            except Exception:
                pass

            logger.info("Facture réimprimée : %s → %s",
                        self.num_fact, path)

            # ─── Propose d'ouvrir le PDF ───
            rep = QtWidgets.QMessageBox.question(
                self, "Réimpression réussie",
                f"La facture a été régénérée :\n\n{path}\n\n"
                "Voulez-vous l'ouvrir maintenant ?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.Yes)

            if rep == QtWidgets.QMessageBox.Yes:
                try:
                    from PySide6 import QtGui, QtCore
                    QtGui.QDesktopServices.openUrl(
                        QtCore.QUrl.fromLocalFile(
                            os.path.abspath(path)))
                except Exception:
                    logger.exception("Impossible d'ouvrir le PDF")

        except Exception as e:
            logger.exception("Erreur réimpression")
            QtWidgets.QMessageBox.critical(
                self, "Erreur",
                f"Impossible de réimprimer la facture :\n{e}")

    # ══════════════════════════════════════════════════════════════
    def _build_facture_data(self) -> dict:
        """
        Reconstruit le dict `data` attendu par Generer_ticket_final
        depuis les lignes chargées en mémoire.
        """
        first = self._lignes[0]

        # ─── Infos pharmacie ───
        nom_entreprise = "NOVA PHARMA"
        adresse = ""
        telephone = ""
        try:
            ph = db.query_one(
                "SELECT nom, adresse, numero FROM Pharmacie "
                "WHERE id = 1 LIMIT 1")
            if ph:
                nom_entreprise = ph["nom"] or "NOVA PHARMA"
                adresse = ph["adresse"] or ""
                telephone = ph["numero"] or ""
        except Exception:
            pass

        # ─── Panier ───
        panier = []
        for l in self._lignes:
            panier.append([
                l.get("Article") or "",
                int(l.get("Quantite") or 0),
                float(l.get("Prix_uni") or 0),
                float(l.get("Total") or 0),
            ])

        # ─── Total ───
        total_general = sum(float(l.get("Total") or 0)
                            for l in self._lignes)

        # ─── Client ───
        client_name = first.get("Client_name") or "Client anonyme"
        # Sépare "Nom Numéro" → Nom, Numéro
        num_client = ""
        nom_client = client_name
        if client_name and "anonyme" not in client_name.lower():
            parts = client_name.strip().rsplit(" ", 1)
            if len(parts) == 2 and (parts[1].startswith("0")
                                    or parts[1].startswith("+243")):
                nom_client = parts[0]
                num_client = parts[1]

        # ─── Mentions ───
        try:
            mentions = db.get_config("mentions_ticket", None)
            if not isinstance(mentions, list):
                mentions = []
        except Exception:
            mentions = []
        
        # ─── Indicateur "ANNULÉE" ───
        is_annule = int(first.get("annule", 0)) == 1
        if is_annule:
            mentions.insert(0, "*** VENTE ANNULÉE ***")
            motif = first.get("motif_annulation") or ""
            if motif:
                mentions.insert(1, f"Motif : {motif}")

        return {
            "Numero facture": self.num_fact,
            "Numero de la caisse": first.get("Caisse") or "A",
            "Produit vendu": panier,
            "Numero client": num_client,
            "Nom client": nom_client,
            "date": first.get("Date_vent") or "",
            "Total general": total_general,
            "Nom entreprise": nom_entreprise,
            "Adresse entreprise": adresse,
            "Telephone entreprise": telephone,
            "Mention": mentions,
        }

    def _build_facture_data_api(self) -> dict:
        """Construit le dict pour le PDF depuis l'API."""
        api = get_api()
        vente = api.get_vente(self.num_fact)
        lignes = vente.get("lignes", [])

        # Infos pharmacie (locales au client)
        nom_entreprise = "NOVA PHARMA"
        adresse = ""
        telephone = ""
        try:
            ph = db.query_one(
                "SELECT nom, adresse, numero FROM Pharmacie "
                "WHERE id = 1 LIMIT 1")
            if ph:
                nom_entreprise = ph["nom"] or "NOVA PHARMA"
                adresse = ph["adresse"] or ""
                telephone = ph["numero"] or ""
        except Exception:
            pass

        panier = [
            [l.get("Article") or "",
             int(l.get("Quantite") or 0),
             float(l.get("Prix_uni") or 0),
             float(l.get("Total") or 0)]
            for l in lignes
        ]

        client_name = vente.get("Client_name") or "Client anonyme"
        num_client = ""
        nom_client = client_name
        if client_name and "anonyme" not in client_name.lower():
            parts = client_name.strip().rsplit(" ", 1)
            if len(parts) == 2 and (parts[1].startswith("0")
                                    or parts[1].startswith("+243")):
                nom_client = parts[0]
                num_client = parts[1]

        mentions = []
        is_annule = int(vente.get("annule") or 0) == 1
        if is_annule:
            mentions.append("*** VENTE ANNULÉE ***")
            motif = vente.get("motif_annulation") or ""
            if motif:
                mentions.append(f"Motif : {motif}")

        return {
            "Numero facture": self.num_fact,
            "Numero de la caisse": vente.get("Caisse") or "A",
            "Produit vendu": panier,
            "Numero client": num_client,
            "Nom client": nom_client,
            "date": vente.get("Date_vent") or "",
            "Total general": float(vente.get("total") or 0),
            "Nom entreprise": nom_entreprise,
            "Adresse entreprise": adresse,
            "Telephone entreprise": telephone,
            "Mention": mentions,
        }
    
    @staticmethod
    def _caissier_name(uid):
        if not uid:
            return "—"
        try:
            r = db.query_one(
                "SELECT COALESCE(prenom, '') || ' ' || COALESCE(nom, '') "
                "AS nom FROM Utilisateur WHERE id = ? LIMIT 1",
                (uid,))
            return (r["nom"].strip() if r else "—") or "—"
        except Exception:
            return "—"
