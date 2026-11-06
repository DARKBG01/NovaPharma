# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_add_fournisseurxKbKNy.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_DialogAddFournisseur(object):
    def setupUi(self, DialogAddFournisseur):
        if not DialogAddFournisseur.objectName():
            DialogAddFournisseur.setObjectName(u"DialogAddFournisseur")
        DialogAddFournisseur.resize(640, 620)
        DialogAddFournisseur.setMinimumSize(QSize(560, 560))
        DialogAddFournisseur.setStyleSheet(u"QDialog#DialogAddFournisseur { background: #f0f4f8; }\n"
"QDialog#DialogAddFournisseur QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(DialogAddFournisseur)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(DialogAddFournisseur)
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
        icon.addFile(u":/Icon/Icons/truck_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        self.form_card = QFrame(DialogAddFournisseur)
        self.form_card.setObjectName(u"form_card")
        self.form_card.setStyleSheet(u"QFrame#form_card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }\n"
"QFrame#form_card QLabel { background: transparent; }")
        self.formLayout = QVBoxLayout(self.form_card)
        self.formLayout.setSpacing(14)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(20, 20, 20, 20)
        self.row_entreprise = QVBoxLayout()
        self.row_entreprise.setSpacing(6)
        self.row_entreprise.setObjectName(u"row_entreprise")
        self.lbl_entreprise = QLabel(self.form_card)
        self.lbl_entreprise.setObjectName(u"lbl_entreprise")
        self.lbl_entreprise.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.row_entreprise.addWidget(self.lbl_entreprise)

        self.edit_raison_sociale = QLineEdit(self.form_card)
        self.edit_raison_sociale.setObjectName(u"edit_raison_sociale")
        self.edit_raison_sociale.setMinimumSize(QSize(0, 42))
        self.edit_raison_sociale.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 8px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.row_entreprise.addWidget(self.edit_raison_sociale)


        self.formLayout.addLayout(self.row_entreprise)

        self.row_cat_resp = QHBoxLayout()
        self.row_cat_resp.setSpacing(16)
        self.row_cat_resp.setObjectName(u"row_cat_resp")
        self.row_categorie = QVBoxLayout()
        self.row_categorie.setSpacing(6)
        self.row_categorie.setObjectName(u"row_categorie")
        self.lbl_categorie = QLabel(self.form_card)
        self.lbl_categorie.setObjectName(u"lbl_categorie")
        self.lbl_categorie.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.row_categorie.addWidget(self.lbl_categorie)

        self.cmb_categorie = QComboBox(self.form_card)
        self.cmb_categorie.addItem("")
        self.cmb_categorie.addItem("")
        self.cmb_categorie.addItem("")
        self.cmb_categorie.addItem("")
        self.cmb_categorie.addItem("")
        self.cmb_categorie.setObjectName(u"cmb_categorie")
        self.cmb_categorie.setMinimumSize(QSize(0, 40))
        self.cmb_categorie.setStyleSheet(u"QComboBox { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 8px 14px; font-size: 13px; color: #0f172a; min-height: 20px; }\n"
"QComboBox::drop-down { border: none; width: 28px; }\n"
"QComboBox QAbstractItemView { background: #ffffff; color: #0f172a; selection-background-color: #e0f2fe; selection-color: #0f172a; }")

        self.row_categorie.addWidget(self.cmb_categorie)


        self.row_cat_resp.addLayout(self.row_categorie)

        self.row_responsable = QVBoxLayout()
        self.row_responsable.setSpacing(6)
        self.row_responsable.setObjectName(u"row_responsable")
        self.lbl_responsable = QLabel(self.form_card)
        self.lbl_responsable.setObjectName(u"lbl_responsable")
        self.lbl_responsable.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.row_responsable.addWidget(self.lbl_responsable)

        self.edit_nom_contact = QLineEdit(self.form_card)
        self.edit_nom_contact.setObjectName(u"edit_nom_contact")
        self.edit_nom_contact.setMinimumSize(QSize(0, 42))
        self.edit_nom_contact.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 8px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.row_responsable.addWidget(self.edit_nom_contact)


        self.row_cat_resp.addLayout(self.row_responsable)


        self.formLayout.addLayout(self.row_cat_resp)

        self.row_tel_email = QHBoxLayout()
        self.row_tel_email.setSpacing(16)
        self.row_tel_email.setObjectName(u"row_tel_email")
        self.row_tel = QVBoxLayout()
        self.row_tel.setSpacing(6)
        self.row_tel.setObjectName(u"row_tel")
        self.lbl_tel = QLabel(self.form_card)
        self.lbl_tel.setObjectName(u"lbl_tel")
        self.lbl_tel.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.row_tel.addWidget(self.lbl_tel)

        self.edit_tel_contact = QLineEdit(self.form_card)
        self.edit_tel_contact.setObjectName(u"edit_tel_contact")
        self.edit_tel_contact.setMinimumSize(QSize(0, 42))
        self.edit_tel_contact.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 8px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.row_tel.addWidget(self.edit_tel_contact)


        self.row_tel_email.addLayout(self.row_tel)

        self.row_email = QVBoxLayout()
        self.row_email.setSpacing(6)
        self.row_email.setObjectName(u"row_email")
        self.lbl_email = QLabel(self.form_card)
        self.lbl_email.setObjectName(u"lbl_email")
        self.lbl_email.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.row_email.addWidget(self.lbl_email)

        self.edit_email_contact = QLineEdit(self.form_card)
        self.edit_email_contact.setObjectName(u"edit_email_contact")
        self.edit_email_contact.setMinimumSize(QSize(0, 42))
        self.edit_email_contact.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 8px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.row_email.addWidget(self.edit_email_contact)


        self.row_tel_email.addLayout(self.row_email)


        self.formLayout.addLayout(self.row_tel_email)

        self.row_adresse = QVBoxLayout()
        self.row_adresse.setSpacing(6)
        self.row_adresse.setObjectName(u"row_adresse")
        self.lbl_adresse = QLabel(self.form_card)
        self.lbl_adresse.setObjectName(u"lbl_adresse")
        self.lbl_adresse.setStyleSheet(u"color: #475569; font-size: 11px; font-weight: 700; background: transparent;")

        self.row_adresse.addWidget(self.lbl_adresse)

        self.edit_adresse = QLineEdit(self.form_card)
        self.edit_adresse.setObjectName(u"edit_adresse")
        self.edit_adresse.setMinimumSize(QSize(0, 42))
        self.edit_adresse.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 8px 14px; font-size: 13px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.row_adresse.addWidget(self.edit_adresse)


        self.formLayout.addLayout(self.row_adresse)

        self.lbl_error = QLabel(self.form_card)
        self.lbl_error.setObjectName(u"lbl_error")
        self.lbl_error.setVisible(False)
        self.lbl_error.setStyleSheet(u"color: #DC2626; font-size: 11px; font-weight: 600; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 8px 12px;")
        self.lbl_error.setWordWrap(True)

        self.formLayout.addWidget(self.lbl_error)


        self.bodyLayout.addWidget(self.form_card)

        self.bodySpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.bodyLayout.addItem(self.bodySpacer)


        self.mainLayout.addLayout(self.bodyLayout)

        self.footer = QFrame(DialogAddFournisseur)
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


        self.retranslateUi(DialogAddFournisseur)

        QMetaObject.connectSlotsByName(DialogAddFournisseur)
    # setupUi

    def retranslateUi(self, DialogAddFournisseur):
        DialogAddFournisseur.setWindowTitle(QCoreApplication.translate("DialogAddFournisseur", u"Nouveau fournisseur \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("DialogAddFournisseur", u"Nouveau fournisseur", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("DialogAddFournisseur", u"Ajoutez un partenaire d'approvisionnement", None))
        self.lbl_entreprise.setText(QCoreApplication.translate("DialogAddFournisseur", u"Nom de l'entreprise *", None))
        self.edit_raison_sociale.setPlaceholderText(QCoreApplication.translate("DialogAddFournisseur", u"Ex : PHARMA DISTRIB SARL", None))
        self.lbl_categorie.setText(QCoreApplication.translate("DialogAddFournisseur", u"Cat\u00e9gorie", None))
        self.cmb_categorie.setItemText(0, QCoreApplication.translate("DialogAddFournisseur", u"Grossiste", None))
        self.cmb_categorie.setItemText(1, QCoreApplication.translate("DialogAddFournisseur", u"Fabricant", None))
        self.cmb_categorie.setItemText(2, QCoreApplication.translate("DialogAddFournisseur", u"Importateur", None))
        self.cmb_categorie.setItemText(3, QCoreApplication.translate("DialogAddFournisseur", u"Mat\u00e9riel m\u00e9dical", None))
        self.cmb_categorie.setItemText(4, QCoreApplication.translate("DialogAddFournisseur", u"Autre", None))

        self.lbl_responsable.setText(QCoreApplication.translate("DialogAddFournisseur", u"Responsable", None))
        self.edit_nom_contact.setPlaceholderText(QCoreApplication.translate("DialogAddFournisseur", u"Ex : Jean Mukendi", None))
        self.lbl_tel.setText(QCoreApplication.translate("DialogAddFournisseur", u"T\u00e9l\u00e9phone", None))
        self.edit_tel_contact.setPlaceholderText(QCoreApplication.translate("DialogAddFournisseur", u"Ex : +243 800 000 000", None))
        self.lbl_email.setText(QCoreApplication.translate("DialogAddFournisseur", u"Email", None))
        self.edit_email_contact.setPlaceholderText(QCoreApplication.translate("DialogAddFournisseur", u"Ex : contact@fournisseur.cd", None))
        self.lbl_adresse.setText(QCoreApplication.translate("DialogAddFournisseur", u"Adresse", None))
        self.edit_adresse.setPlaceholderText(QCoreApplication.translate("DialogAddFournisseur", u"Ex : Avenue Kasa-Vubu, Kinshasa", None))
        self.lbl_error.setText("")
        self.btn_cancel.setText(QCoreApplication.translate("DialogAddFournisseur", u"Annuler", None))
        self.btn_save.setText(QCoreApplication.translate("DialogAddFournisseur", u"Enregistrer le fournisseur", None))
    # retranslateUi

