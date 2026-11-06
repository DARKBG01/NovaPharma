# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_clientiPPnKB.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import Icon_rc

class Ui_PageClients(object):
    def setupUi(self, PageClients):
        if not PageClients.objectName():
            PageClients.setObjectName(u"PageClients")
        PageClients.resize(858, 763)
        PageClients.setStyleSheet(u"/* ============================================================\n"
"   NOVA PHARMA \u2014 PAGE CLIENTS (table performante)\n"
"   ============================================================ */\n"
"\n"
"QWidget#PageClients { background-color: transparent; }\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 CARTE PRINCIPALE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#card {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 HEADER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QLabel#page_title {\n"
"    color: #0f172a;\n"
"    font-size: 20px;\n"
"    font-weight: 800;\n"
"    letter-spacing: -0.3px;\n"
"    background: transparent;\n"
"}\n"
"QLabel#page_subtitle {\n"
"    color: #64748b;\n"
"    font-size: 12px;\n"
""
                        "    background: transparent;\n"
"}\n"
"QLabel#count_badge {\n"
"    color: #0077B6;\n"
"    font-size: 11px;\n"
"    font-weight: 800;\n"
"    background-color: #e0f7fa;\n"
"    border: 1px solid #bae6fd;\n"
"    border-radius: 10px;\n"
"    padding: 4px 10px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 RECHERCHE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QLineEdit#search_input {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #94a3b8;\n"
"    border-radius: 11px;\n"
"    padding: 10px 14px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    selection-background-color: #bfdbfe;\n"
"}\n"
"QLineEdit#search_input:hover {\n"
"    border-color: #64748b;\n"
"    background-color: #ffffff;\n"
"}\n"
"QLineEdit#search_input:focus {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #0077B6;\n"
"    box-shadow: 0 0 0 3px rgba(0, 119, 182, 0.1);\n"
"}\n"
"QLine"
                        "Edit#search_input::placeholder {\n"
"    color: #94a3b8;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 COMBO FILTRE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QComboBox#filter_combo {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 10px 14px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"    min-width: 160px;\n"
"}\n"
"QComboBox#filter_combo:hover { border-color: #b9c6d8; }\n"
"QComboBox#filter_combo:focus { border-color: #0077B6; }\n"
"QComboBox#filter_combo::drop-down { border: none; width: 26px; }\n"
"QComboBox#filter_combo::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}\n"
"QComboBox#filter_combo QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    s"
                        "election-background-color: #eff6ff;\n"
"    selection-color: #0077B6;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 BOUTONS \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QPushButton#btn_new {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 11px;\n"
"    padding: 11px 22px;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    min-height: 42px;\n"
"    letter-spacing: 0.2px;\n"
"}\n"
"QPushButton#btn_new:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"QPushButton#btn_new:pressed { background: #023E8A; }\n"
"\n"
"QPushButton#btn_refresh {\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 11px 16px;\n"
"    font-size: 1"
                        "3px;\n"
"    font-weight: 600;\n"
"    min-width: 44px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_refresh:hover {\n"
"    background-color: #f8fafc;\n"
"    border-color: #c3cedd;\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"/* Boutons d'action s\u00e9lection */\n"
"QPushButton#btn_view {\n"
"    background-color: #eff6ff;\n"
"    color: #0077B6;\n"
"    border: 1px solid #dbeafe;\n"
"    border-radius: 11px;\n"
"    padding: 9px 18px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 38px;\n"
"}\n"
"QPushButton#btn_view:hover { background-color: #dbeafe; }\n"
"QPushButton#btn_view:disabled {\n"
"    background-color: #f8fafc;\n"
"    color: #cbd5e1;\n"
"    border-color: #e6ebf2;\n"
"}\n"
"\n"
"QPushButton#btn_edit {\n"
"    background-color: #fef3c7;\n"
"    color: #92400e;\n"
"    border: 1px solid #fcd34d;\n"
"    border-radius: 11px;\n"
"    padding: 9px 18px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 38px;\n"
"}\n"
"QPushButton#btn_edit:hover { backgr"
                        "ound-color: #fde68a; }\n"
"QPushButton#btn_edit:disabled {\n"
"    background-color: #f8fafc;\n"
"    color: #cbd5e1;\n"
"    border-color: #e6ebf2;\n"
"}\n"
"\n"
"QPushButton#btn_delete {\n"
"    background-color: #fef2f2;\n"
"    color: #dc2626;\n"
"    border: 1px solid #fecaca;\n"
"    border-radius: 11px;\n"
"    padding: 9px 18px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 38px;\n"
"}\n"
"QPushButton#btn_delete:hover { background-color: #fee2e2; }\n"
"QPushButton#btn_delete:disabled {\n"
"    background-color: #f8fafc;\n"
"    color: #cbd5e1;\n"
"    border-color: #e6ebf2;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 TABLE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QTableWidget#clients_table {\n"
"    background-color: #ffffff;\n"
"    alternate-background-color: #fbfcfe;\n"
"    border: none;\n"
"    border-top: 1px solid #eef2f7;\n"
"    border-bottom: 1px solid #eef2f7"
                        ";\n"
"    gridline-color: transparent;\n"
"    outline: none;\n"
"    color: #334155;\n"
"    font-size: 13px;\n"
"}\n"
"QTableWidget#clients_table::item {\n"
"    padding: 12px 8px;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"    color: #334155;\n"
"}\n"
"QTableWidget#clients_table::item:hover {\n"
"    background-color: #f8fafc;\n"
"}\n"
"QTableWidget#clients_table::item:selected {\n"
"    background-color: #eff6ff;\n"
"    color: #0077B6;\n"
"}\n"
"\n"
"QHeaderView {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #f8fafc;\n"
"    color: #94a3b8;\n"
"    padding: 14px 10px;\n"
"    border: none;\n"
"    border-bottom: 2px solid #e6ebf2;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    text-transform: uppercase;\n"
"}\n"
"QHeaderView::section:hover {\n"
"    background-color: #eff6ff;\n"
"    color: #0077B6;\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #f8fafc;\n"
"    bo"
                        "rder: none;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 PAGINATION \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#pagination_bar {\n"
"    background-color: #f8fafc;\n"
"    border-top: 1px solid #eef2f7;\n"
"    border-bottom: 1px solid #eef2f7;\n"
"}\n"
"QPushButton#btn_prev, QPushButton#btn_next {\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 8px 16px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-width: 90px;\n"
"    min-height: 36px;\n"
"}\n"
"QPushButton#btn_prev:hover:enabled, QPushButton#btn_next:hover:enabled {\n"
"    background-color: #eff6ff;\n"
"    border-color: #93c5fd;\n"
"    color: #0077B6;\n"
"}\n"
"QPushButton#btn_prev:disabled, QPushButton#btn_next:disabled {\n"
"    background-color: #f1f5f9;\n"
"    color: #cbd5e1;\n"
"    border-color: #e6ebf2;\n"
"}\n"
"\n"
"QLabel#"
                        "page_info {\n"
"    color: #475569;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    background: transparent;\n"
"    padding: 0 16px;\n"
"}\n"
"QLabel#total_info {\n"
"    color: #94a3b8;\n"
"    font-size: 11px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QFrame#empty_state {\n"
"    background-color: #fbfcfe;\n"
"    border: 1px dashed #dbe3ec;\n"
"    border-radius: 14px;\n"
"}\n"
"QLabel#empty_text {\n"
"    color: #94a3b8;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 SCROLLBAR \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 2px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #cbd5e1;\n"
"    min-height: 32px;\n"
"    border-radius: 5px;\n"
"}\n"
"QScrollBar:"
                        ":handle:vertical:hover { background: #94a3b8; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px; background: transparent;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: transparent;\n"
"}\n"
"")
        self.root_layout = QVBoxLayout(PageClients)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.card = QFrame(PageClients)
        self.card.setObjectName(u"card")
        self.card.setFrameShape(QFrame.Shape.NoFrame)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setSpacing(0)
        self.card_layout.setObjectName(u"card_layout")
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.card)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 80))
        self.header_frame.setStyleSheet(u"background-color: #ffffff; border-top-left-radius: 18px; border-top-right-radius: 18px;")
        self.header_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.header_layout = QVBoxLayout(self.header_frame)
        self.header_layout.setSpacing(4)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(24, 18, 24, 14)
        self.title_row = QHBoxLayout()
        self.title_row.setSpacing(12)
        self.title_row.setObjectName(u"title_row")
        self.page_title = QLabel(self.header_frame)
        self.page_title.setObjectName(u"page_title")

        self.title_row.addWidget(self.page_title)

        self.count_badge = QLabel(self.header_frame)
        self.count_badge.setObjectName(u"count_badge")

        self.title_row.addWidget(self.count_badge)

        self.title_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.title_row.addItem(self.title_spacer)


        self.header_layout.addLayout(self.title_row)

        self.page_subtitle = QLabel(self.header_frame)
        self.page_subtitle.setObjectName(u"page_subtitle")

        self.header_layout.addWidget(self.page_subtitle)


        self.card_layout.addWidget(self.header_frame)

        self.toolbar_frame = QFrame(self.card)
        self.toolbar_frame.setObjectName(u"toolbar_frame")
        self.toolbar_frame.setMinimumSize(QSize(0, 70))
        self.toolbar_frame.setStyleSheet(u"background-color: #ffffff; border-bottom: 1px solid #eef2f7;")
        self.toolbar_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.toolbar_layout = QHBoxLayout(self.toolbar_frame)
        self.toolbar_layout.setSpacing(12)
        self.toolbar_layout.setObjectName(u"toolbar_layout")
        self.toolbar_layout.setContentsMargins(24, 14, 24, 14)
        self.search_wrapper = QFrame(self.toolbar_frame)
        self.search_wrapper.setObjectName(u"search_wrapper")
        self.search_wrapper.setMinimumSize(QSize(280, 42))
        self.search_wrapper.setMaximumSize(QSize(400, 42))
        self.search_wrapper.setStyleSheet(u"background: transparent; border: none;")
        self.search_wrapper.setFrameShape(QFrame.Shape.NoFrame)
        self.search_wrapper_layout = QHBoxLayout(self.search_wrapper)
        self.search_wrapper_layout.setSpacing(0)
        self.search_wrapper_layout.setObjectName(u"search_wrapper_layout")
        self.search_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        self.search_input = QLineEdit(self.search_wrapper)
        self.search_input.setObjectName(u"search_input")
        self.search_input.setMinimumSize(QSize(0, 42))
        self.search_input.setClearButtonEnabled(True)

        self.search_wrapper_layout.addWidget(self.search_input)


        self.toolbar_layout.addWidget(self.search_wrapper)

        self.filter_combo = QComboBox(self.toolbar_frame)
        self.filter_combo.addItem("")
        self.filter_combo.addItem("")
        self.filter_combo.addItem("")
        self.filter_combo.addItem("")
        self.filter_combo.setObjectName(u"filter_combo")
        self.filter_combo.setMinimumSize(QSize(192, 42))

        self.toolbar_layout.addWidget(self.filter_combo)

        self.toolbar_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolbar_layout.addItem(self.toolbar_spacer)

        self.btn_refresh = QPushButton(self.toolbar_frame)
        self.btn_refresh.setObjectName(u"btn_refresh")
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/refresh.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_refresh.setIcon(icon)
        self.btn_refresh.setIconSize(QSize(16, 16))

        self.toolbar_layout.addWidget(self.btn_refresh)

        self.btn_new = QPushButton(self.toolbar_frame)
        self.btn_new.setObjectName(u"btn_new")
        self.btn_new.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/plus_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_new.setIcon(icon1)
        self.btn_new.setIconSize(QSize(16, 16))

        self.toolbar_layout.addWidget(self.btn_new)


        self.card_layout.addWidget(self.toolbar_frame)

        self.clients_table = QTableWidget(self.card)
        if (self.clients_table.columnCount() < 7):
            self.clients_table.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.clients_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.clients_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.clients_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.clients_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.clients_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.clients_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.clients_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.clients_table.setObjectName(u"clients_table")
        self.clients_table.setMinimumSize(QSize(0, 400))
        self.clients_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.clients_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.clients_table.setAlternatingRowColors(True)
        self.clients_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.clients_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.clients_table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.clients_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.clients_table.setShowGrid(False)
        self.clients_table.setSortingEnabled(False)
        self.clients_table.verticalHeader().setVisible(False)
        self.clients_table.verticalHeader().setDefaultSectionSize(52)

        self.card_layout.addWidget(self.clients_table)

        self.pagination_bar = QFrame(self.card)
        self.pagination_bar.setObjectName(u"pagination_bar")
        self.pagination_bar.setMinimumSize(QSize(0, 60))
        self.pagination_bar.setMaximumSize(QSize(16777215, 60))
        self.pagination_bar.setFrameShape(QFrame.Shape.NoFrame)
        self.pagination_layout = QHBoxLayout(self.pagination_bar)
        self.pagination_layout.setSpacing(8)
        self.pagination_layout.setObjectName(u"pagination_layout")
        self.pagination_layout.setContentsMargins(24, 10, 24, 10)
        self.btn_prev = QPushButton(self.pagination_bar)
        self.btn_prev.setObjectName(u"btn_prev")
        self.btn_prev.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.pagination_layout.addWidget(self.btn_prev)

        self.page_info = QLabel(self.pagination_bar)
        self.page_info.setObjectName(u"page_info")
        self.page_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pagination_layout.addWidget(self.page_info)

        self.btn_next = QPushButton(self.pagination_bar)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.pagination_layout.addWidget(self.btn_next)

        self.pagination_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pagination_layout.addItem(self.pagination_spacer)

        self.total_info = QLabel(self.pagination_bar)
        self.total_info.setObjectName(u"total_info")

        self.pagination_layout.addWidget(self.total_info)


        self.card_layout.addWidget(self.pagination_bar)

        self.actions_frame = QFrame(self.card)
        self.actions_frame.setObjectName(u"actions_frame")
        self.actions_frame.setMinimumSize(QSize(0, 72))
        self.actions_frame.setStyleSheet(u"background-color: #ffffff; border-bottom-left-radius: 18px; border-bottom-right-radius: 18px;")
        self.actions_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.actions_layout = QHBoxLayout(self.actions_frame)
        self.actions_layout.setSpacing(10)
        self.actions_layout.setObjectName(u"actions_layout")
        self.actions_layout.setContentsMargins(24, 14, 24, 14)
        self.hint_selection = QLabel(self.actions_frame)
        self.hint_selection.setObjectName(u"hint_selection")
        self.hint_selection.setStyleSheet(u"color: #94a3b8; font-size: 11px; font-weight: 600; background: transparent;")

        self.actions_layout.addWidget(self.hint_selection)

        self.actions_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.actions_layout.addItem(self.actions_spacer)

        self.btn_view = QPushButton(self.actions_frame)
        self.btn_view.setObjectName(u"btn_view")
        self.btn_view.setEnabled(False)
        self.btn_view.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/eye.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_view.setIcon(icon2)
        self.btn_view.setIconSize(QSize(14, 14))

        self.actions_layout.addWidget(self.btn_view)

        self.btn_edit = QPushButton(self.actions_frame)
        self.btn_edit.setObjectName(u"btn_edit")
        self.btn_edit.setEnabled(False)
        self.btn_edit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/Icon/Icons/edit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_edit.setIcon(icon3)
        self.btn_edit.setIconSize(QSize(14, 14))

        self.actions_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton(self.actions_frame)
        self.btn_delete.setObjectName(u"btn_delete")
        self.btn_delete.setEnabled(False)
        self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/Icon/Icons/trash.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_delete.setIcon(icon4)
        self.btn_delete.setIconSize(QSize(14, 14))

        self.actions_layout.addWidget(self.btn_delete)


        self.card_layout.addWidget(self.actions_frame)


        self.root_layout.addWidget(self.card)


        self.retranslateUi(PageClients)

        QMetaObject.connectSlotsByName(PageClients)
    # setupUi

    def retranslateUi(self, PageClients):
        self.page_title.setText(QCoreApplication.translate("PageClients", u"Gestion des clients", None))
        self.count_badge.setText(QCoreApplication.translate("PageClients", u"0 clients", None))
        self.page_subtitle.setText(QCoreApplication.translate("PageClients", u"Recherchez, consultez et g\u00e9rez les clients de votre officine.", None))
        self.search_input.setPlaceholderText(QCoreApplication.translate("PageClients", u"Rechercher un client\u2026", None))
        self.filter_combo.setItemText(0, QCoreApplication.translate("PageClients", u"Tous les clients", None))
        self.filter_combo.setItemText(1, QCoreApplication.translate("PageClients", u"Clients actifs", None))
        self.filter_combo.setItemText(2, QCoreApplication.translate("PageClients", u"Clients anonymes", None))
        self.filter_combo.setItemText(3, QCoreApplication.translate("PageClients", u"Clients inactifs", None))

#if QT_CONFIG(tooltip)
        self.btn_refresh.setToolTip(QCoreApplication.translate("PageClients", u"Actualiser", None))
#endif // QT_CONFIG(tooltip)
        self.btn_refresh.setText("")
        self.btn_new.setText(QCoreApplication.translate("PageClients", u"Nouveau client", None))
        ___qtablewidgetitem = self.clients_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageClients", u"Nom", None))
        ___qtablewidgetitem1 = self.clients_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageClients", u"Sexe", None))
        ___qtablewidgetitem2 = self.clients_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageClients", u"Num\u00e9ro", None))
        ___qtablewidgetitem3 = self.clients_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageClients", u"Total achet\u00e9", None))
        ___qtablewidgetitem4 = self.clients_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PageClients", u"Visites", None))
        ___qtablewidgetitem5 = self.clients_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PageClients", u"Derni\u00e8re visite", None))
        ___qtablewidgetitem6 = self.clients_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("PageClients", u"Statut", None))
        self.btn_prev.setText(QCoreApplication.translate("PageClients", u"\u25c0  Pr\u00e9c\u00e9dent", None))
        self.page_info.setText(QCoreApplication.translate("PageClients", u"Page 1 / 1", None))
        self.btn_next.setText(QCoreApplication.translate("PageClients", u"Suivant  \u25b6", None))
        self.total_info.setText(QCoreApplication.translate("PageClients", u"0 client", None))
        self.hint_selection.setText(QCoreApplication.translate("PageClients", u"S\u00e9lectionnez un client pour agir", None))
        self.btn_view.setText(QCoreApplication.translate("PageClients", u"Voir la fiche", None))
        self.btn_edit.setText(QCoreApplication.translate("PageClients", u"Modifier", None))
        self.btn_delete.setText(QCoreApplication.translate("PageClients", u"Supprimer", None))
        pass
    # retranslateUi

