# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface_page_surveillanceJcdFNT.ui'
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
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import Icon_rc

class Ui_PageSurveillance(object):
    def setupUi(self, PageSurveillance):
        if not PageSurveillance.objectName():
            PageSurveillance.setObjectName(u"PageSurveillance")
        PageSurveillance.resize(1240, 880)
        PageSurveillance.setStyleSheet(u"\n"
"#PageSurveillance { background: transparent; }\n"
"QLabel { background: transparent; }\n"
"#header_surv {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
"        stop:0 #7c2d12, stop:1 #b91c1c);\n"
"    border-radius: 18px;\n"
"    border: 1px solid #7f1d1d;\n"
"}\n"
"#header_surv QLabel { color: #ffffff; }\n"
"#ico_surv {\n"
"    background: rgba(255,255,255,0.15);\n"
"    border: 1px solid rgba(255,255,255,0.3);\n"
"    border-radius: 14px;\n"
"    padding: 10px;\n"
"}\n"
"#label_surv_title { font-size: 22px; font-weight: 800; }\n"
"#label_surv_sub { font-size: 11px; color: rgba(255,255,255,0.8); }\n"
"#badge_surv {\n"
"    background: rgba(255,255,255,0.2);\n"
"    border: 1px solid rgba(255,255,255,0.4);\n"
"    border-radius: 12px;\n"
"    padding: 8px 18px;\n"
"    color: #ffffff;\n"
"    font-size: 11px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"}\n"
"QFrame#card_surv {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius"
                        ": 16px;\n"
"}\n"
"QLabel#kpi_label_surv {\n"
"    color: #64748b;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"}\n"
"QLabel#kpi_total_surv {\n"
"    color: #0f172a;\n"
"    font-size: 24px;\n"
"    font-weight: 800;\n"
"}\n"
"QLabel#kpi_alertes_surv {\n"
"    color: #b45309;\n"
"    font-size: 24px;\n"
"    font-weight: 800;\n"
"}\n"
"QLabel#kpi_critiques_surv {\n"
"    color: #dc2626;\n"
"    font-size: 24px;\n"
"    font-weight: 800;\n"
"}\n"
"QLabel#kpi_chain_surv {\n"
"    color: #16a34a;\n"
"    font-size: 24px;\n"
"    font-weight: 800;\n"
"}\n"
"\n"
"QPushButton#btn_surv_primary {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"        stop:0 #dc2626, stop:1 #991b1b);\n"
"    color: #ffffff;\n"
"    border: 1px solid #7f1d1d;\n"
"    border-radius: 11px;\n"
"    padding: 10px 20px;\n"
"    font-weight: 800;\n"
"}\n"
"QPushButton#btn_surv_primary:hover { background: #7f1d1d; }\n"
"QPushButton#btn_surv_ghost {\n"
"    background: #ffffff;\n"
"    colo"
                        "r: #475569;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 10px 20px;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton#btn_surv_ghost:hover { background: #f8fafc; }\n"
"\n"
"QComboBox#combo_surv_sev {\n"
"    background: #ffffff;\n"
"    border: 1px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"}\n"
"\n"
"QComboBox::drop-down ,QDateEdit::drop-down { border: none; width: 26px; }\n"
"QComboBox::drop-down ,QDateEdit::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}\n"
"\n"
"QLineEdit#inp_surv_search {\n"
"    background: #ffffff;\n"
"    border: 1px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 8px 14px;\n"
"    min-height: 22px;\n"
"}\n"
"QDateEdit#date_surv_debut, QDateEdit#date_surv_fin {\n"
"    background: #ffffff;\n"
"    border: 1px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 6px 10px;\n"
"    min-height: 22px;\n"
"}\n"
"\n"
"QTableWidget#table_surv {\n"
" "
                        "   background: transparent;\n"
"    border: none;\n"
"    gridline-color: #f1f5f9;\n"
"}\n"
"QTableWidget#table_surv::item {\n"
"    padding: 10px;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"}\n"
"QTableWidget#table_surv::item:selected {\n"
"    background: #eff6ff;\n"
"    color: #1d4ed8;\n"
"}\n"
"QHeaderView::section {\n"
"    background: #f8fafc;\n"
"    color: #94a3b8;\n"
"    padding: 12px;\n"
"    border: none;\n"
"    border-bottom: 1px solid #e6ebf2;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"}\n"
"   ")
        self.root_surv_layout = QVBoxLayout(PageSurveillance)
        self.root_surv_layout.setSpacing(16)
        self.root_surv_layout.setObjectName(u"root_surv_layout")
        self.root_surv_layout.setContentsMargins(20, 20, 20, 20)
        self.header_surv = QFrame(PageSurveillance)
        self.header_surv.setObjectName(u"header_surv")
        self.header_surv.setMinimumSize(QSize(0, 90))
        self.header_surv.setMaximumSize(QSize(16777215, 90))
        self.header_surv_layout = QHBoxLayout(self.header_surv)
        self.header_surv_layout.setSpacing(16)
        self.header_surv_layout.setObjectName(u"header_surv_layout")
        self.header_surv_layout.setContentsMargins(24, 14, 24, 14)
        self.ico_surv = QLabel(self.header_surv)
        self.ico_surv.setObjectName(u"ico_surv")
        self.ico_surv.setMinimumSize(QSize(50, 50))
        self.ico_surv.setMaximumSize(QSize(50, 50))
        self.ico_surv.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.header_surv_layout.addWidget(self.ico_surv)

        self.header_surv_titles = QVBoxLayout()
        self.header_surv_titles.setSpacing(2)
        self.header_surv_titles.setObjectName(u"header_surv_titles")
        self.label_surv_title = QLabel(self.header_surv)
        self.label_surv_title.setObjectName(u"label_surv_title")

        self.header_surv_titles.addWidget(self.label_surv_title)

        self.label_surv_sub = QLabel(self.header_surv)
        self.label_surv_sub.setObjectName(u"label_surv_sub")

        self.header_surv_titles.addWidget(self.label_surv_sub)


        self.header_surv_layout.addLayout(self.header_surv_titles)

        self.spacer_surv = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_surv_layout.addItem(self.spacer_surv)

        self.badge_surv = QLabel(self.header_surv)
        self.badge_surv.setObjectName(u"badge_surv")

        self.header_surv_layout.addWidget(self.badge_surv)


        self.root_surv_layout.addWidget(self.header_surv)

        self.kpi_surv_layout = QHBoxLayout()
        self.kpi_surv_layout.setSpacing(14)
        self.kpi_surv_layout.setObjectName(u"kpi_surv_layout")
        self.card_surv = QFrame(PageSurveillance)
        self.card_surv.setObjectName(u"card_surv")
        self.card_surv.setMinimumSize(QSize(0, 110))
        self.vboxLayout = QVBoxLayout(self.card_surv)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.vboxLayout.setContentsMargins(18, 14, 18, 14)
        self.kpi_label_total = QLabel(self.card_surv)
        self.kpi_label_total.setObjectName(u"kpi_label_total")
        self.kpi_label_total.setStyleSheet(u"color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.vboxLayout.addWidget(self.kpi_label_total)

        self.kpi_surv_total = QLabel(self.card_surv)
        self.kpi_surv_total.setObjectName(u"kpi_surv_total")
        self.kpi_surv_total.setStyleSheet(u"color: #0f172a; font-size: 24px; font-weight: 800;")

        self.vboxLayout.addWidget(self.kpi_surv_total)


        self.kpi_surv_layout.addWidget(self.card_surv)

        self.card_surv1 = QFrame(PageSurveillance)
        self.card_surv1.setObjectName(u"card_surv1")
        self.card_surv1.setMinimumSize(QSize(0, 110))
        self.vboxLayout1 = QVBoxLayout(self.card_surv1)
        self.vboxLayout1.setObjectName(u"vboxLayout1")
        self.vboxLayout1.setContentsMargins(18, 14, 18, 14)
        self.kpi_label_alertes = QLabel(self.card_surv1)
        self.kpi_label_alertes.setObjectName(u"kpi_label_alertes")
        self.kpi_label_alertes.setStyleSheet(u"color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.vboxLayout1.addWidget(self.kpi_label_alertes)

        self.kpi_surv_alertes = QLabel(self.card_surv1)
        self.kpi_surv_alertes.setObjectName(u"kpi_surv_alertes")
        self.kpi_surv_alertes.setStyleSheet(u"color: #b45309; font-size: 24px; font-weight: 800;")

        self.vboxLayout1.addWidget(self.kpi_surv_alertes)


        self.kpi_surv_layout.addWidget(self.card_surv1)

        self.card_surv2 = QFrame(PageSurveillance)
        self.card_surv2.setObjectName(u"card_surv2")
        self.card_surv2.setMinimumSize(QSize(0, 110))
        self.vboxLayout2 = QVBoxLayout(self.card_surv2)
        self.vboxLayout2.setObjectName(u"vboxLayout2")
        self.vboxLayout2.setContentsMargins(18, 14, 18, 14)
        self.kpi_label_critiques = QLabel(self.card_surv2)
        self.kpi_label_critiques.setObjectName(u"kpi_label_critiques")
        self.kpi_label_critiques.setStyleSheet(u"color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.vboxLayout2.addWidget(self.kpi_label_critiques)

        self.kpi_surv_critiques = QLabel(self.card_surv2)
        self.kpi_surv_critiques.setObjectName(u"kpi_surv_critiques")
        self.kpi_surv_critiques.setStyleSheet(u"color: #dc2626; font-size: 24px; font-weight: 800;")

        self.vboxLayout2.addWidget(self.kpi_surv_critiques)


        self.kpi_surv_layout.addWidget(self.card_surv2)

        self.card_surv3 = QFrame(PageSurveillance)
        self.card_surv3.setObjectName(u"card_surv3")
        self.card_surv3.setMinimumSize(QSize(0, 110))
        self.vboxLayout3 = QVBoxLayout(self.card_surv3)
        self.vboxLayout3.setObjectName(u"vboxLayout3")
        self.vboxLayout3.setContentsMargins(18, 14, 18, 14)
        self.kpi_label_chain = QLabel(self.card_surv3)
        self.kpi_label_chain.setObjectName(u"kpi_label_chain")
        self.kpi_label_chain.setStyleSheet(u"color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.vboxLayout3.addWidget(self.kpi_label_chain)

        self.kpi_surv_chain = QLabel(self.card_surv3)
        self.kpi_surv_chain.setObjectName(u"kpi_surv_chain")
        self.kpi_surv_chain.setStyleSheet(u"color: #16a34a; font-size: 24px; font-weight: 800;")

        self.vboxLayout3.addWidget(self.kpi_surv_chain)


        self.kpi_surv_layout.addWidget(self.card_surv3)


        self.root_surv_layout.addLayout(self.kpi_surv_layout)

        self.card_surv4 = QFrame(PageSurveillance)
        self.card_surv4.setObjectName(u"card_surv4")
        self.card_surv4.setMinimumSize(QSize(0, 70))
        self.card_surv4.setMaximumSize(QSize(16777215, 70))
        self.hboxLayout = QHBoxLayout(self.card_surv4)
        self.hboxLayout.setSpacing(12)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.hboxLayout.setContentsMargins(16, 12, 16, 12)
        self.combo_surv_sev = QComboBox(self.card_surv4)
        self.combo_surv_sev.addItem("")
        self.combo_surv_sev.addItem("")
        self.combo_surv_sev.addItem("")
        self.combo_surv_sev.addItem("")
        self.combo_surv_sev.setObjectName(u"combo_surv_sev")
        self.combo_surv_sev.setStyleSheet(u"")

        self.hboxLayout.addWidget(self.combo_surv_sev)

        self.inp_surv_search = QLineEdit(self.card_surv4)
        self.inp_surv_search.setObjectName(u"inp_surv_search")

        self.hboxLayout.addWidget(self.inp_surv_search)

        self.label = QLabel(self.card_surv4)
        self.label.setObjectName(u"label")

        self.hboxLayout.addWidget(self.label)

        self.date_surv_debut = QDateEdit(self.card_surv4)
        self.date_surv_debut.setObjectName(u"date_surv_debut")
        self.date_surv_debut.setCalendarPopup(True)

        self.hboxLayout.addWidget(self.date_surv_debut)

        self.label1 = QLabel(self.card_surv4)
        self.label1.setObjectName(u"label1")

        self.hboxLayout.addWidget(self.label1)

        self.date_surv_fin = QDateEdit(self.card_surv4)
        self.date_surv_fin.setObjectName(u"date_surv_fin")
        self.date_surv_fin.setCalendarPopup(True)

        self.hboxLayout.addWidget(self.date_surv_fin)

        self.spacer_filt = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout.addItem(self.spacer_filt)

        self.btn_surv_chain = QPushButton(self.card_surv4)
        self.btn_surv_chain.setObjectName(u"btn_surv_chain")
        self.btn_surv_chain.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_surv_chain.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #dc2626, stop:1 #991b1b); color: #ffffff; border: 1px solid #7f1d1d; border-radius: 11px; padding: 10px 20px; font-weight: 800;")

        self.hboxLayout.addWidget(self.btn_surv_chain)

        self.btn_surv_refresh = QPushButton(self.card_surv4)
        self.btn_surv_refresh.setObjectName(u"btn_surv_refresh")
        self.btn_surv_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_surv_refresh.setStyleSheet(u"background: #ffffff; color: #475569; border: 1.5px solid #dbe3ec; border-radius: 11px; padding: 10px 20px; font-weight: 700;")

        self.hboxLayout.addWidget(self.btn_surv_refresh)


        self.root_surv_layout.addWidget(self.card_surv4)

        self.card_surv5 = QFrame(PageSurveillance)
        self.card_surv5.setObjectName(u"card_surv5")
        self.vboxLayout4 = QVBoxLayout(self.card_surv5)
        self.vboxLayout4.setObjectName(u"vboxLayout4")
        self.vboxLayout4.setContentsMargins(0, 0, 0, 0)
        self.table_surv = QTableWidget(self.card_surv5)
        if (self.table_surv.columnCount() < 7):
            self.table_surv.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_surv.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_surv.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_surv.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_surv.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_surv.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_surv.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_surv.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.table_surv.setObjectName(u"table_surv")
        self.table_surv.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_surv.setAlternatingRowColors(True)
        self.table_surv.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_surv.setShowGrid(False)
        self.table_surv.setColumnCount(7)
        self.table_surv.horizontalHeader().setVisible(True)
        self.table_surv.verticalHeader().setVisible(False)
        self.table_surv.verticalHeader().setDefaultSectionSize(52)

        self.vboxLayout4.addWidget(self.table_surv)


        self.root_surv_layout.addWidget(self.card_surv5)


        self.retranslateUi(PageSurveillance)

        QMetaObject.connectSlotsByName(PageSurveillance)
    # setupUi

    def retranslateUi(self, PageSurveillance):
        self.ico_surv.setText("")
        self.label_surv_title.setText(QCoreApplication.translate("PageSurveillance", u"Surveillance & S\u00e9curit\u00e9", None))
        self.label_surv_sub.setText(QCoreApplication.translate("PageSurveillance", u"Monitoring des actions sensibles et int\u00e9grit\u00e9 de l'audit", None))
        self.badge_surv.setText(QCoreApplication.translate("PageSurveillance", u"\u25cf  OWNER / DEVELOPER", None))
        self.kpi_label_total.setText(QCoreApplication.translate("PageSurveillance", u"ACTIONS AUJOURD'HUI", None))
        self.kpi_surv_total.setText(QCoreApplication.translate("PageSurveillance", u"0", None))
        self.kpi_label_alertes.setText(QCoreApplication.translate("PageSurveillance", u"ALERTES (warning + danger)", None))
        self.kpi_surv_alertes.setText(QCoreApplication.translate("PageSurveillance", u"0", None))
        self.kpi_label_critiques.setText(QCoreApplication.translate("PageSurveillance", u"ACTIONS CRITIQUES", None))
        self.kpi_surv_critiques.setText(QCoreApplication.translate("PageSurveillance", u"0", None))
        self.kpi_label_chain.setText(QCoreApplication.translate("PageSurveillance", u"INT\u00c9GRIT\u00c9 CHA\u00ceNE", None))
        self.kpi_surv_chain.setText(QCoreApplication.translate("PageSurveillance", u"\u2014", None))
        self.combo_surv_sev.setItemText(0, QCoreApplication.translate("PageSurveillance", u"Toutes s\u00e9v\u00e9rit\u00e9s", None))
        self.combo_surv_sev.setItemText(1, QCoreApplication.translate("PageSurveillance", u"\U0001f534 Danger", None))
        self.combo_surv_sev.setItemText(2, QCoreApplication.translate("PageSurveillance", u"\U0001f7e0 Warning", None))
        self.combo_surv_sev.setItemText(3, QCoreApplication.translate("PageSurveillance", u"\U0001f535 Info", None))

        self.inp_surv_search.setPlaceholderText(QCoreApplication.translate("PageSurveillance", u"Rechercher (utilisateur, action, cible\u2026)", None))
        self.label.setText(QCoreApplication.translate("PageSurveillance", u"Du", None))
        self.label1.setText(QCoreApplication.translate("PageSurveillance", u"au", None))
        self.btn_surv_chain.setText(QCoreApplication.translate("PageSurveillance", u"\U0001f512  V\U000000e9rifier l'int\U000000e9grit\U000000e9", None))
        self.btn_surv_refresh.setText(QCoreApplication.translate("PageSurveillance", u"Actualiser", None))
        ___qtablewidgetitem = self.table_surv.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageSurveillance", u"DATE", None))
        ___qtablewidgetitem1 = self.table_surv.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageSurveillance", u"UTILISATEUR", None))
        ___qtablewidgetitem2 = self.table_surv.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageSurveillance", u"S\u00c9V\u00c9RIT\u00c9", None))
        ___qtablewidgetitem3 = self.table_surv.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageSurveillance", u"ACTION", None))
        ___qtablewidgetitem4 = self.table_surv.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PageSurveillance", u"CIBLE", None))
        ___qtablewidgetitem5 = self.table_surv.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PageSurveillance", u"IP", None))
        ___qtablewidgetitem6 = self.table_surv.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("PageSurveillance", u"D\u00c9TAILS", None))
        pass
    # retranslateUi

