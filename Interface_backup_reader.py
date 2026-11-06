# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_backup_readerLaIlSU.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(860, 640)
        Dialog.setMinimumSize(QSize(720, 520))
        Dialog.setStyleSheet(u"QDialog#Dialog { background: #f0f4f8; }\n"
"QDialog#Dialog QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(Dialog)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(Dialog)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 88))
        self.header.setMaximumSize(QSize(16777215, 88))
        self.header.setStyleSheet(u"QFrame#header { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #64748b, stop:1 #475569); border: none; }\n"
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
        icon.addFile(u":/Icon/Icons/lock_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        self.lbl_header_sub.setStyleSheet(u"font-size: 11px; color: rgba(255,255,255,0.85); background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_header_sub)


        self.headerLayout.addLayout(self.headerTitleBox)


        self.mainLayout.addWidget(self.header)

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.setSpacing(14)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(24, 20, 24, 20)
        self.lbl_warning = QLabel(Dialog)
        self.lbl_warning.setObjectName(u"lbl_warning")
        self.lbl_warning.setStyleSheet(u"color: #b45309; font-size: 11px; font-weight: 600; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 14px;")
        self.lbl_warning.setWordWrap(True)

        self.bodyLayout.addWidget(self.lbl_warning)

        self.tabs = QTabWidget(Dialog)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setStyleSheet(u"QTabWidget::pane { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; top: -1px; }\n"
"QTabBar { background: #ffffff; }\n"
"QTabBar::tab { background: #ffffff; color: #64748b; padding: 10px 20px; font-size: 12px; font-weight: 700; border: none; border-bottom: 3px solid transparent; }\n"
"QTabBar::tab:selected { color: #023E8A; border-bottom: 3px solid #023E8A; }\n"
"QTabBar::tab:hover:!selected { color: #0077B6; }")
        self.tab_ventes = QWidget()
        self.tab_ventes.setObjectName(u"tab_ventes")
        self.tabVentesLayout = QVBoxLayout(self.tab_ventes)
        self.tabVentesLayout.setSpacing(14)
        self.tabVentesLayout.setObjectName(u"tabVentesLayout")
        self.tabVentesLayout.setContentsMargins(20, 20, 20, 20)
        self.lbl_ventes_stats = QLabel(self.tab_ventes)
        self.lbl_ventes_stats.setObjectName(u"lbl_ventes_stats")
        self.lbl_ventes_stats.setStyleSheet(u"color: #0f172a; font-size: 12px; background: transparent; line-height: 1.8;")
        self.lbl_ventes_stats.setWordWrap(True)

        self.tabVentesLayout.addWidget(self.lbl_ventes_stats)

        self.table_top_produits = QTableWidget(self.tab_ventes)
        if (self.table_top_produits.columnCount() < 3):
            self.table_top_produits.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_top_produits.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_top_produits.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_top_produits.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_top_produits.setObjectName(u"table_top_produits")
        self.table_top_produits.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 8px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_top_produits.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tabVentesLayout.addWidget(self.table_top_produits)

        self.tabs.addTab(self.tab_ventes, "")
        self.tab_clients = QWidget()
        self.tab_clients.setObjectName(u"tab_clients")
        self.tabClientsLayout = QVBoxLayout(self.tab_clients)
        self.tabClientsLayout.setSpacing(14)
        self.tabClientsLayout.setObjectName(u"tabClientsLayout")
        self.tabClientsLayout.setContentsMargins(20, 20, 20, 20)
        self.lbl_clients_stats = QLabel(self.tab_clients)
        self.lbl_clients_stats.setObjectName(u"lbl_clients_stats")
        self.lbl_clients_stats.setStyleSheet(u"color: #0f172a; font-size: 12px; background: transparent; line-height: 1.8;")
        self.lbl_clients_stats.setWordWrap(True)

        self.tabClientsLayout.addWidget(self.lbl_clients_stats)

        self.table_top_clients = QTableWidget(self.tab_clients)
        if (self.table_top_clients.columnCount() < 2):
            self.table_top_clients.setColumnCount(2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_top_clients.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_top_clients.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        self.table_top_clients.setObjectName(u"table_top_clients")
        self.table_top_clients.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 8px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_top_clients.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tabClientsLayout.addWidget(self.table_top_clients)

        self.tabs.addTab(self.tab_clients, "")
        self.tab_stocks = QWidget()
        self.tab_stocks.setObjectName(u"tab_stocks")
        self.tabStocksLayout = QVBoxLayout(self.tab_stocks)
        self.tabStocksLayout.setSpacing(14)
        self.tabStocksLayout.setObjectName(u"tabStocksLayout")
        self.tabStocksLayout.setContentsMargins(20, 20, 20, 20)
        self.lbl_stocks_stats = QLabel(self.tab_stocks)
        self.lbl_stocks_stats.setObjectName(u"lbl_stocks_stats")
        self.lbl_stocks_stats.setStyleSheet(u"color: #0f172a; font-size: 12px; background: transparent; line-height: 1.8;")
        self.lbl_stocks_stats.setWordWrap(True)

        self.tabStocksLayout.addWidget(self.lbl_stocks_stats)

        self.table_rupture = QTableWidget(self.tab_stocks)
        if (self.table_rupture.columnCount() < 2):
            self.table_rupture.setColumnCount(2)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_rupture.setHorizontalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_rupture.setHorizontalHeaderItem(1, __qtablewidgetitem6)
        self.table_rupture.setObjectName(u"table_rupture")
        self.table_rupture.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 8px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_rupture.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tabStocksLayout.addWidget(self.table_rupture)

        self.tabs.addTab(self.tab_stocks, "")

        self.bodyLayout.addWidget(self.tabs)


        self.mainLayout.addLayout(self.bodyLayout)

        self.footer = QFrame(Dialog)
        self.footer.setObjectName(u"footer")
        self.footer.setMinimumSize(QSize(0, 72))
        self.footer.setMaximumSize(QSize(16777215, 72))
        self.footer.setStyleSheet(u"QFrame#footer { background: #ffffff; border-top: 1px solid #e2e8f0; }")
        self.footerLayout = QHBoxLayout(self.footer)
        self.footerLayout.setSpacing(12)
        self.footerLayout.setObjectName(u"footerLayout")
        self.footerLayout.setContentsMargins(24, -1, 24, -1)
        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerLayout.addItem(self.footerSpacer)

        self.btn_close = QPushButton(self.footer)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMinimumSize(QSize(0, 42))
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 24px; }\n"
"QPushButton:hover { background: #0077B6; }")

        self.footerLayout.addWidget(self.btn_close)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Archive \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("Dialog", u"Archive \u2014 lecture seule", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_warning.setText(QCoreApplication.translate("Dialog", u"\u26a0\ufe0f Vue de consultation \u2014 aucune modification possible. Cette archive contient les donn\u00e9es telles qu'elles \u00e9taient \u00e0 la date indiqu\u00e9e.", None))
        self.lbl_ventes_stats.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        ___qtablewidgetitem = self.table_top_produits.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"PRODUIT", None))
        ___qtablewidgetitem1 = self.table_top_produits.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"QUANTIT\u00c9", None))
        ___qtablewidgetitem2 = self.table_top_produits.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"CA", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_ventes), QCoreApplication.translate("Dialog", u"Ventes", None))
        self.lbl_clients_stats.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        ___qtablewidgetitem3 = self.table_top_clients.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"CLIENT", None))
        ___qtablewidgetitem4 = self.table_top_clients.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"TOTAL ACHET\u00c9", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_clients), QCoreApplication.translate("Dialog", u"Clients", None))
        self.lbl_stocks_stats.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        ___qtablewidgetitem5 = self.table_rupture.horizontalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"PRODUIT", None))
        ___qtablewidgetitem6 = self.table_rupture.horizontalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"STOCK", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_stocks), QCoreApplication.translate("Dialog", u"Stocks", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
    # retranslateUi

