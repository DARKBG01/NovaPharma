# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_configurationpNsYxy.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QDoubleSpinBox,
    QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget, QWizard, QWizardPage)
import Icon_rc

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.resize(817, 902)
        Wizard.setMinimumSize(QSize(760, 800))
        Wizard.setStyleSheet(u"/* ============================================================\n"
"   NOVA PHARMA \u2014 TH\u00c8ME WIZARD PREMIUM\n"
"   Palette : #023E8A \u2192 #0077B6 \u2192 #00B4D8 \u2192 #90E0EF \u2192 #CAF0F8\n"
"   Accent Or : #F4A261 | Succ\u00e8s : #16A34A | Erreur : #DC2626\n"
"   ============================================================ */\n"
"\n"
"QWizard { background-color: #f0f4f8; }\n"
"QWizardPage { background-color: transparent; }\n"
"\n"
"/* ===================== HEADERS GRADIENT ===================== */\n"
"#header_welcome, #header_identity, #header_contact,\n"
"#header_pharmacy, #header_settings, #header_summary, #header_type, #header_client_config, #header_client_summary {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:0.4 #0077B6, stop:1 #00B4D8);\n"
"    border-top-left-radius: 16px;\n"
"    border-top-right-radius: 16px;\n"
"    padding: 0;\n"
"}\n"
"\n"
".header_title {\n"
"    color: #ffffff; font-size: 20px; font-weight: 800;\n"
"    letter-spacing:"
                        " 0.5px; background: transparent;\n"
"}\n"
".header_subtitle {\n"
"    color: #CAF0F8; font-size: 12px; font-weight: 400;\n"
"    background: transparent;\n"
"}\n"
".header_icon { background: transparent; }\n"
"\n"
"/* ===================== CARDS ===================== */\n"
"#card_welcome, #card_identity, #card_contact,\n"
"#card_pharmacy, #card_settings, #card_summary {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-top: none;\n"
"    border-bottom-left-radius: 16px;\n"
"    border-bottom-right-radius: 16px;\n"
"}\n"
"\n"
"/* ===================== SECTION TITLES ===================== */\n"
".section_title {\n"
"    color: #023E8A; font-size: 15px; font-weight: 700;\n"
"    background: transparent; padding: 0 0 4px 0;\n"
"}\n"
"\n"
"/* ===================== LABELS ===================== */\n"
"QLabel { color: #334155; font-weight: 500; font-size: 13px; background: transparent; }\n"
"\n"
"/* ===================== INPUTS ===================== */\n"
"QLineEdit, QComboBox, QDoub"
                        "leSpinBox, QSpinBox, QDateEdit {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #e2e8f0;\n"
"    border-radius: 10px;\n"
"    padding: 10px 14px;\n"
"    color: #1e293b;\n"
"    font-size: 13px;\n"
"    selection-background-color: #0077B6;\n"
"    selection-color: #ffffff;\n"
"}\n"
"QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus,\n"
"QSpinBox:focus, QDateEdit:focus {\n"
"    background-color: #ffffff;\n"
"    border: 1.5px solid #00B4D8;\n"
"}\n"
"QLineEdit:hover, QComboBox:hover, QDoubleSpinBox:hover,\n"
"QSpinBox:hover, QDateEdit:hover { border-color: #94A3B8; }\n"
"QLineEdit[echoMode=\"2\"] { font-family: \"Segoe UI\", sans-serif; letter-spacing: 2px; }\n"
"\n"
"/* ===================== COMBOBOX ===================== */\n"
"QComboBox { padding-right: 30px; }\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding; subcontrol-position: top right;\n"
"    width: 30px; border-left: 1px solid #e2e8f0;\n"
"    border-top-right-radius: 10px; border-bottom-right-radius: 10px;\n"
"    "
                        "background: transparent;\n"
"}\n"
"QComboBox::down-arrow { image: url(:/Icon/Icons/chevron-down.svg); width: 14px; height: 14px; }\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #ffffff; border: 1px solid #e2e8f0;\n"
"    border-radius: 10px;\n"
"    selection-background-color: #e0f7fa;\n"
"    selection-color: #023E8A;\n"
"    outline: none; padding: 4px;\n"
"}\n"
"\n"
"/* ===================== SPINBOX ===================== */\n"
"QDoubleSpinBox::up-button, QSpinBox::up-button {\n"
"    subcontrol-origin: border; subcontrol-position: top right;\n"
"    width: 24px; height: 20px; border-top-right-radius: 10px; background: transparent;\n"
"}\n"
"QDoubleSpinBox::down-button, QSpinBox::down-button {\n"
"    subcontrol-origin: border; subcontrol-position: bottom right;\n"
"    width: 24px; height: 20px; border-bottom-right-radius: 10px; background: transparent;\n"
"}\n"
"\n"
"/* ===================== RADIO / CHECKBOX ===================== */\n"
"QRadioButton {\n"
"    spacing: 10px; color: #475569; fo"
                        "nt-size: 13px;\n"
"    font-weight: 500; background: transparent; padding: 4px 0;\n"
"}\n"
"QRadioButton::indicator { width: 20px; height: 20px; }\n"
"QRadioButton::indicator:unchecked {\n"
"    border: 2px solid #cbd5e1; border-radius: 10px; background-color: #ffffff;\n"
"}\n"
"QRadioButton::indicator:unchecked:hover { border-color: #00B4D8; }\n"
"QRadioButton::indicator:checked {\n"
"    border: 2px solid #0077B6; border-radius: 10px; background-color: #0077B6;\n"
"    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOCIgaGVpZ2h0PSI4IiB2aWV3Qm94PSIwIDAgOCA4IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxjaXJjbGUgY3g9IjQiIGN5PSI0IiByPSIyIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==);\n"
"}\n"
"QCheckBox {\n"
"    spacing: 10px; color: #475569; font-size: 13px;\n"
"    font-weight: 500; background: transparent;\n"
"}\n"
"QCheckBox::indicator {\n"
"    width: 20px; height: 20px; border: 2px solid #cbd5e1;\n"
"    border-radius: 5px; background-color: #ffffff;\n"
"}\n"
"QCheckBox::indicator:hover { border-color: #00B4"
                        "D8; }\n"
"QCheckBox::indicator:checked {\n"
"    border: 2px solid #0077B6; background-color: #0077B6;\n"
"    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEgNEwzLjUgNi41TDkgMSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L3N2Zz4=);\n"
"}\n"
"\n"
"/* ===================== PHOTO UPLOAD ===================== */\n"
"#photo_label {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f8fafc, stop:1 #e2e8f0);\n"
"    border: 2px dashed #94A3B8; border-radius: 80px;\n"
"    color: #64748b; font-size: 12px; font-weight: 500;\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}\n"
"#photo_label:hover {\n"
"    border: 2px dashed #00B4D8;\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #eff6ff, stop:1 #dbeafe);\n"
"}\n"
"#btn_upload_photo, #btn_upload_logo {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2"
                        ":0, stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: #ffffff; border: none; border-radius: 10px;\n"
"    padding: 10px 24px; font-size: 13px; font-weight: 600;\n"
"    letter-spacing: 0.3px;\n"
"}\n"
"#btn_upload_photo:hover, #btn_upload_logo:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"#btn_upload_photo:pressed, #btn_upload_logo:pressed { background: #023E8A; }\n"
"\n"
"/* ===================== ROLE CARDS ===================== */\n"
".role_card_selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f0f9ff, stop:1 #e0f7fa);\n"
"    border: 2px solid #00B4D8; border-radius: 14px; padding: 20px;\n"
"}\n"
"\n"
"/* ===================== FEATURE CARDS ===================== */\n"
".feature_card {\n"
"    background-color: #f8fafc; border: 1px solid #e2e8f0;\n"
"    border-radius: 12px; padding: 16px;\n"
"}\n"
".feature_title { color: #023E8A; font-size: 13px; font-weight: 700; background: transparent; }\n"
".feature_desc  { colo"
                        "r: #64748b; font-size: 11px; background: transparent; }\n"
"\n"
"/* ===================== SUMMARY CARDS ===================== */\n"
".summary_card {\n"
"    background-color: #f8fafc; border: 1px solid #e2e8f0;\n"
"    border-radius: 12px; padding: 16px;\n"
"}\n"
".summary_label {\n"
"    color: #94A3B8; font-size: 11px; font-weight: 500;\n"
"    background: transparent; letter-spacing: 0.5px;\n"
"}\n"
".summary_value { color: #1e293b; font-size: 14px; font-weight: 600; background: transparent; }\n"
"\n"
"/* ===================== PASSWORD ERROR ===================== */\n"
"#label_pwd_error {\n"
"    color: #dc2626; font-size: 12px; font-weight: 600;\n"
"    padding: 4px 0 0 4px; background: transparent;\n"
"}\n"
"#label_pwd_error[valid=\"true\"] { color: #16a34a; }\n"
"\n"
"/* ===================== INFO BOX ===================== */\n"
"#info_box, #info_box_final {\n"
"    background-color: #f0f9ff; border: 1px solid #bae6fd;\n"
"    border-left: 4px solid #00B4D8; border-radius: 10px; padding: 14px 18px;\n"
"}"
                        "\n"
"\n"
"/* ===================== WIZARD BUTTONS ===================== */\n"
"QWizard QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: #ffffff; border: none; border-radius: 10px;\n"
"    padding: 10px 28px; font-size: 13px; font-weight: 700;\n"
"    min-width: 110px; letter-spacing: 0.3px;\n"
"}\n"
"QWizard QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"QWizard QPushButton:pressed { background: #023E8A; }\n"
"QWizard QPushButton:disabled { background: #e2e8f0; color: #94a3b8; }\n"
"\n"
"QWizard QPushButton[text=\"Cancel\"],\n"
"QWizard QPushButton[text=\"Annuler\"],\n"
"QWizard QPushButton[text=\"&Annuler\"],\n"
"QWizard QPushButton[text=\"< &Back\"],\n"
"QWizard QPushButton[text=\"< Back\"],\n"
"QWizard QPushButton[text=\"&Pr\u00e9c\u00e9dent\"],\n"
"QWizard QPushButton[text=\"Pr\u00e9c\u00e9dent\"] {\n"
"    background: transparent; color: #64748b; border: 1.5p"
                        "x solid #e2e8f0;\n"
"}\n"
"QWizard QPushButton[text=\"Cancel\"]:hover,\n"
"QWizard QPushButton[text=\"Annuler\"]:hover,\n"
"QWizard QPushButton[text=\"&Annuler\"]:hover,\n"
"QWizard QPushButton[text=\"< &Back\"]:hover,\n"
"QWizard QPushButton[text=\"< Back\"]:hover,\n"
"QWizard QPushButton[text=\"&Pr\u00e9c\u00e9dent\"]:hover,\n"
"QWizard QPushButton[text=\"Pr\u00e9c\u00e9dent\"]:hover {\n"
"    background: #fef2f2; color: #dc2626; border-color: #fecaca;\n"
"}\n"
"")
        Wizard.setWizardStyle(QWizard.WizardStyle.ClassicStyle)
        Wizard.setOptions(QWizard.WizardOption.NoBackButtonOnStartPage|QWizard.WizardOption.NoCancelButton)
        Wizard.setCurrentId(2)
        self.page_type = QWizardPage()
        self.page_type.setObjectName(u"page_type")
        self.layout_type = QVBoxLayout(self.page_type)
        self.layout_type.setSpacing(0)
        self.layout_type.setObjectName(u"layout_type")
        self.layout_type.setContentsMargins(0, 0, 0, 0)
        self.header_type = QFrame(self.page_type)
        self.header_type.setObjectName(u"header_type")
        self.header_type.setMinimumSize(QSize(0, 80))
        self.header_type.setMaximumSize(QSize(16777215, 80))
        self.header_type_layout = QHBoxLayout(self.header_type)
        self.header_type_layout.setObjectName(u"header_type_layout")
        self.header_type_layout.setContentsMargins(40, 16, 40, 16)
        self.type_icon = QLabel(self.header_type)
        self.type_icon.setObjectName(u"type_icon")
        self.type_icon.setMinimumSize(QSize(36, 36))
        self.type_icon.setMaximumSize(QSize(36, 36))
        self.type_icon.setStyleSheet(u"background: transparent;")
        self.type_icon.setPixmap(QPixmap(u":/Icon/Icons/settings_white.svg"))
        self.type_icon.setScaledContents(True)

        self.header_type_layout.addWidget(self.type_icon)

        self.type_text_layout = QVBoxLayout()
        self.type_text_layout.setSpacing(2)
        self.type_text_layout.setObjectName(u"type_text_layout")
        self.type_title = QLabel(self.header_type)
        self.type_title.setObjectName(u"type_title")
        self.type_title.setStyleSheet(u"color: #ffffff; font-size: 18px; font-weight: 700; background: transparent;")

        self.type_text_layout.addWidget(self.type_title)

        self.type_subtitle = QLabel(self.header_type)
        self.type_subtitle.setObjectName(u"type_subtitle")
        self.type_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.type_text_layout.addWidget(self.type_subtitle)


        self.header_type_layout.addLayout(self.type_text_layout)

        self.type_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_type_layout.addItem(self.type_header_spacer)


        self.layout_type.addWidget(self.header_type)

        self.card_type = QFrame(self.page_type)
        self.card_type.setObjectName(u"card_type")
        self.card_type.setFrameShape(QFrame.Shape.NoFrame)
        self.type_content = QVBoxLayout(self.card_type)
        self.type_content.setSpacing(18)
        self.type_content.setObjectName(u"type_content")
        self.type_content.setContentsMargins(40, 30, 40, 30)
        self.type_question = QLabel(self.card_type)
        self.type_question.setObjectName(u"type_question")
        self.type_question.setStyleSheet(u"color: #023E8A; font-size: 16px; font-weight: 700; background: transparent;")

        self.type_content.addWidget(self.type_question)

        self.type_card_server = QFrame(self.card_type)
        self.type_card_server.setObjectName(u"type_card_server")
        self.type_card_server.setMinimumSize(QSize(0, 130))
        self.type_card_server.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.type_card_server.setStyleSheet(u"#type_card_server {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #e2e8f0;\n"
"    border-radius: 14px;\n"
"}\n"
"#type_card_server:hover { border-color: #94A3B8; }\n"
"#type_card_server[selected=\"true\"] {\n"
"    background-color: #f0f9ff;\n"
"    border: 2px solid #00B4D8;\n"
"}")
        self.type_card_server_layout = QHBoxLayout(self.type_card_server)
        self.type_card_server_layout.setSpacing(18)
        self.type_card_server_layout.setObjectName(u"type_card_server_layout")
        self.type_card_server_layout.setContentsMargins(20, 18, 20, 18)
        self.type_server_icon = QLabel(self.type_card_server)
        self.type_server_icon.setObjectName(u"type_server_icon")
        self.type_server_icon.setMinimumSize(QSize(48, 48))
        self.type_server_icon.setMaximumSize(QSize(48, 48))
        self.type_server_icon.setStyleSheet(u"background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 8px;")
        self.type_server_icon.setPixmap(QPixmap(u":/Icon/Icons/server.svg"))
        self.type_server_icon.setScaledContents(True)

        self.type_card_server_layout.addWidget(self.type_server_icon)

        self.type_server_text_layout = QVBoxLayout()
        self.type_server_text_layout.setSpacing(4)
        self.type_server_text_layout.setObjectName(u"type_server_text_layout")
        self.type_server_title = QLabel(self.type_card_server)
        self.type_server_title.setObjectName(u"type_server_title")
        self.type_server_title.setStyleSheet(u"color: #0f172a; font-size: 15px; font-weight: 800; background: transparent;")

        self.type_server_text_layout.addWidget(self.type_server_title)

        self.type_server_desc = QLabel(self.type_card_server)
        self.type_server_desc.setObjectName(u"type_server_desc")
        self.type_server_desc.setStyleSheet(u"color: #475569; font-size: 12px; background: transparent;")
        self.type_server_desc.setWordWrap(True)

        self.type_server_text_layout.addWidget(self.type_server_desc)


        self.type_card_server_layout.addLayout(self.type_server_text_layout)

        self.radio_type_server = QRadioButton(self.type_card_server)
        self.radio_type_server.setObjectName(u"radio_type_server")
        self.radio_type_server.setMinimumSize(QSize(24, 24))
        self.radio_type_server.setMaximumSize(QSize(24, 24))

        self.type_card_server_layout.addWidget(self.radio_type_server)


        self.type_content.addWidget(self.type_card_server)

        self.type_card_client = QFrame(self.card_type)
        self.type_card_client.setObjectName(u"type_card_client")
        self.type_card_client.setMinimumSize(QSize(0, 130))
        self.type_card_client.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.type_card_client.setStyleSheet(u"#type_card_client {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #e2e8f0;\n"
"    border-radius: 14px;\n"
"}\n"
"#type_card_client:hover { border-color: #94A3B8; }\n"
"#type_card_client[selected=\"true\"] {\n"
"    background-color: #f0fdf4;\n"
"    border: 2px solid #16A34A;\n"
"}")
        self.type_card_client_layout = QHBoxLayout(self.type_card_client)
        self.type_card_client_layout.setSpacing(18)
        self.type_card_client_layout.setObjectName(u"type_card_client_layout")
        self.type_card_client_layout.setContentsMargins(20, 18, 20, 18)
        self.type_client_icon = QLabel(self.type_card_client)
        self.type_client_icon.setObjectName(u"type_client_icon")
        self.type_client_icon.setMinimumSize(QSize(48, 48))
        self.type_client_icon.setMaximumSize(QSize(48, 48))
        self.type_client_icon.setStyleSheet(u"background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 8px;")
        self.type_client_icon.setPixmap(QPixmap(u":/Icon/Icons/monitor.svg"))
        self.type_client_icon.setScaledContents(True)

        self.type_card_client_layout.addWidget(self.type_client_icon)

        self.type_client_text_layout = QVBoxLayout()
        self.type_client_text_layout.setSpacing(4)
        self.type_client_text_layout.setObjectName(u"type_client_text_layout")
        self.type_client_title = QLabel(self.type_card_client)
        self.type_client_title.setObjectName(u"type_client_title")
        self.type_client_title.setStyleSheet(u"color: #0f172a; font-size: 15px; font-weight: 800; background: transparent;")

        self.type_client_text_layout.addWidget(self.type_client_title)

        self.type_client_desc = QLabel(self.type_card_client)
        self.type_client_desc.setObjectName(u"type_client_desc")
        self.type_client_desc.setStyleSheet(u"color: #475569; font-size: 12px; background: transparent;")
        self.type_client_desc.setWordWrap(True)

        self.type_client_text_layout.addWidget(self.type_client_desc)


        self.type_card_client_layout.addLayout(self.type_client_text_layout)

        self.radio_type_client = QRadioButton(self.type_card_client)
        self.radio_type_client.setObjectName(u"radio_type_client")
        self.radio_type_client.setMinimumSize(QSize(24, 24))
        self.radio_type_client.setMaximumSize(QSize(24, 24))

        self.type_card_client_layout.addWidget(self.radio_type_client)


        self.type_content.addWidget(self.type_card_client)

        self.type_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.type_content.addItem(self.type_bottom_spacer)


        self.layout_type.addWidget(self.card_type)

        Wizard.addPage(self.page_type)
        self.page_welcome = QWizardPage()
        self.page_welcome.setObjectName(u"page_welcome")
        self.layout_welcome = QVBoxLayout(self.page_welcome)
        self.layout_welcome.setSpacing(0)
        self.layout_welcome.setObjectName(u"layout_welcome")
        self.layout_welcome.setContentsMargins(0, 0, 0, 0)
        self.header_welcome = QFrame(self.page_welcome)
        self.header_welcome.setObjectName(u"header_welcome")
        self.header_welcome.setMinimumSize(QSize(0, 100))
        self.header_welcome.setMaximumSize(QSize(16777215, 100))
        self.header_welcome_layout = QHBoxLayout(self.header_welcome)
        self.header_welcome_layout.setObjectName(u"header_welcome_layout")
        self.header_welcome_layout.setContentsMargins(40, 20, 40, 20)
        self.welcome_logo = QLabel(self.header_welcome)
        self.welcome_logo.setObjectName(u"welcome_logo")
        self.welcome_logo.setMinimumSize(QSize(60, 60))
        self.welcome_logo.setMaximumSize(QSize(60, 60))
        self.welcome_logo.setPixmap(QPixmap(u":/Icon/Icons/1758107223736.png"))
        self.welcome_logo.setScaledContents(True)

        self.header_welcome_layout.addWidget(self.welcome_logo)

        self.welcome_text_layout = QVBoxLayout()
        self.welcome_text_layout.setSpacing(2)
        self.welcome_text_layout.setObjectName(u"welcome_text_layout")
        self.welcome_title = QLabel(self.header_welcome)
        self.welcome_title.setObjectName(u"welcome_title")
        self.welcome_title.setStyleSheet(u"color: #ffffff; font-size: 22px; font-weight: 800; background: transparent; letter-spacing: 2px;")

        self.welcome_text_layout.addWidget(self.welcome_title)

        self.welcome_subtitle = QLabel(self.header_welcome)
        self.welcome_subtitle.setObjectName(u"welcome_subtitle")
        self.welcome_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.welcome_text_layout.addWidget(self.welcome_subtitle)


        self.header_welcome_layout.addLayout(self.welcome_text_layout)

        self.welcome_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_welcome_layout.addItem(self.welcome_header_spacer)


        self.layout_welcome.addWidget(self.header_welcome)

        self.card_welcome = QFrame(self.page_welcome)
        self.card_welcome.setObjectName(u"card_welcome")
        self.card_welcome.setFrameShape(QFrame.Shape.NoFrame)
        self.welcome_content = QVBoxLayout(self.card_welcome)
        self.welcome_content.setSpacing(20)
        self.welcome_content.setObjectName(u"welcome_content")
        self.welcome_content.setContentsMargins(50, 35, 50, 35)
        self.welcome_main_title = QLabel(self.card_welcome)
        self.welcome_main_title.setObjectName(u"welcome_main_title")
        self.welcome_main_title.setStyleSheet(u"color: #023E8A; font-size: 24px; font-weight: 800; letter-spacing: 1px; background: transparent;")
        self.welcome_main_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.welcome_content.addWidget(self.welcome_main_title)

        self.welcome_main_subtitle = QLabel(self.card_welcome)
        self.welcome_main_subtitle.setObjectName(u"welcome_main_subtitle")
        self.welcome_main_subtitle.setStyleSheet(u"color: #64748b; font-size: 13px; background: transparent;")
        self.welcome_main_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_main_subtitle.setWordWrap(True)

        self.welcome_content.addWidget(self.welcome_main_subtitle)

        self.divider_welcome = QFrame(self.card_welcome)
        self.divider_welcome.setObjectName(u"divider_welcome")
        self.divider_welcome.setFrameShape(QFrame.Shape.HLine)

        self.welcome_content.addWidget(self.divider_welcome)

        self.role_section_header = QHBoxLayout()
        self.role_section_header.setSpacing(10)
        self.role_section_header.setObjectName(u"role_section_header")
        self.role_section_icon = QLabel(self.card_welcome)
        self.role_section_icon.setObjectName(u"role_section_icon")
        self.role_section_icon.setMinimumSize(QSize(20, 20))
        self.role_section_icon.setMaximumSize(QSize(20, 20))
        self.role_section_icon.setPixmap(QPixmap(u":/Icon/Icons/user-check.svg"))
        self.role_section_icon.setScaledContents(True)

        self.role_section_header.addWidget(self.role_section_icon)

        self.role_section_title = QLabel(self.card_welcome)
        self.role_section_title.setObjectName(u"role_section_title")
        self.role_section_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.role_section_header.addWidget(self.role_section_title)

        self.role_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.role_section_header.addItem(self.role_header_spacer)


        self.welcome_content.addLayout(self.role_section_header)

        self.role_cards_layout = QHBoxLayout()
        self.role_cards_layout.setSpacing(20)
        self.role_cards_layout.setObjectName(u"role_cards_layout")
        self.role_left_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.role_cards_layout.addItem(self.role_left_spacer)

        self.role_card_pharmacien = QFrame(self.card_welcome)
        self.role_card_pharmacien.setObjectName(u"role_card_pharmacien")
        self.role_card_pharmacien.setMinimumSize(QSize(440, 200))
        self.role_card_pharmacien.setMaximumSize(QSize(440, 200))
        self.role_card_pharmacien.setStyleSheet(u".role_card_selected {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f0f9ff, stop:1 #e0f7fa);\n"
"    border: 2px solid #00B4D8;\n"
"    border-radius: 14px;\n"
"    padding: 20px;\n"
"}")
        self.pharmacien_card_layout = QVBoxLayout(self.role_card_pharmacien)
        self.pharmacien_card_layout.setSpacing(10)
        self.pharmacien_card_layout.setObjectName(u"pharmacien_card_layout")
        self.pharmacien_icon = QLabel(self.role_card_pharmacien)
        self.pharmacien_icon.setObjectName(u"pharmacien_icon")
        self.pharmacien_icon.setMinimumSize(QSize(48, 48))
        self.pharmacien_icon.setMaximumSize(QSize(48, 48))
        self.pharmacien_icon.setPixmap(QPixmap(u":/Icon/Icons/pharmacy.svg"))
        self.pharmacien_icon.setScaledContents(True)

        self.pharmacien_card_layout.addWidget(self.pharmacien_icon, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pharmacien_label = QLabel(self.role_card_pharmacien)
        self.pharmacien_label.setObjectName(u"pharmacien_label")
        self.pharmacien_label.setStyleSheet(u"color: #023E8A; font-size: 18px; font-weight: 700; background: transparent;")

        self.pharmacien_card_layout.addWidget(self.pharmacien_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pharmacien_desc = QLabel(self.role_card_pharmacien)
        self.pharmacien_desc.setObjectName(u"pharmacien_desc")
        self.pharmacien_desc.setStyleSheet(u"color: #64748b; font-size: 12px; background: transparent;")
        self.pharmacien_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pharmacien_desc.setWordWrap(True)

        self.pharmacien_card_layout.addWidget(self.pharmacien_desc)


        self.role_cards_layout.addWidget(self.role_card_pharmacien)

        self.role_right_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.role_cards_layout.addItem(self.role_right_spacer)


        self.welcome_content.addLayout(self.role_cards_layout)

        self.features_layout = QHBoxLayout()
        self.features_layout.setSpacing(14)
        self.features_layout.setObjectName(u"features_layout")
        self.feature_1 = QFrame(self.card_welcome)
        self.feature_1.setObjectName(u"feature_1")
        self.feature_1.setMinimumSize(QSize(150, 110))
        self.feature_1.setStyleSheet(u".feature_card { background-color: #f0f9ff; border: 1px solid #bae6fd; border-radius: 12px; padding: 14px; }")
        self.f1_layout = QVBoxLayout(self.feature_1)
        self.f1_layout.setSpacing(6)
        self.f1_layout.setObjectName(u"f1_layout")
        self.f1_icon = QLabel(self.feature_1)
        self.f1_icon.setObjectName(u"f1_icon")
        self.f1_icon.setMinimumSize(QSize(28, 28))
        self.f1_icon.setMaximumSize(QSize(28, 28))
        self.f1_icon.setPixmap(QPixmap(u":/Icon/Icons/search.svg"))
        self.f1_icon.setScaledContents(True)

        self.f1_layout.addWidget(self.f1_icon, 0, Qt.AlignmentFlag.AlignHCenter)

        self.f1_title = QLabel(self.feature_1)
        self.f1_title.setObjectName(u"f1_title")
        self.f1_title.setStyleSheet(u".feature_title { color: #023E8A; font-size: 12px; font-weight: 700; background: transparent; }")
        self.f1_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.f1_layout.addWidget(self.f1_title)

        self.f1_desc = QLabel(self.feature_1)
        self.f1_desc.setObjectName(u"f1_desc")
        self.f1_desc.setStyleSheet(u".feature_desc { color: #64748b; font-size: 10px; background: transparent; }")
        self.f1_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.f1_desc.setWordWrap(True)

        self.f1_layout.addWidget(self.f1_desc)


        self.features_layout.addWidget(self.feature_1)

        self.feature_2 = QFrame(self.card_welcome)
        self.feature_2.setObjectName(u"feature_2")
        self.feature_2.setMinimumSize(QSize(150, 110))
        self.feature_2.setStyleSheet(u".feature_card { background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 14px; }")
        self.f2_layout = QVBoxLayout(self.feature_2)
        self.f2_layout.setSpacing(6)
        self.f2_layout.setObjectName(u"f2_layout")
        self.f2_icon = QLabel(self.feature_2)
        self.f2_icon.setObjectName(u"f2_icon")
        self.f2_icon.setMinimumSize(QSize(28, 28))
        self.f2_icon.setMaximumSize(QSize(28, 28))
        self.f2_icon.setPixmap(QPixmap(u":/Icon/Icons/clock.svg"))
        self.f2_icon.setScaledContents(True)

        self.f2_layout.addWidget(self.f2_icon, 0, Qt.AlignmentFlag.AlignHCenter)

        self.f2_title = QLabel(self.feature_2)
        self.f2_title.setObjectName(u"f2_title")
        self.f2_title.setStyleSheet(u".feature_title { color: #166534; font-size: 12px; font-weight: 700; background: transparent; }")
        self.f2_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.f2_layout.addWidget(self.f2_title)

        self.f2_desc = QLabel(self.feature_2)
        self.f2_desc.setObjectName(u"f2_desc")
        self.f2_desc.setStyleSheet(u".feature_desc { color: #64748b; font-size: 10px; background: transparent; }")
        self.f2_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.f2_desc.setWordWrap(True)

        self.f2_layout.addWidget(self.f2_desc)


        self.features_layout.addWidget(self.feature_2)

        self.feature_3 = QFrame(self.card_welcome)
        self.feature_3.setObjectName(u"feature_3")
        self.feature_3.setMinimumSize(QSize(150, 110))
        self.feature_3.setStyleSheet(u".feature_card { background-color: #fefce8; border: 1px solid #fef08a; border-radius: 12px; padding: 14px; }")
        self.f3_layout = QVBoxLayout(self.feature_3)
        self.f3_layout.setSpacing(6)
        self.f3_layout.setObjectName(u"f3_layout")
        self.f3_icon = QLabel(self.feature_3)
        self.f3_icon.setObjectName(u"f3_icon")
        self.f3_icon.setMinimumSize(QSize(28, 28))
        self.f3_icon.setMaximumSize(QSize(28, 28))
        self.f3_icon.setPixmap(QPixmap(u":/Icon/Icons/archive.svg"))
        self.f3_icon.setScaledContents(True)

        self.f3_layout.addWidget(self.f3_icon, 0, Qt.AlignmentFlag.AlignHCenter)

        self.f3_title = QLabel(self.feature_3)
        self.f3_title.setObjectName(u"f3_title")
        self.f3_title.setStyleSheet(u".feature_title { color: #854d0e; font-size: 12px; font-weight: 700; background: transparent; }")
        self.f3_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.f3_layout.addWidget(self.f3_title)

        self.f3_desc = QLabel(self.feature_3)
        self.f3_desc.setObjectName(u"f3_desc")
        self.f3_desc.setStyleSheet(u".feature_desc { color: #64748b; font-size: 10px; background: transparent; }")
        self.f3_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.f3_desc.setWordWrap(True)

        self.f3_layout.addWidget(self.f3_desc)


        self.features_layout.addWidget(self.feature_3)


        self.welcome_content.addLayout(self.features_layout)

        self.welcome_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.welcome_content.addItem(self.welcome_bottom_spacer)


        self.layout_welcome.addWidget(self.card_welcome)

        Wizard.addPage(self.page_welcome)
        self.page_identity = QWizardPage()
        self.page_identity.setObjectName(u"page_identity")
        self.layout_identity = QVBoxLayout(self.page_identity)
        self.layout_identity.setSpacing(0)
        self.layout_identity.setObjectName(u"layout_identity")
        self.layout_identity.setContentsMargins(0, 0, 0, 0)
        self.header_identity = QFrame(self.page_identity)
        self.header_identity.setObjectName(u"header_identity")
        self.header_identity.setMinimumSize(QSize(0, 80))
        self.header_identity.setMaximumSize(QSize(16777215, 80))
        self.header_identity_layout = QHBoxLayout(self.header_identity)
        self.header_identity_layout.setObjectName(u"header_identity_layout")
        self.header_identity_layout.setContentsMargins(40, 16, 40, 16)
        self.identity_icon = QLabel(self.header_identity)
        self.identity_icon.setObjectName(u"identity_icon")
        self.identity_icon.setMinimumSize(QSize(36, 36))
        self.identity_icon.setMaximumSize(QSize(36, 36))
        self.identity_icon.setStyleSheet(u"background: transparent;")
        self.identity_icon.setPixmap(QPixmap(u":/Icon/Icons/identity_white.svg"))
        self.identity_icon.setScaledContents(True)

        self.header_identity_layout.addWidget(self.identity_icon)

        self.identity_text_layout = QVBoxLayout()
        self.identity_text_layout.setSpacing(2)
        self.identity_text_layout.setObjectName(u"identity_text_layout")
        self.identity_title = QLabel(self.header_identity)
        self.identity_title.setObjectName(u"identity_title")
        self.identity_title.setStyleSheet(u"color: #ffffff; font-size: 18px; font-weight: 700; background: transparent;")

        self.identity_text_layout.addWidget(self.identity_title)

        self.identity_subtitle = QLabel(self.header_identity)
        self.identity_subtitle.setObjectName(u"identity_subtitle")
        self.identity_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.identity_text_layout.addWidget(self.identity_subtitle)


        self.header_identity_layout.addLayout(self.identity_text_layout)

        self.identity_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_identity_layout.addItem(self.identity_header_spacer)


        self.layout_identity.addWidget(self.header_identity)

        self.card_identity = QFrame(self.page_identity)
        self.card_identity.setObjectName(u"card_identity")
        self.card_identity.setFrameShape(QFrame.Shape.NoFrame)
        self.identity_content = QVBoxLayout(self.card_identity)
        self.identity_content.setSpacing(18)
        self.identity_content.setObjectName(u"identity_content")
        self.identity_content.setContentsMargins(40, 30, 40, 30)
        self.photo_layout = QVBoxLayout()
        self.photo_layout.setSpacing(10)
        self.photo_layout.setObjectName(u"photo_layout")
        self.photo_label = QLabel(self.card_identity)
        self.photo_label.setObjectName(u"photo_label")
        self.photo_label.setMinimumSize(QSize(130, 130))
        self.photo_label.setMaximumSize(QSize(130, 130))
        self.photo_label.setScaledContents(True)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.photo_layout.addWidget(self.photo_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.btn_upload_photo = QPushButton(self.card_identity)
        self.btn_upload_photo.setObjectName(u"btn_upload_photo")
        self.btn_upload_photo.setMinimumSize(QSize(158, 40))
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/camera_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_upload_photo.setIcon(icon)
        self.btn_upload_photo.setIconSize(QSize(16, 16))

        self.photo_layout.addWidget(self.btn_upload_photo, 0, Qt.AlignmentFlag.AlignHCenter)

        self.photo_hint = QLabel(self.card_identity)
        self.photo_hint.setObjectName(u"photo_hint")
        self.photo_hint.setStyleSheet(u"color: #94A3B8; font-size: 11px; background: transparent;")

        self.photo_layout.addWidget(self.photo_hint, 0, Qt.AlignmentFlag.AlignHCenter)


        self.identity_content.addLayout(self.photo_layout)

        self.divider_identity_1 = QFrame(self.card_identity)
        self.divider_identity_1.setObjectName(u"divider_identity_1")
        self.divider_identity_1.setFrameShape(QFrame.Shape.HLine)

        self.identity_content.addWidget(self.divider_identity_1)

        self.section_identity_header_layout = QHBoxLayout()
        self.section_identity_header_layout.setSpacing(10)
        self.section_identity_header_layout.setObjectName(u"section_identity_header_layout")
        self.section_identity_icon = QLabel(self.card_identity)
        self.section_identity_icon.setObjectName(u"section_identity_icon")
        self.section_identity_icon.setMinimumSize(QSize(20, 20))
        self.section_identity_icon.setMaximumSize(QSize(20, 20))
        self.section_identity_icon.setPixmap(QPixmap(u":/Icon/Icons/identity.svg"))
        self.section_identity_icon.setScaledContents(True)

        self.section_identity_header_layout.addWidget(self.section_identity_icon)

        self.section_identity_title = QLabel(self.card_identity)
        self.section_identity_title.setObjectName(u"section_identity_title")
        self.section_identity_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.section_identity_header_layout.addWidget(self.section_identity_title)

        self.section_identity_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.section_identity_header_layout.addItem(self.section_identity_spacer)


        self.identity_content.addLayout(self.section_identity_header_layout)

        self.form_identity = QFormLayout()
        self.form_identity.setObjectName(u"form_identity")
        self.form_identity.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.form_identity.setHorizontalSpacing(20)
        self.form_identity.setVerticalSpacing(12)
        self.label_first_name = QLabel(self.card_identity)
        self.label_first_name.setObjectName(u"label_first_name")

        self.form_identity.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_first_name)

        self.input_first_name = QLineEdit(self.card_identity)
        self.input_first_name.setObjectName(u"input_first_name")
        self.input_first_name.setMinimumSize(QSize(0, 44))

        self.form_identity.setWidget(0, QFormLayout.ItemRole.FieldRole, self.input_first_name)

        self.label_name = QLabel(self.card_identity)
        self.label_name.setObjectName(u"label_name")

        self.form_identity.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_name)

        self.input_name = QLineEdit(self.card_identity)
        self.input_name.setObjectName(u"input_name")
        self.input_name.setMinimumSize(QSize(0, 44))

        self.form_identity.setWidget(1, QFormLayout.ItemRole.FieldRole, self.input_name)

        self.label_last_name = QLabel(self.card_identity)
        self.label_last_name.setObjectName(u"label_last_name")

        self.form_identity.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_last_name)

        self.input_last_name = QLineEdit(self.card_identity)
        self.input_last_name.setObjectName(u"input_last_name")
        self.input_last_name.setMinimumSize(QSize(0, 44))

        self.form_identity.setWidget(2, QFormLayout.ItemRole.FieldRole, self.input_last_name)


        self.identity_content.addLayout(self.form_identity)

        self.divider_identity_2 = QFrame(self.card_identity)
        self.divider_identity_2.setObjectName(u"divider_identity_2")
        self.divider_identity_2.setFrameShape(QFrame.Shape.HLine)

        self.identity_content.addWidget(self.divider_identity_2)

        self.section_demo_header_layout = QHBoxLayout()
        self.section_demo_header_layout.setSpacing(10)
        self.section_demo_header_layout.setObjectName(u"section_demo_header_layout")
        self.section_demo_icon = QLabel(self.card_identity)
        self.section_demo_icon.setObjectName(u"section_demo_icon")
        self.section_demo_icon.setMinimumSize(QSize(20, 20))
        self.section_demo_icon.setMaximumSize(QSize(20, 20))
        self.section_demo_icon.setPixmap(QPixmap(u":/Icon/Icons/globe.svg"))
        self.section_demo_icon.setScaledContents(True)

        self.section_demo_header_layout.addWidget(self.section_demo_icon)

        self.section_demo_title = QLabel(self.card_identity)
        self.section_demo_title.setObjectName(u"section_demo_title")
        self.section_demo_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.section_demo_header_layout.addWidget(self.section_demo_title)

        self.section_demo_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.section_demo_header_layout.addItem(self.section_demo_spacer)


        self.identity_content.addLayout(self.section_demo_header_layout)

        self.form_demo = QFormLayout()
        self.form_demo.setObjectName(u"form_demo")
        self.form_demo.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.form_demo.setHorizontalSpacing(20)
        self.form_demo.setVerticalSpacing(12)
        self.label_sexe = QLabel(self.card_identity)
        self.label_sexe.setObjectName(u"label_sexe")

        self.form_demo.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_sexe)

        self.frame_sexe = QFrame(self.card_identity)
        self.frame_sexe.setObjectName(u"frame_sexe")
        self.frame_sexe.setStyleSheet(u"#frame_sexe { background: transparent; }")
        self.sexe_layout = QHBoxLayout(self.frame_sexe)
        self.sexe_layout.setSpacing(24)
        self.sexe_layout.setObjectName(u"sexe_layout")
        self.sexe_layout.setContentsMargins(0, 0, 0, 0)
        self.radio_homme = QRadioButton(self.frame_sexe)
        self.radio_homme.setObjectName(u"radio_homme")
        self.radio_homme.setMinimumSize(QSize(0, 44))
        self.radio_homme.setChecked(True)

        self.sexe_layout.addWidget(self.radio_homme)

        self.radio_femme = QRadioButton(self.frame_sexe)
        self.radio_femme.setObjectName(u"radio_femme")
        self.radio_femme.setMinimumSize(QSize(0, 44))

        self.sexe_layout.addWidget(self.radio_femme)

        self.sexe_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.sexe_layout.addItem(self.sexe_spacer)


        self.form_demo.setWidget(0, QFormLayout.ItemRole.FieldRole, self.frame_sexe)

        self.label_dob = QLabel(self.card_identity)
        self.label_dob.setObjectName(u"label_dob")

        self.form_demo.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_dob)

        self.input_date_of_birth = QDateEdit(self.card_identity)
        self.input_date_of_birth.setObjectName(u"input_date_of_birth")
        self.input_date_of_birth.setMinimumSize(QSize(0, 44))
        self.input_date_of_birth.setCalendarPopup(True)

        self.form_demo.setWidget(1, QFormLayout.ItemRole.FieldRole, self.input_date_of_birth)

        self.label_age = QLabel(self.card_identity)
        self.label_age.setObjectName(u"label_age")

        self.form_demo.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_age)

        self.input_age = QSpinBox(self.card_identity)
        self.input_age.setObjectName(u"input_age")
        self.input_age.setMinimumSize(QSize(0, 44))
        self.input_age.setReadOnly(True)
        self.input_age.setMaximum(120)

        self.form_demo.setWidget(2, QFormLayout.ItemRole.FieldRole, self.input_age)

        self.label_nationality = QLabel(self.card_identity)
        self.label_nationality.setObjectName(u"label_nationality")

        self.form_demo.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_nationality)

        self.input_nationality = QComboBox(self.card_identity)
        self.input_nationality.setObjectName(u"input_nationality")
        self.input_nationality.setMinimumSize(QSize(0, 44))

        self.form_demo.setWidget(3, QFormLayout.ItemRole.FieldRole, self.input_nationality)


        self.identity_content.addLayout(self.form_demo)

        self.identity_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.identity_content.addItem(self.identity_bottom_spacer)


        self.layout_identity.addWidget(self.card_identity)

        Wizard.addPage(self.page_identity)
        self.page_contact = QWizardPage()
        self.page_contact.setObjectName(u"page_contact")
        self.layout_contact = QVBoxLayout(self.page_contact)
        self.layout_contact.setSpacing(0)
        self.layout_contact.setObjectName(u"layout_contact")
        self.layout_contact.setContentsMargins(0, 0, 0, 0)
        self.header_contact = QFrame(self.page_contact)
        self.header_contact.setObjectName(u"header_contact")
        self.header_contact.setMinimumSize(QSize(0, 80))
        self.header_contact.setMaximumSize(QSize(16777215, 80))
        self.header_contact_layout = QHBoxLayout(self.header_contact)
        self.header_contact_layout.setObjectName(u"header_contact_layout")
        self.header_contact_layout.setContentsMargins(40, 16, 40, 16)
        self.contact_icon = QLabel(self.header_contact)
        self.contact_icon.setObjectName(u"contact_icon")
        self.contact_icon.setMinimumSize(QSize(36, 36))
        self.contact_icon.setMaximumSize(QSize(36, 36))
        self.contact_icon.setStyleSheet(u"background: transparent;")
        self.contact_icon.setPixmap(QPixmap(u":/Icon/Icons/lock_white.svg"))
        self.contact_icon.setScaledContents(True)

        self.header_contact_layout.addWidget(self.contact_icon)

        self.contact_text_layout = QVBoxLayout()
        self.contact_text_layout.setSpacing(2)
        self.contact_text_layout.setObjectName(u"contact_text_layout")
        self.contact_title = QLabel(self.header_contact)
        self.contact_title.setObjectName(u"contact_title")
        self.contact_title.setStyleSheet(u"color: #ffffff; font-size: 18px; font-weight: 700; background: transparent;")

        self.contact_text_layout.addWidget(self.contact_title)

        self.contact_subtitle = QLabel(self.header_contact)
        self.contact_subtitle.setObjectName(u"contact_subtitle")
        self.contact_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.contact_text_layout.addWidget(self.contact_subtitle)


        self.header_contact_layout.addLayout(self.contact_text_layout)

        self.contact_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_contact_layout.addItem(self.contact_header_spacer)


        self.layout_contact.addWidget(self.header_contact)

        self.card_contact = QFrame(self.page_contact)
        self.card_contact.setObjectName(u"card_contact")
        self.card_contact.setFrameShape(QFrame.Shape.NoFrame)
        self.contact_content = QVBoxLayout(self.card_contact)
        self.contact_content.setSpacing(18)
        self.contact_content.setObjectName(u"contact_content")
        self.contact_content.setContentsMargins(40, 30, 40, 30)
        self.section_contact_header_layout = QHBoxLayout()
        self.section_contact_header_layout.setSpacing(10)
        self.section_contact_header_layout.setObjectName(u"section_contact_header_layout")
        self.section_contact_icon = QLabel(self.card_contact)
        self.section_contact_icon.setObjectName(u"section_contact_icon")
        self.section_contact_icon.setMinimumSize(QSize(20, 20))
        self.section_contact_icon.setMaximumSize(QSize(20, 20))
        self.section_contact_icon.setPixmap(QPixmap(u":/Icon/Icons/phone.svg"))
        self.section_contact_icon.setScaledContents(True)

        self.section_contact_header_layout.addWidget(self.section_contact_icon)

        self.section_contact_title = QLabel(self.card_contact)
        self.section_contact_title.setObjectName(u"section_contact_title")
        self.section_contact_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.section_contact_header_layout.addWidget(self.section_contact_title)

        self.section_contact_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.section_contact_header_layout.addItem(self.section_contact_spacer)


        self.contact_content.addLayout(self.section_contact_header_layout)

        self.form_contact = QFormLayout()
        self.form_contact.setObjectName(u"form_contact")
        self.form_contact.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.form_contact.setHorizontalSpacing(20)
        self.form_contact.setVerticalSpacing(12)
        self.label_email = QLabel(self.card_contact)
        self.label_email.setObjectName(u"label_email")

        self.form_contact.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_email)

        self.input_email = QLineEdit(self.card_contact)
        self.input_email.setObjectName(u"input_email")
        self.input_email.setMinimumSize(QSize(0, 44))

        self.form_contact.setWidget(0, QFormLayout.ItemRole.FieldRole, self.input_email)

        self.label_phone = QLabel(self.card_contact)
        self.label_phone.setObjectName(u"label_phone")

        self.form_contact.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_phone)

        self.input_phone = QLineEdit(self.card_contact)
        self.input_phone.setObjectName(u"input_phone")
        self.input_phone.setMinimumSize(QSize(0, 44))

        self.form_contact.setWidget(1, QFormLayout.ItemRole.FieldRole, self.input_phone)


        self.contact_content.addLayout(self.form_contact)

        self.divider_contact = QFrame(self.card_contact)
        self.divider_contact.setObjectName(u"divider_contact")
        self.divider_contact.setFrameShape(QFrame.Shape.HLine)

        self.contact_content.addWidget(self.divider_contact)

        self.section_security_header_layout = QHBoxLayout()
        self.section_security_header_layout.setSpacing(10)
        self.section_security_header_layout.setObjectName(u"section_security_header_layout")
        self.section_security_icon = QLabel(self.card_contact)
        self.section_security_icon.setObjectName(u"section_security_icon")
        self.section_security_icon.setMinimumSize(QSize(20, 20))
        self.section_security_icon.setMaximumSize(QSize(20, 20))
        self.section_security_icon.setPixmap(QPixmap(u":/Icon/Icons/lock.svg"))
        self.section_security_icon.setScaledContents(True)

        self.section_security_header_layout.addWidget(self.section_security_icon)

        self.section_security_title = QLabel(self.card_contact)
        self.section_security_title.setObjectName(u"section_security_title")
        self.section_security_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.section_security_header_layout.addWidget(self.section_security_title)

        self.section_security_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.section_security_header_layout.addItem(self.section_security_spacer)


        self.contact_content.addLayout(self.section_security_header_layout)

        self.form_security = QFormLayout()
        self.form_security.setObjectName(u"form_security")
        self.form_security.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.form_security.setHorizontalSpacing(20)
        self.form_security.setVerticalSpacing(12)
        self.label_password = QLabel(self.card_contact)
        self.label_password.setObjectName(u"label_password")

        self.form_security.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_password)

        self.input_password = QLineEdit(self.card_contact)
        self.input_password.setObjectName(u"input_password")
        self.input_password.setMinimumSize(QSize(0, 44))
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.form_security.setWidget(0, QFormLayout.ItemRole.FieldRole, self.input_password)

        self.label_password_confirm = QLabel(self.card_contact)
        self.label_password_confirm.setObjectName(u"label_password_confirm")

        self.form_security.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_password_confirm)

        self.input_password_confirm = QLineEdit(self.card_contact)
        self.input_password_confirm.setObjectName(u"input_password_confirm")
        self.input_password_confirm.setMinimumSize(QSize(0, 44))
        self.input_password_confirm.setEchoMode(QLineEdit.EchoMode.Password)

        self.form_security.setWidget(1, QFormLayout.ItemRole.FieldRole, self.input_password_confirm)


        self.contact_content.addLayout(self.form_security)

        self.label_pwd_error = QLabel(self.card_contact)
        self.label_pwd_error.setObjectName(u"label_pwd_error")
        self.label_pwd_error.setWordWrap(True)

        self.contact_content.addWidget(self.label_pwd_error)

        self.contact_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.contact_content.addItem(self.contact_bottom_spacer)


        self.layout_contact.addWidget(self.card_contact)

        Wizard.addPage(self.page_contact)
        self.page_pharmacy = QWizardPage()
        self.page_pharmacy.setObjectName(u"page_pharmacy")
        self.layout_pharmacy = QVBoxLayout(self.page_pharmacy)
        self.layout_pharmacy.setSpacing(0)
        self.layout_pharmacy.setObjectName(u"layout_pharmacy")
        self.layout_pharmacy.setContentsMargins(0, 0, 0, 0)
        self.header_pharmacy = QFrame(self.page_pharmacy)
        self.header_pharmacy.setObjectName(u"header_pharmacy")
        self.header_pharmacy.setMinimumSize(QSize(0, 80))
        self.header_pharmacy.setMaximumSize(QSize(16777215, 80))
        self.header_pharmacy_layout = QHBoxLayout(self.header_pharmacy)
        self.header_pharmacy_layout.setObjectName(u"header_pharmacy_layout")
        self.header_pharmacy_layout.setContentsMargins(40, 16, 40, 16)
        self.pharmacy_icon = QLabel(self.header_pharmacy)
        self.pharmacy_icon.setObjectName(u"pharmacy_icon")
        self.pharmacy_icon.setMinimumSize(QSize(36, 36))
        self.pharmacy_icon.setMaximumSize(QSize(36, 36))
        self.pharmacy_icon.setStyleSheet(u"background: transparent;")
        self.pharmacy_icon.setPixmap(QPixmap(u":/Icon/Icons/pharmacy_white.svg"))
        self.pharmacy_icon.setScaledContents(True)

        self.header_pharmacy_layout.addWidget(self.pharmacy_icon)

        self.pharmacy_text_layout = QVBoxLayout()
        self.pharmacy_text_layout.setSpacing(2)
        self.pharmacy_text_layout.setObjectName(u"pharmacy_text_layout")
        self.pharmacy_title = QLabel(self.header_pharmacy)
        self.pharmacy_title.setObjectName(u"pharmacy_title")
        self.pharmacy_title.setStyleSheet(u"color: #ffffff; font-size: 18px; font-weight: 700; background: transparent;")

        self.pharmacy_text_layout.addWidget(self.pharmacy_title)

        self.pharmacy_subtitle = QLabel(self.header_pharmacy)
        self.pharmacy_subtitle.setObjectName(u"pharmacy_subtitle")
        self.pharmacy_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.pharmacy_text_layout.addWidget(self.pharmacy_subtitle)


        self.header_pharmacy_layout.addLayout(self.pharmacy_text_layout)

        self.pharmacy_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_pharmacy_layout.addItem(self.pharmacy_header_spacer)


        self.layout_pharmacy.addWidget(self.header_pharmacy)

        self.card_pharmacy = QFrame(self.page_pharmacy)
        self.card_pharmacy.setObjectName(u"card_pharmacy")
        self.card_pharmacy.setFrameShape(QFrame.Shape.NoFrame)
        self.pharmacy_content = QVBoxLayout(self.card_pharmacy)
        self.pharmacy_content.setSpacing(18)
        self.pharmacy_content.setObjectName(u"pharmacy_content")
        self.pharmacy_content.setContentsMargins(40, 30, 40, 30)
        self.logo_layout = QVBoxLayout()
        self.logo_layout.setSpacing(10)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_label = QLabel(self.card_pharmacy)
        self.logo_label.setObjectName(u"logo_label")
        self.logo_label.setMinimumSize(QSize(120, 120))
        self.logo_label.setMaximumSize(QSize(120, 120))
        self.logo_label.setStyleSheet(u"#logo_label {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f8fafc, stop:1 #e2e8f0);\n"
"    border: 2px dashed #94A3B8;\n"
"    border-radius: 16px;\n"
"    color: #64748b;\n"
"    font-size: 11px;\n"
"    font-weight: 500;\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}\n"
"#logo_label:hover { border: 2px dashed #00B4D8; }")
        self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_layout.addWidget(self.logo_label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.btn_upload_logo = QPushButton(self.card_pharmacy)
        self.btn_upload_logo.setObjectName(u"btn_upload_logo")
        self.btn_upload_logo.setMinimumSize(QSize(158, 40))
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/upload_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_upload_logo.setIcon(icon1)
        self.btn_upload_logo.setIconSize(QSize(16, 16))

        self.logo_layout.addWidget(self.btn_upload_logo, 0, Qt.AlignmentFlag.AlignHCenter)

        self.logo_hint = QLabel(self.card_pharmacy)
        self.logo_hint.setObjectName(u"logo_hint")
        self.logo_hint.setStyleSheet(u"color: #94A3B8; font-size: 11px; background: transparent;")

        self.logo_layout.addWidget(self.logo_hint, 0, Qt.AlignmentFlag.AlignHCenter)


        self.pharmacy_content.addLayout(self.logo_layout)

        self.divider_pharmacy_1 = QFrame(self.card_pharmacy)
        self.divider_pharmacy_1.setObjectName(u"divider_pharmacy_1")
        self.divider_pharmacy_1.setFrameShape(QFrame.Shape.HLine)

        self.pharmacy_content.addWidget(self.divider_pharmacy_1)

        self.section_pharmacy_id_header_layout = QHBoxLayout()
        self.section_pharmacy_id_header_layout.setSpacing(10)
        self.section_pharmacy_id_header_layout.setObjectName(u"section_pharmacy_id_header_layout")
        self.section_pharmacy_id_icon = QLabel(self.card_pharmacy)
        self.section_pharmacy_id_icon.setObjectName(u"section_pharmacy_id_icon")
        self.section_pharmacy_id_icon.setMinimumSize(QSize(20, 20))
        self.section_pharmacy_id_icon.setMaximumSize(QSize(20, 20))
        self.section_pharmacy_id_icon.setPixmap(QPixmap(u":/Icon/Icons/pharmacy.svg"))
        self.section_pharmacy_id_icon.setScaledContents(True)

        self.section_pharmacy_id_header_layout.addWidget(self.section_pharmacy_id_icon)

        self.section_pharmacy_id_title = QLabel(self.card_pharmacy)
        self.section_pharmacy_id_title.setObjectName(u"section_pharmacy_id_title")
        self.section_pharmacy_id_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.section_pharmacy_id_header_layout.addWidget(self.section_pharmacy_id_title)

        self.section_pharmacy_id_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.section_pharmacy_id_header_layout.addItem(self.section_pharmacy_id_spacer)


        self.pharmacy_content.addLayout(self.section_pharmacy_id_header_layout)

        self.form_pharmacy_id = QFormLayout()
        self.form_pharmacy_id.setObjectName(u"form_pharmacy_id")
        self.form_pharmacy_id.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.form_pharmacy_id.setHorizontalSpacing(20)
        self.form_pharmacy_id.setVerticalSpacing(12)
        self.label_name_pharmacy = QLabel(self.card_pharmacy)
        self.label_name_pharmacy.setObjectName(u"label_name_pharmacy")

        self.form_pharmacy_id.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_name_pharmacy)

        self.input_name_pharmacy = QLineEdit(self.card_pharmacy)
        self.input_name_pharmacy.setObjectName(u"input_name_pharmacy")
        self.input_name_pharmacy.setMinimumSize(QSize(0, 44))

        self.form_pharmacy_id.setWidget(0, QFormLayout.ItemRole.FieldRole, self.input_name_pharmacy)

        self.label_type_pharmacy = QLabel(self.card_pharmacy)
        self.label_type_pharmacy.setObjectName(u"label_type_pharmacy")

        self.form_pharmacy_id.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_type_pharmacy)

        self.input_type_pharmacy = QComboBox(self.card_pharmacy)
        self.input_type_pharmacy.addItem("")
        self.input_type_pharmacy.addItem("")
        self.input_type_pharmacy.addItem("")
        self.input_type_pharmacy.setObjectName(u"input_type_pharmacy")
        self.input_type_pharmacy.setMinimumSize(QSize(0, 44))

        self.form_pharmacy_id.setWidget(1, QFormLayout.ItemRole.FieldRole, self.input_type_pharmacy)


        self.pharmacy_content.addLayout(self.form_pharmacy_id)

        self.divider_pharmacy_2 = QFrame(self.card_pharmacy)
        self.divider_pharmacy_2.setObjectName(u"divider_pharmacy_2")
        self.divider_pharmacy_2.setFrameShape(QFrame.Shape.HLine)

        self.pharmacy_content.addWidget(self.divider_pharmacy_2)

        self.section_pharmacy_contact_header_layout = QHBoxLayout()
        self.section_pharmacy_contact_header_layout.setSpacing(10)
        self.section_pharmacy_contact_header_layout.setObjectName(u"section_pharmacy_contact_header_layout")
        self.section_pharmacy_contact_icon = QLabel(self.card_pharmacy)
        self.section_pharmacy_contact_icon.setObjectName(u"section_pharmacy_contact_icon")
        self.section_pharmacy_contact_icon.setMinimumSize(QSize(20, 20))
        self.section_pharmacy_contact_icon.setMaximumSize(QSize(20, 20))
        self.section_pharmacy_contact_icon.setPixmap(QPixmap(u":/Icon/Icons/map-pin.svg"))
        self.section_pharmacy_contact_icon.setScaledContents(True)

        self.section_pharmacy_contact_header_layout.addWidget(self.section_pharmacy_contact_icon)

        self.section_pharmacy_contact_title = QLabel(self.card_pharmacy)
        self.section_pharmacy_contact_title.setObjectName(u"section_pharmacy_contact_title")
        self.section_pharmacy_contact_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.section_pharmacy_contact_header_layout.addWidget(self.section_pharmacy_contact_title)

        self.section_pharmacy_contact_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.section_pharmacy_contact_header_layout.addItem(self.section_pharmacy_contact_spacer)


        self.pharmacy_content.addLayout(self.section_pharmacy_contact_header_layout)

        self.form_pharmacy_contact = QFormLayout()
        self.form_pharmacy_contact.setObjectName(u"form_pharmacy_contact")
        self.form_pharmacy_contact.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.form_pharmacy_contact.setHorizontalSpacing(20)
        self.form_pharmacy_contact.setVerticalSpacing(12)
        self.label_email_pharmacy = QLabel(self.card_pharmacy)
        self.label_email_pharmacy.setObjectName(u"label_email_pharmacy")

        self.form_pharmacy_contact.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_email_pharmacy)

        self.input_email_pharmacy = QLineEdit(self.card_pharmacy)
        self.input_email_pharmacy.setObjectName(u"input_email_pharmacy")
        self.input_email_pharmacy.setMinimumSize(QSize(0, 44))

        self.form_pharmacy_contact.setWidget(0, QFormLayout.ItemRole.FieldRole, self.input_email_pharmacy)

        self.label_phone_pharmacy = QLabel(self.card_pharmacy)
        self.label_phone_pharmacy.setObjectName(u"label_phone_pharmacy")

        self.form_pharmacy_contact.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_phone_pharmacy)

        self.input_phone_pharmacy = QLineEdit(self.card_pharmacy)
        self.input_phone_pharmacy.setObjectName(u"input_phone_pharmacy")
        self.input_phone_pharmacy.setMinimumSize(QSize(0, 44))

        self.form_pharmacy_contact.setWidget(1, QFormLayout.ItemRole.FieldRole, self.input_phone_pharmacy)

        self.label_adress = QLabel(self.card_pharmacy)
        self.label_adress.setObjectName(u"label_adress")

        self.form_pharmacy_contact.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_adress)

        self.input_adress = QLineEdit(self.card_pharmacy)
        self.input_adress.setObjectName(u"input_adress")
        self.input_adress.setMinimumSize(QSize(0, 44))

        self.form_pharmacy_contact.setWidget(2, QFormLayout.ItemRole.FieldRole, self.input_adress)


        self.pharmacy_content.addLayout(self.form_pharmacy_contact)

        self.pharmacy_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.pharmacy_content.addItem(self.pharmacy_bottom_spacer)


        self.layout_pharmacy.addWidget(self.card_pharmacy)

        Wizard.addPage(self.page_pharmacy)
        self.page_settings = QWizardPage()
        self.page_settings.setObjectName(u"page_settings")
        self.layout_settings = QVBoxLayout(self.page_settings)
        self.layout_settings.setSpacing(0)
        self.layout_settings.setObjectName(u"layout_settings")
        self.layout_settings.setContentsMargins(0, 0, 0, 0)
        self.header_settings = QFrame(self.page_settings)
        self.header_settings.setObjectName(u"header_settings")
        self.header_settings.setMinimumSize(QSize(0, 80))
        self.header_settings.setMaximumSize(QSize(16777215, 80))
        self.header_settings_layout = QHBoxLayout(self.header_settings)
        self.header_settings_layout.setObjectName(u"header_settings_layout")
        self.header_settings_layout.setContentsMargins(40, 16, 40, 16)
        self.settings_icon = QLabel(self.header_settings)
        self.settings_icon.setObjectName(u"settings_icon")
        self.settings_icon.setMinimumSize(QSize(36, 36))
        self.settings_icon.setMaximumSize(QSize(36, 36))
        self.settings_icon.setStyleSheet(u"background: transparent;")
        self.settings_icon.setPixmap(QPixmap(u":/Icon/Icons/settings_white.svg"))
        self.settings_icon.setScaledContents(True)

        self.header_settings_layout.addWidget(self.settings_icon)

        self.settings_text_layout = QVBoxLayout()
        self.settings_text_layout.setSpacing(2)
        self.settings_text_layout.setObjectName(u"settings_text_layout")
        self.settings_title = QLabel(self.header_settings)
        self.settings_title.setObjectName(u"settings_title")
        self.settings_title.setStyleSheet(u"color: #ffffff; font-size: 18px; font-weight: 700; background: transparent;")

        self.settings_text_layout.addWidget(self.settings_title)

        self.settings_subtitle = QLabel(self.header_settings)
        self.settings_subtitle.setObjectName(u"settings_subtitle")
        self.settings_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.settings_text_layout.addWidget(self.settings_subtitle)


        self.header_settings_layout.addLayout(self.settings_text_layout)

        self.settings_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_settings_layout.addItem(self.settings_header_spacer)


        self.layout_settings.addWidget(self.header_settings)

        self.card_settings = QFrame(self.page_settings)
        self.card_settings.setObjectName(u"card_settings")
        self.card_settings.setFrameShape(QFrame.Shape.NoFrame)
        self.settings_content = QVBoxLayout(self.card_settings)
        self.settings_content.setSpacing(20)
        self.settings_content.setObjectName(u"settings_content")
        self.settings_content.setContentsMargins(40, 30, 40, 30)
        self.section_stock_header_layout = QHBoxLayout()
        self.section_stock_header_layout.setSpacing(10)
        self.section_stock_header_layout.setObjectName(u"section_stock_header_layout")
        self.section_stock_icon = QLabel(self.card_settings)
        self.section_stock_icon.setObjectName(u"section_stock_icon")
        self.section_stock_icon.setMinimumSize(QSize(20, 20))
        self.section_stock_icon.setMaximumSize(QSize(20, 20))
        self.section_stock_icon.setPixmap(QPixmap(u":/Icon/Icons/archive.svg"))
        self.section_stock_icon.setScaledContents(True)

        self.section_stock_header_layout.addWidget(self.section_stock_icon)

        self.section_stock_title = QLabel(self.card_settings)
        self.section_stock_title.setObjectName(u"section_stock_title")
        self.section_stock_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.section_stock_header_layout.addWidget(self.section_stock_title)

        self.section_stock_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.section_stock_header_layout.addItem(self.section_stock_spacer)


        self.settings_content.addLayout(self.section_stock_header_layout)

        self.form_stock = QFormLayout()
        self.form_stock.setObjectName(u"form_stock")
        self.form_stock.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.form_stock.setHorizontalSpacing(20)
        self.form_stock.setVerticalSpacing(12)
        self.label_low_stock = QLabel(self.card_settings)
        self.label_low_stock.setObjectName(u"label_low_stock")

        self.form_stock.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_low_stock)

        self.low_stock_layout = QHBoxLayout()
        self.low_stock_layout.setObjectName(u"low_stock_layout")
        self.input_low_stock_threshold = QSpinBox(self.card_settings)
        self.input_low_stock_threshold.setObjectName(u"input_low_stock_threshold")
        self.input_low_stock_threshold.setMinimumSize(QSize(0, 44))
        self.input_low_stock_threshold.setMinimum(1)
        self.input_low_stock_threshold.setMaximum(1000)
        self.input_low_stock_threshold.setValue(25)

        self.low_stock_layout.addWidget(self.input_low_stock_threshold)


        self.form_stock.setLayout(0, QFormLayout.ItemRole.FieldRole, self.low_stock_layout)


        self.settings_content.addLayout(self.form_stock)

        self.stock_help_box = QFrame(self.card_settings)
        self.stock_help_box.setObjectName(u"stock_help_box")
        self.stock_help_box.setStyleSheet(u"#stock_help_box {\n"
"    background-color: #fefce8;\n"
"    border: 1px solid #fef08a;\n"
"    border-left: 4px solid #F4A261;\n"
"    border-radius: 10px;\n"
"    padding: 12px 16px;\n"
"}")
        self.stock_help_layout = QVBoxLayout(self.stock_help_box)
        self.stock_help_layout.setSpacing(6)
        self.stock_help_layout.setObjectName(u"stock_help_layout")
        self.stock_help_title_layout = QHBoxLayout()
        self.stock_help_title_layout.setSpacing(8)
        self.stock_help_title_layout.setObjectName(u"stock_help_title_layout")
        self.stock_help_icon = QLabel(self.stock_help_box)
        self.stock_help_icon.setObjectName(u"stock_help_icon")
        self.stock_help_icon.setMinimumSize(QSize(16, 16))
        self.stock_help_icon.setMaximumSize(QSize(16, 16))
        self.stock_help_icon.setPixmap(QPixmap(u":/Icon/Icons/star.svg"))
        self.stock_help_icon.setScaledContents(True)

        self.stock_help_title_layout.addWidget(self.stock_help_icon)

        self.stock_help_title = QLabel(self.stock_help_box)
        self.stock_help_title.setObjectName(u"stock_help_title")
        self.stock_help_title.setStyleSheet(u"color: #854d0e; font-size: 12px; font-weight: 600; background: transparent;")

        self.stock_help_title_layout.addWidget(self.stock_help_title)

        self.stock_help_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.stock_help_title_layout.addItem(self.stock_help_spacer)


        self.stock_help_layout.addLayout(self.stock_help_title_layout)

        self.stock_help_text = QLabel(self.stock_help_box)
        self.stock_help_text.setObjectName(u"stock_help_text")
        self.stock_help_text.setStyleSheet(u"color: #a16207; font-size: 11px; background: transparent;")

        self.stock_help_layout.addWidget(self.stock_help_text)


        self.settings_content.addWidget(self.stock_help_box)

        self.divider_settings = QFrame(self.card_settings)
        self.divider_settings.setObjectName(u"divider_settings")
        self.divider_settings.setFrameShape(QFrame.Shape.HLine)

        self.settings_content.addWidget(self.divider_settings)

        self.section_pricing_header_layout = QHBoxLayout()
        self.section_pricing_header_layout.setSpacing(10)
        self.section_pricing_header_layout.setObjectName(u"section_pricing_header_layout")
        self.section_pricing_icon = QLabel(self.card_settings)
        self.section_pricing_icon.setObjectName(u"section_pricing_icon")
        self.section_pricing_icon.setMinimumSize(QSize(20, 20))
        self.section_pricing_icon.setMaximumSize(QSize(20, 20))
        self.section_pricing_icon.setPixmap(QPixmap(u":/Icon/Icons/percent.svg"))
        self.section_pricing_icon.setScaledContents(True)

        self.section_pricing_header_layout.addWidget(self.section_pricing_icon)

        self.section_pricing_title = QLabel(self.card_settings)
        self.section_pricing_title.setObjectName(u"section_pricing_title")
        self.section_pricing_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 15px; font-weight: 700; background: transparent; }")

        self.section_pricing_header_layout.addWidget(self.section_pricing_title)

        self.section_pricing_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.section_pricing_header_layout.addItem(self.section_pricing_spacer)


        self.settings_content.addLayout(self.section_pricing_header_layout)

        self.form_pricing = QFormLayout()
        self.form_pricing.setObjectName(u"form_pricing")
        self.form_pricing.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.form_pricing.setHorizontalSpacing(20)
        self.form_pricing.setVerticalSpacing(12)
        self.label_profit_margin = QLabel(self.card_settings)
        self.label_profit_margin.setObjectName(u"label_profit_margin")

        self.form_pricing.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_profit_margin)

        self.profit_margin_layout = QHBoxLayout()
        self.profit_margin_layout.setObjectName(u"profit_margin_layout")
        self.input_profit_margin = QDoubleSpinBox(self.card_settings)
        self.input_profit_margin.setObjectName(u"input_profit_margin")
        self.input_profit_margin.setMinimumSize(QSize(0, 44))
        self.input_profit_margin.setDecimals(1)
        self.input_profit_margin.setMinimum(0.000000000000000)
        self.input_profit_margin.setMaximum(0.000000000000000)
        self.input_profit_margin.setValue(0.000000000000000)

        self.profit_margin_layout.addWidget(self.input_profit_margin)


        self.form_pricing.setLayout(0, QFormLayout.ItemRole.FieldRole, self.profit_margin_layout)


        self.settings_content.addLayout(self.form_pricing)

        self.pricing_help_box = QFrame(self.card_settings)
        self.pricing_help_box.setObjectName(u"pricing_help_box")
        self.pricing_help_box.setStyleSheet(u"#pricing_help_box {\n"
"    background-color: #f0fdf4;\n"
"    border: 1px solid #bbf7d0;\n"
"    border-left: 4px solid #16A34A;\n"
"    border-radius: 10px;\n"
"    padding: 12px 16px;\n"
"}")
        self.pricing_help_layout = QVBoxLayout(self.pricing_help_box)
        self.pricing_help_layout.setSpacing(6)
        self.pricing_help_layout.setObjectName(u"pricing_help_layout")
        self.pricing_help_title_layout = QHBoxLayout()
        self.pricing_help_title_layout.setSpacing(8)
        self.pricing_help_title_layout.setObjectName(u"pricing_help_title_layout")
        self.pricing_help_icon = QLabel(self.pricing_help_box)
        self.pricing_help_icon.setObjectName(u"pricing_help_icon")
        self.pricing_help_icon.setMinimumSize(QSize(16, 16))
        self.pricing_help_icon.setMaximumSize(QSize(16, 16))
        self.pricing_help_icon.setPixmap(QPixmap(u":/Icon/Icons/calculator.svg"))
        self.pricing_help_icon.setScaledContents(True)

        self.pricing_help_title_layout.addWidget(self.pricing_help_icon)

        self.pricing_help_title = QLabel(self.pricing_help_box)
        self.pricing_help_title.setObjectName(u"pricing_help_title")
        self.pricing_help_title.setStyleSheet(u"color: #166534; font-size: 12px; font-weight: 600; background: transparent;")

        self.pricing_help_title_layout.addWidget(self.pricing_help_title)

        self.pricing_help_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pricing_help_title_layout.addItem(self.pricing_help_spacer)


        self.pricing_help_layout.addLayout(self.pricing_help_title_layout)

        self.pricing_help_text = QLabel(self.pricing_help_box)
        self.pricing_help_text.setObjectName(u"pricing_help_text")
        self.pricing_help_text.setStyleSheet(u"color: #15803d; font-size: 11px; background: transparent;")

        self.pricing_help_layout.addWidget(self.pricing_help_text)


        self.settings_content.addWidget(self.pricing_help_box)

        self.settings_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settings_content.addItem(self.settings_bottom_spacer)


        self.layout_settings.addWidget(self.card_settings)

        Wizard.addPage(self.page_settings)
        self.page_summary = QWizardPage()
        self.page_summary.setObjectName(u"page_summary")
        self.layout_summary = QVBoxLayout(self.page_summary)
        self.layout_summary.setSpacing(0)
        self.layout_summary.setObjectName(u"layout_summary")
        self.layout_summary.setContentsMargins(0, 0, 0, 0)
        self.header_summary = QFrame(self.page_summary)
        self.header_summary.setObjectName(u"header_summary")
        self.header_summary.setMinimumSize(QSize(0, 80))
        self.header_summary.setMaximumSize(QSize(16777215, 80))
        self.header_summary_layout = QHBoxLayout(self.header_summary)
        self.header_summary_layout.setObjectName(u"header_summary_layout")
        self.header_summary_layout.setContentsMargins(40, 16, 40, 16)
        self.summary_icon = QLabel(self.header_summary)
        self.summary_icon.setObjectName(u"summary_icon")
        self.summary_icon.setMinimumSize(QSize(36, 36))
        self.summary_icon.setMaximumSize(QSize(36, 36))
        self.summary_icon.setStyleSheet(u"background: transparent;")
        self.summary_icon.setPixmap(QPixmap(u":/Icon/Icons/check-circle_white.svg"))
        self.summary_icon.setScaledContents(True)

        self.header_summary_layout.addWidget(self.summary_icon)

        self.summary_text_layout = QVBoxLayout()
        self.summary_text_layout.setSpacing(2)
        self.summary_text_layout.setObjectName(u"summary_text_layout")
        self.summary_title = QLabel(self.header_summary)
        self.summary_title.setObjectName(u"summary_title")
        self.summary_title.setStyleSheet(u"color: #ffffff; font-size: 18px; font-weight: 700; background: transparent;")

        self.summary_text_layout.addWidget(self.summary_title)

        self.summary_subtitle = QLabel(self.header_summary)
        self.summary_subtitle.setObjectName(u"summary_subtitle")
        self.summary_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.summary_text_layout.addWidget(self.summary_subtitle)


        self.header_summary_layout.addLayout(self.summary_text_layout)

        self.summary_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_summary_layout.addItem(self.summary_header_spacer)


        self.layout_summary.addWidget(self.header_summary)

        self.card_summary = QFrame(self.page_summary)
        self.card_summary.setObjectName(u"card_summary")
        self.card_summary.setFrameShape(QFrame.Shape.NoFrame)
        self.summary_content = QVBoxLayout(self.card_summary)
        self.summary_content.setSpacing(16)
        self.summary_content.setObjectName(u"summary_content")
        self.summary_content.setContentsMargins(40, 30, 40, 30)
        self.summary_section_1_header_layout = QHBoxLayout()
        self.summary_section_1_header_layout.setSpacing(10)
        self.summary_section_1_header_layout.setObjectName(u"summary_section_1_header_layout")
        self.summary_section_1_icon = QLabel(self.card_summary)
        self.summary_section_1_icon.setObjectName(u"summary_section_1_icon")
        self.summary_section_1_icon.setMinimumSize(QSize(20, 20))
        self.summary_section_1_icon.setMaximumSize(QSize(20, 20))
        self.summary_section_1_icon.setPixmap(QPixmap(u":/Icon/Icons/identity.svg"))
        self.summary_section_1_icon.setScaledContents(True)

        self.summary_section_1_header_layout.addWidget(self.summary_section_1_icon)

        self.summary_section_1_title = QLabel(self.card_summary)
        self.summary_section_1_title.setObjectName(u"summary_section_1_title")
        self.summary_section_1_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 14px; font-weight: 700; background: transparent; }")

        self.summary_section_1_header_layout.addWidget(self.summary_section_1_title)

        self.summary_section_1_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.summary_section_1_header_layout.addItem(self.summary_section_1_spacer)


        self.summary_content.addLayout(self.summary_section_1_header_layout)

        self.summary_grid_1 = QGridLayout()
        self.summary_grid_1.setObjectName(u"summary_grid_1")
        self.summary_grid_1.setHorizontalSpacing(16)
        self.summary_grid_1.setVerticalSpacing(10)
        self.summary_card_name = QFrame(self.card_summary)
        self.summary_card_name.setObjectName(u"summary_card_name")
        self.summary_card_name.setStyleSheet(u".summary_card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }")
        self.sc_name_layout = QVBoxLayout(self.summary_card_name)
        self.sc_name_layout.setSpacing(2)
        self.sc_name_layout.setObjectName(u"sc_name_layout")
        self.sc_name_label = QLabel(self.summary_card_name)
        self.sc_name_label.setObjectName(u"sc_name_label")
        self.sc_name_label.setStyleSheet(u".summary_label { color: #94A3B8; font-size: 10px; font-weight: 600; background: transparent; letter-spacing: 0.5px; }")

        self.sc_name_layout.addWidget(self.sc_name_label)

        self.sc_name_value = QLabel(self.summary_card_name)
        self.sc_name_value.setObjectName(u"sc_name_value")
        self.sc_name_value.setStyleSheet(u".summary_value { color: #1e293b; font-size: 13px; font-weight: 600; background: transparent; }")

        self.sc_name_layout.addWidget(self.sc_name_value)


        self.summary_grid_1.addWidget(self.summary_card_name, 0, 0, 1, 1)

        self.summary_card_email = QFrame(self.card_summary)
        self.summary_card_email.setObjectName(u"summary_card_email")
        self.summary_card_email.setStyleSheet(u".summary_card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }")
        self.sc_email_layout = QVBoxLayout(self.summary_card_email)
        self.sc_email_layout.setSpacing(2)
        self.sc_email_layout.setObjectName(u"sc_email_layout")
        self.sc_email_label = QLabel(self.summary_card_email)
        self.sc_email_label.setObjectName(u"sc_email_label")
        self.sc_email_label.setStyleSheet(u".summary_label { color: #94A3B8; font-size: 10px; font-weight: 600; background: transparent; letter-spacing: 0.5px; }")

        self.sc_email_layout.addWidget(self.sc_email_label)

        self.sc_email_value = QLabel(self.summary_card_email)
        self.sc_email_value.setObjectName(u"sc_email_value")
        self.sc_email_value.setStyleSheet(u".summary_value { color: #1e293b; font-size: 13px; font-weight: 600; background: transparent; }")

        self.sc_email_layout.addWidget(self.sc_email_value)


        self.summary_grid_1.addWidget(self.summary_card_email, 0, 1, 1, 1)

        self.summary_card_phone = QFrame(self.card_summary)
        self.summary_card_phone.setObjectName(u"summary_card_phone")
        self.summary_card_phone.setStyleSheet(u".summary_card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }")
        self.sc_phone_layout = QVBoxLayout(self.summary_card_phone)
        self.sc_phone_layout.setSpacing(2)
        self.sc_phone_layout.setObjectName(u"sc_phone_layout")
        self.sc_phone_label = QLabel(self.summary_card_phone)
        self.sc_phone_label.setObjectName(u"sc_phone_label")
        self.sc_phone_label.setStyleSheet(u".summary_label { color: #94A3B8; font-size: 10px; font-weight: 600; background: transparent; letter-spacing: 0.5px; }")

        self.sc_phone_layout.addWidget(self.sc_phone_label)

        self.sc_phone_value = QLabel(self.summary_card_phone)
        self.sc_phone_value.setObjectName(u"sc_phone_value")
        self.sc_phone_value.setStyleSheet(u".summary_value { color: #1e293b; font-size: 13px; font-weight: 600; background: transparent; }")

        self.sc_phone_layout.addWidget(self.sc_phone_value)


        self.summary_grid_1.addWidget(self.summary_card_phone, 1, 0, 1, 1)

        self.summary_card_role = QFrame(self.card_summary)
        self.summary_card_role.setObjectName(u"summary_card_role")
        self.summary_card_role.setStyleSheet(u".summary_card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }")
        self.sc_role_layout = QVBoxLayout(self.summary_card_role)
        self.sc_role_layout.setSpacing(2)
        self.sc_role_layout.setObjectName(u"sc_role_layout")
        self.sc_role_label = QLabel(self.summary_card_role)
        self.sc_role_label.setObjectName(u"sc_role_label")
        self.sc_role_label.setStyleSheet(u".summary_label { color: #94A3B8; font-size: 10px; font-weight: 600; background: transparent; letter-spacing: 0.5px; }")

        self.sc_role_layout.addWidget(self.sc_role_label)

        self.sc_role_value = QLabel(self.summary_card_role)
        self.sc_role_value.setObjectName(u"sc_role_value")
        self.sc_role_value.setStyleSheet(u".summary_value { color: #1e293b; font-size: 13px; font-weight: 600; background: transparent; }")

        self.sc_role_layout.addWidget(self.sc_role_value)


        self.summary_grid_1.addWidget(self.summary_card_role, 1, 1, 1, 1)


        self.summary_content.addLayout(self.summary_grid_1)

        self.summary_section_2_header_layout = QHBoxLayout()
        self.summary_section_2_header_layout.setSpacing(10)
        self.summary_section_2_header_layout.setObjectName(u"summary_section_2_header_layout")
        self.summary_section_2_icon = QLabel(self.card_summary)
        self.summary_section_2_icon.setObjectName(u"summary_section_2_icon")
        self.summary_section_2_icon.setMinimumSize(QSize(20, 20))
        self.summary_section_2_icon.setMaximumSize(QSize(20, 20))
        self.summary_section_2_icon.setPixmap(QPixmap(u":/Icon/Icons/pharmacy.svg"))
        self.summary_section_2_icon.setScaledContents(True)

        self.summary_section_2_header_layout.addWidget(self.summary_section_2_icon)

        self.summary_section_2_title = QLabel(self.card_summary)
        self.summary_section_2_title.setObjectName(u"summary_section_2_title")
        self.summary_section_2_title.setStyleSheet(u".section_title { color: #023E8A; font-size: 14px; font-weight: 700; background: transparent; }")

        self.summary_section_2_header_layout.addWidget(self.summary_section_2_title)

        self.summary_section_2_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.summary_section_2_header_layout.addItem(self.summary_section_2_spacer)


        self.summary_content.addLayout(self.summary_section_2_header_layout)

        self.summary_grid_2 = QGridLayout()
        self.summary_grid_2.setObjectName(u"summary_grid_2")
        self.summary_grid_2.setHorizontalSpacing(16)
        self.summary_grid_2.setVerticalSpacing(10)
        self.summary_card_pharmacy_name = QFrame(self.card_summary)
        self.summary_card_pharmacy_name.setObjectName(u"summary_card_pharmacy_name")
        self.summary_card_pharmacy_name.setStyleSheet(u".summary_card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }")
        self.sc_pname_layout = QVBoxLayout(self.summary_card_pharmacy_name)
        self.sc_pname_layout.setSpacing(2)
        self.sc_pname_layout.setObjectName(u"sc_pname_layout")
        self.sc_pname_label = QLabel(self.summary_card_pharmacy_name)
        self.sc_pname_label.setObjectName(u"sc_pname_label")
        self.sc_pname_label.setStyleSheet(u".summary_label { color: #94A3B8; font-size: 10px; font-weight: 600; background: transparent; letter-spacing: 0.5px; }")

        self.sc_pname_layout.addWidget(self.sc_pname_label)

        self.sc_pname_value = QLabel(self.summary_card_pharmacy_name)
        self.sc_pname_value.setObjectName(u"sc_pname_value")
        self.sc_pname_value.setStyleSheet(u".summary_value { color: #1e293b; font-size: 13px; font-weight: 600; background: transparent; }")

        self.sc_pname_layout.addWidget(self.sc_pname_value)


        self.summary_grid_2.addWidget(self.summary_card_pharmacy_name, 0, 0, 1, 1)

        self.summary_card_pharmacy_type = QFrame(self.card_summary)
        self.summary_card_pharmacy_type.setObjectName(u"summary_card_pharmacy_type")
        self.summary_card_pharmacy_type.setStyleSheet(u".summary_card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }")
        self.sc_ptype_layout = QVBoxLayout(self.summary_card_pharmacy_type)
        self.sc_ptype_layout.setSpacing(2)
        self.sc_ptype_layout.setObjectName(u"sc_ptype_layout")
        self.sc_ptype_label = QLabel(self.summary_card_pharmacy_type)
        self.sc_ptype_label.setObjectName(u"sc_ptype_label")
        self.sc_ptype_label.setStyleSheet(u".summary_label { color: #94A3B8; font-size: 10px; font-weight: 600; background: transparent; letter-spacing: 0.5px; }")

        self.sc_ptype_layout.addWidget(self.sc_ptype_label)

        self.sc_ptype_value = QLabel(self.summary_card_pharmacy_type)
        self.sc_ptype_value.setObjectName(u"sc_ptype_value")
        self.sc_ptype_value.setStyleSheet(u".summary_value { color: #1e293b; font-size: 13px; font-weight: 600; background: transparent; }")

        self.sc_ptype_layout.addWidget(self.sc_ptype_value)


        self.summary_grid_2.addWidget(self.summary_card_pharmacy_type, 0, 1, 1, 1)

        self.summary_card_address = QFrame(self.card_summary)
        self.summary_card_address.setObjectName(u"summary_card_address")
        self.summary_card_address.setStyleSheet(u".summary_card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }")
        self.sc_addr_layout = QVBoxLayout(self.summary_card_address)
        self.sc_addr_layout.setSpacing(2)
        self.sc_addr_layout.setObjectName(u"sc_addr_layout")
        self.sc_addr_label = QLabel(self.summary_card_address)
        self.sc_addr_label.setObjectName(u"sc_addr_label")
        self.sc_addr_label.setStyleSheet(u".summary_label { color: #94A3B8; font-size: 10px; font-weight: 600; background: transparent; letter-spacing: 0.5px; }")

        self.sc_addr_layout.addWidget(self.sc_addr_label)

        self.sc_addr_value = QLabel(self.summary_card_address)
        self.sc_addr_value.setObjectName(u"sc_addr_value")
        self.sc_addr_value.setStyleSheet(u".summary_value { color: #1e293b; font-size: 13px; font-weight: 600; background: transparent; }")

        self.sc_addr_layout.addWidget(self.sc_addr_value)


        self.summary_grid_2.addWidget(self.summary_card_address, 1, 0, 1, 1)

        self.summary_card_margin = QFrame(self.card_summary)
        self.summary_card_margin.setObjectName(u"summary_card_margin")
        self.summary_card_margin.setStyleSheet(u".summary_card { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px 16px; }")
        self.sc_margin_layout = QVBoxLayout(self.summary_card_margin)
        self.sc_margin_layout.setSpacing(2)
        self.sc_margin_layout.setObjectName(u"sc_margin_layout")
        self.sc_margin_label = QLabel(self.summary_card_margin)
        self.sc_margin_label.setObjectName(u"sc_margin_label")
        self.sc_margin_label.setStyleSheet(u".summary_label { color: #94A3B8; font-size: 10px; font-weight: 600; background: transparent; letter-spacing: 0.5px; }")

        self.sc_margin_layout.addWidget(self.sc_margin_label)

        self.sc_margin_value = QLabel(self.summary_card_margin)
        self.sc_margin_value.setObjectName(u"sc_margin_value")
        self.sc_margin_value.setStyleSheet(u".summary_value { color: #1e293b; font-size: 13px; font-weight: 600; background: transparent; }")

        self.sc_margin_layout.addWidget(self.sc_margin_value)


        self.summary_grid_2.addWidget(self.summary_card_margin, 1, 1, 1, 1)


        self.summary_content.addLayout(self.summary_grid_2)

        self.divider_summary = QFrame(self.card_summary)
        self.divider_summary.setObjectName(u"divider_summary")
        self.divider_summary.setFrameShape(QFrame.Shape.HLine)

        self.summary_content.addWidget(self.divider_summary)

        self.summary_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.summary_content.addItem(self.summary_bottom_spacer)


        self.layout_summary.addWidget(self.card_summary)

        Wizard.addPage(self.page_summary)
        self.page_client_config = QWizardPage()
        self.page_client_config.setObjectName(u"page_client_config")
        self.layout_client_config = QVBoxLayout(self.page_client_config)
        self.layout_client_config.setSpacing(0)
        self.layout_client_config.setObjectName(u"layout_client_config")
        self.layout_client_config.setContentsMargins(0, 0, 0, 0)
        self.header_client_config = QFrame(self.page_client_config)
        self.header_client_config.setObjectName(u"header_client_config")
        self.header_client_config.setMinimumSize(QSize(0, 80))
        self.header_client_config.setMaximumSize(QSize(16777215, 80))
        self.header_client_config_layout = QHBoxLayout(self.header_client_config)
        self.header_client_config_layout.setObjectName(u"header_client_config_layout")
        self.header_client_config_layout.setContentsMargins(40, 16, 40, 16)
        self.client_config_icon = QLabel(self.header_client_config)
        self.client_config_icon.setObjectName(u"client_config_icon")
        self.client_config_icon.setMinimumSize(QSize(36, 36))
        self.client_config_icon.setMaximumSize(QSize(36, 36))
        self.client_config_icon.setStyleSheet(u"background: transparent;")
        self.client_config_icon.setPixmap(QPixmap(u":/Icon/Icons/wifi_white.svg"))
        self.client_config_icon.setScaledContents(True)

        self.header_client_config_layout.addWidget(self.client_config_icon)

        self.client_config_text_layout = QVBoxLayout()
        self.client_config_text_layout.setSpacing(2)
        self.client_config_text_layout.setObjectName(u"client_config_text_layout")
        self.client_config_title = QLabel(self.header_client_config)
        self.client_config_title.setObjectName(u"client_config_title")
        self.client_config_title.setStyleSheet(u"color: #ffffff; font-size: 18px; font-weight: 700; background: transparent;")

        self.client_config_text_layout.addWidget(self.client_config_title)

        self.client_config_subtitle = QLabel(self.header_client_config)
        self.client_config_subtitle.setObjectName(u"client_config_subtitle")
        self.client_config_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.client_config_text_layout.addWidget(self.client_config_subtitle)


        self.header_client_config_layout.addLayout(self.client_config_text_layout)

        self.client_config_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_client_config_layout.addItem(self.client_config_header_spacer)


        self.layout_client_config.addWidget(self.header_client_config)

        self.card_client_config = QFrame(self.page_client_config)
        self.card_client_config.setObjectName(u"card_client_config")
        self.card_client_config.setFrameShape(QFrame.Shape.NoFrame)
        self.client_config_content = QVBoxLayout(self.card_client_config)
        self.client_config_content.setSpacing(18)
        self.client_config_content.setObjectName(u"client_config_content")
        self.client_config_content.setContentsMargins(40, 30, 40, 30)
        self.client_info_box = QFrame(self.card_client_config)
        self.client_info_box.setObjectName(u"client_info_box")
        self.client_info_box.setStyleSheet(u"#client_info_box {\n"
"    background-color: #eff6ff;\n"
"    border: 1px solid #bfdbfe;\n"
"    border-left: 4px solid #00B4D8;\n"
"    border-radius: 10px;\n"
"    padding: 14px 18px;\n"
"}")
        self.client_info_layout = QVBoxLayout(self.client_info_box)
        self.client_info_layout.setSpacing(6)
        self.client_info_layout.setObjectName(u"client_info_layout")
        self.client_info_title_layout = QHBoxLayout()
        self.client_info_title_layout.setSpacing(8)
        self.client_info_title_layout.setObjectName(u"client_info_title_layout")
        self.client_info_icon = QLabel(self.client_info_box)
        self.client_info_icon.setObjectName(u"client_info_icon")
        self.client_info_icon.setMinimumSize(QSize(18, 18))
        self.client_info_icon.setMaximumSize(QSize(18, 18))
        self.client_info_icon.setPixmap(QPixmap(u":/Icon/Icons/info.svg"))
        self.client_info_icon.setScaledContents(True)

        self.client_info_title_layout.addWidget(self.client_info_icon)

        self.client_info_title = QLabel(self.client_info_box)
        self.client_info_title.setObjectName(u"client_info_title")
        self.client_info_title.setStyleSheet(u"color: #1e40af; font-size: 12px; font-weight: 700; background: transparent;")

        self.client_info_title_layout.addWidget(self.client_info_title)

        self.client_info_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.client_info_title_layout.addItem(self.client_info_spacer)


        self.client_info_layout.addLayout(self.client_info_title_layout)

        self.client_info_desc = QLabel(self.client_info_box)
        self.client_info_desc.setObjectName(u"client_info_desc")
        self.client_info_desc.setStyleSheet(u"color: #1e40af; font-size: 11px; background: transparent;")
        self.client_info_desc.setWordWrap(True)

        self.client_info_layout.addWidget(self.client_info_desc)


        self.client_config_content.addWidget(self.client_info_box)

        self.client_config_form = QFormLayout()
        self.client_config_form.setObjectName(u"client_config_form")
        self.client_config_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.client_config_form.setHorizontalSpacing(20)
        self.client_config_form.setVerticalSpacing(12)
        self.label_client_host = QLabel(self.card_client_config)
        self.label_client_host.setObjectName(u"label_client_host")

        self.client_config_form.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_client_host)

        self.input_client_host = QLineEdit(self.card_client_config)
        self.input_client_host.setObjectName(u"input_client_host")
        self.input_client_host.setMinimumSize(QSize(0, 44))

        self.client_config_form.setWidget(0, QFormLayout.ItemRole.FieldRole, self.input_client_host)

        self.label_client_port = QLabel(self.card_client_config)
        self.label_client_port.setObjectName(u"label_client_port")

        self.client_config_form.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_client_port)

        self.input_client_port = QSpinBox(self.card_client_config)
        self.input_client_port.setObjectName(u"input_client_port")
        self.input_client_port.setMinimumSize(QSize(0, 44))
        self.input_client_port.setMinimum(1)
        self.input_client_port.setMaximum(65535)
        self.input_client_port.setValue(5001)

        self.client_config_form.setWidget(1, QFormLayout.ItemRole.FieldRole, self.input_client_port)


        self.client_config_content.addLayout(self.client_config_form)

        self.btn_client_test = QPushButton(self.card_client_config)
        self.btn_client_test.setObjectName(u"btn_client_test")
        self.btn_client_test.setMinimumSize(QSize(166, 48))
        self.btn_client_test.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/refresh_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_client_test.setIcon(icon2)
        self.btn_client_test.setIconSize(QSize(16, 16))

        self.client_config_content.addWidget(self.btn_client_test)

        self.label_client_test_result = QLabel(self.card_client_config)
        self.label_client_test_result.setObjectName(u"label_client_test_result")
        self.label_client_test_result.setMinimumSize(QSize(0, 60))
        self.label_client_test_result.setStyleSheet(u"#label_client_test_result {\n"
"    background-color: #f8fafc;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 10px;\n"
"    padding: 12px 16px;\n"
"    color: #64748b;\n"
"    font-size: 12px;\n"
"    font-weight: 600;\n"
"}\n"
"#label_client_test_result[status=\"success\"] {\n"
"    background-color: #dcfce7;\n"
"    border: 1px solid #bbf7d0;\n"
"    color: #15803d;\n"
"}\n"
"#label_client_test_result[status=\"error\"] {\n"
"    background-color: #fee2e2;\n"
"    border: 1px solid #fecaca;\n"
"    color: #b91c1c;\n"
"}\n"
"#label_client_test_result[status=\"pending\"] {\n"
"    background-color: #eff6ff;\n"
"    border: 1px solid #bfdbfe;\n"
"    color: #1e40af;\n"
"}")
        self.label_client_test_result.setWordWrap(True)

        self.client_config_content.addWidget(self.label_client_test_result)

        self.client_config_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.client_config_content.addItem(self.client_config_bottom_spacer)


        self.layout_client_config.addWidget(self.card_client_config)

        Wizard.addPage(self.page_client_config)
        self.page_client_summary = QWizardPage()
        self.page_client_summary.setObjectName(u"page_client_summary")
        self.layout_client_summary = QVBoxLayout(self.page_client_summary)
        self.layout_client_summary.setSpacing(0)
        self.layout_client_summary.setObjectName(u"layout_client_summary")
        self.layout_client_summary.setContentsMargins(0, 0, 0, 0)
        self.header_client_summary = QFrame(self.page_client_summary)
        self.header_client_summary.setObjectName(u"header_client_summary")
        self.header_client_summary.setMinimumSize(QSize(0, 80))
        self.header_client_summary.setMaximumSize(QSize(16777215, 80))
        self.header_client_summary_layout = QHBoxLayout(self.header_client_summary)
        self.header_client_summary_layout.setObjectName(u"header_client_summary_layout")
        self.header_client_summary_layout.setContentsMargins(40, 16, 40, 16)
        self.client_summary_icon = QLabel(self.header_client_summary)
        self.client_summary_icon.setObjectName(u"client_summary_icon")
        self.client_summary_icon.setMinimumSize(QSize(36, 36))
        self.client_summary_icon.setMaximumSize(QSize(36, 36))
        self.client_summary_icon.setStyleSheet(u"background: transparent;")
        self.client_summary_icon.setPixmap(QPixmap(u":/Icon/Icons/check-circle_white.svg"))
        self.client_summary_icon.setScaledContents(True)

        self.header_client_summary_layout.addWidget(self.client_summary_icon)

        self.client_summary_text_layout = QVBoxLayout()
        self.client_summary_text_layout.setSpacing(2)
        self.client_summary_text_layout.setObjectName(u"client_summary_text_layout")
        self.client_summary_title = QLabel(self.header_client_summary)
        self.client_summary_title.setObjectName(u"client_summary_title")
        self.client_summary_title.setStyleSheet(u"color: #ffffff; font-size: 18px; font-weight: 700; background: transparent;")

        self.client_summary_text_layout.addWidget(self.client_summary_title)

        self.client_summary_subtitle = QLabel(self.header_client_summary)
        self.client_summary_subtitle.setObjectName(u"client_summary_subtitle")
        self.client_summary_subtitle.setStyleSheet(u"color: #CAF0F8; font-size: 12px; background: transparent;")

        self.client_summary_text_layout.addWidget(self.client_summary_subtitle)


        self.header_client_summary_layout.addLayout(self.client_summary_text_layout)

        self.client_summary_header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_client_summary_layout.addItem(self.client_summary_header_spacer)


        self.layout_client_summary.addWidget(self.header_client_summary)

        self.card_client_summary = QFrame(self.page_client_summary)
        self.card_client_summary.setObjectName(u"card_client_summary")
        self.card_client_summary.setFrameShape(QFrame.Shape.NoFrame)
        self.client_summary_content = QVBoxLayout(self.card_client_summary)
        self.client_summary_content.setSpacing(18)
        self.client_summary_content.setObjectName(u"client_summary_content")
        self.client_summary_content.setContentsMargins(40, 30, 40, 30)
        self.client_summary_success_box = QFrame(self.card_client_summary)
        self.client_summary_success_box.setObjectName(u"client_summary_success_box")
        self.client_summary_success_box.setStyleSheet(u"#client_summary_success_box {\n"
"    background-color: #f0fdf4;\n"
"    border: 1px solid #bbf7d0;\n"
"    border-radius: 14px;\n"
"}")
        self.client_summary_success_layout = QVBoxLayout(self.client_summary_success_box)
        self.client_summary_success_layout.setSpacing(8)
        self.client_summary_success_layout.setObjectName(u"client_summary_success_layout")
        self.client_summary_success_layout.setContentsMargins(24, 22, 24, 22)
        self.client_summary_check_icon = QLabel(self.client_summary_success_box)
        self.client_summary_check_icon.setObjectName(u"client_summary_check_icon")
        self.client_summary_check_icon.setMinimumSize(QSize(56, 56))
        self.client_summary_check_icon.setMaximumSize(QSize(56, 56))
        self.client_summary_check_icon.setPixmap(QPixmap(u":/Icon/Icons/check-circle.svg"))
        self.client_summary_check_icon.setScaledContents(True)

        self.client_summary_success_layout.addWidget(self.client_summary_check_icon, 0, Qt.AlignmentFlag.AlignHCenter)

        self.client_summary_success_title = QLabel(self.client_summary_success_box)
        self.client_summary_success_title.setObjectName(u"client_summary_success_title")
        self.client_summary_success_title.setStyleSheet(u"color: #15803d; font-size: 16px; font-weight: 800; background: transparent;")
        self.client_summary_success_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.client_summary_success_layout.addWidget(self.client_summary_success_title)

        self.client_summary_details = QLabel(self.client_summary_success_box)
        self.client_summary_details.setObjectName(u"client_summary_details")
        self.client_summary_details.setStyleSheet(u"color: #166534; font-size: 13px; font-weight: 600; background: transparent;")
        self.client_summary_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.client_summary_details.setWordWrap(True)

        self.client_summary_success_layout.addWidget(self.client_summary_details)


        self.client_summary_content.addWidget(self.client_summary_success_box)

        self.client_summary_info_box = QFrame(self.card_client_summary)
        self.client_summary_info_box.setObjectName(u"client_summary_info_box")
        self.client_summary_info_box.setStyleSheet(u"#client_summary_info_box {\n"
"    background-color: #eff6ff;\n"
"    border: 1px solid #bfdbfe;\n"
"    border-left: 4px solid #00B4D8;\n"
"    border-radius: 10px;\n"
"    padding: 14px 18px;\n"
"}")
        self.client_summary_info_layout = QHBoxLayout(self.client_summary_info_box)
        self.client_summary_info_layout.setSpacing(10)
        self.client_summary_info_layout.setObjectName(u"client_summary_info_layout")
        self.client_summary_info_icon = QLabel(self.client_summary_info_box)
        self.client_summary_info_icon.setObjectName(u"client_summary_info_icon")
        self.client_summary_info_icon.setMinimumSize(QSize(20, 20))
        self.client_summary_info_icon.setMaximumSize(QSize(20, 20))
        self.client_summary_info_icon.setPixmap(QPixmap(u":/Icon/Icons/info.svg"))
        self.client_summary_info_icon.setScaledContents(True)

        self.client_summary_info_layout.addWidget(self.client_summary_info_icon)

        self.client_summary_info_text = QLabel(self.client_summary_info_box)
        self.client_summary_info_text.setObjectName(u"client_summary_info_text")
        self.client_summary_info_text.setStyleSheet(u"color: #1e40af; font-size: 12px; background: transparent;")
        self.client_summary_info_text.setWordWrap(True)

        self.client_summary_info_layout.addWidget(self.client_summary_info_text)


        self.client_summary_content.addWidget(self.client_summary_info_box)

        self.client_summary_bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.client_summary_content.addItem(self.client_summary_bottom_spacer)


        self.layout_client_summary.addWidget(self.card_client_summary)

        Wizard.addPage(self.page_client_summary)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"Nova Pharma \u2014 Inscription", None))
        self.page_type.setTitle("")
        self.page_type.setSubTitle("")
        self.type_title.setText(QCoreApplication.translate("Wizard", u"Type d'installation", None))
        self.type_subtitle.setText(QCoreApplication.translate("Wizard", u"Comment ce poste utilisera-t-il Nova Pharma ?", None))
        self.type_question.setText(QCoreApplication.translate("Wizard", u"S\u00e9lectionnez le r\u00f4le de ce poste :", None))
        self.type_server_title.setText(QCoreApplication.translate("Wizard", u"Serveur principal", None))
        self.type_server_desc.setText(QCoreApplication.translate("Wizard", u"Ce PC h\u00e9berge la base de donn\u00e9es et partage les donn\u00e9es avec les autres postes du r\u00e9seau. Il doit rester allum\u00e9 pour que les autres postes puissent travailler.", None))
        self.radio_type_server.setText("")
        self.type_client_title.setText(QCoreApplication.translate("Wizard", u"Poste client", None))
        self.type_client_desc.setText(QCoreApplication.translate("Wizard", u"Ce PC se connecte \u00e0 un serveur distant. Id\u00e9al pour les caisses secondaires, les vendeurs, ou tout poste qui n'h\u00e9berge pas les donn\u00e9es.", None))
        self.radio_type_client.setText("")
        self.page_welcome.setTitle("")
        self.page_welcome.setSubTitle("")
        self.welcome_title.setText(QCoreApplication.translate("Wizard", u"NOVA PHARMA", None))
        self.welcome_subtitle.setText(QCoreApplication.translate("Wizard", u"Pharmaceutical Management Software", None))
        self.welcome_main_title.setText(QCoreApplication.translate("Wizard", u"BIENVENUE SUR NOVA PHARMA", None))
        self.welcome_main_subtitle.setText(QCoreApplication.translate("Wizard", u"Logiciel de gestion pharmaceutique. enregistrez votre officine en quelques \u00e9tapes.", None))
        self.role_section_title.setText(QCoreApplication.translate("Wizard", u"Vous \u00eates :", None))
        self.pharmacien_label.setText(QCoreApplication.translate("Wizard", u"Pharmacien", None))
        self.pharmacien_desc.setText(QCoreApplication.translate("Wizard", u"Enregistrez votre officine et g\u00e9rez la visibilit\u00e9 de vos stocks sur la carte interactive de Nova Pharma.", None))
        self.f1_title.setText(QCoreApplication.translate("Wizard", u"Visibilit\u00e9", None))
        self.f1_desc.setText(QCoreApplication.translate("Wizard", u"R\u00e9f\u00e9rencez votre officine", None))
        self.f2_title.setText(QCoreApplication.translate("Wizard", u"Horaires 24/7", None))
        self.f2_desc.setText(QCoreApplication.translate("Wizard", u"G\u00e9rez votre garde", None))
        self.f3_title.setText(QCoreApplication.translate("Wizard", u"Stocks v\u00e9rifi\u00e9s", None))
        self.f3_desc.setText(QCoreApplication.translate("Wizard", u"Infos en temps r\u00e9el", None))
        self.page_identity.setTitle("")
        self.page_identity.setSubTitle("")
        self.identity_title.setText(QCoreApplication.translate("Wizard", u"Identit\u00e9 & Profil", None))
        self.identity_subtitle.setText(QCoreApplication.translate("Wizard", u"\u00c9tape 1 sur 4 \u2014 Renseignez vos informations personnelles", None))
        self.btn_upload_photo.setText(QCoreApplication.translate("Wizard", u"  Choisir une photo", None))
        self.photo_hint.setText(QCoreApplication.translate("Wizard", u"JPG, PNG ou GIF (max 5MB) \u2014 Optionnel", None))
        self.section_identity_title.setText(QCoreApplication.translate("Wizard", u"Identit\u00e9", None))
        self.label_first_name.setText(QCoreApplication.translate("Wizard", u"Pr\u00e9nom *", None))
        self.input_first_name.setPlaceholderText(QCoreApplication.translate("Wizard", u"Entrez votre pr\u00e9nom", None))
        self.label_name.setText(QCoreApplication.translate("Wizard", u"Nom *", None))
        self.input_name.setPlaceholderText(QCoreApplication.translate("Wizard", u"Entrez votre nom", None))
        self.label_last_name.setText(QCoreApplication.translate("Wizard", u"Post-nom *", None))
        self.input_last_name.setPlaceholderText(QCoreApplication.translate("Wizard", u"Entrez votre post-nom", None))
        self.section_demo_title.setText(QCoreApplication.translate("Wizard", u"D\u00e9mographie", None))
        self.label_sexe.setText(QCoreApplication.translate("Wizard", u"Sexe *", None))
        self.radio_homme.setText(QCoreApplication.translate("Wizard", u"Homme", None))
        self.radio_femme.setText(QCoreApplication.translate("Wizard", u"Femme", None))
        self.label_dob.setText(QCoreApplication.translate("Wizard", u"Date de naissance *", None))
        self.input_date_of_birth.setDisplayFormat(QCoreApplication.translate("Wizard", u"dd/MM/yyyy", None))
        self.label_age.setText(QCoreApplication.translate("Wizard", u"\u00c2ge", None))
        self.input_age.setSuffix(QCoreApplication.translate("Wizard", u" ans", None))
        self.label_nationality.setText(QCoreApplication.translate("Wizard", u"Nationalit\u00e9 *", None))
        self.input_nationality.setPlaceholderText(QCoreApplication.translate("Wizard", u"S\u00e9lectionnez votre nationalit\u00e9", None))
        self.page_contact.setTitle("")
        self.page_contact.setSubTitle("")
        self.contact_title.setText(QCoreApplication.translate("Wizard", u"Contact & S\u00e9curit\u00e9", None))
        self.contact_subtitle.setText(QCoreApplication.translate("Wizard", u"\u00c9tape 2 sur 4 \u2014 Vos coordonn\u00e9es et identifiants de connexion", None))
        self.section_contact_title.setText(QCoreApplication.translate("Wizard", u"Coordonn\u00e9es", None))
        self.label_email.setText(QCoreApplication.translate("Wizard", u"Email *", None))
        self.input_email.setPlaceholderText(QCoreApplication.translate("Wizard", u"exemple@email.com", None))
        self.label_phone.setText(QCoreApplication.translate("Wizard", u"T\u00e9l\u00e9phone *", None))
        self.input_phone.setPlaceholderText(QCoreApplication.translate("Wizard", u"+243 XXX XXX XXX", None))
        self.section_security_title.setText(QCoreApplication.translate("Wizard", u"Mot de passe", None))
        self.label_password.setText(QCoreApplication.translate("Wizard", u"Mot de passe *", None))
        self.input_password.setPlaceholderText(QCoreApplication.translate("Wizard", u"Entrez un mot de passe s\u00e9curis\u00e9", None))
        self.label_password_confirm.setText(QCoreApplication.translate("Wizard", u"Confirmation *", None))
        self.input_password_confirm.setPlaceholderText(QCoreApplication.translate("Wizard", u"R\u00e9p\u00e9tez le mot de passe", None))
        self.label_pwd_error.setText("")
        self.page_pharmacy.setTitle("")
        self.page_pharmacy.setSubTitle("")
        self.pharmacy_title.setText(QCoreApplication.translate("Wizard", u"Informations de l'Officine", None))
        self.pharmacy_subtitle.setText(QCoreApplication.translate("Wizard", u"\u00c9tape 3 sur 4 \u2014 Ces informations seront visibles sur la carte interactive", None))
        self.logo_label.setText(QCoreApplication.translate("Wizard", u"Logo", None))
        self.btn_upload_logo.setText(QCoreApplication.translate("Wizard", u"  Choisir un logo", None))
        self.logo_hint.setText(QCoreApplication.translate("Wizard", u"PNG, JPG (max 2MB)", None))
        self.section_pharmacy_id_title.setText(QCoreApplication.translate("Wizard", u"Identit\u00e9 de l'officine", None))
        self.label_name_pharmacy.setText(QCoreApplication.translate("Wizard", u"Nom de la pharmacie *", None))
        self.input_name_pharmacy.setPlaceholderText(QCoreApplication.translate("Wizard", u"Nom officiel de votre officine", None))
        self.label_type_pharmacy.setText(QCoreApplication.translate("Wizard", u"Type *", None))
        self.input_type_pharmacy.setItemText(0, QCoreApplication.translate("Wizard", u"Petite", None))
        self.input_type_pharmacy.setItemText(1, QCoreApplication.translate("Wizard", u"Moyenne", None))
        self.input_type_pharmacy.setItemText(2, QCoreApplication.translate("Wizard", u"Grande", None))

        self.input_type_pharmacy.setPlaceholderText(QCoreApplication.translate("Wizard", u"S\u00e9lectionnez le type", None))
        self.section_pharmacy_contact_title.setText(QCoreApplication.translate("Wizard", u"Contact & Localisation", None))
        self.label_email_pharmacy.setText(QCoreApplication.translate("Wizard", u"Email officine *", None))
        self.input_email_pharmacy.setPlaceholderText(QCoreApplication.translate("Wizard", u"contact@pharmacie.cd", None))
        self.label_phone_pharmacy.setText(QCoreApplication.translate("Wizard", u"T\u00e9l\u00e9phone officine *", None))
        self.input_phone_pharmacy.setPlaceholderText(QCoreApplication.translate("Wizard", u"+243 XXX XXX XXX", None))
        self.label_adress.setText(QCoreApplication.translate("Wizard", u"Adresse *", None))
        self.input_adress.setPlaceholderText(QCoreApplication.translate("Wizard", u"Ex: Avenue Kasa-Vubu, n\u00b0123, Kinshasa/Gombe", None))
        self.page_settings.setTitle("")
        self.page_settings.setSubTitle("")
        self.settings_title.setText(QCoreApplication.translate("Wizard", u"Param\u00e8tres de Gestion", None))
        self.settings_subtitle.setText(QCoreApplication.translate("Wizard", u"\u00c9tape 4 sur 4 \u2014 Configurez les param\u00e8tres de votre officine", None))
        self.section_stock_title.setText(QCoreApplication.translate("Wizard", u"Gestion des stocks", None))
        self.label_low_stock.setText(QCoreApplication.translate("Wizard", u"Seuil d'alerte stock *", None))
        self.input_low_stock_threshold.setSuffix(QCoreApplication.translate("Wizard", u" unit\u00e9s", None))
        self.stock_help_title.setText(QCoreApplication.translate("Wizard", u"Recommandations", None))
        self.stock_help_text.setText(QCoreApplication.translate("Wizard", u"Petite officine : 10 unit\u00e9s  \u2022  Moyenne : 25 unit\u00e9s  \u2022  Grande : 50+ unit\u00e9s", None))
        self.section_pricing_title.setText(QCoreApplication.translate("Wizard", u"Tarification", None))
        self.label_profit_margin.setText(QCoreApplication.translate("Wizard", u"Marge b\u00e9n\u00e9ficiaire *", None))
        self.input_profit_margin.setSuffix(QCoreApplication.translate("Wizard", u" %", None))
        self.pricing_help_title.setText(QCoreApplication.translate("Wizard", u"Exemple de calcul", None))
        self.pricing_help_text.setText(QCoreApplication.translate("Wizard", u"30% signifie : Prix de vente = Prix d'achat \u00d7 1,30", None))
        self.page_summary.setTitle("")
        self.page_summary.setSubTitle("")
        self.summary_title.setText(QCoreApplication.translate("Wizard", u"R\u00e9capitulatif", None))
        self.summary_subtitle.setText(QCoreApplication.translate("Wizard", u"V\u00e9rifiez vos informations avant de finaliser l'inscription", None))
        self.summary_section_1_title.setText(QCoreApplication.translate("Wizard", u"Identit\u00e9 & Profil", None))
        self.sc_name_label.setText(QCoreApplication.translate("Wizard", u"Nom complet", None))
        self.sc_name_value.setText(QCoreApplication.translate("Wizard", u"\u2014", None))
        self.sc_email_label.setText(QCoreApplication.translate("Wizard", u"Email", None))
        self.sc_email_value.setText(QCoreApplication.translate("Wizard", u"\u2014", None))
        self.sc_phone_label.setText(QCoreApplication.translate("Wizard", u"T\u00e9l\u00e9phone", None))
        self.sc_phone_value.setText(QCoreApplication.translate("Wizard", u"\u2014", None))
        self.sc_role_label.setText(QCoreApplication.translate("Wizard", u"R\u00f4le", None))
        self.sc_role_value.setText(QCoreApplication.translate("Wizard", u"Pharmacien", None))
        self.summary_section_2_title.setText(QCoreApplication.translate("Wizard", u"Informations Pharmacie", None))
        self.sc_pname_label.setText(QCoreApplication.translate("Wizard", u"Nom officine", None))
        self.sc_pname_value.setText(QCoreApplication.translate("Wizard", u"\u2014", None))
        self.sc_ptype_label.setText(QCoreApplication.translate("Wizard", u"Type", None))
        self.sc_ptype_value.setText(QCoreApplication.translate("Wizard", u"\u2014", None))
        self.sc_addr_label.setText(QCoreApplication.translate("Wizard", u"Adresse", None))
        self.sc_addr_value.setText(QCoreApplication.translate("Wizard", u"\u2014", None))
        self.sc_margin_label.setText(QCoreApplication.translate("Wizard", u"Marge b\u00e9n\u00e9ficiaire", None))
        self.sc_margin_value.setText(QCoreApplication.translate("Wizard", u"\u2014", None))
        self.page_client_config.setTitle("")
        self.page_client_config.setSubTitle("")
        self.client_config_title.setText(QCoreApplication.translate("Wizard", u"Connexion au serveur", None))
        self.client_config_subtitle.setText(QCoreApplication.translate("Wizard", u"Saisissez l'adresse du serveur Nova Pharma", None))
        self.client_info_title.setText(QCoreApplication.translate("Wizard", u"Comment obtenir l'adresse ?", None))
        self.client_info_desc.setText(QCoreApplication.translate("Wizard", u"Sur le PC serveur, ouvrez Nova Pharma \u2192 Param\u00e8tres \u2192 R\u00e9seau. L'adresse IP y est affich\u00e9e (ex : 192.168.1.15).", None))
        self.label_client_host.setText(QCoreApplication.translate("Wizard", u"Adresse IP du serveur *", None))
        self.input_client_host.setPlaceholderText(QCoreApplication.translate("Wizard", u"Ex : 192.168.1.15", None))
        self.label_client_port.setText(QCoreApplication.translate("Wizard", u"Port *", None))
        self.btn_client_test.setText(QCoreApplication.translate("Wizard", u"Tester la connexion au serveur", None))
        self.label_client_test_result.setText(QCoreApplication.translate("Wizard", u"Saisissez l'adresse IP puis cliquez sur \u00ab Tester la connexion \u00bb.", None))
        self.page_client_summary.setTitle("")
        self.page_client_summary.setSubTitle("")
        self.client_summary_title.setText(QCoreApplication.translate("Wizard", u"Configuration termin\u00e9e", None))
        self.client_summary_subtitle.setText(QCoreApplication.translate("Wizard", u"Ce poste est configur\u00e9 comme client", None))
        self.client_summary_success_title.setText(QCoreApplication.translate("Wizard", u"Poste client configur\u00e9", None))
        self.client_summary_details.setText(QCoreApplication.translate("Wizard", u"Serveur : \u2014", None))
        self.client_summary_info_text.setText(QCoreApplication.translate("Wizard", u"Prochaine \u00e9tape : connectez-vous avec un compte cr\u00e9\u00e9 par l'administrateur sur le serveur.", None))
    # retranslateUi

