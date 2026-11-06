#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rapport_engine.py — Moteur de calcul des rapports.
====================================================
- Résolution des périodes (jour/hebdo/mois/année/custom)
- Comparaison N-1 automatique
- KPIs : CA, ventes, panier, clients, articles
- Données pour graphiques et tableaux
"""

import logging
from datetime import datetime, timedelta

from Database import db

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════
# Résolution des périodes
# ══════════════════════════════════════════════════════════════════
PERIODES = ["Aujourd'hui", "Cette semaine", "Ce mois", "Cette année",
            "30 derniers jours", "90 derniers jours", "Personnalisé"]


def resolve_period(label: str, custom_start=None, custom_end=None):
    """
    Retourne (debut_str, fin_str, debut_n1_str, fin_n1_str) au format
    'YYYY-MM-DD HH:MM:SS'. N-1 = même période l'année précédente.
    """
    today = datetime.now().replace(hour=23, minute=59, second=59)

    if label == "Aujourd'hui":
        debut = today.replace(hour=0, minute=0, second=0)
        fin = today
    elif label == "Cette semaine":
        debut = today - timedelta(days=today.weekday())
        debut = debut.replace(hour=0, minute=0, second=0)
        fin = today
    elif label == "Ce mois":
        debut = today.replace(day=1, hour=0, minute=0, second=0)
        fin = today
    elif label == "Cette année":
        debut = today.replace(month=1, day=1, hour=0, minute=0, second=0)
        fin = today
    elif label == "30 derniers jours":
        debut = (today - timedelta(days=30)).replace(
            hour=0, minute=0, second=0)
        fin = today
    elif label == "90 derniers jours":
        debut = (today - timedelta(days=90)).replace(
            hour=0, minute=0, second=0)
        fin = today
    elif label == "Personnalisé" and custom_start and custom_end:
        debut = custom_start.replace(hour=0, minute=0, second=0)
        fin = custom_end.replace(hour=23, minute=59, second=59)
    else:
        # fallback : mois courant
        debut = today.replace(day=1, hour=0, minute=0, second=0)
        fin = today

    # N-1 : même période un an avant
    try:
        debut_n1 = debut.replace(year=debut.year - 1)
        fin_n1 = fin.replace(year=fin.year - 1)
    except ValueError:
        # 29 février → 28
        debut_n1 = debut.replace(year=debut.year - 1, day=28)
        fin_n1 = fin.replace(year=fin.year - 1, day=28)

        # ⚠️ Historique.Date_vent est stocké au format DD/MM/YYYY HH:MM:SS
    fmt = "%d/%m/%Y %H:%M:%S"
    return (debut.strftime(fmt), fin.strftime(fmt),
            debut_n1.strftime(fmt), fin_n1.strftime(fmt))


# ══════════════════════════════════════════════════════════════════
# Helpers dates — Historique stocke en "DD/MM/YYYY HH:MM:SS"
# ══════════════════════════════════════════════════════════════════
def _to_iso(fr_date: str) -> str:
    """Convertit 'DD/MM/YYYY HH:MM:SS' → 'YYYY-MM-DD HH:MM:SS'."""
    try:
        d, rest = fr_date.split(" ", 1)
        day, month, year = d.split("/")
        return f"{year}-{month}-{day} {rest}"
    except Exception:
        return fr_date


def _iso_expr(col: str) -> str:
    """Expression SQL qui convertit une colonne FR en ISO."""
    return (
        f"(substr({col}, 7, 4) || '-' || "
        f"substr({col}, 4, 2) || '-' || "
        f"substr({col}, 1, 2) || "
        f"substr({col}, 11))"
    )

# ══════════════════════════════════════════════════════════════════
# KPIs génériques
# ══════════════════════════════════════════════════════════════════
def compute_kpis(debut, fin):
    """
    KPIs pour la période [debut, fin] sur Historique.
    Retourne un dict :
      ca_total, nb_ventes, panier_moyen,
      nb_clients, nb_articles
    """
    try:
        debut_iso = _to_iso(debut)
        fin_iso = _to_iso(fin)
        date_iso = _iso_expr("Date_vent")

        row = db.query_one(
            f"""SELECT
                 COALESCE(SUM(Total), 0) AS ca,
                 COUNT(DISTINCT Num_fact) AS n_ventes,
                 SUM(Quantite) AS n_articles,
                 COUNT(DISTINCT Client_name) AS n_clients
               FROM Historique
               WHERE {date_iso} >= ? AND {date_iso} <= ?
                 AND COALESCE(annule, 0) = 0""",
            (debut_iso, fin_iso))
        if not row:
            return _empty_kpis()

        ca = float(row["ca"] or 0)
        n_ventes = int(row["n_ventes"] or 0)
        n_articles = int(row["n_articles"] or 0)
        n_clients = int(row["n_clients"] or 0)
        panier = (ca / n_ventes) if n_ventes else 0

        return {
            "ca_total": ca,
            "nb_ventes": n_ventes,
            "panier_moyen": panier,
            "nb_clients": n_clients,
            "nb_articles": n_articles,
        }
    except Exception:
        logger.exception("Erreur compute_kpis")
        return _empty_kpis()


def _empty_kpis():
    return {"ca_total": 0, "nb_ventes": 0, "panier_moyen": 0,
            "nb_clients": 0, "nb_articles": 0}


def compare_n1(kpi_current, kpi_n1):
    """Retourne un dict de % de variation (None si N-1 = 0)."""
    out = {}
    for k in ("ca_total", "nb_ventes", "panier_moyen",
              "nb_clients", "nb_articles"):
        prev = kpi_n1.get(k, 0)
        cur = kpi_current.get(k, 0)
        out[k] = ((cur - prev) / prev * 100) if prev else None
    return out


# ══════════════════════════════════════════════════════════════════
# Série temporelle (évolution CA)
# ══════════════════════════════════════════════════════════════════
def serie_ca_journalier(debut, fin):
    """Retourne [(date_str, ca_float), ...] agrégé par jour."""
    try:
        debut_iso = _to_iso(debut)
        fin_iso = _to_iso(fin)
        date_iso = _iso_expr("Date_vent")

        rows = db.query(
            f"""SELECT substr(Date_vent, 1, 10) AS jour,
                      SUM(Total) AS ca
               FROM Historique
               WHERE {date_iso} >= ? AND {date_iso} <= ?
                 AND COALESCE(annule, 0) = 0
               GROUP BY jour ORDER BY jour ASC""",
            (debut_iso, fin_iso))
        # Trie par date réelle (DD/MM/YYYY)
        def _parse_jour(s):
            try:
                d, m, y = s.split("/")
                return (int(y), int(m), int(d))
            except Exception:
                return (0, 0, 0)
        result = [(r["jour"], float(r["ca"] or 0)) for r in rows]
        result.sort(key=lambda x: _parse_jour(x[0]))
        return result
    except Exception:
        logger.exception("Erreur serie_ca")
        return []


# ══════════════════════════════════════════════════════════════════
# Top N produits / catégories
# ══════════════════════════════════════════════════════════════════
def top_produits(debut, fin, n=10):
    try:
        debut_iso = _to_iso(debut)
        fin_iso = _to_iso(fin)
        date_iso = _iso_expr("h.Date_vent")

        rows = db.query(
            f"""SELECT h.Article AS nom,
                      SUM(h.Quantite) AS qte,
                      SUM(h.Total) AS ca,
                      COALESCE(p.Categorie, '—') AS categorie
               FROM Historique h
               LEFT JOIN produits p ON p.Nom = h.Article
               WHERE {date_iso} >= ? AND {date_iso} <= ?
                 AND COALESCE(h.annule, 0) = 0
               GROUP BY h.Article
               ORDER BY ca DESC LIMIT ?""",
            (debut_iso, fin_iso, n))
        return [dict(r) for r in rows]
    except Exception:
        logger.exception("Erreur top_produits")
        return []


def repartition_categories(debut, fin):
    try:
        debut_iso = _to_iso(debut)
        fin_iso = _to_iso(fin)
        date_iso = _iso_expr("h.Date_vent")

        rows = db.query(
            f"""SELECT COALESCE(p.Categorie, '—') AS cat,
                      SUM(h.Total) AS ca
               FROM Historique h
               LEFT JOIN produits p ON p.Nom = h.Article
               WHERE {date_iso} >= ? AND {date_iso} <= ?
                 AND COALESCE(h.annule, 0) = 0
               GROUP BY cat ORDER BY ca DESC""",
            (debut_iso, fin_iso))
        return [dict(r) for r in rows]
    except Exception:
        logger.exception("Erreur repartition_categories")
        return []


# ══════════════════════════════════════════════════════════════════
# Rapport Équipe
# ══════════════════════════════════════════════════════════════════
def equipe_vendeurs(debut, fin):
    """Agrégation par utilisateur ayant vendu."""
    try:
        debut_iso = _to_iso(debut)
        fin_iso = _to_iso(fin)
        date_iso = _iso_expr("h.Date_vent")

        rows = db.query(
            f"""SELECT COALESCE(h.utilisateur_id, 'inconnu') AS uid,
                      SUM(h.Total) AS ca,
                      COUNT(DISTINCT h.Num_fact) AS n_ventes,
                      SUM(h.Quantite) AS n_articles,
                      COUNT(DISTINCT h.Client_name) AS n_clients
               FROM Historique h
               WHERE {date_iso} >= ? AND {date_iso} <= ?
                 AND COALESCE(h.annule, 0) = 0
               GROUP BY uid ORDER BY ca DESC""",
            (debut_iso, fin_iso))
        out = []
        for r in rows:
            uid = r["uid"]
            name = "Inconnu"
            if uid and uid != "inconnu":
                u = db.query_one(
                    "SELECT prenom, nom FROM Utilisateur WHERE id = ? LIMIT 1",
                    (uid,))
                if u:
                    name = f"{u['prenom'] or ''} {u['nom'] or ''}".strip()
            out.append({
                "uid": uid, "nom": name,
                "ca": float(r["ca"] or 0),
                "n_ventes": int(r["n_ventes"] or 0),
                "n_articles": int(r["n_articles"] or 0),
                "n_clients": int(r["n_clients"] or 0),
                "panier": (float(r["ca"] or 0) / int(r["n_ventes"] or 1)),
            })
        total = sum(x["ca"] for x in out) or 1
        for x in out:
            x["part"] = x["ca"] / total * 100
        return out
    except Exception:
        logger.exception("Erreur equipe_vendeurs")
        return []


def equipe_annulations(debut, fin):
    """Taux d'annulation par utilisateur."""
    try:
        debut_iso = _to_iso(debut)
        fin_iso = _to_iso(fin)
        date_iso = _iso_expr("Date_vent")

        rows = db.query(
            f"""SELECT COALESCE(utilisateur_id, 'inconnu') AS uid,
                      SUM(CASE WHEN annule = 1 THEN 1 ELSE 0 END) AS n_annul,
                      COUNT(*) AS n_total
               FROM Historique
               WHERE {date_iso} >= ? AND {date_iso} <= ?
               GROUP BY uid""",
            (debut_iso, fin_iso))
        out = []
        for r in rows:
            n_total = int(r["n_total"] or 0)
            n_annul = int(r["n_annul"] or 0)
            taux = (n_annul / n_total * 100) if n_total else 0
            uid = r["uid"]
            name = "Inconnu"
            if uid and uid != "inconnu":
                u = db.query_one(
                    "SELECT prenom, nom FROM Utilisateur WHERE id = ? LIMIT 1",
                    (uid,))
                if u:
                    name = f"{u['prenom'] or ''} {u['nom'] or ''}".strip()
            out.append({
                "uid": uid, "nom": name,
                "n_annul": n_annul, "n_total": n_total, "taux": taux,
                # ─── Alerte seulement si volume suffisant ───
                "alerte": (taux > 5 and n_total >= 20),
                # ─── Permet d'ignorer manuellement ───
                "ignorer": False,
            })
        return sorted(out, key=lambda x: -x["taux"])
    except Exception:
        logger.exception("Erreur equipe_annulations")
        return []


# ══════════════════════════════════════════════════════════════════
# Rapport Opérations
# ══════════════════════════════════════════════════════════════════
def marges(debut, fin):
    """Marge globale + top/bottom produits."""
    try:
        debut_iso = _to_iso(debut)
        fin_iso = _to_iso(fin)
        date_iso = _iso_expr("h.Date_vent")

        rows = db.query(
            f"""SELECT h.Article AS nom,
                      SUM(h.Quantite) AS qte,
                      SUM(h.Total) AS ca,
                      COALESCE(p.Prix_achat, 0) AS pa
               FROM Historique h
               LEFT JOIN produits p ON p.Nom = h.Article
               WHERE {date_iso} >= ? AND {date_iso} <= ?
                 AND COALESCE(h.annule, 0) = 0
               GROUP BY h.Article ORDER BY ca DESC""",
            (debut_iso, fin_iso))
        items = []
        for r in rows:
            qte = float(r["qte"] or 0)
            ca = float(r["ca"] or 0)
            pa = float(r["pa"] or 0)
            cout = pa * qte
            marge = ca - cout
            marge_pct = (marge / ca * 100) if ca else 0
            # ─── Marge % = marge / CA (pas marge / prix unitaire) ───
            items.append({
                "nom": r["nom"], "qte": qte, "ca": ca,
                "cout": cout, "marge": marge,
                "marge_pct": round(marge_pct, 2),
                # ─── Taux de marque = marge / CA ───
                "taux_marque": round(
                    (marge / ca * 100) if ca else 0, 2),
            })
        return items
    except Exception:
        logger.exception("Erreur marges")
        return []


def stock_et_blf(debut, fin):
    """État du stock + BLF de la période."""
    out = {}
    try:
        row = db.query_one(
            """SELECT COUNT(*) AS n_prod,
                      COALESCE(SUM(Quantite), 0) AS total_qte,
                      COALESCE(SUM(Quantite * Prix_achat), 0) AS valeur
               FROM produits WHERE actif = 1""")
        out["stock"] = dict(row) if row else {}

        row = db.query_one(
            """SELECT COUNT(*) AS n_rupture FROM produits
               WHERE actif = 1 AND Quantite <= 5""")
        out["rupture"] = int(row["n_rupture"] or 0) if row else 0

        debut_sql = _fr_to_sql(debut)
        fin_sql = _fr_to_sql(fin)
        rows = db.query(
            """SELECT statut, COUNT(*) AS n, SUM(total_achat) AS ca
               FROM BonLivraison
               WHERE date_livraison >= ? AND date_livraison <= ?
               GROUP BY statut""",
            (debut_sql, fin_sql))
        out["blf"] = [dict(r) for r in rows]

        rows = db.query(
            """SELECT p.Code_reference, p.Nom, p.Quantite
               FROM produits p WHERE p.actif = 1
               ORDER BY p.Quantite ASC LIMIT 10""")
        out["low_stock"] = [dict(r) for r in rows]
    except Exception:
        logger.exception("Erreur stock_et_blf")
    return out


def clients_stats(debut, fin):
    """Clients : nouveaux, fidèles, top, inactifs, ratio anon."""
    out = {}
    try:
        row = db.query_one(
            """SELECT COUNT(*) AS n FROM Client
               WHERE actif = 1
                 AND created_at >= ? AND created_at <= ?""",
            (debut, fin))
        out["nouveaux"] = int(row["n"] or 0) if row else 0

        rows = db.query(
            """SELECT COALESCE(C_name, nom) AS nom, Montant_total AS ca
               FROM Client WHERE actif = 1
               ORDER BY Montant_total DESC LIMIT 10""")
        out["top_clients"] = [dict(r) for r in rows]

        row = db.query_one(
            """SELECT
                 SUM(CASE WHEN numero LIKE 'ANON-%' THEN 1 ELSE 0 END) AS anon,
                 COUNT(*) AS total
               FROM Client WHERE actif = 1""")
        total = int(row["total"] or 0) if row else 0
        anon = int(row["anon"] or 0) if row else 0
        out["ratio_anon"] = (anon / total * 100) if total else 0
    except Exception:
        logger.exception("Erreur clients_stats")
    return out


def operations_resume(debut, fin):
    """Annulations ventes + ajustements stock + BLF annulés."""
    out = {}
    try:
        # Historique : format français
        debut_iso = _to_iso(debut)
        fin_iso = _to_iso(fin)
        date_iso = _iso_expr("Date_vent")

        row = db.query_one(
            f"""SELECT COUNT(*) AS n FROM Historique
               WHERE annule = 1 AND {date_iso} >= ? AND {date_iso} <= ?""",
            (debut_iso, fin_iso))
        out["ventes_annulees"] = int(row["n"] or 0) if row else 0

        # AjustementStock : format SQL → convertit
        debut_sql = _fr_to_sql(debut)
        fin_sql = _fr_to_sql(fin)

        row = db.query_one(
            """SELECT COUNT(*) AS n, COALESCE(SUM(ABS(difference)), 0) AS qte
               FROM AjustementStock
               WHERE date_ajustement >= ? AND date_ajustement <= ?""",
            (debut_sql, fin_sql))
        out["ajustements"] = dict(row) if row else {}

        row = db.query_one(
            """SELECT COUNT(*) AS n FROM BonLivraison
               WHERE statut = 'ANNULEE'
                 AND cancelled_at >= ? AND cancelled_at <= ?""",
            (debut_sql, fin_sql))
        out["blf_annules"] = int(row["n"] or 0) if row else 0
    except Exception:
        logger.exception("Erreur operations_resume")
    return out


def _fr_to_sql(fr_date):
    """Convertit DD/MM/YYYY HH:MM:SS → YYYY-MM-DD HH:MM:SS."""
    try:
        d, rest = fr_date.split(" ", 1)
        day, month, year = d.split("/")
        return f"{year}-{month}-{day} {rest}"
    except Exception:
        return fr_date