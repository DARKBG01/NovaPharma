#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setting_all_charts.py — Affiche tous les graphiques Nova Pharma.
=================================================================
Ouvert depuis le bouton "Voir tous les graphiques" du dashboard.
"""

import logging

from PySide6 import QtWidgets, QtCore

from Interface_all_charts import Ui_Dialog
from Charts import (
    ChartCard,
    chart_revenue_line, chart_revenue_monthly, chart_revenue_hourly,
    chart_sales_count_line, chart_top_products, chart_categories_donut,
    chart_top_clients, chart_new_clients, chart_anonyme_split,
    chart_low_stock, chart_year_comparison,
)

logger = logging.getLogger(__name__)


class Setting_all_charts(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.btn_close.clicked.connect(self.accept)

        self._install_charts()

    # ══════════════════════════════════════════════════════════════
    def _install_charts(self):
        layout = self.charts_layout

        # ("pair", ...) = 2 par ligne  |  ("wide", ...) = pleine largeur
        definitions = [
            ("pair", "Revenus 7 derniers jours", "CA quotidien",
             lambda: chart_revenue_line(7)),
            ("pair", "Anonymes vs identifiés", "Répartition des factures",
             chart_anonyme_split),

            ("wide", "Chiffre d'affaires mensuel", "12 derniers mois",
             lambda: chart_revenue_monthly(12)),

            ("pair", "Top 10 médicaments", "Par quantité vendue",
             lambda: chart_top_products("quantity", 10)),
            ("pair", "Répartition par catégorie", "CA par catégorie",
             chart_categories_donut),

            ("wide", "Comparaison annuelle",
             "Année courante vs année précédente",
             chart_year_comparison),

            ("pair", "Activité horaire", "CA par heure",
             chart_revenue_hourly),
            ("pair", "Ventes quotidiennes", "30 derniers jours",
             lambda: chart_sales_count_line(30)),

            ("pair", "Top 10 clients", "CA cumulé",
             lambda: chart_top_clients(10)),
            ("pair", "Nouveaux clients", "6 derniers mois",
             lambda: chart_new_clients(6)),

            ("wide", "Produits en rupture", "Stock ≤ 20 unités",
             lambda: chart_low_stock(10)),
        ]

        i = 0
        while i < len(definitions):
            typ, title, sub, fn = definitions[i]

            if typ == "wide":
                card = self._make_card(title, sub, fn)
                card.setMinimumHeight(300)
                layout.addWidget(card)
                i += 1
            else:
                row = QtWidgets.QHBoxLayout()
                row.setSpacing(16)

                card1 = self._make_card(title, sub, fn)
                card1.setMinimumHeight(300)
                row.addWidget(card1, 1)

                # Regarde si le suivant est aussi un "pair"
                if i + 1 < len(definitions):
                    nt, nt_title, nt_sub, nt_fn = definitions[i + 1]
                    if nt == "pair":
                        card2 = self._make_card(nt_title, nt_sub, nt_fn)
                        card2.setMinimumHeight(300)
                        row.addWidget(card2, 1)
                        i += 2
                    else:
                        i += 1
                else:
                    i += 1

                layout.addLayout(row)

        layout.addStretch()

    def _make_card(self, title, sub, fn) -> ChartCard:
        card = ChartCard(title, sub)
        chart = fn()
        if chart.series():
            card.set_chart(chart)
        else:
            card.set_empty()
        return card


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    from Database import db
    app = QtWidgets.QApplication(sys.argv)
    db.get_conn()

    dlg = Setting_all_charts()
    sys.exit(dlg.exec())