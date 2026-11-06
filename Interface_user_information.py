# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_user_informationrwqFqP.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(530, 491)
        Dialog.setStyleSheet(u"/* ============================================================\n"
"   INTERFACE INFORMATIONS UTILISATEUR - THEME MODERNE\n"
"   Cible les \u00e9l\u00e9ments du fichier Interface_user_information.ui\n"
"   ============================================================ */\n"
"\n"
"/* Style de la fen\u00eatre principale */\n"
"QDialog {\n"
"    background-color: #f8fafc; /* Fond tr\u00e8s clair */\n"
"}\n"
"\n"
"/* Zone Photo et QR Code */\n"
"QLabel#lbl_photo, QLabel#lbl_qrcode {\n"
"    background-color: #ffffff;\n"
"    border: 2px dashed #cbd5e1;\n"
"    border-radius: 12px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"/* Label du Nom (Gros titre) */\n"
"QLabel#lbl_nom, QLabel#label_5 {\n"
"    font-size: 16pt;\n"
"    font-weight: bold;\n"
"    color: #1e293b;\n"
"    margin-top: 10px;\n"
"}\n"
"\n"
"/* Style des GroupBox (Sections d'information) */\n"
"QGroupBox {\n"
"    font-weight: bold;\n"
"    font-size: 11pt;\n"
"    color: #3b82f6; /* Bleu primaire */\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius:"
                        " 10px;\n"
"    margin-top: 1.5em;\n"
"    background-color: #ffffff;\n"
"    padding-top: 20px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top center;\n"
"    padding: 0 5px;\n"
"}\n"
"\n"
"/* Labels d'information \u00e0 l'int\u00e9rieur des GroupBox */\n"
"QGroupBox QLabel {\n"
"    color: #475569;\n"
"    font-weight: normal;\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"/* Boutons d'action (Sauvegarder, Modifier, Fermer) */\n"
"QPushButton {\n"
"    background-color: #3b82f6;\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 8px;\n"
"    padding: 10px 20px;\n"
"    min-width: 100px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2563eb;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1d4ed8;\n"
"}\n"
"\n"
"/* Bouton sp\u00e9cifique pour Annuler/Fermer (s'il existe un ID pushButton_3) */\n"
"QPushButton#pushButton_3 {\n"
"    background-color: transparent;\n"
"    border: 1px solid #e2e8f0;\n"
"    color: #6"
                        "4748b;\n"
"}\n"
"\n"
"QPushButton#pushButton_3:hover {\n"
"    background-color: #f1f5f9;\n"
"    color: #ef4444; /* Devient rouge au survol */\n"
"}\n"
"\n"
"/* Champs \u00e9ditables (QLineEdit) \u00e0 l'int\u00e9rieur de l'interface */\n"
"QLineEdit {\n"
"    background-color: #f1f5f9;\n"
"    border: 1px solid #cbd5e1;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"    color: #1e293b;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #3b82f6;\n"
"    background-color: #ffffff;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_photo = QLabel(Dialog)
        self.lbl_photo.setObjectName(u"lbl_photo")
        self.lbl_photo.setMinimumSize(QSize(250, 250))
        self.lbl_photo.setMaximumSize(QSize(250, 250))
        self.lbl_photo.setScaledContents(True)
        self.lbl_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_photo, 0, Qt.AlignmentFlag.AlignHCenter)

        self.lbl_nom = QLabel(Dialog)
        self.lbl_nom.setObjectName(u"lbl_nom")
        self.lbl_nom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_nom)

        self.verticalLayout.setStretch(0, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, -1, -1, -1)
        self.lbl_qrcode = QLabel(Dialog)
        self.lbl_qrcode.setObjectName(u"lbl_qrcode")
        self.lbl_qrcode.setMinimumSize(QSize(250, 250))
        self.lbl_qrcode.setMaximumSize(QSize(250, 250))
        self.lbl_qrcode.setScaledContents(True)
        self.lbl_qrcode.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.lbl_qrcode)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_5)


        self.horizontalLayout_2.addLayout(self.verticalLayout_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setEnabled(False)
        self.label.setStyleSheet(u"")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextEditable|Qt.TextInteractionFlag.TextEditorInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.label)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_3.addWidget(self.lineEdit)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(False)
        self.label_2.setStyleSheet(u"")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextEditable|Qt.TextInteractionFlag.TextEditorInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_4.addWidget(self.label_2)

        self.lineEdit_2 = QLineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout_4.addWidget(self.lineEdit_2)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(False)
        self.label_3.setStyleSheet(u"")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextEditable|Qt.TextInteractionFlag.TextEditorInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_5.addWidget(self.label_3)

        self.lineEdit_3 = QLineEdit(self.groupBox_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.verticalLayout_5.addWidget(self.lineEdit_3)


        self.horizontalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(Dialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_4 = QLabel(self.groupBox_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(False)
        self.label_4.setStyleSheet(u"")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextEditable|Qt.TextInteractionFlag.TextEditorInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_6.addWidget(self.label_4)

        self.lineEdit_4 = QLineEdit(self.groupBox_4)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.verticalLayout_6.addWidget(self.lineEdit_4)


        self.horizontalLayout.addWidget(self.groupBox_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2.setStretch(0, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lbl_photo.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.lbl_nom.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.lbl_qrcode.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Num\u00e9ro de la caisse", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"A", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Numero de t\u00e9l\u00e9phone", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"R\u00f4le", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Mots de passe", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Sauvegarder", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Modifier", None))
    # retranslateUi

