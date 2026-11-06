# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_page_blfERRQGj.ui'
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

class Ui_PageBLF(object):
    def setupUi(self, PageBLF):
        if not PageBLF.objectName():
            PageBLF.setObjectName(u"PageBLF")
        PageBLF.resize(1031, 732)
        PageBLF.setStyleSheet(u"/* ============================================================\n"
"   NOVA PHARMA \u2014 PAGE BLF (design system v2)\n"
"   ============================================================ */\n"
"\n"
"QWidget#PageBLF {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 CARTE PRINCIPALE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#main_card {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 HEADER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#header_frame {\n"
"    background-color: #ffffff;\n"
"    border-top-left-radius: 18px;\n"
"    border-top-right-radius: 18px;\n"
"    border: none;\n"
"}\n"
"QLabel#header_title {\n"
"    color: #0f172a;\n"
"    font-size: 20px;\n"
""
                        "    font-weight: 800;\n"
"    letter-spacing: -0.3px;\n"
"    background: transparent;\n"
"}\n"
"QLabel#header_subtitle {\n"
"    color: #64748b;\n"
"    font-size: 12px;\n"
"    background: transparent;\n"
"}\n"
"QLabel#header_badge {\n"
"    color: #0077B6;\n"
"    font-size: 11px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 0.5px;\n"
"    background-color: #e0f7fa;\n"
"    border: 1px solid #bae6fd;\n"
"    border-radius: 10px;\n"
"    padding: 5px 12px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 BARRE DE S\u00c9PARATION \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#header_sep {\n"
"    background-color: #eef2f7;\n"
"    border: none;\n"
"    min-height: 1px;\n"
"    max-height: 1px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 TOOLBAR \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#"
                        "toolbar_frame {\n"
"    background-color: #ffffff;\n"
"    border: none;\n"
"}\n"
"QLineEdit#search_input {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 10px 14px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    selection-background-color: #bfdbfe;\n"
"}\n"
"QLineEdit#search_input:hover { border-color: #b9c6d8; }\n"
"QLineEdit#search_input:focus {\n"
"    background-color: #ffffff;\n"
"    border: 1.5px solid #0077B6;\n"
"}\n"
"\n"
"QComboBox#filter_combo {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 10px 14px;\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"}\n"
"QComboBox#filter_combo:hover { border-color: #b9c6d8; }\n"
"QComboBox#filter_combo:focus { border-color: #0077B6; }\n"
"QComboBox#filter_combo::drop-down { border: none; width: 26px; }\n"
"QComboBox#filter_combo::down-arrow {\n"
"    image: "
                        "url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}\n"
"QComboBox#filter_combo QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 10px;\n"
"    padding: 6px;\n"
"    selection-background-color: #eff6ff;\n"
"    selection-color: #0077B6;\n"
"    outline: none;\n"
"}\n"
"\n"
"QPushButton#btn_refresh {\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 11px;\n"
"    min-width: 42px;\n"
"    max-width: 42px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_refresh:hover {\n"
"    background-color: #f8fafc;\n"
"    border-color: #c3cedd;\n"
"    color: #0f172a;\n"
"}\n"
"QPushButton#btn_refresh:pressed { background-color: #eef2f7; }\n"
"\n"
"/* \u2500\u2500\u2500 Bouton \"Nouveau fournisseur\" (blanc / outline bleu) \u2500\u2500\u2500 */\n"
"QPushButton#btn_new_supplier {\n"
"    background-color: #ffffff;\n"
"    color: #023E8A;\n"
"   "
                        " border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
"    padding: 11px 20px;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    letter-spacing: 0.2px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_new_supplier:hover {\n"
"    background-color: #eff6ff;\n"
"    border-color: #bfdbfe;\n"
"    color: #0077B6;\n"
"}\n"
"QPushButton#btn_new_supplier:pressed {\n"
"    background-color: #dbeafe;\n"
"    border-color: #93c5fd;\n"
"}\n"
"\n"
"/* \u2500\u2500\u2500 Bouton \"Nouveau BLF\" (primaire d\u00e9grad\u00e9) \u2500\u2500\u2500 */\n"
"QPushButton#btn_new {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 11px;\n"
"    padding: 11px 22px;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 0.2px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_new:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A,"
                        " stop:1 #0077B6);\n"
"}\n"
"QPushButton#btn_new:pressed { background: #023E8A; }\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 TABLE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QTableWidget#blf_table {\n"
"    background-color: #ffffff;\n"
"    alternate-background-color: #fbfcfe;\n"
"    border: none;\n"
"    border-top: 1px solid #eef2f7;\n"
"    border-bottom: 1px solid #eef2f7;\n"
"    gridline-color: transparent;\n"
"    outline: none;\n"
"    color: #334155;\n"
"    font-size: 13px;\n"
"}\n"
"QTableWidget#blf_table::item {\n"
"    padding: 12px 8px;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"    color: #334155;\n"
"}\n"
"QTableWidget#blf_table::item:hover {\n"
"    background-color: #f8fafc;\n"
"}\n"
"QTableWidget#blf_table::item:selected {\n"
"    background-color: #eff6ff;\n"
"    color: #0077B6;\n"
"}\n"
"\n"
"QHeaderView {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"QHeader"
                        "View::section {\n"
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
"QTableCornerButton::section {\n"
"    background-color: #f8fafc;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 PAGINATION \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#pagination_frame {\n"
"    background-color: #f8fafc;\n"
"    border: none;\n"
"    border-top: 1px solid #eef2f7;\n"
"    border-bottom: 1px solid #eef2f7;\n"
"}\n"
"QPushButton#btn_prev,\n"
"QPushButton#btn_next {\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 8px 16px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-wi"
                        "dth: 95px;\n"
"    min-height: 36px;\n"
"}\n"
"QPushButton#btn_prev:hover:enabled,\n"
"QPushButton#btn_next:hover:enabled {\n"
"    background-color: #eff6ff;\n"
"    border-color: #93c5fd;\n"
"    color: #0077B6;\n"
"}\n"
"QPushButton#btn_prev:disabled,\n"
"QPushButton#btn_next:disabled {\n"
"    background-color: #f1f5f9;\n"
"    color: #cbd5e1;\n"
"    border-color: #e6ebf2;\n"
"}\n"
"QLabel#page_info {\n"
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
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 ACTIONS (footer) \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#actions_frame {\n"
"    background-color: #ffffff;\n"
"    border-bottom-left-radius: 18px;\n"
"    border-bottom-right-radiu"
                        "s: 18px;\n"
"    border: none;\n"
"}\n"
"QLabel#hint_selection {\n"
"    color: #94a3b8;\n"
"    font-size: 11px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"}\n"
"QPushButton#btn_view {\n"
"    background-color: #eff6ff;\n"
"    color: #0077B6;\n"
"    border: 1px solid #dbeafe;\n"
"    border-radius: 10px;\n"
"    padding: 9px 20px;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    min-height: 38px;\n"
"}\n"
"QPushButton#btn_view:hover:enabled {\n"
"    background-color: #dbeafe;\n"
"    border-color: #93c5fd;\n"
"}\n"
"QPushButton#btn_view:disabled {\n"
"    background-color: #f8fafc;\n"
"    color: #cbd5e1;\n"
"    border-color: #e6ebf2;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 SCROLLBAR \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 10px;\n"
"    margin: 2px;\n"
"}\n"
"QScrollBar::h"
                        "andle:vertical {\n"
"    background: #cbd5e1;\n"
"    min-height: 32px;\n"
"    border-radius: 5px;\n"
"}\n"
"QScrollBar::handle:vertical:hover { background: #94a3b8; }\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    background: transparent;\n"
"}\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical {\n"
"    background: transparent;\n"
"}\n"
"")
        self.root_layout = QVBoxLayout(PageBLF)
        self.root_layout.setSpacing(0)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.main_card = QFrame(PageBLF)
        self.main_card.setObjectName(u"main_card")
        self.main_card.setFrameShape(QFrame.Shape.NoFrame)
        self.main_card_layout = QVBoxLayout(self.main_card)
        self.main_card_layout.setSpacing(0)
        self.main_card_layout.setObjectName(u"main_card_layout")
        self.main_card_layout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.main_card)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 110))
        self.header_frame.setMaximumSize(QSize(16777215, 110))
        self.header_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.header_layout = QVBoxLayout(self.header_frame)
        self.header_layout.setSpacing(6)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(28, 22, 28, 18)
        self.title_row = QHBoxLayout()
        self.title_row.setSpacing(12)
        self.title_row.setObjectName(u"title_row")
        self.header_title = QLabel(self.header_frame)
        self.header_title.setObjectName(u"header_title")

        self.title_row.addWidget(self.header_title)

        self.header_badge = QLabel(self.header_frame)
        self.header_badge.setObjectName(u"header_badge")
        self.header_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_row.addWidget(self.header_badge)

        self.title_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.title_row.addItem(self.title_spacer)


        self.header_layout.addLayout(self.title_row)

        self.header_subtitle = QLabel(self.header_frame)
        self.header_subtitle.setObjectName(u"header_subtitle")

        self.header_layout.addWidget(self.header_subtitle)


        self.main_card_layout.addWidget(self.header_frame)

        self.header_sep = QFrame(self.main_card)
        self.header_sep.setObjectName(u"header_sep")
        self.header_sep.setFrameShape(QFrame.Shape.NoFrame)

        self.main_card_layout.addWidget(self.header_sep)

        self.toolbar_frame = QFrame(self.main_card)
        self.toolbar_frame.setObjectName(u"toolbar_frame")
        self.toolbar_frame.setMinimumSize(QSize(0, 74))
        self.toolbar_frame.setMaximumSize(QSize(16777215, 74))
        self.toolbar_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.toolbar_layout = QHBoxLayout(self.toolbar_frame)
        self.toolbar_layout.setSpacing(12)
        self.toolbar_layout.setObjectName(u"toolbar_layout")
        self.toolbar_layout.setContentsMargins(28, 16, 28, 16)
        self.search_input = QLineEdit(self.toolbar_frame)
        self.search_input.setObjectName(u"search_input")
        self.search_input.setMinimumSize(QSize(280, 42))
        self.search_input.setMaximumSize(QSize(450, 42))
        self.search_input.setClearButtonEnabled(True)

        self.toolbar_layout.addWidget(self.search_input)

        self.filter_combo = QComboBox(self.toolbar_frame)
        self.filter_combo.addItem("")
        self.filter_combo.addItem("")
        self.filter_combo.addItem("")
        self.filter_combo.addItem("")
        self.filter_combo.setObjectName(u"filter_combo")
        self.filter_combo.setMinimumSize(QSize(180, 42))
        self.filter_combo.setMaximumSize(QSize(200, 42))

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

        self.btn_new_supplier = QPushButton(self.toolbar_frame)
        self.btn_new_supplier.setObjectName(u"btn_new_supplier")
        self.btn_new_supplier.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/truck.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_new_supplier.setIcon(icon1)
        self.btn_new_supplier.setIconSize(QSize(16, 16))

        self.toolbar_layout.addWidget(self.btn_new_supplier)

        self.btn_new = QPushButton(self.toolbar_frame)
        self.btn_new.setObjectName(u"btn_new")
        self.btn_new.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/plus_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_new.setIcon(icon2)
        self.btn_new.setIconSize(QSize(16, 16))

        self.toolbar_layout.addWidget(self.btn_new)


        self.main_card_layout.addWidget(self.toolbar_frame)

        self.blf_table = QTableWidget(self.main_card)
        if (self.blf_table.columnCount() < 8):
            self.blf_table.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.blf_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.blf_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.blf_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.blf_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.blf_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.blf_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.blf_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.blf_table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.blf_table.setObjectName(u"blf_table")
        self.blf_table.setMinimumSize(QSize(0, 360))
        self.blf_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.blf_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.blf_table.setAlternatingRowColors(True)
        self.blf_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.blf_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.blf_table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.blf_table.setShowGrid(False)
        self.blf_table.setSortingEnabled(False)
        self.blf_table.verticalHeader().setVisible(False)
        self.blf_table.verticalHeader().setDefaultSectionSize(52)

        self.main_card_layout.addWidget(self.blf_table)

        self.pagination_frame = QFrame(self.main_card)
        self.pagination_frame.setObjectName(u"pagination_frame")
        self.pagination_frame.setMinimumSize(QSize(0, 60))
        self.pagination_frame.setMaximumSize(QSize(16777215, 60))
        self.pagination_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.pagination_layout = QHBoxLayout(self.pagination_frame)
        self.pagination_layout.setSpacing(8)
        self.pagination_layout.setObjectName(u"pagination_layout")
        self.pagination_layout.setContentsMargins(28, 10, 28, 10)
        self.btn_prev = QPushButton(self.pagination_frame)
        self.btn_prev.setObjectName(u"btn_prev")
        self.btn_prev.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_prev.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        icon3 = QIcon()
        icon3.addFile(u":/Icon/Icons/chevron-left.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_prev.setIcon(icon3)
        self.btn_prev.setIconSize(QSize(12, 12))

        self.pagination_layout.addWidget(self.btn_prev)

        self.page_info = QLabel(self.pagination_frame)
        self.page_info.setObjectName(u"page_info")
        self.page_info.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pagination_layout.addWidget(self.page_info)

        self.btn_next = QPushButton(self.pagination_frame)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/Icon/Icons/chevron-right.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_next.setIcon(icon4)
        self.btn_next.setIconSize(QSize(12, 12))

        self.pagination_layout.addWidget(self.btn_next)

        self.pagination_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.pagination_layout.addItem(self.pagination_spacer)

        self.total_info = QLabel(self.pagination_frame)
        self.total_info.setObjectName(u"total_info")

        self.pagination_layout.addWidget(self.total_info)


        self.main_card_layout.addWidget(self.pagination_frame)

        self.actions_frame = QFrame(self.main_card)
        self.actions_frame.setObjectName(u"actions_frame")
        self.actions_frame.setMinimumSize(QSize(0, 76))
        self.actions_frame.setMaximumSize(QSize(16777215, 76))
        self.actions_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.actions_layout = QHBoxLayout(self.actions_frame)
        self.actions_layout.setSpacing(10)
        self.actions_layout.setObjectName(u"actions_layout")
        self.actions_layout.setContentsMargins(28, 16, 28, 16)
        self.hint_selection = QLabel(self.actions_frame)
        self.hint_selection.setObjectName(u"hint_selection")

        self.actions_layout.addWidget(self.hint_selection)

        self.actions_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.actions_layout.addItem(self.actions_spacer)

        self.btn_view = QPushButton(self.actions_frame)
        self.btn_view.setObjectName(u"btn_view")
        self.btn_view.setEnabled(False)
        self.btn_view.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon5 = QIcon()
        icon5.addFile(u":/Icon/Icons/eye.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_view.setIcon(icon5)
        self.btn_view.setIconSize(QSize(14, 14))

        self.actions_layout.addWidget(self.btn_view)


        self.main_card_layout.addWidget(self.actions_frame)


        self.root_layout.addWidget(self.main_card)


        self.retranslateUi(PageBLF)

        QMetaObject.connectSlotsByName(PageBLF)
    # setupUi

    def retranslateUi(self, PageBLF):
        PageBLF.setWindowTitle(QCoreApplication.translate("PageBLF", u"Bons de Livraison", None))
        self.header_title.setText(QCoreApplication.translate("PageBLF", u"Bons de Livraison Fournisseur", None))
        self.header_badge.setText(QCoreApplication.translate("PageBLF", u"0 BLF", None))
        self.header_subtitle.setText(QCoreApplication.translate("PageBLF", u"R\u00e9ceptionnez vos commandes fournisseurs et g\u00e9rez votre stock en toute tra\u00e7abilit\u00e9.", None))
        self.search_input.setPlaceholderText(QCoreApplication.translate("PageBLF", u"Rechercher par num\u00e9ro ou fournisseur\u2026", None))
        self.filter_combo.setItemText(0, QCoreApplication.translate("PageBLF", u"Tous les BLF", None))
        self.filter_combo.setItemText(1, QCoreApplication.translate("PageBLF", u"Brouillons", None))
        self.filter_combo.setItemText(2, QCoreApplication.translate("PageBLF", u"Valid\u00e9es", None))
        self.filter_combo.setItemText(3, QCoreApplication.translate("PageBLF", u"Annul\u00e9es", None))

#if QT_CONFIG(tooltip)
        self.btn_refresh.setToolTip(QCoreApplication.translate("PageBLF", u"Actualiser la liste", None))
#endif // QT_CONFIG(tooltip)
        self.btn_refresh.setText("")
#if QT_CONFIG(tooltip)
        self.btn_new_supplier.setToolTip(QCoreApplication.translate("PageBLF", u"Ajouter un fournisseur \u00e0 votre r\u00e9pertoire", None))
#endif // QT_CONFIG(tooltip)
        self.btn_new_supplier.setText(QCoreApplication.translate("PageBLF", u"Nouveau fournisseur", None))
        self.btn_new.setText(QCoreApplication.translate("PageBLF", u"Nouveau BLF", None))
        ___qtablewidgetitem = self.blf_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PageBLF", u"N\u00b0 BLF", None))
        ___qtablewidgetitem1 = self.blf_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PageBLF", u"Fournisseur", None))
        ___qtablewidgetitem2 = self.blf_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PageBLF", u"Date", None))
        ___qtablewidgetitem3 = self.blf_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PageBLF", u"Articles", None))
        ___qtablewidgetitem4 = self.blf_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PageBLF", u"Unit\u00e9s", None))
        ___qtablewidgetitem5 = self.blf_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PageBLF", u"Total", None))
        ___qtablewidgetitem6 = self.blf_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("PageBLF", u"Statut", None))
        ___qtablewidgetitem7 = self.blf_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("PageBLF", u"Cr\u00e9\u00e9 par", None))
        self.btn_prev.setText(QCoreApplication.translate("PageBLF", u"Pr\u00e9c\u00e9dent", None))
        self.page_info.setText(QCoreApplication.translate("PageBLF", u"Page 1 / 1", None))
        self.btn_next.setText(QCoreApplication.translate("PageBLF", u"Suivant", None))
        self.total_info.setText(QCoreApplication.translate("PageBLF", u"0 BLF au total", None))
        self.hint_selection.setText(QCoreApplication.translate("PageBLF", u"S\u00e9lectionnez un BLF pour voir les d\u00e9tails", None))
        self.btn_view.setText(QCoreApplication.translate("PageBLF", u"Voir le d\u00e9tail", None))
    # retranslateUi

