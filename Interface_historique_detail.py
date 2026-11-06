# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_historique_detailjzpPHE.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(760, 649)
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
        icon.addFile(u":/Icon/Icons/invoice_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        self.bodyLayout.setSpacing(12)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(24, 20, 24, 20)
        self.info_card = QFrame(Dialog)
        self.info_card.setObjectName(u"info_card")
        self.info_card.setStyleSheet(u"QFrame#info_card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }\n"
"QFrame#info_card QLabel { background: transparent; }")
        self.infoGrid = QGridLayout(self.info_card)
        self.infoGrid.setObjectName(u"infoGrid")
        self.infoGrid.setHorizontalSpacing(24)
        self.infoGrid.setVerticalSpacing(12)
        self.infoGrid.setContentsMargins(20, 20, 20, 20)
        self.lbl_k_fact = QLabel(self.info_card)
        self.lbl_k_fact.setObjectName(u"lbl_k_fact")
        self.lbl_k_fact.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_fact, 0, 0, 1, 1)

        self.val_fact = QLabel(self.info_card)
        self.val_fact.setObjectName(u"val_fact")
        self.val_fact.setStyleSheet(u"color: #023E8A; font-size: 13px; font-weight: 800; font-family: 'Courier New';")

        self.infoGrid.addWidget(self.val_fact, 0, 1, 1, 1)

        self.lbl_k_date = QLabel(self.info_card)
        self.lbl_k_date.setObjectName(u"lbl_k_date")
        self.lbl_k_date.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_date, 1, 0, 1, 1)

        self.val_date = QLabel(self.info_card)
        self.val_date.setObjectName(u"val_date")
        self.val_date.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_date, 1, 1, 1, 1)

        self.lbl_k_client = QLabel(self.info_card)
        self.lbl_k_client.setObjectName(u"lbl_k_client")
        self.lbl_k_client.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_client, 2, 0, 1, 1)

        self.val_client = QLabel(self.info_card)
        self.val_client.setObjectName(u"val_client")
        self.val_client.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_client, 2, 1, 1, 1)

        self.lbl_k_caissier = QLabel(self.info_card)
        self.lbl_k_caissier.setObjectName(u"lbl_k_caissier")
        self.lbl_k_caissier.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_caissier, 3, 0, 1, 1)

        self.val_caissier = QLabel(self.info_card)
        self.val_caissier.setObjectName(u"val_caissier")
        self.val_caissier.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_caissier, 3, 1, 1, 1)

        self.lbl_k_statut = QLabel(self.info_card)
        self.lbl_k_statut.setObjectName(u"lbl_k_statut")
        self.lbl_k_statut.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_statut, 4, 0, 1, 1)

        self.val_statut = QLabel(self.info_card)
        self.val_statut.setObjectName(u"val_statut")
        self.val_statut.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_statut, 4, 1, 1, 1)


        self.bodyLayout.addWidget(self.info_card)

        self.lbl_lignes_titre = QLabel(Dialog)
        self.lbl_lignes_titre.setObjectName(u"lbl_lignes_titre")
        self.lbl_lignes_titre.setStyleSheet(u"color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent;")

        self.bodyLayout.addWidget(self.lbl_lignes_titre)

        self.table_lignes = QTableWidget(Dialog)
        if (self.table_lignes.columnCount() < 4):
            self.table_lignes.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table_lignes.setObjectName(u"table_lignes")
        self.table_lignes.setMinimumSize(QSize(0, 200))
        self.table_lignes.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 6px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_lignes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_lignes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_lignes.setShowGrid(False)

        self.bodyLayout.addWidget(self.table_lignes)

        self.totalRow = QHBoxLayout()
        self.totalRow.setObjectName(u"totalRow")
        self.totalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.totalRow.addItem(self.totalSpacer)

        self.lbl_total_label = QLabel(Dialog)
        self.lbl_total_label.setObjectName(u"lbl_total_label")
        self.lbl_total_label.setStyleSheet(u"color: #475569; font-size: 12px; font-weight: 800; letter-spacing: 1px; background: transparent;")

        self.totalRow.addWidget(self.lbl_total_label)

        self.lbl_total_value = QLabel(Dialog)
        self.lbl_total_value.setObjectName(u"lbl_total_value")
        self.lbl_total_value.setStyleSheet(u"color: #16A34A; font-size: 22px; font-weight: 800; background: transparent;")

        self.totalRow.addWidget(self.lbl_total_value)


        self.bodyLayout.addLayout(self.totalRow)

        self.lbl_motif_annul = QLabel(Dialog)
        self.lbl_motif_annul.setObjectName(u"lbl_motif_annul")
        self.lbl_motif_annul.setVisible(False)
        self.lbl_motif_annul.setStyleSheet(u"color: #b91c1c; font-size: 11px; font-weight: 600; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 8px 12px;")
        self.lbl_motif_annul.setWordWrap(True)

        self.bodyLayout.addWidget(self.lbl_motif_annul)


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

        self.btn_close = QPushButton(self.footer)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMinimumSize(QSize(0, 42))
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 24px; }\n"
"QPushButton:hover { background: #0077B6; }")

        self.footerLayout.addWidget(self.btn_close)

        self.btn_reprint = QPushButton(self.footer)
        self.btn_reprint.setObjectName(u"btn_reprint")
        self.btn_reprint.setMinimumSize(QSize(0, 42))
        self.btn_reprint.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_reprint.setStyleSheet(u"QPushButton {\n"
"    background: #eff6ff;\n"
"    color: #023E8A;\n"
"    border: 1.5px solid #bfdbfe;\n"
"    border-radius: 10px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    padding: 0 18px;\n"
"}\n"
"QPushButton:hover { background: #dbeafe; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/printer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_reprint.setIcon(icon1)
        self.btn_reprint.setIconSize(QSize(16, 16))

        self.footerLayout.addWidget(self.btn_reprint)

        self.btn_cancel_sale = QPushButton(self.footer)
        self.btn_cancel_sale.setObjectName(u"btn_cancel_sale")
        self.btn_cancel_sale.setMinimumSize(QSize(0, 42))
        self.btn_cancel_sale.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cancel_sale.setStyleSheet(u"QPushButton {\n"
"    background: #fef2f2;\n"
"    color: #b91c1c;\n"
"    border: 1.5px solid #fecaca;\n"
"    border-radius: 10px;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"    padding: 0 20px;\n"
"}\n"
"QPushButton:hover { background: #fee2e2; }")

        self.footerLayout.addWidget(self.btn_cancel_sale)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"D\u00e9tail facture \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("Dialog", u"Facture", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_fact.setText(QCoreApplication.translate("Dialog", u"N\u00b0 FACTURE", None))
        self.val_fact.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_date.setText(QCoreApplication.translate("Dialog", u"DATE", None))
        self.val_date.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_client.setText(QCoreApplication.translate("Dialog", u"CLIENT", None))
        self.val_client.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_caissier.setText(QCoreApplication.translate("Dialog", u"CAISSIER", None))
        self.val_caissier.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_statut.setText(QCoreApplication.translate("Dialog", u"STATUT", None))
        self.val_statut.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_lignes_titre.setText(QCoreApplication.translate("Dialog", u"ARTICLES", None))
        ___qtablewidgetitem = self.table_lignes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"ARTICLE", None))
        ___qtablewidgetitem1 = self.table_lignes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"QT\u00c9", None))
        ___qtablewidgetitem2 = self.table_lignes.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"P.U", None))
        ___qtablewidgetitem3 = self.table_lignes.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"TOTAL", None))
        self.lbl_total_label.setText(QCoreApplication.translate("Dialog", u"TOTAL G\u00c9N\u00c9RAL", None))
        self.lbl_total_value.setText(QCoreApplication.translate("Dialog", u"0 FC", None))
        self.lbl_motif_annul.setText("")
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
        self.btn_reprint.setText(QCoreApplication.translate("Dialog", u"  R\u00e9imprimer", None))
        self.btn_cancel_sale.setText(QCoreApplication.translate("Dialog", u"Annuler la vente", None))
    # retranslateUi

