# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_blf_detailTfQLXq.ui'
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
    QTableWidgetItem, QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(980, 760)
        Dialog.setMinimumSize(QSize(900, 700))
        Dialog.setStyleSheet(u"/* ============================================================\n"
"   NOVA PHARMA \u2014 D\u00c9TAIL BLF\n"
"   ============================================================ */\n"
"\n"
"QDialog { background-color: #f0f4f8; }\n"
"\n"
"QWidget {\n"
"    font-family: \"Segoe UI\", \"Inter\", \"Roboto\", sans-serif;\n"
"    font-size: 13px;\n"
"    color: #0f172a;\n"
"    outline: none;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 HEADER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#header_frame {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:0.4 #0077B6, stop:1 #00B4D8);\n"
"    border-top-left-radius: 18px;\n"
"    border-top-right-radius: 18px;\n"
"    border: none;\n"
"}\n"
"QLabel#header_icon {\n"
"    background-color: rgba(255,255,255,0.15);\n"
"    border: 1px solid rgba(255,255,255,0.25);\n"
"    border-radius: 14px;\n"
"    padding: 10px;\n"
"}\n"
"QLabel#header_numero {\n"
"    color: #ffffff;\n"
""
                        "    font-size: 20px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"    letter-spacing: 0.3px;\n"
"}\n"
"QLabel#header_sub {\n"
"    color: #CAF0F8;\n"
"    font-size: 12px;\n"
"    background: transparent;\n"
"}\n"
"QLabel#statut_badge {\n"
"    font-size: 11px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    border-radius: 10px;\n"
"    padding: 8px 16px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 CARTE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#card {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-top: none;\n"
"    border-bottom-left-radius: 18px;\n"
"    border-bottom-right-radius: 18px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 M\u00c9TADONN\u00c9ES \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QLabel#meta_key {\n"
"    color: #94a3b8;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1p"
                        "x;\n"
"    background: transparent;\n"
"}\n"
"QLabel#meta_value {\n"
"    color: #0f172a;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 LIGNES \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QLabel#section_title {\n"
"    color: #334155;\n"
"    font-size: 11px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    background: transparent;\n"
"}\n"
"QTableWidget#table_lignes {\n"
"    background-color: #ffffff;\n"
"    alternate-background-color: #fbfcfe;\n"
"    border: none;\n"
"    border-top: 1px solid #eef2f7;\n"
"    gridline-color: transparent;\n"
"    outline: none;\n"
"    color: #334155;\n"
"}\n"
"QTableWidget#table_lignes::item {\n"
"    padding: 10px 8px;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"}\n"
"QTableWidget#table_lignes::item:selected {\n"
"    background-color: #eff6ff;\n"
"    color: #0077B6;\n"
"}\n"
"QHeaderView::section {\n"
"    backgrou"
                        "nd-color: #f8fafc;\n"
"    color: #94a3b8;\n"
"    padding: 12px 8px;\n"
"    border: none;\n"
"    border-bottom: 2px solid #e6ebf2;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 TOTAUX \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#total_box {\n"
"    background-color: #eff6ff;\n"
"    border-top: 1px solid #dbeafe;\n"
"}\n"
"QLabel#total_caption {\n"
"    color: #1e40af;\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#total_value {\n"
"    color: #023E8A;\n"
"    font-size: 20px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"QLabel#total_info {\n"
"    color: #1e40af;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 NOTES \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 "
                        "*/\n"
"QFrame#notes_wrap {\n"
"    background-color: #fefce8;\n"
"    border-top: 1px solid #fef08a;\n"
"}\n"
"QLabel#notes_text {\n"
"    color: #854d0e;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 MOTIF ANNULATION \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#motif_wrap {\n"
"    background-color: #fef2f2;\n"
"    border-top: 1px solid #fecaca;\n"
"}\n"
"QLabel#motif_text {\n"
"    color: #991b1b;\n"
"    font-size: 12px;\n"
"    font-weight: 500;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 FOOTER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#footer_frame {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"QPushButton#btn_cancel_blf {\n"
"    background-color: #ffffff;\n"
"    color: #dc2626;\n"
"    bord"
                        "er: 1.5px solid #fecaca;\n"
"    border-radius: 10px;\n"
"    padding: 10px 22px;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_cancel_blf:hover { background-color: #fef2f2; }\n"
"\n"
"QPushButton#btn_validate_blf {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #16A34A, stop:1 #22c55e);\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    padding: 10px 24px;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    min-width: 180px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_validate_blf:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #15803d, stop:1 #16A34A);\n"
"}\n"
"\n"
"QPushButton#btn_close {\n"
"    background-color: #ffffff;\n"
"    color: #475569;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 10px;\n"
"    padding: 10px 24px;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"    min-width: 110px;\n"
"    min-height: "
                        "42px;\n"
"}\n"
"QPushButton#btn_close:hover { background-color: #f8fafc; }\n"
"\n"
"/* Scrollbar */\n"
"QScrollBar:vertical {\n"
"    border: none; background: transparent;\n"
"    width: 10px; margin: 2px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #cbd5e1; min-height: 32px; border-radius: 5px;\n"
"}\n"
"QScrollBar::handle:vertical:hover { background: #94a3b8; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }\n"
"")
        self.root_layout = QVBoxLayout(Dialog)
        self.root_layout.setSpacing(14)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.header_frame = QFrame(Dialog)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 110))
        self.header_frame.setMaximumSize(QSize(16777215, 110))
        self.header_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setSpacing(16)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(28, 20, 28, 20)
        self.header_icon = QLabel(self.header_frame)
        self.header_icon.setObjectName(u"header_icon")
        self.header_icon.setMinimumSize(QSize(48, 48))
        self.header_icon.setMaximumSize(QSize(48, 48))
        self.header_icon.setPixmap(QPixmap(u":/Icon/Icons/package_white.svg"))
        self.header_icon.setScaledContents(True)

        self.header_layout.addWidget(self.header_icon)

        self.header_text = QVBoxLayout()
        self.header_text.setSpacing(4)
        self.header_text.setObjectName(u"header_text")
        self.header_numero = QLabel(self.header_frame)
        self.header_numero.setObjectName(u"header_numero")

        self.header_text.addWidget(self.header_numero)

        self.header_sub = QLabel(self.header_frame)
        self.header_sub.setObjectName(u"header_sub")

        self.header_text.addWidget(self.header_sub)


        self.header_layout.addLayout(self.header_text)

        self.header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_layout.addItem(self.header_spacer)

        self.statut_badge = QLabel(self.header_frame)
        self.statut_badge.setObjectName(u"statut_badge")

        self.header_layout.addWidget(self.statut_badge)


        self.root_layout.addWidget(self.header_frame)

        self.card = QFrame(Dialog)
        self.card.setObjectName(u"card")
        self.card.setFrameShape(QFrame.Shape.NoFrame)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setSpacing(0)
        self.card_layout.setObjectName(u"card_layout")
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.meta_grid = QGridLayout()
        self.meta_grid.setObjectName(u"meta_grid")
        self.meta_grid.setHorizontalSpacing(30)
        self.meta_grid.setVerticalSpacing(12)
        self.meta_grid.setContentsMargins(28, 22, 28, 18)
        self.key_fournisseur = QLabel(self.card)
        self.key_fournisseur.setObjectName(u"key_fournisseur")

        self.meta_grid.addWidget(self.key_fournisseur, 0, 0, 1, 1)

        self.key_ref_ext = QLabel(self.card)
        self.key_ref_ext.setObjectName(u"key_ref_ext")

        self.meta_grid.addWidget(self.key_ref_ext, 0, 1, 1, 1)

        self.key_date = QLabel(self.card)
        self.key_date.setObjectName(u"key_date")

        self.meta_grid.addWidget(self.key_date, 0, 2, 1, 1)

        self.val_fournisseur = QLabel(self.card)
        self.val_fournisseur.setObjectName(u"val_fournisseur")

        self.meta_grid.addWidget(self.val_fournisseur, 1, 0, 1, 1)

        self.val_ref_ext = QLabel(self.card)
        self.val_ref_ext.setObjectName(u"val_ref_ext")

        self.meta_grid.addWidget(self.val_ref_ext, 1, 1, 1, 1)

        self.val_date = QLabel(self.card)
        self.val_date.setObjectName(u"val_date")

        self.meta_grid.addWidget(self.val_date, 1, 2, 1, 1)

        self.key_created = QLabel(self.card)
        self.key_created.setObjectName(u"key_created")

        self.meta_grid.addWidget(self.key_created, 2, 0, 1, 1)

        self.key_validated = QLabel(self.card)
        self.key_validated.setObjectName(u"key_validated")

        self.meta_grid.addWidget(self.key_validated, 2, 1, 1, 1)

        self.key_cancelled = QLabel(self.card)
        self.key_cancelled.setObjectName(u"key_cancelled")

        self.meta_grid.addWidget(self.key_cancelled, 2, 2, 1, 1)

        self.val_created = QLabel(self.card)
        self.val_created.setObjectName(u"val_created")

        self.meta_grid.addWidget(self.val_created, 3, 0, 1, 1)

        self.val_validated = QLabel(self.card)
        self.val_validated.setObjectName(u"val_validated")

        self.meta_grid.addWidget(self.val_validated, 3, 1, 1, 1)

        self.val_cancelled = QLabel(self.card)
        self.val_cancelled.setObjectName(u"val_cancelled")

        self.meta_grid.addWidget(self.val_cancelled, 3, 2, 1, 1)


        self.card_layout.addLayout(self.meta_grid)

        self.sep_1 = QFrame(self.card)
        self.sep_1.setObjectName(u"sep_1")
        self.sep_1.setMinimumSize(QSize(0, 1))
        self.sep_1.setMaximumSize(QSize(16777215, 1))
        self.sep_1.setStyleSheet(u"background-color: #eef2f7;")
        self.sep_1.setFrameShape(QFrame.Shape.NoFrame)

        self.card_layout.addWidget(self.sep_1)

        self.section_title = QLabel(self.card)
        self.section_title.setObjectName(u"section_title")
        self.section_title.setStyleSheet(u"color: #334155; font-size: 11px; font-weight: 800; letter-spacing: 1px; background: transparent; padding: 18px 28px 10px 28px;")

        self.card_layout.addWidget(self.section_title)

        self.table_lignes = QTableWidget(self.card)
        if (self.table_lignes.columnCount() < 7):
            self.table_lignes.setColumnCount(7)
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
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_lignes.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.table_lignes.setObjectName(u"table_lignes")
        self.table_lignes.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_lignes.setAlternatingRowColors(True)
        self.table_lignes.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_lignes.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table_lignes.setShowGrid(False)
        self.table_lignes.verticalHeader().setVisible(False)
        self.table_lignes.verticalHeader().setDefaultSectionSize(46)

        self.card_layout.addWidget(self.table_lignes)

        self.total_box = QFrame(self.card)
        self.total_box.setObjectName(u"total_box")
        self.total_box.setMinimumSize(QSize(0, 60))
        self.total_box.setFrameShape(QFrame.Shape.NoFrame)
        self.total_layout = QHBoxLayout(self.total_box)
        self.total_layout.setSpacing(30)
        self.total_layout.setObjectName(u"total_layout")
        self.total_layout.setContentsMargins(28, 14, 28, 14)
        self.val_nb_articles = QLabel(self.total_box)
        self.val_nb_articles.setObjectName(u"val_nb_articles")
        self.val_nb_articles.setStyleSheet(u"color: #1e40af; font-size: 12px; font-weight: 700; background: transparent;")

        self.total_layout.addWidget(self.val_nb_articles)

        self.val_nb_unites = QLabel(self.total_box)
        self.val_nb_unites.setObjectName(u"val_nb_unites")
        self.val_nb_unites.setStyleSheet(u"color: #1e40af; font-size: 12px; font-weight: 700; background: transparent;")

        self.total_layout.addWidget(self.val_nb_unites)

        self.total_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.total_layout.addItem(self.total_spacer)

        self.total_caption = QLabel(self.total_box)
        self.total_caption.setObjectName(u"total_caption")

        self.total_layout.addWidget(self.total_caption)

        self.total_value = QLabel(self.total_box)
        self.total_value.setObjectName(u"total_value")

        self.total_layout.addWidget(self.total_value)


        self.card_layout.addWidget(self.total_box)

        self.notes_wrap = QFrame(self.card)
        self.notes_wrap.setObjectName(u"notes_wrap")
        self.notes_wrap.setVisible(False)
        self.notes_wrap.setFrameShape(QFrame.Shape.NoFrame)
        self.notes_layout = QHBoxLayout(self.notes_wrap)
        self.notes_layout.setSpacing(10)
        self.notes_layout.setObjectName(u"notes_layout")
        self.notes_layout.setContentsMargins(28, 12, 28, 12)
        self.notes_icon = QLabel(self.notes_wrap)
        self.notes_icon.setObjectName(u"notes_icon")
        self.notes_icon.setMinimumSize(QSize(16, 16))
        self.notes_icon.setMaximumSize(QSize(16, 16))
        self.notes_icon.setPixmap(QPixmap(u":/Icon/Icons/info.svg"))
        self.notes_icon.setScaledContents(True)

        self.notes_layout.addWidget(self.notes_icon)

        self.notes_text = QLabel(self.notes_wrap)
        self.notes_text.setObjectName(u"notes_text")
        self.notes_text.setWordWrap(True)

        self.notes_layout.addWidget(self.notes_text)


        self.card_layout.addWidget(self.notes_wrap)

        self.motif_wrap = QFrame(self.card)
        self.motif_wrap.setObjectName(u"motif_wrap")
        self.motif_wrap.setVisible(False)
        self.motif_wrap.setFrameShape(QFrame.Shape.NoFrame)
        self.motif_layout = QHBoxLayout(self.motif_wrap)
        self.motif_layout.setSpacing(10)
        self.motif_layout.setObjectName(u"motif_layout")
        self.motif_layout.setContentsMargins(28, 12, 28, 12)
        self.motif_icon = QLabel(self.motif_wrap)
        self.motif_icon.setObjectName(u"motif_icon")
        self.motif_icon.setMinimumSize(QSize(16, 16))
        self.motif_icon.setMaximumSize(QSize(16, 16))
        self.motif_icon.setPixmap(QPixmap(u":/Icon/Icons/alert-circle.svg"))
        self.motif_icon.setScaledContents(True)

        self.motif_layout.addWidget(self.motif_icon)

        self.motif_text = QLabel(self.motif_wrap)
        self.motif_text.setObjectName(u"motif_text")
        self.motif_text.setWordWrap(True)

        self.motif_layout.addWidget(self.motif_text)


        self.card_layout.addWidget(self.motif_wrap)


        self.root_layout.addWidget(self.card)

        self.footer_frame = QFrame(Dialog)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setMinimumSize(QSize(0, 80))
        self.footer_frame.setMaximumSize(QSize(16777215, 80))
        self.footer_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.footer_layout = QHBoxLayout(self.footer_frame)
        self.footer_layout.setSpacing(10)
        self.footer_layout.setObjectName(u"footer_layout")
        self.footer_layout.setContentsMargins(24, 0, 24, 0)
        self.btn_cancel_blf = QPushButton(self.footer_frame)
        self.btn_cancel_blf.setObjectName(u"btn_cancel_blf")
        self.btn_cancel_blf.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/x-circle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_cancel_blf.setIcon(icon)
        self.btn_cancel_blf.setIconSize(QSize(16, 16))

        self.footer_layout.addWidget(self.btn_cancel_blf)

        self.footer_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footer_layout.addItem(self.footer_spacer)

        self.btn_validate_blf = QPushButton(self.footer_frame)
        self.btn_validate_blf.setObjectName(u"btn_validate_blf")
        self.btn_validate_blf.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/check-circle_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_validate_blf.setIcon(icon1)
        self.btn_validate_blf.setIconSize(QSize(16, 16))

        self.footer_layout.addWidget(self.btn_validate_blf)

        self.btn_close = QPushButton(self.footer_frame)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.footer_layout.addWidget(self.btn_close)


        self.root_layout.addWidget(self.footer_frame)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"D\u00e9tail BLF \u2014 Nova Pharma", None))
        self.header_numero.setText(QCoreApplication.translate("Dialog", u"BLF \u2014", None))
        self.header_sub.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.statut_badge.setText(QCoreApplication.translate("Dialog", u"BROUILLON", None))
        self.key_fournisseur.setText(QCoreApplication.translate("Dialog", u"FOURNISSEUR", None))
        self.key_ref_ext.setText(QCoreApplication.translate("Dialog", u"R\u00c9F\u00c9RENCE EXTERNE", None))
        self.key_date.setText(QCoreApplication.translate("Dialog", u"DATE DE LIVRAISON", None))
        self.val_fournisseur.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.val_ref_ext.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.val_date.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.key_created.setText(QCoreApplication.translate("Dialog", u"CR\u00c9\u00c9 PAR", None))
        self.key_validated.setText(QCoreApplication.translate("Dialog", u"VALID\u00c9 PAR", None))
        self.key_cancelled.setText(QCoreApplication.translate("Dialog", u"ANNUL\u00c9 PAR", None))
        self.val_created.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.val_validated.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.val_cancelled.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.section_title.setText(QCoreApplication.translate("Dialog", u"D\u00c9TAIL DES PRODUITS", None))
        ___qtablewidgetitem = self.table_lignes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Code", None))
        ___qtablewidgetitem1 = self.table_lignes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Produit", None))
        ___qtablewidgetitem2 = self.table_lignes.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Qt\u00e9", None))
        ___qtablewidgetitem3 = self.table_lignes.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Prix achat", None))
        ___qtablewidgetitem4 = self.table_lignes.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Prix vente", None))
        ___qtablewidgetitem5 = self.table_lignes.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"Total", None))
        ___qtablewidgetitem6 = self.table_lignes.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Stock (avant \u2192 apr\u00e8s)", None))
        self.val_nb_articles.setText(QCoreApplication.translate("Dialog", u"0 article(s)", None))
        self.val_nb_unites.setText(QCoreApplication.translate("Dialog", u"0 unit\u00e9(s)", None))
        self.total_caption.setText(QCoreApplication.translate("Dialog", u"TOTAL ACHAT :", None))
        self.total_value.setText(QCoreApplication.translate("Dialog", u"0 FC", None))
        self.notes_text.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.motif_text.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.btn_cancel_blf.setText(QCoreApplication.translate("Dialog", u"Annuler le BLF", None))
        self.btn_validate_blf.setText(QCoreApplication.translate("Dialog", u"Valider le BLF", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
    # retranslateUi

