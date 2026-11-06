# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_page_auditQrmIqt.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDateEdit,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import Icon_rc

class Ui_PageAudit(object):
    def setupUi(self, PageAudit):
        if not PageAudit.objectName():
            PageAudit.setObjectName(u"PageAudit")
        PageAudit.resize(1200, 800)
        PageAudit.setStyleSheet(u"QWidget#PageAudit { background: #f0f4f8; }\n"
"QWidget#PageAudit QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(PageAudit)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 20)
        self.headerRow = QHBoxLayout()
        self.headerRow.setObjectName(u"headerRow")
        self.headerTitleBox = QVBoxLayout()
        self.headerTitleBox.setSpacing(2)
        self.headerTitleBox.setObjectName(u"headerTitleBox")
        self.lbl_title = QLabel(PageAudit)
        self.lbl_title.setObjectName(u"lbl_title")
        self.lbl_title.setStyleSheet(u"color: #023E8A; font-size: 24px; font-weight: 800; background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_title)

        self.lbl_subtitle = QLabel(PageAudit)
        self.lbl_subtitle.setObjectName(u"lbl_subtitle")
        self.lbl_subtitle.setStyleSheet(u"color: #64748b; font-size: 12px; background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_subtitle)


        self.headerRow.addLayout(self.headerTitleBox)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerRow.addItem(self.headerSpacer)

        self.lbl_count_badge = QLabel(PageAudit)
        self.lbl_count_badge.setObjectName(u"lbl_count_badge")
        self.lbl_count_badge.setStyleSheet(u"background: #dbeafe; color: #1e40af; font-size: 11px; font-weight: 800; padding: 8px 14px; border-radius: 12px; letter-spacing: 1px;")

        self.headerRow.addWidget(self.lbl_count_badge)

        self.btn_export_csv = QPushButton(PageAudit)
        self.btn_export_csv.setObjectName(u"btn_export_csv")
        self.btn_export_csv.setMinimumSize(QSize(0, 44))
        self.btn_export_csv.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_export_csv.setStyleSheet(u"QPushButton { background: #16A34A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 20px; }\n"
"QPushButton:hover { background: #15803d; }")
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/download.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_export_csv.setIcon(icon)
        self.btn_export_csv.setIconSize(QSize(16, 16))

        self.headerRow.addWidget(self.btn_export_csv)


        self.mainLayout.addLayout(self.headerRow)

        self.toolbar = QFrame(PageAudit)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setMinimumSize(QSize(0, 60))
        self.toolbar.setStyleSheet(u"QFrame#toolbar { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }")
        self.toolbarLayout = QHBoxLayout(self.toolbar)
        self.toolbarLayout.setSpacing(12)
        self.toolbarLayout.setObjectName(u"toolbarLayout")
        self.toolbarLayout.setContentsMargins(16, -1, 16, -1)
        self.inp_search = QLineEdit(self.toolbar)
        self.inp_search.setObjectName(u"inp_search")
        self.inp_search.setMinimumSize(QSize(280, 36))
        self.inp_search.setStyleSheet(u"QLineEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; background: #ffffff; }")

        self.toolbarLayout.addWidget(self.inp_search)

        self.combo_action = QComboBox(self.toolbar)
        self.combo_action.addItem("")
        self.combo_action.setObjectName(u"combo_action")
        self.combo_action.setMinimumSize(QSize(200, 36))
        self.combo_action.setStyleSheet(u"QComboBox { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"QComboBox::drop-down { border: none; width: 24px; }\n"
"QComboBox QAbstractItemView { background: #ffffff; color: #0f172a; selection-background-color: #e0f2fe; selection-color: #0f172a; }")

        self.toolbarLayout.addWidget(self.combo_action)

        self.date_debut = QDateEdit(self.toolbar)
        self.date_debut.setObjectName(u"date_debut")
        self.date_debut.setMinimumSize(QSize(140, 36))
        self.date_debut.setStyleSheet(u"QDateEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"\n"
"QDateEdit::drop-down { border: none; width: 26px; }\n"
"QDateEdit::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}")
        self.date_debut.setCalendarPopup(True)

        self.toolbarLayout.addWidget(self.date_debut)

        self.lbl_to = QLabel(self.toolbar)
        self.lbl_to.setObjectName(u"lbl_to")
        self.lbl_to.setStyleSheet(u"color: #94a3b8; font-size: 12px; background: transparent;")

        self.toolbarLayout.addWidget(self.lbl_to)

        self.date_fin = QDateEdit(self.toolbar)
        self.date_fin.setObjectName(u"date_fin")
        self.date_fin.setMinimumSize(QSize(140, 36))
        self.date_fin.setStyleSheet(u"QDateEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"\n"
"QDateEdit::drop-down { border: none; width: 26px; }\n"
"QDateEdit::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}")
        self.date_fin.setCalendarPopup(True)

        self.toolbarLayout.addWidget(self.date_fin)

        self.toolbarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbarLayout.addItem(self.toolbarSpacer)

        self.btn_reset_filters = QPushButton(self.toolbar)
        self.btn_reset_filters.setObjectName(u"btn_reset_filters")
        self.btn_reset_filters.setMinimumSize(QSize(0, 36))
        self.btn_reset_filters.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_reset_filters.setStyleSheet(u"QPushButton { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 0 14px; }\n"
"QPushButton:hover { background: #e2e8f0; }")

        self.toolbarLayout.addWidget(self.btn_reset_filters)

        self.btn_refresh = QPushButton(self.toolbar)
        self.btn_refresh.setObjectName(u"btn_refresh")
        self.btn_refresh.setMinimumSize(QSize(36, 36))
        self.btn_refresh.setMaximumSize(QSize(36, 36))
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_refresh.setStyleSheet(u"QPushButton { background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 8px; }\n"
"QPushButton:hover { background: #e2e8f0; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/refresh.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_refresh.setIcon(icon1)
        self.btn_refresh.setIconSize(QSize(16, 16))

        self.toolbarLayout.addWidget(self.btn_refresh)


        self.mainLayout.addWidget(self.toolbar)

        self.audit_table = QTableWidget(PageAudit)
        if (self.audit_table.columnCount() < 5):
            self.audit_table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.audit_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.audit_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.audit_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.audit_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.audit_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.audit_table.setObjectName(u"audit_table")
        self.audit_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.audit_table.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; alternate-background-color: #f8fafc; }\n"
"QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }\n"
"QTableWidget::item:selected { background: #e0f2fe; color: #0f172a; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 10px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.audit_table.setAlternatingRowColors(True)
        self.audit_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.audit_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.audit_table.setShowGrid(False)

        self.mainLayout.addWidget(self.audit_table)

        self.paginationRow = QHBoxLayout()
        self.paginationRow.setObjectName(u"paginationRow")
        self.lbl_total_info = QLabel(PageAudit)
        self.lbl_total_info.setObjectName(u"lbl_total_info")
        self.lbl_total_info.setStyleSheet(u"color: #64748b; font-size: 11px; font-weight: 600; background: transparent;")

        self.paginationRow.addWidget(self.lbl_total_info)

        self.lbl_hint = QLabel(PageAudit)
        self.lbl_hint.setObjectName(u"lbl_hint")
        self.lbl_hint.setStyleSheet(u"color: #94a3b8; font-size: 11px; font-style: italic; padding-left: 12px; background: transparent;")

        self.paginationRow.addWidget(self.lbl_hint)

        self.paginationSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.paginationRow.addItem(self.paginationSpacer)

        self.btn_prev = QPushButton(PageAudit)
        self.btn_prev.setObjectName(u"btn_prev")
        self.btn_prev.setMinimumSize(QSize(0, 34))
        self.btn_prev.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_prev.setStyleSheet(u"QPushButton { background: #ffffff; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 0 12px; }\n"
"QPushButton:hover { background: #f1f5f9; }\n"
"QPushButton:disabled { color: #cbd5e1; }")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/chevron-left.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_prev.setIcon(icon2)
        self.btn_prev.setIconSize(QSize(14, 14))

        self.paginationRow.addWidget(self.btn_prev)

        self.lbl_page_info = QLabel(PageAudit)
        self.lbl_page_info.setObjectName(u"lbl_page_info")
        self.lbl_page_info.setStyleSheet(u"color: #0f172a; font-size: 11px; font-weight: 700; padding: 0 12px; background: transparent;")

        self.paginationRow.addWidget(self.lbl_page_info)

        self.btn_next = QPushButton(PageAudit)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setMinimumSize(QSize(0, 34))
        self.btn_next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_next.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.btn_next.setStyleSheet(u"QPushButton { background: #ffffff; color: #475569; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 11px; font-weight: 700; padding: 0 12px; }\n"
"QPushButton:hover { background: #f1f5f9; }\n"
"QPushButton:disabled { color: #cbd5e1; }")
        icon3 = QIcon()
        icon3.addFile(u":/Icon/Icons/chevron-right.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_next.setIcon(icon3)
        self.btn_next.setIconSize(QSize(14, 14))

        self.paginationRow.addWidget(self.btn_next)


        self.mainLayout.addLayout(self.paginationRow)


        self.retranslateUi(PageAudit)

        QMetaObject.connectSlotsByName(PageAudit)
    # setupUi

    def retranslateUi(self, PageAudit):
        self.lbl_title.setText(QCoreApplication.translate("PageAudit", u"Journal d'audit", None))
        self.lbl_subtitle.setText(QCoreApplication.translate("PageAudit", u"Historique des actions sensibles effectu\u00e9es dans l'application", None))
        self.lbl_count_badge.setText(QCoreApplication.translate("PageAudit", u"0 entr\u00e9e", None))
        self.btn_export_csv.setText(QCoreApplication.translate("PageAudit", u"Exporter CSV", None))
        self.inp_search.setPlaceholderText(QCoreApplication.translate("PageAudit", u"Rechercher par utilisateur, cible, action\u2026", None))
        self.combo_action.setItemText(0, QCoreApplication.translate("PageAudit", u"Toutes les actions", None))

        self.date_debut.setDisplayFormat(QCoreApplication.translate("PageAudit", u"dd/MM/yyyy", None))
        self.lbl_to.setText(QCoreApplication.translate("PageAudit", u"\u00e0", None))
        self.date_fin.setDisplayFormat(QCoreApplication.translate("PageAudit", u"dd/MM/yyyy", None))
        self.btn_reset_filters.setText(QCoreApplication.translate("PageAudit", u"R\u00e9initialiser", None))
#if QT_CONFIG(tooltip)
        self.btn_refresh.setToolTip(QCoreApplication.translate("PageAudit", u"Rafra\u00eechir", None))
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem = self.audit_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageAudit", u"DATE", None))
        ___qtablewidgetitem1 = self.audit_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageAudit", u"UTILISATEUR", None))
        ___qtablewidgetitem2 = self.audit_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageAudit", u"ACTION", None))
        ___qtablewidgetitem3 = self.audit_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageAudit", u"CIBLE", None))
        ___qtablewidgetitem4 = self.audit_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PageAudit", u"MACHINE", None))
        self.lbl_total_info.setText(QCoreApplication.translate("PageAudit", u"0 entr\u00e9e", None))
        self.lbl_hint.setText(QCoreApplication.translate("PageAudit", u"Double-cliquez sur une ligne pour voir les d\u00e9tails", None))
        self.btn_prev.setText(QCoreApplication.translate("PageAudit", u"Pr\u00e9c\u00e9dent", None))
        self.lbl_page_info.setText(QCoreApplication.translate("PageAudit", u"Page 1 / 1", None))
        self.btn_next.setText(QCoreApplication.translate("PageAudit", u"Suivant", None))
        pass
    # retranslateUi

