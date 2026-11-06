# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_sauvegardeGlFRVO.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_Setting_save(object):
    def setupUi(self, Setting_save):
        if not Setting_save.objectName():
            Setting_save.setObjectName(u"Setting_save")
        Setting_save.resize(578, 587)
        Setting_save.setMinimumSize(QSize(560, 440))
        Setting_save.setStyleSheet(u"QDialog#Setting_save { background: #f0f4f8; }\n"
"QDialog#Setting_save QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(Setting_save)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(Setting_save)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 88))
        self.header.setMaximumSize(QSize(16777215, 88))
        self.header.setStyleSheet(u"QFrame#header { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #023E8A, stop:1 #0077B6); border: none; }\n"
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
        icon.addFile(u":/Icon/Icons/save_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        self.lbl_header_sub.setStyleSheet(u"font-size: 11px; color: rgba(255,255,255,0.75); background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_header_sub)


        self.headerLayout.addLayout(self.headerTitleBox)


        self.mainLayout.addWidget(self.header)

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.setSpacing(14)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(28, 24, 28, 20)
        self.lbl_info = QLabel(Setting_save)
        self.lbl_info.setObjectName(u"lbl_info")
        self.lbl_info.setStyleSheet(u"color: #023E8A; font-size: 12px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 10px; padding: 12px 14px;")
        self.lbl_info.setWordWrap(True)

        self.bodyLayout.addWidget(self.lbl_info)

        self.lbl_dossier = QLabel(Setting_save)
        self.lbl_dossier.setObjectName(u"lbl_dossier")
        self.lbl_dossier.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700;")

        self.bodyLayout.addWidget(self.lbl_dossier)

        self.folderRow = QHBoxLayout()
        self.folderRow.setSpacing(10)
        self.folderRow.setObjectName(u"folderRow")
        self.edit_dossier = QLineEdit(Setting_save)
        self.edit_dossier.setObjectName(u"edit_dossier")
        self.edit_dossier.setMinimumSize(QSize(0, 42))
        self.edit_dossier.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #dbe3ec; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.folderRow.addWidget(self.edit_dossier)

        self.btn_browse = QPushButton(Setting_save)
        self.btn_browse.setObjectName(u"btn_browse")
        self.btn_browse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_browse.setStyleSheet(u"QPushButton { background: #eff6ff; color: #023E8A; border: 1.5px solid #bfdbfe; border-radius: 10px; padding: 10px 20px; font-size: 12px; font-weight: 700; min-height: 42px; }\n"
"QPushButton:hover { background: #dbeafe; border-color: #93c5fd; }")

        self.folderRow.addWidget(self.btn_browse)


        self.bodyLayout.addLayout(self.folderRow)

        self.lbl_pwd = QLabel(Setting_save)
        self.lbl_pwd.setObjectName(u"lbl_pwd")
        self.lbl_pwd.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700;")

        self.bodyLayout.addWidget(self.lbl_pwd)

        self.pwdRow = QHBoxLayout()
        self.pwdRow.setSpacing(8)
        self.pwdRow.setObjectName(u"pwdRow")
        self.edit_pwd = QLineEdit(Setting_save)
        self.edit_pwd.setObjectName(u"edit_pwd")
        self.edit_pwd.setMinimumSize(QSize(0, 42))
        self.edit_pwd.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #dbe3ec; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")
        self.edit_pwd.setEchoMode(QLineEdit.EchoMode.Password)

        self.pwdRow.addWidget(self.edit_pwd)

        self.btn_toggle_pwd = QPushButton(Setting_save)
        self.btn_toggle_pwd.setObjectName(u"btn_toggle_pwd")
        self.btn_toggle_pwd.setMinimumSize(QSize(44, 44))
        self.btn_toggle_pwd.setMaximumSize(QSize(44, 44))
        self.btn_toggle_pwd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_toggle_pwd.setStyleSheet(u"QPushButton { background: #f1f5f9; border: 1.5px solid #e2e8f0; border-radius: 10px; }\n"
"QPushButton:hover { background: #e2e8f0; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/eye.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_toggle_pwd.setIcon(icon1)
        self.btn_toggle_pwd.setIconSize(QSize(18, 18))

        self.pwdRow.addWidget(self.btn_toggle_pwd)


        self.bodyLayout.addLayout(self.pwdRow)

        self.lbl_nom = QLabel(Setting_save)
        self.lbl_nom.setObjectName(u"lbl_nom")
        self.lbl_nom.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700;")

        self.bodyLayout.addWidget(self.lbl_nom)

        self.edit_nom = QLineEdit(Setting_save)
        self.edit_nom.setObjectName(u"edit_nom")
        self.edit_nom.setMinimumSize(QSize(0, 42))
        self.edit_nom.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #dbe3ec; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.bodyLayout.addWidget(self.edit_nom)

        self.progress = QProgressBar(Setting_save)
        self.progress.setObjectName(u"progress")
        self.progress.setMinimumSize(QSize(0, 8))
        self.progress.setMaximumSize(QSize(16777215, 8))
        self.progress.setVisible(False)
        self.progress.setStyleSheet(u"QProgressBar { background: #e2e8f0; border: none; border-radius: 4px; }\n"
"QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0077B6, stop:1 #00B4D8); border-radius: 4px; }")
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        self.bodyLayout.addWidget(self.progress)

        self.lbl_error = QLabel(Setting_save)
        self.lbl_error.setObjectName(u"lbl_error")
        self.lbl_error.setVisible(False)
        self.lbl_error.setStyleSheet(u"color: #DC2626; font-size: 11px; font-weight: 600; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 8px 12px;")
        self.lbl_error.setWordWrap(True)

        self.bodyLayout.addWidget(self.lbl_error)

        self.bodySpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.bodyLayout.addItem(self.bodySpacer)


        self.mainLayout.addLayout(self.bodyLayout)

        self.footer = QFrame(Setting_save)
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

        self.btn_cancel = QPushButton(self.footer)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setMinimumSize(QSize(0, 42))
        self.btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cancel.setStyleSheet(u"QPushButton { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 20px; }\n"
"QPushButton:hover { background: #e2e8f0; }")

        self.footerLayout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton(self.footer)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setEnabled(False)
        self.btn_save.setMinimumSize(QSize(0, 42))
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 24px; }\n"
"QPushButton:hover { background: #0077B6; }\n"
"QPushButton:disabled { background: #94a3b8; }")

        self.footerLayout.addWidget(self.btn_save)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(Setting_save)

        QMetaObject.connectSlotsByName(Setting_save)
    # setupUi

    def retranslateUi(self, Setting_save):
        Setting_save.setWindowTitle(QCoreApplication.translate("Setting_save", u"Sauvegarde \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("Setting_save", u"Sauvegarde de la base", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("Setting_save", u"Cr\u00e9e une archive ZIP prot\u00e9g\u00e9e par mot de passe", None))
        self.lbl_info.setText(QCoreApplication.translate("Setting_save", u"L'archive contiendra la base de donn\u00e9es compl\u00e8te (produits, clients, ventes, utilisateurs, configuration).", None))
        self.lbl_dossier.setText(QCoreApplication.translate("Setting_save", u"DOSSIER DE DESTINATION", None))
        self.edit_dossier.setPlaceholderText(QCoreApplication.translate("Setting_save", u"Aucun dossier s\u00e9lectionn\u00e9", None))
        self.btn_browse.setText(QCoreApplication.translate("Setting_save", u"Parcourir\u2026", None))
        self.lbl_pwd.setText(QCoreApplication.translate("Setting_save", u"MOT DE PASSE DE L'ARCHIVE", None))
        self.edit_pwd.setPlaceholderText(QCoreApplication.translate("Setting_save", u"Mot de passe pour prot\u00e9ger l'archive", None))
        self.btn_toggle_pwd.setText("")
        self.lbl_nom.setText(QCoreApplication.translate("Setting_save", u"NOM DU FICHIER", None))
        self.edit_nom.setPlaceholderText(QCoreApplication.translate("Setting_save", u"NovaPharma_backup_YYYYMMDD_HHMM.zip", None))
        self.lbl_error.setText("")
        self.btn_cancel.setText(QCoreApplication.translate("Setting_save", u"Annuler", None))
        self.btn_save.setText(QCoreApplication.translate("Setting_save", u"Lancer la sauvegarde", None))
    # retranslateUi

