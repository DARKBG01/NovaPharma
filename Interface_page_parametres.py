# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_page_parametressIYJDy.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPlainTextEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import Icon_rc

class Ui_PageParametres(object):
    def setupUi(self, PageParametres):
        if not PageParametres.objectName():
            PageParametres.setObjectName(u"PageParametres")
        PageParametres.resize(1100, 891)
        PageParametres.setStyleSheet(u"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 BASE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QWidget#PageParametres {\n"
"    background: #f0f4f8;\n"
"}\n"
"\n"
"QWidget#PageParametres QLabel {\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 CARTE PRINCIPALE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#card {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 20px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 HEADER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#header_frame {\n"
"    background: #ffffff;\n"
"    border-top-left-radius: 20px;\n"
"    border-top-right-radius: 20px;\n"
"    border: none;"
                        "\n"
"}\n"
"\n"
"QLabel#header_icon {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"        stop:0 #0077B6, stop:1 #00B4D8);\n"
"    border-radius: 14px;\n"
"    padding: 12px;\n"
"}\n"
"\n"
"QLabel#page_title {\n"
"    color: #0f172a;\n"
"    font-size: 22px;\n"
"    font-weight: 800;\n"
"    letter-spacing: -0.3px;\n"
"}\n"
"\n"
"QLabel#page_subtitle {\n"
"    color: #64748b;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QLabel#version_badge {\n"
"    background: #eff6ff;\n"
"    color: #023E8A;\n"
"    border: 1px solid #bfdbfe;\n"
"    border-radius: 10px;\n"
"    padding: 6px 12px;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 TABS (style pill) \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QTabWidget::pane {\n"
"    background: transparent;\n"
"    border: none;\n"
"    top: 0;\n"
"}\n"
"\n"
"QTabBar {\n"
""
                        "    background: transparent;\n"
"    qproperty-drawBase: 0;\n"
"    qproperty-expanding: 1;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: transparent;\n"
"    color: #64748b;\n"
"    padding: 9px 18px;\n"
"    margin-right: 6px;\n"
"    border-radius: 10px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    border: 1px solid transparent;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: #023E8A;\n"
"    color: #ffffff;\n"
"    border-color: #023E8A;\n"
"}\n"
"\n"
"QTabBar::tab:hover:!selected {\n"
"    background: #eff6ff;\n"
"    color: #0077B6;\n"
"    border-color: #dbeafe;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 SECTIONS (cartes blanches) \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#section_card {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 14px;\n"
"}\n"
"\n"
"QFrame#section_sep {\n"
"    background: #eef2f7;\n"
"  "
                        "  border: none;\n"
"    max-height: 1px;\n"
"    min-height: 1px;\n"
"}\n"
"\n"
"QLabel#section_icon {\n"
"    background: #e0f2fe;\n"
"    color: #023E8A;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"}\n"
"\n"
"QLabel#section_title {\n"
"    color: #0f172a;\n"
"    font-size: 14px;\n"
"    font-weight: 800;\n"
"    letter-spacing: -0.1px;\n"
"}\n"
"\n"
"QLabel#section_hint {\n"
"    color: #94a3b8;\n"
"    font-size: 11px;\n"
"    font-style: italic;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 LABELS DE CHAMPS \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */ QLabel[fieldLabel=\"true\"] {\n"
"    color: #475569;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 0.2px; } QLabel[fieldHint=\"true\"] {\n"
"    color: #94a3b8;\n"
"    font-size: 10px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
                        "\u2550\u2550\u2550\u2550\u2550 CHAMPS DE SAISIE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QLineEdit,\n"
"QComboBox,\n"
"QSpinBox,\n"
"QDoubleSpinBox,\n"
"QPlainTextEdit {\n"
"    background: #ffffff;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 10px 14px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    min-height: 22px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 SPINBOX \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"/* Note : l'alignement du texte est g\u00e9r\u00e9 en Python via\n"
"   _fix_spinbox_alignment() \u2014 qproperty-alignment ne marche\n"
"   PAS sur QSpinBox en Qt6 (bug connu). */\n"
"QSpinBox,\n"
"QDoubleSpinBox {\n"
"    padding-right: 26px;\n"
"}\n"
"\n"
"QSpinBox::up-button,\n"
"QDoubleSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    sub"
                        "control-position: top right;\n"
"    width: 20px;\n"
"    border: none;\n"
"    border-top-right-radius: 8px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QSpinBox::down-button,\n"
"QDoubleSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 20px;\n"
"    border: none;\n"
"    border-bottom-right-radius: 8px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QSpinBox::up-button:hover,\n"
"QDoubleSpinBox::up-button:hover,\n"
"QSpinBox::down-button:hover,\n"
"QDoubleSpinBox::down-button:hover {\n"
"    background: #eff6ff;\n"
"}\n"
"\n"
"QSpinBox::up-arrow,\n"
"QDoubleSpinBox::up-arrow {\n"
"    image: url(:/Icon/Icons/chevron-up.svg);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow,\n"
"QDoubleSpinBox::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 COM"
                        "BOBOX \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 26px;\n"
"    border: none;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    selection-background-color: #eff6ff;\n"
"    selection-color: #0077B6;\n"
"    outline: none;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 HOVER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QLineEdit:hover,\n"
"QComboBox:hover,\n"
"QSpinBox:hover,\n"
"QDoubleSpinBox:hover,\n"
"QPlainTextEdit:hover {\n"
"    border-color: #b9c6d8;\n"
"}\n"
"\n"
"/* \u2550\u2550"
                        "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 FOCUS \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QLineEdit:focus,\n"
"QComboBox:focus,\n"
"QSpinBox:focus,\n"
"QDoubleSpinBox:focus,\n"
"QPlainTextEdit:focus {\n"
"    background: #ffffff;\n"
"    border: 1.5px solid #0077B6;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 CHECKBOX \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QCheckBox {\n"
"    color: #334155;\n"
"    font-size: 12px;\n"
"    font-weight: 600;\n"
"    spacing: 10px;\n"
"    padding: 6px 0;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 18px;\n"
"    height: 18px;\n"
"    border: 1.5px solid #cbd5e1;\n"
"    background: #ffffff;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    border-color: #0077B6;\n"
"}\n"
"\n"
"QCheckBox::indica"
                        "tor:checked {\n"
"    background: #0077B6;\n"
"    border-color: #0077B6;\n"
"    image: url(:/Icon/Icons/check_white.svg);\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 BOUTONS D'ACTION \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QPushButton#btn_save {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 11px;\n"
"    padding: 12px 28px;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    min-height: 44px;\n"
"    letter-spacing: 0.3px;\n"
"}\n"
"\n"
"QPushButton#btn_save:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"\n"
"QPushButton#btn_save:pressed {\n"
"    background: #023E8A;\n"
"}\n"
"\n"
"QPushButton#btn_reload {\n"
"    background: #ffffff;\n"
"    color: #475569;\n"
"    border: 1.5px"
                        " solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 12px 22px;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    min-height: 44px;\n"
"}\n"
"\n"
"QPushButton#btn_reload:hover {\n"
"    background: #f8fafc;\n"
"    border-color: #c3cedd;\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"QPushButton#btn_upload_logo {\n"
"    background: #eff6ff;\n"
"    color: #023E8A;\n"
"    border: 1.5px solid #bfdbfe;\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 40px;\n"
"}\n"
"\n"
"QPushButton#btn_upload_logo:hover {\n"
"    background: #dbeafe;\n"
"    border-color: #93c5fd;\n"
"}\n"
"\n"
"QPushButton#btn_remove_logo {\n"
"    background: #ffffff;\n"
"    color: #dc2626;\n"
"    border: 1.5px solid #fecaca;\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 40px;\n"
"}\n"
"\n"
"QPushButton#btn_remove_logo:hover {\n"
"    background: #fef2f2;\n"
"}\n"
"\n"
"Q"
                        "PushButton#btn_browse_save {\n"
"    background: #eff6ff;\n"
"    color: #023E8A;\n"
"    border: 1.5px solid #bfdbfe;\n"
"    border-radius: 10px;\n"
"    padding: 10px 20px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 40px;\n"
"}\n"
"\n"
"QPushButton#btn_browse_save:hover {\n"
"    background: #dbeafe;\n"
"    border-color: #93c5fd;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 DANGER ZONE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#danger_card_info {\n"
"    background: #fffbeb;\n"
"    border: 1px solid #fde68a;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QFrame#danger_card_warn {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QFrame#danger_card_danger {\n"
"    background: #fef2f2;\n"
"    border: 1px solid #fecaca;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QLabel#danger_icon_info {\n"
"    back"
                        "ground: #fde68a;\n"
"    color: #92400e;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"}\n"
"\n"
"QLabel#danger_icon_warn {\n"
"    background: #dbeafe;\n"
"    color: #023E8A;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"}\n"
"\n"
"QLabel#danger_icon_danger {\n"
"    background: #fecaca;\n"
"    color: #b91c1c;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"}\n"
"\n"
"QLabel#danger_title {\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"}\n"
"\n"
"QLabel#danger_title_red {\n"
"    color: #b91c1c;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"}\n"
"\n"
"QLabel#danger_desc {\n"
"    color: #64748b;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"QLabel#danger_desc_red {\n"
"    color: #991b1b;\n"
"    font-size: 11px;\n"
"}\n"
"\n"
"QPushButton#btn_export_db {\n"
"    background: #eff6ff;\n"
"    color: #0"
                        "23E8A;\n"
"    border: 1.5px solid #bfdbfe;\n"
"    border-radius: 10px;\n"
"    padding: 10px 22px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 42px;\n"
"}\n"
"\n"
"QPushButton#btn_export_db:hover {\n"
"    background: #dbeafe;\n"
"}\n"
"\n"
"QPushButton#btn_restore_db {\n"
"    background: #fef3c7;\n"
"    color: #92400e;\n"
"    border: 1.5px solid #fcd34d;\n"
"    border-radius: 10px;\n"
"    padding: 10px 22px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 42px;\n"
"}\n"
"\n"
"QPushButton#btn_restore_db:hover {\n"
"    background: #fde68a;\n"
"}\n"
"\n"
"QPushButton#btn_reset_all {\n"
"    background: #dc2626;\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 10px 22px;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"    min-height: 42px;\n"
"}\n"
"\n"
"QPushButton#btn_reset_all:hover {\n"
"    background: #b91c1c;\n"
"}\n"
"\n"
"QPushButton#btn_reset_all:pressed {\n"
"    background: #991b1b;\n"
"}\n"
"\n"
""
                        "/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 FOOTER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#footer_frame {\n"
"    background: #f8fafc;\n"
"    border-top: 1px solid #eef2f7;\n"
"    border-bottom-left-radius: 20px;\n"
"    border-bottom-right-radius: 20px;\n"
"    border: none;\n"
"}\n"
"\n"
"QLabel#lbl_status {\n"
"    color: #94a3b8;\n"
"    font-size: 11px;\n"
"    font-weight: 600; } QLabel#lbl_status[status=\"ok\"] {\n"
"    color: #16A34A;\n"
"    font-weight: 700; } QLabel#lbl_status[status=\"warn\"] {\n"
"    color: #b45309;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 SCROLLBARS \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QScrollArea {\n"
"    background: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"QScrollArea > QWidget > QWidget {\n"
"    b"
                        "ackground: transparent;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #cbd5e1;\n"
"    min-height: 32px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #94a3b8;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 S\u00c9PARATEURS \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */ QFrame[isSep=\"true\"] {\n"
"    background: #eef2f7;\n"
"    border: none;\n"
"    max-height: 1px;\n"
"    min-height: 1px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
                        "\u2550 TABLE MONITORING \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QTableWidget#table_monitoring {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 10px;\n"
"    gridline-color: transparent;\n"
"    alternate-background-color: #f8fafc;\n"
"}\n"
"\n"
"QTableWidget#table_monitoring::item {\n"
"    padding: 8px;\n"
"    color: #0f172a;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"}\n"
"\n"
"QTableWidget#table_monitoring::item:selected {\n"
"    background: #e0f2fe;\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"QTableWidget#table_monitoring QHeaderView::section {\n"
"    background: #f8fafc;\n"
"    color: #64748b;\n"
"    padding: 8px;\n"
"    border: none;\n"
"    border-bottom: 1px solid #e2e8f0;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"}")
        self.root_layout = QVBoxLayout(PageParametres)
        self.root_layout.setSpacing(0)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.card = QFrame(PageParametres)
        self.card.setObjectName(u"card")
        self.card.setFrameShape(QFrame.Shape.NoFrame)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setSpacing(0)
        self.card_layout.setObjectName(u"card_layout")
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.card)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 100))
        self.header_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setSpacing(18)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(28, 22, 28, 22)
        self.header_icon = QLabel(self.header_frame)
        self.header_icon.setObjectName(u"header_icon")
        self.header_icon.setMinimumSize(QSize(48, 48))
        self.header_icon.setMaximumSize(QSize(48, 48))

        self.header_layout.addWidget(self.header_icon)

        self.headerTitles = QVBoxLayout()
        self.headerTitles.setSpacing(4)
        self.headerTitles.setObjectName(u"headerTitles")
        self.page_title = QLabel(self.header_frame)
        self.page_title.setObjectName(u"page_title")

        self.headerTitles.addWidget(self.page_title)

        self.page_subtitle = QLabel(self.header_frame)
        self.page_subtitle.setObjectName(u"page_subtitle")

        self.headerTitles.addWidget(self.page_subtitle)


        self.header_layout.addLayout(self.headerTitles)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_layout.addItem(self.headerSpacer)

        self.version_badge = QLabel(self.header_frame)
        self.version_badge.setObjectName(u"version_badge")

        self.header_layout.addWidget(self.version_badge)


        self.card_layout.addWidget(self.header_frame)

        self.tabs = QTabWidget(self.card)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setUsesScrollButtons(False)
        self.tabs.setDocumentMode(False)
        self.tabs.setTabBarAutoHide(False)
        self.tab_entreprise = QWidget()
        self.tab_entreprise.setObjectName(u"tab_entreprise")
        self.tabEntrepriseLayout = QVBoxLayout(self.tab_entreprise)
        self.tabEntrepriseLayout.setSpacing(0)
        self.tabEntrepriseLayout.setObjectName(u"tabEntrepriseLayout")
        self.tabEntrepriseLayout.setContentsMargins(24, 20, 24, 20)
        self.scrollEntreprise = QScrollArea(self.tab_entreprise)
        self.scrollEntreprise.setObjectName(u"scrollEntreprise")
        self.scrollEntreprise.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollEntreprise.setWidgetResizable(True)
        self.scrollEntrepriseContent = QWidget()
        self.scrollEntrepriseContent.setObjectName(u"scrollEntrepriseContent")
        self.scrollEntrepriseContent.setGeometry(QRect(0, 0, 1000, 758))
        self.scrollEntrepriseLayout = QVBoxLayout(self.scrollEntrepriseContent)
        self.scrollEntrepriseLayout.setSpacing(16)
        self.scrollEntrepriseLayout.setObjectName(u"scrollEntrepriseLayout")
        self.scrollEntrepriseLayout.setContentsMargins(0, 0, 0, 0)
        self.section_card = QFrame(self.scrollEntrepriseContent)
        self.section_card.setObjectName(u"section_card")
        self.sectionIdentityLayout = QVBoxLayout(self.section_card)
        self.sectionIdentityLayout.setSpacing(14)
        self.sectionIdentityLayout.setObjectName(u"sectionIdentityLayout")
        self.sectionIdentityLayout.setContentsMargins(22, 20, 22, 20)
        self.secIdHeader = QHBoxLayout()
        self.secIdHeader.setSpacing(10)
        self.secIdHeader.setObjectName(u"secIdHeader")
        self.secIdIcon = QLabel(self.section_card)
        self.secIdIcon.setObjectName(u"secIdIcon")
        self.secIdIcon.setMinimumSize(QSize(32, 32))
        self.secIdIcon.setMaximumSize(QSize(32, 32))
        self.secIdIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secIdIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secIdHeader.addWidget(self.secIdIcon)

        self.secIdTitle = QLabel(self.section_card)
        self.secIdTitle.setObjectName(u"secIdTitle")
        self.secIdTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secIdHeader.addWidget(self.secIdTitle)

        self.secIdSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secIdHeader.addItem(self.secIdSpacer)

        self.secIdHint = QLabel(self.section_card)
        self.secIdHint.setObjectName(u"secIdHint")
        self.secIdHint.setStyleSheet(u"color: #94a3b8; font-size: 11px; font-style: italic;")

        self.secIdHeader.addWidget(self.secIdHint)


        self.sectionIdentityLayout.addLayout(self.secIdHeader)

        self.sep1 = QFrame(self.section_card)
        self.sep1.setObjectName(u"sep1")
        self.sep1.setMaximumSize(QSize(16777215, 1))
        self.sep1.setStyleSheet(u"QFrame#sep1 { background: #eef2f7; border: none; max-height: 1px; }")
        self.sep1.setFrameShape(QFrame.Shape.HLine)
        self.sep1.setFrameShadow(QFrame.Shadow.Plain)

        self.sectionIdentityLayout.addWidget(self.sep1)

        self.identityGrid = QGridLayout()
        self.identityGrid.setObjectName(u"identityGrid")
        self.identityGrid.setHorizontalSpacing(16)
        self.identityGrid.setVerticalSpacing(14)
        self.lbl_nom = QLabel(self.section_card)
        self.lbl_nom.setObjectName(u"lbl_nom")
        self.lbl_nom.setProperty(u"fieldLabel", True)

        self.identityGrid.addWidget(self.lbl_nom, 0, 0, 1, 1)

        self.edit_nom = QLineEdit(self.section_card)
        self.edit_nom.setObjectName(u"edit_nom")

        self.identityGrid.addWidget(self.edit_nom, 1, 0, 1, 1)

        self.lbl_type = QLabel(self.section_card)
        self.lbl_type.setObjectName(u"lbl_type")
        self.lbl_type.setProperty(u"fieldLabel", True)

        self.identityGrid.addWidget(self.lbl_type, 0, 1, 1, 1)

        self.combo_type = QComboBox(self.section_card)
        self.combo_type.addItem("")
        self.combo_type.addItem("")
        self.combo_type.addItem("")
        self.combo_type.setObjectName(u"combo_type")
        self.combo_type.setStyleSheet(u"QComboBox::drop-down { border: none; width: 26px; }\n"
"QComboBox::down-arrow {\n"
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
"}")

        self.identityGrid.addWidget(self.combo_type, 1, 1, 1, 1)


        self.sectionIdentityLayout.addLayout(self.identityGrid)


        self.scrollEntrepriseLayout.addWidget(self.section_card)

        self.section_card1 = QFrame(self.scrollEntrepriseContent)
        self.section_card1.setObjectName(u"section_card1")
        self.sectionContactLayout = QVBoxLayout(self.section_card1)
        self.sectionContactLayout.setSpacing(14)
        self.sectionContactLayout.setObjectName(u"sectionContactLayout")
        self.sectionContactLayout.setContentsMargins(22, 20, 22, 20)
        self.secContactHeader = QHBoxLayout()
        self.secContactHeader.setSpacing(10)
        self.secContactHeader.setObjectName(u"secContactHeader")
        self.secContactIcon = QLabel(self.section_card1)
        self.secContactIcon.setObjectName(u"secContactIcon")
        self.secContactIcon.setMinimumSize(QSize(32, 32))
        self.secContactIcon.setMaximumSize(QSize(32, 32))
        self.secContactIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secContactIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secContactHeader.addWidget(self.secContactIcon)

        self.secContactTitle = QLabel(self.section_card1)
        self.secContactTitle.setObjectName(u"secContactTitle")
        self.secContactTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secContactHeader.addWidget(self.secContactTitle)

        self.secContactSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secContactHeader.addItem(self.secContactSpacer)


        self.sectionContactLayout.addLayout(self.secContactHeader)

        self.sep2 = QFrame(self.section_card1)
        self.sep2.setObjectName(u"sep2")
        self.sep2.setMaximumSize(QSize(16777215, 1))
        self.sep2.setStyleSheet(u"QFrame#sep2 { background: #eef2f7; border: none; max-height: 1px; }")
        self.sep2.setFrameShape(QFrame.Shape.HLine)
        self.sep2.setFrameShadow(QFrame.Shadow.Plain)

        self.sectionContactLayout.addWidget(self.sep2)

        self.contactGrid = QGridLayout()
        self.contactGrid.setObjectName(u"contactGrid")
        self.contactGrid.setHorizontalSpacing(16)
        self.contactGrid.setVerticalSpacing(14)
        self.lbl_tel = QLabel(self.section_card1)
        self.lbl_tel.setObjectName(u"lbl_tel")
        self.lbl_tel.setProperty(u"fieldLabel", True)

        self.contactGrid.addWidget(self.lbl_tel, 0, 0, 1, 1)

        self.edit_tel = QLineEdit(self.section_card1)
        self.edit_tel.setObjectName(u"edit_tel")

        self.contactGrid.addWidget(self.edit_tel, 1, 0, 1, 1)

        self.lbl_email_ent = QLabel(self.section_card1)
        self.lbl_email_ent.setObjectName(u"lbl_email_ent")
        self.lbl_email_ent.setProperty(u"fieldLabel", True)

        self.contactGrid.addWidget(self.lbl_email_ent, 0, 1, 1, 1)

        self.edit_email_ent = QLineEdit(self.section_card1)
        self.edit_email_ent.setObjectName(u"edit_email_ent")

        self.contactGrid.addWidget(self.edit_email_ent, 1, 1, 1, 1)

        self.lbl_adresse = QLabel(self.section_card1)
        self.lbl_adresse.setObjectName(u"lbl_adresse")
        self.lbl_adresse.setProperty(u"fieldLabel", True)

        self.contactGrid.addWidget(self.lbl_adresse, 2, 0, 1, 2)

        self.edit_adresse = QLineEdit(self.section_card1)
        self.edit_adresse.setObjectName(u"edit_adresse")

        self.contactGrid.addWidget(self.edit_adresse, 3, 0, 1, 2)


        self.sectionContactLayout.addLayout(self.contactGrid)


        self.scrollEntrepriseLayout.addWidget(self.section_card1)

        self.section_card2 = QFrame(self.scrollEntrepriseContent)
        self.section_card2.setObjectName(u"section_card2")
        self.sectionLogoLayout = QVBoxLayout(self.section_card2)
        self.sectionLogoLayout.setSpacing(14)
        self.sectionLogoLayout.setObjectName(u"sectionLogoLayout")
        self.sectionLogoLayout.setContentsMargins(22, 20, 22, 20)
        self.secLogoHeader = QHBoxLayout()
        self.secLogoHeader.setSpacing(10)
        self.secLogoHeader.setObjectName(u"secLogoHeader")
        self.secLogoIcon = QLabel(self.section_card2)
        self.secLogoIcon.setObjectName(u"secLogoIcon")
        self.secLogoIcon.setMinimumSize(QSize(32, 32))
        self.secLogoIcon.setMaximumSize(QSize(32, 32))
        self.secLogoIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secLogoIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secLogoHeader.addWidget(self.secLogoIcon)

        self.secLogoTitle = QLabel(self.section_card2)
        self.secLogoTitle.setObjectName(u"secLogoTitle")
        self.secLogoTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secLogoHeader.addWidget(self.secLogoTitle)

        self.secLogoSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secLogoHeader.addItem(self.secLogoSpacer)


        self.sectionLogoLayout.addLayout(self.secLogoHeader)

        self.sep3 = QFrame(self.section_card2)
        self.sep3.setObjectName(u"sep3")
        self.sep3.setMaximumSize(QSize(16777215, 1))
        self.sep3.setStyleSheet(u"QFrame#sep3 { background: #eef2f7; border: none; max-height: 1px; }")
        self.sep3.setFrameShape(QFrame.Shape.HLine)
        self.sep3.setFrameShadow(QFrame.Shadow.Plain)

        self.sectionLogoLayout.addWidget(self.sep3)

        self.logoRow = QHBoxLayout()
        self.logoRow.setSpacing(20)
        self.logoRow.setObjectName(u"logoRow")
        self.logo_preview = QLabel(self.section_card2)
        self.logo_preview.setObjectName(u"logo_preview")
        self.logo_preview.setMinimumSize(QSize(100, 100))
        self.logo_preview.setMaximumSize(QSize(100, 100))
        self.logo_preview.setStyleSheet(u"QLabel { background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px; color: #94a3b8; font-size: 11px; font-weight: 700; }")
        self.logo_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logoRow.addWidget(self.logo_preview)

        self.logoRight = QVBoxLayout()
        self.logoRight.setSpacing(8)
        self.logoRight.setObjectName(u"logoRight")
        self.lbl_logo_title = QLabel(self.section_card2)
        self.lbl_logo_title.setObjectName(u"lbl_logo_title")
        self.lbl_logo_title.setStyleSheet(u"color: #475569; font-size: 12px; font-weight: 600;")
        self.lbl_logo_title.setWordWrap(True)

        self.logoRight.addWidget(self.lbl_logo_title)

        self.lbl_logo_hint = QLabel(self.section_card2)
        self.lbl_logo_hint.setObjectName(u"lbl_logo_hint")
        self.lbl_logo_hint.setStyleSheet(u"color: #94a3b8; font-size: 11px;")
        self.lbl_logo_hint.setWordWrap(True)

        self.logoRight.addWidget(self.lbl_logo_hint)

        self.logoBtns = QHBoxLayout()
        self.logoBtns.setSpacing(10)
        self.logoBtns.setObjectName(u"logoBtns")
        self.btn_upload_logo = QPushButton(self.section_card2)
        self.btn_upload_logo.setObjectName(u"btn_upload_logo")
        self.btn_upload_logo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.logoBtns.addWidget(self.btn_upload_logo)

        self.btn_remove_logo = QPushButton(self.section_card2)
        self.btn_remove_logo.setObjectName(u"btn_remove_logo")
        self.btn_remove_logo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.logoBtns.addWidget(self.btn_remove_logo)

        self.logoBtnSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.logoBtns.addItem(self.logoBtnSpacer)


        self.logoRight.addLayout(self.logoBtns)


        self.logoRow.addLayout(self.logoRight)


        self.sectionLogoLayout.addLayout(self.logoRow)


        self.scrollEntrepriseLayout.addWidget(self.section_card2)

        self.spacerEntreprise = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.scrollEntrepriseLayout.addItem(self.spacerEntreprise)

        self.scrollEntreprise.setWidget(self.scrollEntrepriseContent)

        self.tabEntrepriseLayout.addWidget(self.scrollEntreprise)

        self.tabs.addTab(self.tab_entreprise, "")
        self.tab_vente = QWidget()
        self.tab_vente.setObjectName(u"tab_vente")
        self.tabVenteLayout = QVBoxLayout(self.tab_vente)
        self.tabVenteLayout.setSpacing(0)
        self.tabVenteLayout.setObjectName(u"tabVenteLayout")
        self.tabVenteLayout.setContentsMargins(24, 20, 24, 20)
        self.scrollVente = QScrollArea(self.tab_vente)
        self.scrollVente.setObjectName(u"scrollVente")
        self.scrollVente.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollVente.setWidgetResizable(True)
        self.scrollVenteContent = QWidget()
        self.scrollVenteContent.setObjectName(u"scrollVenteContent")
        self.scrollVenteContent.setGeometry(QRect(0, 0, 458, 634))
        self.scrollVenteLayout = QVBoxLayout(self.scrollVenteContent)
        self.scrollVenteLayout.setSpacing(16)
        self.scrollVenteLayout.setObjectName(u"scrollVenteLayout")
        self.scrollVenteLayout.setContentsMargins(0, 0, 0, 0)
        self.section_card3 = QFrame(self.scrollVenteContent)
        self.section_card3.setObjectName(u"section_card3")
        self.secVenteLayout = QVBoxLayout(self.section_card3)
        self.secVenteLayout.setSpacing(14)
        self.secVenteLayout.setObjectName(u"secVenteLayout")
        self.secVenteLayout.setContentsMargins(22, 20, 22, 20)
        self.secVenteHeader = QHBoxLayout()
        self.secVenteHeader.setSpacing(10)
        self.secVenteHeader.setObjectName(u"secVenteHeader")
        self.secVenteIcon = QLabel(self.section_card3)
        self.secVenteIcon.setObjectName(u"secVenteIcon")
        self.secVenteIcon.setMinimumSize(QSize(32, 32))
        self.secVenteIcon.setMaximumSize(QSize(32, 32))
        self.secVenteIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secVenteIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secVenteHeader.addWidget(self.secVenteIcon)

        self.secVenteTitle = QLabel(self.section_card3)
        self.secVenteTitle.setObjectName(u"secVenteTitle")
        self.secVenteTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secVenteHeader.addWidget(self.secVenteTitle)

        self.secVenteSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secVenteHeader.addItem(self.secVenteSpacer)


        self.secVenteLayout.addLayout(self.secVenteHeader)

        self.sepV = QFrame(self.section_card3)
        self.sepV.setObjectName(u"sepV")
        self.sepV.setMaximumSize(QSize(16777215, 1))
        self.sepV.setStyleSheet(u"QFrame#sepV { background: #eef2f7; border: none; max-height: 1px; }")
        self.sepV.setFrameShape(QFrame.Shape.HLine)
        self.sepV.setFrameShadow(QFrame.Shadow.Plain)

        self.secVenteLayout.addWidget(self.sepV)

        self.venteGrid = QGridLayout()
        self.venteGrid.setObjectName(u"venteGrid")
        self.venteGrid.setHorizontalSpacing(16)
        self.venteGrid.setVerticalSpacing(14)
        self.lbl_seuil_desc = QLabel(self.section_card3)
        self.lbl_seuil_desc.setObjectName(u"lbl_seuil_desc")
        self.lbl_seuil_desc.setStyleSheet(u"color: #64748b; font-size: 11px;")
        self.lbl_seuil_desc.setWordWrap(True)

        self.venteGrid.addWidget(self.lbl_seuil_desc, 7, 0, 1, 1)

        self.lbl_periode_ca = QLabel(self.section_card3)
        self.lbl_periode_ca.setObjectName(u"lbl_periode_ca")
        self.lbl_periode_ca.setProperty(u"fieldLabel", True)

        self.venteGrid.addWidget(self.lbl_periode_ca, 0, 1, 1, 1)

        self.combo_devise = QComboBox(self.section_card3)
        self.combo_devise.addItem("")
        self.combo_devise.addItem("")
        self.combo_devise.addItem("")
        self.combo_devise.addItem("")
        self.combo_devise.setObjectName(u"combo_devise")

        self.venteGrid.addWidget(self.combo_devise, 1, 0, 1, 1)

        self.spin_max_postes = QSpinBox(self.section_card3)
        self.spin_max_postes.setObjectName(u"spin_max_postes")
        self.spin_max_postes.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spin_max_postes.setMinimum(1)
        self.spin_max_postes.setMaximum(500)
        self.spin_max_postes.setValue(100)

        self.venteGrid.addWidget(self.spin_max_postes, 5, 0, 1, 1)

        self.lbl_taux_change = QLabel(self.section_card3)
        self.lbl_taux_change.setObjectName(u"lbl_taux_change")
        self.lbl_taux_change.setProperty(u"fieldLabel", True)

        self.venteGrid.addWidget(self.lbl_taux_change, 4, 1, 1, 1)

        self.spin_taux_change = QDoubleSpinBox(self.section_card3)
        self.spin_taux_change.setObjectName(u"spin_taux_change")
        self.spin_taux_change.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spin_taux_change.setDecimals(2)
        self.spin_taux_change.setMinimum(1.000000000000000)
        self.spin_taux_change.setMaximum(999999.989999999990687)
        self.spin_taux_change.setValue(2250.000000000000000)

        self.venteGrid.addWidget(self.spin_taux_change, 5, 1, 1, 1)

        self.lbl_caisse = QLabel(self.section_card3)
        self.lbl_caisse.setObjectName(u"lbl_caisse")
        self.lbl_caisse.setProperty(u"fieldLabel", True)

        self.venteGrid.addWidget(self.lbl_caisse, 2, 1, 1, 1)

        self.lbl_devise = QLabel(self.section_card3)
        self.lbl_devise.setObjectName(u"lbl_devise")
        self.lbl_devise.setProperty(u"fieldLabel", True)

        self.venteGrid.addWidget(self.lbl_devise, 0, 0, 1, 1)

        self.combo_periode_ca = QComboBox(self.section_card3)
        self.combo_periode_ca.addItem("")
        self.combo_periode_ca.addItem("")
        self.combo_periode_ca.setObjectName(u"combo_periode_ca")

        self.venteGrid.addWidget(self.combo_periode_ca, 1, 1, 1, 1)

        self.lbl_max_postes = QLabel(self.section_card3)
        self.lbl_max_postes.setObjectName(u"lbl_max_postes")
        self.lbl_max_postes.setProperty(u"fieldLabel", True)

        self.venteGrid.addWidget(self.lbl_max_postes, 4, 0, 1, 1)

        self.lbl_marge = QLabel(self.section_card3)
        self.lbl_marge.setObjectName(u"lbl_marge")
        self.lbl_marge.setProperty(u"fieldLabel", True)

        self.venteGrid.addWidget(self.lbl_marge, 2, 0, 1, 1)

        self.edit_caisse = QLineEdit(self.section_card3)
        self.edit_caisse.setObjectName(u"edit_caisse")
        self.edit_caisse.setMaxLength(2)

        self.venteGrid.addWidget(self.edit_caisse, 3, 1, 1, 1)

        self.spin_seuil_stock = QSpinBox(self.section_card3)
        self.spin_seuil_stock.setObjectName(u"spin_seuil_stock")
        self.spin_seuil_stock.setMinimumSize(QSize(120, 46))
        self.spin_seuil_stock.setStyleSheet(u"")
        self.spin_seuil_stock.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spin_seuil_stock.setMinimum(0)
        self.spin_seuil_stock.setMaximum(1000)
        self.spin_seuil_stock.setValue(20)

        self.venteGrid.addWidget(self.spin_seuil_stock, 7, 1, 1, 1)

        self.spin_marge = QDoubleSpinBox(self.section_card3)
        self.spin_marge.setObjectName(u"spin_marge")
        self.spin_marge.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spin_marge.setDecimals(1)
        self.spin_marge.setMaximum(200.000000000000000)
        self.spin_marge.setValue(30.000000000000000)

        self.venteGrid.addWidget(self.spin_marge, 3, 0, 1, 1)

        self.lbl_seuil_title = QLabel(self.section_card3)
        self.lbl_seuil_title.setObjectName(u"lbl_seuil_title")
        self.lbl_seuil_title.setProperty(u"fieldLabel", True)

        self.venteGrid.addWidget(self.lbl_seuil_title, 6, 0, 1, 1)


        self.secVenteLayout.addLayout(self.venteGrid)

        self.lbl_info_caisse = QLabel(self.section_card3)
        self.lbl_info_caisse.setObjectName(u"lbl_info_caisse")
        self.lbl_info_caisse.setStyleSheet(u"color: #023E8A; font-size: 11px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px;")
        self.lbl_info_caisse.setWordWrap(True)

        self.secVenteLayout.addWidget(self.lbl_info_caisse)

        self.lbl_info_taux = QLabel(self.section_card3)
        self.lbl_info_taux.setObjectName(u"lbl_info_taux")
        self.lbl_info_taux.setStyleSheet(u"color: #b45309; font-size: 11px; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 14px;")
        self.lbl_info_taux.setWordWrap(True)

        self.secVenteLayout.addWidget(self.lbl_info_taux)


        self.scrollVenteLayout.addWidget(self.section_card3)

        self.spacerVente = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.scrollVenteLayout.addItem(self.spacerVente)

        self.scrollVente.setWidget(self.scrollVenteContent)

        self.tabVenteLayout.addWidget(self.scrollVente)

        self.tabs.addTab(self.tab_vente, "")
        self.tab_facturation = QWidget()
        self.tab_facturation.setObjectName(u"tab_facturation")
        self.tabFacturationLayout = QVBoxLayout(self.tab_facturation)
        self.tabFacturationLayout.setSpacing(0)
        self.tabFacturationLayout.setObjectName(u"tabFacturationLayout")
        self.tabFacturationLayout.setContentsMargins(24, 20, 24, 20)
        self.scrollFacturation = QScrollArea(self.tab_facturation)
        self.scrollFacturation.setObjectName(u"scrollFacturation")
        self.scrollFacturation.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollFacturation.setWidgetResizable(True)
        self.scrollFacturationContent = QWidget()
        self.scrollFacturationContent.setObjectName(u"scrollFacturationContent")
        self.scrollFacturationContent.setGeometry(QRect(0, 0, 433, 388))
        self.scrollFacturationLayout = QVBoxLayout(self.scrollFacturationContent)
        self.scrollFacturationLayout.setSpacing(16)
        self.scrollFacturationLayout.setObjectName(u"scrollFacturationLayout")
        self.scrollFacturationLayout.setContentsMargins(0, 0, 0, 0)
        self.section_card4 = QFrame(self.scrollFacturationContent)
        self.section_card4.setObjectName(u"section_card4")
        self.secFactLayout = QVBoxLayout(self.section_card4)
        self.secFactLayout.setSpacing(14)
        self.secFactLayout.setObjectName(u"secFactLayout")
        self.secFactLayout.setContentsMargins(22, 20, 22, 20)
        self.secFactHeader = QHBoxLayout()
        self.secFactHeader.setSpacing(10)
        self.secFactHeader.setObjectName(u"secFactHeader")
        self.secFactIcon = QLabel(self.section_card4)
        self.secFactIcon.setObjectName(u"secFactIcon")
        self.secFactIcon.setMinimumSize(QSize(32, 32))
        self.secFactIcon.setMaximumSize(QSize(32, 32))
        self.secFactIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secFactIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secFactHeader.addWidget(self.secFactIcon)

        self.secFactTitle = QLabel(self.section_card4)
        self.secFactTitle.setObjectName(u"secFactTitle")
        self.secFactTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secFactHeader.addWidget(self.secFactTitle)

        self.secFactSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secFactHeader.addItem(self.secFactSpacer)


        self.secFactLayout.addLayout(self.secFactHeader)

        self.sepF = QFrame(self.section_card4)
        self.sepF.setObjectName(u"sepF")
        self.sepF.setMaximumSize(QSize(16777215, 1))
        self.sepF.setStyleSheet(u"QFrame#sepF { background: #eef2f7; border: none; max-height: 1px; }")
        self.sepF.setFrameShape(QFrame.Shape.HLine)
        self.sepF.setFrameShadow(QFrame.Shadow.Plain)

        self.secFactLayout.addWidget(self.sepF)

        self.chk_impression_auto = QCheckBox(self.section_card4)
        self.chk_impression_auto.setObjectName(u"chk_impression_auto")
        self.chk_impression_auto.setChecked(True)

        self.secFactLayout.addWidget(self.chk_impression_auto)

        self.chk_qrcode = QCheckBox(self.section_card4)
        self.chk_qrcode.setObjectName(u"chk_qrcode")
        self.chk_qrcode.setChecked(True)

        self.secFactLayout.addWidget(self.chk_qrcode)


        self.scrollFacturationLayout.addWidget(self.section_card4)

        self.section_card5 = QFrame(self.scrollFacturationContent)
        self.section_card5.setObjectName(u"section_card5")
        self.secMentionsLayout = QVBoxLayout(self.section_card5)
        self.secMentionsLayout.setSpacing(14)
        self.secMentionsLayout.setObjectName(u"secMentionsLayout")
        self.secMentionsLayout.setContentsMargins(22, 20, 22, 20)
        self.secMentionsHeader = QHBoxLayout()
        self.secMentionsHeader.setSpacing(10)
        self.secMentionsHeader.setObjectName(u"secMentionsHeader")
        self.secMentionsIcon = QLabel(self.section_card5)
        self.secMentionsIcon.setObjectName(u"secMentionsIcon")
        self.secMentionsIcon.setMinimumSize(QSize(32, 32))
        self.secMentionsIcon.setMaximumSize(QSize(32, 32))
        self.secMentionsIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secMentionsIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secMentionsHeader.addWidget(self.secMentionsIcon)

        self.secMentionsTitle = QLabel(self.section_card5)
        self.secMentionsTitle.setObjectName(u"secMentionsTitle")
        self.secMentionsTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secMentionsHeader.addWidget(self.secMentionsTitle)

        self.secMentionsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secMentionsHeader.addItem(self.secMentionsSpacer)

        self.lbl_mentions_hint = QLabel(self.section_card5)
        self.lbl_mentions_hint.setObjectName(u"lbl_mentions_hint")
        self.lbl_mentions_hint.setStyleSheet(u"color: #94a3b8; font-size: 11px; font-style: italic;")

        self.secMentionsHeader.addWidget(self.lbl_mentions_hint)


        self.secMentionsLayout.addLayout(self.secMentionsHeader)

        self.sepM = QFrame(self.section_card5)
        self.sepM.setObjectName(u"sepM")
        self.sepM.setMaximumSize(QSize(16777215, 1))
        self.sepM.setStyleSheet(u"QFrame#sepM { background: #eef2f7; border: none; max-height: 1px; }")
        self.sepM.setFrameShape(QFrame.Shape.HLine)
        self.sepM.setFrameShadow(QFrame.Shadow.Plain)

        self.secMentionsLayout.addWidget(self.sepM)

        self.edit_mentions = QPlainTextEdit(self.section_card5)
        self.edit_mentions.setObjectName(u"edit_mentions")
        self.edit_mentions.setMinimumSize(QSize(0, 46))

        self.secMentionsLayout.addWidget(self.edit_mentions)


        self.scrollFacturationLayout.addWidget(self.section_card5)

        self.spacerFact = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.scrollFacturationLayout.addItem(self.spacerFact)

        self.scrollFacturation.setWidget(self.scrollFacturationContent)

        self.tabFacturationLayout.addWidget(self.scrollFacturation)

        self.tabs.addTab(self.tab_facturation, "")
        self.tab_sauvegarde = QWidget()
        self.tab_sauvegarde.setObjectName(u"tab_sauvegarde")
        self.tabSauvegardeLayout = QVBoxLayout(self.tab_sauvegarde)
        self.tabSauvegardeLayout.setSpacing(0)
        self.tabSauvegardeLayout.setObjectName(u"tabSauvegardeLayout")
        self.tabSauvegardeLayout.setContentsMargins(24, 20, 24, 20)
        self.scrollSauvegarde = QScrollArea(self.tab_sauvegarde)
        self.scrollSauvegarde.setObjectName(u"scrollSauvegarde")
        self.scrollSauvegarde.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollSauvegarde.setWidgetResizable(True)
        self.scrollSauvegardeContent = QWidget()
        self.scrollSauvegardeContent.setObjectName(u"scrollSauvegardeContent")
        self.scrollSauvegardeContent.setGeometry(QRect(0, 0, 455, 784))
        self.scrollSauvegardeLayout = QVBoxLayout(self.scrollSauvegardeContent)
        self.scrollSauvegardeLayout.setSpacing(16)
        self.scrollSauvegardeLayout.setObjectName(u"scrollSauvegardeLayout")
        self.scrollSauvegardeLayout.setContentsMargins(0, 0, 0, 0)
        self.section_card6 = QFrame(self.scrollSauvegardeContent)
        self.section_card6.setObjectName(u"section_card6")
        self.secSaveLayout = QVBoxLayout(self.section_card6)
        self.secSaveLayout.setSpacing(14)
        self.secSaveLayout.setObjectName(u"secSaveLayout")
        self.secSaveLayout.setContentsMargins(22, 20, 22, 20)
        self.secSaveHeader = QHBoxLayout()
        self.secSaveHeader.setSpacing(10)
        self.secSaveHeader.setObjectName(u"secSaveHeader")
        self.secSaveIcon = QLabel(self.section_card6)
        self.secSaveIcon.setObjectName(u"secSaveIcon")
        self.secSaveIcon.setMinimumSize(QSize(32, 32))
        self.secSaveIcon.setMaximumSize(QSize(32, 32))
        self.secSaveIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secSaveIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secSaveHeader.addWidget(self.secSaveIcon)

        self.secSaveTitle = QLabel(self.section_card6)
        self.secSaveTitle.setObjectName(u"secSaveTitle")
        self.secSaveTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secSaveHeader.addWidget(self.secSaveTitle)

        self.secSaveSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secSaveHeader.addItem(self.secSaveSpacer)


        self.secSaveLayout.addLayout(self.secSaveHeader)

        self.sepS = QFrame(self.section_card6)
        self.sepS.setObjectName(u"sepS")
        self.sepS.setMaximumSize(QSize(16777215, 1))
        self.sepS.setStyleSheet(u"QFrame#sepS { background: #eef2f7; border: none; max-height: 1px; }")
        self.sepS.setFrameShape(QFrame.Shape.HLine)
        self.sepS.setFrameShadow(QFrame.Shadow.Plain)

        self.secSaveLayout.addWidget(self.sepS)

        self.chk_sauvegarde_auto = QCheckBox(self.section_card6)
        self.chk_sauvegarde_auto.setObjectName(u"chk_sauvegarde_auto")

        self.secSaveLayout.addWidget(self.chk_sauvegarde_auto)

        self.saveGrid = QGridLayout()
        self.saveGrid.setObjectName(u"saveGrid")
        self.saveGrid.setHorizontalSpacing(16)
        self.saveGrid.setVerticalSpacing(14)
        self.lbl_freq_save = QLabel(self.section_card6)
        self.lbl_freq_save.setObjectName(u"lbl_freq_save")
        self.lbl_freq_save.setProperty(u"fieldLabel", True)

        self.saveGrid.addWidget(self.lbl_freq_save, 0, 0, 1, 1)

        self.spin_freq_save = QSpinBox(self.section_card6)
        self.spin_freq_save.setObjectName(u"spin_freq_save")
        self.spin_freq_save.setMinimum(1)
        self.spin_freq_save.setMaximum(90)
        self.spin_freq_save.setValue(7)

        self.saveGrid.addWidget(self.spin_freq_save, 1, 0, 1, 1)

        self.lbl_max_save = QLabel(self.section_card6)
        self.lbl_max_save.setObjectName(u"lbl_max_save")
        self.lbl_max_save.setProperty(u"fieldLabel", True)

        self.saveGrid.addWidget(self.lbl_max_save, 0, 1, 1, 1)

        self.spin_max_save = QSpinBox(self.section_card6)
        self.spin_max_save.setObjectName(u"spin_max_save")
        self.spin_max_save.setMinimum(1)
        self.spin_max_save.setMaximum(100)
        self.spin_max_save.setValue(10)

        self.saveGrid.addWidget(self.spin_max_save, 1, 1, 1, 1)


        self.secSaveLayout.addLayout(self.saveGrid)

        self.lbl_save_info = QLabel(self.section_card6)
        self.lbl_save_info.setObjectName(u"lbl_save_info")
        self.lbl_save_info.setStyleSheet(u"color: #023E8A; font-size: 11px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px;")
        self.lbl_save_info.setWordWrap(True)

        self.secSaveLayout.addWidget(self.lbl_save_info)


        self.scrollSauvegardeLayout.addWidget(self.section_card6)

        self.section_card7 = QFrame(self.scrollSauvegardeContent)
        self.section_card7.setObjectName(u"section_card7")
        self.secBackupLayout = QVBoxLayout(self.section_card7)
        self.secBackupLayout.setSpacing(14)
        self.secBackupLayout.setObjectName(u"secBackupLayout")
        self.secBackupLayout.setContentsMargins(22, 20, 22, 20)
        self.secBackupHeader = QHBoxLayout()
        self.secBackupHeader.setSpacing(10)
        self.secBackupHeader.setObjectName(u"secBackupHeader")
        self.secBackupIcon = QLabel(self.section_card7)
        self.secBackupIcon.setObjectName(u"secBackupIcon")
        self.secBackupIcon.setMinimumSize(QSize(32, 32))
        self.secBackupIcon.setMaximumSize(QSize(32, 32))
        self.secBackupIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secBackupIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secBackupHeader.addWidget(self.secBackupIcon)

        self.secBackupTitle = QLabel(self.section_card7)
        self.secBackupTitle.setObjectName(u"secBackupTitle")
        self.secBackupTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secBackupHeader.addWidget(self.secBackupTitle)

        self.secBackupSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secBackupHeader.addItem(self.secBackupSpacer)

        self.btn_manage_backups = QPushButton(self.section_card7)
        self.btn_manage_backups.setObjectName(u"btn_manage_backups")
        self.btn_manage_backups.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_manage_backups.setStyleSheet(u"QPushButton { background: #eff6ff; color: #023E8A; border: 1.5px solid #bfdbfe; border-radius: 10px; padding: 8px 16px; font-size: 12px; font-weight: 700; } QPushButton:hover { background: #dbeafe; border-color: #93c5fd; }")

        self.secBackupHeader.addWidget(self.btn_manage_backups)


        self.secBackupLayout.addLayout(self.secBackupHeader)

        self.sepBk = QFrame(self.section_card7)
        self.sepBk.setObjectName(u"sepBk")
        self.sepBk.setMaximumSize(QSize(16777215, 1))
        self.sepBk.setStyleSheet(u"QFrame#sepBk { background: #eef2f7; border: none; max-height: 1px; }")
        self.sepBk.setFrameShape(QFrame.Shape.HLine)
        self.sepBk.setFrameShadow(QFrame.Shadow.Plain)

        self.secBackupLayout.addWidget(self.sepBk)

        self.lbl_dossier_save = QLabel(self.section_card7)
        self.lbl_dossier_save.setObjectName(u"lbl_dossier_save")
        self.lbl_dossier_save.setProperty(u"fieldLabel", True)

        self.secBackupLayout.addWidget(self.lbl_dossier_save)

        self.saveFolderRow = QHBoxLayout()
        self.saveFolderRow.setSpacing(10)
        self.saveFolderRow.setObjectName(u"saveFolderRow")
        self.edit_dossier_save = QLineEdit(self.section_card7)
        self.edit_dossier_save.setObjectName(u"edit_dossier_save")

        self.saveFolderRow.addWidget(self.edit_dossier_save)

        self.btn_browse_save = QPushButton(self.section_card7)
        self.btn_browse_save.setObjectName(u"btn_browse_save")
        self.btn_browse_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.saveFolderRow.addWidget(self.btn_browse_save)


        self.secBackupLayout.addLayout(self.saveFolderRow)

        self.chk_backup_secondary = QCheckBox(self.section_card7)
        self.chk_backup_secondary.setObjectName(u"chk_backup_secondary")

        self.secBackupLayout.addWidget(self.chk_backup_secondary)

        self.lbl_backup_secondary = QLabel(self.section_card7)
        self.lbl_backup_secondary.setObjectName(u"lbl_backup_secondary")
        self.lbl_backup_secondary.setProperty(u"fieldLabel", True)

        self.secBackupLayout.addWidget(self.lbl_backup_secondary)

        self.backupSecRow = QHBoxLayout()
        self.backupSecRow.setSpacing(10)
        self.backupSecRow.setObjectName(u"backupSecRow")
        self.edit_backup_secondary = QLineEdit(self.section_card7)
        self.edit_backup_secondary.setObjectName(u"edit_backup_secondary")
        self.edit_backup_secondary.setEnabled(False)

        self.backupSecRow.addWidget(self.edit_backup_secondary)

        self.btn_browse_backup_secondary = QPushButton(self.section_card7)
        self.btn_browse_backup_secondary.setObjectName(u"btn_browse_backup_secondary")
        self.btn_browse_backup_secondary.setEnabled(False)
        self.btn_browse_backup_secondary.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.backupSecRow.addWidget(self.btn_browse_backup_secondary)


        self.secBackupLayout.addLayout(self.backupSecRow)

        self.lbl_backup_secondary_info = QLabel(self.section_card7)
        self.lbl_backup_secondary_info.setObjectName(u"lbl_backup_secondary_info")
        self.lbl_backup_secondary_info.setStyleSheet(u"color: #b45309; font-size: 11px; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 14px;")
        self.lbl_backup_secondary_info.setWordWrap(True)

        self.secBackupLayout.addWidget(self.lbl_backup_secondary_info)


        self.scrollSauvegardeLayout.addWidget(self.section_card7)

        self.spacerSave = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.scrollSauvegardeLayout.addItem(self.spacerSave)

        self.scrollSauvegarde.setWidget(self.scrollSauvegardeContent)

        self.tabSauvegardeLayout.addWidget(self.scrollSauvegarde)

        self.tabs.addTab(self.tab_sauvegarde, "")
        self.tab_securite = QWidget()
        self.tab_securite.setObjectName(u"tab_securite")
        self.tabSecuriteLayout = QVBoxLayout(self.tab_securite)
        self.tabSecuriteLayout.setSpacing(0)
        self.tabSecuriteLayout.setObjectName(u"tabSecuriteLayout")
        self.tabSecuriteLayout.setContentsMargins(24, 20, 24, 20)
        self.scrollSecurite = QScrollArea(self.tab_securite)
        self.scrollSecurite.setObjectName(u"scrollSecurite")
        self.scrollSecurite.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollSecurite.setWidgetResizable(True)
        self.scrollSecuriteContent = QWidget()
        self.scrollSecuriteContent.setObjectName(u"scrollSecuriteContent")
        self.scrollSecuriteContent.setGeometry(QRect(0, 0, 700, 963))
        self.scrollSecuriteLayout = QVBoxLayout(self.scrollSecuriteContent)
        self.scrollSecuriteLayout.setSpacing(16)
        self.scrollSecuriteLayout.setObjectName(u"scrollSecuriteLayout")
        self.scrollSecuriteLayout.setContentsMargins(0, 0, 0, 0)
        self.section_card8 = QFrame(self.scrollSecuriteContent)
        self.section_card8.setObjectName(u"section_card8")
        self.secSecuLayout = QVBoxLayout(self.section_card8)
        self.secSecuLayout.setSpacing(14)
        self.secSecuLayout.setObjectName(u"secSecuLayout")
        self.secSecuLayout.setContentsMargins(22, 20, 22, 20)
        self.secSecuHeader = QHBoxLayout()
        self.secSecuHeader.setSpacing(10)
        self.secSecuHeader.setObjectName(u"secSecuHeader")
        self.secSecuIcon = QLabel(self.section_card8)
        self.secSecuIcon.setObjectName(u"secSecuIcon")
        self.secSecuIcon.setMinimumSize(QSize(32, 32))
        self.secSecuIcon.setMaximumSize(QSize(32, 32))
        self.secSecuIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secSecuIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secSecuHeader.addWidget(self.secSecuIcon)

        self.secSecuTitle = QLabel(self.section_card8)
        self.secSecuTitle.setObjectName(u"secSecuTitle")
        self.secSecuTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secSecuHeader.addWidget(self.secSecuTitle)

        self.secSecuSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secSecuHeader.addItem(self.secSecuSpacer)


        self.secSecuLayout.addLayout(self.secSecuHeader)

        self.sepSec = QFrame(self.section_card8)
        self.sepSec.setObjectName(u"sepSec")
        self.sepSec.setMaximumSize(QSize(16777215, 1))
        self.sepSec.setStyleSheet(u"QFrame#sepSec { background: #eef2f7; border: none; max-height: 1px; }")
        self.sepSec.setFrameShape(QFrame.Shape.HLine)
        self.sepSec.setFrameShadow(QFrame.Shadow.Plain)

        self.secSecuLayout.addWidget(self.sepSec)

        self.securiteGrid = QGridLayout()
        self.securiteGrid.setObjectName(u"securiteGrid")
        self.securiteGrid.setHorizontalSpacing(16)
        self.securiteGrid.setVerticalSpacing(14)
        self.lbl_pwd_min = QLabel(self.section_card8)
        self.lbl_pwd_min.setObjectName(u"lbl_pwd_min")
        self.lbl_pwd_min.setProperty(u"fieldLabel", True)

        self.securiteGrid.addWidget(self.lbl_pwd_min, 0, 0, 1, 1)

        self.spin_pwd_min = QSpinBox(self.section_card8)
        self.spin_pwd_min.setObjectName(u"spin_pwd_min")
        self.spin_pwd_min.setMinimum(4)
        self.spin_pwd_min.setMaximum(32)
        self.spin_pwd_min.setValue(8)

        self.securiteGrid.addWidget(self.spin_pwd_min, 1, 0, 1, 1)

        self.lbl_pwd_exp = QLabel(self.section_card8)
        self.lbl_pwd_exp.setObjectName(u"lbl_pwd_exp")
        self.lbl_pwd_exp.setProperty(u"fieldLabel", True)

        self.securiteGrid.addWidget(self.lbl_pwd_exp, 0, 1, 1, 1)

        self.spin_pwd_exp = QSpinBox(self.section_card8)
        self.spin_pwd_exp.setObjectName(u"spin_pwd_exp")
        self.spin_pwd_exp.setMaximum(3650)
        self.spin_pwd_exp.setValue(0)

        self.securiteGrid.addWidget(self.spin_pwd_exp, 1, 1, 1, 1)


        self.secSecuLayout.addLayout(self.securiteGrid)

        self.lbl_complexite = QLabel(self.section_card8)
        self.lbl_complexite.setObjectName(u"lbl_complexite")
        self.lbl_complexite.setProperty(u"fieldLabel", True)

        self.secSecuLayout.addWidget(self.lbl_complexite)

        self.complexityLayout = QVBoxLayout()
        self.complexityLayout.setSpacing(4)
        self.complexityLayout.setObjectName(u"complexityLayout")
        self.chk_require_digit = QCheckBox(self.section_card8)
        self.chk_require_digit.setObjectName(u"chk_require_digit")

        self.complexityLayout.addWidget(self.chk_require_digit)

        self.chk_require_upper = QCheckBox(self.section_card8)
        self.chk_require_upper.setObjectName(u"chk_require_upper")

        self.complexityLayout.addWidget(self.chk_require_upper)

        self.chk_require_special = QCheckBox(self.section_card8)
        self.chk_require_special.setObjectName(u"chk_require_special")

        self.complexityLayout.addWidget(self.chk_require_special)


        self.secSecuLayout.addLayout(self.complexityLayout)

        self.lbl_secu_info = QLabel(self.section_card8)
        self.lbl_secu_info.setObjectName(u"lbl_secu_info")
        self.lbl_secu_info.setStyleSheet(u"color: #b45309; font-size: 11px; font-weight: 600; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 14px;")
        self.lbl_secu_info.setWordWrap(True)

        self.secSecuLayout.addWidget(self.lbl_secu_info)

        self.sepSec2 = QFrame(self.section_card8)
        self.sepSec2.setObjectName(u"sepSec2")
        self.sepSec2.setMaximumSize(QSize(16777215, 1))
        self.sepSec2.setStyleSheet(u"QFrame#sepSec2 { background: #eef2f7; border: none; max-height: 1px; }")
        self.sepSec2.setFrameShape(QFrame.Shape.HLine)
        self.sepSec2.setFrameShadow(QFrame.Shadow.Plain)

        self.secSecuLayout.addWidget(self.sepSec2)

        self.seuilLayout_4 = QVBoxLayout()
        self.seuilLayout_4.setSpacing(14)
        self.seuilLayout_4.setObjectName(u"seuilLayout_4")
        self.lbl_seuil_title_4 = QLabel(self.section_card8)
        self.lbl_seuil_title_4.setObjectName(u"lbl_seuil_title_4")
        self.lbl_seuil_title_4.setProperty(u"fieldLabel", True)

        self.seuilLayout_4.addWidget(self.lbl_seuil_title_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.chk_backup_urgence = QCheckBox(self.section_card8)
        self.chk_backup_urgence.setObjectName(u"chk_backup_urgence")
        self.chk_backup_urgence.setChecked(True)

        self.verticalLayout.addWidget(self.chk_backup_urgence)

        self.chk_allow_admin_client = QCheckBox(self.section_card8)
        self.chk_allow_admin_client.setObjectName(u"chk_allow_admin_client")
        self.chk_allow_admin_client.setChecked(True)

        self.verticalLayout.addWidget(self.chk_allow_admin_client)


        self.seuilLayout_4.addLayout(self.verticalLayout)


        self.secSecuLayout.addLayout(self.seuilLayout_4)


        self.scrollSecuriteLayout.addWidget(self.section_card8)

        self.section_card9 = QFrame(self.scrollSecuriteContent)
        self.section_card9.setObjectName(u"section_card9")
        self.secMonitoringLayout = QVBoxLayout(self.section_card9)
        self.secMonitoringLayout.setSpacing(14)
        self.secMonitoringLayout.setObjectName(u"secMonitoringLayout")
        self.secMonitoringLayout.setContentsMargins(22, 20, 22, 20)
        self.secMonitoringHeader = QHBoxLayout()
        self.secMonitoringHeader.setSpacing(10)
        self.secMonitoringHeader.setObjectName(u"secMonitoringHeader")
        self.secMonitoringIcon = QLabel(self.section_card9)
        self.secMonitoringIcon.setObjectName(u"secMonitoringIcon")
        self.secMonitoringIcon.setMinimumSize(QSize(32, 32))
        self.secMonitoringIcon.setMaximumSize(QSize(32, 32))
        self.secMonitoringIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secMonitoringIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secMonitoringHeader.addWidget(self.secMonitoringIcon)

        self.secMonitoringTitle = QLabel(self.section_card9)
        self.secMonitoringTitle.setObjectName(u"secMonitoringTitle")
        self.secMonitoringTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secMonitoringHeader.addWidget(self.secMonitoringTitle)

        self.secMonitoringSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secMonitoringHeader.addItem(self.secMonitoringSpacer)

        self.monitoring_count_badge = QLabel(self.section_card9)
        self.monitoring_count_badge.setObjectName(u"monitoring_count_badge")
        self.monitoring_count_badge.setStyleSheet(u"background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; border-radius: 10px; padding: 4px 14px; font-size: 11px; font-weight: 800;")

        self.secMonitoringHeader.addWidget(self.monitoring_count_badge)


        self.secMonitoringLayout.addLayout(self.secMonitoringHeader)

        self.sepMon = QFrame(self.section_card9)
        self.sepMon.setObjectName(u"sepMon")
        self.sepMon.setMaximumSize(QSize(16777215, 1))
        self.sepMon.setStyleSheet(u"QFrame#sepMon { background: #eef2f7; border: none; max-height: 1px; }")
        self.sepMon.setFrameShape(QFrame.Shape.HLine)
        self.sepMon.setFrameShadow(QFrame.Shadow.Plain)

        self.secMonitoringLayout.addWidget(self.sepMon)

        self.monitoring_client_info = QLabel(self.section_card9)
        self.monitoring_client_info.setObjectName(u"monitoring_client_info")
        self.monitoring_client_info.setVisible(False)
        self.monitoring_client_info.setStyleSheet(u"color: #92400e; font-size: 11px; font-weight: 600; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 14px;")
        self.monitoring_client_info.setWordWrap(True)

        self.secMonitoringLayout.addWidget(self.monitoring_client_info)

        self.monitoring_add_bar = QWidget(self.section_card9)
        self.monitoring_add_bar.setObjectName(u"monitoring_add_bar")
        self.monitoringAddBarLayout = QHBoxLayout(self.monitoring_add_bar)
        self.monitoringAddBarLayout.setSpacing(10)
        self.monitoringAddBarLayout.setObjectName(u"monitoringAddBarLayout")
        self.monitoringAddBarLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_monitoring_role = QLabel(self.monitoring_add_bar)
        self.lbl_monitoring_role.setObjectName(u"lbl_monitoring_role")
        self.lbl_monitoring_role.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700;")

        self.monitoringAddBarLayout.addWidget(self.lbl_monitoring_role)

        self.combo_monitoring_role = QComboBox(self.monitoring_add_bar)
        self.combo_monitoring_role.addItem("")
        self.combo_monitoring_role.addItem("")
        self.combo_monitoring_role.addItem("")
        self.combo_monitoring_role.addItem("")
        self.combo_monitoring_role.setObjectName(u"combo_monitoring_role")
        self.combo_monitoring_role.setMinimumSize(QSize(220, 46))

        self.monitoringAddBarLayout.addWidget(self.combo_monitoring_role)

        self.btn_add_monitoring = QPushButton(self.monitoring_add_bar)
        self.btn_add_monitoring.setObjectName(u"btn_add_monitoring")
        self.btn_add_monitoring.setMinimumSize(QSize(0, 40))
        self.btn_add_monitoring.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_monitoring.setStyleSheet(u"QPushButton { background: #0077B6; color: #ffffff; border: none; border-radius: 10px; padding: 8px 20px; font-size: 12px; font-weight: 700; } QPushButton:hover { background: #023E8A; } QPushButton:disabled { background: #cbd5e1; color: #64748b; }")

        self.monitoringAddBarLayout.addWidget(self.btn_add_monitoring)

        self.monitoringAddSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.monitoringAddBarLayout.addItem(self.monitoringAddSpacer)

        self.btn_refresh_monitoring = QPushButton(self.monitoring_add_bar)
        self.btn_refresh_monitoring.setObjectName(u"btn_refresh_monitoring")
        self.btn_refresh_monitoring.setMinimumSize(QSize(0, 40))
        self.btn_refresh_monitoring.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_refresh_monitoring.setStyleSheet(u"QPushButton { background: #f8fafc; color: #475569; border: 1.5px solid #dbe3ec; border-radius: 10px; padding: 8px 16px; font-size: 12px; font-weight: 700; } QPushButton:hover { background: #f1f5f9; }")

        self.monitoringAddBarLayout.addWidget(self.btn_refresh_monitoring)


        self.secMonitoringLayout.addWidget(self.monitoring_add_bar)

        self.table_monitoring = QTableWidget(self.section_card9)
        if (self.table_monitoring.columnCount() < 5):
            self.table_monitoring.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_monitoring.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_monitoring.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_monitoring.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_monitoring.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_monitoring.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.table_monitoring.setObjectName(u"table_monitoring")
        self.table_monitoring.setMinimumSize(QSize(0, 200))
        self.table_monitoring.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_monitoring.setAlternatingRowColors(True)
        self.table_monitoring.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_monitoring.setShowGrid(False)
        self.table_monitoring.setColumnCount(5)

        self.secMonitoringLayout.addWidget(self.table_monitoring)

        self.lbl_monitoring_empty = QLabel(self.section_card9)
        self.lbl_monitoring_empty.setObjectName(u"lbl_monitoring_empty")
        self.lbl_monitoring_empty.setVisible(False)
        self.lbl_monitoring_empty.setStyleSheet(u"color: #94a3b8; font-size: 11px; font-style: italic; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 10px; padding: 20px;")
        self.lbl_monitoring_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_monitoring_empty.setWordWrap(True)

        self.secMonitoringLayout.addWidget(self.lbl_monitoring_empty)


        self.scrollSecuriteLayout.addWidget(self.section_card9)

        self.spacerSecu = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.scrollSecuriteLayout.addItem(self.spacerSecu)

        self.scrollSecurite.setWidget(self.scrollSecuriteContent)

        self.tabSecuriteLayout.addWidget(self.scrollSecurite)

        self.tabs.addTab(self.tab_securite, "")
        self.tab_imprimantes = QWidget()
        self.tab_imprimantes.setObjectName(u"tab_imprimantes")
        self.tabImprimantesLayout = QVBoxLayout(self.tab_imprimantes)
        self.tabImprimantesLayout.setSpacing(0)
        self.tabImprimantesLayout.setObjectName(u"tabImprimantesLayout")
        self.tabImprimantesLayout.setContentsMargins(24, 20, 24, 20)
        self.scrollImprimantes = QScrollArea(self.tab_imprimantes)
        self.scrollImprimantes.setObjectName(u"scrollImprimantes")
        self.scrollImprimantes.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollImprimantes.setWidgetResizable(True)
        self.scrollImprimantesContent = QWidget()
        self.scrollImprimantesContent.setObjectName(u"scrollImprimantesContent")
        self.scrollImprimantesContent.setGeometry(QRect(0, 0, 497, 668))
        self.scrollImprimantesLayout = QVBoxLayout(self.scrollImprimantesContent)
        self.scrollImprimantesLayout.setSpacing(16)
        self.scrollImprimantesLayout.setObjectName(u"scrollImprimantesLayout")
        self.scrollImprimantesLayout.setContentsMargins(0, 0, 0, 0)
        self.section_card10 = QFrame(self.scrollImprimantesContent)
        self.section_card10.setObjectName(u"section_card10")
        self.secPrinterTicketLayout = QVBoxLayout(self.section_card10)
        self.secPrinterTicketLayout.setSpacing(14)
        self.secPrinterTicketLayout.setObjectName(u"secPrinterTicketLayout")
        self.secPrinterTicketLayout.setContentsMargins(22, 20, 22, 20)
        self.secPrinterTicketHeader = QHBoxLayout()
        self.secPrinterTicketHeader.setSpacing(10)
        self.secPrinterTicketHeader.setObjectName(u"secPrinterTicketHeader")
        self.secPrinterTicketIcon = QLabel(self.section_card10)
        self.secPrinterTicketIcon.setObjectName(u"secPrinterTicketIcon")
        self.secPrinterTicketIcon.setMinimumSize(QSize(32, 32))
        self.secPrinterTicketIcon.setMaximumSize(QSize(32, 32))
        self.secPrinterTicketIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secPrinterTicketIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secPrinterTicketHeader.addWidget(self.secPrinterTicketIcon)

        self.secPrinterTicketTitle = QLabel(self.section_card10)
        self.secPrinterTicketTitle.setObjectName(u"secPrinterTicketTitle")
        self.secPrinterTicketTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secPrinterTicketHeader.addWidget(self.secPrinterTicketTitle)

        self.secPrinterTicketSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secPrinterTicketHeader.addItem(self.secPrinterTicketSpacer)


        self.secPrinterTicketLayout.addLayout(self.secPrinterTicketHeader)

        self.lbl_printer_ticket_desc = QLabel(self.section_card10)
        self.lbl_printer_ticket_desc.setObjectName(u"lbl_printer_ticket_desc")
        self.lbl_printer_ticket_desc.setStyleSheet(u"color: #64748b; font-size: 11px;")
        self.lbl_printer_ticket_desc.setWordWrap(True)

        self.secPrinterTicketLayout.addWidget(self.lbl_printer_ticket_desc)

        self.printerTicketRow = QHBoxLayout()
        self.printerTicketRow.setSpacing(10)
        self.printerTicketRow.setObjectName(u"printerTicketRow")
        self.combo_printer_ticket = QComboBox(self.section_card10)
        self.combo_printer_ticket.setObjectName(u"combo_printer_ticket")
        self.combo_printer_ticket.setMinimumSize(QSize(0, 46))

        self.printerTicketRow.addWidget(self.combo_printer_ticket)

        self.btn_refresh_printers_ticket = QPushButton(self.section_card10)
        self.btn_refresh_printers_ticket.setObjectName(u"btn_refresh_printers_ticket")
        self.btn_refresh_printers_ticket.setMinimumSize(QSize(0, 44))
        self.btn_refresh_printers_ticket.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_refresh_printers_ticket.setStyleSheet(u"QPushButton { background: #ffffff; color: #023E8A; border: 1.5px solid #dbe3ec; border-radius: 10px; padding: 0 20px; font-size: 12px; font-weight: 700; }\n"
"QPushButton:hover { background: #eff6ff; border-color: #bfdbfe; }")

        self.printerTicketRow.addWidget(self.btn_refresh_printers_ticket)

        self.btn_test_print_ticket = QPushButton(self.section_card10)
        self.btn_test_print_ticket.setObjectName(u"btn_test_print_ticket")
        self.btn_test_print_ticket.setMinimumSize(QSize(0, 44))
        self.btn_test_print_ticket.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_test_print_ticket.setStyleSheet(u"QPushButton { background: #eff6ff; color: #023E8A; border: 1.5px solid #bfdbfe; border-radius: 10px; padding: 0 20px; font-size: 12px; font-weight: 700; }\n"
"QPushButton:hover { background: #dbeafe; }")

        self.printerTicketRow.addWidget(self.btn_test_print_ticket)


        self.secPrinterTicketLayout.addLayout(self.printerTicketRow)


        self.scrollImprimantesLayout.addWidget(self.section_card10)

        self.section_card11 = QFrame(self.scrollImprimantesContent)
        self.section_card11.setObjectName(u"section_card11")
        self.secPrinterReportLayout = QVBoxLayout(self.section_card11)
        self.secPrinterReportLayout.setSpacing(14)
        self.secPrinterReportLayout.setObjectName(u"secPrinterReportLayout")
        self.secPrinterReportLayout.setContentsMargins(22, 20, 22, 20)
        self.secPrinterReportHeader = QHBoxLayout()
        self.secPrinterReportHeader.setSpacing(10)
        self.secPrinterReportHeader.setObjectName(u"secPrinterReportHeader")
        self.secPrinterReportIcon = QLabel(self.section_card11)
        self.secPrinterReportIcon.setObjectName(u"secPrinterReportIcon")
        self.secPrinterReportIcon.setMinimumSize(QSize(32, 32))
        self.secPrinterReportIcon.setMaximumSize(QSize(32, 32))
        self.secPrinterReportIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secPrinterReportIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secPrinterReportHeader.addWidget(self.secPrinterReportIcon)

        self.secPrinterReportTitle = QLabel(self.section_card11)
        self.secPrinterReportTitle.setObjectName(u"secPrinterReportTitle")
        self.secPrinterReportTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secPrinterReportHeader.addWidget(self.secPrinterReportTitle)

        self.secPrinterReportSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.secPrinterReportHeader.addItem(self.secPrinterReportSpacer)


        self.secPrinterReportLayout.addLayout(self.secPrinterReportHeader)

        self.lbl_printer_report_desc = QLabel(self.section_card11)
        self.lbl_printer_report_desc.setObjectName(u"lbl_printer_report_desc")
        self.lbl_printer_report_desc.setStyleSheet(u"color: #64748b; font-size: 11px;")
        self.lbl_printer_report_desc.setWordWrap(True)

        self.secPrinterReportLayout.addWidget(self.lbl_printer_report_desc)

        self.printerReportRow = QHBoxLayout()
        self.printerReportRow.setSpacing(10)
        self.printerReportRow.setObjectName(u"printerReportRow")
        self.combo_printer_report = QComboBox(self.section_card11)
        self.combo_printer_report.setObjectName(u"combo_printer_report")
        self.combo_printer_report.setMinimumSize(QSize(0, 46))

        self.printerReportRow.addWidget(self.combo_printer_report)

        self.btn_test_print_report = QPushButton(self.section_card11)
        self.btn_test_print_report.setObjectName(u"btn_test_print_report")
        self.btn_test_print_report.setMinimumSize(QSize(0, 44))
        self.btn_test_print_report.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_test_print_report.setStyleSheet(u"QPushButton { background: #eff6ff; color: #023E8A; border: 1.5px solid #bfdbfe; border-radius: 10px; padding: 0 20px; font-size: 12px; font-weight: 700; }\n"
"QPushButton:hover { background: #dbeafe; }")

        self.printerReportRow.addWidget(self.btn_test_print_report)


        self.secPrinterReportLayout.addLayout(self.printerReportRow)


        self.scrollImprimantesLayout.addWidget(self.section_card11)

        self.section_card12 = QFrame(self.scrollImprimantesContent)
        self.section_card12.setObjectName(u"section_card12")
        self.secPrintAutoLayout = QVBoxLayout(self.section_card12)
        self.secPrintAutoLayout.setSpacing(14)
        self.secPrintAutoLayout.setObjectName(u"secPrintAutoLayout")
        self.secPrintAutoLayout.setContentsMargins(22, 20, 22, 20)
        self.secPrintAutoHeader = QHBoxLayout()
        self.secPrintAutoHeader.setSpacing(10)
        self.secPrintAutoHeader.setObjectName(u"secPrintAutoHeader")
        self.secPrintAutoIcon = QLabel(self.section_card12)
        self.secPrintAutoIcon.setObjectName(u"secPrintAutoIcon")
        self.secPrintAutoIcon.setMinimumSize(QSize(32, 32))
        self.secPrintAutoIcon.setMaximumSize(QSize(32, 32))
        self.secPrintAutoIcon.setStyleSheet(u"QLabel#section_icon { background: #e0f2fe; color: #023E8A; border-radius: 8px; padding: 6px; font-size: 12px; font-weight: 800; }")
        self.secPrintAutoIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.secPrintAutoHeader.addWidget(self.secPrintAutoIcon)

        self.secPrintAutoTitle = QLabel(self.section_card12)
        self.secPrintAutoTitle.setObjectName(u"secPrintAutoTitle")
        self.secPrintAutoTitle.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 800;")

        self.secPrintAutoHeader.addWidget(self.secPrintAutoTitle)


        self.secPrintAutoLayout.addLayout(self.secPrintAutoHeader)

        self.chk_auto_print = QCheckBox(self.section_card12)
        self.chk_auto_print.setObjectName(u"chk_auto_print")

        self.secPrintAutoLayout.addWidget(self.chk_auto_print)

        self.chk_auto_print_report = QCheckBox(self.section_card12)
        self.chk_auto_print_report.setObjectName(u"chk_auto_print_report")

        self.secPrintAutoLayout.addWidget(self.chk_auto_print_report)

        self.chk_auto_open_pdf = QCheckBox(self.section_card12)
        self.chk_auto_open_pdf.setObjectName(u"chk_auto_open_pdf")
        self.chk_auto_open_pdf.setChecked(True)

        self.secPrintAutoLayout.addWidget(self.chk_auto_open_pdf)


        self.scrollImprimantesLayout.addWidget(self.section_card12)

        self.spacerPrinters = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.scrollImprimantesLayout.addItem(self.spacerPrinters)

        self.scrollImprimantes.setWidget(self.scrollImprimantesContent)

        self.tabImprimantesLayout.addWidget(self.scrollImprimantes)

        self.tabs.addTab(self.tab_imprimantes, "")
        self.tab_danger = QWidget()
        self.tab_danger.setObjectName(u"tab_danger")
        self.tabDangerLayout = QVBoxLayout(self.tab_danger)
        self.tabDangerLayout.setSpacing(0)
        self.tabDangerLayout.setObjectName(u"tabDangerLayout")
        self.tabDangerLayout.setContentsMargins(24, 20, 24, 20)
        self.scrollDanger = QScrollArea(self.tab_danger)
        self.scrollDanger.setObjectName(u"scrollDanger")
        self.scrollDanger.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollDanger.setWidgetResizable(True)
        self.scrollDangerContent = QWidget()
        self.scrollDangerContent.setObjectName(u"scrollDangerContent")
        self.scrollDangerContent.setGeometry(QRect(0, 0, 409, 495))
        self.scrollDangerLayout = QVBoxLayout(self.scrollDangerContent)
        self.scrollDangerLayout.setSpacing(14)
        self.scrollDangerLayout.setObjectName(u"scrollDangerLayout")
        self.scrollDangerLayout.setContentsMargins(0, 0, 0, 0)
        self.danger_card_info = QFrame(self.scrollDangerContent)
        self.danger_card_info.setObjectName(u"danger_card_info")
        self.dangerInfoLayout = QHBoxLayout(self.danger_card_info)
        self.dangerInfoLayout.setSpacing(12)
        self.dangerInfoLayout.setObjectName(u"dangerInfoLayout")
        self.dangerInfoLayout.setContentsMargins(18, 16, 18, 16)
        self.dangerInfoIcon = QLabel(self.danger_card_info)
        self.dangerInfoIcon.setObjectName(u"dangerInfoIcon")
        self.dangerInfoIcon.setMinimumSize(QSize(32, 32))
        self.dangerInfoIcon.setMaximumSize(QSize(32, 32))
        self.dangerInfoIcon.setStyleSheet(u"background: #fde68a; color: #92400e; border-radius: 8px; font-size: 16px; font-weight: 800;")
        self.dangerInfoIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dangerInfoLayout.addWidget(self.dangerInfoIcon)

        self.dangerInfoText = QVBoxLayout()
        self.dangerInfoText.setSpacing(2)
        self.dangerInfoText.setObjectName(u"dangerInfoText")
        self.dangerInfoTitle = QLabel(self.danger_card_info)
        self.dangerInfoTitle.setObjectName(u"dangerInfoTitle")
        self.dangerInfoTitle.setStyleSheet(u"color: #92400e; font-size: 13px; font-weight: 800;")

        self.dangerInfoText.addWidget(self.dangerInfoTitle)

        self.dangerInfoDesc = QLabel(self.danger_card_info)
        self.dangerInfoDesc.setObjectName(u"dangerInfoDesc")
        self.dangerInfoDesc.setStyleSheet(u"color: #a16207; font-size: 11px;")
        self.dangerInfoDesc.setWordWrap(True)

        self.dangerInfoText.addWidget(self.dangerInfoDesc)


        self.dangerInfoLayout.addLayout(self.dangerInfoText)


        self.scrollDangerLayout.addWidget(self.danger_card_info)

        self.danger_card_warn = QFrame(self.scrollDangerContent)
        self.danger_card_warn.setObjectName(u"danger_card_warn")
        self.dangerExportLayout = QHBoxLayout(self.danger_card_warn)
        self.dangerExportLayout.setSpacing(16)
        self.dangerExportLayout.setObjectName(u"dangerExportLayout")
        self.dangerExportLayout.setContentsMargins(20, 18, 20, 18)
        self.dangerExportIcon = QLabel(self.danger_card_warn)
        self.dangerExportIcon.setObjectName(u"dangerExportIcon")
        self.dangerExportIcon.setMinimumSize(QSize(36, 36))
        self.dangerExportIcon.setMaximumSize(QSize(36, 36))
        self.dangerExportIcon.setStyleSheet(u"background: #dbeafe; color: #023E8A; border-radius: 10px; font-size: 18px; font-weight: 800;")
        self.dangerExportIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dangerExportLayout.addWidget(self.dangerExportIcon)

        self.dangerExportText = QVBoxLayout()
        self.dangerExportText.setSpacing(3)
        self.dangerExportText.setObjectName(u"dangerExportText")
        self.dangerExportTitle = QLabel(self.danger_card_warn)
        self.dangerExportTitle.setObjectName(u"dangerExportTitle")
        self.dangerExportTitle.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 800;")

        self.dangerExportText.addWidget(self.dangerExportTitle)

        self.dangerExportDesc = QLabel(self.danger_card_warn)
        self.dangerExportDesc.setObjectName(u"dangerExportDesc")
        self.dangerExportDesc.setStyleSheet(u"color: #64748b; font-size: 11px;")
        self.dangerExportDesc.setWordWrap(True)

        self.dangerExportText.addWidget(self.dangerExportDesc)


        self.dangerExportLayout.addLayout(self.dangerExportText)

        self.btn_export_db = QPushButton(self.danger_card_warn)
        self.btn_export_db.setObjectName(u"btn_export_db")
        self.btn_export_db.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.dangerExportLayout.addWidget(self.btn_export_db)


        self.scrollDangerLayout.addWidget(self.danger_card_warn)

        self.danger_card_warn1 = QFrame(self.scrollDangerContent)
        self.danger_card_warn1.setObjectName(u"danger_card_warn1")
        self.dangerRestoreLayout = QHBoxLayout(self.danger_card_warn1)
        self.dangerRestoreLayout.setSpacing(16)
        self.dangerRestoreLayout.setObjectName(u"dangerRestoreLayout")
        self.dangerRestoreLayout.setContentsMargins(20, 18, 20, 18)
        self.dangerRestoreIcon = QLabel(self.danger_card_warn1)
        self.dangerRestoreIcon.setObjectName(u"dangerRestoreIcon")
        self.dangerRestoreIcon.setMinimumSize(QSize(36, 36))
        self.dangerRestoreIcon.setMaximumSize(QSize(36, 36))
        self.dangerRestoreIcon.setStyleSheet(u"background: #fde68a; color: #92400e; border-radius: 10px; font-size: 18px; font-weight: 800;")
        self.dangerRestoreIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dangerRestoreLayout.addWidget(self.dangerRestoreIcon)

        self.dangerRestoreText = QVBoxLayout()
        self.dangerRestoreText.setSpacing(3)
        self.dangerRestoreText.setObjectName(u"dangerRestoreText")
        self.dangerRestoreTitle = QLabel(self.danger_card_warn1)
        self.dangerRestoreTitle.setObjectName(u"dangerRestoreTitle")
        self.dangerRestoreTitle.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 800;")

        self.dangerRestoreText.addWidget(self.dangerRestoreTitle)

        self.dangerRestoreDesc = QLabel(self.danger_card_warn1)
        self.dangerRestoreDesc.setObjectName(u"dangerRestoreDesc")
        self.dangerRestoreDesc.setStyleSheet(u"color: #64748b; font-size: 11px;")
        self.dangerRestoreDesc.setWordWrap(True)

        self.dangerRestoreText.addWidget(self.dangerRestoreDesc)


        self.dangerRestoreLayout.addLayout(self.dangerRestoreText)

        self.btn_restore_db = QPushButton(self.danger_card_warn1)
        self.btn_restore_db.setObjectName(u"btn_restore_db")
        self.btn_restore_db.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.dangerRestoreLayout.addWidget(self.btn_restore_db)


        self.scrollDangerLayout.addWidget(self.danger_card_warn1)

        self.danger_card_danger = QFrame(self.scrollDangerContent)
        self.danger_card_danger.setObjectName(u"danger_card_danger")
        self.dangerResetLayout = QHBoxLayout(self.danger_card_danger)
        self.dangerResetLayout.setSpacing(16)
        self.dangerResetLayout.setObjectName(u"dangerResetLayout")
        self.dangerResetLayout.setContentsMargins(20, 18, 20, 18)
        self.dangerResetIcon = QLabel(self.danger_card_danger)
        self.dangerResetIcon.setObjectName(u"dangerResetIcon")
        self.dangerResetIcon.setMinimumSize(QSize(36, 36))
        self.dangerResetIcon.setMaximumSize(QSize(36, 36))
        self.dangerResetIcon.setStyleSheet(u"background: #fecaca; color: #b91c1c; border-radius: 10px; font-size: 20px; font-weight: 800;")
        self.dangerResetIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dangerResetLayout.addWidget(self.dangerResetIcon)

        self.dangerResetText = QVBoxLayout()
        self.dangerResetText.setSpacing(3)
        self.dangerResetText.setObjectName(u"dangerResetText")
        self.dangerResetTitle = QLabel(self.danger_card_danger)
        self.dangerResetTitle.setObjectName(u"dangerResetTitle")
        self.dangerResetTitle.setStyleSheet(u"color: #b91c1c; font-size: 13px; font-weight: 800;")

        self.dangerResetText.addWidget(self.dangerResetTitle)

        self.dangerResetDesc = QLabel(self.danger_card_danger)
        self.dangerResetDesc.setObjectName(u"dangerResetDesc")
        self.dangerResetDesc.setStyleSheet(u"color: #991b1b; font-size: 11px;")
        self.dangerResetDesc.setWordWrap(True)

        self.dangerResetText.addWidget(self.dangerResetDesc)


        self.dangerResetLayout.addLayout(self.dangerResetText)

        self.btn_reset_all = QPushButton(self.danger_card_danger)
        self.btn_reset_all.setObjectName(u"btn_reset_all")
        self.btn_reset_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.dangerResetLayout.addWidget(self.btn_reset_all)


        self.scrollDangerLayout.addWidget(self.danger_card_danger)

        self.spacerDanger = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.scrollDangerLayout.addItem(self.spacerDanger)

        self.scrollDanger.setWidget(self.scrollDangerContent)

        self.tabDangerLayout.addWidget(self.scrollDanger)

        self.tabs.addTab(self.tab_danger, "")

        self.card_layout.addWidget(self.tabs)

        self.footer_frame = QFrame(self.card)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setMinimumSize(QSize(0, 80))
        self.footer_frame.setMaximumSize(QSize(16777215, 80))
        self.footer_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.footerLayout = QHBoxLayout(self.footer_frame)
        self.footerLayout.setSpacing(12)
        self.footerLayout.setObjectName(u"footerLayout")
        self.footerLayout.setContentsMargins(28, 18, 28, 18)
        self.lbl_status = QLabel(self.footer_frame)
        self.lbl_status.setObjectName(u"lbl_status")
        self.lbl_status.setStyleSheet(u"color: #94a3b8; font-size: 11px; font-weight: 600;")

        self.footerLayout.addWidget(self.lbl_status)

        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerLayout.addItem(self.footerSpacer)

        self.btn_reload = QPushButton(self.footer_frame)
        self.btn_reload.setObjectName(u"btn_reload")
        self.btn_reload.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.footerLayout.addWidget(self.btn_reload)

        self.btn_save = QPushButton(self.footer_frame)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.footerLayout.addWidget(self.btn_save)


        self.card_layout.addWidget(self.footer_frame)


        self.root_layout.addWidget(self.card)


        self.retranslateUi(PageParametres)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PageParametres)
    # setupUi

    def retranslateUi(self, PageParametres):
        self.header_icon.setText("")
        self.page_title.setText(QCoreApplication.translate("PageParametres", u"Param\u00e8tres", None))
        self.page_subtitle.setText(QCoreApplication.translate("PageParametres", u"Configurez le comportement de l'application, la facturation et la s\u00e9curit\u00e9.", None))
        self.version_badge.setText(QCoreApplication.translate("PageParametres", u"NOVA PHARMA v2.0.0", None))
        self.secIdIcon.setText(QCoreApplication.translate("PageParametres", u"01", None))
        self.secIdTitle.setText(QCoreApplication.translate("PageParametres", u"Identit\u00e9 de l'officine", None))
        self.secIdHint.setText(QCoreApplication.translate("PageParametres", u"Ces informations apparaissent sur les factures", None))
        self.lbl_nom.setText(QCoreApplication.translate("PageParametres", u"NOM DE LA PHARMACIE", None))
        self.edit_nom.setPlaceholderText(QCoreApplication.translate("PageParametres", u"Ex : Pharmacie Bonne Sant\u00e9", None))
        self.lbl_type.setText(QCoreApplication.translate("PageParametres", u"TYPE D'OFFICINE", None))
        self.combo_type.setItemText(0, QCoreApplication.translate("PageParametres", u"PETITE", None))
        self.combo_type.setItemText(1, QCoreApplication.translate("PageParametres", u"MOYENNE", None))
        self.combo_type.setItemText(2, QCoreApplication.translate("PageParametres", u"GRANDE", None))

        self.secContactIcon.setText(QCoreApplication.translate("PageParametres", u"02", None))
        self.secContactTitle.setText(QCoreApplication.translate("PageParametres", u"Coordonn\u00e9es", None))
        self.lbl_tel.setText(QCoreApplication.translate("PageParametres", u"T\u00c9L\u00c9PHONE", None))
        self.edit_tel.setPlaceholderText(QCoreApplication.translate("PageParametres", u"Ex : +243 800 000 000", None))
        self.lbl_email_ent.setText(QCoreApplication.translate("PageParametres", u"EMAIL", None))
        self.edit_email_ent.setPlaceholderText(QCoreApplication.translate("PageParametres", u"Ex : contact@pharmacie.cd", None))
        self.lbl_adresse.setText(QCoreApplication.translate("PageParametres", u"ADRESSE COMPL\u00c8TE", None))
        self.edit_adresse.setPlaceholderText(QCoreApplication.translate("PageParametres", u"Ex : Avenue Kasa-Vubu, n\u00b0123, Kinshasa/Gombe", None))
        self.secLogoIcon.setText(QCoreApplication.translate("PageParametres", u"03", None))
        self.secLogoTitle.setText(QCoreApplication.translate("PageParametres", u"Logo de la pharmacie", None))
        self.logo_preview.setText(QCoreApplication.translate("PageParametres", u"Logo", None))
        self.lbl_logo_title.setText(QCoreApplication.translate("PageParametres", u"Format recommand\u00e9 : PNG ou JPG, carr\u00e9 200\u00d7200 px", None))
        self.lbl_logo_hint.setText(QCoreApplication.translate("PageParametres", u"Ce logo appara\u00eetra en en-t\u00eate des factures imprim\u00e9es et des rapports PDF.", None))
        self.btn_upload_logo.setText(QCoreApplication.translate("PageParametres", u"Changer le logo", None))
        self.btn_remove_logo.setText(QCoreApplication.translate("PageParametres", u"Supprimer", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_entreprise), QCoreApplication.translate("PageParametres", u"Entreprise", None))
        self.secVenteIcon.setText(QCoreApplication.translate("PageParametres", u"01", None))
        self.secVenteTitle.setText(QCoreApplication.translate("PageParametres", u"Param\u00e8tres de vente", None))
        self.lbl_seuil_desc.setText(QCoreApplication.translate("PageParametres", u"Quantit\u00e9 minimale avant qu'un produit soit consid\u00e9r\u00e9 \"en rupture\". Utilis\u00e9 pour les alertes et le filtre sur la page Articles.", None))
        self.lbl_periode_ca.setText(QCoreApplication.translate("PageParametres", u"P\u00c9RIODE DU CHIFFRE D'AFFAIRES", None))
        self.combo_devise.setItemText(0, QCoreApplication.translate("PageParametres", u"FC", None))
        self.combo_devise.setItemText(1, QCoreApplication.translate("PageParametres", u"CDF", None))
        self.combo_devise.setItemText(2, QCoreApplication.translate("PageParametres", u"USD", None))
        self.combo_devise.setItemText(3, QCoreApplication.translate("PageParametres", u"EUR", None))

        self.spin_max_postes.setSuffix(QCoreApplication.translate("PageParametres", u" postes", None))
        self.lbl_taux_change.setText(QCoreApplication.translate("PageParametres", u"TAUX DE CHANGE (1 USD =)", None))
#if QT_CONFIG(tooltip)
        self.spin_taux_change.setToolTip(QCoreApplication.translate("PageParametres", u"Modifiable uniquement par un administrateur", None))
#endif // QT_CONFIG(tooltip)
        self.spin_taux_change.setSuffix(QCoreApplication.translate("PageParametres", u" FC", None))
        self.lbl_caisse.setText(QCoreApplication.translate("PageParametres", u"CODE CAISSE PAR D\u00c9FAUT", None))
        self.lbl_devise.setText(QCoreApplication.translate("PageParametres", u"DEVISE AFFICH\u00c9E", None))
        self.combo_periode_ca.setItemText(0, QCoreApplication.translate("PageParametres", u"Mois", None))
        self.combo_periode_ca.setItemText(1, QCoreApplication.translate("PageParametres", u"Semaine", None))

        self.lbl_max_postes.setText(QCoreApplication.translate("PageParametres", u"NOMBRE MAX DE POSTES CONNECT\u00c9S", None))
        self.lbl_marge.setText(QCoreApplication.translate("PageParametres", u"MARGE B\u00c9N\u00c9FICIAIRE PAR D\u00c9FAUT", None))
        self.edit_caisse.setPlaceholderText(QCoreApplication.translate("PageParametres", u"Ex : 01", None))
        self.spin_seuil_stock.setSuffix(QCoreApplication.translate("PageParametres", u"unit\u00e9s", None))
        self.spin_marge.setSuffix(QCoreApplication.translate("PageParametres", u"%", None))
        self.lbl_seuil_title.setText(QCoreApplication.translate("PageParametres", u"SEUIL D'ALERTE STOCK", None))
        self.lbl_info_caisse.setText(QCoreApplication.translate("PageParametres", u"Le code caisse est utilis\u00e9 dans les num\u00e9ros de facture. Il doit contenir 1 \u00e0 2 chiffres. Exemple : F01-2026-000000001 (caisse 01), F02-2026-000000001 (caisse 02).", None))
        self.lbl_info_taux.setText(QCoreApplication.translate("PageParametres", u"Le taux de change est utilis\u00e9 pour afficher l'\u00e9quivalent USD des montants en FC. Modifiable uniquement par un administrateur (ou via Ctrl+Alt+T).", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_vente), QCoreApplication.translate("PageParametres", u"Vente & Devise", None))
        self.secFactIcon.setText(QCoreApplication.translate("PageParametres", u"01", None))
        self.secFactTitle.setText(QCoreApplication.translate("PageParametres", u"Comportement d'impression", None))
        self.chk_impression_auto.setText(QCoreApplication.translate("PageParametres", u"Imprimer automatiquement les factures apr\u00e8s validation", None))
        self.chk_qrcode.setText(QCoreApplication.translate("PageParametres", u"Afficher un QR code sur les factures (v\u00e9rification d'authenticit\u00e9)", None))
        self.secMentionsIcon.setText(QCoreApplication.translate("PageParametres", u"02", None))
        self.secMentionsTitle.setText(QCoreApplication.translate("PageParametres", u"Mentions sur le ticket", None))
        self.lbl_mentions_hint.setText(QCoreApplication.translate("PageParametres", u"Une mention par ligne", None))
        self.edit_mentions.setPlaceholderText(QCoreApplication.translate("PageParametres", u"Les m\u00e9dicaments vendus ne sont ni repris ni \u00e9chang\u00e9s \u00c0 conserver hors de la port\u00e9e des enfants Signature ou cachet de la pharmacie", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_facturation), QCoreApplication.translate("PageParametres", u"Facturation", None))
        self.secSaveIcon.setText(QCoreApplication.translate("PageParametres", u"01", None))
        self.secSaveTitle.setText(QCoreApplication.translate("PageParametres", u"Sauvegarde automatique", None))
        self.chk_sauvegarde_auto.setText(QCoreApplication.translate("PageParametres", u"Activer la sauvegarde automatique de la base de donn\u00e9es", None))
        self.lbl_freq_save.setText(QCoreApplication.translate("PageParametres", u"FR\u00c9QUENCE (JOURS)", None))
        self.lbl_max_save.setText(QCoreApplication.translate("PageParametres", u"SAUVEGARDES MAXIMUM CONSERV\u00c9ES", None))
        self.lbl_save_info.setText(QCoreApplication.translate("PageParametres", u"Les sauvegardes quotidiennes / hebdomadaires / mensuelles / annuelles sont d\u00e9clench\u00e9es au lancement de l'application. Elles sont prot\u00e9g\u00e9es par un mot de passe d\u00e9riv\u00e9 de cette machine.", None))
        self.secBackupIcon.setText(QCoreApplication.translate("PageParametres", u"02", None))
        self.secBackupTitle.setText(QCoreApplication.translate("PageParametres", u"Emplacements de sauvegarde", None))
        self.btn_manage_backups.setText(QCoreApplication.translate("PageParametres", u"G\u00e9rer les archives", None))
        self.lbl_dossier_save.setText(QCoreApplication.translate("PageParametres", u"DOSSIER PRINCIPAL DE SAUVEGARDE", None))
        self.edit_dossier_save.setPlaceholderText(QCoreApplication.translate("PageParametres", u"~/Documents/NovaPharma/Backups", None))
        self.btn_browse_save.setText(QCoreApplication.translate("PageParametres", u"Parcourir\u2026", None))
        self.chk_backup_secondary.setText(QCoreApplication.translate("PageParametres", u"Activer la copie de secours hors-site (cl\u00e9 USB / NAS / dossier r\u00e9seau)", None))
        self.lbl_backup_secondary.setText(QCoreApplication.translate("PageParametres", u"DOSSIER SECONDAIRE (HORS-SITE)", None))
        self.edit_backup_secondary.setPlaceholderText(QCoreApplication.translate("PageParametres", u"Ex : E:/NovaPharma-Backups ou /mnt/usb/backups", None))
        self.btn_browse_backup_secondary.setText(QCoreApplication.translate("PageParametres", u"Parcourir\u2026", None))
        self.lbl_backup_secondary_info.setText(QCoreApplication.translate("PageParametres", u"Le dossier secondaire doit \u00eatre sur un support physique diff\u00e9rent (cl\u00e9 USB d\u00e9di\u00e9e, NAS r\u00e9seau). Si la cl\u00e9 est d\u00e9branch\u00e9e, la copie est ignor\u00e9e mais le backup principal reste cr\u00e9\u00e9.", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_sauvegarde), QCoreApplication.translate("PageParametres", u"Sauvegarde", None))
        self.secSecuIcon.setText(QCoreApplication.translate("PageParametres", u"01", None))
        self.secSecuTitle.setText(QCoreApplication.translate("PageParametres", u"Politique de mot de passe", None))
        self.lbl_pwd_min.setText(QCoreApplication.translate("PageParametres", u"LONGUEUR MINIMALE (CARACT\u00c8RES)", None))
        self.lbl_pwd_exp.setText(QCoreApplication.translate("PageParametres", u"EXPIRATION (JOURS, 0 = JAMAIS)", None))
        self.lbl_complexite.setText(QCoreApplication.translate("PageParametres", u"COMPLEXIT\u00c9 REQUISE", None))
        self.chk_require_digit.setText(QCoreApplication.translate("PageParametres", u"Exiger au moins un chiffre", None))
        self.chk_require_upper.setText(QCoreApplication.translate("PageParametres", u"Exiger au moins une lettre majuscule", None))
        self.chk_require_special.setText(QCoreApplication.translate("PageParametres", u"Exiger au moins un caract\u00e8re sp\u00e9cial (!@#$\u2026)", None))
        self.lbl_secu_info.setText(QCoreApplication.translate("PageParametres", u"Ces r\u00e8gles s'appliquent uniquement aux NOUVEAUX mots de passe. Les mots de passe existants ne sont pas affect\u00e9s.", None))
        self.lbl_seuil_title_4.setText(QCoreApplication.translate("PageParametres", u"S\u00c9CURIT\u00c9 RENFORC\u00c9E", None))
        self.chk_backup_urgence.setText(QCoreApplication.translate("PageParametres", u"Cr\u00e9er une sauvegarde d'urgence automatique avant chaque action critique", None))
        self.chk_allow_admin_client.setText(QCoreApplication.translate("PageParametres", u"Autoriser les connexions ADMIN/OWNER/DEV depuis un poste client (recommand\u00e9 : D\u00c9SACTIV\u00c9 en production)", None))
        self.secMonitoringIcon.setText(QCoreApplication.translate("PageParametres", u"02", None))
        self.secMonitoringTitle.setText(QCoreApplication.translate("PageParametres", u"PC de monitoring", None))
        self.monitoring_count_badge.setText(QCoreApplication.translate("PageParametres", u"0 / 3", None))
        self.monitoring_client_info.setText(QCoreApplication.translate("PageParametres", u"La whitelist ne peut \u00eatre modifi\u00e9e que depuis le serveur physique.", None))
        self.lbl_monitoring_role.setText(QCoreApplication.translate("PageParametres", u"R\u00f4le autoris\u00e9 :", None))
        self.combo_monitoring_role.setItemText(0, QCoreApplication.translate("PageParametres", u"Tous (OWNER + ADMIN + DEV)", None))
        self.combo_monitoring_role.setItemText(1, QCoreApplication.translate("PageParametres", u"OWNER uniquement", None))
        self.combo_monitoring_role.setItemText(2, QCoreApplication.translate("PageParametres", u"ADMIN uniquement", None))
        self.combo_monitoring_role.setItemText(3, QCoreApplication.translate("PageParametres", u"DEV uniquement", None))

        self.btn_add_monitoring.setText(QCoreApplication.translate("PageParametres", u"Ajouter ce PC", None))
        self.btn_refresh_monitoring.setText(QCoreApplication.translate("PageParametres", u"Actualiser", None))
        ___qtablewidgetitem = self.table_monitoring.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageParametres", u"Machine ID", None))
        ___qtablewidgetitem1 = self.table_monitoring.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageParametres", u"Hostname", None))
        ___qtablewidgetitem2 = self.table_monitoring.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageParametres", u"R\u00f4le autoris\u00e9", None))
        ___qtablewidgetitem3 = self.table_monitoring.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageParametres", u"Ajout\u00e9e le", None))
        ___qtablewidgetitem4 = self.table_monitoring.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PageParametres", u"Statut", None))
        self.lbl_monitoring_empty.setText(QCoreApplication.translate("PageParametres", u"Aucun PC autoris\u00e9. Cliquez sur \u00ab Ajouter ce PC \u00bb pour whitelister cette machine.", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_securite), QCoreApplication.translate("PageParametres", u"S\u00e9curit\u00e9", None))
        self.secPrinterTicketIcon.setText(QCoreApplication.translate("PageParametres", u"01", None))
        self.secPrinterTicketTitle.setText(QCoreApplication.translate("PageParametres", u"Imprimante TICKET (factures)", None))
        self.lbl_printer_ticket_desc.setText(QCoreApplication.translate("PageParametres", u"Imprimante thermique 80mm utilis\u00e9e pour les tickets de caisse. Configuration enregistr\u00e9e sur ce poste uniquement.", None))
        self.btn_refresh_printers_ticket.setText(QCoreApplication.translate("PageParametres", u"Actualiser", None))
        self.btn_test_print_ticket.setText(QCoreApplication.translate("PageParametres", u"Test ticket", None))
        self.secPrinterReportIcon.setText(QCoreApplication.translate("PageParametres", u"02", None))
        self.secPrinterReportTitle.setText(QCoreApplication.translate("PageParametres", u"Imprimante RAPPORT (A4)", None))
        self.lbl_printer_report_desc.setText(QCoreApplication.translate("PageParametres", u"Imprimante A4 utilis\u00e9e pour les rapports, Rapports Z (format A4) et exports PDF. Configuration enregistr\u00e9e sur ce poste uniquement.", None))
        self.btn_test_print_report.setText(QCoreApplication.translate("PageParametres", u"Test rapport", None))
        self.secPrintAutoIcon.setText(QCoreApplication.translate("PageParametres", u"03", None))
        self.secPrintAutoTitle.setText(QCoreApplication.translate("PageParametres", u"Impression automatique", None))
        self.chk_auto_print.setText(QCoreApplication.translate("PageParametres", u"Imprimer automatiquement les TICKETS apr\u00e8s chaque vente (sans dialogue)", None))
        self.chk_auto_print_report.setText(QCoreApplication.translate("PageParametres", u"Imprimer automatiquement les RAPPORTS (PDF) apr\u00e8s g\u00e9n\u00e9ration", None))
        self.chk_auto_open_pdf.setText(QCoreApplication.translate("PageParametres", u"Ouvrir automatiquement le PDF apr\u00e8s g\u00e9n\u00e9ration", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_imprimantes), QCoreApplication.translate("PageParametres", u"  Impression  ", None))
        self.dangerInfoIcon.setText(QCoreApplication.translate("PageParametres", u"!", None))
        self.dangerInfoTitle.setText(QCoreApplication.translate("PageParametres", u"Zone r\u00e9serv\u00e9e aux administrateurs", None))
        self.dangerInfoDesc.setText(QCoreApplication.translate("PageParametres", u"Ces actions sont irr\u00e9versibles. Elles n\u00e9cessitent une confirmation \u00e0 plusieurs \u00e9tapes.", None))
        self.dangerExportIcon.setText(QCoreApplication.translate("PageParametres", u"\u2193", None))
        self.dangerExportTitle.setText(QCoreApplication.translate("PageParametres", u"Exporter la base de donn\u00e9es", None))
        self.dangerExportDesc.setText(QCoreApplication.translate("PageParametres", u"Cr\u00e9e une copie de la base compl\u00e8te pour archivage ou migration.", None))
        self.btn_export_db.setText(QCoreApplication.translate("PageParametres", u"Exporter\u2026", None))
        self.dangerRestoreIcon.setText(QCoreApplication.translate("PageParametres", u"\u2191", None))
        self.dangerRestoreTitle.setText(QCoreApplication.translate("PageParametres", u"Restaurer une sauvegarde", None))
        self.dangerRestoreDesc.setText(QCoreApplication.translate("PageParametres", u"Remplace la base actuelle par une sauvegarde. Une sauvegarde de s\u00e9curit\u00e9 est cr\u00e9\u00e9e avant l'op\u00e9ration.", None))
        self.btn_restore_db.setText(QCoreApplication.translate("PageParametres", u"Restaurer\u2026", None))
        self.dangerResetIcon.setText(QCoreApplication.translate("PageParametres", u"\u00d7", None))
        self.dangerResetTitle.setText(QCoreApplication.translate("PageParametres", u"R\u00e9initialisation compl\u00e8te", None))
        self.dangerResetDesc.setText(QCoreApplication.translate("PageParametres", u"Supprime TOUTES les donn\u00e9es : produits, clients, ventes, utilisateurs, historique. L'application revient \u00e0 son \u00e9tat initial.", None))
        self.btn_reset_all.setText(QCoreApplication.translate("PageParametres", u"Tout r\u00e9initialiser", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_danger), QCoreApplication.translate("PageParametres", u"Danger Zone", None))
        self.lbl_status.setText(QCoreApplication.translate("PageParametres", u"Modifiez un param\u00e8tre puis cliquez sur Enregistrer.", None))
        self.btn_reload.setText(QCoreApplication.translate("PageParametres", u"Recharger", None))
        self.btn_save.setText(QCoreApplication.translate("PageParametres", u"Enregistrer les modifications", None))
        pass
    # retranslateUi

