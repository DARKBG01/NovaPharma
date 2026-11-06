# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_audit_detailsYrGqD.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPlainTextEdit, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(720, 754)
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
        icon.addFile(u":/Icon/Icons/history_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)


        self.mainLayout.addWidget(self.header)

        self.bodyScroll = QScrollArea(Dialog)
        self.bodyScroll.setObjectName(u"bodyScroll")
        self.bodyScroll.setStyleSheet(u"QScrollArea { background: #f0f4f8; border: none; }")
        self.bodyScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.bodyScroll.setWidgetResizable(True)
        self.bodyContent = QWidget()
        self.bodyContent.setObjectName(u"bodyContent")
        self.bodyContent.setGeometry(QRect(0, 0, 720, 594))
        self.bodyContent.setStyleSheet(u"QWidget#bodyContent { background: #f0f4f8; }")
        self.bodyLayout = QVBoxLayout(self.bodyContent)
        self.bodyLayout.setSpacing(12)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(24, 20, 24, 20)
        self.info_card = QFrame(self.bodyContent)
        self.info_card.setObjectName(u"info_card")
        self.info_card.setStyleSheet(u"QFrame#info_card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }\n"
"QFrame#info_card QLabel { background: transparent; }")
        self.infoGrid = QGridLayout(self.info_card)
        self.infoGrid.setObjectName(u"infoGrid")
        self.infoGrid.setHorizontalSpacing(24)
        self.infoGrid.setVerticalSpacing(14)
        self.infoGrid.setContentsMargins(20, 20, 20, 20)
        self.lbl_k_action = QLabel(self.info_card)
        self.lbl_k_action.setObjectName(u"lbl_k_action")
        self.lbl_k_action.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_action, 0, 0, 1, 1)

        self.val_action = QLabel(self.info_card)
        self.val_action.setObjectName(u"val_action")
        self.val_action.setStyleSheet(u"color: #023E8A; font-size: 13px; font-weight: 800;")

        self.infoGrid.addWidget(self.val_action, 0, 1, 1, 1)

        self.lbl_k_user = QLabel(self.info_card)
        self.lbl_k_user.setObjectName(u"lbl_k_user")
        self.lbl_k_user.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_user, 1, 0, 1, 1)

        self.val_user = QLabel(self.info_card)
        self.val_user.setObjectName(u"val_user")
        self.val_user.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_user, 1, 1, 1, 1)

        self.lbl_k_date = QLabel(self.info_card)
        self.lbl_k_date.setObjectName(u"lbl_k_date")
        self.lbl_k_date.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_date, 2, 0, 1, 1)

        self.val_date = QLabel(self.info_card)
        self.val_date.setObjectName(u"val_date")
        self.val_date.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_date, 2, 1, 1, 1)

        self.lbl_k_cible = QLabel(self.info_card)
        self.lbl_k_cible.setObjectName(u"lbl_k_cible")
        self.lbl_k_cible.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_cible, 3, 0, 1, 1)

        self.val_cible = QLabel(self.info_card)
        self.val_cible.setObjectName(u"val_cible")
        self.val_cible.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_cible, 3, 1, 1, 1)

        self.lbl_k_machine = QLabel(self.info_card)
        self.lbl_k_machine.setObjectName(u"lbl_k_machine")
        self.lbl_k_machine.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_machine, 4, 0, 1, 1)

        self.val_machine = QLabel(self.info_card)
        self.val_machine.setObjectName(u"val_machine")
        self.val_machine.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_machine, 4, 1, 1, 1)

        self.lbl_k_id = QLabel(self.info_card)
        self.lbl_k_id.setObjectName(u"lbl_k_id")
        self.lbl_k_id.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_id, 5, 0, 1, 1)

        self.val_id = QLabel(self.info_card)
        self.val_id.setObjectName(u"val_id")
        self.val_id.setStyleSheet(u"color: #64748b; font-size: 11px; font-family: 'Courier New';")

        self.infoGrid.addWidget(self.val_id, 5, 1, 1, 1)


        self.bodyLayout.addWidget(self.info_card)

        self.section_details = QToolButton(self.bodyContent)
        self.section_details.setObjectName(u"section_details")
        self.section_details.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.section_details.setStyleSheet(u"QToolButton { color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent; border: none; padding: 0; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/file-text.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.section_details.setIcon(icon1)
        self.section_details.setIconSize(QSize(18, 18))
        self.section_details.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.section_details.setAutoRaise(True)

        self.bodyLayout.addWidget(self.section_details)

        self.txt_details = QPlainTextEdit(self.bodyContent)
        self.txt_details.setObjectName(u"txt_details")
        self.txt_details.setMinimumSize(QSize(0, 120))
        self.txt_details.setStyleSheet(u"QPlainTextEdit { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; font-family: 'Courier New'; font-size: 11px; color: #0f172a; }")
        self.txt_details.setReadOnly(True)

        self.bodyLayout.addWidget(self.txt_details)

        self.avantApresRow = QHBoxLayout()
        self.avantApresRow.setSpacing(12)
        self.avantApresRow.setObjectName(u"avantApresRow")
        self.avantCol = QVBoxLayout()
        self.avantCol.setSpacing(6)
        self.avantCol.setObjectName(u"avantCol")
        self.lbl_avant = QLabel(self.bodyContent)
        self.lbl_avant.setObjectName(u"lbl_avant")
        self.lbl_avant.setStyleSheet(u"color: #b45309; font-size: 11px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.avantCol.addWidget(self.lbl_avant)

        self.txt_avant = QPlainTextEdit(self.bodyContent)
        self.txt_avant.setObjectName(u"txt_avant")
        self.txt_avant.setMinimumSize(QSize(0, 120))
        self.txt_avant.setStyleSheet(u"QPlainTextEdit { background: #fffbeb; border: 1px solid #fde68a; border-radius: 10px; padding: 12px; font-family: 'Courier New'; font-size: 11px; color: #78350f; }")
        self.txt_avant.setReadOnly(True)

        self.avantCol.addWidget(self.txt_avant)


        self.avantApresRow.addLayout(self.avantCol)

        self.apresCol = QVBoxLayout()
        self.apresCol.setSpacing(6)
        self.apresCol.setObjectName(u"apresCol")
        self.lbl_apres = QLabel(self.bodyContent)
        self.lbl_apres.setObjectName(u"lbl_apres")
        self.lbl_apres.setStyleSheet(u"color: #15803d; font-size: 11px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.apresCol.addWidget(self.lbl_apres)

        self.txt_apres = QPlainTextEdit(self.bodyContent)
        self.txt_apres.setObjectName(u"txt_apres")
        self.txt_apres.setMinimumSize(QSize(0, 120))
        self.txt_apres.setStyleSheet(u"QPlainTextEdit { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 12px; font-family: 'Courier New'; font-size: 11px; color: #14532d; }")
        self.txt_apres.setReadOnly(True)

        self.apresCol.addWidget(self.txt_apres)


        self.avantApresRow.addLayout(self.apresCol)


        self.bodyLayout.addLayout(self.avantApresRow)

        self.bodySpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.bodyLayout.addItem(self.bodySpacer)

        self.bodyScroll.setWidget(self.bodyContent)

        self.mainLayout.addWidget(self.bodyScroll)

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

        self.btn_close = QPushButton(self.footer)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMinimumSize(QSize(0, 42))
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 24px; }\n"
"QPushButton:hover { background: #0077B6; }")

        self.footerLayout.addWidget(self.btn_close)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"D\u00e9tail de l'action \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("Dialog", u"D\u00e9tail de l'action", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("Dialog", u"Informations compl\u00e8tes de l'entr\u00e9e d'audit", None))
        self.lbl_k_action.setText(QCoreApplication.translate("Dialog", u"ACTION", None))
        self.val_action.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_user.setText(QCoreApplication.translate("Dialog", u"UTILISATEUR", None))
        self.val_user.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_date.setText(QCoreApplication.translate("Dialog", u"DATE", None))
        self.val_date.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_cible.setText(QCoreApplication.translate("Dialog", u"CIBLE", None))
        self.val_cible.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_machine.setText(QCoreApplication.translate("Dialog", u"MACHINE", None))
        self.val_machine.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_id.setText(QCoreApplication.translate("Dialog", u"ID ENTR\u00c9E", None))
        self.val_id.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.section_details.setText(QCoreApplication.translate("Dialog", u"D\u00c9TAILS", None))
        self.lbl_avant.setText(QCoreApplication.translate("Dialog", u"AVANT", None))
        self.lbl_apres.setText(QCoreApplication.translate("Dialog", u"APR\u00c8S", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
    # retranslateUi

