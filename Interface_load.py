# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_loaddpvZGb.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(560, 559)
        Dialog.setMinimumSize(QSize(560, 500))
        Dialog.setStyleSheet(u"QDialog#Dialog { background: #f0f4f8; }\n"
"QDialog#Dialog QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(Dialog)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(Dialog)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 88))
        self.header.setMaximumSize(QSize(16777215, 88))
        self.header.setStyleSheet(u"QFrame#header { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #b45309, stop:1 #ea580c); border: none; }\n"
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
        icon.addFile(u":/Icon/Icons/upload_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        self.lbl_header_sub.setStyleSheet(u"font-size: 11px; color: rgba(255,255,255,0.85); background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_header_sub)


        self.headerLayout.addLayout(self.headerTitleBox)


        self.mainLayout.addWidget(self.header)

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.setSpacing(14)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(28, 24, 28, 20)
        self.lbl_warning = QLabel(Dialog)
        self.lbl_warning.setObjectName(u"lbl_warning")
        self.lbl_warning.setStyleSheet(u"color: #991b1b; font-size: 11px; font-weight: 600; background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; padding: 12px 14px;")
        self.lbl_warning.setWordWrap(True)

        self.bodyLayout.addWidget(self.lbl_warning)

        self.lbl_archive = QLabel(Dialog)
        self.lbl_archive.setObjectName(u"lbl_archive")
        self.lbl_archive.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700;")

        self.bodyLayout.addWidget(self.lbl_archive)

        self.archiveRow = QHBoxLayout()
        self.archiveRow.setSpacing(10)
        self.archiveRow.setObjectName(u"archiveRow")
        self.edit_archive = QLineEdit(Dialog)
        self.edit_archive.setObjectName(u"edit_archive")
        self.edit_archive.setMinimumSize(QSize(0, 42))
        self.edit_archive.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #dbe3ec; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:read-only { background: #f8fafc; color: #475569; }")
        self.edit_archive.setReadOnly(True)

        self.archiveRow.addWidget(self.edit_archive)

        self.btn_browse = QPushButton(Dialog)
        self.btn_browse.setObjectName(u"btn_browse")
        self.btn_browse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_browse.setStyleSheet(u"QPushButton { background: #eff6ff; color: #023E8A; border: 1.5px solid #bfdbfe; border-radius: 10px; padding: 10px 20px; font-size: 12px; font-weight: 700; min-height: 42px; }\n"
"QPushButton:hover { background: #dbeafe; border-color: #93c5fd; }")

        self.archiveRow.addWidget(self.btn_browse)


        self.bodyLayout.addLayout(self.archiveRow)

        self.lbl_pwd = QLabel(Dialog)
        self.lbl_pwd.setObjectName(u"lbl_pwd")
        self.lbl_pwd.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700;")

        self.bodyLayout.addWidget(self.lbl_pwd)

        self.pwdRow = QHBoxLayout()
        self.pwdRow.setSpacing(8)
        self.pwdRow.setObjectName(u"pwdRow")
        self.edit_pwd = QLineEdit(Dialog)
        self.edit_pwd.setObjectName(u"edit_pwd")
        self.edit_pwd.setMinimumSize(QSize(0, 42))
        self.edit_pwd.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #dbe3ec; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")
        self.edit_pwd.setEchoMode(QLineEdit.EchoMode.Password)

        self.pwdRow.addWidget(self.edit_pwd)

        self.btn_toggle_pwd = QPushButton(Dialog)
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

        self.lbl_pwd_info = QLabel(Dialog)
        self.lbl_pwd_info.setObjectName(u"lbl_pwd_info")
        self.lbl_pwd_info.setStyleSheet(u"color: #023E8A; font-size: 11px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 10px 14px;")
        self.lbl_pwd_info.setWordWrap(True)

        self.bodyLayout.addWidget(self.lbl_pwd_info)

        self.progress = QProgressBar(Dialog)
        self.progress.setObjectName(u"progress")
        self.progress.setMinimumSize(QSize(0, 8))
        self.progress.setMaximumSize(QSize(16777215, 8))
        self.progress.setVisible(False)
        self.progress.setStyleSheet(u"QProgressBar { background: #e2e8f0; border: none; border-radius: 4px; }\n"
"QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ea580c, stop:1 #f97316); border-radius: 4px; }")
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        self.bodyLayout.addWidget(self.progress)

        self.lbl_error = QLabel(Dialog)
        self.lbl_error.setObjectName(u"lbl_error")
        self.lbl_error.setVisible(False)
        self.lbl_error.setStyleSheet(u"color: #DC2626; font-size: 11px; font-weight: 600; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 8px 12px;")
        self.lbl_error.setWordWrap(True)

        self.bodyLayout.addWidget(self.lbl_error)

        self.bodySpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.bodyLayout.addItem(self.bodySpacer)


        self.mainLayout.addLayout(self.bodyLayout)

        self.footer = QFrame(Dialog)
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

        self.btn_restore = QPushButton(self.footer)
        self.btn_restore.setObjectName(u"btn_restore")
        self.btn_restore.setEnabled(False)
        self.btn_restore.setMinimumSize(QSize(0, 42))
        self.btn_restore.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_restore.setStyleSheet(u"QPushButton { background: #dc2626; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 24px; }\n"
"QPushButton:hover { background: #b91c1c; }\n"
"QPushButton:disabled { background: #94a3b8; }")

        self.footerLayout.addWidget(self.btn_restore)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Restaurer une sauvegarde \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("Dialog", u"Restaurer une sauvegarde", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("Dialog", u"Remplacer la base actuelle par une archive", None))
        self.lbl_warning.setText(QCoreApplication.translate("Dialog", u"\u26a0 Cette op\u00e9ration remplace TOUTES les donn\u00e9es actuelles (produits, clients, ventes, etc.) par celles de l'archive. Une sauvegarde automatique de s\u00e9curit\u00e9 sera cr\u00e9\u00e9e avant l'op\u00e9ration.", None))
        self.lbl_archive.setText(QCoreApplication.translate("Dialog", u"ARCHIVE \u00c0 RESTAURER", None))
        self.edit_archive.setPlaceholderText(QCoreApplication.translate("Dialog", u"Aucune archive s\u00e9lectionn\u00e9e", None))
        self.btn_browse.setText(QCoreApplication.translate("Dialog", u"Parcourir\u2026", None))
        self.lbl_pwd.setText(QCoreApplication.translate("Dialog", u"MOT DE PASSE DE L'ARCHIVE", None))
        self.edit_pwd.setPlaceholderText(QCoreApplication.translate("Dialog", u"Mot de passe de l'archive", None))
        self.btn_toggle_pwd.setText("")
        self.lbl_pwd_info.setText(QCoreApplication.translate("Dialog", u"Le mot de passe des archives est d\u00e9riv\u00e9 de cette machine. Pour une archive cr\u00e9\u00e9e sur un autre PC, contactez le support.", None))
        self.lbl_error.setText("")
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"Annuler", None))
        self.btn_restore.setText(QCoreApplication.translate("Dialog", u"Restaurer", None))
    # retranslateUi

