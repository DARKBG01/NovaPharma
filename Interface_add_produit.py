# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_add_produitErWiLb.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDialog, QDoubleSpinBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1130, 910)
        Dialog.setMinimumSize(QSize(980, 720))
        Dialog.setStyleSheet(u"/* ============================================================\n"
"   NOVA PHARMA \u2014 DIALOG AJOUT PRODUIT\n"
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
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 SIDEBAR \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#sidebar {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0.7, y2:1,\n"
"        stop:0 #023E8A, stop:0.5 #0077B6, stop:1 #00B4D8);\n"
"    border: none;\n"
"    border-top-left-radius: 16px;\n"
"    border-bottom-left-radius: 16px;\n"
"}\n"
"\n"
"QLabel#brand_badge {\n"
"    color: #ffffff;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1.5px;\n"
"    background: rgba(255,255,255,0.18);\n"
""
                        "    border: 1px solid rgba(255,255,255,0.28);\n"
"    border-radius: 14px;\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QLabel#sidebar_title {\n"
"    color: #ffffff;\n"
"    font-size: 26px;\n"
"    font-weight: 800;\n"
"    letter-spacing: -0.5px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#sidebar_lead {\n"
"    color: #CAF0F8;\n"
"    font-size: 13px;\n"
"    font-weight: 400;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QFrame#check_row {\n"
"    background: rgba(255,255,255,0.10);\n"
"    border: 1px solid rgba(255,255,255,0.15);\n"
"    border-radius: 12px;\n"
"}\n"
"QFrame#check_row[done=\"true\"] {\n"
"    background: rgba(255,255,255,0.25);\n"
"    border: 1px solid rgba(255,255,255,0.40);\n"
"}\n"
"QLabel#check_text {\n"
"    color: #e0e7ff;\n"
"    font-size: 12px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"}\n"
"QFrame#check_row[done=\"true\"] QLabel#check_text {\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QLabel#progress_label {\n"
"    color: #ffffff;\n"
"    font-size:"
                        " 12px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"    min-width: 45px;\n"
"    qproperty-alignment: 'AlignRight | AlignVCenter';\n"
"}\n"
"QProgressBar#progress_bar {\n"
"    background-color: rgba(255,255,255,0.18);\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"    max-height: 10px;\n"
"    text-align: center;\n"
"}\n"
"QProgressBar#progress_bar::chunk {\n"
"    background-color: #90E0EF;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QLabel#sidebar_footer {\n"
"    color: rgba(255,255,255,0.65);\n"
"    font-size: 11px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 PANEL \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#panel {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-top-right-radius: 16px;\n"
"    border-bottom-right-radius: 16px;\n"
"}\n"
"\n"
"QLabel#panel_title {\n"
"    color: "
                        "#0f172a;\n"
"    font-size: 20px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#panel_subtitle {\n"
"    color: #64748b;\n"
"    font-size: 12px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* Section numbers */\n"
"QLabel#section_num {\n"
"    background-color: #e0f7fa;\n"
"    color: #0077B6;\n"
"    border-radius: 8px;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"    min-width: 26px;\n"
"    max-width: 26px;\n"
"    min-height: 26px;\n"
"    max-height: 26px;\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}\n"
"QLabel#section_title {\n"
"    color: #334155;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* Labels de champs */\n"
"QLabel#field_label {\n"
"    color: #334155;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    background: transparent;\n"
"}\n"
"QLabel#field_required {\n"
"    color: #dc2626;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    background: "
                        "transparent;\n"
"}\n"
"QLabel#field_opt {\n"
"    color: #0077B6;\n"
"    font-size: 10px;\n"
"    font-weight: 700;\n"
"    background-color: #e0f7fa;\n"
"    border-radius: 8px;\n"
"    padding: 2px 8px;\n"
"}\n"
"\n"
"/* Inputs */\n"
"QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 10px 14px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    selection-background-color: #bfdbfe;\n"
"}\n"
"QLineEdit:hover, QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {\n"
"    border-color: #b9c6d8;\n"
"}\n"
"QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {\n"
"    background-color: #ffffff;\n"
"    border: 1.5px solid #0077B6;\n"
"}\n"
"QLineEdit[readOnly=\"true\"], QDoubleSpinBox[readOnly=\"true\"] {\n"
"    background-color: #f1f5f9;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QComboBox::drop-down { border: none; width: 26px; }\n"
"QComboBox::dow"
                        "n-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    selection-background-color: #eff6ff;\n"
"    selection-color: #0077B6;\n"
"    outline: none;\n"
"}\n"
"\n"
"/* Compteur du nom */\n"
"QLabel#name_counter {\n"
"    color: #0077B6;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    background-color: #e0f7fa;\n"
"    border: 1px solid #bae6fd;\n"
"    border-radius: 10px;\n"
"    padding: 3px 10px;\n"
"}\n"
"\n"
"/* Aper\u00e7u code-barre */\n"
"QFrame#barcode_preview {\n"
"    background-color: #fbfcfe;\n"
"    border: 1px dashed #dbe3ec;\n"
"    border-radius: 10px;\n"
"    min-height: 44px;\n"
"    max-height: 44px;\n"
"}\n"
"QLabel#barcode_hint {\n"
"    color: #94a3b8;\n"
"    font-size: 11px;\n"
"    background: transparent;\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}\n"
"\n"
"/* T"
                        "oggle auto */\n"
"QFrame#auto_box {\n"
"    background-color: #f0f9ff;\n"
"    border: 1.5px solid #bae6fd;\n"
"    border-radius: 12px;\n"
"    min-height: 54px;\n"
"}\n"
"QFrame#auto_box[on=\"true\"] {\n"
"    background-color: #e0f7fa;\n"
"    border: 1.5px solid #00B4D8;\n"
"}\n"
"QCheckBox#auto_check {\n"
"    color: #0369a1;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    spacing: 10px;\n"
"    background: transparent;\n"
"}\n"
"QCheckBox#auto_check::indicator {\n"
"    width: 20px; height: 20px;\n"
"    border: 2px solid #bae6fd;\n"
"    border-radius: 10px;\n"
"    background-color: #ffffff;\n"
"}\n"
"QCheckBox#auto_check::indicator:checked {\n"
"    background-color: #0077B6;\n"
"    border: 2px solid #0077B6;\n"
"    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxjaXJjbGUgY3g9IjQiIGN5PSI0IiByPSIyIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==);\n"
"}\n"
"QLabel#auto_hint {\n"
"    color: #0284c7;\n"
"    font"
                        "-size: 11px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* Totaux */\n"
"QFrame#tot_buy_card {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #e6ebf2;\n"
"    border-left: 4px solid #0077B6;\n"
"    border-radius: 14px;\n"
"    min-height: 90px;\n"
"}\n"
"QFrame#tot_sell_card {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #e6ebf2;\n"
"    border-left: 4px solid #16A34A;\n"
"    border-radius: 14px;\n"
"    min-height: 90px;\n"
"}\n"
"QLabel#tot_buy_label, QLabel#tot_sell_label {\n"
"    color: #64748b;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    background: transparent;\n"
"}\n"
"QLabel#tot_buy_value {\n"
"    color: #023E8A;\n"
"    font-size: 22px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#tot_sell_value {\n"
"    color: #16A34A;\n"
"    font-size: 22px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#margin_label, QLabel#profit_label "
                        "{\n"
"    color: #64748b;\n"
"    font-size: 12px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"}\n"
"QLabel#margin_value, QLabel#profit_value {\n"
"    color: #0077B6;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* Erreur */\n"
"QLabel#label_error {\n"
"    color: #dc2626;\n"
"    font-size: 12px;\n"
"    font-weight: 600;\n"
"    background-color: #fef2f2;\n"
"    border: 1px solid #fecaca;\n"
"    border-left: 4px solid #dc2626;\n"
"    border-radius: 10px;\n"
"    padding: 10px 14px;\n"
"}\n"
"\n"
"/* Footer */\n"
"QFrame#panel_footer {\n"
"    background-color: #f8fafc;\n"
"    border-top: 1px solid #eef2f7;\n"
"    border-bottom-right-radius: 16px;\n"
"}\n"
"\n"
"QPushButton#btn_cancel {\n"
"    background-color: #ffffff;\n"
"    color: #64748b;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 12px 26px;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"    min-width: 120px;\n"
"    min-height:"
                        " 44px;\n"
"}\n"
"QPushButton#btn_cancel:hover {\n"
"    background-color: #fef2f2;\n"
"    color: #dc2626;\n"
"    border-color: #fecaca;\n"
"}\n"
"\n"
"QPushButton#btn_save {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 11px;\n"
"    padding: 12px 30px;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    min-width: 190px;\n"
"    min-height: 44px;\n"
"    letter-spacing: 0.3px;\n"
"}\n"
"QPushButton#btn_save:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"QPushButton#btn_save:pressed { background: #023E8A; }\n"
"QPushButton#btn_save:disabled { background: #cbd5e1; color: #94a3b8; }\n"
"\n"
"QPushButton#btn_gen_ref {\n"
"    background-color: #eff6ff;\n"
"    color: #0077B6;\n"
"    border: 1px solid #bae6fd;\n"
"    border-radius: 9px;\n"
"    padding: 8px 14px;\n"
"    font-size: 12px;\n"
"    font-we"
                        "ight: 700;\n"
"}\n"
"QPushButton#btn_gen_ref:hover {\n"
"    background-color: #dbeafe;\n"
"    border-color: #93c5fd;\n"
"}\n"
"\n"
"/* ScrollArea */\n"
"QScrollArea {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"QScrollArea > QWidget > QWidget {\n"
"    background-color: #ffffff;\n"
"}\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 2px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #cbd5e1;\n"
"    min-height: 32px;\n"
"    border-radius: 5px;\n"
"}\n"
"QScrollBar::handle:vertical:hover { background: #94a3b8; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px; background: transparent;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: transparent;\n"
"}\n"
"")
        self.root_layout = QHBoxLayout(Dialog)
        self.root_layout.setSpacing(0)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.sidebar = QFrame(Dialog)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(320, 0))
        self.sidebar.setMaximumSize(QSize(320, 16777215))
        self.sidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setSpacing(14)
        self.sidebar_layout.setObjectName(u"sidebar_layout")
        self.sidebar_layout.setContentsMargins(32, 36, 32, 28)
        self.brand_badge = QLabel(self.sidebar)
        self.brand_badge.setObjectName(u"brand_badge")
        self.brand_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebar_layout.addWidget(self.brand_badge)

        self.side_spacer_1 = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebar_layout.addItem(self.side_spacer_1)

        self.sidebar_title = QLabel(self.sidebar)
        self.sidebar_title.setObjectName(u"sidebar_title")
        self.sidebar_title.setWordWrap(True)

        self.sidebar_layout.addWidget(self.sidebar_title)

        self.sidebar_lead = QLabel(self.sidebar)
        self.sidebar_lead.setObjectName(u"sidebar_lead")
        self.sidebar_lead.setWordWrap(True)

        self.sidebar_layout.addWidget(self.sidebar_lead)

        self.side_spacer_2 = QSpacerItem(0, 16, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebar_layout.addItem(self.side_spacer_2)

        self.check_row_code = QFrame(self.sidebar)
        self.check_row_code.setObjectName(u"check_row_code")
        self.check_row_code.setMinimumSize(QSize(0, 42))
        self.check_row_code.setMaximumSize(QSize(16777215, 42))
        self.check_row_code.setFrameShape(QFrame.Shape.NoFrame)
        self.check_code_layout = QHBoxLayout(self.check_row_code)
        self.check_code_layout.setSpacing(10)
        self.check_code_layout.setObjectName(u"check_code_layout")
        self.check_code_layout.setContentsMargins(12, 0, 12, 0)
        self.check_code_icon = QLabel(self.check_row_code)
        self.check_code_icon.setObjectName(u"check_code_icon")
        self.check_code_icon.setMinimumSize(QSize(20, 20))
        self.check_code_icon.setMaximumSize(QSize(20, 20))
        self.check_code_icon.setPixmap(QPixmap(u":/Icon/Icons/circle_white.svg"))
        self.check_code_icon.setScaledContents(True)

        self.check_code_layout.addWidget(self.check_code_icon)

        self.check_code_text = QLabel(self.check_row_code)
        self.check_code_text.setObjectName(u"check_code_text")
        self.check_code_text.setStyleSheet(u"color: #e0e7ff; font-size: 12px; font-weight: 600; background: transparent;")

        self.check_code_layout.addWidget(self.check_code_text)

        self.code_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.check_code_layout.addItem(self.code_spacer)


        self.sidebar_layout.addWidget(self.check_row_code)

        self.check_row_name = QFrame(self.sidebar)
        self.check_row_name.setObjectName(u"check_row_name")
        self.check_row_name.setMinimumSize(QSize(0, 42))
        self.check_row_name.setMaximumSize(QSize(16777215, 42))
        self.check_row_name.setFrameShape(QFrame.Shape.NoFrame)
        self.check_name_layout = QHBoxLayout(self.check_row_name)
        self.check_name_layout.setSpacing(10)
        self.check_name_layout.setObjectName(u"check_name_layout")
        self.check_name_layout.setContentsMargins(12, 0, 12, 0)
        self.check_name_icon = QLabel(self.check_row_name)
        self.check_name_icon.setObjectName(u"check_name_icon")
        self.check_name_icon.setMinimumSize(QSize(20, 20))
        self.check_name_icon.setMaximumSize(QSize(20, 20))
        self.check_name_icon.setPixmap(QPixmap(u":/Icon/Icons/circle_white.svg"))
        self.check_name_icon.setScaledContents(True)

        self.check_name_layout.addWidget(self.check_name_icon)

        self.check_name_text = QLabel(self.check_row_name)
        self.check_name_text.setObjectName(u"check_name_text")
        self.check_name_text.setStyleSheet(u"color: #e0e7ff; font-size: 12px; font-weight: 600; background: transparent;")

        self.check_name_layout.addWidget(self.check_name_text)

        self.name_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.check_name_layout.addItem(self.name_spacer)


        self.sidebar_layout.addWidget(self.check_row_name)

        self.check_row_cat = QFrame(self.sidebar)
        self.check_row_cat.setObjectName(u"check_row_cat")
        self.check_row_cat.setMinimumSize(QSize(0, 42))
        self.check_row_cat.setMaximumSize(QSize(16777215, 42))
        self.check_row_cat.setFrameShape(QFrame.Shape.NoFrame)
        self.check_cat_layout = QHBoxLayout(self.check_row_cat)
        self.check_cat_layout.setSpacing(10)
        self.check_cat_layout.setObjectName(u"check_cat_layout")
        self.check_cat_layout.setContentsMargins(12, 0, 12, 0)
        self.check_cat_icon = QLabel(self.check_row_cat)
        self.check_cat_icon.setObjectName(u"check_cat_icon")
        self.check_cat_icon.setMinimumSize(QSize(20, 20))
        self.check_cat_icon.setMaximumSize(QSize(20, 20))
        self.check_cat_icon.setPixmap(QPixmap(u":/Icon/Icons/circle_white.svg"))
        self.check_cat_icon.setScaledContents(True)

        self.check_cat_layout.addWidget(self.check_cat_icon)

        self.check_cat_text = QLabel(self.check_row_cat)
        self.check_cat_text.setObjectName(u"check_cat_text")
        self.check_cat_text.setStyleSheet(u"color: #e0e7ff; font-size: 12px; font-weight: 600; background: transparent;")

        self.check_cat_layout.addWidget(self.check_cat_text)

        self.cat_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.check_cat_layout.addItem(self.cat_spacer)


        self.sidebar_layout.addWidget(self.check_row_cat)

        self.check_row_stock = QFrame(self.sidebar)
        self.check_row_stock.setObjectName(u"check_row_stock")
        self.check_row_stock.setMinimumSize(QSize(0, 42))
        self.check_row_stock.setMaximumSize(QSize(16777215, 42))
        self.check_row_stock.setFrameShape(QFrame.Shape.NoFrame)
        self.check_stock_layout = QHBoxLayout(self.check_row_stock)
        self.check_stock_layout.setSpacing(10)
        self.check_stock_layout.setObjectName(u"check_stock_layout")
        self.check_stock_layout.setContentsMargins(12, 0, 12, 0)
        self.check_stock_icon = QLabel(self.check_row_stock)
        self.check_stock_icon.setObjectName(u"check_stock_icon")
        self.check_stock_icon.setMinimumSize(QSize(20, 20))
        self.check_stock_icon.setMaximumSize(QSize(20, 20))
        self.check_stock_icon.setPixmap(QPixmap(u":/Icon/Icons/circle_white.svg"))
        self.check_stock_icon.setScaledContents(True)

        self.check_stock_layout.addWidget(self.check_stock_icon)

        self.check_stock_text = QLabel(self.check_row_stock)
        self.check_stock_text.setObjectName(u"check_stock_text")
        self.check_stock_text.setStyleSheet(u"color: #e0e7ff; font-size: 12px; font-weight: 600; background: transparent;")

        self.check_stock_layout.addWidget(self.check_stock_text)

        self.stock_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.check_stock_layout.addItem(self.stock_spacer)


        self.sidebar_layout.addWidget(self.check_row_stock)

        self.side_spacer_3 = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebar_layout.addItem(self.side_spacer_3)

        self.progress_layout = QHBoxLayout()
        self.progress_layout.setSpacing(12)
        self.progress_layout.setObjectName(u"progress_layout")
        self.progress_bar = QProgressBar(self.sidebar)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.progress_layout.addWidget(self.progress_bar)

        self.progress_label = QLabel(self.sidebar)
        self.progress_label.setObjectName(u"progress_label")

        self.progress_layout.addWidget(self.progress_label)


        self.sidebar_layout.addLayout(self.progress_layout)

        self.sidebar_footer = QLabel(self.sidebar)
        self.sidebar_footer.setObjectName(u"sidebar_footer")
        self.sidebar_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebar_layout.addWidget(self.sidebar_footer)


        self.root_layout.addWidget(self.sidebar)

        self.panel = QFrame(Dialog)
        self.panel.setObjectName(u"panel")
        self.panel.setFrameShape(QFrame.Shape.NoFrame)
        self.panel_layout = QVBoxLayout(self.panel)
        self.panel_layout.setSpacing(0)
        self.panel_layout.setObjectName(u"panel_layout")
        self.panel_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_header = QFrame(self.panel)
        self.panel_header.setObjectName(u"panel_header")
        self.panel_header.setMinimumSize(QSize(0, 70))
        self.panel_header.setMaximumSize(QSize(16777215, 70))
        self.panel_header.setStyleSheet(u"background-color: #ffffff; border-bottom: 1px solid #eef2f7; border-top-right-radius: 16px;")
        self.panel_header.setFrameShape(QFrame.Shape.NoFrame)
        self.panel_header_layout = QHBoxLayout(self.panel_header)
        self.panel_header_layout.setSpacing(14)
        self.panel_header_layout.setObjectName(u"panel_header_layout")
        self.panel_header_layout.setContentsMargins(28, 0, 28, 0)
        self.panel_header_icon = QLabel(self.panel_header)
        self.panel_header_icon.setObjectName(u"panel_header_icon")
        self.panel_header_icon.setMinimumSize(QSize(40, 40))
        self.panel_header_icon.setMaximumSize(QSize(40, 40))
        self.panel_header_icon.setStyleSheet(u"background-color: #e0f7fa; border-radius: 12px; padding: 9px;")
        self.panel_header_icon.setPixmap(QPixmap(u":/Icon/Icons/plus.svg"))
        self.panel_header_icon.setScaledContents(True)

        self.panel_header_layout.addWidget(self.panel_header_icon)

        self.panel_header_text = QVBoxLayout()
        self.panel_header_text.setSpacing(2)
        self.panel_header_text.setObjectName(u"panel_header_text")
        self.panel_title = QLabel(self.panel_header)
        self.panel_title.setObjectName(u"panel_title")

        self.panel_header_text.addWidget(self.panel_title)

        self.panel_subtitle = QLabel(self.panel_header)
        self.panel_subtitle.setObjectName(u"panel_subtitle")

        self.panel_header_text.addWidget(self.panel_subtitle)


        self.panel_header_layout.addLayout(self.panel_header_text)

        self.header_panel_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.panel_header_layout.addItem(self.header_panel_spacer)


        self.panel_layout.addWidget(self.panel_header)

        self.scroll_area = QScrollArea(self.panel)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName(u"scroll_content")
        self.scroll_content.setGeometry(QRect(0, 0, 758, 785))
        self.scroll_content.setStyleSheet(u"background-color: #ffffff;")
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setSpacing(18)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(28, 22, 28, 22)
        self.sec1_header = QHBoxLayout()
        self.sec1_header.setSpacing(10)
        self.sec1_header.setObjectName(u"sec1_header")
        self.sec1_num = QLabel(self.scroll_content)
        self.sec1_num.setObjectName(u"sec1_num")
        self.sec1_num.setStyleSheet(u"QLabel { background-color: #e0f7fa; color: #0077B6; border-radius: 8px; font-size: 12px; font-weight: 800; min-width: 26px; max-width: 26px; min-height: 26px; max-height: 26px; qproperty-alignment: 'AlignCenter'; }")

        self.sec1_header.addWidget(self.sec1_num)

        self.sec1_title = QLabel(self.scroll_content)
        self.sec1_title.setObjectName(u"sec1_title")
        self.sec1_title.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.sec1_header.addWidget(self.sec1_title)

        self.sec1_line = QFrame(self.scroll_content)
        self.sec1_line.setObjectName(u"sec1_line")
        self.sec1_line.setStyleSheet(u"background-color: #eef2f7; border: none; max-height: 1px; min-height: 1px;")
        self.sec1_line.setFrameShape(QFrame.Shape.HLine)

        self.sec1_header.addWidget(self.sec1_line)


        self.content_layout.addLayout(self.sec1_header)

        self.row_code = QHBoxLayout()
        self.row_code.setSpacing(14)
        self.row_code.setObjectName(u"row_code")
        self.layout_code_ref = QVBoxLayout()
        self.layout_code_ref.setSpacing(6)
        self.layout_code_ref.setObjectName(u"layout_code_ref")
        self.code_ref_label_layout = QHBoxLayout()
        self.code_ref_label_layout.setSpacing(4)
        self.code_ref_label_layout.setObjectName(u"code_ref_label_layout")
        self.lbl_code_ref = QLabel(self.scroll_content)
        self.lbl_code_ref.setObjectName(u"lbl_code_ref")
        self.lbl_code_ref.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.code_ref_label_layout.addWidget(self.lbl_code_ref)

        self.req_code = QLabel(self.scroll_content)
        self.req_code.setObjectName(u"req_code")
        self.req_code.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.code_ref_label_layout.addWidget(self.req_code)

        self.code_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.code_ref_label_layout.addItem(self.code_label_spacer)


        self.layout_code_ref.addLayout(self.code_ref_label_layout)

        self.code_ref_input_layout = QHBoxLayout()
        self.code_ref_input_layout.setSpacing(8)
        self.code_ref_input_layout.setObjectName(u"code_ref_input_layout")
        self.input_code_ref = QLineEdit(self.scroll_content)
        self.input_code_ref.setObjectName(u"input_code_ref")
        self.input_code_ref.setMinimumSize(QSize(0, 44))

        self.code_ref_input_layout.addWidget(self.input_code_ref)

        self.btn_gen_ref = QPushButton(self.scroll_content)
        self.btn_gen_ref.setObjectName(u"btn_gen_ref")
        self.btn_gen_ref.setMinimumSize(QSize(0, 0))
        self.btn_gen_ref.setMaximumSize(QSize(16777215, 44))
        self.btn_gen_ref.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.code_ref_input_layout.addWidget(self.btn_gen_ref)


        self.layout_code_ref.addLayout(self.code_ref_input_layout)


        self.row_code.addLayout(self.layout_code_ref)

        self.layout_code_barre = QVBoxLayout()
        self.layout_code_barre.setSpacing(6)
        self.layout_code_barre.setObjectName(u"layout_code_barre")
        self.barcode_label_layout = QHBoxLayout()
        self.barcode_label_layout.setSpacing(4)
        self.barcode_label_layout.setObjectName(u"barcode_label_layout")
        self.lbl_code_barre = QLabel(self.scroll_content)
        self.lbl_code_barre.setObjectName(u"lbl_code_barre")
        self.lbl_code_barre.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.barcode_label_layout.addWidget(self.lbl_code_barre)

        self.barcode_opt = QLabel(self.scroll_content)
        self.barcode_opt.setObjectName(u"barcode_opt")
        self.barcode_opt.setStyleSheet(u"color: #0077B6; font-size: 10px; font-weight: 700; background: #e0f7fa; border-radius: 8px; padding: 2px 8px;")

        self.barcode_label_layout.addWidget(self.barcode_opt)

        self.barcode_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.barcode_label_layout.addItem(self.barcode_label_spacer)


        self.layout_code_barre.addLayout(self.barcode_label_layout)

        self.input_code_barre = QLineEdit(self.scroll_content)
        self.input_code_barre.setObjectName(u"input_code_barre")
        self.input_code_barre.setMinimumSize(QSize(0, 44))

        self.layout_code_barre.addWidget(self.input_code_barre)


        self.row_code.addLayout(self.layout_code_barre)


        self.content_layout.addLayout(self.row_code)

        self.barcode_preview = QFrame(self.scroll_content)
        self.barcode_preview.setObjectName(u"barcode_preview")
        self.barcode_preview.setFrameShape(QFrame.Shape.NoFrame)
        self.barcode_preview_layout = QHBoxLayout(self.barcode_preview)
        self.barcode_preview_layout.setSpacing(2)
        self.barcode_preview_layout.setObjectName(u"barcode_preview_layout")
        self.barcode_preview_layout.setContentsMargins(14, 4, 14, 4)

        self.content_layout.addWidget(self.barcode_preview)

        self.layout_nom = QVBoxLayout()
        self.layout_nom.setSpacing(6)
        self.layout_nom.setObjectName(u"layout_nom")
        self.nom_label_layout = QHBoxLayout()
        self.nom_label_layout.setSpacing(4)
        self.nom_label_layout.setObjectName(u"nom_label_layout")
        self.lbl_nom = QLabel(self.scroll_content)
        self.lbl_nom.setObjectName(u"lbl_nom")
        self.lbl_nom.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.nom_label_layout.addWidget(self.lbl_nom)

        self.req_nom = QLabel(self.scroll_content)
        self.req_nom.setObjectName(u"req_nom")
        self.req_nom.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.nom_label_layout.addWidget(self.req_nom)

        self.nom_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.nom_label_layout.addItem(self.nom_label_spacer)

        self.name_counter = QLabel(self.scroll_content)
        self.name_counter.setObjectName(u"name_counter")

        self.nom_label_layout.addWidget(self.name_counter)


        self.layout_nom.addLayout(self.nom_label_layout)

        self.input_nom = QLineEdit(self.scroll_content)
        self.input_nom.setObjectName(u"input_nom")
        self.input_nom.setMinimumSize(QSize(0, 44))
        self.input_nom.setMaxLength(120)

        self.layout_nom.addWidget(self.input_nom)


        self.content_layout.addLayout(self.layout_nom)

        self.row_cat_unite = QHBoxLayout()
        self.row_cat_unite.setSpacing(14)
        self.row_cat_unite.setObjectName(u"row_cat_unite")
        self.layout_cat = QVBoxLayout()
        self.layout_cat.setSpacing(6)
        self.layout_cat.setObjectName(u"layout_cat")
        self.cat_label_layout = QHBoxLayout()
        self.cat_label_layout.setSpacing(4)
        self.cat_label_layout.setObjectName(u"cat_label_layout")
        self.lbl_cat = QLabel(self.scroll_content)
        self.lbl_cat.setObjectName(u"lbl_cat")
        self.lbl_cat.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.cat_label_layout.addWidget(self.lbl_cat)

        self.req_cat = QLabel(self.scroll_content)
        self.req_cat.setObjectName(u"req_cat")
        self.req_cat.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.cat_label_layout.addWidget(self.req_cat)

        self.cat_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cat_label_layout.addItem(self.cat_label_spacer)


        self.layout_cat.addLayout(self.cat_label_layout)

        self.input_categorie = QComboBox(self.scroll_content)
        self.input_categorie.setObjectName(u"input_categorie")
        self.input_categorie.setMinimumSize(QSize(0, 44))

        self.layout_cat.addWidget(self.input_categorie)


        self.row_cat_unite.addLayout(self.layout_cat)

        self.layout_unite = QVBoxLayout()
        self.layout_unite.setSpacing(6)
        self.layout_unite.setObjectName(u"layout_unite")
        self.unite_label_layout = QHBoxLayout()
        self.unite_label_layout.setSpacing(4)
        self.unite_label_layout.setObjectName(u"unite_label_layout")
        self.lbl_unite = QLabel(self.scroll_content)
        self.lbl_unite.setObjectName(u"lbl_unite")
        self.lbl_unite.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.unite_label_layout.addWidget(self.lbl_unite)

        self.req_unite = QLabel(self.scroll_content)
        self.req_unite.setObjectName(u"req_unite")
        self.req_unite.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.unite_label_layout.addWidget(self.req_unite)

        self.unite_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.unite_label_layout.addItem(self.unite_label_spacer)


        self.layout_unite.addLayout(self.unite_label_layout)

        self.input_unite = QComboBox(self.scroll_content)
        self.input_unite.addItem("")
        self.input_unite.addItem("")
        self.input_unite.addItem("")
        self.input_unite.addItem("")
        self.input_unite.addItem("")
        self.input_unite.addItem("")
        self.input_unite.addItem("")
        self.input_unite.addItem("")
        self.input_unite.addItem("")
        self.input_unite.setObjectName(u"input_unite")
        self.input_unite.setMinimumSize(QSize(0, 44))

        self.layout_unite.addWidget(self.input_unite)


        self.row_cat_unite.addLayout(self.layout_unite)


        self.content_layout.addLayout(self.row_cat_unite)

        self.sec2_header = QHBoxLayout()
        self.sec2_header.setSpacing(10)
        self.sec2_header.setObjectName(u"sec2_header")
        self.sec2_num = QLabel(self.scroll_content)
        self.sec2_num.setObjectName(u"sec2_num")
        self.sec2_num.setStyleSheet(u"QLabel { background-color: #e0f7fa; color: #0077B6; border-radius: 8px; font-size: 12px; font-weight: 800; min-width: 26px; max-width: 26px; min-height: 26px; max-height: 26px; qproperty-alignment: 'AlignCenter'; }")

        self.sec2_header.addWidget(self.sec2_num)

        self.sec2_title = QLabel(self.scroll_content)
        self.sec2_title.setObjectName(u"sec2_title")
        self.sec2_title.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.sec2_header.addWidget(self.sec2_title)

        self.sec2_line = QFrame(self.scroll_content)
        self.sec2_line.setObjectName(u"sec2_line")
        self.sec2_line.setStyleSheet(u"background-color: #eef2f7; border: none; max-height: 1px; min-height: 1px;")
        self.sec2_line.setFrameShape(QFrame.Shape.HLine)

        self.sec2_header.addWidget(self.sec2_line)


        self.content_layout.addLayout(self.sec2_header)

        self.row_stock = QHBoxLayout()
        self.row_stock.setSpacing(14)
        self.row_stock.setObjectName(u"row_stock")
        self.layout_qte = QVBoxLayout()
        self.layout_qte.setSpacing(6)
        self.layout_qte.setObjectName(u"layout_qte")
        self.qte_label_layout = QHBoxLayout()
        self.qte_label_layout.setSpacing(4)
        self.qte_label_layout.setObjectName(u"qte_label_layout")
        self.lbl_qte = QLabel(self.scroll_content)
        self.lbl_qte.setObjectName(u"lbl_qte")
        self.lbl_qte.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.qte_label_layout.addWidget(self.lbl_qte)

        self.req_qte = QLabel(self.scroll_content)
        self.req_qte.setObjectName(u"req_qte")
        self.req_qte.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.qte_label_layout.addWidget(self.req_qte)

        self.qte_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.qte_label_layout.addItem(self.qte_label_spacer)


        self.layout_qte.addLayout(self.qte_label_layout)

        self.input_quantite = QSpinBox(self.scroll_content)
        self.input_quantite.setObjectName(u"input_quantite")
        self.input_quantite.setMinimumSize(QSize(0, 44))
        self.input_quantite.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.input_quantite.setMinimum(0)
        self.input_quantite.setMaximum(1000000)

        self.layout_qte.addWidget(self.input_quantite)


        self.row_stock.addLayout(self.layout_qte)

        self.layout_prix_achat = QVBoxLayout()
        self.layout_prix_achat.setSpacing(6)
        self.layout_prix_achat.setObjectName(u"layout_prix_achat")
        self.pa_label_layout = QHBoxLayout()
        self.pa_label_layout.setSpacing(4)
        self.pa_label_layout.setObjectName(u"pa_label_layout")
        self.lbl_prix_achat = QLabel(self.scroll_content)
        self.lbl_prix_achat.setObjectName(u"lbl_prix_achat")
        self.lbl_prix_achat.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.pa_label_layout.addWidget(self.lbl_prix_achat)

        self.req_pa = QLabel(self.scroll_content)
        self.req_pa.setObjectName(u"req_pa")
        self.req_pa.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.pa_label_layout.addWidget(self.req_pa)

        self.pa_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pa_label_layout.addItem(self.pa_label_spacer)


        self.layout_prix_achat.addLayout(self.pa_label_layout)

        self.input_prix_achat = QDoubleSpinBox(self.scroll_content)
        self.input_prix_achat.setObjectName(u"input_prix_achat")
        self.input_prix_achat.setMinimumSize(QSize(0, 44))
        self.input_prix_achat.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.input_prix_achat.setDecimals(2)
        self.input_prix_achat.setMaximum(999999999999999.000000000000000)

        self.layout_prix_achat.addWidget(self.input_prix_achat)


        self.row_stock.addLayout(self.layout_prix_achat)

        self.layout_prix_vente = QVBoxLayout()
        self.layout_prix_vente.setSpacing(6)
        self.layout_prix_vente.setObjectName(u"layout_prix_vente")
        self.pv_label_layout = QHBoxLayout()
        self.pv_label_layout.setSpacing(4)
        self.pv_label_layout.setObjectName(u"pv_label_layout")
        self.lbl_prix_vente = QLabel(self.scroll_content)
        self.lbl_prix_vente.setObjectName(u"lbl_prix_vente")
        self.lbl_prix_vente.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.pv_label_layout.addWidget(self.lbl_prix_vente)

        self.req_pv = QLabel(self.scroll_content)
        self.req_pv.setObjectName(u"req_pv")
        self.req_pv.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.pv_label_layout.addWidget(self.req_pv)

        self.pv_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pv_label_layout.addItem(self.pv_label_spacer)


        self.layout_prix_vente.addLayout(self.pv_label_layout)

        self.input_prix_vente = QDoubleSpinBox(self.scroll_content)
        self.input_prix_vente.setObjectName(u"input_prix_vente")
        self.input_prix_vente.setMinimumSize(QSize(0, 44))
        self.input_prix_vente.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.input_prix_vente.setDecimals(2)
        self.input_prix_vente.setMaximum(999999999999999.000000000000000)

        self.layout_prix_vente.addWidget(self.input_prix_vente)


        self.row_stock.addLayout(self.layout_prix_vente)


        self.content_layout.addLayout(self.row_stock)

        self.auto_box = QFrame(self.scroll_content)
        self.auto_box.setObjectName(u"auto_box")
        self.auto_box.setFrameShape(QFrame.Shape.NoFrame)
        self.auto_layout = QHBoxLayout(self.auto_box)
        self.auto_layout.setSpacing(12)
        self.auto_layout.setObjectName(u"auto_layout")
        self.auto_layout.setContentsMargins(16, 10, 16, 10)
        self.auto_check = QCheckBox(self.auto_box)
        self.auto_check.setObjectName(u"auto_check")
        self.auto_check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.auto_layout.addWidget(self.auto_check)

        self.auto_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.auto_layout.addItem(self.auto_spacer)

        self.auto_hint = QLabel(self.auto_box)
        self.auto_hint.setObjectName(u"auto_hint")

        self.auto_layout.addWidget(self.auto_hint)


        self.content_layout.addWidget(self.auto_box)

        self.totals_layout = QHBoxLayout()
        self.totals_layout.setSpacing(14)
        self.totals_layout.setObjectName(u"totals_layout")
        self.tot_buy_card = QFrame(self.scroll_content)
        self.tot_buy_card.setObjectName(u"tot_buy_card")
        self.tot_buy_card.setFrameShape(QFrame.Shape.NoFrame)
        self.tot_buy_layout = QVBoxLayout(self.tot_buy_card)
        self.tot_buy_layout.setSpacing(4)
        self.tot_buy_layout.setObjectName(u"tot_buy_layout")
        self.tot_buy_layout.setContentsMargins(18, 14, 18, 14)
        self.tot_buy_label = QLabel(self.tot_buy_card)
        self.tot_buy_label.setObjectName(u"tot_buy_label")

        self.tot_buy_layout.addWidget(self.tot_buy_label)

        self.tot_buy_value = QLabel(self.tot_buy_card)
        self.tot_buy_value.setObjectName(u"tot_buy_value")

        self.tot_buy_layout.addWidget(self.tot_buy_value)


        self.totals_layout.addWidget(self.tot_buy_card)

        self.tot_sell_card = QFrame(self.scroll_content)
        self.tot_sell_card.setObjectName(u"tot_sell_card")
        self.tot_sell_card.setFrameShape(QFrame.Shape.NoFrame)
        self.tot_sell_layout = QVBoxLayout(self.tot_sell_card)
        self.tot_sell_layout.setSpacing(4)
        self.tot_sell_layout.setObjectName(u"tot_sell_layout")
        self.tot_sell_layout.setContentsMargins(18, 14, 18, 14)
        self.tot_sell_label = QLabel(self.tot_sell_card)
        self.tot_sell_label.setObjectName(u"tot_sell_label")

        self.tot_sell_layout.addWidget(self.tot_sell_label)

        self.tot_sell_value = QLabel(self.tot_sell_card)
        self.tot_sell_value.setObjectName(u"tot_sell_value")

        self.tot_sell_layout.addWidget(self.tot_sell_value)


        self.totals_layout.addWidget(self.tot_sell_card)


        self.content_layout.addLayout(self.totals_layout)

        self.margin_layout = QHBoxLayout()
        self.margin_layout.setSpacing(20)
        self.margin_layout.setObjectName(u"margin_layout")
        self.margin_applied_layout = QHBoxLayout()
        self.margin_applied_layout.setSpacing(6)
        self.margin_applied_layout.setObjectName(u"margin_applied_layout")
        self.margin_label = QLabel(self.scroll_content)
        self.margin_label.setObjectName(u"margin_label")

        self.margin_applied_layout.addWidget(self.margin_label)

        self.margin_value = QLabel(self.scroll_content)
        self.margin_value.setObjectName(u"margin_value")

        self.margin_applied_layout.addWidget(self.margin_value)


        self.margin_layout.addLayout(self.margin_applied_layout)

        self.profit_layout = QHBoxLayout()
        self.profit_layout.setSpacing(6)
        self.profit_layout.setObjectName(u"profit_layout")
        self.profit_label = QLabel(self.scroll_content)
        self.profit_label.setObjectName(u"profit_label")

        self.profit_layout.addWidget(self.profit_label)

        self.profit_value = QLabel(self.scroll_content)
        self.profit_value.setObjectName(u"profit_value")

        self.profit_layout.addWidget(self.profit_value)


        self.margin_layout.addLayout(self.profit_layout)

        self.margin_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.margin_layout.addItem(self.margin_spacer)


        self.content_layout.addLayout(self.margin_layout)

        self.label_error = QLabel(self.scroll_content)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setVisible(False)
        self.label_error.setWordWrap(True)

        self.content_layout.addWidget(self.label_error)

        self.scroll_area.setWidget(self.scroll_content)

        self.panel_layout.addWidget(self.scroll_area)

        self.panel_footer = QFrame(self.panel)
        self.panel_footer.setObjectName(u"panel_footer")
        self.panel_footer.setMinimumSize(QSize(0, 80))
        self.panel_footer.setMaximumSize(QSize(16777215, 80))
        self.panel_footer.setFrameShape(QFrame.Shape.NoFrame)
        self.panel_footer_layout = QHBoxLayout(self.panel_footer)
        self.panel_footer_layout.setSpacing(10)
        self.panel_footer_layout.setObjectName(u"panel_footer_layout")
        self.panel_footer_layout.setContentsMargins(28, 0, 28, 0)
        self.footer_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.panel_footer_layout.addItem(self.footer_spacer)

        self.btn_cancel = QPushButton(self.panel_footer)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.panel_footer_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton(self.panel_footer)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.panel_footer_layout.addWidget(self.btn_save)


        self.panel_layout.addWidget(self.panel_footer)


        self.root_layout.addWidget(self.panel)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Nouveau produit \u2014 Nova Pharma", None))
        self.brand_badge.setText(QCoreApplication.translate("Dialog", u"\uff0b  NOUVELLE FICHE PRODUIT", None))
        self.sidebar_title.setText(QCoreApplication.translate("Dialog", u"Ajouter un produit", None))
        self.sidebar_lead.setText(QCoreApplication.translate("Dialog", u"Remplissez les informations pour r\u00e9f\u00e9rencer ce produit dans votre officine.", None))
        self.check_code_text.setText(QCoreApplication.translate("Dialog", u"Code r\u00e9f\u00e9rence", None))
        self.check_name_text.setText(QCoreApplication.translate("Dialog", u"Nom renseign\u00e9", None))
        self.check_cat_text.setText(QCoreApplication.translate("Dialog", u"Cat\u00e9gorie s\u00e9lectionn\u00e9e", None))
        self.check_stock_text.setText(QCoreApplication.translate("Dialog", u"Stock & prix renseign\u00e9s", None))
        self.progress_label.setText(QCoreApplication.translate("Dialog", u"0 %", None))
        self.sidebar_footer.setText(QCoreApplication.translate("Dialog", u"Nova Pharma \u2014 Gestion des produits", None))
        self.panel_title.setText(QCoreApplication.translate("Dialog", u"Fiche produit", None))
        self.panel_subtitle.setText(QCoreApplication.translate("Dialog", u"Les champs marqu\u00e9s d'une * sont obligatoires.", None))
        self.sec1_num.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.sec1_title.setText(QCoreApplication.translate("Dialog", u"INFORMATIONS DU PRODUIT", None))
        self.lbl_code_ref.setText(QCoreApplication.translate("Dialog", u"Code r\u00e9f\u00e9rence", None))
        self.req_code.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.input_code_ref.setPlaceholderText(QCoreApplication.translate("Dialog", u"MED-00001", None))
#if QT_CONFIG(tooltip)
        self.btn_gen_ref.setToolTip(QCoreApplication.translate("Dialog", u"G\u00e9n\u00e9rer un nouveau code", None))
#endif // QT_CONFIG(tooltip)
        self.btn_gen_ref.setText(QCoreApplication.translate("Dialog", u"Auto", None))
        self.lbl_code_barre.setText(QCoreApplication.translate("Dialog", u"Code-barre", None))
        self.barcode_opt.setText(QCoreApplication.translate("Dialog", u"Optionnel", None))
        self.input_code_barre.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ex : 3401234567890", None))
        self.lbl_nom.setText(QCoreApplication.translate("Dialog", u"Nom du produit", None))
        self.req_nom.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.name_counter.setText(QCoreApplication.translate("Dialog", u"0/120", None))
        self.input_nom.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ex : Doliprane 1000 mg", None))
        self.lbl_cat.setText(QCoreApplication.translate("Dialog", u"Cat\u00e9gorie", None))
        self.req_cat.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.lbl_unite.setText(QCoreApplication.translate("Dialog", u"Unit\u00e9", None))
        self.req_unite.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.input_unite.setItemText(0, QCoreApplication.translate("Dialog", u"pi\u00e8ce", None))
        self.input_unite.setItemText(1, QCoreApplication.translate("Dialog", u"comprim\u00e9", None))
        self.input_unite.setItemText(2, QCoreApplication.translate("Dialog", u"bo\u00eete", None))
        self.input_unite.setItemText(3, QCoreApplication.translate("Dialog", u"flacon", None))
        self.input_unite.setItemText(4, QCoreApplication.translate("Dialog", u"tube", None))
        self.input_unite.setItemText(5, QCoreApplication.translate("Dialog", u"sachet", None))
        self.input_unite.setItemText(6, QCoreApplication.translate("Dialog", u"ampoule", None))
        self.input_unite.setItemText(7, QCoreApplication.translate("Dialog", u"plaquette", None))
        self.input_unite.setItemText(8, QCoreApplication.translate("Dialog", u"autre", None))

        self.sec2_num.setText(QCoreApplication.translate("Dialog", u"2", None))
        self.sec2_title.setText(QCoreApplication.translate("Dialog", u"STOCK & PRIX", None))
        self.lbl_qte.setText(QCoreApplication.translate("Dialog", u"Quantit\u00e9 initiale", None))
        self.req_qte.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.input_quantite.setSuffix(QCoreApplication.translate("Dialog", u" unit\u00e9(s)", None))
        self.lbl_prix_achat.setText(QCoreApplication.translate("Dialog", u"Prix d'achat (FC)", None))
        self.req_pa.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.input_prix_achat.setSuffix(QCoreApplication.translate("Dialog", u" FC", None))
        self.lbl_prix_vente.setText(QCoreApplication.translate("Dialog", u"Prix de vente (FC)", None))
        self.req_pv.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.input_prix_vente.setSuffix(QCoreApplication.translate("Dialog", u" FC", None))
        self.auto_check.setText(QCoreApplication.translate("Dialog", u"Calculer automatiquement le prix de vente", None))
        self.auto_hint.setText(QCoreApplication.translate("Dialog", u"Marge : 30,0 %", None))
        self.tot_buy_label.setText(QCoreApplication.translate("Dialog", u"TOTAL ACHAT", None))
        self.tot_buy_value.setText(QCoreApplication.translate("Dialog", u"0,00 FC", None))
        self.tot_sell_label.setText(QCoreApplication.translate("Dialog", u"TOTAL VENTE", None))
        self.tot_sell_value.setText(QCoreApplication.translate("Dialog", u"0,00 FC", None))
        self.margin_label.setText(QCoreApplication.translate("Dialog", u"Marge appliqu\u00e9e :", None))
        self.margin_value.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.profit_label.setText(QCoreApplication.translate("Dialog", u"B\u00e9n\u00e9fice estim\u00e9 :", None))
        self.profit_value.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.label_error.setText("")
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"Annuler", None))
        self.btn_save.setText(QCoreApplication.translate("Dialog", u"\uff0b  Enregistrer le produit", None))
    # retranslateUi

