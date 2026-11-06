# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_blf_dialogEtHKcC.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1200, 780)
        Dialog.setMinimumSize(QSize(1100, 700))
        Dialog.setStyleSheet(u"/* ============================================================\n"
"   NOVA PHARMA \u2014 DIALOG BLF\n"
"   ============================================================ */\n"
"\n"
"QDialog { background-color: #f0f4f8; }\n"
"\n"
"QWidget {\n"
"    font-family: \"Segoe UI\", \"Inter\", \"Roboto\", sans-serif;\n"
"    font-size: 13px;\n"
"    color: #0f172a;\n"
"    outline: none;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 PANNEAU CATALOGUE (gauche) \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#panel_catalogue {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 18px;\n"
"}\n"
"QLabel#catalogue_title {\n"
"    color: #0f172a;\n"
"    font-size: 16px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#catalogue_subtitle {\n"
"    color: #94a3b8;\n"
"    font-size: 11px;\n"
"    background: transparent;\n"
"}\n"
"QLineEdit#search_produit {\n"
"    background-color: #f8fafc;\n"
"    bor"
                        "der: 1.5px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 10px 14px;\n"
"    font-size: 13px;\n"
"    color: #0f172a;\n"
"}\n"
"QLineEdit#search_produit:focus {\n"
"    background-color: #ffffff;\n"
"    border-color: #0077B6;\n"
"}\n"
"QTableWidget#table_produits {\n"
"    background-color: #ffffff;\n"
"    alternate-background-color: #fbfcfe;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 10px;\n"
"    gridline-color: transparent;\n"
"    outline: none;\n"
"    color: #334155;\n"
"}\n"
"QTableWidget#table_produits::item {\n"
"    padding: 8px 6px;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"}\n"
"QTableWidget#table_produits::item:selected {\n"
"    background-color: #eff6ff;\n"
"    color: #0077B6;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #f8fafc;\n"
"    color: #94a3b8;\n"
"    padding: 10px 8px;\n"
"    border: none;\n"
"    border-bottom: 2px solid #e6ebf2;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
"/* \u2550\u2550"
                        "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 PANNEAU BLF (droite) \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#panel_blf {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"QFrame#blf_header {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:0.4 #0077B6, stop:1 #00B4D8);\n"
"    border-top-left-radius: 18px;\n"
"    border-top-right-radius: 18px;\n"
"    border: none;\n"
"}\n"
"QLabel#blf_header_title {\n"
"    color: #ffffff;\n"
"    font-size: 20px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#blf_header_subtitle {\n"
"    color: #CAF0F8;\n"
"    font-size: 12px;\n"
"    background: transparent;\n"
"}\n"
"QLabel#blf_header_icon {\n"
"    background-color: rgba(255,255,255,0.15);\n"
"    border: 1px solid rgba(255,255,255,0.25);\n"
"    border-radius: 14px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"/* Champs */\n"
"QLabel#field_label {\n"
"   "
                        " color: #64748b;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 0.5px;\n"
"    background: transparent;\n"
"}\n"
"QComboBox#combo_fournisseur,\n"
"QLineEdit#edit_ref_externe,\n"
"QLineEdit#edit_notes {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 10px 14px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"QComboBox#combo_fournisseur:focus,\n"
"QLineEdit#edit_ref_externe:focus,\n"
"QLineEdit#edit_notes:focus {\n"
"    background-color: #ffffff;\n"
"    border-color: #0077B6;\n"
"}\n"
"QComboBox#combo_fournisseur::drop-down { border: none; width: 26px; }\n"
"QComboBox#combo_fournisseur::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    selection-background-color: "
                        "#eff6ff;\n"
"    selection-color: #0077B6;\n"
"}\n"
"\n"
"/* Zone scrollable lignes */\n"
"QScrollArea#scroll_lignes {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"QWidget#scroll_content {\n"
"    background-color: transparent;\n"
"}\n"
"QLabel#label_empty {\n"
"    color: #94a3b8;\n"
"    font-size: 12px;\n"
"    font-style: italic;\n"
"    background-color: #fbfcfe;\n"
"    border: 1px dashed #dbe3ec;\n"
"    border-radius: 12px;\n"
"    padding: 30px;\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}\n"
"\n"
"/* Totaux */\n"
"QFrame#total_box {\n"
"    background-color: #eff6ff;\n"
"    border: 1.5px solid #dbeafe;\n"
"    border-left: 4px solid #0077B6;\n"
"    border-radius: 12px;\n"
"}\n"
"QLabel#label_nb_articles {\n"
"    color: #1e40af;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    background: transparent;\n"
"}\n"
"QLabel#label_total_caption {\n"
"    color: #1e40af;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QL"
                        "abel#label_total_value {\n"
"    color: #023E8A;\n"
"    font-size: 18px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* Footer */\n"
"QFrame#blf_footer {\n"
"    background-color: #f8fafc;\n"
"    border-top: 1px solid #eef2f7;\n"
"    border-bottom-left-radius: 18px;\n"
"    border-bottom-right-radius: 18px;\n"
"}\n"
"\n"
"QPushButton#btn_cancel {\n"
"    background-color: #ffffff;\n"
"    color: #64748b;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 10px 24px;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"    min-width: 110px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_cancel:hover {\n"
"    background-color: #fef2f2;\n"
"    color: #dc2626;\n"
"    border-color: #fecaca;\n"
"}\n"
"\n"
"QPushButton#btn_draft {\n"
"    background-color: #ffffff;\n"
"    color: #0077B6;\n"
"    border: 1.5px solid #bae6fd;\n"
"    border-radius: 10px;\n"
"    padding: 10px 22px;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    min-h"
                        "eight: 42px;\n"
"}\n"
"QPushButton#btn_draft:hover { background-color: #eff6ff; }\n"
"\n"
"QPushButton#btn_validate {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 10px 28px;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    min-width: 220px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_validate:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"\n"
"/* Scrollbar */\n"
"QScrollBar:vertical {\n"
"    border: none; background: transparent;\n"
"    width: 10px; margin: 2px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #cbd5e1; min-height: 32px; border-radius: 5px;\n"
"}\n"
"QScrollBar::handle:vertical:hover { background: #94a3b8; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }\n"
"")
        self.root_layout = QHBoxLayout(Dialog)
        self.root_layout.setSpacing(20)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.panel_catalogue = QFrame(Dialog)
        self.panel_catalogue.setObjectName(u"panel_catalogue")
        self.panel_catalogue.setMinimumSize(QSize(420, 0))
        self.panel_catalogue.setMaximumSize(QSize(460, 16777215))
        self.panel_catalogue.setFrameShape(QFrame.Shape.NoFrame)
        self.catalogue_layout = QVBoxLayout(self.panel_catalogue)
        self.catalogue_layout.setSpacing(12)
        self.catalogue_layout.setObjectName(u"catalogue_layout")
        self.catalogue_layout.setContentsMargins(20, 20, 20, 20)
        self.catalogue_title = QLabel(self.panel_catalogue)
        self.catalogue_title.setObjectName(u"catalogue_title")

        self.catalogue_layout.addWidget(self.catalogue_title)

        self.catalogue_subtitle = QLabel(self.panel_catalogue)
        self.catalogue_subtitle.setObjectName(u"catalogue_subtitle")

        self.catalogue_layout.addWidget(self.catalogue_subtitle)

        self.search_produit = QLineEdit(self.panel_catalogue)
        self.search_produit.setObjectName(u"search_produit")
        self.search_produit.setClearButtonEnabled(True)

        self.catalogue_layout.addWidget(self.search_produit)

        self.table_produits = QTableWidget(self.panel_catalogue)
        if (self.table_produits.columnCount() < 4):
            self.table_produits.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_produits.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_produits.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_produits.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_produits.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table_produits.setObjectName(u"table_produits")
        self.table_produits.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_produits.setAlternatingRowColors(True)
        self.table_produits.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_produits.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_produits.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table_produits.setShowGrid(False)
        self.table_produits.verticalHeader().setVisible(False)
        self.table_produits.verticalHeader().setDefaultSectionSize(40)

        self.catalogue_layout.addWidget(self.table_produits)


        self.root_layout.addWidget(self.panel_catalogue)

        self.panel_blf = QFrame(Dialog)
        self.panel_blf.setObjectName(u"panel_blf")
        self.panel_blf.setFrameShape(QFrame.Shape.NoFrame)
        self.blf_layout = QVBoxLayout(self.panel_blf)
        self.blf_layout.setSpacing(0)
        self.blf_layout.setObjectName(u"blf_layout")
        self.blf_layout.setContentsMargins(0, 0, 0, 0)
        self.blf_header = QFrame(self.panel_blf)
        self.blf_header.setObjectName(u"blf_header")
        self.blf_header.setMinimumSize(QSize(0, 90))
        self.blf_header.setMaximumSize(QSize(16777215, 90))
        self.blf_header.setFrameShape(QFrame.Shape.NoFrame)
        self.blf_header_layout = QHBoxLayout(self.blf_header)
        self.blf_header_layout.setSpacing(16)
        self.blf_header_layout.setObjectName(u"blf_header_layout")
        self.blf_header_layout.setContentsMargins(28, 16, 28, 16)
        self.blf_header_icon = QLabel(self.blf_header)
        self.blf_header_icon.setObjectName(u"blf_header_icon")
        self.blf_header_icon.setMinimumSize(QSize(48, 48))
        self.blf_header_icon.setMaximumSize(QSize(48, 48))
        self.blf_header_icon.setPixmap(QPixmap(u":/Icon/Icons/package_white.svg"))
        self.blf_header_icon.setScaledContents(True)

        self.blf_header_layout.addWidget(self.blf_header_icon)

        self.blf_header_text = QVBoxLayout()
        self.blf_header_text.setSpacing(4)
        self.blf_header_text.setObjectName(u"blf_header_text")
        self.blf_header_title = QLabel(self.blf_header)
        self.blf_header_title.setObjectName(u"blf_header_title")

        self.blf_header_text.addWidget(self.blf_header_title)

        self.blf_header_subtitle = QLabel(self.blf_header)
        self.blf_header_subtitle.setObjectName(u"blf_header_subtitle")

        self.blf_header_text.addWidget(self.blf_header_subtitle)


        self.blf_header_layout.addLayout(self.blf_header_text)

        self.blf_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.blf_header_layout.addItem(self.blf_header_spacer)


        self.blf_layout.addWidget(self.blf_header)

        self.blf_content_layout = QVBoxLayout()
        self.blf_content_layout.setSpacing(14)
        self.blf_content_layout.setObjectName(u"blf_content_layout")
        self.blf_content_layout.setContentsMargins(24, 20, 24, 20)
        self.fournisseur_row = QHBoxLayout()
        self.fournisseur_row.setSpacing(12)
        self.fournisseur_row.setObjectName(u"fournisseur_row")
        self.fournisseur_layout = QVBoxLayout()
        self.fournisseur_layout.setSpacing(4)
        self.fournisseur_layout.setObjectName(u"fournisseur_layout")
        self.label_fournisseur = QLabel(self.panel_blf)
        self.label_fournisseur.setObjectName(u"label_fournisseur")
        self.label_fournisseur.setStyleSheet(u"color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")

        self.fournisseur_layout.addWidget(self.label_fournisseur)

        self.combo_fournisseur = QComboBox(self.panel_blf)
        self.combo_fournisseur.setObjectName(u"combo_fournisseur")
        self.combo_fournisseur.setMinimumSize(QSize(0, 42))

        self.fournisseur_layout.addWidget(self.combo_fournisseur)


        self.fournisseur_row.addLayout(self.fournisseur_layout)

        self.ref_layout = QVBoxLayout()
        self.ref_layout.setSpacing(4)
        self.ref_layout.setObjectName(u"ref_layout")
        self.label_ref = QLabel(self.panel_blf)
        self.label_ref.setObjectName(u"label_ref")
        self.label_ref.setStyleSheet(u"color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")

        self.ref_layout.addWidget(self.label_ref)

        self.edit_ref_externe = QLineEdit(self.panel_blf)
        self.edit_ref_externe.setObjectName(u"edit_ref_externe")
        self.edit_ref_externe.setMinimumSize(QSize(0, 42))

        self.ref_layout.addWidget(self.edit_ref_externe)


        self.fournisseur_row.addLayout(self.ref_layout)


        self.blf_content_layout.addLayout(self.fournisseur_row)

        self.label_section_produits = QLabel(self.panel_blf)
        self.label_section_produits.setObjectName(u"label_section_produits")
        self.label_section_produits.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 800; background: transparent;")

        self.blf_content_layout.addWidget(self.label_section_produits)

        self.scroll_lignes = QScrollArea(self.panel_blf)
        self.scroll_lignes.setObjectName(u"scroll_lignes")
        self.scroll_lignes.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_lignes.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_lignes.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName(u"scroll_content")
        self.scroll_content.setGeometry(QRect(0, 0, 670, 156))
        self.scroll_content.setStyleSheet(u"background-color: transparent;")
        self.verticalLayout_lignes = QVBoxLayout(self.scroll_content)
        self.verticalLayout_lignes.setSpacing(8)
        self.verticalLayout_lignes.setObjectName(u"verticalLayout_lignes")
        self.verticalLayout_lignes.setContentsMargins(0, 0, 0, 0)
        self.lignes_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_lignes.addItem(self.lignes_spacer)

        self.scroll_lignes.setWidget(self.scroll_content)

        self.blf_content_layout.addWidget(self.scroll_lignes)

        self.label_empty = QLabel(self.panel_blf)
        self.label_empty.setObjectName(u"label_empty")
        self.label_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.blf_content_layout.addWidget(self.label_empty)

        self.notes_layout = QVBoxLayout()
        self.notes_layout.setSpacing(4)
        self.notes_layout.setObjectName(u"notes_layout")
        self.label_notes = QLabel(self.panel_blf)
        self.label_notes.setObjectName(u"label_notes")
        self.label_notes.setStyleSheet(u"color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; background: transparent;")

        self.notes_layout.addWidget(self.label_notes)

        self.edit_notes = QLineEdit(self.panel_blf)
        self.edit_notes.setObjectName(u"edit_notes")
        self.edit_notes.setMinimumSize(QSize(0, 42))

        self.notes_layout.addWidget(self.edit_notes)


        self.blf_content_layout.addLayout(self.notes_layout)

        self.total_box = QFrame(self.panel_blf)
        self.total_box.setObjectName(u"total_box")
        self.total_box.setMinimumSize(QSize(0, 56))
        self.total_box.setFrameShape(QFrame.Shape.NoFrame)
        self.total_layout = QHBoxLayout(self.total_box)
        self.total_layout.setSpacing(12)
        self.total_layout.setObjectName(u"total_layout")
        self.total_layout.setContentsMargins(18, 12, 18, 12)
        self.label_nb_articles = QLabel(self.total_box)
        self.label_nb_articles.setObjectName(u"label_nb_articles")

        self.total_layout.addWidget(self.label_nb_articles)

        self.total_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.total_layout.addItem(self.total_spacer)

        self.label_total_caption = QLabel(self.total_box)
        self.label_total_caption.setObjectName(u"label_total_caption")

        self.total_layout.addWidget(self.label_total_caption)

        self.label_total_value = QLabel(self.total_box)
        self.label_total_value.setObjectName(u"label_total_value")

        self.total_layout.addWidget(self.label_total_value)


        self.blf_content_layout.addWidget(self.total_box)


        self.blf_layout.addLayout(self.blf_content_layout)

        self.blf_footer = QFrame(self.panel_blf)
        self.blf_footer.setObjectName(u"blf_footer")
        self.blf_footer.setMinimumSize(QSize(0, 80))
        self.blf_footer.setMaximumSize(QSize(16777215, 80))
        self.blf_footer.setFrameShape(QFrame.Shape.NoFrame)
        self.blf_footer_layout = QHBoxLayout(self.blf_footer)
        self.blf_footer_layout.setSpacing(10)
        self.blf_footer_layout.setObjectName(u"blf_footer_layout")
        self.blf_footer_layout.setContentsMargins(24, 0, 24, 0)
        self.footer_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.blf_footer_layout.addItem(self.footer_spacer)

        self.btn_cancel = QPushButton(self.blf_footer)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.blf_footer_layout.addWidget(self.btn_cancel)

        self.btn_draft = QPushButton(self.blf_footer)
        self.btn_draft.setObjectName(u"btn_draft")
        self.btn_draft.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.blf_footer_layout.addWidget(self.btn_draft)

        self.btn_validate = QPushButton(self.blf_footer)
        self.btn_validate.setObjectName(u"btn_validate")
        self.btn_validate.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/check-circle_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_validate.setIcon(icon)
        self.btn_validate.setIconSize(QSize(16, 16))

        self.blf_footer_layout.addWidget(self.btn_validate)


        self.blf_layout.addWidget(self.blf_footer)


        self.root_layout.addWidget(self.panel_blf)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Nouveau Bon de Livraison \u2014 Nova Pharma", None))
        self.catalogue_title.setText(QCoreApplication.translate("Dialog", u"Catalogue produits", None))
        self.catalogue_subtitle.setText(QCoreApplication.translate("Dialog", u"Double-cliquez pour ajouter au BLF", None))
        self.search_produit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Rechercher un produit\u2026", None))
        ___qtablewidgetitem = self.table_produits.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Code", None))
        ___qtablewidgetitem1 = self.table_produits.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Produit", None))
        ___qtablewidgetitem2 = self.table_produits.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Stock", None))
        ___qtablewidgetitem3 = self.table_produits.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Prix", None))
        self.blf_header_title.setText(QCoreApplication.translate("Dialog", u"Nouveau Bon de Livraison", None))
        self.blf_header_subtitle.setText(QCoreApplication.translate("Dialog", u"Cr\u00e9\u00e9 par Utilisateur \u2014 Date", None))
        self.label_fournisseur.setText(QCoreApplication.translate("Dialog", u"Fournisseur", None))
        self.label_ref.setText(QCoreApplication.translate("Dialog", u"R\u00e9f\u00e9rence facture (optionnel)", None))
        self.edit_ref_externe.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ex : FAC-F-2026-1234", None))
        self.label_section_produits.setText(QCoreApplication.translate("Dialog", u"Produits du BLF", None))
        self.label_empty.setText(QCoreApplication.translate("Dialog", u"Aucun produit dans le BLF.\n"
"Double-cliquez sur un produit \u00e0 gauche pour l'ajouter.", None))
        self.label_notes.setText(QCoreApplication.translate("Dialog", u"Notes internes (optionnel)", None))
        self.edit_notes.setPlaceholderText(QCoreApplication.translate("Dialog", u"Remarques, \u00e9tat des colis\u2026", None))
        self.label_nb_articles.setText(QCoreApplication.translate("Dialog", u"0 article(s)", None))
        self.label_total_caption.setText(QCoreApplication.translate("Dialog", u"TOTAL :", None))
        self.label_total_value.setText(QCoreApplication.translate("Dialog", u"0 FC", None))
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"Annuler", None))
        self.btn_draft.setText(QCoreApplication.translate("Dialog", u"Enregistrer en brouillon", None))
        self.btn_validate.setText(QCoreApplication.translate("Dialog", u"Valider et mettre \u00e0 jour le stock", None))
    # retranslateUi

