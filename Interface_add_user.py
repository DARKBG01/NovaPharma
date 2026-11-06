# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_add_userzuwoBt.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(668, 784)
        Dialog.setStyleSheet(u"/* ============================================================\n"
"NOVA PHARMA - TH\u00c8ME WIZARD MODERNE\n"
"Palette : Slate 50/200/800 & Blue 600\n"
"============================================================ */\n"
"\n"
"/* Fen\u00eatre principale du Wizard */\n"
"QDialog {\n"
"background-color: #f8fafc;\n"
"}\n"
"\n"
"/* Contenu des pages du Wizard */\n"
"QFrame {\n"
"background-color: #f8fafc;\n"
"}\n"
"\n"
"/* --- SECTION PHOTO --- */\n"
"\n"
"#label {\n"
"background-color: #ffffff;\n"
"border: 2px dashed #cbd5e1;\n"
"border-radius: 75px;\n"
"color: #64748b;\n"
"font-weight: bold;\n"
"margin-bottom: 5px;\n"
"qproperty-alignment: 'AlignCenter';\n"
"}\n"
"\n"
"#label:hover {\n"
"border: 2px dashed #2563eb;\n"
"background-color: #eff6ff;\n"
"}\n"
"\n"
"#pushButton {\n"
"background-color: #ffffff;\n"
"color: #475569;\n"
"border: 1px solid #e2e8f0;\n"
"border-radius: 8px;\n"
"padding: 6px 15px;\n"
"font-weight: 600;\n"
"}\n"
"\n"
"#pushButton:hover {\n"
"background-color: #f1f5f9;\n"
"border-color: #cbd5e1"
                        ";\n"
"color: #2563eb;\n"
"}\n"
"\n"
"/* --- GROUPE D'INFORMATION --- */\n"
"\n"
"QGroupBox {\n"
"background-color: #ffffff;\n"
"border: 1px solid #e2e8f0;\n"
"border-radius: 15px;\n"
"margin-top: 25px;\n"
"font-weight: bold;\n"
"color: #1e293b;\n"
"padding-top: 30px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"subcontrol-origin: margin;\n"
"subcontrol-position: top left;\n"
"left: 20px;\n"
"padding: 0 5px;\n"
"color: #2563eb;\n"
"}\n"
"\n"
"/* --- FORMULAIRE & INPUTS --- */\n"
"\n"
"QLabel {\n"
"color: #475569;\n"
"font-weight: 500;\n"
"background: transparent;\n"
"}\n"
"\n"
"QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox {\n"
"background-color: #f1f5f9;\n"
"border: 1px solid transparent;\n"
"border-radius: 8px;\n"
"padding: 8px 12px;\n"
"color: #1e293b;\n"
"selection-background-color: #2563eb;\n"
"}\n"
"\n"
"QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus {\n"
"background-color: #ffffff;\n"
"border: 1px solid #2563eb;\n"
"}\n"
"\n"
"/* --- QCOMBOBOX SP\u00c9CIFIQUE --- */\n"
"\n"
"QComboBox {\n"
"padding-rig"
                        "ht: 20px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"width: 25px;\n"
"border-left: none;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"image: url(:/Icon/Icons/chevron-down copy.svg);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"background-color: #ffffff;\n"
"border: 1px solid #e2e8f0;\n"
"border-radius: 8px;\n"
"selection-background-color: #eff6ff;\n"
"selection-color: #2563eb;\n"
"outline: none;\n"
"}\n"
"\n"
"/* --- QDOUBLESPINBOX SP\u00c9CIFIQUE --- */\n"
"\n"
"QDoubleSpinBox::up-button, QSpinBox::up-button {\n"
"subcontrol-origin: border;\n"
"subcontrol-position: top right;\n"
"width: 20px;\n"
"border-top-right-radius: 8px;\n"
"background: transparent;\n"
"}\n"
"\n"
"QDoubleSpinBox::down-button, QSpinBox::down-button {\n"
"subcontrol-origin: border;\n"
"subcontrol-position: bottom right;\n"
"width: 20px;\n"
"border-bottom-right-radius: 8px;\n"
"background: transparent;\n"
"}\n"
"\n"
"/* --- RADIO BUTTONS --- */\n"
"\n"
"QRadioButton {\n"
""
                        "spacing: 8px;\n"
"color: #475569;\n"
"background: transparent;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"width: 18px;\n"
"height: 18px;\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"border: 2px solid #cbd5e1;\n"
"border-radius: 10px;\n"
"background-color: white;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"border: 2px solid #2563eb;\n"
"border-radius: 10px;\n"
"background-color: #2563eb;\n"
"image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNiIgaGVpZ2h0PSI2IiB2aWV3Qm94PSIwIDAgNiA2IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxjaXJjbGUgY3g9IjMiIGN5PSIzIiByPSIxLjUiIGZpbGw9IndoaXRlIi8+PC9zdmc+);\n"
"}\n"
"\n"
"/* --- BOUTONS DE NAVIGATION DU WIZARD --- */\n"
"\n"
"QPushButton {\n"
"background-color: #2563eb;\n"
"color: #ffffff;\n"
"border-radius: 8px;\n"
"padding: 8px 20px;\n"
"font-weight: bold;\n"
"min-width: 100px;\n"
"border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: #1d4ed8;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: #1e40af;\n"
""
                        "}\n"
"\n"
"QPushButton:disabled {\n"
"background-color: #e2e8f0;\n"
"color: #94a3b8;\n"
"}\n"
"")
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(300, 300))
        self.label.setMaximumSize(QSize(300, 300))
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(132, 0))

        self.verticalLayout.addWidget(self.pushButton, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(647, 2, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 50))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(0, 50))

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(0, 50))

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lineEdit_3)

        self.lineEdit_4 = QLineEdit(self.groupBox)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(0, 50))

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.lineEdit_4)

        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.radioButton = QRadioButton(self.frame)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.radioButton, 0, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.frame)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setMinimumSize(QSize(0, 50))

        self.gridLayout.addWidget(self.radioButton_2, 0, 1, 1, 1)


        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.frame)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout_2.addWidget(self.pushButton_2)


        self.verticalLayout_3.addWidget(self.groupBox)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Ajouter un utilisateur", None))
        self.label.setText("")
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Charger", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Information sur l'utilisateur", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Nom Complet : ", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Entrez le nom complet", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Sexe : ", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Numero de t\u00e9l\u00e9phone : ", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Mots de passe : ", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Confirmer le mots de passe : ", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Dialog", u"+243XXXXXXXXX", None))
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"Homme", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", u"Femme", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Confirmer", None))
    # retranslateUi

