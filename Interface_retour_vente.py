# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_retour_venteqSgbsb.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QPlainTextEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_DialogRetourVente(object):
    def setupUi(self, DialogRetourVente):
        if not DialogRetourVente.objectName():
            DialogRetourVente.setObjectName(u"DialogRetourVente")
        DialogRetourVente.resize(900, 907)
        DialogRetourVente.setMinimumSize(QSize(900, 720))
        DialogRetourVente.setStyleSheet(u"\n"
"    QDialog { background: #f0f4f8; }\n"
"    QFrame#header { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,\n"
"        stop:0 #991b1b, stop:1 #dc2626); border-top-left-radius:14px;\n"
"        border-top-right-radius:14px; }\n"
"    QLabel#header_title { color: white; font-size: 18px; font-weight: 800; }\n"
"    QLabel#header_sub { color: #fecaca; font-size: 11px; }\n"
"    QFrame#card { background: white; border: 1px solid #e2e8f0;\n"
"        border-radius: 12px; }\n"
"    QLabel { color: #334155; font-size: 13px; background: transparent; }\n"
"    QLabel#section_title { color: #991b1b; font-size: 13px;\n"
"        font-weight: 800; }\n"
"    QTableWidget { background: white; border: 1px solid #e2e8f0;\n"
"        border-radius: 10px; gridline-color: #f1f5f9; }\n"
"    QHeaderView::section { background: #f8fafc; color: #64748b;\n"
"        font-weight: 700; padding: 10px; border: none;\n"
"        border-bottom: 1px solid #e2e8f0; }\n"
"    QComboBox, QLineEdit, QPlainTextEdit { background: #f8fafc;\n"
""
                        "        border: 1.5px solid #e2e8f0; border-radius: 10px;\n"
"        padding: 8px 12px; font-size: 13px; color: #0f172a; }\n"
"    QComboBox:focus, QLineEdit:focus, QPlainTextEdit:focus {\n"
"        background: white; border-color: #dc2626; }\n"
"    QPushButton#btn_primary { background: qlineargradient(x1:0,y1:0,x2:0,y2:1,\n"
"        stop:0 #dc2626, stop:1 #991b1b); color: white; border: none;\n"
"        border-radius: 10px; padding: 10px 24px; font-weight: 800;\n"
"        font-size: 13px; min-width: 150px; }\n"
"    QPushButton#btn_primary:hover { background: #991b1b; }\n"
"    QPushButton#btn_secondary { background: transparent;\n"
"        color: #64748b; border: 1.5px solid #e2e8f0;\n"
"        border-radius: 10px; padding: 10px 24px; font-weight: 700; }\n"
"  ")
        self.root = QVBoxLayout(DialogRetourVente)
        self.root.setSpacing(0)
        self.root.setObjectName(u"root")
        self.root.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(DialogRetourVente)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 80))
        self.hboxLayout = QHBoxLayout(self.header)
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.hboxLayout.setContentsMargins(24, 16, 24, 16)
        self.header_icon = QLabel(self.header)
        self.header_icon.setObjectName(u"header_icon")
        self.header_icon.setMinimumSize(QSize(40, 40))
        self.header_icon.setMaximumSize(QSize(40, 40))
        self.header_icon.setPixmap(QPixmap(u":/Icon/Icons/arrow-left_white.svg"))
        self.header_icon.setScaledContents(True)

        self.hboxLayout.addWidget(self.header_icon)

        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.setSpacing(2)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.header_title = QLabel(self.header)
        self.header_title.setObjectName(u"header_title")

        self.vboxLayout.addWidget(self.header_title)

        self.header_sub = QLabel(self.header)
        self.header_sub.setObjectName(u"header_sub")

        self.vboxLayout.addWidget(self.header_sub)


        self.hboxLayout.addLayout(self.vboxLayout)


        self.root.addWidget(self.header)

        self.scrollArea = QScrollArea(DialogRetourVente)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName(u"scroll_content")
        self.scroll_content.setGeometry(QRect(0, 0, 900, 757))
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setSpacing(14)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.card = QFrame(self.scroll_content)
        self.card.setObjectName(u"card")
        self.vboxLayout1 = QVBoxLayout(self.card)
        self.vboxLayout1.setObjectName(u"vboxLayout1")
        self.vboxLayout1.setContentsMargins(20, 16, 20, 16)
        self.section_title = QLabel(self.card)
        self.section_title.setObjectName(u"section_title")

        self.vboxLayout1.addWidget(self.section_title)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(10)
        self.label = QLabel(self.card)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.lbl_num_fact = QLabel(self.card)
        self.lbl_num_fact.setObjectName(u"lbl_num_fact")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lbl_num_fact)

        self.label1 = QLabel(self.card)
        self.label1.setObjectName(u"label1")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label1)

        self.lbl_date = QLabel(self.card)
        self.lbl_date.setObjectName(u"lbl_date")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lbl_date)

        self.label2 = QLabel(self.card)
        self.label2.setObjectName(u"label2")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label2)

        self.lbl_client = QLabel(self.card)
        self.lbl_client.setObjectName(u"lbl_client")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lbl_client)

        self.label3 = QLabel(self.card)
        self.label3.setObjectName(u"label3")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label3)

        self.lbl_montant_initial = QLabel(self.card)
        self.lbl_montant_initial.setObjectName(u"lbl_montant_initial")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lbl_montant_initial)


        self.vboxLayout1.addLayout(self.formLayout)


        self.content_layout.addWidget(self.card)

        self.card1 = QFrame(self.scroll_content)
        self.card1.setObjectName(u"card1")
        self.vboxLayout2 = QVBoxLayout(self.card1)
        self.vboxLayout2.setObjectName(u"vboxLayout2")
        self.vboxLayout2.setContentsMargins(20, 16, 20, 16)
        self.section_title1 = QLabel(self.card1)
        self.section_title1.setObjectName(u"section_title1")

        self.vboxLayout2.addWidget(self.section_title1)

        self.table_lignes = QTableWidget(self.card1)
        if (self.table_lignes.columnCount() < 6):
            self.table_lignes.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.table_lignes.setObjectName(u"table_lignes")
        self.table_lignes.setColumnCount(6)

        self.vboxLayout2.addWidget(self.table_lignes)


        self.content_layout.addWidget(self.card1)

        self.card2 = QFrame(self.scroll_content)
        self.card2.setObjectName(u"card2")
        self.vboxLayout3 = QVBoxLayout(self.card2)
        self.vboxLayout3.setObjectName(u"vboxLayout3")
        self.vboxLayout3.setContentsMargins(20, 16, 20, 16)
        self.section_title2 = QLabel(self.card2)
        self.section_title2.setObjectName(u"section_title2")

        self.vboxLayout3.addWidget(self.section_title2)

        self.formLayout1 = QFormLayout()
        self.formLayout1.setObjectName(u"formLayout1")
        self.formLayout1.setHorizontalSpacing(10)
        self.formLayout1.setVerticalSpacing(10)
        self.label4 = QLabel(self.card2)
        self.label4.setObjectName(u"label4")

        self.formLayout1.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label4)

        self.combo_motif = QComboBox(self.card2)
        self.combo_motif.addItem("")
        self.combo_motif.addItem("")
        self.combo_motif.addItem("")
        self.combo_motif.addItem("")
        self.combo_motif.addItem("")
        self.combo_motif.addItem("")
        self.combo_motif.setObjectName(u"combo_motif")

        self.formLayout1.setWidget(0, QFormLayout.ItemRole.FieldRole, self.combo_motif)

        self.label5 = QLabel(self.card2)
        self.label5.setObjectName(u"label5")

        self.formLayout1.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label5)

        self.txt_notes = QPlainTextEdit(self.card2)
        self.txt_notes.setObjectName(u"txt_notes")

        self.formLayout1.setWidget(1, QFormLayout.ItemRole.FieldRole, self.txt_notes)


        self.vboxLayout3.addLayout(self.formLayout1)


        self.content_layout.addWidget(self.card2)

        self.card3 = QFrame(self.scroll_content)
        self.card3.setObjectName(u"card3")
        self.hboxLayout1 = QHBoxLayout(self.card3)
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.hboxLayout1.setContentsMargins(20, 16, 20, 16)
        self.label6 = QLabel(self.card3)
        self.label6.setObjectName(u"label6")

        self.hboxLayout1.addWidget(self.label6)

        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout1.addItem(self.spacerItem)

        self.lbl_total = QLabel(self.card3)
        self.lbl_total.setObjectName(u"lbl_total")

        self.hboxLayout1.addWidget(self.lbl_total)


        self.content_layout.addWidget(self.card3)

        self.scrollArea.setWidget(self.scroll_content)

        self.root.addWidget(self.scrollArea)

        self.frame = QFrame(DialogRetourVente)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 70))
        self.hboxLayout2 = QHBoxLayout(self.frame)
        self.hboxLayout2.setObjectName(u"hboxLayout2")
        self.hboxLayout2.setContentsMargins(20, -1, 20, -1)
        self.spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout2.addItem(self.spacerItem1)

        self.btn_secondary = QPushButton(self.frame)
        self.btn_secondary.setObjectName(u"btn_secondary")

        self.hboxLayout2.addWidget(self.btn_secondary)

        self.btn_primary = QPushButton(self.frame)
        self.btn_primary.setObjectName(u"btn_primary")

        self.hboxLayout2.addWidget(self.btn_primary)


        self.root.addWidget(self.frame)


        self.retranslateUi(DialogRetourVente)

        QMetaObject.connectSlotsByName(DialogRetourVente)
    # setupUi

    def retranslateUi(self, DialogRetourVente):
        DialogRetourVente.setWindowTitle(QCoreApplication.translate("DialogRetourVente", u"Retour de vente", None))
        self.header_title.setText(QCoreApplication.translate("DialogRetourVente", u"Retour de vente / Avoir", None))
        self.header_sub.setText(QCoreApplication.translate("DialogRetourVente", u"Facture d'origine : \u2014", None))
        self.scroll_content.setStyleSheet(QCoreApplication.translate("DialogRetourVente", u"background: transparent;", None))
        self.section_title.setText(QCoreApplication.translate("DialogRetourVente", u"Informations", None))
        self.label.setText(QCoreApplication.translate("DialogRetourVente", u"Num\u00e9ro facture", None))
        self.lbl_num_fact.setStyleSheet(QCoreApplication.translate("DialogRetourVente", u"font-weight: 800; color: #023E8A;", None))
        self.lbl_num_fact.setText(QCoreApplication.translate("DialogRetourVente", u"\u2014", None))
        self.label1.setText(QCoreApplication.translate("DialogRetourVente", u"Date", None))
        self.lbl_date.setText(QCoreApplication.translate("DialogRetourVente", u"\u2014", None))
        self.label2.setText(QCoreApplication.translate("DialogRetourVente", u"Client", None))
        self.lbl_client.setText(QCoreApplication.translate("DialogRetourVente", u"\u2014", None))
        self.label3.setText(QCoreApplication.translate("DialogRetourVente", u"Montant initial", None))
        self.lbl_montant_initial.setStyleSheet(QCoreApplication.translate("DialogRetourVente", u"font-weight: 800; color: #16A34A;", None))
        self.lbl_montant_initial.setText(QCoreApplication.translate("DialogRetourVente", u"\u2014", None))
        self.section_title1.setText(QCoreApplication.translate("DialogRetourVente", u"Articles \u00e0 retourner", None))
        ___qtablewidgetitem = self.table_lignes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DialogRetourVente", u"Retour ?", None))
        ___qtablewidgetitem1 = self.table_lignes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DialogRetourVente", u"Article", None))
        ___qtablewidgetitem2 = self.table_lignes.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DialogRetourVente", u"Qt\u00e9 factur\u00e9e", None))
        ___qtablewidgetitem3 = self.table_lignes.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("DialogRetourVente", u"Qt\u00e9 retour", None))
        ___qtablewidgetitem4 = self.table_lignes.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("DialogRetourVente", u"P.U.", None))
        ___qtablewidgetitem5 = self.table_lignes.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("DialogRetourVente", u"Total", None))
        self.section_title2.setText(QCoreApplication.translate("DialogRetourVente", u"Motif du retour", None))
        self.label4.setText(QCoreApplication.translate("DialogRetourVente", u"Motif", None))
        self.combo_motif.setItemText(0, QCoreApplication.translate("DialogRetourVente", u"Erreur de saisie", None))
        self.combo_motif.setItemText(1, QCoreApplication.translate("DialogRetourVente", u"Client s'est ravis\u00e9", None))
        self.combo_motif.setItemText(2, QCoreApplication.translate("DialogRetourVente", u"Produit d\u00e9fectueux", None))
        self.combo_motif.setItemText(3, QCoreApplication.translate("DialogRetourVente", u"Doublon", None))
        self.combo_motif.setItemText(4, QCoreApplication.translate("DialogRetourVente", u"Prix incorrect", None))
        self.combo_motif.setItemText(5, QCoreApplication.translate("DialogRetourVente", u"Autre", None))

        self.label5.setText(QCoreApplication.translate("DialogRetourVente", u"Notes", None))
        self.label6.setStyleSheet(QCoreApplication.translate("DialogRetourVente", u"font-size: 14px; font-weight: 700;", None))
        self.label6.setText(QCoreApplication.translate("DialogRetourVente", u"Montant \u00e0 rembourser :", None))
        self.lbl_total.setStyleSheet(QCoreApplication.translate("DialogRetourVente", u"font-size: 22px; font-weight: 800; color: #dc2626;", None))
        self.lbl_total.setText(QCoreApplication.translate("DialogRetourVente", u"0 FC", None))
        self.frame.setStyleSheet(QCoreApplication.translate("DialogRetourVente", u"QFrame { background: white; border-top: 1px solid #e2e8f0; }", None))
        self.btn_secondary.setText(QCoreApplication.translate("DialogRetourVente", u"Annuler", None))
        self.btn_primary.setText(QCoreApplication.translate("DialogRetourVente", u"Valider le retour", None))
    # retranslateUi

