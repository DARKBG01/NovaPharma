# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_loginnZuEWQ.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName(u"LoginDialog")
        LoginDialog.resize(1080, 740)
        LoginDialog.setMinimumSize(QSize(1000, 680))
        LoginDialog.setStyleSheet(u"/* ==================================================================\n"
"   NOVA PHARMA \u2014 LOGIN DESIGN SYSTEM v3\n"
"   ------------------------------------------------------------------\n"
"   Palette\n"
"     Fond droit      : #f4f6fb\n"
"     Carte formulaire: #ffffff / bordure #e6ebf2 / rayon 20px\n"
"     Sidebar         : #0b1220 -> #16233d (navy profond)\n"
"     Primaire        : #2563eb (hover #1d4ed8, pressed #1e40af)\n"
"     Texte           : #0f172a / #475569 / #94a3b8\n"
"     Succ\u00e8s          : #16a34a / fond #f0fdf4 / bord #bbf7d0\n"
"   ================================================================== */\n"
"\n"
"QDialog {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.4, y2:1,\n"
"                                      stop:0 #f6f8fc, stop:1 #eef2f7);\n"
"}\n"
"\n"
"QWidget {\n"
"    font-family: \"Segoe UI\", \"Inter\", \"Roboto\", \"Helvetica Neue\", sans-serif;\n"
"    font-size: 14px;\n"
"    color: #0f172a;\n"
"    outline: none;\n"
"    selection-backgr"
                        "ound-color: #bfdbfe;\n"
"    selection-color: #0f172a;\n"
"}\n"
"\n"
"QLabel { background-color: transparent; border: none; color: #1e293b; }\n"
"\n"
"QToolTip {\n"
"    background-color: #0f172a;\n"
"    color: #f8fafc;\n"
"    border: 1px solid #334155;\n"
"    border-radius: 6px;\n"
"    padding: 6px 10px;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"/* --------------------------- SIDEBAR --------------------------- */\n"
"QFrame#frameSidebar {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.7, y2:1,\n"
"                                      stop:0 #0b1220, stop:0.55 #101c33, stop:1 #1d4ed8);\n"
"    border: none;\n"
"}\n"
"QFrame#frameSidebar QLabel { background-color: transparent; }\n"
"\n"
"/* Pastille ic\u00f4ne principale (verre d\u00e9poli) */\n"
"QLabel#labelIconContainer {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
"                                      stop:0 rgba(59, 130, 246, 90),\n"
"                                      stop:1 rgba(37, 99,"
                        " 235, 55));\n"
"    border: 1px solid rgba(255, 255, 255, 45);\n"
"    border-radius: 20px;\n"
"    padding: 15px;\n"
"}\n"
"\n"
"QLabel#labelTitle {\n"
"    color: #ffffff;\n"
"    font-size: 34px;\n"
"    font-weight: 800;\n"
"    letter-spacing: -0.6px;\n"
"}\n"
"\n"
"QLabel#labelDesc {\n"
"    color: #bfdbfe;\n"
"    font-size: 14px;\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"/* Liste de features sidebar */\n"
"QFrame#frameFeatureRow {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"QLabel#labelFeatureIcon {\n"
"    background-color: rgba(59, 130, 246, 40);\n"
"    border: 1px solid rgba(255, 255, 255, 30);\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"}\n"
"QLabel#labelFeatureText {\n"
"    color: #e0e7ff;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"/* Badge d'information (carte verre) */\n"
"QFrame#frameBadgeInfo {\n"
"    background-color: rgba(255, 255, 255, 16);\n"
"    border: 1px solid rgba(255, 255, 255, 30);\n"
"    border-radius: 16px;\n"
"}\n"
""
                        "QLabel#labelBadgeIcon {\n"
"    background-color: rgba(59, 130, 246, 60);\n"
"    border: 1px solid rgba(255, 255, 255, 40);\n"
"    border-radius: 8px;\n"
"    padding: 5px;\n"
"}\n"
"QLabel#labelBadgeTitle {\n"
"    color: #ffffff;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"}\n"
"QLabel#labelBadgeText {\n"
"    color: #93c5fd;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"QLabel#labelVersion {\n"
"    color: rgba(255, 255, 255, 110);\n"
"    font-size: 11px;\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"/* ---------------------- COLONNE FORMULAIRE ---------------------- */\n"
"QFrame#frameFormContainer { background-color: transparent; border: none; }\n"
"\n"
"/* Carte principale */\n"
"QFrame#frameFormFields {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 20px;\n"
"}\n"
"\n"
"QLabel#labelHeader {\n"
"    font-size: 26px;\n"
"    font-weight: 800;\n"
"    color: #0f172a;\n"
"    letter-spacing: -0.4px;\n"
"}\n"
"\n"
"QLabel#labelSubhead"
                        "er {\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    color: #64748b;\n"
"}\n"
"\n"
"QLabel#labelUser, QLabel#labelPassword {\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    color: #64748b;\n"
"    letter-spacing: 0.8px;\n"
"}\n"
"\n"
"QLabel#labelForgot {\n"
"    color: #2563eb;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"}\n"
"QLabel#labelForgot:hover { color: #1d4ed8; }\n"
"\n"
"QLabel#labelHelp { color: #64748b; font-size: 13px; }\n"
"\n"
"/* ------------------------- CHAMPS DE SAISIE ------------------------- */\n"
"QFrame#frameUsernameField, QFrame#framePasswordField {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #dbe3ec;\n"
"    border-radius: 12px;\n"
"}\n"
"QFrame#frameUsernameField:hover, QFrame#framePasswordField:hover {\n"
"    border: 1px solid #b9c6d8;\n"
"}\n"
"QFrame#frameUsernameField[focused=\"true\"],\n"
"QFrame#framePasswordField[focused=\"true\"] {\n"
"    border: 1px solid #2563eb;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QLineEdit#"
                        "lineEdit_username, QLineEdit#lineEdit_password {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    padding: 0;\n"
"    font-size: 14px;\n"
"    font-weight: 500;\n"
"    color: #0f172a;\n"
"    selection-background-color: #bfdbfe;\n"
"    selection-color: #0f172a;\n"
"}\n"
"\n"
"QToolButton#btn_toggle_pwd {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"}\n"
"QToolButton#btn_toggle_pwd:hover {\n"
"    background-color: #eff6ff;\n"
"}\n"
"\n"
"/* ----------------------------- BOUTON ----------------------------- */\n"
"QPushButton#pushButton_login {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #3b82f6, stop:1 #2563eb);\n"
"    color: #ffffff;\n"
"    border: 1px solid #1d4ed8;\n"
"    border-radius: 12px;\n"
"    padding: 14px;\n"
"    font-size: 15px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 0.2px;\n"
"}\n"
"QPushButton#pushButton_logi"
                        "n:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 #2f74e8, stop:1 #1d4ed8);\n"
"    border: 1px solid #1e40af;\n"
"}\n"
"QPushButton#pushButton_login:pressed {\n"
"    background-color: #1e40af;\n"
"    border: 1px solid #1e3a8a;\n"
"}\n"
"QPushButton#pushButton_login:disabled {\n"
"    background-color: #cbd5e1;\n"
"    border: 1px solid #cbd5e1;\n"
"    color: #f8fafc;\n"
"}\n"
"\n"
"/* ---------------------------- CHECKBOX ---------------------------- */\n"
"QCheckBox {\n"
"    spacing: 10px;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    color: #475569;\n"
"    background-color: transparent;\n"
"}\n"
"QCheckBox::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    border-radius: 6px;\n"
"    border: 1px solid #cbd5e1;\n"
"    background-color: #ffffff;\n"
"}\n"
"QCheckBox::indicator:hover { border: 1px solid #2563eb; }\n"
"QCheckBox::indicator:checked {\n"
"    background-color: #2563eb;\n"
"    bor"
                        "der: 1px solid #2563eb;\n"
"    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEwIDgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTEgNEwzLjUgNi41TDkgMSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L3N2Zz4=);\n"
"}\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: #1d4ed8;\n"
"    border: 1px solid #1d4ed8;\n"
"}\n"
"\n"
"/* ------------------------ BANNI\u00c8RE ERREUR ------------------------ */\n"
"QFrame#frameError {\n"
"    background-color: #fef2f2;\n"
"    border: 1px solid #fecaca;\n"
"    border-left: 4px solid #dc2626;\n"
"    border-radius: 10px;\n"
"}\n"
"QLabel#labelErrorText {\n"
"    color: #991b1b;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"}\n"
"\n"
"/* --------------------------- S\u00c9PARATEUR --------------------------- */\n"
"QFrame#frameDivider {\n"
"    background-color: #eef2f7;\n"
"    border: none;\n"
"    max-height: 1px;\n"
"}\n"
"\n"
""
                        "/* ------------------------- FOOTER / LEGAL ------------------------- */\n"
"QFrame#frameLegal {\n"
"    background-color: #f8fafc;\n"
"    border: none;\n"
"    border-top: 1px solid #e6ebf2;\n"
"}\n"
"QLabel#labelLegalText {\n"
"    color: #94a3b8;\n"
"    font-size: 11px;\n"
"    font-weight: 500;\n"
"}\n"
"QLabel#labelLegalIcon {\n"
"    background-color: transparent;\n"
"    padding: 0;\n"
"}\n"
"")
        self.horizontalLayout_root = QHBoxLayout(LoginDialog)
        self.horizontalLayout_root.setSpacing(0)
        self.horizontalLayout_root.setObjectName(u"horizontalLayout_root")
        self.horizontalLayout_root.setContentsMargins(0, 0, 0, 0)
        self.frameSidebar = QFrame(LoginDialog)
        self.frameSidebar.setObjectName(u"frameSidebar")
        self.frameSidebar.setMinimumSize(QSize(440, 0))
        self.frameSidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_sidebar = QVBoxLayout(self.frameSidebar)
        self.verticalLayout_sidebar.setSpacing(22)
        self.verticalLayout_sidebar.setObjectName(u"verticalLayout_sidebar")
        self.verticalLayout_sidebar.setContentsMargins(48, 64, 44, 40)
        self.labelIconContainer = QLabel(self.frameSidebar)
        self.labelIconContainer.setObjectName(u"labelIconContainer")
        self.labelIconContainer.setMinimumSize(QSize(72, 72))
        self.labelIconContainer.setMaximumSize(QSize(72, 72))
        self.labelIconContainer.setPixmap(QPixmap(u":/Icon/Icons/pill_white.svg"))
        self.labelIconContainer.setScaledContents(True)
        self.labelIconContainer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_sidebar.addWidget(self.labelIconContainer)

        self.labelTitle = QLabel(self.frameSidebar)
        self.labelTitle.setObjectName(u"labelTitle")

        self.verticalLayout_sidebar.addWidget(self.labelTitle)

        self.labelDesc = QLabel(self.frameSidebar)
        self.labelDesc.setObjectName(u"labelDesc")
        self.labelDesc.setWordWrap(True)

        self.verticalLayout_sidebar.addWidget(self.labelDesc)

        self.spacer_after_desc = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_sidebar.addItem(self.spacer_after_desc)

        self.frameFeatureRow1 = QFrame(self.frameSidebar)
        self.frameFeatureRow1.setObjectName(u"frameFeatureRow1")
        self.frameFeatureRow1.setFrameShape(QFrame.Shape.NoFrame)
        self.feature1_layout = QHBoxLayout(self.frameFeatureRow1)
        self.feature1_layout.setSpacing(12)
        self.feature1_layout.setObjectName(u"feature1_layout")
        self.feature1_layout.setContentsMargins(0, 0, 0, 0)
        self.labelFeatureIcon1 = QLabel(self.frameFeatureRow1)
        self.labelFeatureIcon1.setObjectName(u"labelFeatureIcon1")
        self.labelFeatureIcon1.setMinimumSize(QSize(32, 32))
        self.labelFeatureIcon1.setMaximumSize(QSize(32, 32))
        self.labelFeatureIcon1.setPixmap(QPixmap(u":/Icon/Icons/package_white.svg"))
        self.labelFeatureIcon1.setScaledContents(True)
        self.labelFeatureIcon1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.feature1_layout.addWidget(self.labelFeatureIcon1)

        self.labelFeatureText1 = QLabel(self.frameFeatureRow1)
        self.labelFeatureText1.setObjectName(u"labelFeatureText1")
        self.labelFeatureText1.setStyleSheet(u"color : white;")

        self.feature1_layout.addWidget(self.labelFeatureText1)

        self.spacer_f1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.feature1_layout.addItem(self.spacer_f1)


        self.verticalLayout_sidebar.addWidget(self.frameFeatureRow1)

        self.frameFeatureRow2 = QFrame(self.frameSidebar)
        self.frameFeatureRow2.setObjectName(u"frameFeatureRow2")
        self.frameFeatureRow2.setFrameShape(QFrame.Shape.NoFrame)
        self.feature2_layout = QHBoxLayout(self.frameFeatureRow2)
        self.feature2_layout.setSpacing(12)
        self.feature2_layout.setObjectName(u"feature2_layout")
        self.feature2_layout.setContentsMargins(0, 0, 0, 0)
        self.labelFeatureIcon2 = QLabel(self.frameFeatureRow2)
        self.labelFeatureIcon2.setObjectName(u"labelFeatureIcon2")
        self.labelFeatureIcon2.setMinimumSize(QSize(32, 32))
        self.labelFeatureIcon2.setMaximumSize(QSize(32, 32))
        self.labelFeatureIcon2.setPixmap(QPixmap(u":/Icon/Icons/archive_white.svg"))
        self.labelFeatureIcon2.setScaledContents(True)
        self.labelFeatureIcon2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.feature2_layout.addWidget(self.labelFeatureIcon2)

        self.labelFeatureText2 = QLabel(self.frameFeatureRow2)
        self.labelFeatureText2.setObjectName(u"labelFeatureText2")
        self.labelFeatureText2.setStyleSheet(u"color : white;")

        self.feature2_layout.addWidget(self.labelFeatureText2)

        self.spacer_f2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.feature2_layout.addItem(self.spacer_f2)


        self.verticalLayout_sidebar.addWidget(self.frameFeatureRow2)

        self.frameFeatureRow3 = QFrame(self.frameSidebar)
        self.frameFeatureRow3.setObjectName(u"frameFeatureRow3")
        self.frameFeatureRow3.setFrameShape(QFrame.Shape.NoFrame)
        self.feature3_layout = QHBoxLayout(self.frameFeatureRow3)
        self.feature3_layout.setSpacing(12)
        self.feature3_layout.setObjectName(u"feature3_layout")
        self.feature3_layout.setContentsMargins(0, 0, 0, 0)
        self.labelFeatureIcon3 = QLabel(self.frameFeatureRow3)
        self.labelFeatureIcon3.setObjectName(u"labelFeatureIcon3")
        self.labelFeatureIcon3.setMinimumSize(QSize(32, 32))
        self.labelFeatureIcon3.setMaximumSize(QSize(32, 32))
        self.labelFeatureIcon3.setPixmap(QPixmap(u":/Icon/Icons/shield-check_white.svg"))
        self.labelFeatureIcon3.setScaledContents(True)
        self.labelFeatureIcon3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.feature3_layout.addWidget(self.labelFeatureIcon3)

        self.labelFeatureText3 = QLabel(self.frameFeatureRow3)
        self.labelFeatureText3.setObjectName(u"labelFeatureText3")
        self.labelFeatureText3.setStyleSheet(u"color : white;")

        self.feature3_layout.addWidget(self.labelFeatureText3)

        self.spacer_f3 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.feature3_layout.addItem(self.spacer_f3)


        self.verticalLayout_sidebar.addWidget(self.frameFeatureRow3)

        self.verticalSpacer_sidebar = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_sidebar.addItem(self.verticalSpacer_sidebar)

        self.frameBadgeInfo = QFrame(self.frameSidebar)
        self.frameBadgeInfo.setObjectName(u"frameBadgeInfo")
        self.badge_layout = QHBoxLayout(self.frameBadgeInfo)
        self.badge_layout.setSpacing(12)
        self.badge_layout.setObjectName(u"badge_layout")
        self.badge_layout.setContentsMargins(16, 14, 16, 14)
        self.labelBadgeIcon = QLabel(self.frameBadgeInfo)
        self.labelBadgeIcon.setObjectName(u"labelBadgeIcon")
        self.labelBadgeIcon.setMinimumSize(QSize(32, 32))
        self.labelBadgeIcon.setMaximumSize(QSize(32, 32))
        self.labelBadgeIcon.setPixmap(QPixmap(u":/Icon/Icons/zap_white.svg"))
        self.labelBadgeIcon.setScaledContents(True)
        self.labelBadgeIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.badge_layout.addWidget(self.labelBadgeIcon)

        self.badge_text_layout = QVBoxLayout()
        self.badge_text_layout.setSpacing(2)
        self.badge_text_layout.setObjectName(u"badge_text_layout")
        self.labelBadgeTitle = QLabel(self.frameBadgeInfo)
        self.labelBadgeTitle.setObjectName(u"labelBadgeTitle")

        self.badge_text_layout.addWidget(self.labelBadgeTitle)


        self.badge_layout.addLayout(self.badge_text_layout)


        self.verticalLayout_sidebar.addWidget(self.frameBadgeInfo)

        self.labelVersion = QLabel(self.frameSidebar)
        self.labelVersion.setObjectName(u"labelVersion")

        self.verticalLayout_sidebar.addWidget(self.labelVersion)


        self.horizontalLayout_root.addWidget(self.frameSidebar)

        self.frameFormContainer = QFrame(LoginDialog)
        self.frameFormContainer.setObjectName(u"frameFormContainer")
        self.frameFormContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_mainForm = QVBoxLayout(self.frameFormContainer)
        self.verticalLayout_mainForm.setSpacing(0)
        self.verticalLayout_mainForm.setObjectName(u"verticalLayout_mainForm")
        self.verticalLayout_mainForm.setContentsMargins(40, 40, 40, 0)
        self.frameFormFields = QFrame(self.frameFormContainer)
        self.frameFormFields.setObjectName(u"frameFormFields")
        self.frameFormFields.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout_innerForm = QVBoxLayout(self.frameFormFields)
        self.verticalLayout_innerForm.setSpacing(16)
        self.verticalLayout_innerForm.setObjectName(u"verticalLayout_innerForm")
        self.verticalLayout_innerForm.setContentsMargins(56, 44, 56, 36)
        self.labelHeader = QLabel(self.frameFormFields)
        self.labelHeader.setObjectName(u"labelHeader")

        self.verticalLayout_innerForm.addWidget(self.labelHeader)

        self.labelSubheader = QLabel(self.frameFormFields)
        self.labelSubheader.setObjectName(u"labelSubheader")

        self.verticalLayout_innerForm.addWidget(self.labelSubheader)

        self.spacer_header = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_innerForm.addItem(self.spacer_header)

        self.layoutUserField = QVBoxLayout()
        self.layoutUserField.setSpacing(8)
        self.layoutUserField.setObjectName(u"layoutUserField")
        self.labelUser = QLabel(self.frameFormFields)
        self.labelUser.setObjectName(u"labelUser")

        self.layoutUserField.addWidget(self.labelUser)

        self.frameUsernameField = QFrame(self.frameFormFields)
        self.frameUsernameField.setObjectName(u"frameUsernameField")
        self.frameUsernameField.setMinimumSize(QSize(0, 50))
        self.frameUsernameField.setMaximumSize(QSize(16777215, 50))
        self.username_field_layout = QHBoxLayout(self.frameUsernameField)
        self.username_field_layout.setSpacing(10)
        self.username_field_layout.setObjectName(u"username_field_layout")
        self.username_field_layout.setContentsMargins(14, 0, 14, 0)
        self.icon_username = QLabel(self.frameUsernameField)
        self.icon_username.setObjectName(u"icon_username")
        self.icon_username.setMinimumSize(QSize(18, 18))
        self.icon_username.setMaximumSize(QSize(18, 18))
        self.icon_username.setPixmap(QPixmap(u":/Icon/Icons/mail.svg"))
        self.icon_username.setScaledContents(True)

        self.username_field_layout.addWidget(self.icon_username)

        self.lineEdit_username = QLineEdit(self.frameUsernameField)
        self.lineEdit_username.setObjectName(u"lineEdit_username")
        self.lineEdit_username.setMinimumSize(QSize(0, 48))

        self.username_field_layout.addWidget(self.lineEdit_username)


        self.layoutUserField.addWidget(self.frameUsernameField)


        self.verticalLayout_innerForm.addLayout(self.layoutUserField)

        self.layoutPassField = QVBoxLayout()
        self.layoutPassField.setSpacing(8)
        self.layoutPassField.setObjectName(u"layoutPassField")
        self.horizontalLayout_passHeader = QHBoxLayout()
        self.horizontalLayout_passHeader.setSpacing(8)
        self.horizontalLayout_passHeader.setObjectName(u"horizontalLayout_passHeader")
        self.labelPassword = QLabel(self.frameFormFields)
        self.labelPassword.setObjectName(u"labelPassword")

        self.horizontalLayout_passHeader.addWidget(self.labelPassword)

        self.horizontalSpacer_pass = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_passHeader.addItem(self.horizontalSpacer_pass)

        self.labelForgot = QLabel(self.frameFormFields)
        self.labelForgot.setObjectName(u"labelForgot")
        self.labelForgot.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_passHeader.addWidget(self.labelForgot)


        self.layoutPassField.addLayout(self.horizontalLayout_passHeader)

        self.framePasswordField = QFrame(self.frameFormFields)
        self.framePasswordField.setObjectName(u"framePasswordField")
        self.framePasswordField.setMinimumSize(QSize(0, 50))
        self.framePasswordField.setMaximumSize(QSize(16777215, 50))
        self.password_field_layout = QHBoxLayout(self.framePasswordField)
        self.password_field_layout.setSpacing(10)
        self.password_field_layout.setObjectName(u"password_field_layout")
        self.password_field_layout.setContentsMargins(14, 0, 8, 0)
        self.icon_password = QLabel(self.framePasswordField)
        self.icon_password.setObjectName(u"icon_password")
        self.icon_password.setMinimumSize(QSize(18, 18))
        self.icon_password.setMaximumSize(QSize(18, 18))
        self.icon_password.setPixmap(QPixmap(u":/Icon/Icons/lock.svg"))
        self.icon_password.setScaledContents(True)

        self.password_field_layout.addWidget(self.icon_password)

        self.lineEdit_password = QLineEdit(self.framePasswordField)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setMinimumSize(QSize(0, 48))
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.password_field_layout.addWidget(self.lineEdit_password)

        self.btn_toggle_pwd = QToolButton(self.framePasswordField)
        self.btn_toggle_pwd.setObjectName(u"btn_toggle_pwd")
        self.btn_toggle_pwd.setMinimumSize(QSize(32, 32))
        self.btn_toggle_pwd.setMaximumSize(QSize(32, 32))
        self.btn_toggle_pwd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/eye.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_toggle_pwd.setIcon(icon)
        self.btn_toggle_pwd.setIconSize(QSize(18, 18))

        self.password_field_layout.addWidget(self.btn_toggle_pwd)


        self.layoutPassField.addWidget(self.framePasswordField)


        self.verticalLayout_innerForm.addLayout(self.layoutPassField)

        self.horizontalLayout_options = QHBoxLayout()
        self.horizontalLayout_options.setSpacing(8)
        self.horizontalLayout_options.setObjectName(u"horizontalLayout_options")
        self.checkBox_remember = QCheckBox(self.frameFormFields)
        self.checkBox_remember.setObjectName(u"checkBox_remember")
        self.checkBox_remember.setChecked(True)

        self.horizontalLayout_options.addWidget(self.checkBox_remember)

        self.horizontalSpacer_options = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_options.addItem(self.horizontalSpacer_options)


        self.verticalLayout_innerForm.addLayout(self.horizontalLayout_options)

        self.frameError = QFrame(self.frameFormFields)
        self.frameError.setObjectName(u"frameError")
        self.frameError.setVisible(False)
        self.error_layout = QHBoxLayout(self.frameError)
        self.error_layout.setSpacing(10)
        self.error_layout.setObjectName(u"error_layout")
        self.error_layout.setContentsMargins(12, 10, 12, 10)
        self.iconError = QLabel(self.frameError)
        self.iconError.setObjectName(u"iconError")
        self.iconError.setMinimumSize(QSize(18, 18))
        self.iconError.setMaximumSize(QSize(18, 18))
        self.iconError.setPixmap(QPixmap(u":/Icon/Icons/alert-circle.svg"))
        self.iconError.setScaledContents(True)

        self.error_layout.addWidget(self.iconError)

        self.labelErrorText = QLabel(self.frameError)
        self.labelErrorText.setObjectName(u"labelErrorText")
        self.labelErrorText.setWordWrap(True)

        self.error_layout.addWidget(self.labelErrorText)


        self.verticalLayout_innerForm.addWidget(self.frameError)

        self.spacer_before_button = QSpacerItem(20, 4, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_innerForm.addItem(self.spacer_before_button)

        self.pushButton_login = QPushButton(self.frameFormFields)
        self.pushButton_login.setObjectName(u"pushButton_login")
        self.pushButton_login.setMinimumSize(QSize(0, 52))
        self.pushButton_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/log-in_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_login.setIcon(icon1)
        self.pushButton_login.setIconSize(QSize(18, 18))

        self.verticalLayout_innerForm.addWidget(self.pushButton_login)

        self.frameDivider = QFrame(self.frameFormFields)
        self.frameDivider.setObjectName(u"frameDivider")
        self.frameDivider.setMinimumSize(QSize(0, 1))
        self.frameDivider.setMaximumSize(QSize(16777215, 1))
        self.frameDivider.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_innerForm.addWidget(self.frameDivider)

        self.labelHelp = QLabel(self.frameFormFields)
        self.labelHelp.setObjectName(u"labelHelp")
        self.labelHelp.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.labelHelp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_innerForm.addWidget(self.labelHelp)

        self.verticalSpacer_formBottom = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_innerForm.addItem(self.verticalSpacer_formBottom)


        self.verticalLayout_mainForm.addWidget(self.frameFormFields)

        self.frameLegal = QFrame(self.frameFormContainer)
        self.frameLegal.setObjectName(u"frameLegal")
        self.frameLegal.setMinimumSize(QSize(0, 72))
        self.frameLegal.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_legal = QHBoxLayout(self.frameLegal)
        self.horizontalLayout_legal.setSpacing(12)
        self.horizontalLayout_legal.setObjectName(u"horizontalLayout_legal")
        self.horizontalLayout_legal.setContentsMargins(40, 14, 40, 14)
        self.labelLegalIcon = QLabel(self.frameLegal)
        self.labelLegalIcon.setObjectName(u"labelLegalIcon")
        self.labelLegalIcon.setMinimumSize(QSize(16, 16))
        self.labelLegalIcon.setMaximumSize(QSize(16, 16))
        self.labelLegalIcon.setPixmap(QPixmap(u":/Icon/Icons/shield.svg"))
        self.labelLegalIcon.setScaledContents(True)

        self.horizontalLayout_legal.addWidget(self.labelLegalIcon)

        self.labelLegalText = QLabel(self.frameLegal)
        self.labelLegalText.setObjectName(u"labelLegalText")
        self.labelLegalText.setWordWrap(True)

        self.horizontalLayout_legal.addWidget(self.labelLegalText)


        self.verticalLayout_mainForm.addWidget(self.frameLegal)


        self.horizontalLayout_root.addWidget(self.frameFormContainer)


        self.retranslateUi(LoginDialog)

        QMetaObject.connectSlotsByName(LoginDialog)
    # setupUi

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QCoreApplication.translate("LoginDialog", u"Nova Pharma \u2014 Portail de Connexion", None))
        self.labelIconContainer.setText("")
        self.labelTitle.setText(QCoreApplication.translate("LoginDialog", u"Nova Pharma", None))
        self.labelDesc.setText(QCoreApplication.translate("LoginDialog", u"Bienvenue dans votre centre de commande intelligent. G\u00e9rez vos inventaires et assurez la conformit\u00e9 en quelques clics.", None))
        self.labelFeatureText1.setText(QCoreApplication.translate("LoginDialog", u"Gestion des stocks en temps r\u00e9el", None))
        self.labelFeatureText2.setText(QCoreApplication.translate("LoginDialog", u"Tra\u00e7abilit\u00e9 compl\u00e8te des lots", None))
        self.labelFeatureText3.setText(QCoreApplication.translate("LoginDialog", u"Protection des donn\u00e9es", None))
        self.labelBadgeTitle.setText(QCoreApplication.translate("LoginDialog", u"Nouveaut\u00e9s v2.0", None))
        self.labelVersion.setText(QCoreApplication.translate("LoginDialog", u"\u00a9 2025 Team Nova", None))
        self.labelHeader.setText(QCoreApplication.translate("LoginDialog", u"Connexion s\u00e9curis\u00e9e", None))
        self.labelSubheader.setText(QCoreApplication.translate("LoginDialog", u"Identifiez-vous pour acc\u00e9der au panel administratif.", None))
        self.labelUser.setText(QCoreApplication.translate("LoginDialog", u"IDENTIFIANT OU EMAIL", None))
        self.lineEdit_username.setPlaceholderText(QCoreApplication.translate("LoginDialog", u"exemple@gmail.com", None))
        self.labelPassword.setText(QCoreApplication.translate("LoginDialog", u"MOT DE PASSE", None))
        self.labelForgot.setText(QCoreApplication.translate("LoginDialog", u"Mot de passe oubli\u00e9 ?", None))
        self.lineEdit_password.setPlaceholderText(QCoreApplication.translate("LoginDialog", u"Votre mot de passe", None))
#if QT_CONFIG(tooltip)
        self.btn_toggle_pwd.setToolTip(QCoreApplication.translate("LoginDialog", u"Afficher / masquer le mot de passe", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_remember.setText(QCoreApplication.translate("LoginDialog", u"Rester connect\u00e9 pendant 30 jours", None))
        self.labelErrorText.setText("")
        self.pushButton_login.setText(QCoreApplication.translate("LoginDialog", u"  Se connecter au portail", None))
        self.labelHelp.setText(QCoreApplication.translate("LoginDialog", u"Difficult\u00e9s de connexion ? <a href=\"#support\" style=\"color: #2563eb; font-weight: 600;\">Contacter le support IT</a>", None))
        self.labelLegalText.setText(QCoreApplication.translate("LoginDialog", u"En vous connectant, vous acceptez nos conditions g\u00e9n\u00e9rales d'utilisation et notre politique de protection des donn\u00e9es de sant\u00e9.", None))
    # retranslateUi

