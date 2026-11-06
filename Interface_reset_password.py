# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_reset_passwordrzIRmB.ui'
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(520, 651)
        Dialog.setStyleSheet(u"QDialog#Dialog { background: #f0f4f8; }\n"
"QDialog#Dialog QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(Dialog)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 24, 24, 24)
        self.lbl_title = QLabel(Dialog)
        self.lbl_title.setObjectName(u"lbl_title")
        self.lbl_title.setStyleSheet(u"color: #023E8A; font-size: 18px; font-weight: 800; background: transparent;")

        self.mainLayout.addWidget(self.lbl_title)

        self.lbl_subtitle = QLabel(Dialog)
        self.lbl_subtitle.setObjectName(u"lbl_subtitle")
        self.lbl_subtitle.setStyleSheet(u"color: #64748b; font-size: 12px; background: transparent;")
        self.lbl_subtitle.setWordWrap(True)

        self.mainLayout.addWidget(self.lbl_subtitle)

        self.pwd_box = QFrame(Dialog)
        self.pwd_box.setObjectName(u"pwd_box")
        self.pwd_box.setStyleSheet(u"QFrame#pwd_box { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }")
        self.pwdBoxLayout = QVBoxLayout(self.pwd_box)
        self.pwdBoxLayout.setSpacing(12)
        self.pwdBoxLayout.setObjectName(u"pwdBoxLayout")
        self.pwdBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.lbl_pwd = QLabel(self.pwd_box)
        self.lbl_pwd.setObjectName(u"lbl_pwd")
        self.lbl_pwd.setStyleSheet(u"font-size: 22px; font-weight: 800; color: #023E8A; font-family: 'Courier New'; background: #f0f9ff; border: 2px dashed #bae6fd; border-radius: 10px; padding: 18px; letter-spacing: 2px;")
        self.lbl_pwd.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pwdBoxLayout.addWidget(self.lbl_pwd)

        self.btn_copy = QPushButton(self.pwd_box)
        self.btn_copy.setObjectName(u"btn_copy")
        self.btn_copy.setMinimumSize(QSize(0, 40))
        self.btn_copy.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_copy.setStyleSheet(u"QPushButton { background: #eff6ff; color: #023E8A; border: 1px solid #bfdbfe; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 16px; }\n"
"QPushButton:hover { background: #dbeafe; }")
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/copy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_copy.setIcon(icon)
        self.btn_copy.setIconSize(QSize(16, 16))

        self.pwdBoxLayout.addWidget(self.btn_copy)


        self.mainLayout.addWidget(self.pwd_box)

        self.lbl_qr_title = QLabel(Dialog)
        self.lbl_qr_title.setObjectName(u"lbl_qr_title")
        self.lbl_qr_title.setStyleSheet(u"color: #475569; font-size: 12px; font-weight: 700; background: transparent;")

        self.mainLayout.addWidget(self.lbl_qr_title)

        self.lbl_qrcode = QLabel(Dialog)
        self.lbl_qrcode.setObjectName(u"lbl_qrcode")
        self.lbl_qrcode.setMinimumSize(QSize(0, 200))
        self.lbl_qrcode.setStyleSheet(u"background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; color: #94a3b8;")
        self.lbl_qrcode.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mainLayout.addWidget(self.lbl_qrcode)

        self.lbl_warning = QLabel(Dialog)
        self.lbl_warning.setObjectName(u"lbl_warning")
        self.lbl_warning.setStyleSheet(u"color: #b45309; font-size: 11px; font-weight: 600; background: #fef3c7; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 12px;")
        self.lbl_warning.setWordWrap(True)

        self.mainLayout.addWidget(self.lbl_warning)

        self.spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mainLayout.addItem(self.spacer)

        self.footerRow = QHBoxLayout()
        self.footerRow.setObjectName(u"footerRow")
        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerRow.addItem(self.footerSpacer)

        self.btn_close = QPushButton(Dialog)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMinimumSize(QSize(0, 42))
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 24px; }\n"
"QPushButton:hover { background: #0077B6; }")

        self.footerRow.addWidget(self.btn_close)


        self.mainLayout.addLayout(self.footerRow)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"R\u00e9initialiser mot de passe", None))
        self.lbl_title.setText(QCoreApplication.translate("Dialog", u"R\u00e9initialiser le mot de passe", None))
        self.lbl_subtitle.setText(QCoreApplication.translate("Dialog", u"Un nouveau mot de passe temporaire sera g\u00e9n\u00e9r\u00e9. L'utilisateur devra le changer \u00e0 sa prochaine connexion.", None))
        self.lbl_pwd.setText(QCoreApplication.translate("Dialog", u"NOVA-2026-A4F2", None))
        self.btn_copy.setText(QCoreApplication.translate("Dialog", u"Copier dans le presse-papier", None))
        self.lbl_qr_title.setText(QCoreApplication.translate("Dialog", u"QR code (optionnel)", None))
        self.lbl_qrcode.setText(QCoreApplication.translate("Dialog", u"G\u00e9n\u00e9ration\u2026", None))
        self.lbl_warning.setText(QCoreApplication.translate("Dialog", u"Le mot de passe ne sera plus jamais affich\u00e9 apr\u00e8s fermeture de cette fen\u00eatre. Notez-le maintenant.", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
    # retranslateUi

