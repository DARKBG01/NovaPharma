# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_page_usersxgWLEu.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import Icon_rc

class Ui_PageUsers(object):
    def setupUi(self, PageUsers):
        if not PageUsers.objectName():
            PageUsers.setObjectName(u"PageUsers")
        PageUsers.resize(1200, 800)
        PageUsers.setStyleSheet(u"QWidget#PageUsers { background: #f0f4f8; }\n"
"QWidget#PageUsers QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(PageUsers)
        self.mainLayout.setSpacing(16)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 20)
        self.headerRow = QHBoxLayout()
        self.headerRow.setObjectName(u"headerRow")
        self.headerTitleBox = QVBoxLayout()
        self.headerTitleBox.setSpacing(2)
        self.headerTitleBox.setObjectName(u"headerTitleBox")
        self.lbl_title = QLabel(PageUsers)
        self.lbl_title.setObjectName(u"lbl_title")
        self.lbl_title.setStyleSheet(u"color: #023E8A; font-size: 24px; font-weight: 800; background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_title)

        self.lbl_subtitle = QLabel(PageUsers)
        self.lbl_subtitle.setObjectName(u"lbl_subtitle")
        self.lbl_subtitle.setStyleSheet(u"color: #64748b; font-size: 12px; background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_subtitle)


        self.headerRow.addLayout(self.headerTitleBox)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerRow.addItem(self.headerSpacer)

        self.lbl_count_badge = QLabel(PageUsers)
        self.lbl_count_badge.setObjectName(u"lbl_count_badge")
        self.lbl_count_badge.setStyleSheet(u"background: #dbeafe; color: #1e40af; font-size: 11px; font-weight: 800; padding: 8px 14px; border-radius: 12px; letter-spacing: 1px;")

        self.headerRow.addWidget(self.lbl_count_badge)

        self.btn_new = QPushButton(PageUsers)
        self.btn_new.setObjectName(u"btn_new")
        self.btn_new.setMinimumSize(QSize(0, 44))
        self.btn_new.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_new.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 20px; }\n"
"QPushButton:hover { background: #0077B6; }")
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/plus_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_new.setIcon(icon)
        self.btn_new.setIconSize(QSize(16, 16))

        self.headerRow.addWidget(self.btn_new)


        self.mainLayout.addLayout(self.headerRow)

        self.toolbar = QFrame(PageUsers)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setMinimumSize(QSize(0, 60))
        self.toolbar.setStyleSheet(u"QFrame#toolbar { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }")
        self.toolbarLayout = QHBoxLayout(self.toolbar)
        self.toolbarLayout.setSpacing(12)
        self.toolbarLayout.setObjectName(u"toolbarLayout")
        self.toolbarLayout.setContentsMargins(16, -1, 16, -1)
        self.inp_search = QLineEdit(self.toolbar)
        self.inp_search.setObjectName(u"inp_search")
        self.inp_search.setMinimumSize(QSize(320, 36))
        self.inp_search.setStyleSheet(u"QLineEdit { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; background: #ffffff; }")

        self.toolbarLayout.addWidget(self.inp_search)

        self.combo_filter = QComboBox(self.toolbar)
        self.combo_filter.addItem("")
        self.combo_filter.addItem("")
        self.combo_filter.addItem("")
        self.combo_filter.addItem("")
        self.combo_filter.addItem("")
        self.combo_filter.addItem("")
        self.combo_filter.setObjectName(u"combo_filter")
        self.combo_filter.setMinimumSize(QSize(180, 36))
        self.combo_filter.setStyleSheet(u"QComboBox { background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 6px 12px; font-size: 12px; color: #0f172a; }\n"
"QComboBox::drop-down { border: none; width: 24px; }\n"
"QComboBox QAbstractItemView { background: #ffffff; color: #0f172a; selection-background-color: #e0f2fe; selection-color: #0f172a; }\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}")

        self.toolbarLayout.addWidget(self.combo_filter)

        self.toolbarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbarLayout.addItem(self.toolbarSpacer)

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

        self.users_table = QTableWidget(PageUsers)
        if (self.users_table.columnCount() < 6):
            self.users_table.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.users_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.users_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.users_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.users_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.users_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.users_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.users_table.setObjectName(u"users_table")
        self.users_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.users_table.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; alternate-background-color: #f8fafc; }\n"
"QTableWidget::item { padding: 8px; border-bottom: 1px solid #f1f5f9; }\n"
"QTableWidget::item:selected { background: #e0f2fe; color: #0f172a; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 10px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; letter-spacing: 1px; }")
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.users_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.users_table.setShowGrid(False)

        self.mainLayout.addWidget(self.users_table)

        self.paginationRow = QHBoxLayout()
        self.paginationRow.setObjectName(u"paginationRow")
        self.lbl_total_info = QLabel(PageUsers)
        self.lbl_total_info.setObjectName(u"lbl_total_info")
        self.lbl_total_info.setStyleSheet(u"color: #64748b; font-size: 11px; font-weight: 600; background: transparent;")

        self.paginationRow.addWidget(self.lbl_total_info)

        self.paginationSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.paginationRow.addItem(self.paginationSpacer)

        self.btn_prev = QPushButton(PageUsers)
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

        self.lbl_page_info = QLabel(PageUsers)
        self.lbl_page_info.setObjectName(u"lbl_page_info")
        self.lbl_page_info.setStyleSheet(u"color: #0f172a; font-size: 11px; font-weight: 700; padding: 0 12px; background: transparent;")

        self.paginationRow.addWidget(self.lbl_page_info)

        self.btn_next = QPushButton(PageUsers)
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


        self.retranslateUi(PageUsers)

        QMetaObject.connectSlotsByName(PageUsers)
    # setupUi

    def retranslateUi(self, PageUsers):
        self.lbl_title.setText(QCoreApplication.translate("PageUsers", u"Utilisateurs", None))
        self.lbl_subtitle.setText(QCoreApplication.translate("PageUsers", u"G\u00e9rez les comptes et les permissions de votre \u00e9quipe", None))
        self.lbl_count_badge.setText(QCoreApplication.translate("PageUsers", u"0 utilisateur", None))
        self.btn_new.setText(QCoreApplication.translate("PageUsers", u"Nouvel utilisateur", None))
        self.inp_search.setPlaceholderText(QCoreApplication.translate("PageUsers", u"Rechercher par nom, email, t\u00e9l\u00e9phone\u2026", None))
        self.combo_filter.setItemText(0, QCoreApplication.translate("PageUsers", u"Tous les utilisateurs", None))
        self.combo_filter.setItemText(1, QCoreApplication.translate("PageUsers", u"Actifs", None))
        self.combo_filter.setItemText(2, QCoreApplication.translate("PageUsers", u"Inactifs", None))
        self.combo_filter.setItemText(3, QCoreApplication.translate("PageUsers", u"R\u00f4le : ADMIN", None))
        self.combo_filter.setItemText(4, QCoreApplication.translate("PageUsers", u"R\u00f4le : UTILISATEUR", None))
        self.combo_filter.setItemText(5, QCoreApplication.translate("PageUsers", u"R\u00f4le : CAISSIER", None))

#if QT_CONFIG(tooltip)
        self.btn_refresh.setToolTip(QCoreApplication.translate("PageUsers", u"Rafra\u00eechir", None))
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem = self.users_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageUsers", u"UTILISATEUR", None))
        ___qtablewidgetitem1 = self.users_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageUsers", u"EMAIL", None))
        ___qtablewidgetitem2 = self.users_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageUsers", u"T\u00c9L\u00c9PHONE", None))
        ___qtablewidgetitem3 = self.users_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageUsers", u"R\u00d4LE", None))
        ___qtablewidgetitem4 = self.users_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PageUsers", u"STATUT", None))
        ___qtablewidgetitem5 = self.users_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PageUsers", u"DERNI\u00c8RE CONNEXION", None))
        self.lbl_total_info.setText(QCoreApplication.translate("PageUsers", u"0 utilisateur", None))
        self.btn_prev.setText(QCoreApplication.translate("PageUsers", u"Pr\u00e9c\u00e9dent", None))
        self.lbl_page_info.setText(QCoreApplication.translate("PageUsers", u"Page 1 / 1", None))
        self.btn_next.setText(QCoreApplication.translate("PageUsers", u"Suivant", None))
        pass
    # retranslateUi

