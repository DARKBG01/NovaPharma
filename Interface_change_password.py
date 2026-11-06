# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_change_passwordsiuitt.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(520, 600)
        Dialog.setMinimumSize(QSize(520, 600))
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
        icon.addFile(u":/Icon/Icons/key_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        self.bodyLayout.setSpacing(16)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(28, 24, 28, 20)
        self.lbl_info = QLabel(Dialog)
        self.lbl_info.setObjectName(u"lbl_info")
        self.lbl_info.setStyleSheet(u"color: #b45309; font-size: 12px; font-weight: 600; background: #fef3c7; border: 1px solid #fde68a; border-radius: 10px; padding: 12px 14px;")
        self.lbl_info.setWordWrap(True)

        self.bodyLayout.addWidget(self.lbl_info)

        self.pwd1Box = QVBoxLayout()
        self.pwd1Box.setSpacing(6)
        self.pwd1Box.setObjectName(u"pwd1Box")
        self.lbl_pwd1 = QLabel(Dialog)
        self.lbl_pwd1.setObjectName(u"lbl_pwd1")
        self.lbl_pwd1.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.pwd1Box.addWidget(self.lbl_pwd1)

        self.pwd1Row = QHBoxLayout()
        self.pwd1Row.setSpacing(8)
        self.pwd1Row.setObjectName(u"pwd1Row")
        self.inp_pwd1 = QLineEdit(Dialog)
        self.inp_pwd1.setObjectName(u"inp_pwd1")
        self.inp_pwd1.setMinimumSize(QSize(0, 44))
        self.inp_pwd1.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")
        self.inp_pwd1.setEchoMode(QLineEdit.EchoMode.Password)

        self.pwd1Row.addWidget(self.inp_pwd1)

        self.btn_toggle_pwd1 = QPushButton(Dialog)
        self.btn_toggle_pwd1.setObjectName(u"btn_toggle_pwd1")
        self.btn_toggle_pwd1.setMinimumSize(QSize(44, 44))
        self.btn_toggle_pwd1.setMaximumSize(QSize(44, 44))
        self.btn_toggle_pwd1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_toggle_pwd1.setStyleSheet(u"QPushButton { background: #f1f5f9; border: 1.5px solid #e2e8f0; border-radius: 10px; }\n"
"QPushButton:hover { background: #e2e8f0; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/eye.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_toggle_pwd1.setIcon(icon1)
        self.btn_toggle_pwd1.setIconSize(QSize(18, 18))

        self.pwd1Row.addWidget(self.btn_toggle_pwd1)


        self.pwd1Box.addLayout(self.pwd1Row)


        self.bodyLayout.addLayout(self.pwd1Box)

        self.strengthBox = QVBoxLayout()
        self.strengthBox.setSpacing(6)
        self.strengthBox.setObjectName(u"strengthBox")
        self.bar_strength = QProgressBar(Dialog)
        self.bar_strength.setObjectName(u"bar_strength")
        self.bar_strength.setMaximumSize(QSize(16777215, 6))
        self.bar_strength.setStyleSheet(u"QProgressBar { background: #e2e8f0; border: none; border-radius: 3px; }\n"
"QProgressBar::chunk { background: #DC2626; border-radius: 3px; }")
        self.bar_strength.setValue(0)
        self.bar_strength.setTextVisible(False)

        self.strengthBox.addWidget(self.bar_strength)

        self.lbl_strength = QLabel(Dialog)
        self.lbl_strength.setObjectName(u"lbl_strength")
        self.lbl_strength.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 700; background: transparent;")

        self.strengthBox.addWidget(self.lbl_strength)


        self.bodyLayout.addLayout(self.strengthBox)

        self.pwd2Box = QVBoxLayout()
        self.pwd2Box.setSpacing(6)
        self.pwd2Box.setObjectName(u"pwd2Box")
        self.lbl_pwd2 = QLabel(Dialog)
        self.lbl_pwd2.setObjectName(u"lbl_pwd2")
        self.lbl_pwd2.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.pwd2Box.addWidget(self.lbl_pwd2)

        self.pwd2Row = QHBoxLayout()
        self.pwd2Row.setSpacing(8)
        self.pwd2Row.setObjectName(u"pwd2Row")
        self.inp_pwd2 = QLineEdit(Dialog)
        self.inp_pwd2.setObjectName(u"inp_pwd2")
        self.inp_pwd2.setMinimumSize(QSize(0, 44))
        self.inp_pwd2.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 10px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")
        self.inp_pwd2.setEchoMode(QLineEdit.EchoMode.Password)

        self.pwd2Row.addWidget(self.inp_pwd2)

        self.btn_toggle_pwd2 = QPushButton(Dialog)
        self.btn_toggle_pwd2.setObjectName(u"btn_toggle_pwd2")
        self.btn_toggle_pwd2.setMinimumSize(QSize(44, 44))
        self.btn_toggle_pwd2.setMaximumSize(QSize(44, 44))
        self.btn_toggle_pwd2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_toggle_pwd2.setStyleSheet(u"QPushButton { background: #f1f5f9; border: 1.5px solid #e2e8f0; border-radius: 10px; }\n"
"QPushButton:hover { background: #e2e8f0; }")
        self.btn_toggle_pwd2.setIcon(icon1)
        self.btn_toggle_pwd2.setIconSize(QSize(18, 18))

        self.pwd2Row.addWidget(self.btn_toggle_pwd2)


        self.pwd2Box.addLayout(self.pwd2Row)


        self.bodyLayout.addLayout(self.pwd2Box)

        self.checklist = QFrame(Dialog)
        self.checklist.setObjectName(u"checklist")
        self.checklist.setStyleSheet(u"QFrame#checklist { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; }")
        self.checklistLayout = QVBoxLayout(self.checklist)
        self.checklistLayout.setSpacing(6)
        self.checklistLayout.setObjectName(u"checklistLayout")
        self.checklistLayout.setContentsMargins(14, 12, 14, 12)
        self.checkLen = QHBoxLayout()
        self.checkLen.setSpacing(8)
        self.checkLen.setObjectName(u"checkLen")
        self.ico_len = QLabel(self.checklist)
        self.ico_len.setObjectName(u"ico_len")
        self.ico_len.setMinimumSize(QSize(16, 16))
        self.ico_len.setMaximumSize(QSize(16, 16))

        self.checkLen.addWidget(self.ico_len)

        self.lbl_len = QLabel(self.checklist)
        self.lbl_len.setObjectName(u"lbl_len")
        self.lbl_len.setStyleSheet(u"color: #64748b; font-size: 11px; background: transparent;")

        self.checkLen.addWidget(self.lbl_len)

        self.spacer_len = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.checkLen.addItem(self.spacer_len)


        self.checklistLayout.addLayout(self.checkLen)

        self.checkMatch = QHBoxLayout()
        self.checkMatch.setSpacing(8)
        self.checkMatch.setObjectName(u"checkMatch")
        self.ico_match = QLabel(self.checklist)
        self.ico_match.setObjectName(u"ico_match")
        self.ico_match.setMinimumSize(QSize(16, 16))
        self.ico_match.setMaximumSize(QSize(16, 16))

        self.checkMatch.addWidget(self.ico_match)

        self.lbl_match = QLabel(self.checklist)
        self.lbl_match.setObjectName(u"lbl_match")
        self.lbl_match.setStyleSheet(u"color: #64748b; font-size: 11px; background: transparent;")

        self.checkMatch.addWidget(self.lbl_match)

        self.spacer_match = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.checkMatch.addItem(self.spacer_match)


        self.checklistLayout.addLayout(self.checkMatch)

        self.checkDiff = QHBoxLayout()
        self.checkDiff.setSpacing(8)
        self.checkDiff.setObjectName(u"checkDiff")
        self.ico_diff = QLabel(self.checklist)
        self.ico_diff.setObjectName(u"ico_diff")
        self.ico_diff.setMinimumSize(QSize(16, 16))
        self.ico_diff.setMaximumSize(QSize(16, 16))

        self.checkDiff.addWidget(self.ico_diff)

        self.lbl_diff = QLabel(self.checklist)
        self.lbl_diff.setObjectName(u"lbl_diff")
        self.lbl_diff.setStyleSheet(u"color: #64748b; font-size: 11px; background: transparent;")

        self.checkDiff.addWidget(self.lbl_diff)

        self.spacer_diff = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.checkDiff.addItem(self.spacer_diff)


        self.checklistLayout.addLayout(self.checkDiff)


        self.bodyLayout.addWidget(self.checklist)

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


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Changement de mot de passe \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("Dialog", u"Nouveau mot de passe", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("Dialog", u"Votre mot de passe actuel est temporaire", None))
        self.lbl_info.setText(QCoreApplication.translate("Dialog", u"Un administrateur a r\u00e9initialis\u00e9 votre mot de passe. Vous devez en d\u00e9finir un nouveau pour continuer.", None))
        self.lbl_pwd1.setText(QCoreApplication.translate("Dialog", u"Nouveau mot de passe", None))
        self.inp_pwd1.setPlaceholderText(QCoreApplication.translate("Dialog", u"Minimum 8 caract\u00e8res", None))
        self.btn_toggle_pwd1.setText("")
        self.lbl_strength.setText("")
        self.lbl_pwd2.setText(QCoreApplication.translate("Dialog", u"Confirmer le mot de passe", None))
        self.inp_pwd2.setPlaceholderText(QCoreApplication.translate("Dialog", u"Ressaisissez le mot de passe", None))
        self.btn_toggle_pwd2.setText("")
        self.ico_len.setText("")
        self.lbl_len.setText(QCoreApplication.translate("Dialog", u"Au moins 8 caract\u00e8res", None))
        self.ico_match.setText("")
        self.lbl_match.setText(QCoreApplication.translate("Dialog", u"Les deux mots de passe correspondent", None))
        self.ico_diff.setText("")
        self.lbl_diff.setText(QCoreApplication.translate("Dialog", u"Diff\u00e9rent du mot de passe temporaire", None))
        self.lbl_error.setText("")
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"Quitter", None))
        self.btn_save.setText(QCoreApplication.translate("Dialog", u"Enregistrer", None))
    # retranslateUi

