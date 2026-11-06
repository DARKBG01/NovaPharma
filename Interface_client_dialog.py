# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_client_dialogsnMdNN.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(987, 797)
        Dialog.setMinimumSize(QSize(820, 620))
        Dialog.setStyleSheet(u"/* ============================================================\n"
"   NOVA PHARMA \u2014 DIALOG CLIENT (ajout / modification)\n"
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
"QFrame#brand_badge {\n"
"    background: rgba(255,255,255,0.18);\n"
"    border: 1px solid rgba(255,255,255,0.28);\n"
"    border-radius: 14px;\n"
"}\n"
"QLa"
                        "bel#brand_badge_text {\n"
"    color: #ffffff;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1.5px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#sidebar_title {\n"
"    color: #ffffff;\n"
"    font-size: 24px;\n"
"    font-weight: 800;\n"
"    letter-spacing: -0.5px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#sidebar_lead {\n"
"    color: #CAF0F8;\n"
"    font-size: 12px;\n"
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
"QFrame#check_row[done=\"true\"] QLabel#check_text { color: #ffffff; }\n"
"\n"
"QLabel#progress_label {\n"
"    color: #ffff"
                        "ff;\n"
"    font-size: 12px;\n"
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
"    color: #0f172"
                        "a;\n"
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
"    background: transparent;\n"
"}\n"
"QLabel#field_opt {\n"
"    color: #0"
                        "077B6;\n"
"    font-size: 10px;\n"
"    font-weight: 700;\n"
"    background-color: #e0f7fa;\n"
"    border-radius: 8px;\n"
"    padding: 2px 8px;\n"
"}\n"
"\n"
"QLineEdit, QTextEdit,QComboBox {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 10px 14px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    selection-background-color: #bfdbfe;\n"
"}\n"
"QLineEdit:hover, QTextEdit:hover, QComboBox:hover { border-color: #b9c6d8; }\n"
"QLineEdit:focus, QTextEdit:focus, QComboBox:focus {\n"
"    background-color: #ffffff;\n"
"    border: 1.5px solid #0077B6;\n"
"}\n"
"\n"
"QComboBox::drop-down { border: none; width: 26px; }\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    selection-backgr"
                        "ound-color: #eff6ff;\n"
"    selection-color: #0077B6;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background-color: #f1f5f9;\n"
"    color: #94a3b8;\n"
"    border-color: #e6ebf2;\n"
"}\n"
"\n"
"/* Toggle anonymat */\n"
"QFrame#anon_box {\n"
"    background-color: #f0f9ff;\n"
"    border: 1.5px solid #bae6fd;\n"
"    border-radius: 12px;\n"
"}\n"
"QFrame#anon_box[on=\"true\"] {\n"
"    background-color: #fef3c7;\n"
"    border: 1.5px solid #fcd34d;\n"
"}\n"
"QCheckBox#anon_check {\n"
"    color: #0369a1;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    spacing: 10px;\n"
"    background: transparent;\n"
"}\n"
"QCheckBox#anon_check::indicator {\n"
"    width: 22px; height: 22px;\n"
"    border: 2px solid #bae6fd;\n"
"    border-radius: 6px;\n"
"    background-color: #ffffff;\n"
"}\n"
"QCheckBox#anon_check::indicator:checked {\n"
"    background-color: #d97706;\n"
"    border: 2px solid #d97706;\n"
"    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmll"
                        "d0JveD0iMCAwIDEwIDgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEgNEwzLjUgNi41TDkgMSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L3N2Zz4=);\n"
"}\n"
"QLabel#anon_hint {\n"
"    color: #0284c7;\n"
"    font-size: 11px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* Bandeau info anonyme */\n"
"QFrame#anon_banner {\n"
"    background-color: #fef3c7;\n"
"    border: 1px solid #fcd34d;\n"
"    border-left: 4px solid #d97706;\n"
"    border-radius: 10px;\n"
"}\n"
"QLabel#anon_banner_text {\n"
"    color: #92400e;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* Erreur */\n"
"QFrame#error_box {\n"
"    background-color: #fef2f2;\n"
"    border: 1px solid #fecaca;\n"
"    border-left: 4px solid #dc2626;\n"
"    border-radius: 10px;\n"
"}\n"
"QLabel#label_error {\n"
"    color: #991b1b;\n"
"    font-size: 12px;\n"
"    font-weight: 600;\n"
"    background:"
                        " transparent;\n"
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
"    min-height: 44px;\n"
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
"}\n"
"QPushButton#btn_save:hover {\n"
"    background: qlinea"
                        "rgradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"QPushButton#btn_save:pressed { background: #023E8A; }\n"
"\n"
"/* Scroll */\n"
"QScrollArea { background-color: transparent; border: none; }\n"
"QScrollArea > QWidget > QWidget { background-color: #ffffff; }\n"
"QScrollBar:vertical { border: none; background: transparent; width: 10px; margin: 2px; }\n"
"QScrollBar::handle:vertical { background: #cbd5e1; min-height: 32px; border-radius: 5px; }\n"
"QScrollBar::handle:vertical:hover { background: #94a3b8; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }\n"
"")
        self.root_layout = QHBoxLayout(Dialog)
        self.root_layout.setSpacing(0)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.sidebar = QFrame(Dialog)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(280, 0))
        self.sidebar.setMaximumSize(QSize(280, 16777215))
        self.sidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setSpacing(14)
        self.sidebar_layout.setObjectName(u"sidebar_layout")
        self.sidebar_layout.setContentsMargins(28, 32, 28, 24)
        self.brand_badge = QFrame(self.sidebar)
        self.brand_badge.setObjectName(u"brand_badge")
        self.brand_badge.setMinimumSize(QSize(0, 32))
        self.brand_badge.setMaximumSize(QSize(16777215, 32))
        self.brand_badge.setFrameShape(QFrame.Shape.NoFrame)
        self.brand_badge_layout = QHBoxLayout(self.brand_badge)
        self.brand_badge_layout.setSpacing(8)
        self.brand_badge_layout.setObjectName(u"brand_badge_layout")
        self.brand_badge_layout.setContentsMargins(14, 0, 14, 0)
        self.brand_badge_icon = QLabel(self.brand_badge)
        self.brand_badge_icon.setObjectName(u"brand_badge_icon")
        self.brand_badge_icon.setMinimumSize(QSize(14, 14))
        self.brand_badge_icon.setMaximumSize(QSize(14, 14))
        self.brand_badge_icon.setPixmap(QPixmap(u":/Icon/Icons/users_white.svg"))
        self.brand_badge_icon.setScaledContents(True)

        self.brand_badge_layout.addWidget(self.brand_badge_icon)

        self.brand_badge_text = QLabel(self.brand_badge)
        self.brand_badge_text.setObjectName(u"brand_badge_text")

        self.brand_badge_layout.addWidget(self.brand_badge_text)

        self.brand_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.brand_badge_layout.addItem(self.brand_spacer)


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

        self.check_row_phone = QFrame(self.sidebar)
        self.check_row_phone.setObjectName(u"check_row_phone")
        self.check_row_phone.setMinimumSize(QSize(0, 42))
        self.check_row_phone.setMaximumSize(QSize(16777215, 42))
        self.check_row_phone.setFrameShape(QFrame.Shape.NoFrame)
        self.check_phone_layout = QHBoxLayout(self.check_row_phone)
        self.check_phone_layout.setSpacing(10)
        self.check_phone_layout.setObjectName(u"check_phone_layout")
        self.check_phone_layout.setContentsMargins(12, 0, 12, 0)
        self.check_phone_icon = QLabel(self.check_row_phone)
        self.check_phone_icon.setObjectName(u"check_phone_icon")
        self.check_phone_icon.setMinimumSize(QSize(20, 20))
        self.check_phone_icon.setMaximumSize(QSize(20, 20))
        self.check_phone_icon.setPixmap(QPixmap(u":/Icon/Icons/circle_white.svg"))
        self.check_phone_icon.setScaledContents(True)

        self.check_phone_layout.addWidget(self.check_phone_icon)

        self.check_phone_text = QLabel(self.check_row_phone)
        self.check_phone_text.setObjectName(u"check_phone_text")
        self.check_phone_text.setStyleSheet(u"color: #e0e7ff; font-size: 12px; font-weight: 600; background: transparent;")

        self.check_phone_layout.addWidget(self.check_phone_text)

        self.phone_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.check_phone_layout.addItem(self.phone_spacer)


        self.sidebar_layout.addWidget(self.check_row_phone)

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
        self.panel_header_icon.setStyleSheet(u"background-color: #0077B6; border-radius: 12px; padding: 10px;")
        self.panel_header_icon.setPixmap(QPixmap(u":/Icon/Icons/user-plus_white.svg"))
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
        self.scroll_content.setGeometry(QRect(0, -23, 655, 628))
        self.scroll_content.setStyleSheet(u"background-color: #ffffff;")
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setSpacing(18)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(28, 22, 28, 22)
        self.anon_box = QFrame(self.scroll_content)
        self.anon_box.setObjectName(u"anon_box")
        self.anon_box.setMinimumSize(QSize(0, 60))
        self.anon_box.setFrameShape(QFrame.Shape.NoFrame)
        self.anon_layout = QHBoxLayout(self.anon_box)
        self.anon_layout.setSpacing(12)
        self.anon_layout.setObjectName(u"anon_layout")
        self.anon_layout.setContentsMargins(16, 10, 16, 10)
        self.anon_icon = QLabel(self.anon_box)
        self.anon_icon.setObjectName(u"anon_icon")
        self.anon_icon.setMinimumSize(QSize(20, 20))
        self.anon_icon.setMaximumSize(QSize(20, 20))
        self.anon_icon.setPixmap(QPixmap(u":/Icon/Icons/lock.svg"))
        self.anon_icon.setScaledContents(True)

        self.anon_layout.addWidget(self.anon_icon)

        self.anon_check = QCheckBox(self.anon_box)
        self.anon_check.setObjectName(u"anon_check")
        self.anon_check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.anon_layout.addWidget(self.anon_check)

        self.anon_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.anon_layout.addItem(self.anon_spacer)

        self.anon_hint = QLabel(self.anon_box)
        self.anon_hint.setObjectName(u"anon_hint")

        self.anon_layout.addWidget(self.anon_hint)


        self.content_layout.addWidget(self.anon_box)

        self.anon_banner = QFrame(self.scroll_content)
        self.anon_banner.setObjectName(u"anon_banner")
        self.anon_banner.setVisible(False)
        self.anon_banner.setFrameShape(QFrame.Shape.NoFrame)
        self.anon_banner_layout = QHBoxLayout(self.anon_banner)
        self.anon_banner_layout.setSpacing(10)
        self.anon_banner_layout.setObjectName(u"anon_banner_layout")
        self.anon_banner_layout.setContentsMargins(14, 10, 14, 10)
        self.anon_banner_icon = QLabel(self.anon_banner)
        self.anon_banner_icon.setObjectName(u"anon_banner_icon")
        self.anon_banner_icon.setMinimumSize(QSize(18, 18))
        self.anon_banner_icon.setMaximumSize(QSize(18, 18))
        self.anon_banner_icon.setPixmap(QPixmap(u":/Icon/Icons/info.svg"))
        self.anon_banner_icon.setScaledContents(True)

        self.anon_banner_layout.addWidget(self.anon_banner_icon)

        self.anon_banner_text = QLabel(self.anon_banner)
        self.anon_banner_text.setObjectName(u"anon_banner_text")
        self.anon_banner_text.setWordWrap(True)

        self.anon_banner_layout.addWidget(self.anon_banner_text)


        self.content_layout.addWidget(self.anon_banner)

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


        self.layout_nom.addLayout(self.nom_label_layout)

        self.input_nom = QLineEdit(self.scroll_content)
        self.input_nom.setObjectName(u"input_nom")
        self.input_nom.setMinimumSize(QSize(0, 44))
        self.input_nom.setMaxLength(120)

        self.layout_nom.addWidget(self.input_nom)


        self.content_layout.addLayout(self.layout_nom)

        self.layout_nom_2 = QVBoxLayout()
        self.layout_nom_2.setSpacing(6)
        self.layout_nom_2.setObjectName(u"layout_nom_2")
        self.nom_label_layout_2 = QHBoxLayout()
        self.nom_label_layout_2.setSpacing(4)
        self.nom_label_layout_2.setObjectName(u"nom_label_layout_2")
        self.lbl_sexe = QLabel(self.scroll_content)
        self.lbl_sexe.setObjectName(u"lbl_sexe")
        self.lbl_sexe.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.nom_label_layout_2.addWidget(self.lbl_sexe)

        self.req_nom_2 = QLabel(self.scroll_content)
        self.req_nom_2.setObjectName(u"req_nom_2")
        self.req_nom_2.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.nom_label_layout_2.addWidget(self.req_nom_2)

        self.nom_label_spacer_2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.nom_label_layout_2.addItem(self.nom_label_spacer_2)


        self.layout_nom_2.addLayout(self.nom_label_layout_2)

        self.input_sexe = QComboBox(self.scroll_content)
        self.input_sexe.addItem("")
        self.input_sexe.addItem("")
        self.input_sexe.setObjectName(u"input_sexe")

        self.layout_nom_2.addWidget(self.input_sexe)


        self.content_layout.addLayout(self.layout_nom_2)

        self.row_contact = QHBoxLayout()
        self.row_contact.setSpacing(14)
        self.row_contact.setObjectName(u"row_contact")
        self.layout_numero = QVBoxLayout()
        self.layout_numero.setSpacing(6)
        self.layout_numero.setObjectName(u"layout_numero")
        self.numero_label_layout = QHBoxLayout()
        self.numero_label_layout.setSpacing(4)
        self.numero_label_layout.setObjectName(u"numero_label_layout")
        self.lbl_numero = QLabel(self.scroll_content)
        self.lbl_numero.setObjectName(u"lbl_numero")
        self.lbl_numero.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.numero_label_layout.addWidget(self.lbl_numero)

        self.req_numero = QLabel(self.scroll_content)
        self.req_numero.setObjectName(u"req_numero")
        self.req_numero.setStyleSheet(u"color: #dc2626; font-size: 13px; font-weight: 800;")

        self.numero_label_layout.addWidget(self.req_numero)

        self.numero_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.numero_label_layout.addItem(self.numero_label_spacer)


        self.layout_numero.addLayout(self.numero_label_layout)

        self.input_numero = QLineEdit(self.scroll_content)
        self.input_numero.setObjectName(u"input_numero")
        self.input_numero.setMinimumSize(QSize(0, 44))

        self.layout_numero.addWidget(self.input_numero)


        self.row_contact.addLayout(self.layout_numero)

        self.layout_email = QVBoxLayout()
        self.layout_email.setSpacing(6)
        self.layout_email.setObjectName(u"layout_email")
        self.email_label_layout = QHBoxLayout()
        self.email_label_layout.setSpacing(4)
        self.email_label_layout.setObjectName(u"email_label_layout")
        self.lbl_email = QLabel(self.scroll_content)
        self.lbl_email.setObjectName(u"lbl_email")
        self.lbl_email.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.email_label_layout.addWidget(self.lbl_email)

        self.email_opt = QLabel(self.scroll_content)
        self.email_opt.setObjectName(u"email_opt")
        self.email_opt.setStyleSheet(u"color: #0077B6; font-size: 10px; font-weight: 700; background: #e0f7fa; border-radius: 8px; padding: 2px 8px;")

        self.email_label_layout.addWidget(self.email_opt)

        self.email_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.email_label_layout.addItem(self.email_label_spacer)


        self.layout_email.addLayout(self.email_label_layout)

        self.input_email = QLineEdit(self.scroll_content)
        self.input_email.setObjectName(u"input_email")
        self.input_email.setMinimumSize(QSize(0, 44))

        self.layout_email.addWidget(self.input_email)


        self.row_contact.addLayout(self.layout_email)


        self.content_layout.addLayout(self.row_contact)

        self.layout_adresse = QVBoxLayout()
        self.layout_adresse.setSpacing(6)
        self.layout_adresse.setObjectName(u"layout_adresse")
        self.adresse_label_layout = QHBoxLayout()
        self.adresse_label_layout.setSpacing(4)
        self.adresse_label_layout.setObjectName(u"adresse_label_layout")
        self.lbl_adresse = QLabel(self.scroll_content)
        self.lbl_adresse.setObjectName(u"lbl_adresse")
        self.lbl_adresse.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.adresse_label_layout.addWidget(self.lbl_adresse)

        self.adresse_opt = QLabel(self.scroll_content)
        self.adresse_opt.setObjectName(u"adresse_opt")
        self.adresse_opt.setStyleSheet(u"color: #0077B6; font-size: 10px; font-weight: 700; background: #e0f7fa; border-radius: 8px; padding: 2px 8px;")

        self.adresse_label_layout.addWidget(self.adresse_opt)

        self.adresse_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.adresse_label_layout.addItem(self.adresse_label_spacer)


        self.layout_adresse.addLayout(self.adresse_label_layout)

        self.input_adresse = QLineEdit(self.scroll_content)
        self.input_adresse.setObjectName(u"input_adresse")
        self.input_adresse.setMinimumSize(QSize(0, 44))

        self.layout_adresse.addWidget(self.input_adresse)


        self.content_layout.addLayout(self.layout_adresse)

        self.layout_notes = QVBoxLayout()
        self.layout_notes.setSpacing(6)
        self.layout_notes.setObjectName(u"layout_notes")
        self.notes_label_layout = QHBoxLayout()
        self.notes_label_layout.setSpacing(4)
        self.notes_label_layout.setObjectName(u"notes_label_layout")
        self.lbl_notes = QLabel(self.scroll_content)
        self.lbl_notes.setObjectName(u"lbl_notes")
        self.lbl_notes.setStyleSheet(u"color: #334155; font-size: 12px; font-weight: 700;")

        self.notes_label_layout.addWidget(self.lbl_notes)

        self.notes_opt = QLabel(self.scroll_content)
        self.notes_opt.setObjectName(u"notes_opt")
        self.notes_opt.setStyleSheet(u"color: #0077B6; font-size: 10px; font-weight: 700; background: #e0f7fa; border-radius: 8px; padding: 2px 8px;")

        self.notes_label_layout.addWidget(self.notes_opt)

        self.notes_label_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.notes_label_layout.addItem(self.notes_label_spacer)


        self.layout_notes.addLayout(self.notes_label_layout)

        self.input_notes = QTextEdit(self.scroll_content)
        self.input_notes.setObjectName(u"input_notes")
        self.input_notes.setMinimumSize(QSize(0, 70))
        self.input_notes.setMaximumSize(QSize(16777215, 100))

        self.layout_notes.addWidget(self.input_notes)


        self.content_layout.addLayout(self.layout_notes)

        self.error_box = QFrame(self.scroll_content)
        self.error_box.setObjectName(u"error_box")
        self.error_box.setVisible(False)
        self.error_box.setFrameShape(QFrame.Shape.NoFrame)
        self.error_layout = QHBoxLayout(self.error_box)
        self.error_layout.setSpacing(10)
        self.error_layout.setObjectName(u"error_layout")
        self.error_layout.setContentsMargins(12, 10, 12, 10)
        self.error_icon = QLabel(self.error_box)
        self.error_icon.setObjectName(u"error_icon")
        self.error_icon.setMinimumSize(QSize(18, 18))
        self.error_icon.setMaximumSize(QSize(18, 18))
        self.error_icon.setPixmap(QPixmap(u":/Icon/Icons/alert-circle.svg"))
        self.error_icon.setScaledContents(True)

        self.error_layout.addWidget(self.error_icon)

        self.label_error = QLabel(self.error_box)
        self.label_error.setObjectName(u"label_error")
        self.label_error.setWordWrap(True)

        self.error_layout.addWidget(self.label_error)


        self.content_layout.addWidget(self.error_box)

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
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/check-circle_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_save.setIcon(icon)
        self.btn_save.setIconSize(QSize(16, 16))

        self.panel_footer_layout.addWidget(self.btn_save)


        self.panel_layout.addWidget(self.panel_footer)


        self.root_layout.addWidget(self.panel)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Client \u2014 Nova Pharma", None))
        self.brand_badge_text.setText(QCoreApplication.translate("Dialog", u"NOUVEAU CLIENT", None))
        self.sidebar_title.setText(QCoreApplication.translate("Dialog", u"Ajouter un client", None))
        self.sidebar_lead.setText(QCoreApplication.translate("Dialog", u"Enregistrez un nouveau client pour suivre ses achats et son historique.", None))
        self.check_name_text.setText(QCoreApplication.translate("Dialog", u"Nom renseign\u00e9", None))
        self.check_phone_text.setText(QCoreApplication.translate("Dialog", u"Num\u00e9ro valide", None))
        self.progress_label.setText(QCoreApplication.translate("Dialog", u"0 %", None))
        self.sidebar_footer.setText(QCoreApplication.translate("Dialog", u"Nova Pharma \u2014 Gestion clients", None))
        self.panel_title.setText(QCoreApplication.translate("Dialog", u"Fiche client", None))
        self.panel_subtitle.setText(QCoreApplication.translate("Dialog", u"Les champs marqu\u00e9s d'une * sont obligatoires.", None))
        self.anon_check.setText(QCoreApplication.translate("Dialog", u"Respecter l'anonymat du client", None))
        self.anon_hint.setText(QCoreApplication.translate("Dialog", u"Aucune donn\u00e9e personnelle ne sera conserv\u00e9e", None))
        self.anon_banner_text.setText(QCoreApplication.translate("Dialog", u"Un identifiant anonyme sera g\u00e9n\u00e9r\u00e9 automatiquement (ex : ANON-20261007-A3F2). Aucune information personnelle ne sera demand\u00e9e ni stock\u00e9e.", None))
        self.sec1_num.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.sec1_title.setText(QCoreApplication.translate("Dialog", u"COORDONN\u00c9ES DU CLIENT", None))
        self.lbl_nom.setText(QCoreApplication.translate("Dialog", u"Nom complet", None))
        self.req_nom.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.input_nom.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ex : Jean", None))
        self.lbl_sexe.setText(QCoreApplication.translate("Dialog", u"Sexe", None))
        self.req_nom_2.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.input_sexe.setItemText(0, QCoreApplication.translate("Dialog", u"Masculin", None))
        self.input_sexe.setItemText(1, QCoreApplication.translate("Dialog", u"F\u00e9minin", None))

        self.lbl_numero.setText(QCoreApplication.translate("Dialog", u"Num\u00e9ro de t\u00e9l\u00e9phone", None))
        self.req_numero.setText(QCoreApplication.translate("Dialog", u"*", None))
        self.input_numero.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ex : +243 800 000 000", None))
        self.lbl_email.setText(QCoreApplication.translate("Dialog", u"Email", None))
        self.email_opt.setText(QCoreApplication.translate("Dialog", u"Optionnel", None))
        self.input_email.setPlaceholderText(QCoreApplication.translate("Dialog", u"exemple@email.com", None))
        self.lbl_adresse.setText(QCoreApplication.translate("Dialog", u"Adresse", None))
        self.adresse_opt.setText(QCoreApplication.translate("Dialog", u"Optionnel", None))
        self.input_adresse.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ex : Avenue Lumumba, n\u00b045, Kinshasa/Gombe", None))
        self.lbl_notes.setText(QCoreApplication.translate("Dialog", u"Notes internes", None))
        self.notes_opt.setText(QCoreApplication.translate("Dialog", u"Optionnel", None))
        self.input_notes.setPlaceholderText(QCoreApplication.translate("Dialog", u"Allergies, pr\u00e9f\u00e9rences, remarques\u2026", None))
        self.label_error.setText("")
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"Annuler", None))
        self.btn_save.setText(QCoreApplication.translate("Dialog", u"Enregistrer le client", None))
    # retranslateUi

