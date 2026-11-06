# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_page_facturationzXNVpW.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QFormLayout,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_PageFacturation(object):
    def setupUi(self, PageFacturation):
        if not PageFacturation.objectName():
            PageFacturation.setObjectName(u"PageFacturation")
        PageFacturation.resize(935, 727)
        PageFacturation.setStyleSheet(u"/* \U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\n"
"   PAGE FACTURATION \U00002014 NOVA PHARMA POS v6 (10/10 Responsive)\n"
"   Philosophie : Vitesse caissier \U000000b7 Responsive strict \U000000b7 Z\U000000e9ro friction\n"
"   \U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550"
                        "\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550\U00002550 */\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 BASE \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#PageFacturation { background-color: #f1f5f9; }\n"
"#PageFacturation QLabel { background: transparent; color: #0f172a; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 HEADER \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#frame_page_header {\n"
"    background-color: qlineargradient(spr"
                        "ead:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1e40af, stop:0.5 #2563eb, stop:1 #4f46e5);\n"
"    border: none; border-radius: 16px;\n"
"}\n"
"#frame_page_header QLabel { background: transparent; color: #ffffff; }\n"
"#ico_page_header { image: url(:/Icon/Icons/receipt_white.svg); background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.35); border-radius: 12px; padding: 8px; }\n"
"#label_23 { color: #ffffff; }\n"
"#label_23_date { color: rgba(255,255,255,0.75); font-size: 11px; font-weight: 500; }\n"
"#badge_mode_vente { background: rgba(255,255,255,0.22); color: #ffffff; border: 1px solid rgba(255,255,255,0.45); border-radius: 20px; padding: 6px 14px; font-size: 10px; font-weight: 800; letter-spacing: 1.2px; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 CARTES \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#frame_13, #frame_12, #frame_bottom_actions {\n"
"    background-color: #ffffff; borde"
                        "r: 1px solid #e2e8f0; border-radius: 16px;\n"
"}\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 IC\U000000d4NES DE SECTION \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#ico_card_articles, #ico_card_panier, #ico_card_client, #ico_card_client_info, #ico_card_resume { border-radius: 8px; padding: 5px; }\n"
"#ico_card_articles { image: url(:/Icon/Icons/pill.svg); background: #eff6ff; border: 1px solid #dbeafe; }\n"
"#ico_card_panier { image: url(:/Icon/Icons/shopping-cart.svg); background: #eff6ff; border: 1px solid #dbeafe; }\n"
"#ico_card_client { image: url(:/Icon/Icons/user.svg); background: #eff6ff; border: 1px solid #dbeafe; }\n"
"#ico_card_client_info { image: url(:/Icon/Icons/user-check.svg); background: #f0fdf4; border: 1px solid #bbf7d0; }\n"
"#ico_card_resume { image: url(:/Icon/Icons/dollar.svg); background: #f0fdf4; border: 1px solid #bbf7d0; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500"
                        "\U00002500\U00002500\U00002500\U00002500\U00002500 TITRES \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#label_4, #label_8, #label_24, #label_37, #label_panier_title { color: #0f172a; font-size: 14px; font-weight: 800; letter-spacing: -0.2px; }\n"
"#label_panier_title { font-size: 15px; }\n"
"#label_7, #label_21, #label_22, #label_31, #label_38, #label_39 { color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1.2px; text-transform: uppercase; }\n"
"#label_27 { color: #94a3b8; font-size: 11px; font-weight: 600; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 CHAMPS (RESPONSIVE) \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#edit_name_client, #edit_identification_client, #edit_numero_client, #spin_quantite_facture, #spin_nbr_stock {\n"
"    background-color: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 10px;\n"
"    padding: 10px 14"
                        "px; color: #0f172a; font-size: 13px; font-weight: 500; min-height: 22px;\n"
"}\n"
"/* \U0001f31f Zone de Scan/Recherche : Mise en \U000000e9vidence maximale */\n"
"#edit_recherche_produit {\n"
"    background-color: #ffffff; border: 2px solid #bfdbfe; border-radius: 12px;\n"
"    padding: 12px 16px; color: #0f172a; font-size: 15px; font-weight: 600; min-height: 24px;\n"
"}\n"
"#edit_recherche_produit:hover, #edit_name_client:hover, #spin_quantite_facture:hover { border-color: #94a3b8; background-color: #ffffff; }\n"
"#edit_recherche_produit:focus, #edit_name_client:focus, #spin_quantite_facture:focus { border: 2px solid #2563eb; background-color: #ffffff; }\n"
"#edit_identification_client, #edit_numero_client, #spin_nbr_stock { background-color: #f1f5f9; color: #64748b; border-color: #e2e8f0; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 BOUTONS PRINCIPAUX \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
""
                        "#btn_add_produit_for_facture, #btn_recheche_person_facture {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #3b82f6, stop:1 #2563eb);\n"
"    color: #ffffff; border: none; border-radius: 10px; padding: 10px 20px; font-size: 13px; font-weight: 800; min-height: 22px;\n"
"}\n"
"#btn_add_produit_for_facture:hover, #btn_recheche_person_facture:hover { background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #2563eb, stop:1 #1d4ed8); }\n"
"#btn_register_new_client { background: #f0fdf4; color: #15803d; border: 1.5px solid #bbf7d0; border-radius: 10px; padding: 10px 16px; font-size: 12px; font-weight: 700; min-height: 22px; }\n"
"#btn_register_new_client:hover { background: #dcfce7; border-color: #86efac; }\n"
"\n"
"/* \U0001f31f Bouton Imprimer/Valider : G\U000000e9ant et accessible */\n"
"#btn_print_facture {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #16a34a, stop:1 #15803d);\n"
"    color: #ffffff; border: none; border-radius: 14px;"
                        " padding: 16px 20px; font-size: 16px; font-weight: 800; letter-spacing: 0.3px; min-height: 26px;\n"
"}\n"
"#btn_print_facture:hover { background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #15803d, stop:1 #166534); }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 BOUTONS SECONDAIRES (TOOLBAR) \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#btn_remove_line_facture, #btn_clear_table_facture, #btn_mes_ventes_jour, #btn_rapport_z {\n"
"    background: #f8fafc; color: #475569; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 16px; font-size: 12px; font-weight: 700;\n"
"}\n"
"#btn_remove_line_facture { color: #dc2626; border-color: #fecaca; }\n"
"#btn_remove_line_facture:hover { background: #fef2f2; border-color: #fca5a5; }\n"
"#btn_mes_ventes_jour { color: #1d4ed8; border-color: #bfdbfe; }\n"
"#btn_mes_ventes_jour:hover { background: #eff6ff; border-color: #93c5fd; }\n"
"#btn_rappo"
                        "rt_z { color: #92400e; border-color: #fde68a; }\n"
"#btn_rapport_z:hover { background: #fefce8; border-color: #fcd34d; }\n"
"#btn_clear_table_facture:hover { background: #f1f5f9; border-color: #cbd5e1; color: #0f172a; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 TABLE PANIER \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#tableWidget { background-color: transparent; border: none; outline: none; font-size: 13px; font-weight: 500; }\n"
"#tableWidget::item { padding: 14px 12px; border-bottom: 1px solid #f1f5f9; color: #334155; }\n"
"#tableWidget::item:hover { background-color: #f8fafc; }\n"
"#tableWidget::item:selected { background-color: #eff6ff; color: #1d4ed8; border-left: 4px solid #2563eb; }\n"
"#tableWidget QHeaderView::section { background-color: #f8fafc; color: #94a3b8; padding: 12px; border: none; border-bottom: 2px solid #e6ebf2; font-size: 10px; font-weight: 800; letter-spacing: 1.2px; text-tr"
                        "ansform: uppercase; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 TOTAUX \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#lbl_total_nbr_produit { color: #0f172a; font-size: 18px; font-weight: 800; }\n"
"#lbl_totale_calc { color: #16a34a; font-size: 36px; font-weight: 900; letter-spacing: -1px; }\n"
"#label_25, #label_28 { color: #64748b; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 S\U000000c9PARATEURS \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"#PageFacturation QFrame[frameShape=\"4\"], #PageFacturation Line { background-color: #f1f5f9; border: none; max-height: 1px; }\n"
"\n"
"/* \U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 SCROLLBARS \U00002500\U00002500\U00002500"
                        "\U00002500\U00002500\U00002500\U00002500\U00002500\U00002500 */\n"
"QScrollBar:vertical { border: none; background: transparent; width: 6px; margin: 2px; }\n"
"QScrollBar::handle:vertical { background: #e2e8f0; min-height: 36px; border-radius: 3px; }\n"
"QScrollBar::handle:vertical:hover { background: #94a3b8; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }\n"
"")
        self.root_layout = QVBoxLayout(PageFacturation)
        self.root_layout.setSpacing(10)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_page_header = QFrame(PageFacturation)
        self.frame_page_header.setObjectName(u"frame_page_header")
        self.frame_page_header.setMinimumSize(QSize(0, 72))
        self.frame_page_header.setMaximumSize(QSize(16777215, 72))
        self.header_layout = QHBoxLayout(self.frame_page_header)
        self.header_layout.setSpacing(14)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(20, 12, 20, 12)
        self.ico_page_header = QLabel(self.frame_page_header)
        self.ico_page_header.setObjectName(u"ico_page_header")
        self.ico_page_header.setMinimumSize(QSize(44, 44))
        self.ico_page_header.setMaximumSize(QSize(44, 44))

        self.header_layout.addWidget(self.ico_page_header)

        self.header_info_layout = QVBoxLayout()
        self.header_info_layout.setSpacing(1)
        self.header_info_layout.setObjectName(u"header_info_layout")
        self.label_23 = QLabel(self.frame_page_header)
        self.label_23.setObjectName(u"label_23")

        self.header_info_layout.addWidget(self.label_23)

        self.label_23_date = QLabel(self.frame_page_header)
        self.label_23_date.setObjectName(u"label_23_date")

        self.header_info_layout.addWidget(self.label_23_date)


        self.header_layout.addLayout(self.header_info_layout)

        self.header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_layout.addItem(self.header_spacer)

        self.badge_mode_vente = QLabel(self.frame_page_header)
        self.badge_mode_vente.setObjectName(u"badge_mode_vente")

        self.header_layout.addWidget(self.badge_mode_vente)


        self.root_layout.addWidget(self.frame_page_header)

        self.main_content_layout = QHBoxLayout()
        self.main_content_layout.setSpacing(10)
        self.main_content_layout.setObjectName(u"main_content_layout")
        self.left_column = QVBoxLayout()
        self.left_column.setSpacing(12)
        self.left_column.setObjectName(u"left_column")
        self.frame_13 = QFrame(PageFacturation)
        self.frame_13.setObjectName(u"frame_13")
        self.verticalLayout_29 = QVBoxLayout(self.frame_13)
        self.verticalLayout_29.setSpacing(12)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(18, 16, 18, 16)
        self.header_articles_layout = QHBoxLayout()
        self.header_articles_layout.setObjectName(u"header_articles_layout")
        self.ico_card_articles = QLabel(self.frame_13)
        self.ico_card_articles.setObjectName(u"ico_card_articles")
        self.ico_card_articles.setMinimumSize(QSize(26, 26))
        self.ico_card_articles.setMaximumSize(QSize(26, 26))

        self.header_articles_layout.addWidget(self.ico_card_articles)

        self.label_8 = QLabel(self.frame_13)
        self.label_8.setObjectName(u"label_8")

        self.header_articles_layout.addWidget(self.label_8)

        self.spacer_header_articles = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_articles_layout.addItem(self.spacer_header_articles)


        self.verticalLayout_29.addLayout(self.header_articles_layout)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(10)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.edit_recherche_produit = QLineEdit(self.frame_13)
        self.edit_recherche_produit.setObjectName(u"edit_recherche_produit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_recherche_produit.sizePolicy().hasHeightForWidth())
        self.edit_recherche_produit.setSizePolicy(sizePolicy)
        self.edit_recherche_produit.setMinimumSize(QSize(0, 46))
        self.edit_recherche_produit.setClearButtonEnabled(True)

        self.horizontalLayout_8.addWidget(self.edit_recherche_produit, 0, Qt.AlignmentFlag.AlignBottom)

        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setSpacing(4)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.label_22 = QLabel(self.frame_13)
        self.label_22.setObjectName(u"label_22")

        self.verticalLayout_18.addWidget(self.label_22)

        self.spin_quantite_facture = QSpinBox(self.frame_13)
        self.spin_quantite_facture.setObjectName(u"spin_quantite_facture")
        self.spin_quantite_facture.setMinimumSize(QSize(45, 46))
        self.spin_quantite_facture.setMaximumSize(QSize(90, 16777215))
        self.spin_quantite_facture.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_quantite_facture.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spin_quantite_facture.setMaximum(999999)
        self.spin_quantite_facture.setValue(1)

        self.verticalLayout_18.addWidget(self.spin_quantite_facture)


        self.horizontalLayout_8.addLayout(self.verticalLayout_18)

        self.verticalLayout_37 = QVBoxLayout()
        self.verticalLayout_37.setSpacing(4)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.label_31 = QLabel(self.frame_13)
        self.label_31.setObjectName(u"label_31")

        self.verticalLayout_37.addWidget(self.label_31)

        self.spin_nbr_stock = QSpinBox(self.frame_13)
        self.spin_nbr_stock.setObjectName(u"spin_nbr_stock")
        self.spin_nbr_stock.setEnabled(False)
        self.spin_nbr_stock.setMinimumSize(QSize(45, 46))
        self.spin_nbr_stock.setMaximumSize(QSize(90, 16777215))
        self.spin_nbr_stock.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_nbr_stock.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spin_nbr_stock.setMaximum(999999)
        self.spin_nbr_stock.setValue(0)

        self.verticalLayout_37.addWidget(self.spin_nbr_stock)


        self.horizontalLayout_8.addLayout(self.verticalLayout_37)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setSpacing(4)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.lbl_placeholder_add = QLabel(self.frame_13)
        self.lbl_placeholder_add.setObjectName(u"lbl_placeholder_add")
        self.lbl_placeholder_add.setStyleSheet(u"color: transparent;")

        self.verticalLayout_19.addWidget(self.lbl_placeholder_add)

        self.btn_add_produit_for_facture = QPushButton(self.frame_13)
        self.btn_add_produit_for_facture.setObjectName(u"btn_add_produit_for_facture")
        self.btn_add_produit_for_facture.setMinimumSize(QSize(120, 46))
        self.btn_add_produit_for_facture.setMaximumSize(QSize(120, 16777215))
        self.btn_add_produit_for_facture.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/add-svgrepo-com_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_add_produit_for_facture.setIcon(icon)

        self.verticalLayout_19.addWidget(self.btn_add_produit_for_facture)


        self.horizontalLayout_8.addLayout(self.verticalLayout_19)

        self.horizontalLayout_8.setStretch(0, 1)

        self.verticalLayout_29.addLayout(self.horizontalLayout_8)

        self.header_panier_layout = QHBoxLayout()
        self.header_panier_layout.setObjectName(u"header_panier_layout")
        self.header_panier_layout.setContentsMargins(-1, 8, -1, -1)
        self.ico_card_panier = QLabel(self.frame_13)
        self.ico_card_panier.setObjectName(u"ico_card_panier")
        self.ico_card_panier.setMinimumSize(QSize(26, 26))
        self.ico_card_panier.setMaximumSize(QSize(26, 26))

        self.header_panier_layout.addWidget(self.ico_card_panier)

        self.label_panier_title = QLabel(self.frame_13)
        self.label_panier_title.setObjectName(u"label_panier_title")

        self.header_panier_layout.addWidget(self.label_panier_title)

        self.spacer_header_panier = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_panier_layout.addItem(self.spacer_header_panier)


        self.verticalLayout_29.addLayout(self.header_panier_layout)

        self.tableWidget = QTableWidget(self.frame_13)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(140)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(48)

        self.verticalLayout_29.addWidget(self.tableWidget)


        self.left_column.addWidget(self.frame_13)

        self.frame_bottom_actions = QFrame(PageFacturation)
        self.frame_bottom_actions.setObjectName(u"frame_bottom_actions")
        self.frame_bottom_actions.setMinimumSize(QSize(0, 60))
        self.frame_bottom_actions.setMaximumSize(QSize(16777215, 60))
        self.layout_bottom_actions = QHBoxLayout(self.frame_bottom_actions)
        self.layout_bottom_actions.setSpacing(10)
        self.layout_bottom_actions.setObjectName(u"layout_bottom_actions")
        self.layout_bottom_actions.setContentsMargins(12, 8, 12, 8)
        self.btn_remove_line_facture = QPushButton(self.frame_bottom_actions)
        self.btn_remove_line_facture.setObjectName(u"btn_remove_line_facture")
        self.btn_remove_line_facture.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layout_bottom_actions.addWidget(self.btn_remove_line_facture)

        self.btn_clear_table_facture = QPushButton(self.frame_bottom_actions)
        self.btn_clear_table_facture.setObjectName(u"btn_clear_table_facture")
        self.btn_clear_table_facture.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layout_bottom_actions.addWidget(self.btn_clear_table_facture)

        self.spacer_bottom = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layout_bottom_actions.addItem(self.spacer_bottom)

        self.btn_mes_ventes_jour = QPushButton(self.frame_bottom_actions)
        self.btn_mes_ventes_jour.setObjectName(u"btn_mes_ventes_jour")
        self.btn_mes_ventes_jour.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layout_bottom_actions.addWidget(self.btn_mes_ventes_jour)

        self.btn_rapport_z = QPushButton(self.frame_bottom_actions)
        self.btn_rapport_z.setObjectName(u"btn_rapport_z")
        self.btn_rapport_z.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layout_bottom_actions.addWidget(self.btn_rapport_z)


        self.left_column.addWidget(self.frame_bottom_actions)

        self.left_column.setStretch(0, 1)

        self.main_content_layout.addLayout(self.left_column)

        self.frame_12 = QFrame(PageFacturation)
        self.frame_12.setObjectName(u"frame_12")
        self.verticalLayout_28 = QVBoxLayout(self.frame_12)
        self.verticalLayout_28.setSpacing(16)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_client_search = QVBoxLayout()
        self.verticalLayout_client_search.setSpacing(6)
        self.verticalLayout_client_search.setObjectName(u"verticalLayout_client_search")
        self.header_client_layout = QHBoxLayout()
        self.header_client_layout.setObjectName(u"header_client_layout")
        self.ico_card_client = QLabel(self.frame_12)
        self.ico_card_client.setObjectName(u"ico_card_client")
        self.ico_card_client.setMinimumSize(QSize(26, 26))
        self.ico_card_client.setMaximumSize(QSize(26, 26))

        self.header_client_layout.addWidget(self.ico_card_client)

        self.label_4 = QLabel(self.frame_12)
        self.label_4.setObjectName(u"label_4")

        self.header_client_layout.addWidget(self.label_4)

        self.spacer_header_client = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_client_layout.addItem(self.spacer_header_client)


        self.verticalLayout_client_search.addLayout(self.header_client_layout)

        self.label_7 = QLabel(self.frame_12)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_client_search.addWidget(self.label_7)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setSpacing(8)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.edit_name_client = QLineEdit(self.frame_12)
        self.edit_name_client.setObjectName(u"edit_name_client")
        self.edit_name_client.setMinimumSize(QSize(0, 46))
        self.edit_name_client.setClearButtonEnabled(True)

        self.horizontalLayout_16.addWidget(self.edit_name_client)

        self.btn_recheche_person_facture = QPushButton(self.frame_12)
        self.btn_recheche_person_facture.setObjectName(u"btn_recheche_person_facture")
        self.btn_recheche_person_facture.setMinimumSize(QSize(80, 42))
        self.btn_recheche_person_facture.setMaximumSize(QSize(80, 42))

        self.horizontalLayout_16.addWidget(self.btn_recheche_person_facture)


        self.verticalLayout_client_search.addLayout(self.horizontalLayout_16)

        self.label_27 = QLabel(self.frame_12)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_client_search.addWidget(self.label_27)

        self.btn_register_new_client = QPushButton(self.frame_12)
        self.btn_register_new_client.setObjectName(u"btn_register_new_client")
        self.btn_register_new_client.setMinimumSize(QSize(0, 46))
        self.btn_register_new_client.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_client_search.addWidget(self.btn_register_new_client)


        self.verticalLayout_28.addLayout(self.verticalLayout_client_search)

        self.line = QFrame(self.frame_12)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_28.addWidget(self.line)

        self.verticalLayout_client_details = QVBoxLayout()
        self.verticalLayout_client_details.setSpacing(8)
        self.verticalLayout_client_details.setObjectName(u"verticalLayout_client_details")
        self.header_client_info_layout = QHBoxLayout()
        self.header_client_info_layout.setObjectName(u"header_client_info_layout")
        self.ico_card_client_info = QLabel(self.frame_12)
        self.ico_card_client_info.setObjectName(u"ico_card_client_info")
        self.ico_card_client_info.setMinimumSize(QSize(26, 26))
        self.ico_card_client_info.setMaximumSize(QSize(26, 26))

        self.header_client_info_layout.addWidget(self.ico_card_client_info)

        self.label_37 = QLabel(self.frame_12)
        self.label_37.setObjectName(u"label_37")

        self.header_client_info_layout.addWidget(self.label_37)

        self.spacer_header_client_info = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_client_info_layout.addItem(self.spacer_header_client_info)


        self.verticalLayout_client_details.addLayout(self.header_client_info_layout)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(8)
        self.label_38 = QLabel(self.frame_12)
        self.label_38.setObjectName(u"label_38")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_38)

        self.edit_identification_client = QLineEdit(self.frame_12)
        self.edit_identification_client.setObjectName(u"edit_identification_client")
        self.edit_identification_client.setMinimumSize(QSize(0, 46))
        self.edit_identification_client.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.edit_identification_client)

        self.label_39 = QLabel(self.frame_12)
        self.label_39.setObjectName(u"label_39")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_39)

        self.edit_numero_client = QLineEdit(self.frame_12)
        self.edit_numero_client.setObjectName(u"edit_numero_client")
        self.edit_numero_client.setMinimumSize(QSize(0, 46))
        self.edit_numero_client.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.edit_numero_client)


        self.verticalLayout_client_details.addLayout(self.formLayout)


        self.verticalLayout_28.addLayout(self.verticalLayout_client_details)

        self.verticalSpacer_payment = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_28.addItem(self.verticalSpacer_payment)

        self.frame_payment_summary = QFrame(self.frame_12)
        self.frame_payment_summary.setObjectName(u"frame_payment_summary")
        self.frame_payment_summary.setStyleSheet(u"#frame_payment_summary { background: #f0fdf4; border: 1px solid #dcfce7; border-radius: 14px; }")
        self.layout_payment_summary = QVBoxLayout(self.frame_payment_summary)
        self.layout_payment_summary.setSpacing(8)
        self.layout_payment_summary.setObjectName(u"layout_payment_summary")
        self.layout_payment_summary.setContentsMargins(16, 16, 16, 16)
        self.header_resume_layout = QHBoxLayout()
        self.header_resume_layout.setObjectName(u"header_resume_layout")
        self.ico_card_resume = QLabel(self.frame_payment_summary)
        self.ico_card_resume.setObjectName(u"ico_card_resume")
        self.ico_card_resume.setMinimumSize(QSize(26, 26))
        self.ico_card_resume.setMaximumSize(QSize(26, 26))

        self.header_resume_layout.addWidget(self.ico_card_resume)

        self.label_24 = QLabel(self.frame_payment_summary)
        self.label_24.setObjectName(u"label_24")

        self.header_resume_layout.addWidget(self.label_24)

        self.spacer_header_resume = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_resume_layout.addItem(self.spacer_header_resume)


        self.layout_payment_summary.addLayout(self.header_resume_layout)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_28 = QLabel(self.frame_payment_summary)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_15.addWidget(self.label_28)

        self.spacer_nbr = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.spacer_nbr)

        self.lbl_total_nbr_produit = QLabel(self.frame_payment_summary)
        self.lbl_total_nbr_produit.setObjectName(u"lbl_total_nbr_produit")
        self.lbl_total_nbr_produit.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.lbl_total_nbr_produit)


        self.layout_payment_summary.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_25 = QLabel(self.frame_payment_summary)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_9.addWidget(self.label_25)

        self.spacer_total = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.spacer_total)

        self.lbl_totale_calc = QLabel(self.frame_payment_summary)
        self.lbl_totale_calc.setObjectName(u"lbl_totale_calc")
        self.lbl_totale_calc.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.lbl_totale_calc)


        self.layout_payment_summary.addLayout(self.horizontalLayout_9)


        self.verticalLayout_28.addWidget(self.frame_payment_summary)

        self.btn_print_facture = QPushButton(self.frame_12)
        self.btn_print_facture.setObjectName(u"btn_print_facture")
        self.btn_print_facture.setMinimumSize(QSize(0, 58))
        self.btn_print_facture.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_28.addWidget(self.btn_print_facture)


        self.main_content_layout.addWidget(self.frame_12)

        self.main_content_layout.setStretch(0, 7)
        self.main_content_layout.setStretch(1, 3)

        self.root_layout.addLayout(self.main_content_layout)


        self.retranslateUi(PageFacturation)
        self.spin_quantite_facture.returnPressed.connect(self.btn_add_produit_for_facture.click)
        self.edit_name_client.returnPressed.connect(self.btn_recheche_person_facture.click)

        QMetaObject.connectSlotsByName(PageFacturation)
    # setupUi

    def retranslateUi(self, PageFacturation):
        PageFacturation.setWindowTitle(QCoreApplication.translate("PageFacturation", u"Facturation \u2014 Nova Pharma", None))
        self.ico_page_header.setText("")
        self.label_23.setText(QCoreApplication.translate("PageFacturation", u"<html><head/><body><p><span style=\" font-size:13pt; font-weight:800;\">Nouvelle vente</span><span style=\" font-size:10pt; font-weight:600; color:rgba(255,255,255,0.7);\">  \u00b7  FA-2026-00000</span></p></body></html>", None))
        self.label_23_date.setText(QCoreApplication.translate("PageFacturation", u"\u2014", None))
        self.badge_mode_vente.setText(QCoreApplication.translate("PageFacturation", u"\u25cf EN CAISSE", None))
        self.ico_card_articles.setText("")
        self.label_8.setText(QCoreApplication.translate("PageFacturation", u"Scanner ou rechercher un article", None))
        self.edit_recherche_produit.setPlaceholderText(QCoreApplication.translate("PageFacturation", u" Code-barres, nom du m\u00e9dicament\u2026", None))
        self.label_22.setText(QCoreApplication.translate("PageFacturation", u"Qt\u00e9", None))
        self.label_31.setText(QCoreApplication.translate("PageFacturation", u"Stock", None))
        self.lbl_placeholder_add.setText(QCoreApplication.translate("PageFacturation", u".", None))
        self.btn_add_produit_for_facture.setText(QCoreApplication.translate("PageFacturation", u"Ajouter", None))
        self.ico_card_panier.setText("")
        self.label_panier_title.setText(QCoreApplication.translate("PageFacturation", u"Panier", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageFacturation", u"D\u00e9signation", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageFacturation", u"Qt\u00e9", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageFacturation", u"P.U", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageFacturation", u"Total", None))
        self.btn_remove_line_facture.setText(QCoreApplication.translate("PageFacturation", u"\u2212 Retirer ligne", None))
        self.btn_clear_table_facture.setText(QCoreApplication.translate("PageFacturation", u"Annuler saisie", None))
        self.btn_mes_ventes_jour.setText(QCoreApplication.translate("PageFacturation", u"Mes ventes", None))
        self.btn_rapport_z.setText(QCoreApplication.translate("PageFacturation", u"Cl\u00f4ture Z", None))
        self.ico_card_client.setText("")
        self.label_4.setText(QCoreApplication.translate("PageFacturation", u"Client", None))
        self.label_7.setText(QCoreApplication.translate("PageFacturation", u"Num\u00e9ro du client", None))
        self.edit_name_client.setPlaceholderText(QCoreApplication.translate("PageFacturation", u"N\u00b0 ou vide = anonyme", None))
        self.btn_recheche_person_facture.setText(QCoreApplication.translate("PageFacturation", u"OK", None))
        self.label_27.setText(QCoreApplication.translate("PageFacturation", u"Pas encore enregistr\u00e9 ?", None))
        self.btn_register_new_client.setText(QCoreApplication.translate("PageFacturation", u"+ Cr\u00e9er ce client", None))
        self.ico_card_client_info.setText("")
        self.label_37.setText(QCoreApplication.translate("PageFacturation", u"Client retenu", None))
        self.label_38.setText(QCoreApplication.translate("PageFacturation", u"Identit\u00e9", None))
        self.label_39.setText(QCoreApplication.translate("PageFacturation", u"N\u00b0", None))
        self.ico_card_resume.setText("")
        self.label_24.setText(QCoreApplication.translate("PageFacturation", u"Paiement", None))
        self.label_28.setText(QCoreApplication.translate("PageFacturation", u"Articles", None))
        self.lbl_total_nbr_produit.setText(QCoreApplication.translate("PageFacturation", u"0", None))
        self.label_25.setText(QCoreApplication.translate("PageFacturation", u"Total", None))
        self.lbl_totale_calc.setText(QCoreApplication.translate("PageFacturation", u"0 Fc", None))
        self.btn_print_facture.setText(QCoreApplication.translate("PageFacturation", u"Imprimer && Valider", None))
    # retranslateUi

