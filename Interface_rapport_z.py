# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_rapport_zYPkzLz.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QDialog, QDoubleSpinBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_DialogRapportZ(object):
    def setupUi(self, DialogRapportZ):
        if not DialogRapportZ.objectName():
            DialogRapportZ.setObjectName(u"DialogRapportZ")
        DialogRapportZ.resize(720, 780)
        DialogRapportZ.setStyleSheet(u"\n"
"QDialog { background: #f0f4f8; }\n"
"QFrame#header_z {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:0.5 #0077B6, stop:1 #00B4D8);\n"
"    border-top-left-radius: 14px;\n"
"    border-top-right-radius: 14px;\n"
"}\n"
"QFrame#card {\n"
"    background: #ffffff;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 12px;\n"
"}\n"
"QLabel { color: #334155; font-size: 13px; background: transparent; }\n"
"QLabel#header_title { color: white; font-size: 18px; font-weight: 800; }\n"
"QLabel#header_sub   { color: #CAF0F8; font-size: 11px; }\n"
"QLabel#section_title {\n"
"    color: #023E8A; font-size: 13px; font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#value_big {\n"
"    color: #0f172a; font-size: 22px; font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#value_money {\n"
"    color: #023E8A; font-size: 14px; font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#ecart_ok    { color: #16A34A; font-size: 16px; font"
                        "-weight: 800; }\n"
"QLabel#ecart_warn  { color: #F4A261; font-size: 16px; font-weight: 800; }\n"
"QLabel#ecart_danger{ color: #DC2626; font-size: 16px; font-weight: 800; }\n"
"QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {\n"
"    background: #f8fafc;\n"
"    border: 1.5px solid #e2e8f0;\n"
"    border-radius: 10px;\n"
"    padding: 8px 12px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    min-height: 22px;\n"
"}\n"
"QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {\n"
"    background: #ffffff;\n"
"    border-color: #00B4D8;\n"
"}\n"
"QPushButton {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 10px 22px;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    min-width: 120px;\n"
"}\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"QPushB"
                        "utton#btn_secondary {\n"
"    background: transparent;\n"
"    color: #64748b;\n"
"    border: 1.5px solid #e2e8f0;\n"
"}\n"
"QPushButton#btn_secondary:hover {\n"
"    background: #fef2f2;\n"
"    color: #dc2626;\n"
"    border-color: #fecaca;\n"
"}\n"
"   ")
        self.root = QVBoxLayout(DialogRapportZ)
        self.root.setSpacing(0)
        self.root.setObjectName(u"root")
        self.root.setContentsMargins(0, 0, 0, 0)
        self.header_z = QFrame(DialogRapportZ)
        self.header_z.setObjectName(u"header_z")
        self.header_z.setMinimumSize(QSize(0, 80))
        self.hboxLayout = QHBoxLayout(self.header_z)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.hboxLayout.setContentsMargins(24, 16, 24, 16)
        self.header_icon = QLabel(self.header_z)
        self.header_icon.setObjectName(u"header_icon")
        self.header_icon.setMinimumSize(QSize(40, 40))
        self.header_icon.setMaximumSize(QSize(40, 40))
        self.header_icon.setPixmap(QPixmap(u":/Icon/Icons/receipt_white.svg"))
        self.header_icon.setScaledContents(True)

        self.hboxLayout.addWidget(self.header_icon)

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setSpacing(2)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.header_title = QLabel(self.header_z)
        self.header_title.setObjectName(u"header_title")

        self.vboxLayout.addWidget(self.header_title)

        self.header_sub = QLabel(self.header_z)
        self.header_sub.setObjectName(u"header_sub")

        self.vboxLayout.addWidget(self.header_sub)


        self.hboxLayout.addLayout(self.vboxLayout)


        self.root.addWidget(self.header_z)

        self.scrollArea = QScrollArea(DialogRapportZ)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName(u"scroll_content")
        self.scroll_content.setGeometry(QRect(0, 0, 706, 840))
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setSpacing(14)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.card = QFrame(self.scroll_content)
        self.card.setObjectName(u"card")
        self.vboxLayout1 = QVBoxLayout(self.card)
        self.vboxLayout1.setSpacing(10)
        self.vboxLayout1.setObjectName(u"vboxLayout1")
        self.vboxLayout1.setContentsMargins(20, 16, 20, 16)
        self.section_title = QLabel(self.card)
        self.section_title.setObjectName(u"section_title")

        self.vboxLayout1.addWidget(self.section_title)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(12)
        self.formLayout.setVerticalSpacing(12)
        self.label = QLabel(self.card)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.combo_periode = QComboBox(self.card)
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.addItem("")
        self.combo_periode.setObjectName(u"combo_periode")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.combo_periode)

        self.label1 = QLabel(self.card)
        self.label1.setObjectName(u"label1")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label1)

        self.date_debut = QDateEdit(self.card)
        self.date_debut.setObjectName(u"date_debut")
        self.date_debut.setCalendarPopup(True)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.date_debut)

        self.label2 = QLabel(self.card)
        self.label2.setObjectName(u"label2")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label2)

        self.date_fin = QDateEdit(self.card)
        self.date_fin.setObjectName(u"date_fin")
        self.date_fin.setCalendarPopup(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.date_fin)

        self.label3 = QLabel(self.card)
        self.label3.setObjectName(u"label3")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label3)

        self.combo_caisse = QComboBox(self.card)
        self.combo_caisse.setObjectName(u"combo_caisse")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.combo_caisse)


        self.vboxLayout1.addLayout(self.formLayout)


        self.content_layout.addWidget(self.card)

        self.card1 = QFrame(self.scroll_content)
        self.card1.setObjectName(u"card1")
        self.vboxLayout2 = QVBoxLayout(self.card1)
        self.vboxLayout2.setSpacing(10)
        self.vboxLayout2.setObjectName(u"vboxLayout2")
        self.vboxLayout2.setContentsMargins(20, 16, 20, 16)
        self.section_title1 = QLabel(self.card1)
        self.section_title1.setObjectName(u"section_title1")

        self.vboxLayout2.addWidget(self.section_title1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(10)
        self.label4 = QLabel(self.card1)
        self.label4.setObjectName(u"label4")

        self.gridLayout.addWidget(self.label4, 0, 0, 1, 1)

        self.value_big = QLabel(self.card1)
        self.value_big.setObjectName(u"value_big")

        self.gridLayout.addWidget(self.value_big, 0, 1, 1, 1)

        self.label5 = QLabel(self.card1)
        self.label5.setObjectName(u"label5")

        self.gridLayout.addWidget(self.label5, 0, 2, 1, 1)

        self.value_big1 = QLabel(self.card1)
        self.value_big1.setObjectName(u"value_big1")

        self.gridLayout.addWidget(self.value_big1, 0, 3, 1, 1)

        self.label6 = QLabel(self.card1)
        self.label6.setObjectName(u"label6")

        self.gridLayout.addWidget(self.label6, 1, 0, 1, 1)

        self.value_money = QLabel(self.card1)
        self.value_money.setObjectName(u"value_money")

        self.gridLayout.addWidget(self.value_money, 1, 1, 1, 1)

        self.label7 = QLabel(self.card1)
        self.label7.setObjectName(u"label7")

        self.gridLayout.addWidget(self.label7, 1, 2, 1, 1)

        self.value_money1 = QLabel(self.card1)
        self.value_money1.setObjectName(u"value_money1")

        self.gridLayout.addWidget(self.value_money1, 1, 3, 1, 1)

        self.label8 = QLabel(self.card1)
        self.label8.setObjectName(u"label8")

        self.gridLayout.addWidget(self.label8, 2, 0, 1, 1)

        self.value_big2 = QLabel(self.card1)
        self.value_big2.setObjectName(u"value_big2")

        self.gridLayout.addWidget(self.value_big2, 2, 1, 1, 1)

        self.label9 = QLabel(self.card1)
        self.label9.setObjectName(u"label9")

        self.gridLayout.addWidget(self.label9, 2, 2, 1, 1)

        self.value_big3 = QLabel(self.card1)
        self.value_big3.setObjectName(u"value_big3")

        self.gridLayout.addWidget(self.value_big3, 2, 3, 1, 1)

        self.label10 = QLabel(self.card1)
        self.label10.setObjectName(u"label10")

        self.gridLayout.addWidget(self.label10, 3, 0, 1, 1)

        self.value_big4 = QLabel(self.card1)
        self.value_big4.setObjectName(u"value_big4")

        self.gridLayout.addWidget(self.value_big4, 3, 1, 1, 1)

        self.label11 = QLabel(self.card1)
        self.label11.setObjectName(u"label11")

        self.gridLayout.addWidget(self.label11, 3, 2, 1, 1)

        self.value_money2 = QLabel(self.card1)
        self.value_money2.setObjectName(u"value_money2")

        self.gridLayout.addWidget(self.value_money2, 3, 3, 1, 1)


        self.vboxLayout2.addLayout(self.gridLayout)


        self.content_layout.addWidget(self.card1)

        self.card2 = QFrame(self.scroll_content)
        self.card2.setObjectName(u"card2")
        self.vboxLayout3 = QVBoxLayout(self.card2)
        self.vboxLayout3.setSpacing(10)
        self.vboxLayout3.setObjectName(u"vboxLayout3")
        self.vboxLayout3.setContentsMargins(20, 16, 20, 16)
        self.section_title2 = QLabel(self.card2)
        self.section_title2.setObjectName(u"section_title2")

        self.vboxLayout3.addWidget(self.section_title2)

        self.formLayout1 = QFormLayout()
        self.formLayout1.setObjectName(u"formLayout1")
        self.formLayout1.setHorizontalSpacing(12)
        self.formLayout1.setVerticalSpacing(12)
        self.label12 = QLabel(self.card2)
        self.label12.setObjectName(u"label12")

        self.formLayout1.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label12)

        self.value_money3 = QLabel(self.card2)
        self.value_money3.setObjectName(u"value_money3")

        self.formLayout1.setWidget(0, QFormLayout.ItemRole.FieldRole, self.value_money3)

        self.label13 = QLabel(self.card2)
        self.label13.setObjectName(u"label13")

        self.formLayout1.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label13)

        self.spin_compte = QDoubleSpinBox(self.card2)
        self.spin_compte.setObjectName(u"spin_compte")
        self.spin_compte.setMinimumSize(QSize(200, 42))
        self.spin_compte.setDecimals(2)
        self.spin_compte.setMaximum(999999999.990000009536743)

        self.formLayout1.setWidget(1, QFormLayout.ItemRole.FieldRole, self.spin_compte)


        self.vboxLayout3.addLayout(self.formLayout1)

        self.ecart_ok = QLabel(self.card2)
        self.ecart_ok.setObjectName(u"ecart_ok")
        self.ecart_ok.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vboxLayout3.addWidget(self.ecart_ok)


        self.content_layout.addWidget(self.card2)

        self.card3 = QFrame(self.scroll_content)
        self.card3.setObjectName(u"card3")
        self.vboxLayout4 = QVBoxLayout(self.card3)
        self.vboxLayout4.setSpacing(10)
        self.vboxLayout4.setObjectName(u"vboxLayout4")
        self.vboxLayout4.setContentsMargins(20, 16, 20, 16)
        self.section_title3 = QLabel(self.card3)
        self.section_title3.setObjectName(u"section_title3")

        self.vboxLayout4.addWidget(self.section_title3)

        self.formLayout2 = QFormLayout()
        self.formLayout2.setObjectName(u"formLayout2")
        self.formLayout2.setHorizontalSpacing(12)
        self.formLayout2.setVerticalSpacing(12)
        self.label14 = QLabel(self.card3)
        self.label14.setObjectName(u"label14")

        self.formLayout2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label14)

        self.combo_format = QComboBox(self.card3)
        self.combo_format.addItem("")
        self.combo_format.addItem("")
        self.combo_format.setObjectName(u"combo_format")

        self.formLayout2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.combo_format)

        self.label15 = QLabel(self.card3)
        self.label15.setObjectName(u"label15")

        self.formLayout2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label15)

        self.chk_print_auto = QCheckBox(self.card3)
        self.chk_print_auto.setObjectName(u"chk_print_auto")
        self.chk_print_auto.setChecked(True)

        self.formLayout2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.chk_print_auto)


        self.vboxLayout4.addLayout(self.formLayout2)


        self.content_layout.addWidget(self.card3)

        self.scrollArea.setWidget(self.scroll_content)

        self.root.addWidget(self.scrollArea)

        self.frame = QFrame(DialogRapportZ)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 70))
        self.hboxLayout1 = QHBoxLayout(self.frame)
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.hboxLayout1.setContentsMargins(20, -1, 20, -1)
        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout1.addItem(self.spacerItem)

        self.btn_secondary = QPushButton(self.frame)
        self.btn_secondary.setObjectName(u"btn_secondary")

        self.hboxLayout1.addWidget(self.btn_secondary)

        self.btn_generer = QPushButton(self.frame)
        self.btn_generer.setObjectName(u"btn_generer")

        self.hboxLayout1.addWidget(self.btn_generer)


        self.root.addWidget(self.frame)


        self.retranslateUi(DialogRapportZ)

        QMetaObject.connectSlotsByName(DialogRapportZ)
    # setupUi

    def retranslateUi(self, DialogRapportZ):
        DialogRapportZ.setWindowTitle(QCoreApplication.translate("DialogRapportZ", u"Cl\u00f4ture de caisse \u2014 Rapport Z", None))
        self.header_title.setText(QCoreApplication.translate("DialogRapportZ", u"Cl\u00f4ture de caisse \u2014 Rapport Z", None))
        self.header_sub.setText(QCoreApplication.translate("DialogRapportZ", u"V\u00e9rifiez votre caisse et imprimez le rapport de fin de p\u00e9riode", None))
        self.scrollArea.setStyleSheet(QCoreApplication.translate("DialogRapportZ", u"background: transparent;", None))
        self.scroll_content.setStyleSheet(QCoreApplication.translate("DialogRapportZ", u"background: transparent;", None))
        self.section_title.setText(QCoreApplication.translate("DialogRapportZ", u"Param\u00e8tres", None))
        self.label.setText(QCoreApplication.translate("DialogRapportZ", u"P\u00e9riode", None))
        self.combo_periode.setItemText(0, QCoreApplication.translate("DialogRapportZ", u"Aujourd'hui", None))
        self.combo_periode.setItemText(1, QCoreApplication.translate("DialogRapportZ", u"Hier", None))
        self.combo_periode.setItemText(2, QCoreApplication.translate("DialogRapportZ", u"Shift en cours", None))
        self.combo_periode.setItemText(3, QCoreApplication.translate("DialogRapportZ", u"7 derniers jours", None))
        self.combo_periode.setItemText(4, QCoreApplication.translate("DialogRapportZ", u"Personnalis\u00e9", None))

        self.label1.setText(QCoreApplication.translate("DialogRapportZ", u"Du", None))
        self.date_debut.setDisplayFormat(QCoreApplication.translate("DialogRapportZ", u"dd/MM/yyyy", None))
        self.label2.setText(QCoreApplication.translate("DialogRapportZ", u"Au", None))
        self.date_fin.setDisplayFormat(QCoreApplication.translate("DialogRapportZ", u"dd/MM/yyyy", None))
        self.label3.setText(QCoreApplication.translate("DialogRapportZ", u"Caisse", None))
        self.section_title1.setText(QCoreApplication.translate("DialogRapportZ", u"Aper\u00e7u des ventes", None))
        self.label4.setText(QCoreApplication.translate("DialogRapportZ", u"Factures", None))
        self.value_big.setText(QCoreApplication.translate("DialogRapportZ", u"0", None))
        self.label5.setText(QCoreApplication.translate("DialogRapportZ", u"Articles", None))
        self.value_big1.setText(QCoreApplication.translate("DialogRapportZ", u"0", None))
        self.label6.setText(QCoreApplication.translate("DialogRapportZ", u"CA total", None))
        self.value_money.setText(QCoreApplication.translate("DialogRapportZ", u"0 FC", None))
        self.label7.setText(QCoreApplication.translate("DialogRapportZ", u"Panier moyen", None))
        self.value_money1.setText(QCoreApplication.translate("DialogRapportZ", u"0 FC", None))
        self.label8.setText(QCoreApplication.translate("DialogRapportZ", u"Clients identifi\u00e9s", None))
        self.value_big2.setText(QCoreApplication.translate("DialogRapportZ", u"0", None))
        self.label9.setText(QCoreApplication.translate("DialogRapportZ", u"Clients anonymes", None))
        self.value_big3.setText(QCoreApplication.translate("DialogRapportZ", u"0", None))
        self.label10.setText(QCoreApplication.translate("DialogRapportZ", u"Annulations (nb)", None))
        self.value_big4.setText(QCoreApplication.translate("DialogRapportZ", u"0", None))
        self.label11.setText(QCoreApplication.translate("DialogRapportZ", u"Montant annul\u00e9", None))
        self.value_money2.setText(QCoreApplication.translate("DialogRapportZ", u"0 FC", None))
        self.section_title2.setText(QCoreApplication.translate("DialogRapportZ", u"Contr\u00f4le de caisse", None))
        self.label12.setText(QCoreApplication.translate("DialogRapportZ", u"Montant CA syst\u00e8me", None))
        self.value_money3.setText(QCoreApplication.translate("DialogRapportZ", u"0 FC", None))
        self.label13.setText(QCoreApplication.translate("DialogRapportZ", u"Montant compt\u00e9 en caisse", None))
        self.spin_compte.setSuffix(QCoreApplication.translate("DialogRapportZ", u" FC", None))
        self.ecart_ok.setText(QCoreApplication.translate("DialogRapportZ", u"\u00c9cart : 0 FC", None))
        self.section_title3.setText(QCoreApplication.translate("DialogRapportZ", u"Options", None))
        self.label14.setText(QCoreApplication.translate("DialogRapportZ", u"Format PDF", None))
        self.combo_format.setItemText(0, QCoreApplication.translate("DialogRapportZ", u"Ticket 80mm", None))
        self.combo_format.setItemText(1, QCoreApplication.translate("DialogRapportZ", u"Feuille A4", None))

        self.label15.setText(QCoreApplication.translate("DialogRapportZ", u"Impression", None))
        self.chk_print_auto.setText(QCoreApplication.translate("DialogRapportZ", u"Envoyer automatiquement \u00e0 l'imprimante apr\u00e8s g\u00e9n\u00e9ration", None))
        self.frame.setStyleSheet(QCoreApplication.translate("DialogRapportZ", u"QFrame { background: #ffffff; border-top: 1px solid #e2e8f0; }", None))
        self.btn_secondary.setText(QCoreApplication.translate("DialogRapportZ", u"Fermer", None))
        self.btn_generer.setText(QCoreApplication.translate("DialogRapportZ", u"G\u00e9n\u00e9rer & Imprimer", None))
    # retranslateUi

