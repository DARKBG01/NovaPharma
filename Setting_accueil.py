#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_accueil.py — Page d'accueil premium.
=============================================
Utilise Interface_page_accueil.py (généré depuis Page_accueil.ui).

Contenu :
  - Hero avec CA en gros + tendance N-1
  - 3 pills de période (Semaine / Mois / Année)
  - 4 KPI cards avec tendances
  - Top 5 produits (cartes avec barres)
  - Alertes en cartes individuelles
  - Bandeau secondaire (stock / marge / annulations)
"""

import logging
from datetime import datetime, timedelta

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from Database import db
from Interface_page_accueil import Ui_PageAccueil

logger = logging.getLogger(__name__)

def _to_iso(fr_date: str) -> str:
    try:
        d, rest = fr_date.split(" ", 1)
        day, month, year = d.split("/")
        return f"{year}-{month}-{day} {rest}"
    except Exception:
        return fr_date


def _iso_expr(col: str) -> str:
    return (
        f"(substr({col}, 7, 4) || '-' || "
        f"substr({col}, 4, 2) || '-' || "
        f"substr({col}, 1, 2) || "
        f"substr({col}, 11))"
    )

# ══════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════
def _resolve_period(periode: str) -> tuple:
    """Retourne (debut, fin, debut_n1, fin_n1) format FR."""
    today = datetime.now().replace(hour=23, minute=59, second=59)
    fmt = "%d/%m/%Y %H:%M:%S"

    periode = (periode or "").strip()

    if periode == "Semaine":
        debut = today - timedelta(days=today.weekday())
    elif periode == "Mois":
        debut = today.replace(day=1)
    elif periode in ("Année", "Annee"):
        debut = today.replace(month=1, day=1, hour=0, minute=0, second=0)
    else:
        debut = today.replace(day=1)

    debut = debut.replace(hour=0, minute=0, second=0)

    try:
        debut_n1 = debut.replace(year=debut.year - 1)
        fin_n1 = today.replace(year=today.year - 1)
    except ValueError:
        debut_n1 = debut.replace(year=debut.year - 1, day=28)
        fin_n1 = today.replace(year=today.year - 1, day=28)

    return (debut.strftime(fmt), today.strftime(fmt),
            debut_n1.strftime(fmt), fin_n1.strftime(fmt))


def _fmt_money(valeur: float, devise: str = "FC") -> str:
    try:
        v = float(valeur or 0)
    except Exception:
        v = 0.0
    if abs(v) >= 1_000_000_000:
        s = f"{v/1_000_000_000:.2f}".rstrip("0").rstrip(".") + " Md"
    elif abs(v) >= 1_000_000:
        s = f"{v/1_000_000:.2f}".rstrip("0").rstrip(".") + " M"
    else:
        s = f"{v:,.0f}".replace(",", " ")
    return f"{s} {devise}"


def _trend_pct(current: float, previous: float):
    if not previous:
        return None
    try:
        return (current - previous) / previous * 100
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════
# Sous-widgets dynamiques
# ══════════════════════════════════════════════════════════════════
class TopProduitCard(QtWidgets.QFrame):
    """Une ligne produit du Top 5."""

    def __init__(self, rang: int, nom: str, qte: int,
                 ca: float, part: float, devise: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: #f8fafc;
                border: 1px solid #f1f5f9;
                border-radius: 10px;
            }
        """)
        self.setMinimumHeight(54)

        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(12, 10, 14, 10)
        h.setSpacing(12)

        # Badge rang
        badge = QtWidgets.QLabel(str(rang))
        badge.setFixedSize(28, 28)
        badge.setAlignment(Qt.AlignCenter)
        colors = {
            1: ("#fef3c7", "#92400e"),
            2: ("#e2e8f0", "#475569"),
            3: ("#fed7aa", "#9a3412"),
        }
        bg, fg = colors.get(rang, ("#f1f5f9", "#64748b"))
        badge.setStyleSheet(
            f"background: {bg}; color: {fg}; border-radius: 14px; "
            f"font-size: 12px; font-weight: 800;")
        h.addWidget(badge)

        # Nom + barre
        v = QtWidgets.QVBoxLayout()
        v.setSpacing(5)

        nom_lbl = QtWidgets.QLabel(nom[:32])
        nom_lbl.setStyleSheet(
            "color: #0f172a; font-size: 12px; font-weight: 700; "
            "background: transparent;")
        v.addWidget(nom_lbl)

        bar = QtWidgets.QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(int(min(100, part)))
        bar.setTextVisible(False)
        bar.setFixedHeight(5)
        bar.setStyleSheet("""
            QProgressBar {
                background: #e2e8f0;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #023E8A, stop:1 #00B4D8);
                border-radius: 2px;
            }
        """)
        v.addWidget(bar)

        h.addLayout(v, 1)

        # Montant
        val = QtWidgets.QLabel(_fmt_money(ca, devise))
        val.setStyleSheet(
            "color: #023E8A; font-size: 12px; font-weight: 800; "
            "background: transparent;")
        val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        val.setMinimumWidth(90)
        h.addWidget(val)

        # Quantité
        qte_lbl = QtWidgets.QLabel(f"{qte}")
        qte_lbl.setStyleSheet(
            "color: #64748b; font-size: 10px; font-weight: 700; "
            "background: transparent;")
        qte_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        qte_lbl.setMinimumWidth(40)
        h.addWidget(qte_lbl)


class AlertCard(QtWidgets.QFrame):
    """Une carte d'alerte."""

    def __init__(self, message: str, level: str = "warning",
                 parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)

        styles = {
            "danger":  ("#fef2f2", "#fecaca", "#b91c1c", "x-circle"),
            "warning": ("#fef3c7", "#fde68a", "#b45309",
                        "alert-triangle"),
            "info":    ("#eff6ff", "#bfdbfe", "#1e40af", "info"),
        }
        bg, border, fg, icon_name = styles.get(
            level, styles["warning"])

        self.setStyleSheet(f"""
            QFrame {{
                background: {bg};
                border: 1px solid {border};
                border-radius: 10px;
            }}
            QFrame:hover {{ border-color: {fg}; }}
            QLabel {{ color: {fg}; background: transparent; }}
        """)
        self.setMinimumHeight(48)

        h = QtWidgets.QHBoxLayout(self)
        h.setContentsMargins(12, 10, 12, 10)
        h.setSpacing(10)

        icon = QtWidgets.QLabel()
        icon.setFixedSize(20, 20)
        pix = QtGui.QPixmap(f":/Icon/Icons/{icon_name}.svg")
        if not pix.isNull():
            icon.setPixmap(pix.scaled(
                18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h.addWidget(icon)

        lbl = QtWidgets.QLabel(message)
        lbl.setStyleSheet(
            f"color: {fg}; font-size: 12px; font-weight: 700; "
            f"background: transparent;")
        lbl.setWordWrap(True)
        h.addWidget(lbl, 1)


# ══════════════════════════════════════════════════════════════════
# Page Accueil
# ══════════════════════════════════════════════════════════════════
class PageAccueil(QtWidgets.QWidget, Ui_PageAccueil):

    def __init__(self, parent=None, user_id=None, user_name="",
                 role="UTILISATEUR", is_owner=False,
                 is_developer=False):
        super().__init__(parent)
        self.setupUi(self)

        self.user_id = user_id
        self.user_name = user_name or "Utilisateur"
        self.role = (role or "UTILISATEUR").upper()
        self.is_owner = is_owner
        self.is_developer = is_developer

        self._periode = "Mois"
        self.devise = db.get_config("devise", "FC")

        self._setup_icons()
        self._setup_texts()
        self._connect_signals()
        self.refresh()

    # ══════════════════════════════════════════════════════════════
    def _setup_icons(self):
        """Charge les icônes SVG dans les QLabel."""
        def _load(label, svg, size):
            pix = QtGui.QPixmap(f":/Icon/Icons/{svg}.svg")
            if not pix.isNull():
                label.setPixmap(pix.scaled(
                    size, size, Qt.KeepAspectRatio,
                    Qt.SmoothTransformation))

        # KPI icons
        _load(self.kpi_ventes_icon,   "receipt",          20)
        _load(self.kpi_panier_icon,   "shopping-cart",    20)
        _load(self.kpi_clients_icon,  "users",            20)
        _load(self.kpi_ruptures_icon, "alert-triangle",   20)

        # Top5 / Alertes icons
        _load(self.lbl_top5_icon,    "award",  18)
        _load(self.lbl_alertes_icon, "bell",   18)

    def _setup_texts(self):
        """Renseigne les textes dynamiques."""
        self.lbl_salutation.setText(f"Bonjour {self.user_name}")
        self.lbl_date.setText(
            datetime.now().strftime("%A %d %B %Y").capitalize())

    def _connect_signals(self):
        """Connecte les pills de période."""
        self.btn_periode_semaine.clicked.connect(
            lambda: self._on_periode_changed("Semaine"))
        self.btn_periode_mois.clicked.connect(
            lambda: self._on_periode_changed("Mois"))
        self.btn_periode_annee.clicked.connect(
            lambda: self._on_periode_changed("Année"))

    # ══════════════════════════════════════════════════════════════
    def _on_periode_changed(self, periode: str):
        periode = (periode or "").strip()
        self._periode = periode

        # Met à jour l'état coché des pills
        self.btn_periode_semaine.setChecked(periode == "Semaine")
        self.btn_periode_mois.setChecked(periode == "Mois")
        self.btn_periode_annee.setChecked(periode == "Année")

        self.refresh()

    # ══════════════════════════════════════════════════════════════
    def refresh(self):
        """Recharge tous les KPIs."""
        try:
            self.devise = db.get_config("devise", "FC")
            self._setup_texts()

            debut, fin, debut_n1, fin_n1 = _resolve_period(self._periode)

            self._load_hero(debut, fin, debut_n1, fin_n1)
            self._load_kpis(debut, fin, debut_n1, fin_n1)
            self._load_top5(debut, fin)
            self._load_alertes()
            self._load_secondary(debut, fin)

        except Exception:
            logger.exception("Erreur refresh accueil")

    # ─── Hero ───
    def _load_hero(self, debut, fin, debut_n1, fin_n1):
        try:
            # ─── CA période courante ───
            row = db.query_one(
                f"""SELECT COALESCE(SUM(Total), 0) AS ca
                    FROM Historique
                    WHERE annule = 0
                      AND {_iso_expr('Date_vent')} >= ? 
                      AND {_iso_expr('Date_vent')} <= ?""",
                (_to_iso(debut), _to_iso(fin)))
            ca = float(row["ca"] or 0) if row else 0

            # ─── CA période N-1 (même période, an dernier) ───
            row = db.query_one(
                f"""SELECT COALESCE(SUM(Total), 0) AS ca
                    FROM Historique
                    WHERE annule = 0
                      AND {_iso_expr('Date_vent')} >= ? 
                      AND {_iso_expr('Date_vent')} <= ?""",
                (_to_iso(debut_n1), _to_iso(fin_n1)))
            ca_n1 = float(row["ca"] or 0) if row else 0

            self.lbl_ca_value.setText(_fmt_money(ca, self.devise))

            pct = _trend_pct(ca, ca_n1)
            if pct is None:
                self.lbl_ca_trend.setText("Première période")
            elif pct >= 0:
                self.lbl_ca_trend.setText(
                    f"↑  {pct:+.1f} %  vs période précédente")
            else:
                self.lbl_ca_trend.setText(
                    f"↓  {pct:+.1f} %  vs période précédente")

        except Exception:
            logger.exception("Erreur hero")

    # ─── KPIs ───
    def _load_kpis(self, debut, fin, debut_n1, fin_n1):
        try:
            row = db.query_one(
                f"""SELECT
                     COUNT(DISTINCT CASE WHEN annule=0 THEN Num_fact END) AS n_ventes,
                     COALESCE(SUM(CASE WHEN annule=0 THEN Total ELSE 0 END), 0) AS ca,
                     COUNT(DISTINCT CASE WHEN annule=0 THEN Client_name END) AS n_clients
                   FROM Historique
                   WHERE {_iso_expr('Date_vent')} >= ? 
                     AND {_iso_expr('Date_vent')} <= ?""",
                (_to_iso(debut), _to_iso(fin)))
            n_ventes = int(row["n_ventes"] or 0)
            ca = float(row["ca"] or 0)
            n_clients = int(row["n_clients"] or 0)

            row = db.query_one(
                f"""SELECT
                     COUNT(DISTINCT CASE WHEN annule=0 THEN Num_fact END) AS n_ventes,
                     COALESCE(SUM(CASE WHEN annule=0 THEN Total ELSE 0 END), 0) AS ca,
                     COUNT(DISTINCT CASE WHEN annule=0 THEN Client_name END) AS n_clients
                   FROM Historique
                   WHERE {_iso_expr('Date_vent')} >= ? 
                     AND {_iso_expr('Date_vent')} <= ?""",
                (_to_iso(debut_n1), _to_iso(fin_n1)))
            n_ventes_n1 = int(row["n_ventes"] or 0)
            ca_n1 = float(row["ca"] or 0)
            n_clients_n1 = int(row["n_clients"] or 0)

            # Ventes
            trend = _trend_pct(n_ventes, n_ventes_n1)
            self.kpi_ventes_value.setText(str(n_ventes))
            self.kpi_ventes_sub.setText("vs période préc.")
            self._set_trend_label(self.kpi_ventes_trend, trend)

            # Panier
            panier = ca / n_ventes if n_ventes else 0
            panier_n1 = ca_n1 / n_ventes_n1 if n_ventes_n1 else 0
            trend = _trend_pct(panier, panier_n1)
            self.kpi_panier_value.setText(
                _fmt_money(panier, self.devise))
            self.kpi_panier_sub.setText("par vente")
            self._set_trend_label(self.kpi_panier_trend, trend)

            # Clients
            trend = _trend_pct(n_clients, n_clients_n1)
            self.kpi_clients_value.setText(str(n_clients))
            self.kpi_clients_sub.setText("clients distincts")
            self._set_trend_label(self.kpi_clients_trend, trend)

        except Exception:
            logger.exception("Erreur KPIs ventes/clients")

        # ── Ruptures ──
        try:
            seuil = int(db.get_config("seuil_stock", 20))
            row = db.query_one(
                "SELECT COUNT(*) AS n FROM produits "
                "WHERE actif = 1 AND Quantite <= ?", (seuil,))
            n = int(row["n"] or 0) if row else 0

            self.kpi_ruptures_value.setText(str(n))
            self.kpi_ruptures_sub.setText(
                f"≤ {seuil} unités" if n > 0 else "aucun produit")
            self.kpi_ruptures_trend.setText("")
        except Exception:
            self.kpi_ruptures_value.setText("—")

    @staticmethod
    def _set_trend_label(label: QtWidgets.QLabel, pct):
        if pct is None:
            label.setText("")
            return
        if pct >= 0:
            label.setText(f"↑ {pct:+.1f} %")
            label.setStyleSheet(
                "color: #16A34A; font-size: 11px; font-weight: 700; "
                "background: transparent;")
        else:
            label.setText(f"↓ {pct:+.1f} %")
            label.setStyleSheet(
                "color: #DC2626; font-size: 11px; font-weight: 700; "
                "background: transparent;")

    # ─── Top 5 ───
    def _load_top5(self, debut, fin):
        layout = self.top5_layout

        # Vide le layout
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        try:
            rows = db.query(
                f"""SELECT Article,
                          SUM(Quantite) AS qte,
                          SUM(Total) AS ca
                   FROM Historique
                   WHERE annule = 0
                     AND {_iso_expr('Date_vent')} >= ? 
                     AND {_iso_expr('Date_vent')} <= ?
                   GROUP BY Article
                   ORDER BY ca DESC
                   LIMIT 5""",
                (_to_iso(debut), _to_iso(fin)))

            if not rows:
                empty = QtWidgets.QLabel(
                    "Aucune vente sur la période sélectionnée")
                empty.setAlignment(Qt.AlignCenter)
                empty.setStyleSheet(
                    "color: #94a3b8; font-size: 12px; "
                    "font-style: italic; background: transparent; "
                    "padding: 30px;")
                layout.addWidget(empty)
                return

            max_ca = max(float(r["ca"] or 0) for r in rows) or 1

            for i, r in enumerate(rows, 1):
                part = float(r["ca"] or 0) / max_ca * 100
                card = TopProduitCard(
                    rang=i,
                    nom=r["Article"] or "—",
                    qte=int(r["qte"] or 0),
                    ca=float(r["ca"] or 0),
                    part=part,
                    devise=self.devise)
                layout.addWidget(card)

            layout.addStretch()

        except Exception:
            logger.exception("Erreur top 5")

    # ─── Alertes ───
    def _load_alertes(self):
        layout = self.alertes_layout

        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()

        alerts = []

        # Ruptures
        try:
            seuil_fr = (datetime.now() - timedelta(days=7)
                        ).strftime("%d/%m/%Y %H:%M:%S")
            row = db.query_one(
                f"""SELECT COUNT(*) AS n FROM Historique
                    WHERE annule = 1 
                      AND {_iso_expr('Date_vent')} >= ?""",
                (_to_iso(seuil_fr),))
            n = int(row["n"] or 0) if row else 0
            if n > 0:
                alerts.append((
                    f"{n} produit(s) en rupture de stock", "danger"))
        except Exception:
            pass

        # Ventes annulées
        try:
            seuil = (datetime.now() - timedelta(days=7)
                     ).strftime("%d/%m/%Y %H:%M:%S")
            row = db.query_one(
                """SELECT COUNT(*) AS n FROM Historique
                   WHERE annule = 1 AND Date_vent >= ?""", (seuil,))
            n = int(row["n"] or 0) if row else 0
            if n > 0:
                alerts.append((
                    f"{n} vente(s) annulée(s) cette semaine",
                    "warning"))
        except Exception:
            pass

        # Backup
        try:
            last = db.get_config("backup_last_daily", "")
            if not last:
                alerts.append(("Aucune sauvegarde effectuée",
                               "warning"))
            else:
                dt = datetime.fromisoformat(last)
                jours = (datetime.now() - dt).days
                if jours > 7:
                    alerts.append((
                        f"Sauvegarde ancienne ({jours} jours)",
                        "warning"))
        except Exception:
            pass

        # Badge
        if alerts:
            self.lbl_alertes_count.setText(f"{len(alerts)}")
            self.lbl_alertes_count.setVisible(True)
        else:
            self.lbl_alertes_count.setVisible(False)

        # Affichage
        if not alerts:
            ok = QtWidgets.QLabel(
                "✓  Aucun point d'attention\nTout va bien !")
            ok.setAlignment(Qt.AlignCenter)
            ok.setStyleSheet("""
                color: #15803d; font-size: 12px; font-weight: 700;
                background: #f0fdf4; border: 1px solid #bbf7d0;
                border-radius: 10px; padding: 30px;
            """)
            layout.addWidget(ok)
            layout.addStretch()
            return

        for msg, level in alerts:
            card = AlertCard(msg, level=level)
            layout.addWidget(card)

        layout.addStretch()

    # ─── Bandeau secondaire ───
    def _load_secondary(self, debut, fin):
        # Stock
        try:
            row = db.query_one(
                """SELECT COALESCE(SUM(Quantite * Prix_achat), 0) AS v
                   FROM produits WHERE actif = 1""")
            v = float(row["v"] or 0)
            self.blk_stock_value.setText(_fmt_money(v, self.devise))
        except Exception:
            self.blk_stock_value.setText("—")

        # Marge
        try:
            row = db.query_one(
                f"""SELECT
                     COALESCE(SUM(CASE WHEN annule=0 THEN
                       (h.Total - h.Quantite * COALESCE(p.Prix_achat, 0))
                       ELSE 0 END), 0) AS marge
                   FROM Historique h
                   LEFT JOIN produits p ON p.Nom = h.Article
                   WHERE {_iso_expr('h.Date_vent')} >= ? 
                     AND {_iso_expr('h.Date_vent')} <= ?""",
                (_to_iso(debut), _to_iso(fin)))
            m = float(row["marge"] or 0)
            self.blk_marge_value.setText(_fmt_money(m, self.devise))
        except Exception:
            self.blk_marge_value.setText("—")

        # Annulations
        try:
            row = db.query_one(
                f"""SELECT COUNT(*) AS n FROM Historique
                   WHERE annule = 1
                     AND {_iso_expr('Date_vent')} >= ? 
                     AND {_iso_expr('Date_vent')} <= ?""",
                (_to_iso(debut), _to_iso(fin)))
            n = int(row["n"] or 0) if row else 0
            self.blk_annul_value.setText(str(n))
            if n > 0:
                self.blk_annul_value.setStyleSheet(
                    "color: #DC2626; font-size: 16px; font-weight: 800; "
                    "background: transparent;")
            else:
                self.blk_annul_value.setStyleSheet(
                    "color: #16A34A; font-size: 16px; font-weight: 800; "
                    "background: transparent;")
        except Exception:
            self.blk_annul_value.setText("—")


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()

    w = PageAccueil(user_id="TEST", user_name="Daniel",
                    role="ADMIN", is_owner=True)
    w.resize(1280, 800)
    w.show()
    sys.exit(app.exec())