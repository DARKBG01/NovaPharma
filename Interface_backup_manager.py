# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_backup_managerKlpTwF.ui'
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
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QToolButton, QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(860, 620)
        Dialog.setMinimumSize(QSize(720, 520))
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
        icon.addFile(u":/Icon/Icons/package_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
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
        self.bodyLayout.setSpacing(14)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(24, 20, 24, 20)
        self.statsRow = QHBoxLayout()
        self.statsRow.setSpacing(12)
        self.statsRow.setObjectName(u"statsRow")
        self.lbl_stats = QLabel(Dialog)
        self.lbl_stats.setObjectName(u"lbl_stats")
        self.lbl_stats.setStyleSheet(u"color: #475569; font-size: 12px; font-weight: 700; background: transparent;")

        self.statsRow.addWidget(self.lbl_stats)

        self.statsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.statsRow.addItem(self.statsSpacer)

        self.btn_new_backup = QPushButton(Dialog)
        self.btn_new_backup.setObjectName(u"btn_new_backup")
        self.btn_new_backup.setMinimumSize(QSize(0, 38))
        self.btn_new_backup.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_new_backup.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 18px; }\n"
"QPushButton:hover { background: #0077B6; }")

        self.statsRow.addWidget(self.btn_new_backup)


        self.bodyLayout.addLayout(self.statsRow)

        self.table_backups = QTableWidget(Dialog)
        if (self.table_backups.columnCount() < 4):
            self.table_backups.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_backups.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_backups.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_backups.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_backups.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table_backups.setObjectName(u"table_backups")
        self.table_backups.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; alternate-background-color: #f8fafc; }\n"
"QTableWidget::item { padding: 10px; border-bottom: 1px solid #f1f5f9; }\n"
"QTableWidget::item:selected { background: #e0f2fe; color: #0f172a; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 10px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.table_backups.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_backups.setAlternatingRowColors(True)
        self.table_backups.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_backups.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_backups.setShowGrid(False)

        self.bodyLayout.addWidget(self.table_backups)

        self.actionsRow = QHBoxLayout()
        self.actionsRow.setSpacing(10)
        self.actionsRow.setObjectName(u"actionsRow")
        self.actionsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.actionsRow.addItem(self.actionsSpacer)

        self.btn_delete = QPushButton(Dialog)
        self.btn_delete.setObjectName(u"btn_delete")
        self.btn_delete.setEnabled(False)
        self.btn_delete.setMinimumSize(QSize(0, 38))
        self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_delete.setStyleSheet(u"QPushButton { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 18px; }\n"
"QPushButton:hover:enabled { background: #fee2e2; }\n"
"QPushButton:disabled { background: #f8fafc; color: #cbd5e1; border-color: #e2e8f0; }")

        self.actionsRow.addWidget(self.btn_delete)

        self.btn_view = QPushButton(Dialog)
        self.btn_view.setObjectName(u"btn_view")
        self.btn_view.setEnabled(False)
        self.btn_view.setMinimumSize(QSize(0, 38))
        self.btn_view.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_view.setStyleSheet(u"QPushButton { background: #eff6ff; color: #023E8A; border: 1.5px solid #bfdbfe; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 18px; }\n"
"QPushButton:hover:enabled { background: #dbeafe; }\n"
"QPushButton:disabled { background: #f8fafc; color: #cbd5e1; border-color: #e2e8f0; }")

        self.actionsRow.addWidget(self.btn_view)


        self.bodyLayout.addLayout(self.actionsRow)


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
        self.btn_close.setStyleSheet(u"QPushButton { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 24px; }\n"
"QPushButton:hover { background: #e2e8f0; }")

        self.footerLayout.addWidget(self.btn_close)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Historique des sauvegardes \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("Dialog", u"Historique des sauvegardes", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("Dialog", u"Consultez et g\u00e9rez les archives disponibles", None))
        self.lbl_stats.setText(QCoreApplication.translate("Dialog", u"\u2014 archives \u2022 \u2014 total", None))
        self.btn_new_backup.setText(QCoreApplication.translate("Dialog", u"Cr\u00e9er une sauvegarde maintenant", None))
        ___qtablewidgetitem = self.table_backups.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"FICHIER", None))
        ___qtablewidgetitem1 = self.table_backups.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"TYPE", None))
        ___qtablewidgetitem2 = self.table_backups.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"DATE", None))
        ___qtablewidgetitem3 = self.table_backups.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"TAILLE", None))
        self.btn_delete.setText(QCoreApplication.translate("Dialog", u"Supprimer", None))
        self.btn_view.setText(QCoreApplication.translate("Dialog", u"Ouvrir en lecture seule", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
    # retranslateUi

