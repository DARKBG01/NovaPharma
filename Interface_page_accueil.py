# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_page_accueilOqMnVR.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_PageAccueil(object):
    def setupUi(self, PageAccueil):
        if not PageAccueil.objectName():
            PageAccueil.setObjectName(u"PageAccueil")
        PageAccueil.resize(1200, 800)
        PageAccueil.setStyleSheet(u"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n"
"   PAGE ACCUEIL \u2014 Nova Pharma\n"
"   \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QWidget#PageAccueil { background: #f0f4f8; }\n"
"QWidget#PageAccueil QLabel { background: transparent; }\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 HERO \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
                        "\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#header_frame {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"        stop:0 #023E8A, stop:0.5 #0077B6, stop:1 #00B4D8);\n"
"    border-radius: 20px;\n"
"    border: none;\n"
"}\n"
"QFrame#header_frame QLabel { color: #ffffff; }\n"
"\n"
"QLabel#lbl_salutation {\n"
"    font-size: 14px; font-weight: 600;\n"
"    color: rgba(255,255,255,0.85);\n"
"}\n"
"QLabel#lbl_date {\n"
"    font-size: 11px; font-weight: 600;\n"
"    color: rgba(255,255,255,0.65); letter-spacing: 0.5px;\n"
"}\n"
"QLabel#lbl_ca_title {\n"
"    font-size: 10px; font-weight: 800;\n"
"    color: rgba(255,255,255,0.75); letter-spacing: 2px;\n"
"}\n"
"QLabel#lbl_ca_value {\n"
"    font-size: 42px; font-weight: 800;\n"
"    color: #ffffff; letter-spacing: -1px;\n"
"}\n"
"QLabel#lbl_ca_trend {\n"
"    font-size: 12px; font-weight: 700;\n"
"    color: rgba(255,255,255,0.9);\n"
"}\n"
"QLabel#lbl_periode_title {\n"
"    font-size: 10px; font-weight: 800;\n"
"    color: rgba(255,255,255"
                        ",0.75); letter-spacing: 2px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 PILLS p\u00e9riode \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QPushButton[pill=\"true\"] {\n"
"    background: rgba(255,255,255,0.15);\n"
"    color: rgba(255,255,255,0.8);\n"
"    border: 1px solid rgba(255,255,255,0.2);\n"
"    border-radius: 17px;\n"
"    padding: 0 20px;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    min-height: 34px;\n"
"    letter-spacing: 0.3px;\n"
"}\n"
"QPushButton[pill=\"true\"]:hover {\n"
"    background: rgba(255,255,255,0.25);\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton[pill=\"true\"]:checked {\n"
"    background: #ffffff;\n"
"    color: #023E8A;\n"
"    border-color: #ffffff;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 KPI CARDS \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
                        " */\n"
"QFrame#kpi_ventes, QFrame#kpi_panier,\n"
"QFrame#kpi_clients, QFrame#kpi_ruptures {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 14px;\n"
"}\n"
"QFrame#kpi_ventes:hover    { border-color: #0077B6; }\n"
"QFrame#kpi_panier:hover    { border-color: #00B4D8; }\n"
"QFrame#kpi_clients:hover   { border-color: #16A34A; }\n"
"QFrame#kpi_ruptures:hover  { border-color: #DC2626; }\n"
"\n"
"QLabel#kpi_ventes_icon    { background: #0077B620; border-radius: 10px; }\n"
"QLabel#kpi_panier_icon    { background: #00B4D820; border-radius: 10px; }\n"
"QLabel#kpi_clients_icon   { background: #16A34A20; border-radius: 10px; }\n"
"QLabel#kpi_ruptures_icon  { background: #DC262620; border-radius: 10px; }\n"
"\n"
"QLabel#kpi_ventes_title   { font-size: 10px; font-weight: 800; color: #0077B6; letter-spacing: 1.2px; }\n"
"QLabel#kpi_panier_title   { font-size: 10px; font-weight: 800; color: #00B4D8; letter-spacing: 1.2px; }\n"
"QLabel#kpi_clients_title  { font-size: 10px; font-weight: 80"
                        "0; color: #16A34A; letter-spacing: 1.2px; }\n"
"QLabel#kpi_ruptures_title { font-size: 10px; font-weight: 800; color: #DC2626; letter-spacing: 1.2px; }\n"
"\n"
"QLabel#kpi_ventes_value, QLabel#kpi_panier_value,\n"
"QLabel#kpi_clients_value, QLabel#kpi_ruptures_value {\n"
"    font-size: 26px; font-weight: 800;\n"
"    color: #0f172a; letter-spacing: -0.5px;\n"
"}\n"
"QLabel#kpi_ventes_trend, QLabel#kpi_panier_trend,\n"
"QLabel#kpi_clients_trend, QLabel#kpi_ruptures_trend {\n"
"    font-size: 11px; font-weight: 700; color: #16A34A;\n"
"}\n"
"QLabel#kpi_ventes_sub, QLabel#kpi_panier_sub,\n"
"QLabel#kpi_clients_sub, QLabel#kpi_ruptures_sub {\n"
"    font-size: 10px; font-weight: 600; color: #94a3b8;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 CARTES TOP5 / ALERTES \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#card_top5, QFrame#card_alertes {\n"
"    background: #ffffff;\n"
"    border: 1px s"
                        "olid #e6ebf2;\n"
"    border-radius: 14px;\n"
"}\n"
"QLabel#lbl_top5_title, QLabel#lbl_alertes_title {\n"
"    font-size: 14px; font-weight: 800; color: #0f172a;\n"
"}\n"
"QLabel#lbl_alertes_count {\n"
"    background: #fef2f2;\n"
"    color: #b91c1c;\n"
"    border-radius: 10px;\n"
"    padding: 3px 10px;\n"
"    font-size: 10px; font-weight: 800;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 BANDEAU SECONDAIRE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#secondary_bar {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 12px;\n"
"}\n"
"QLabel#blk_stock_title,\n"
"QLabel#blk_marge_title,\n"
"QLabel#blk_annul_title {\n"
"    font-size: 9px; font-weight: 800;\n"
"    color: #94a3b8; letter-spacing: 1.2px;\n"
"}\n"
"QLabel#blk_stock_value,\n"
"QLabel#blk_marge_value,\n"
"QLabel#blk_annul_value {\n"
"    font-size: 16px; font-weight: 800;\n"
"    color: #0f"
                        "172a;\n"
"}\n"
"")
        self.root_layout = QVBoxLayout(PageAccueil)
        self.root_layout.setSpacing(18)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(24, 24, 24, 24)
        self.header_frame = QFrame(PageAccueil)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 160))
        self.header_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.hero_layout = QHBoxLayout(self.header_frame)
        self.hero_layout.setSpacing(24)
        self.hero_layout.setObjectName(u"hero_layout")
        self.hero_layout.setContentsMargins(32, 24, 32, 24)
        self.hero_left = QVBoxLayout()
        self.hero_left.setSpacing(4)
        self.hero_left.setObjectName(u"hero_left")
        self.lbl_salutation = QLabel(self.header_frame)
        self.lbl_salutation.setObjectName(u"lbl_salutation")

        self.hero_left.addWidget(self.lbl_salutation)

        self.lbl_date = QLabel(self.header_frame)
        self.lbl_date.setObjectName(u"lbl_date")

        self.hero_left.addWidget(self.lbl_date)

        self.hero_spacer_1 = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.hero_left.addItem(self.hero_spacer_1)

        self.lbl_ca_title = QLabel(self.header_frame)
        self.lbl_ca_title.setObjectName(u"lbl_ca_title")

        self.hero_left.addWidget(self.lbl_ca_title)

        self.lbl_ca_value = QLabel(self.header_frame)
        self.lbl_ca_value.setObjectName(u"lbl_ca_value")

        self.hero_left.addWidget(self.lbl_ca_value)

        self.lbl_ca_trend = QLabel(self.header_frame)
        self.lbl_ca_trend.setObjectName(u"lbl_ca_trend")

        self.hero_left.addWidget(self.lbl_ca_trend)


        self.hero_layout.addLayout(self.hero_left)

        self.hero_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hero_layout.addItem(self.hero_spacer_2)

        self.hero_right = QVBoxLayout()
        self.hero_right.setSpacing(10)
        self.hero_right.setObjectName(u"hero_right")
        self.lbl_periode_title = QLabel(self.header_frame)
        self.lbl_periode_title.setObjectName(u"lbl_periode_title")
        self.lbl_periode_title.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.hero_right.addWidget(self.lbl_periode_title)

        self.pills_row = QHBoxLayout()
        self.pills_row.setSpacing(6)
        self.pills_row.setObjectName(u"pills_row")
        self.btn_periode_semaine = QPushButton(self.header_frame)
        self.btn_periode_semaine.setObjectName(u"btn_periode_semaine")
        self.btn_periode_semaine.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_periode_semaine.setCheckable(True)
        self.btn_periode_semaine.setProperty(u"pill", True)

        self.pills_row.addWidget(self.btn_periode_semaine)

        self.btn_periode_mois = QPushButton(self.header_frame)
        self.btn_periode_mois.setObjectName(u"btn_periode_mois")
        self.btn_periode_mois.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_periode_mois.setCheckable(True)
        self.btn_periode_mois.setChecked(True)
        self.btn_periode_mois.setProperty(u"pill", True)

        self.pills_row.addWidget(self.btn_periode_mois)

        self.btn_periode_annee = QPushButton(self.header_frame)
        self.btn_periode_annee.setObjectName(u"btn_periode_annee")
        self.btn_periode_annee.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_periode_annee.setCheckable(True)
        self.btn_periode_annee.setProperty(u"pill", True)

        self.pills_row.addWidget(self.btn_periode_annee)


        self.hero_right.addLayout(self.pills_row)


        self.hero_layout.addLayout(self.hero_right)


        self.root_layout.addWidget(self.header_frame)

        self.kpis_row = QHBoxLayout()
        self.kpis_row.setSpacing(14)
        self.kpis_row.setObjectName(u"kpis_row")
        self.kpi_ventes = QFrame(PageAccueil)
        self.kpi_ventes.setObjectName(u"kpi_ventes")
        self.kpi_ventes.setMinimumSize(QSize(0, 128))
        self.kpi_ventes.setFrameShape(QFrame.Shape.NoFrame)
        self.kpi_ventes_layout = QVBoxLayout(self.kpi_ventes)
        self.kpi_ventes_layout.setSpacing(8)
        self.kpi_ventes_layout.setObjectName(u"kpi_ventes_layout")
        self.kpi_ventes_layout.setContentsMargins(20, 18, 20, 18)
        self.kpi_ventes_header = QHBoxLayout()
        self.kpi_ventes_header.setSpacing(10)
        self.kpi_ventes_header.setObjectName(u"kpi_ventes_header")
        self.kpi_ventes_icon = QLabel(self.kpi_ventes)
        self.kpi_ventes_icon.setObjectName(u"kpi_ventes_icon")
        self.kpi_ventes_icon.setMinimumSize(QSize(34, 34))
        self.kpi_ventes_icon.setMaximumSize(QSize(34, 34))
        self.kpi_ventes_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.kpi_ventes_header.addWidget(self.kpi_ventes_icon)

        self.kpi_ventes_title = QLabel(self.kpi_ventes)
        self.kpi_ventes_title.setObjectName(u"kpi_ventes_title")

        self.kpi_ventes_header.addWidget(self.kpi_ventes_title)

        self.kpi_ventes_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi_ventes_header.addItem(self.kpi_ventes_spacer)


        self.kpi_ventes_layout.addLayout(self.kpi_ventes_header)

        self.kpi_ventes_value = QLabel(self.kpi_ventes)
        self.kpi_ventes_value.setObjectName(u"kpi_ventes_value")

        self.kpi_ventes_layout.addWidget(self.kpi_ventes_value)

        self.kpi_ventes_footer = QHBoxLayout()
        self.kpi_ventes_footer.setSpacing(6)
        self.kpi_ventes_footer.setObjectName(u"kpi_ventes_footer")
        self.kpi_ventes_trend = QLabel(self.kpi_ventes)
        self.kpi_ventes_trend.setObjectName(u"kpi_ventes_trend")

        self.kpi_ventes_footer.addWidget(self.kpi_ventes_trend)

        self.kpi_ventes_sub = QLabel(self.kpi_ventes)
        self.kpi_ventes_sub.setObjectName(u"kpi_ventes_sub")

        self.kpi_ventes_footer.addWidget(self.kpi_ventes_sub)

        self.kpi_ventes_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi_ventes_footer.addItem(self.kpi_ventes_spacer_2)


        self.kpi_ventes_layout.addLayout(self.kpi_ventes_footer)


        self.kpis_row.addWidget(self.kpi_ventes)

        self.kpi_panier = QFrame(PageAccueil)
        self.kpi_panier.setObjectName(u"kpi_panier")
        self.kpi_panier.setMinimumSize(QSize(0, 128))
        self.kpi_panier.setFrameShape(QFrame.Shape.NoFrame)
        self.kpi_panier_layout = QVBoxLayout(self.kpi_panier)
        self.kpi_panier_layout.setSpacing(8)
        self.kpi_panier_layout.setObjectName(u"kpi_panier_layout")
        self.kpi_panier_layout.setContentsMargins(20, 18, 20, 18)
        self.kpi_panier_header = QHBoxLayout()
        self.kpi_panier_header.setSpacing(10)
        self.kpi_panier_header.setObjectName(u"kpi_panier_header")
        self.kpi_panier_icon = QLabel(self.kpi_panier)
        self.kpi_panier_icon.setObjectName(u"kpi_panier_icon")
        self.kpi_panier_icon.setMinimumSize(QSize(34, 34))
        self.kpi_panier_icon.setMaximumSize(QSize(34, 34))
        self.kpi_panier_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.kpi_panier_header.addWidget(self.kpi_panier_icon)

        self.kpi_panier_title = QLabel(self.kpi_panier)
        self.kpi_panier_title.setObjectName(u"kpi_panier_title")

        self.kpi_panier_header.addWidget(self.kpi_panier_title)

        self.kpi_panier_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi_panier_header.addItem(self.kpi_panier_spacer)


        self.kpi_panier_layout.addLayout(self.kpi_panier_header)

        self.kpi_panier_value = QLabel(self.kpi_panier)
        self.kpi_panier_value.setObjectName(u"kpi_panier_value")

        self.kpi_panier_layout.addWidget(self.kpi_panier_value)

        self.kpi_panier_footer = QHBoxLayout()
        self.kpi_panier_footer.setSpacing(6)
        self.kpi_panier_footer.setObjectName(u"kpi_panier_footer")
        self.kpi_panier_trend = QLabel(self.kpi_panier)
        self.kpi_panier_trend.setObjectName(u"kpi_panier_trend")

        self.kpi_panier_footer.addWidget(self.kpi_panier_trend)

        self.kpi_panier_sub = QLabel(self.kpi_panier)
        self.kpi_panier_sub.setObjectName(u"kpi_panier_sub")

        self.kpi_panier_footer.addWidget(self.kpi_panier_sub)

        self.kpi_panier_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi_panier_footer.addItem(self.kpi_panier_spacer_2)


        self.kpi_panier_layout.addLayout(self.kpi_panier_footer)


        self.kpis_row.addWidget(self.kpi_panier)

        self.kpi_clients = QFrame(PageAccueil)
        self.kpi_clients.setObjectName(u"kpi_clients")
        self.kpi_clients.setMinimumSize(QSize(0, 128))
        self.kpi_clients.setFrameShape(QFrame.Shape.NoFrame)
        self.kpi_clients_layout = QVBoxLayout(self.kpi_clients)
        self.kpi_clients_layout.setSpacing(8)
        self.kpi_clients_layout.setObjectName(u"kpi_clients_layout")
        self.kpi_clients_layout.setContentsMargins(20, 18, 20, 18)
        self.kpi_clients_header = QHBoxLayout()
        self.kpi_clients_header.setSpacing(10)
        self.kpi_clients_header.setObjectName(u"kpi_clients_header")
        self.kpi_clients_icon = QLabel(self.kpi_clients)
        self.kpi_clients_icon.setObjectName(u"kpi_clients_icon")
        self.kpi_clients_icon.setMinimumSize(QSize(34, 34))
        self.kpi_clients_icon.setMaximumSize(QSize(34, 34))
        self.kpi_clients_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.kpi_clients_header.addWidget(self.kpi_clients_icon)

        self.kpi_clients_title = QLabel(self.kpi_clients)
        self.kpi_clients_title.setObjectName(u"kpi_clients_title")

        self.kpi_clients_header.addWidget(self.kpi_clients_title)

        self.kpi_clients_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi_clients_header.addItem(self.kpi_clients_spacer)


        self.kpi_clients_layout.addLayout(self.kpi_clients_header)

        self.kpi_clients_value = QLabel(self.kpi_clients)
        self.kpi_clients_value.setObjectName(u"kpi_clients_value")

        self.kpi_clients_layout.addWidget(self.kpi_clients_value)

        self.kpi_clients_footer = QHBoxLayout()
        self.kpi_clients_footer.setSpacing(6)
        self.kpi_clients_footer.setObjectName(u"kpi_clients_footer")
        self.kpi_clients_trend = QLabel(self.kpi_clients)
        self.kpi_clients_trend.setObjectName(u"kpi_clients_trend")

        self.kpi_clients_footer.addWidget(self.kpi_clients_trend)

        self.kpi_clients_sub = QLabel(self.kpi_clients)
        self.kpi_clients_sub.setObjectName(u"kpi_clients_sub")

        self.kpi_clients_footer.addWidget(self.kpi_clients_sub)

        self.kpi_clients_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi_clients_footer.addItem(self.kpi_clients_spacer_2)


        self.kpi_clients_layout.addLayout(self.kpi_clients_footer)


        self.kpis_row.addWidget(self.kpi_clients)

        self.kpi_ruptures = QFrame(PageAccueil)
        self.kpi_ruptures.setObjectName(u"kpi_ruptures")
        self.kpi_ruptures.setMinimumSize(QSize(0, 128))
        self.kpi_ruptures.setFrameShape(QFrame.Shape.NoFrame)
        self.kpi_ruptures_layout = QVBoxLayout(self.kpi_ruptures)
        self.kpi_ruptures_layout.setSpacing(8)
        self.kpi_ruptures_layout.setObjectName(u"kpi_ruptures_layout")
        self.kpi_ruptures_layout.setContentsMargins(20, 18, 20, 18)
        self.kpi_ruptures_header = QHBoxLayout()
        self.kpi_ruptures_header.setSpacing(10)
        self.kpi_ruptures_header.setObjectName(u"kpi_ruptures_header")
        self.kpi_ruptures_icon = QLabel(self.kpi_ruptures)
        self.kpi_ruptures_icon.setObjectName(u"kpi_ruptures_icon")
        self.kpi_ruptures_icon.setMinimumSize(QSize(34, 34))
        self.kpi_ruptures_icon.setMaximumSize(QSize(34, 34))
        self.kpi_ruptures_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.kpi_ruptures_header.addWidget(self.kpi_ruptures_icon)

        self.kpi_ruptures_title = QLabel(self.kpi_ruptures)
        self.kpi_ruptures_title.setObjectName(u"kpi_ruptures_title")

        self.kpi_ruptures_header.addWidget(self.kpi_ruptures_title)

        self.kpi_ruptures_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi_ruptures_header.addItem(self.kpi_ruptures_spacer)


        self.kpi_ruptures_layout.addLayout(self.kpi_ruptures_header)

        self.kpi_ruptures_value = QLabel(self.kpi_ruptures)
        self.kpi_ruptures_value.setObjectName(u"kpi_ruptures_value")

        self.kpi_ruptures_layout.addWidget(self.kpi_ruptures_value)

        self.kpi_ruptures_footer = QHBoxLayout()
        self.kpi_ruptures_footer.setSpacing(6)
        self.kpi_ruptures_footer.setObjectName(u"kpi_ruptures_footer")
        self.kpi_ruptures_trend = QLabel(self.kpi_ruptures)
        self.kpi_ruptures_trend.setObjectName(u"kpi_ruptures_trend")

        self.kpi_ruptures_footer.addWidget(self.kpi_ruptures_trend)

        self.kpi_ruptures_sub = QLabel(self.kpi_ruptures)
        self.kpi_ruptures_sub.setObjectName(u"kpi_ruptures_sub")

        self.kpi_ruptures_footer.addWidget(self.kpi_ruptures_sub)

        self.kpi_ruptures_spacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.kpi_ruptures_footer.addItem(self.kpi_ruptures_spacer_2)


        self.kpi_ruptures_layout.addLayout(self.kpi_ruptures_footer)


        self.kpis_row.addWidget(self.kpi_ruptures)


        self.root_layout.addLayout(self.kpis_row)

        self.bottom_row = QHBoxLayout()
        self.bottom_row.setSpacing(14)
        self.bottom_row.setObjectName(u"bottom_row")
        self.card_top5 = QFrame(PageAccueil)
        self.card_top5.setObjectName(u"card_top5")
        self.card_top5.setMinimumSize(QSize(0, 320))
        self.card_top5.setFrameShape(QFrame.Shape.NoFrame)
        self.card_top5_layout = QVBoxLayout(self.card_top5)
        self.card_top5_layout.setSpacing(14)
        self.card_top5_layout.setObjectName(u"card_top5_layout")
        self.card_top5_layout.setContentsMargins(20, 18, 20, 18)
        self.top5_header = QHBoxLayout()
        self.top5_header.setSpacing(10)
        self.top5_header.setObjectName(u"top5_header")
        self.lbl_top5_icon = QLabel(self.card_top5)
        self.lbl_top5_icon.setObjectName(u"lbl_top5_icon")
        self.lbl_top5_icon.setMinimumSize(QSize(20, 20))
        self.lbl_top5_icon.setMaximumSize(QSize(20, 20))

        self.top5_header.addWidget(self.lbl_top5_icon)

        self.lbl_top5_title = QLabel(self.card_top5)
        self.lbl_top5_title.setObjectName(u"lbl_top5_title")

        self.top5_header.addWidget(self.lbl_top5_title)

        self.top5_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.top5_header.addItem(self.top5_spacer)


        self.card_top5_layout.addLayout(self.top5_header)

        self.top5_container = QWidget(self.card_top5)
        self.top5_container.setObjectName(u"top5_container")
        self.top5_container.setStyleSheet(u"QWidget#top5_container { background: transparent; }")
        self.top5_layout = QVBoxLayout(self.top5_container)
        self.top5_layout.setSpacing(8)
        self.top5_layout.setObjectName(u"top5_layout")
        self.top5_layout.setContentsMargins(0, 0, 0, 0)

        self.card_top5_layout.addWidget(self.top5_container)


        self.bottom_row.addWidget(self.card_top5)

        self.card_alertes = QFrame(PageAccueil)
        self.card_alertes.setObjectName(u"card_alertes")
        self.card_alertes.setMinimumSize(QSize(0, 320))
        self.card_alertes.setFrameShape(QFrame.Shape.NoFrame)
        self.card_alertes_layout = QVBoxLayout(self.card_alertes)
        self.card_alertes_layout.setSpacing(14)
        self.card_alertes_layout.setObjectName(u"card_alertes_layout")
        self.card_alertes_layout.setContentsMargins(20, 18, 20, 18)
        self.alertes_header = QHBoxLayout()
        self.alertes_header.setSpacing(10)
        self.alertes_header.setObjectName(u"alertes_header")
        self.lbl_alertes_icon = QLabel(self.card_alertes)
        self.lbl_alertes_icon.setObjectName(u"lbl_alertes_icon")
        self.lbl_alertes_icon.setMinimumSize(QSize(20, 20))
        self.lbl_alertes_icon.setMaximumSize(QSize(20, 20))

        self.alertes_header.addWidget(self.lbl_alertes_icon)

        self.lbl_alertes_title = QLabel(self.card_alertes)
        self.lbl_alertes_title.setObjectName(u"lbl_alertes_title")

        self.alertes_header.addWidget(self.lbl_alertes_title)

        self.alertes_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.alertes_header.addItem(self.alertes_spacer)

        self.lbl_alertes_count = QLabel(self.card_alertes)
        self.lbl_alertes_count.setObjectName(u"lbl_alertes_count")
        self.lbl_alertes_count.setVisible(False)
        self.lbl_alertes_count.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.alertes_header.addWidget(self.lbl_alertes_count)


        self.card_alertes_layout.addLayout(self.alertes_header)

        self.alertes_container = QWidget(self.card_alertes)
        self.alertes_container.setObjectName(u"alertes_container")
        self.alertes_container.setStyleSheet(u"QWidget#alertes_container { background: transparent; }")
        self.alertes_layout = QVBoxLayout(self.alertes_container)
        self.alertes_layout.setSpacing(8)
        self.alertes_layout.setObjectName(u"alertes_layout")
        self.alertes_layout.setContentsMargins(0, 0, 0, 0)

        self.card_alertes_layout.addWidget(self.alertes_container)


        self.bottom_row.addWidget(self.card_alertes)


        self.root_layout.addLayout(self.bottom_row)

        self.secondary_bar = QFrame(PageAccueil)
        self.secondary_bar.setObjectName(u"secondary_bar")
        self.secondary_bar.setMinimumSize(QSize(0, 72))
        self.secondary_bar.setMaximumSize(QSize(16777215, 72))
        self.secondary_bar.setFrameShape(QFrame.Shape.NoFrame)
        self.secondary_layout = QHBoxLayout(self.secondary_bar)
        self.secondary_layout.setSpacing(32)
        self.secondary_layout.setObjectName(u"secondary_layout")
        self.secondary_layout.setContentsMargins(24, 14, 24, 14)
        self.blk_stock_layout = QVBoxLayout()
        self.blk_stock_layout.setSpacing(2)
        self.blk_stock_layout.setObjectName(u"blk_stock_layout")
        self.blk_stock_title = QLabel(self.secondary_bar)
        self.blk_stock_title.setObjectName(u"blk_stock_title")

        self.blk_stock_layout.addWidget(self.blk_stock_title)

        self.blk_stock_value = QLabel(self.secondary_bar)
        self.blk_stock_value.setObjectName(u"blk_stock_value")

        self.blk_stock_layout.addWidget(self.blk_stock_value)


        self.secondary_layout.addLayout(self.blk_stock_layout)

        self.blk_marge_layout = QVBoxLayout()
        self.blk_marge_layout.setSpacing(2)
        self.blk_marge_layout.setObjectName(u"blk_marge_layout")
        self.blk_marge_title = QLabel(self.secondary_bar)
        self.blk_marge_title.setObjectName(u"blk_marge_title")

        self.blk_marge_layout.addWidget(self.blk_marge_title)

        self.blk_marge_value = QLabel(self.secondary_bar)
        self.blk_marge_value.setObjectName(u"blk_marge_value")

        self.blk_marge_layout.addWidget(self.blk_marge_value)


        self.secondary_layout.addLayout(self.blk_marge_layout)

        self.blk_annul_layout = QVBoxLayout()
        self.blk_annul_layout.setSpacing(2)
        self.blk_annul_layout.setObjectName(u"blk_annul_layout")
        self.blk_annul_title = QLabel(self.secondary_bar)
        self.blk_annul_title.setObjectName(u"blk_annul_title")

        self.blk_annul_layout.addWidget(self.blk_annul_title)

        self.blk_annul_value = QLabel(self.secondary_bar)
        self.blk_annul_value.setObjectName(u"blk_annul_value")

        self.blk_annul_layout.addWidget(self.blk_annul_value)


        self.secondary_layout.addLayout(self.blk_annul_layout)

        self.secondary_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secondary_layout.addItem(self.secondary_spacer)


        self.root_layout.addWidget(self.secondary_bar)


        self.retranslateUi(PageAccueil)

        QMetaObject.connectSlotsByName(PageAccueil)
    # setupUi

    def retranslateUi(self, PageAccueil):
        self.lbl_salutation.setText(QCoreApplication.translate("PageAccueil", u"Bonjour Utilisateur", None))
        self.lbl_date.setText(QCoreApplication.translate("PageAccueil", u"Date du jour", None))
        self.lbl_ca_title.setText(QCoreApplication.translate("PageAccueil", u"CHIFFRE D'AFFAIRES", None))
        self.lbl_ca_value.setText(QCoreApplication.translate("PageAccueil", u"\u2014", None))
        self.lbl_ca_trend.setText("")
        self.lbl_periode_title.setText(QCoreApplication.translate("PageAccueil", u"P\u00c9RIODE", None))
        self.btn_periode_semaine.setText(QCoreApplication.translate("PageAccueil", u"Semaine", None))
        self.btn_periode_mois.setText(QCoreApplication.translate("PageAccueil", u"Mois", None))
        self.btn_periode_annee.setText(QCoreApplication.translate("PageAccueil", u"Ann\u00e9e", None))
        self.kpi_ventes_icon.setText("")
        self.kpi_ventes_title.setText(QCoreApplication.translate("PageAccueil", u"VENTES", None))
        self.kpi_ventes_value.setText(QCoreApplication.translate("PageAccueil", u"\u2014", None))
        self.kpi_ventes_trend.setText("")
        self.kpi_ventes_sub.setText("")
        self.kpi_panier_icon.setText("")
        self.kpi_panier_title.setText(QCoreApplication.translate("PageAccueil", u"PANIER MOYEN", None))
        self.kpi_panier_value.setText(QCoreApplication.translate("PageAccueil", u"\u2014", None))
        self.kpi_panier_trend.setText("")
        self.kpi_panier_sub.setText("")
        self.kpi_clients_icon.setText("")
        self.kpi_clients_title.setText(QCoreApplication.translate("PageAccueil", u"CLIENTS SERVIS", None))
        self.kpi_clients_value.setText(QCoreApplication.translate("PageAccueil", u"\u2014", None))
        self.kpi_clients_trend.setText("")
        self.kpi_clients_sub.setText("")
        self.kpi_ruptures_icon.setText("")
        self.kpi_ruptures_title.setText(QCoreApplication.translate("PageAccueil", u"RUPTURES", None))
        self.kpi_ruptures_value.setText(QCoreApplication.translate("PageAccueil", u"\u2014", None))
        self.kpi_ruptures_trend.setText("")
        self.kpi_ruptures_sub.setText("")
        self.lbl_top5_icon.setText("")
        self.lbl_top5_title.setText(QCoreApplication.translate("PageAccueil", u"Top 5 produits", None))
        self.lbl_alertes_icon.setText("")
        self.lbl_alertes_title.setText(QCoreApplication.translate("PageAccueil", u"Points d'attention", None))
        self.lbl_alertes_count.setText(QCoreApplication.translate("PageAccueil", u"0", None))
        self.blk_stock_title.setText(QCoreApplication.translate("PageAccueil", u"VALEUR DU STOCK", None))
        self.blk_stock_value.setText(QCoreApplication.translate("PageAccueil", u"\u2014", None))
        self.blk_marge_title.setText(QCoreApplication.translate("PageAccueil", u"MARGE ESTIM\u00c9E", None))
        self.blk_marge_value.setText(QCoreApplication.translate("PageAccueil", u"\u2014", None))
        self.blk_annul_title.setText(QCoreApplication.translate("PageAccueil", u"VENTES ANNUL\u00c9ES", None))
        self.blk_annul_value.setText(QCoreApplication.translate("PageAccueil", u"\u2014", None))
        pass
    # retranslateUi

