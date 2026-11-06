# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_page_rapportsBXzFOJ.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDateEdit,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QToolButton, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_PageRapports(object):
    def setupUi(self, PageRapports):
        if not PageRapports.objectName():
            PageRapports.setObjectName(u"PageRapports")
        PageRapports.resize(1282, 970)
        PageRapports.setStyleSheet(u"QWidget#PageRapports { background: #f0f4f8; }\n"
"QWidget#PageRapports QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(PageRapports)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(PageRapports)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 88))
        self.header.setMaximumSize(QSize(16777215, 88))
        self.header.setStyleSheet(u"QFrame#header { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #023E8A, stop:1 #0077B6); border: none; }\n"
"QFrame#header QLabel { background: transparent; color: #ffffff; }")
        self.headerLayout = QHBoxLayout(self.header)
        self.headerLayout.setSpacing(16)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(24, -1, 24, -1)
        self.lbl_header_icon = QToolButton(self.header)
        self.lbl_header_icon.setObjectName(u"lbl_header_icon")
        self.lbl_header_icon.setMinimumSize(QSize(44, 44))
        self.lbl_header_icon.setMaximumSize(QSize(44, 44))
        self.lbl_header_icon.setStyleSheet(u"QToolButton { background: rgba(255,255,255,0.15); border-radius: 12px; border: none; padding: 11px; }")
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/chart-line_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.lbl_header_icon.setIcon(icon)
        self.lbl_header_icon.setIconSize(QSize(22, 22))
        self.lbl_header_icon.setAutoRaise(True)

        self.headerLayout.addWidget(self.lbl_header_icon)

        self.headerTitleBox = QVBoxLayout()
        self.headerTitleBox.setSpacing(2)
        self.headerTitleBox.setObjectName(u"headerTitleBox")
        self.lbl_header_title = QLabel(self.header)
        self.lbl_header_title.setObjectName(u"lbl_header_title")
        self.lbl_header_title.setStyleSheet(u"font-size: 18px; font-weight: 800; color: #ffffff; background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_header_title)

        self.lbl_header_sub = QLabel(self.header)
        self.lbl_header_sub.setObjectName(u"lbl_header_sub")
        self.lbl_header_sub.setStyleSheet(u"font-size: 11px; color: rgba(255,255,255,0.75); background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_header_sub)


        self.headerLayout.addLayout(self.headerTitleBox)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.btn_generer = QPushButton(self.header)
        self.btn_generer.setObjectName(u"btn_generer")
        self.btn_generer.setMinimumSize(QSize(0, 40))
        self.btn_generer.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_generer.setStyleSheet(u"QPushButton { background: #16A34A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 20px; }\n"
"QPushButton:hover { background: #15803d; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/refresh_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_generer.setIcon(icon1)
        self.btn_generer.setIconSize(QSize(16, 16))

        self.headerLayout.addWidget(self.btn_generer)


        self.mainLayout.addWidget(self.header)

        self.config_bar = QFrame(PageRapports)
        self.config_bar.setObjectName(u"config_bar")
        self.config_bar.setMinimumSize(QSize(0, 72))
        self.config_bar.setMaximumSize(QSize(16777215, 72))
        self.config_bar.setStyleSheet(u"QFrame#config_bar { background: #ffffff; border-bottom: 1px solid #e2e8f0; }")
        self.configLayout = QHBoxLayout(self.config_bar)
        self.configLayout.setSpacing(12)
        self.configLayout.setObjectName(u"configLayout")
        self.configLayout.setContentsMargins(24, -1, 24, -1)
        self.lbl_periode = QLabel(self.config_bar)
        self.lbl_periode.setObjectName(u"lbl_periode")
        self.lbl_periode.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.configLayout.addWidget(self.lbl_periode)

        self.combo_periode = QComboBox(self.config_bar)
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.setObjectName(u"combo_periode")
        self.combo_periode.setMinimumSize(QSize(200, 36))
        self.combo_periode.setStyleSheet(u"QComboBox { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"QComboBox::drop-down { border: none; width: 24px; }\n"
"QComboBox QAbstractItemView { background: #ffffff; color: #0f172a; selection-background-color: #e0f2fe; selection-color: #0f172a; }")

        self.configLayout.addWidget(self.combo_periode)

        self.date_debut = QDateEdit(self.config_bar)
        self.date_debut.setObjectName(u"date_debut")
        self.date_debut.setMinimumSize(QSize(140, 36))
        self.date_debut.setVisible(False)
        self.date_debut.setStyleSheet(u"QDateEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }")
        self.date_debut.setCalendarPopup(True)

        self.configLayout.addWidget(self.date_debut)

        self.lbl_au = QLabel(self.config_bar)
        self.lbl_au.setObjectName(u"lbl_au")
        self.lbl_au.setVisible(False)
        self.lbl_au.setStyleSheet(u"color: #94a3b8; font-size: 12px; background: transparent;")

        self.configLayout.addWidget(self.lbl_au)

        self.date_fin = QDateEdit(self.config_bar)
        self.date_fin.setObjectName(u"date_fin")
        self.date_fin.setMinimumSize(QSize(140, 36))
        self.date_fin.setVisible(False)
        self.date_fin.setStyleSheet(u"QDateEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }")
        self.date_fin.setCalendarPopup(True)

        self.configLayout.addWidget(self.date_fin)

        self.lbl_topn = QLabel(self.config_bar)
        self.lbl_topn.setObjectName(u"lbl_topn")
        self.lbl_topn.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; padding-left: 12px; background: transparent;")

        self.configLayout.addWidget(self.lbl_topn)

        self.combo_topn = QComboBox(self.config_bar)
        self.combo_topn.addItem("")
        self.combo_topn.addItem("")
        self.combo_topn.addItem("")
        self.combo_topn.addItem("")
        self.combo_topn.addItem("")
        self.combo_topn.setObjectName(u"combo_topn")
        self.combo_topn.setMinimumSize(QSize(80, 36))
        self.combo_topn.setStyleSheet(u"QComboBox { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"QComboBox::drop-down { border: none; width: 24px; }\n"
"QComboBox QAbstractItemView { background: #ffffff; color: #0f172a; selection-background-color: #e0f2fe; selection-color: #0f172a; }")

        self.configLayout.addWidget(self.combo_topn)

        self.configSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.configLayout.addItem(self.configSpacer)

        self.lbl_periode_active = QLabel(self.config_bar)
        self.lbl_periode_active.setObjectName(u"lbl_periode_active")
        self.lbl_periode_active.setStyleSheet(u"color: #0077B6; font-size: 11px; font-weight: 700; background: transparent;")

        self.configLayout.addWidget(self.lbl_periode_active)


        self.mainLayout.addWidget(self.config_bar)

        self.tabs = QTabWidget(PageRapports)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setStyleSheet(u"QTabWidget::pane { background: #f0f4f8; border: none; }\n"
"QTabBar { background: #ffffff; }\n"
"QTabBar::tab { background: #ffffff; color: #64748b; padding: 12px 24px; font-size: 12px; font-weight: 700; border: none; border-bottom: 3px solid transparent; }\n"
"QTabBar::tab:selected { color: #023E8A; border-bottom: 3px solid #023E8A; }\n"
"QTabBar::tab:hover:!selected { color: #0077B6; }")
        self.tab_ventes = QWidget()
        self.tab_ventes.setObjectName(u"tab_ventes")
        self.tab_ventes.setStyleSheet(u"QWidget#tab_ventes { background: #f0f4f8; }")
        self.tabVentesLayout = QVBoxLayout(self.tab_ventes)
        self.tabVentesLayout.setSpacing(16)
        self.tabVentesLayout.setObjectName(u"tabVentesLayout")
        self.tabVentesLayout.setContentsMargins(24, 20, 24, 20)
        self.kpisVentesRow = QHBoxLayout()
        self.kpisVentesRow.setSpacing(12)
        self.kpisVentesRow.setObjectName(u"kpisVentesRow")
        self.kpi_ca = QFrame(self.tab_ventes)
        self.kpi_ca.setObjectName(u"kpi_ca")
        self.kpi_ca.setMinimumSize(QSize(0, 100))
        self.kpi_ca.setStyleSheet(u"QFrame#kpi_ca { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #023E8A; border-radius: 10px; }")
        self.kpi_ca_layout = QVBoxLayout(self.kpi_ca)
        self.kpi_ca_layout.setSpacing(4)
        self.kpi_ca_layout.setObjectName(u"kpi_ca_layout")
        self.kpi_ca_layout.setContentsMargins(16, 12, 16, 12)
        self.kpi_ca_label = QLabel(self.kpi_ca)
        self.kpi_ca_label.setObjectName(u"kpi_ca_label")
        self.kpi_ca_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_ca_layout.addWidget(self.kpi_ca_label)

        self.kpi_ca_value = QLabel(self.kpi_ca)
        self.kpi_ca_value.setObjectName(u"kpi_ca_value")
        self.kpi_ca_value.setStyleSheet(u"color: #023E8A; font-size: 20px; font-weight: 800; background: transparent;")

        self.kpi_ca_layout.addWidget(self.kpi_ca_value)

        self.kpi_ca_var = QLabel(self.kpi_ca)
        self.kpi_ca_var.setObjectName(u"kpi_ca_var")
        self.kpi_ca_var.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 700; background: transparent;")

        self.kpi_ca_layout.addWidget(self.kpi_ca_var)


        self.kpisVentesRow.addWidget(self.kpi_ca)

        self.kpi_ventes = QFrame(self.tab_ventes)
        self.kpi_ventes.setObjectName(u"kpi_ventes")
        self.kpi_ventes.setMinimumSize(QSize(0, 100))
        self.kpi_ventes.setStyleSheet(u"QFrame#kpi_ventes { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #0077B6; border-radius: 10px; }")
        self.kpi_ventes_layout = QVBoxLayout(self.kpi_ventes)
        self.kpi_ventes_layout.setSpacing(4)
        self.kpi_ventes_layout.setObjectName(u"kpi_ventes_layout")
        self.kpi_ventes_layout.setContentsMargins(16, 12, 16, 12)
        self.kpi_ventes_label = QLabel(self.kpi_ventes)
        self.kpi_ventes_label.setObjectName(u"kpi_ventes_label")
        self.kpi_ventes_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_ventes_layout.addWidget(self.kpi_ventes_label)

        self.kpi_ventes_value = QLabel(self.kpi_ventes)
        self.kpi_ventes_value.setObjectName(u"kpi_ventes_value")
        self.kpi_ventes_value.setStyleSheet(u"color: #0077B6; font-size: 20px; font-weight: 800; background: transparent;")

        self.kpi_ventes_layout.addWidget(self.kpi_ventes_value)

        self.kpi_ventes_var = QLabel(self.kpi_ventes)
        self.kpi_ventes_var.setObjectName(u"kpi_ventes_var")
        self.kpi_ventes_var.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 700; background: transparent;")

        self.kpi_ventes_layout.addWidget(self.kpi_ventes_var)


        self.kpisVentesRow.addWidget(self.kpi_ventes)

        self.kpi_panier = QFrame(self.tab_ventes)
        self.kpi_panier.setObjectName(u"kpi_panier")
        self.kpi_panier.setMinimumSize(QSize(0, 100))
        self.kpi_panier.setStyleSheet(u"QFrame#kpi_panier { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #00B4D8; border-radius: 10px; }")
        self.kpi_panier_layout = QVBoxLayout(self.kpi_panier)
        self.kpi_panier_layout.setSpacing(4)
        self.kpi_panier_layout.setObjectName(u"kpi_panier_layout")
        self.kpi_panier_layout.setContentsMargins(16, 12, 16, 12)
        self.kpi_panier_label = QLabel(self.kpi_panier)
        self.kpi_panier_label.setObjectName(u"kpi_panier_label")
        self.kpi_panier_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_panier_layout.addWidget(self.kpi_panier_label)

        self.kpi_panier_value = QLabel(self.kpi_panier)
        self.kpi_panier_value.setObjectName(u"kpi_panier_value")
        self.kpi_panier_value.setStyleSheet(u"color: #00B4D8; font-size: 20px; font-weight: 800; background: transparent;")

        self.kpi_panier_layout.addWidget(self.kpi_panier_value)

        self.kpi_panier_var = QLabel(self.kpi_panier)
        self.kpi_panier_var.setObjectName(u"kpi_panier_var")
        self.kpi_panier_var.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 700; background: transparent;")

        self.kpi_panier_layout.addWidget(self.kpi_panier_var)


        self.kpisVentesRow.addWidget(self.kpi_panier)

        self.kpi_clients = QFrame(self.tab_ventes)
        self.kpi_clients.setObjectName(u"kpi_clients")
        self.kpi_clients.setMinimumSize(QSize(0, 100))
        self.kpi_clients.setStyleSheet(u"QFrame#kpi_clients { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #16A34A; border-radius: 10px; }")
        self.kpi_clients_layout = QVBoxLayout(self.kpi_clients)
        self.kpi_clients_layout.setSpacing(4)
        self.kpi_clients_layout.setObjectName(u"kpi_clients_layout")
        self.kpi_clients_layout.setContentsMargins(16, 12, 16, 12)
        self.kpi_clients_label = QLabel(self.kpi_clients)
        self.kpi_clients_label.setObjectName(u"kpi_clients_label")
        self.kpi_clients_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_clients_layout.addWidget(self.kpi_clients_label)

        self.kpi_clients_value = QLabel(self.kpi_clients)
        self.kpi_clients_value.setObjectName(u"kpi_clients_value")
        self.kpi_clients_value.setStyleSheet(u"color: #16A34A; font-size: 20px; font-weight: 800; background: transparent;")

        self.kpi_clients_layout.addWidget(self.kpi_clients_value)

        self.kpi_clients_var = QLabel(self.kpi_clients)
        self.kpi_clients_var.setObjectName(u"kpi_clients_var")
        self.kpi_clients_var.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 700; background: transparent;")

        self.kpi_clients_layout.addWidget(self.kpi_clients_var)


        self.kpisVentesRow.addWidget(self.kpi_clients)

        self.kpi_articles = QFrame(self.tab_ventes)
        self.kpi_articles.setObjectName(u"kpi_articles")
        self.kpi_articles.setMinimumSize(QSize(0, 100))
        self.kpi_articles.setStyleSheet(u"QFrame#kpi_articles { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #F4A261; border-radius: 10px; }")
        self.kpi_articles_layout = QVBoxLayout(self.kpi_articles)
        self.kpi_articles_layout.setSpacing(4)
        self.kpi_articles_layout.setObjectName(u"kpi_articles_layout")
        self.kpi_articles_layout.setContentsMargins(16, 12, 16, 12)
        self.kpi_articles_label = QLabel(self.kpi_articles)
        self.kpi_articles_label.setObjectName(u"kpi_articles_label")
        self.kpi_articles_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_articles_layout.addWidget(self.kpi_articles_label)

        self.kpi_articles_value = QLabel(self.kpi_articles)
        self.kpi_articles_value.setObjectName(u"kpi_articles_value")
        self.kpi_articles_value.setStyleSheet(u"color: #F4A261; font-size: 20px; font-weight: 800; background: transparent;")

        self.kpi_articles_layout.addWidget(self.kpi_articles_value)

        self.kpi_articles_var = QLabel(self.kpi_articles)
        self.kpi_articles_var.setObjectName(u"kpi_articles_var")
        self.kpi_articles_var.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 700; background: transparent;")

        self.kpi_articles_layout.addWidget(self.kpi_articles_var)


        self.kpisVentesRow.addWidget(self.kpi_articles)


        self.tabVentesLayout.addLayout(self.kpisVentesRow)

        self.chartsRow = QHBoxLayout()
        self.chartsRow.setSpacing(12)
        self.chartsRow.setObjectName(u"chartsRow")
        self.chart_ca = QFrame(self.tab_ventes)
        self.chart_ca.setObjectName(u"chart_ca")
        self.chart_ca.setMinimumSize(QSize(0, 240))
        self.chart_ca.setStyleSheet(u"QFrame#chart_ca { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }")
        self.chart_ca_layout = QVBoxLayout(self.chart_ca)
        self.chart_ca_layout.setObjectName(u"chart_ca_layout")
        self.chart_ca_layout.setContentsMargins(12, 12, 12, 12)
        self.chart_ca_title = QLabel(self.chart_ca)
        self.chart_ca_title.setObjectName(u"chart_ca_title")
        self.chart_ca_title.setStyleSheet(u"color: #023E8A; font-size: 11px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.chart_ca_layout.addWidget(self.chart_ca_title)


        self.chartsRow.addWidget(self.chart_ca)

        self.chart_cat = QFrame(self.tab_ventes)
        self.chart_cat.setObjectName(u"chart_cat")
        self.chart_cat.setMinimumSize(QSize(0, 240))
        self.chart_cat.setMaximumSize(QSize(400, 240))
        self.chart_cat.setStyleSheet(u"QFrame#chart_cat { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }")
        self.chart_cat_layout = QVBoxLayout(self.chart_cat)
        self.chart_cat_layout.setObjectName(u"chart_cat_layout")
        self.chart_cat_layout.setContentsMargins(12, 12, 12, 12)
        self.chart_cat_title = QLabel(self.chart_cat)
        self.chart_cat_title.setObjectName(u"chart_cat_title")
        self.chart_cat_title.setStyleSheet(u"color: #023E8A; font-size: 11px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.chart_cat_layout.addWidget(self.chart_cat_title)


        self.chartsRow.addWidget(self.chart_cat)


        self.tabVentesLayout.addLayout(self.chartsRow)

        self.lbl_top_produits = QLabel(self.tab_ventes)
        self.lbl_top_produits.setObjectName(u"lbl_top_produits")
        self.lbl_top_produits.setStyleSheet(u"color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent;")

        self.tabVentesLayout.addWidget(self.lbl_top_produits)

        self.table_top_produits = QTableWidget(self.tab_ventes)
        if (self.table_top_produits.columnCount() < 5):
            self.table_top_produits.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_top_produits.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_top_produits.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_top_produits.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_top_produits.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_top_produits.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.table_top_produits.setObjectName(u"table_top_produits")
        self.table_top_produits.setMinimumSize(QSize(0, 200))
        self.table_top_produits.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 6px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_top_produits.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_top_produits.setShowGrid(False)

        self.tabVentesLayout.addWidget(self.table_top_produits)

        self.tabs.addTab(self.tab_ventes, "")
        self.tab_equipe = QWidget()
        self.tab_equipe.setObjectName(u"tab_equipe")
        self.tab_equipe.setStyleSheet(u"QWidget#tab_equipe { background: #f0f4f8; }")
        self.tabEquipeLayout = QVBoxLayout(self.tab_equipe)
        self.tabEquipeLayout.setSpacing(16)
        self.tabEquipeLayout.setObjectName(u"tabEquipeLayout")
        self.tabEquipeLayout.setContentsMargins(24, 20, 24, 20)
        self.lbl_vendeurs = QLabel(self.tab_equipe)
        self.lbl_vendeurs.setObjectName(u"lbl_vendeurs")
        self.lbl_vendeurs.setStyleSheet(u"color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent;")

        self.tabEquipeLayout.addWidget(self.lbl_vendeurs)

        self.table_vendeurs = QTableWidget(self.tab_equipe)
        if (self.table_vendeurs.columnCount() < 6):
            self.table_vendeurs.setColumnCount(6)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_vendeurs.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_vendeurs.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_vendeurs.setHorizontalHeaderItem(2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_vendeurs.setHorizontalHeaderItem(3, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.table_vendeurs.setHorizontalHeaderItem(4, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.table_vendeurs.setHorizontalHeaderItem(5, __qtablewidgetitem10)
        self.table_vendeurs.setObjectName(u"table_vendeurs")
        self.table_vendeurs.setMinimumSize(QSize(0, 280))
        self.table_vendeurs.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 6px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_vendeurs.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_vendeurs.setShowGrid(False)

        self.tabEquipeLayout.addWidget(self.table_vendeurs)

        self.lbl_annulations = QLabel(self.tab_equipe)
        self.lbl_annulations.setObjectName(u"lbl_annulations")
        self.lbl_annulations.setStyleSheet(u"color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent;")

        self.tabEquipeLayout.addWidget(self.lbl_annulations)

        self.lbl_alerte_info = QLabel(self.tab_equipe)
        self.lbl_alerte_info.setObjectName(u"lbl_alerte_info")
        self.lbl_alerte_info.setStyleSheet(u"color: #b45309; font-size: 11px; font-weight: 600; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; padding: 8px 12px;")
        self.lbl_alerte_info.setWordWrap(True)

        self.tabEquipeLayout.addWidget(self.lbl_alerte_info)

        self.table_annulations = QTableWidget(self.tab_equipe)
        if (self.table_annulations.columnCount() < 5):
            self.table_annulations.setColumnCount(5)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.table_annulations.setHorizontalHeaderItem(0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.table_annulations.setHorizontalHeaderItem(1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.table_annulations.setHorizontalHeaderItem(2, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.table_annulations.setHorizontalHeaderItem(3, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.table_annulations.setHorizontalHeaderItem(4, __qtablewidgetitem15)
        self.table_annulations.setObjectName(u"table_annulations")
        self.table_annulations.setMinimumSize(QSize(0, 200))
        self.table_annulations.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 6px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_annulations.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_annulations.setShowGrid(False)

        self.tabEquipeLayout.addWidget(self.table_annulations)

        self.tabs.addTab(self.tab_equipe, "")
        self.tab_operations = QWidget()
        self.tab_operations.setObjectName(u"tab_operations")
        self.tab_operations.setStyleSheet(u"QWidget#tab_operations { background: #f0f4f8; }")
        self.tabOperationsLayout = QVBoxLayout(self.tab_operations)
        self.tabOperationsLayout.setSpacing(16)
        self.tabOperationsLayout.setObjectName(u"tabOperationsLayout")
        self.tabOperationsLayout.setContentsMargins(24, 20, 24, 20)
        self.lbl_marges_title = QLabel(self.tab_operations)
        self.lbl_marges_title.setObjectName(u"lbl_marges_title")
        self.lbl_marges_title.setStyleSheet(u"color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent;")

        self.tabOperationsLayout.addWidget(self.lbl_marges_title)

        self.margeKpiRow = QHBoxLayout()
        self.margeKpiRow.setSpacing(12)
        self.margeKpiRow.setObjectName(u"margeKpiRow")
        self.kpi_marge = QFrame(self.tab_operations)
        self.kpi_marge.setObjectName(u"kpi_marge")
        self.kpi_marge.setMinimumSize(QSize(0, 90))
        self.kpi_marge.setStyleSheet(u"QFrame#kpi_marge { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #16A34A; border-radius: 10px; }")
        self.kpi_marge_layout = QVBoxLayout(self.kpi_marge)
        self.kpi_marge_layout.setSpacing(4)
        self.kpi_marge_layout.setObjectName(u"kpi_marge_layout")
        self.kpi_marge_layout.setContentsMargins(16, 10, 16, 10)
        self.kpi_marge_label = QLabel(self.kpi_marge)
        self.kpi_marge_label.setObjectName(u"kpi_marge_label")
        self.kpi_marge_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_marge_layout.addWidget(self.kpi_marge_label)

        self.kpi_marge_value = QLabel(self.kpi_marge)
        self.kpi_marge_value.setObjectName(u"kpi_marge_value")
        self.kpi_marge_value.setStyleSheet(u"color: #16A34A; font-size: 18px; font-weight: 800; background: transparent;")

        self.kpi_marge_layout.addWidget(self.kpi_marge_value)


        self.margeKpiRow.addWidget(self.kpi_marge)

        self.kpi_marge_pct = QFrame(self.tab_operations)
        self.kpi_marge_pct.setObjectName(u"kpi_marge_pct")
        self.kpi_marge_pct.setMinimumSize(QSize(0, 90))
        self.kpi_marge_pct.setStyleSheet(u"QFrame#kpi_marge_pct { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #0077B6; border-radius: 10px; }")
        self.kpi_marge_pct_layout = QVBoxLayout(self.kpi_marge_pct)
        self.kpi_marge_pct_layout.setSpacing(4)
        self.kpi_marge_pct_layout.setObjectName(u"kpi_marge_pct_layout")
        self.kpi_marge_pct_layout.setContentsMargins(16, 10, 16, 10)
        self.kpi_marge_pct_label = QLabel(self.kpi_marge_pct)
        self.kpi_marge_pct_label.setObjectName(u"kpi_marge_pct_label")
        self.kpi_marge_pct_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_marge_pct_layout.addWidget(self.kpi_marge_pct_label)

        self.kpi_marge_pct_value = QLabel(self.kpi_marge_pct)
        self.kpi_marge_pct_value.setObjectName(u"kpi_marge_pct_value")
        self.kpi_marge_pct_value.setStyleSheet(u"color: #0077B6; font-size: 18px; font-weight: 800; background: transparent;")

        self.kpi_marge_pct_layout.addWidget(self.kpi_marge_pct_value)


        self.margeKpiRow.addWidget(self.kpi_marge_pct)

        self.kpi_stock_val = QFrame(self.tab_operations)
        self.kpi_stock_val.setObjectName(u"kpi_stock_val")
        self.kpi_stock_val.setMinimumSize(QSize(0, 90))
        self.kpi_stock_val.setStyleSheet(u"QFrame#kpi_stock_val { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #F4A261; border-radius: 10px; }")
        self.kpi_stock_val_layout = QVBoxLayout(self.kpi_stock_val)
        self.kpi_stock_val_layout.setSpacing(4)
        self.kpi_stock_val_layout.setObjectName(u"kpi_stock_val_layout")
        self.kpi_stock_val_layout.setContentsMargins(16, 10, 16, 10)
        self.kpi_stock_val_label = QLabel(self.kpi_stock_val)
        self.kpi_stock_val_label.setObjectName(u"kpi_stock_val_label")
        self.kpi_stock_val_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_stock_val_layout.addWidget(self.kpi_stock_val_label)

        self.kpi_stock_val_value = QLabel(self.kpi_stock_val)
        self.kpi_stock_val_value.setObjectName(u"kpi_stock_val_value")
        self.kpi_stock_val_value.setStyleSheet(u"color: #F4A261; font-size: 18px; font-weight: 800; background: transparent;")

        self.kpi_stock_val_layout.addWidget(self.kpi_stock_val_value)


        self.margeKpiRow.addWidget(self.kpi_stock_val)

        self.kpi_rupture = QFrame(self.tab_operations)
        self.kpi_rupture.setObjectName(u"kpi_rupture")
        self.kpi_rupture.setMinimumSize(QSize(0, 90))
        self.kpi_rupture.setStyleSheet(u"QFrame#kpi_rupture { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #DC2626; border-radius: 10px; }")
        self.kpi_rupture_layout = QVBoxLayout(self.kpi_rupture)
        self.kpi_rupture_layout.setSpacing(4)
        self.kpi_rupture_layout.setObjectName(u"kpi_rupture_layout")
        self.kpi_rupture_layout.setContentsMargins(16, 10, 16, 10)
        self.kpi_rupture_label = QLabel(self.kpi_rupture)
        self.kpi_rupture_label.setObjectName(u"kpi_rupture_label")
        self.kpi_rupture_label.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.kpi_rupture_layout.addWidget(self.kpi_rupture_label)

        self.kpi_rupture_value = QLabel(self.kpi_rupture)
        self.kpi_rupture_value.setObjectName(u"kpi_rupture_value")
        self.kpi_rupture_value.setStyleSheet(u"color: #DC2626; font-size: 18px; font-weight: 800; background: transparent;")

        self.kpi_rupture_layout.addWidget(self.kpi_rupture_value)


        self.margeKpiRow.addWidget(self.kpi_rupture)


        self.tabOperationsLayout.addLayout(self.margeKpiRow)

        self.lbl_top_marge = QLabel(self.tab_operations)
        self.lbl_top_marge.setObjectName(u"lbl_top_marge")
        self.lbl_top_marge.setStyleSheet(u"color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent;")

        self.tabOperationsLayout.addWidget(self.lbl_top_marge)

        self.table_top_marge = QTableWidget(self.tab_operations)
        if (self.table_top_marge.columnCount() < 6):
            self.table_top_marge.setColumnCount(6)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.table_top_marge.setHorizontalHeaderItem(0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.table_top_marge.setHorizontalHeaderItem(1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.table_top_marge.setHorizontalHeaderItem(2, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.table_top_marge.setHorizontalHeaderItem(3, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.table_top_marge.setHorizontalHeaderItem(4, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.table_top_marge.setHorizontalHeaderItem(5, __qtablewidgetitem21)
        self.table_top_marge.setObjectName(u"table_top_marge")
        self.table_top_marge.setMinimumSize(QSize(0, 180))
        self.table_top_marge.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 6px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_top_marge.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_top_marge.setShowGrid(False)

        self.tabOperationsLayout.addWidget(self.table_top_marge)

        self.lbl_rupture_liste = QLabel(self.tab_operations)
        self.lbl_rupture_liste.setObjectName(u"lbl_rupture_liste")
        self.lbl_rupture_liste.setStyleSheet(u"color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent;")

        self.tabOperationsLayout.addWidget(self.lbl_rupture_liste)

        self.table_rupture = QTableWidget(self.tab_operations)
        if (self.table_rupture.columnCount() < 3):
            self.table_rupture.setColumnCount(3)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.table_rupture.setHorizontalHeaderItem(0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.table_rupture.setHorizontalHeaderItem(1, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.table_rupture.setHorizontalHeaderItem(2, __qtablewidgetitem24)
        self.table_rupture.setObjectName(u"table_rupture")
        self.table_rupture.setMinimumSize(QSize(0, 160))
        self.table_rupture.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 6px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_rupture.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_rupture.setShowGrid(False)

        self.tabOperationsLayout.addWidget(self.table_rupture)

        self.lbl_ops_resume = QLabel(self.tab_operations)
        self.lbl_ops_resume.setObjectName(u"lbl_ops_resume")
        self.lbl_ops_resume.setStyleSheet(u"color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent;")

        self.tabOperationsLayout.addWidget(self.lbl_ops_resume)

        self.lbl_ops_text = QLabel(self.tab_operations)
        self.lbl_ops_text.setObjectName(u"lbl_ops_text")
        self.lbl_ops_text.setStyleSheet(u"color: #0f172a; font-size: 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px;")
        self.lbl_ops_text.setWordWrap(True)

        self.tabOperationsLayout.addWidget(self.lbl_ops_text)

        self.tabs.addTab(self.tab_operations, "")

        self.mainLayout.addWidget(self.tabs)

        self.footer = QFrame(PageRapports)
        self.footer.setObjectName(u"footer")
        self.footer.setMinimumSize(QSize(0, 72))
        self.footer.setMaximumSize(QSize(16777215, 72))
        self.footer.setStyleSheet(u"QFrame#footer { background: #ffffff; border-top: 1px solid #e2e8f0; }")
        self.footerLayout = QHBoxLayout(self.footer)
        self.footerLayout.setSpacing(12)
        self.footerLayout.setObjectName(u"footerLayout")
        self.footerLayout.setContentsMargins(24, -1, 24, -1)
        self.lbl_status = QLabel(self.footer)
        self.lbl_status.setObjectName(u"lbl_status")
        self.lbl_status.setStyleSheet(u"color: #94a3b8; font-size: 11px; font-weight: 600; background: transparent;")

        self.footerLayout.addWidget(self.lbl_status)

        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerLayout.addItem(self.footerSpacer)

        self.btn_export_csv = QPushButton(self.footer)
        self.btn_export_csv.setObjectName(u"btn_export_csv")
        self.btn_export_csv.setMinimumSize(QSize(0, 42))
        self.btn_export_csv.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_export_csv.setStyleSheet(u"QPushButton { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 11px; font-weight: 700; padding: 0 18px; }\n"
"QPushButton:hover { background: #e2e8f0; }")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/download.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_export_csv.setIcon(icon2)
        self.btn_export_csv.setIconSize(QSize(14, 14))

        self.footerLayout.addWidget(self.btn_export_csv)

        self.btn_export_excel = QPushButton(self.footer)
        self.btn_export_excel.setObjectName(u"btn_export_excel")
        self.btn_export_excel.setMinimumSize(QSize(0, 42))
        self.btn_export_excel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_export_excel.setStyleSheet(u"QPushButton { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; border-radius: 10px; font-size: 11px; font-weight: 700; padding: 0 18px; }\n"
"QPushButton:hover { background: #d1fae5; }")
        self.btn_export_excel.setIcon(icon2)
        self.btn_export_excel.setIconSize(QSize(14, 14))

        self.footerLayout.addWidget(self.btn_export_excel)

        self.btn_export_pdf = QPushButton(self.footer)
        self.btn_export_pdf.setObjectName(u"btn_export_pdf")
        self.btn_export_pdf.setMinimumSize(QSize(0, 42))
        self.btn_export_pdf.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_export_pdf.setStyleSheet(u"QPushButton { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 10px; font-size: 11px; font-weight: 700; padding: 0 18px; }\n"
"QPushButton:hover { background: #fee2e2; }")
        self.btn_export_pdf.setIcon(icon2)
        self.btn_export_pdf.setIconSize(QSize(14, 14))

        self.footerLayout.addWidget(self.btn_export_pdf)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(PageRapports)

        QMetaObject.connectSlotsByName(PageRapports)
    # setupUi

    def retranslateUi(self, PageRapports):
        self.lbl_header_title.setText(QCoreApplication.translate("PageRapports", u"Rapports", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("PageRapports", u"Analyse des ventes, de l'\u00e9quipe et des op\u00e9rations", None))
        self.btn_generer.setText(QCoreApplication.translate("PageRapports", u"G\u00e9n\u00e9rer", None))
        self.lbl_periode.setText(QCoreApplication.translate("PageRapports", u"P\u00e9riode", None))
        self.combo_periode.setItemText(0, QCoreApplication.translate("PageRapports", u"Aujourd'hui", None))
        self.combo_periode.setItemText(1, QCoreApplication.translate("PageRapports", u"Cette semaine", None))
        self.combo_periode.setItemText(2, QCoreApplication.translate("PageRapports", u"Ce mois", None))
        self.combo_periode.setItemText(3, QCoreApplication.translate("PageRapports", u"Cette ann\u00e9e", None))
        self.combo_periode.setItemText(4, QCoreApplication.translate("PageRapports", u"30 derniers jours", None))
        self.combo_periode.setItemText(5, QCoreApplication.translate("PageRapports", u"90 derniers jours", None))
        self.combo_periode.setItemText(6, QCoreApplication.translate("PageRapports", u"Personnalis\u00e9", None))

        self.date_debut.setDisplayFormat(QCoreApplication.translate("PageRapports", u"dd/MM/yyyy", None))
        self.lbl_au.setText(QCoreApplication.translate("PageRapports", u"au", None))
        self.date_fin.setDisplayFormat(QCoreApplication.translate("PageRapports", u"dd/MM/yyyy", None))
        self.lbl_topn.setText(QCoreApplication.translate("PageRapports", u"Top N", None))
        self.combo_topn.setItemText(0, QCoreApplication.translate("PageRapports", u"5", None))
        self.combo_topn.setItemText(1, QCoreApplication.translate("PageRapports", u"10", None))
        self.combo_topn.setItemText(2, QCoreApplication.translate("PageRapports", u"15", None))
        self.combo_topn.setItemText(3, QCoreApplication.translate("PageRapports", u"20", None))
        self.combo_topn.setItemText(4, QCoreApplication.translate("PageRapports", u"50", None))

        self.lbl_periode_active.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_ca_label.setText(QCoreApplication.translate("PageRapports", u"CA TOTAL", None))
        self.kpi_ca_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_ca_var.setText("")
        self.kpi_ventes_label.setText(QCoreApplication.translate("PageRapports", u"NOMBRE DE VENTES", None))
        self.kpi_ventes_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_ventes_var.setText("")
        self.kpi_panier_label.setText(QCoreApplication.translate("PageRapports", u"PANIER MOYEN", None))
        self.kpi_panier_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_panier_var.setText("")
        self.kpi_clients_label.setText(QCoreApplication.translate("PageRapports", u"CLIENTS SERVIS", None))
        self.kpi_clients_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_clients_var.setText("")
        self.kpi_articles_label.setText(QCoreApplication.translate("PageRapports", u"ARTICLES VENDUS", None))
        self.kpi_articles_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_articles_var.setText("")
        self.chart_ca_title.setText(QCoreApplication.translate("PageRapports", u"\u00c9VOLUTION DU CHIFFRE D'AFFAIRES", None))
        self.chart_cat_title.setText(QCoreApplication.translate("PageRapports", u"R\u00c9PARTITION PAR CAT\u00c9GORIE", None))
        self.lbl_top_produits.setText(QCoreApplication.translate("PageRapports", u"TOP PRODUITS", None))
        ___qtablewidgetitem = self.table_top_produits.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageRapports", u"PRODUIT", None))
        ___qtablewidgetitem1 = self.table_top_produits.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageRapports", u"CAT\u00c9GORIE", None))
        ___qtablewidgetitem2 = self.table_top_produits.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageRapports", u"QT\u00c9", None))
        ___qtablewidgetitem3 = self.table_top_produits.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageRapports", u"CA", None))
        ___qtablewidgetitem4 = self.table_top_produits.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PageRapports", u"PART", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_ventes), QCoreApplication.translate("PageRapports", u"Ventes", None))
        self.lbl_vendeurs.setText(QCoreApplication.translate("PageRapports", u"PERFORMANCE DES VENDEURS", None))
        ___qtablewidgetitem5 = self.table_vendeurs.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PageRapports", u"VENDEUR", None))
        ___qtablewidgetitem6 = self.table_vendeurs.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("PageRapports", u"VENTES", None))
        ___qtablewidgetitem7 = self.table_vendeurs.horizontalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("PageRapports", u"CA", None))
        ___qtablewidgetitem8 = self.table_vendeurs.horizontalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("PageRapports", u"PANIER MOYEN", None))
        ___qtablewidgetitem9 = self.table_vendeurs.horizontalHeaderItem(4)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("PageRapports", u"CLIENTS SERVIS", None))
        ___qtablewidgetitem10 = self.table_vendeurs.horizontalHeaderItem(5)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("PageRapports", u"PART", None))
        self.lbl_annulations.setText(QCoreApplication.translate("PageRapports", u"TAUX D'ANNULATION PAR CAISSIER", None))
        self.lbl_alerte_info.setText(QCoreApplication.translate("PageRapports", u"Toute ligne avec un taux sup\u00e9rieur \u00e0 5 % est signal\u00e9e en rouge.", None))
        ___qtablewidgetitem11 = self.table_annulations.horizontalHeaderItem(0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("PageRapports", u"CAISSIER", None))
        ___qtablewidgetitem12 = self.table_annulations.horizontalHeaderItem(1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("PageRapports", u"TRANSACTIONS", None))
        ___qtablewidgetitem13 = self.table_annulations.horizontalHeaderItem(2)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("PageRapports", u"ANNULATIONS", None))
        ___qtablewidgetitem14 = self.table_annulations.horizontalHeaderItem(3)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("PageRapports", u"TAUX", None))
        ___qtablewidgetitem15 = self.table_annulations.horizontalHeaderItem(4)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("PageRapports", u"ALERTE", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_equipe), QCoreApplication.translate("PageRapports", u"\u00c9quipe", None))
        self.lbl_marges_title.setText(QCoreApplication.translate("PageRapports", u"MARGES", None))
        self.kpi_marge_label.setText(QCoreApplication.translate("PageRapports", u"MARGE GLOBALE", None))
        self.kpi_marge_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_marge_pct_label.setText(QCoreApplication.translate("PageRapports", u"TAUX DE MARGE MOYEN", None))
        self.kpi_marge_pct_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_stock_val_label.setText(QCoreApplication.translate("PageRapports", u"VALEUR DU STOCK", None))
        self.kpi_stock_val_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.kpi_rupture_label.setText(QCoreApplication.translate("PageRapports", u"PRODUITS EN RUPTURE", None))
        self.kpi_rupture_value.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.lbl_top_marge.setText(QCoreApplication.translate("PageRapports", u"TOP PRODUITS PAR MARGE", None))
        ___qtablewidgetitem16 = self.table_top_marge.horizontalHeaderItem(0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("PageRapports", u"PRODUIT", None))
        ___qtablewidgetitem17 = self.table_top_marge.horizontalHeaderItem(1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("PageRapports", u"QT\u00c9", None))
        ___qtablewidgetitem18 = self.table_top_marge.horizontalHeaderItem(2)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("PageRapports", u"CA", None))
        ___qtablewidgetitem19 = self.table_top_marge.horizontalHeaderItem(3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("PageRapports", u"CO\u00dbT", None))
        ___qtablewidgetitem20 = self.table_top_marge.horizontalHeaderItem(4)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("PageRapports", u"MARGE", None))
        ___qtablewidgetitem21 = self.table_top_marge.horizontalHeaderItem(5)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("PageRapports", u"TAUX", None))
        self.lbl_rupture_liste.setText(QCoreApplication.translate("PageRapports", u"PRODUITS EN STOCK FAIBLE", None))
        ___qtablewidgetitem22 = self.table_rupture.horizontalHeaderItem(0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("PageRapports", u"CODE", None))
        ___qtablewidgetitem23 = self.table_rupture.horizontalHeaderItem(1)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("PageRapports", u"PRODUIT", None))
        ___qtablewidgetitem24 = self.table_rupture.horizontalHeaderItem(2)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("PageRapports", u"STOCK ACTUEL", None))
        self.lbl_ops_resume.setText(QCoreApplication.translate("PageRapports", u"ACTIVIT\u00c9 OP\u00c9RATIONNELLE", None))
        self.lbl_ops_text.setText(QCoreApplication.translate("PageRapports", u"\u2014", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_operations), QCoreApplication.translate("PageRapports", u"Op\u00e9rations", None))
        self.lbl_status.setText(QCoreApplication.translate("PageRapports", u"Pr\u00eat", None))
        self.btn_export_csv.setText(QCoreApplication.translate("PageRapports", u"CSV", None))
        self.btn_export_excel.setText(QCoreApplication.translate("PageRapports", u"Excel", None))
        self.btn_export_pdf.setText(QCoreApplication.translate("PageRapports", u"PDF", None))
        pass
    # retranslateUi

