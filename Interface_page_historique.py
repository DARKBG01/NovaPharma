# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_page_historiquewCYfOA.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_PageHistorique(object):
    def setupUi(self, PageHistorique):
        if not PageHistorique.objectName():
            PageHistorique.setObjectName(u"PageHistorique")
        PageHistorique.resize(1200, 800)
        PageHistorique.setStyleSheet(u"QWidget#PageHistorique { background: #f0f4f8; }\n"
"QWidget#PageHistorique QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(PageHistorique)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 20)
        self.headerRow = QHBoxLayout()
        self.headerRow.setObjectName(u"headerRow")
        self.headerTitleBox = QVBoxLayout()
        self.headerTitleBox.setSpacing(2)
        self.headerTitleBox.setObjectName(u"headerTitleBox")
        self.lbl_title = QLabel(PageHistorique)
        self.lbl_title.setObjectName(u"lbl_title")
        self.lbl_title.setStyleSheet(u"color: #023E8A; font-size: 24px; font-weight: 800; background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_title)

        self.lbl_subtitle = QLabel(PageHistorique)
        self.lbl_subtitle.setObjectName(u"lbl_subtitle")
        self.lbl_subtitle.setStyleSheet(u"color: #64748b; font-size: 12px; background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_subtitle)


        self.headerRow.addLayout(self.headerTitleBox)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerRow.addItem(self.headerSpacer)

        self.lbl_count_badge = QLabel(PageHistorique)
        self.lbl_count_badge.setObjectName(u"lbl_count_badge")
        self.lbl_count_badge.setStyleSheet(u"background: #dbeafe; color: #1e40af; font-size: 11px; font-weight: 800; padding: 8px 14px; border-radius: 12px; letter-spacing: 1px;")

        self.headerRow.addWidget(self.lbl_count_badge)

        self.btn_export_csv = QPushButton(PageHistorique)
        self.btn_export_csv.setObjectName(u"btn_export_csv")
        self.btn_export_csv.setMinimumSize(QSize(0, 44))
        self.btn_export_csv.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_export_csv.setStyleSheet(u"QPushButton { background: #16A34A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 20px; }\n"
"QPushButton:hover { background: #15803d; }")
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/download.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_export_csv.setIcon(icon)
        self.btn_export_csv.setIconSize(QSize(16, 16))

        self.headerRow.addWidget(self.btn_export_csv)


        self.mainLayout.addLayout(self.headerRow)

        self.toolbar = QFrame(PageHistorique)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setMinimumSize(QSize(0, 60))
        self.toolbar.setStyleSheet(u"QFrame#toolbar { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }")
        self.toolbarLayout = QHBoxLayout(self.toolbar)
        self.toolbarLayout.setSpacing(12)
        self.toolbarLayout.setObjectName(u"toolbarLayout")
        self.toolbarLayout.setContentsMargins(16, -1, 16, -1)
        self.inp_search = QLineEdit(self.toolbar)
        self.inp_search.setObjectName(u"inp_search")
        self.inp_search.setMinimumSize(QSize(280, 36))
        self.inp_search.setStyleSheet(u"QLineEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; background: #ffffff; }")

        self.toolbarLayout.addWidget(self.inp_search)

        self.combo_periode = QComboBox(self.toolbar)
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.setObjectName(u"combo_periode")
        self.combo_periode.setMinimumSize(QSize(180, 36))
        self.combo_periode.setStyleSheet(u"QComboBox { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"QComboBox::drop-down { border: none; width: 24px; }\n"
"QComboBox QAbstractItemView { background: #ffffff; color: #0f172a; selection-background-color: #e0f2fe; selection-color: #0f172a; }\n"
"QComboBox::drop-down { border: none; width: 26px; }\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}")

        self.toolbarLayout.addWidget(self.combo_periode)

        self.date_debut = QDateEdit(self.toolbar)
        self.date_debut.setObjectName(u"date_debut")
        self.date_debut.setMinimumSize(QSize(130, 36))
        self.date_debut.setVisible(False)
        self.date_debut.setStyleSheet(u"QDateEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }")
        self.date_debut.setCalendarPopup(True)

        self.toolbarLayout.addWidget(self.date_debut)

        self.lbl_au = QLabel(self.toolbar)
        self.lbl_au.setObjectName(u"lbl_au")
        self.lbl_au.setVisible(False)
        self.lbl_au.setStyleSheet(u"color: #94a3b8; font-size: 12px; background: transparent;")

        self.toolbarLayout.addWidget(self.lbl_au)

        self.date_fin = QDateEdit(self.toolbar)
        self.date_fin.setObjectName(u"date_fin")
        self.date_fin.setMinimumSize(QSize(130, 36))
        self.date_fin.setVisible(False)
        self.date_fin.setStyleSheet(u"QDateEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }")
        self.date_fin.setCalendarPopup(True)

        self.toolbarLayout.addWidget(self.date_fin)

        self.toolbarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbarLayout.addItem(self.toolbarSpacer)

        self.btn_reset = QPushButton(self.toolbar)
        self.btn_reset.setObjectName(u"btn_reset")
        self.btn_reset.setMinimumSize(QSize(0, 36))
        self.btn_reset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_reset.setStyleSheet(u"QPushButton { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 0 14px; }\n"
"QPushButton:hover { background: #e2e8f0; }")

        self.toolbarLayout.addWidget(self.btn_reset)

        self.btn_refresh = QPushButton(self.toolbar)
        self.btn_refresh.setObjectName(u"btn_refresh")
        self.btn_refresh.setMinimumSize(QSize(36, 36))
        self.btn_refresh.setMaximumSize(QSize(36, 36))
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_refresh.setStyleSheet(u"QPushButton { background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px; }\n"
"QPushButton:hover { background: #e2e8f0; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/refresh.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_refresh.setIcon(icon1)
        self.btn_refresh.setIconSize(QSize(16, 16))

        self.toolbarLayout.addWidget(self.btn_refresh)


        self.mainLayout.addWidget(self.toolbar)

        self.tabs = QTabWidget(PageHistorique)
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
        self.tabVentesLayout.setSpacing(12)
        self.tabVentesLayout.setObjectName(u"tabVentesLayout")
        self.tabVentesLayout.setContentsMargins(0, 16, 0, 0)
        self.stats_ventes = QFrame(self.tab_ventes)
        self.stats_ventes.setObjectName(u"stats_ventes")
        self.stats_ventes.setMinimumSize(QSize(0, 80))
        self.stats_ventes.setStyleSheet(u"QFrame#stats_ventes { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }")
        self.statsVentesLayout = QHBoxLayout(self.stats_ventes)
        self.statsVentesLayout.setSpacing(40)
        self.statsVentesLayout.setObjectName(u"statsVentesLayout")
        self.statsVentesLayout.setContentsMargins(20, -1, 20, -1)
        self.statCA = QVBoxLayout()
        self.statCA.setSpacing(2)
        self.statCA.setObjectName(u"statCA")
        self.lbl_ca_titre = QLabel(self.stats_ventes)
        self.lbl_ca_titre.setObjectName(u"lbl_ca_titre")
        self.lbl_ca_titre.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.statCA.addWidget(self.lbl_ca_titre)

        self.lbl_ca_valeur = QLabel(self.stats_ventes)
        self.lbl_ca_valeur.setObjectName(u"lbl_ca_valeur")
        self.lbl_ca_valeur.setStyleSheet(u"color: #023E8A; font-size: 18px; font-weight: 800; background: transparent;")

        self.statCA.addWidget(self.lbl_ca_valeur)


        self.statsVentesLayout.addLayout(self.statCA)

        self.statFact = QVBoxLayout()
        self.statFact.setSpacing(2)
        self.statFact.setObjectName(u"statFact")
        self.lbl_fact_titre = QLabel(self.stats_ventes)
        self.lbl_fact_titre.setObjectName(u"lbl_fact_titre")
        self.lbl_fact_titre.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.statFact.addWidget(self.lbl_fact_titre)

        self.lbl_fact_valeur = QLabel(self.stats_ventes)
        self.lbl_fact_valeur.setObjectName(u"lbl_fact_valeur")
        self.lbl_fact_valeur.setStyleSheet(u"color: #0077B6; font-size: 18px; font-weight: 800; background: transparent;")

        self.statFact.addWidget(self.lbl_fact_valeur)


        self.statsVentesLayout.addLayout(self.statFact)

        self.statArticles = QVBoxLayout()
        self.statArticles.setSpacing(2)
        self.statArticles.setObjectName(u"statArticles")
        self.lbl_articles_titre = QLabel(self.stats_ventes)
        self.lbl_articles_titre.setObjectName(u"lbl_articles_titre")
        self.lbl_articles_titre.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.statArticles.addWidget(self.lbl_articles_titre)

        self.lbl_articles_valeur = QLabel(self.stats_ventes)
        self.lbl_articles_valeur.setObjectName(u"lbl_articles_valeur")
        self.lbl_articles_valeur.setStyleSheet(u"color: #16A34A; font-size: 18px; font-weight: 800; background: transparent;")

        self.statArticles.addWidget(self.lbl_articles_valeur)


        self.statsVentesLayout.addLayout(self.statArticles)

        self.statAnnul = QVBoxLayout()
        self.statAnnul.setSpacing(2)
        self.statAnnul.setObjectName(u"statAnnul")
        self.lbl_annul_titre = QLabel(self.stats_ventes)
        self.lbl_annul_titre.setObjectName(u"lbl_annul_titre")
        self.lbl_annul_titre.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.statAnnul.addWidget(self.lbl_annul_titre)

        self.lbl_annul_valeur = QLabel(self.stats_ventes)
        self.lbl_annul_valeur.setObjectName(u"lbl_annul_valeur")
        self.lbl_annul_valeur.setStyleSheet(u"color: #DC2626; font-size: 18px; font-weight: 800; background: transparent;")

        self.statAnnul.addWidget(self.lbl_annul_valeur)


        self.statsVentesLayout.addLayout(self.statAnnul)


        self.tabVentesLayout.addWidget(self.stats_ventes)

        self.table_ventes = QTableWidget(self.tab_ventes)
        if (self.table_ventes.columnCount() < 9):
            self.table_ventes.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_ventes.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.table_ventes.setObjectName(u"table_ventes")
        self.table_ventes.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table_ventes.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; alternate-background-color: #f8fafc; }\n"
"QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }\n"
"QTableWidget::item:selected { background: #e0f2fe; color: #0f172a; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 10px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_ventes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_ventes.setAlternatingRowColors(True)
        self.table_ventes.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_ventes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_ventes.setShowGrid(False)

        self.tabVentesLayout.addWidget(self.table_ventes)

        self.paginationVentesRow = QHBoxLayout()
        self.paginationVentesRow.setObjectName(u"paginationVentesRow")
        self.lbl_total_ventes = QLabel(self.tab_ventes)
        self.lbl_total_ventes.setObjectName(u"lbl_total_ventes")
        self.lbl_total_ventes.setStyleSheet(u"color: #64748b; font-size: 11px; font-weight: 600; background: transparent;")

        self.paginationVentesRow.addWidget(self.lbl_total_ventes)

        self.paginationVentesSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.paginationVentesRow.addItem(self.paginationVentesSpacer)

        self.btn_prev_v = QPushButton(self.tab_ventes)
        self.btn_prev_v.setObjectName(u"btn_prev_v")
        self.btn_prev_v.setMinimumSize(QSize(90, 34))
        self.btn_prev_v.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_prev_v.setStyleSheet(u"QPushButton { background: #ffffff; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 0 12px; }\n"
"QPushButton:hover { background: #f1f5f9; }\n"
"QPushButton:disabled { color: #cbd5e1; }")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/chevron-left.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_prev_v.setIcon(icon2)
        self.btn_prev_v.setIconSize(QSize(14, 14))

        self.paginationVentesRow.addWidget(self.btn_prev_v)

        self.lbl_page_v = QLabel(self.tab_ventes)
        self.lbl_page_v.setObjectName(u"lbl_page_v")
        self.lbl_page_v.setStyleSheet(u"color: #0f172a; font-size: 11px; font-weight: 700; padding: 0 12px; background: transparent;")

        self.paginationVentesRow.addWidget(self.lbl_page_v)

        self.btn_next_v = QPushButton(self.tab_ventes)
        self.btn_next_v.setObjectName(u"btn_next_v")
        self.btn_next_v.setMinimumSize(QSize(90, 34))
        self.btn_next_v.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_next_v.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.btn_next_v.setStyleSheet(u"QPushButton { background: #ffffff; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 0 12px; }\n"
"QPushButton:hover { background: #f1f5f9; }\n"
"QPushButton:disabled { color: #cbd5e1; }")
        icon3 = QIcon()
        icon3.addFile(u":/Icon/Icons/chevron-right.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_next_v.setIcon(icon3)
        self.btn_next_v.setIconSize(QSize(14, 14))

        self.paginationVentesRow.addWidget(self.btn_next_v)


        self.tabVentesLayout.addLayout(self.paginationVentesRow)

        self.tabs.addTab(self.tab_ventes, "")
        self.tab_commandes = QWidget()
        self.tab_commandes.setObjectName(u"tab_commandes")
        self.tab_commandes.setStyleSheet(u"QWidget#tab_commandes { background: #f0f4f8; }")
        self.tabCommandesLayout = QVBoxLayout(self.tab_commandes)
        self.tabCommandesLayout.setSpacing(12)
        self.tabCommandesLayout.setObjectName(u"tabCommandesLayout")
        self.tabCommandesLayout.setContentsMargins(0, 16, 0, 0)
        self.table_commandes = QTableWidget(self.tab_commandes)
        if (self.table_commandes.columnCount() < 8):
            self.table_commandes.setColumnCount(8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.table_commandes.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.table_commandes.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.table_commandes.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.table_commandes.setHorizontalHeaderItem(3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.table_commandes.setHorizontalHeaderItem(4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.table_commandes.setHorizontalHeaderItem(5, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.table_commandes.setHorizontalHeaderItem(6, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.table_commandes.setHorizontalHeaderItem(7, __qtablewidgetitem16)
        self.table_commandes.setObjectName(u"table_commandes")
        self.table_commandes.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; alternate-background-color: #f8fafc; }\n"
"QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }\n"
"QTableWidget::item:selected { background: #e0f2fe; color: #0f172a; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 10px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_commandes.setAlternatingRowColors(True)
        self.table_commandes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_commandes.setShowGrid(False)

        self.tabCommandesLayout.addWidget(self.table_commandes)

        self.paginationCommandesRow = QHBoxLayout()
        self.paginationCommandesRow.setObjectName(u"paginationCommandesRow")
        self.lbl_total_commandes = QLabel(self.tab_commandes)
        self.lbl_total_commandes.setObjectName(u"lbl_total_commandes")
        self.lbl_total_commandes.setStyleSheet(u"color: #64748b; font-size: 11px; font-weight: 600; background: transparent;")

        self.paginationCommandesRow.addWidget(self.lbl_total_commandes)

        self.paginationCommandesSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.paginationCommandesRow.addItem(self.paginationCommandesSpacer)

        self.btn_prev_c = QPushButton(self.tab_commandes)
        self.btn_prev_c.setObjectName(u"btn_prev_c")
        self.btn_prev_c.setMinimumSize(QSize(90, 34))
        self.btn_prev_c.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_prev_c.setStyleSheet(u"QPushButton { background: #ffffff; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 0 12px; }\n"
"QPushButton:hover { background: #f1f5f9; }\n"
"QPushButton:disabled { color: #cbd5e1; }")
        self.btn_prev_c.setIcon(icon2)
        self.btn_prev_c.setIconSize(QSize(14, 14))

        self.paginationCommandesRow.addWidget(self.btn_prev_c)

        self.lbl_page_c = QLabel(self.tab_commandes)
        self.lbl_page_c.setObjectName(u"lbl_page_c")
        self.lbl_page_c.setStyleSheet(u"color: #0f172a; font-size: 11px; font-weight: 700; padding: 0 12px; background: transparent;")

        self.paginationCommandesRow.addWidget(self.lbl_page_c)

        self.btn_next_c = QPushButton(self.tab_commandes)
        self.btn_next_c.setObjectName(u"btn_next_c")
        self.btn_next_c.setMinimumSize(QSize(90, 34))
        self.btn_next_c.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_next_c.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.btn_next_c.setStyleSheet(u"QPushButton { background: #ffffff; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 0 12px; }\n"
"QPushButton:hover { background: #f1f5f9; }\n"
"QPushButton:disabled { color: #cbd5e1; }")
        self.btn_next_c.setIcon(icon3)
        self.btn_next_c.setIconSize(QSize(14, 14))

        self.paginationCommandesRow.addWidget(self.btn_next_c)


        self.tabCommandesLayout.addLayout(self.paginationCommandesRow)

        self.tabs.addTab(self.tab_commandes, "")

        self.mainLayout.addWidget(self.tabs)


        self.retranslateUi(PageHistorique)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PageHistorique)
    # setupUi

    def retranslateUi(self, PageHistorique):
        self.lbl_title.setText(QCoreApplication.translate("PageHistorique", u"Historique", None))
        self.lbl_subtitle.setText(QCoreApplication.translate("PageHistorique", u"Consultez toutes les transactions et commandes", None))
        self.lbl_count_badge.setText(QCoreApplication.translate("PageHistorique", u"0 entr\u00e9e", None))
        self.btn_export_csv.setText(QCoreApplication.translate("PageHistorique", u"Exporter CSV", None))
        self.inp_search.setPlaceholderText(QCoreApplication.translate("PageHistorique", u"Rechercher par facture, article, client\u2026", None))
        self.combo_periode.setItemText(0, QCoreApplication.translate("PageHistorique", u"Tout", None))
        self.combo_periode.setItemText(1, QCoreApplication.translate("PageHistorique", u"Aujourd'hui", None))
        self.combo_periode.setItemText(2, QCoreApplication.translate("PageHistorique", u"7 derniers jours", None))
        self.combo_periode.setItemText(3, QCoreApplication.translate("PageHistorique", u"30 derniers jours", None))
        self.combo_periode.setItemText(4, QCoreApplication.translate("PageHistorique", u"3 derniers mois", None))
        self.combo_periode.setItemText(5, QCoreApplication.translate("PageHistorique", u"Cette ann\u00e9e", None))
        self.combo_periode.setItemText(6, QCoreApplication.translate("PageHistorique", u"Personnalis\u00e9", None))

        self.date_debut.setDisplayFormat(QCoreApplication.translate("PageHistorique", u"dd/MM/yyyy", None))
        self.lbl_au.setText(QCoreApplication.translate("PageHistorique", u"au", None))
        self.date_fin.setDisplayFormat(QCoreApplication.translate("PageHistorique", u"dd/MM/yyyy", None))
        self.btn_reset.setText(QCoreApplication.translate("PageHistorique", u"R\u00e9initialiser", None))
#if QT_CONFIG(tooltip)
        self.btn_refresh.setToolTip(QCoreApplication.translate("PageHistorique", u"Rafra\u00eechir", None))
#endif // QT_CONFIG(tooltip)
        self.lbl_ca_titre.setText(QCoreApplication.translate("PageHistorique", u"CHIFFRE D'AFFAIRES", None))
        self.lbl_ca_valeur.setText(QCoreApplication.translate("PageHistorique", u"0 FC", None))
        self.lbl_fact_titre.setText(QCoreApplication.translate("PageHistorique", u"FACTURES", None))
        self.lbl_fact_valeur.setText(QCoreApplication.translate("PageHistorique", u"0", None))
        self.lbl_articles_titre.setText(QCoreApplication.translate("PageHistorique", u"ARTICLES VENDUS", None))
        self.lbl_articles_valeur.setText(QCoreApplication.translate("PageHistorique", u"0", None))
        self.lbl_annul_titre.setText(QCoreApplication.translate("PageHistorique", u"ANNUL\u00c9ES", None))
        self.lbl_annul_valeur.setText(QCoreApplication.translate("PageHistorique", u"0", None))
        ___qtablewidgetitem = self.table_ventes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageHistorique", u"N\u00b0 FACTURE", None))
        ___qtablewidgetitem1 = self.table_ventes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageHistorique", u"DATE", None))
        ___qtablewidgetitem2 = self.table_ventes.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageHistorique", u"ARTICLE", None))
        ___qtablewidgetitem3 = self.table_ventes.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageHistorique", u"QT\u00c9", None))
        ___qtablewidgetitem4 = self.table_ventes.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PageHistorique", u"P.U", None))
        ___qtablewidgetitem5 = self.table_ventes.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PageHistorique", u"TOTAL", None))
        ___qtablewidgetitem6 = self.table_ventes.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("PageHistorique", u"CLIENT", None))
        ___qtablewidgetitem7 = self.table_ventes.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("PageHistorique", u"CAISSIER", None))
        ___qtablewidgetitem8 = self.table_ventes.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("PageHistorique", u"STATUT", None))
        self.lbl_total_ventes.setText(QCoreApplication.translate("PageHistorique", u"0 entr\u00e9e", None))
        self.btn_prev_v.setText(QCoreApplication.translate("PageHistorique", u"Pr\u00e9c\u00e9dent", None))
        self.lbl_page_v.setText(QCoreApplication.translate("PageHistorique", u"Page 1 / 1", None))
        self.btn_next_v.setText(QCoreApplication.translate("PageHistorique", u"Suivant", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_ventes), QCoreApplication.translate("PageHistorique", u"Ventes", None))
        ___qtablewidgetitem9 = self.table_commandes.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("PageHistorique", u"N\u00b0 COMMANDE", None))
        ___qtablewidgetitem10 = self.table_commandes.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("PageHistorique", u"DATE", None))
        ___qtablewidgetitem11 = self.table_commandes.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("PageHistorique", u"ARTICLE", None))
        ___qtablewidgetitem12 = self.table_commandes.horizontalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("PageHistorique", u"CAT\u00c9GORIE", None))
        ___qtablewidgetitem13 = self.table_commandes.horizontalHeaderItem(4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("PageHistorique", u"QT\u00c9", None))
        ___qtablewidgetitem14 = self.table_commandes.horizontalHeaderItem(5)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("PageHistorique", u"P.U", None))
        ___qtablewidgetitem15 = self.table_commandes.horizontalHeaderItem(6)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("PageHistorique", u"TOTAL", None))
        ___qtablewidgetitem16 = self.table_commandes.horizontalHeaderItem(7)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("PageHistorique", u"FOURNISSEUR", None))
        self.lbl_total_commandes.setText(QCoreApplication.translate("PageHistorique", u"0 entr\u00e9e", None))
        self.btn_prev_c.setText(QCoreApplication.translate("PageHistorique", u"Pr\u00e9c\u00e9dent", None))
        self.lbl_page_c.setText(QCoreApplication.translate("PageHistorique", u"Page 1 / 1", None))
        self.btn_next_c.setText(QCoreApplication.translate("PageHistorique", u"Suivant", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_commandes), QCoreApplication.translate("PageHistorique", u"Commandes", None))
        pass
    # retranslateUi

