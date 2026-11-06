# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_client_informationMKBeeb.ui'
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
    QScrollArea, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(960, 720)
        Dialog.setMinimumSize(QSize(900, 640))
        Dialog.setStyleSheet(u"/* ============================================================\n"
"   NOVA PHARMA \u2014 FICHE CLIENT\n"
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
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 HEADER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#header_frame {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:0.4 #0077B6, stop:1 #00B4D8);\n"
"    border-top-left-radius: 16px;\n"
"    border-top-right-radius: 16px;\n"
"    border: none;\n"
"}\n"
"QLabel#avatar {\n"
"    background: rgba(255,255,255,0.20);\n"
"    border: 2px solid rgba(255,255,255,0.40);\n"
"    border-radius: 32px;\n"
"    color: #ffffff;\n"
"    font-size: 22px"
                        ";\n"
"    font-weight: 800;\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}\n"
"QLabel#header_name {\n"
"    color: #ffffff;\n"
"    font-size: 22px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"    letter-spacing: -0.3px;\n"
"}\n"
"QLabel#header_numero {\n"
"    color: #CAF0F8;\n"
"    font-size: 12px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"    font-family: \"Courier New\", monospace;\n"
"}\n"
"QLabel#header_badge_anon {\n"
"    background-color: #fef3c7;\n"
"    color: #92400e;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    border-radius: 10px;\n"
"    padding: 5px 12px;\n"
"}\n"
"QLabel#header_badge_active {\n"
"    background-color: #dcfce7;\n"
"    color: #15803d;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    border-radius: 10px;\n"
"    padding: 5px 12px;\n"
"}\n"
"QLabel#header_badge_inactive {\n"
"    background-color: #f1f5f9;\n"
"    color: #64748b;\n"
"    font-size: 10px;\n"
""
                        "    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    border-radius: 10px;\n"
"    padding: 5px 12px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 CARTE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#card {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-top: none;\n"
"    border-bottom-left-radius: 16px;\n"
"    border-bottom-right-radius: 16px;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 CARTES STATS \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#stat_total {\n"
"    background-color: #eff6ff;\n"
"    border: 1.5px solid #dbeafe;\n"
"    border-left: 4px solid #2563eb;\n"
"    border-radius: 14px;\n"
"}\n"
"QLabel#stat_total_label {\n"
"    color: #1e40af;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    backgro"
                        "und: transparent;\n"
"}\n"
"QLabel#stat_total_value {\n"
"    color: #1e40af;\n"
"    font-size: 22px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QFrame#stat_visits {\n"
"    background-color: #f0fdf4;\n"
"    border: 1.5px solid #bbf7d0;\n"
"    border-left: 4px solid #16a34a;\n"
"    border-radius: 14px;\n"
"}\n"
"QLabel#stat_visits_label {\n"
"    color: #15803d;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    background: transparent;\n"
"}\n"
"QLabel#stat_visits_value {\n"
"    color: #16a34a;\n"
"    font-size: 22px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QFrame#stat_last {\n"
"    background-color: #fff7ed;\n"
"    border: 1.5px solid #fed7aa;\n"
"    border-left: 4px solid #ea580c;\n"
"    border-radius: 14px;\n"
"}\n"
"QLabel#stat_last_label {\n"
"    color: #9a3412;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    background: transparent;\n"
"}\n"
"QLabel#sta"
                        "t_last_value {\n"
"    color: #ea580c;\n"
"    font-size: 18px;\n"
"    font-weight: 800;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 SECTION TITLES \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QLabel#section_title {\n"
"    color: #334155;\n"
"    font-size: 11px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 COORDONN\u00c9ES \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#coord_box {\n"
"    background-color: #f8fafc;\n"
"    border: 1.5px solid #e6ebf2;\n"
"    border-radius: 12px;\n"
"}\n"
"QLabel#coord_key {\n"
"    color: #94a3b8;\n"
"    font-size: 11px;\n"
"    font-weight: 700;\n"
"    background: transparent;\n"
"    letter-spacing: 0.5px;\n"
"}\n"
"QLabel#coord_val {\n"
""
                        "    color: #1e293b;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"    background: transparent;\n"
"}\n"
"QLabel#coord_val_muted {\n"
"    color: #cbd5e1;\n"
"    font-size: 13px;\n"
"    font-weight: 500;\n"
"    font-style: italic;\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 TABLE HISTORIQUE \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QTableWidget#history_table {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e6ebf2;\n"
"    border-radius: 12px;\n"
"    gridline-color: transparent;\n"
"    outline: none;\n"
"    color: #334155;\n"
"    font-size: 12px;\n"
"}\n"
"QTableWidget#history_table::item {\n"
"    padding: 10px 8px;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"    color: #334155;\n"
"}\n"
"QTableWidget#history_table::item:hover {\n"
"    background-color: #f8fafc;\n"
"}\n"
"QTableWidget#history_table::item:selected {\n"
"    background-colo"
                        "r: #eff6ff;\n"
"    color: #0077B6;\n"
"}\n"
"QHeaderView { background-color: transparent; border: none; }\n"
"QHeaderView::section {\n"
"    background-color: #f8fafc;\n"
"    color: #94a3b8;\n"
"    padding: 12px 10px;\n"
"    border: none;\n"
"    border-bottom: 2px solid #e6ebf2;\n"
"    font-size: 10px;\n"
"    font-weight: 800;\n"
"    letter-spacing: 1px;\n"
"    text-transform: uppercase;\n"
"}\n"
"QTableCornerButton::section { background-color: #f8fafc; border: none; }\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 FOOTER \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QFrame#footer_frame {\n"
"    background-color: #f8fafc;\n"
"    border-top: 1px solid #eef2f7;\n"
"    border-bottom-left-radius: 16px;\n"
"    border-bottom-right-radius: 16px;\n"
"}\n"
"\n"
"QPushButton#btn_close {\n"
"    background-color: #ffffff;\n"
"    color: #64748b;\n"
"    border: 1.5px solid #dbe3ec;\n"
"    border-radius: 11px;\n"
""
                        "    padding: 11px 26px;\n"
"    font-size: 13px;\n"
"    font-weight: 600;\n"
"    min-width: 120px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_close:hover {\n"
"    background-color: #f8fafc;\n"
"    color: #0f172a;\n"
"    border-color: #c3cedd;\n"
"}\n"
"\n"
"QPushButton#btn_edit {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #0077B6, stop:1 #00B4D8);\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    border-radius: 11px;\n"
"    padding: 11px 26px;\n"
"    font-size: 13px;\n"
"    font-weight: 800;\n"
"    min-width: 150px;\n"
"    min-height: 42px;\n"
"}\n"
"QPushButton#btn_edit:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"        stop:0 #023E8A, stop:1 #0077B6);\n"
"}\n"
"\n"
"QPushButton#btn_delete {\n"
"    background-color: #ffffff;\n"
"    color: #dc2626;\n"
"    border: 1.5px solid #fecaca;\n"
"    border-radius: 11px;\n"
"    padding: 11px 22px;\n"
"    font-size: 13px;\n"
"    font-weight: 700;\n"
"    min-width: 130px;\n"
" "
                        "   min-height: 42px;\n"
"}\n"
"QPushButton#btn_delete:hover {\n"
"    background-color: #fef2f2;\n"
"    border-color: #fca5a5;\n"
"    color: #b91c1c;\n"
"}\n"
"\n"
"/* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 SCROLLBAR \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"QScrollArea { background: transparent; border: none; }\n"
"QScrollArea > QWidget > QWidget { background-color: #ffffff; }\n"
"QScrollBar:vertical {\n"
"    border: none; background: transparent; width: 10px; margin: 2px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background: #cbd5e1; min-height: 32px; border-radius: 5px;\n"
"}\n"
"QScrollBar::handle:vertical:hover { background: #94a3b8; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }\n"
"")
        self.root_layout = QVBoxLayout(Dialog)
        self.root_layout.setSpacing(0)
        self.root_layout.setObjectName(u"root_layout")
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.header_frame = QFrame(Dialog)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMinimumSize(QSize(0, 120))
        self.header_frame.setMaximumSize(QSize(16777215, 120))
        self.header_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.setSpacing(18)
        self.header_layout.setObjectName(u"header_layout")
        self.header_layout.setContentsMargins(28, 24, 28, 24)
        self.avatar = QLabel(self.header_frame)
        self.avatar.setObjectName(u"avatar")
        self.avatar.setMinimumSize(QSize(64, 64))
        self.avatar.setMaximumSize(QSize(64, 64))
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.header_layout.addWidget(self.avatar)

        self.header_text_layout = QVBoxLayout()
        self.header_text_layout.setSpacing(6)
        self.header_text_layout.setObjectName(u"header_text_layout")
        self.header_name = QLabel(self.header_frame)
        self.header_name.setObjectName(u"header_name")
        self.header_name.setWordWrap(True)

        self.header_text_layout.addWidget(self.header_name)

        self.header_meta_layout = QHBoxLayout()
        self.header_meta_layout.setSpacing(10)
        self.header_meta_layout.setObjectName(u"header_meta_layout")
        self.header_numero = QLabel(self.header_frame)
        self.header_numero.setObjectName(u"header_numero")

        self.header_meta_layout.addWidget(self.header_numero)

        self.header_badge = QLabel(self.header_frame)
        self.header_badge.setObjectName(u"header_badge")

        self.header_meta_layout.addWidget(self.header_badge)

        self.header_meta_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_meta_layout.addItem(self.header_meta_spacer)


        self.header_text_layout.addLayout(self.header_meta_layout)


        self.header_layout.addLayout(self.header_text_layout)

        self.header_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.header_layout.addItem(self.header_spacer)


        self.root_layout.addWidget(self.header_frame)

        self.card = QFrame(Dialog)
        self.card.setObjectName(u"card")
        self.card.setFrameShape(QFrame.Shape.NoFrame)
        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setSpacing(0)
        self.card_layout.setObjectName(u"card_layout")
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea(self.card)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName(u"scroll_content")
        self.scroll_content.setGeometry(QRect(0, 0, 908, 616))
        self.scroll_content.setStyleSheet(u"background-color: #ffffff;")
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setSpacing(18)
        self.content_layout.setObjectName(u"content_layout")
        self.content_layout.setContentsMargins(28, 22, 28, 22)
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(14)
        self.stats_layout.setObjectName(u"stats_layout")
        self.stat_total = QFrame(self.scroll_content)
        self.stat_total.setObjectName(u"stat_total")
        self.stat_total.setMinimumSize(QSize(0, 90))
        self.stat_total.setFrameShape(QFrame.Shape.NoFrame)
        self.stat_total_layout = QVBoxLayout(self.stat_total)
        self.stat_total_layout.setSpacing(4)
        self.stat_total_layout.setObjectName(u"stat_total_layout")
        self.stat_total_layout.setContentsMargins(18, 14, 18, 14)
        self.stat_total_label = QLabel(self.stat_total)
        self.stat_total_label.setObjectName(u"stat_total_label")

        self.stat_total_layout.addWidget(self.stat_total_label)

        self.stat_total_value = QLabel(self.stat_total)
        self.stat_total_value.setObjectName(u"stat_total_value")

        self.stat_total_layout.addWidget(self.stat_total_value)


        self.stats_layout.addWidget(self.stat_total)

        self.stat_visits = QFrame(self.scroll_content)
        self.stat_visits.setObjectName(u"stat_visits")
        self.stat_visits.setMinimumSize(QSize(0, 90))
        self.stat_visits.setFrameShape(QFrame.Shape.NoFrame)
        self.stat_visits_layout = QVBoxLayout(self.stat_visits)
        self.stat_visits_layout.setSpacing(4)
        self.stat_visits_layout.setObjectName(u"stat_visits_layout")
        self.stat_visits_layout.setContentsMargins(18, 14, 18, 14)
        self.stat_visits_label = QLabel(self.stat_visits)
        self.stat_visits_label.setObjectName(u"stat_visits_label")

        self.stat_visits_layout.addWidget(self.stat_visits_label)

        self.stat_visits_value = QLabel(self.stat_visits)
        self.stat_visits_value.setObjectName(u"stat_visits_value")

        self.stat_visits_layout.addWidget(self.stat_visits_value)


        self.stats_layout.addWidget(self.stat_visits)

        self.stat_last = QFrame(self.scroll_content)
        self.stat_last.setObjectName(u"stat_last")
        self.stat_last.setMinimumSize(QSize(0, 90))
        self.stat_last.setFrameShape(QFrame.Shape.NoFrame)
        self.stat_last_layout = QVBoxLayout(self.stat_last)
        self.stat_last_layout.setSpacing(4)
        self.stat_last_layout.setObjectName(u"stat_last_layout")
        self.stat_last_layout.setContentsMargins(18, 14, 18, 14)
        self.stat_last_label = QLabel(self.stat_last)
        self.stat_last_label.setObjectName(u"stat_last_label")

        self.stat_last_layout.addWidget(self.stat_last_label)

        self.stat_last_value = QLabel(self.stat_last)
        self.stat_last_value.setObjectName(u"stat_last_value")

        self.stat_last_layout.addWidget(self.stat_last_value)


        self.stats_layout.addWidget(self.stat_last)


        self.content_layout.addLayout(self.stats_layout)

        self.section_coord = QLabel(self.scroll_content)
        self.section_coord.setObjectName(u"section_coord")

        self.content_layout.addWidget(self.section_coord)

        self.coord_box = QFrame(self.scroll_content)
        self.coord_box.setObjectName(u"coord_box")
        self.coord_box.setFrameShape(QFrame.Shape.NoFrame)
        self.coord_layout = QVBoxLayout(self.coord_box)
        self.coord_layout.setSpacing(12)
        self.coord_layout.setObjectName(u"coord_layout")
        self.coord_layout.setContentsMargins(20, 16, 20, 16)
        self.row_phone = QHBoxLayout()
        self.row_phone.setSpacing(12)
        self.row_phone.setObjectName(u"row_phone")
        self.coord_key_phone = QLabel(self.coord_box)
        self.coord_key_phone.setObjectName(u"coord_key_phone")
        self.coord_key_phone.setMinimumSize(QSize(100, 0))

        self.row_phone.addWidget(self.coord_key_phone)

        self.coord_val_phone = QLabel(self.coord_box)
        self.coord_val_phone.setObjectName(u"coord_val_phone")

        self.row_phone.addWidget(self.coord_val_phone)

        self.phone_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.row_phone.addItem(self.phone_spacer)


        self.coord_layout.addLayout(self.row_phone)

        self.row_email = QHBoxLayout()
        self.row_email.setSpacing(12)
        self.row_email.setObjectName(u"row_email")
        self.coord_key_email = QLabel(self.coord_box)
        self.coord_key_email.setObjectName(u"coord_key_email")
        self.coord_key_email.setMinimumSize(QSize(100, 0))

        self.row_email.addWidget(self.coord_key_email)

        self.coord_val_email = QLabel(self.coord_box)
        self.coord_val_email.setObjectName(u"coord_val_email")

        self.row_email.addWidget(self.coord_val_email)

        self.email_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.row_email.addItem(self.email_spacer)


        self.coord_layout.addLayout(self.row_email)

        self.row_adresse = QHBoxLayout()
        self.row_adresse.setSpacing(12)
        self.row_adresse.setObjectName(u"row_adresse")
        self.coord_key_adresse = QLabel(self.coord_box)
        self.coord_key_adresse.setObjectName(u"coord_key_adresse")
        self.coord_key_adresse.setMinimumSize(QSize(100, 0))

        self.row_adresse.addWidget(self.coord_key_adresse)

        self.coord_val_adresse = QLabel(self.coord_box)
        self.coord_val_adresse.setObjectName(u"coord_val_adresse")
        self.coord_val_adresse.setWordWrap(True)

        self.row_adresse.addWidget(self.coord_val_adresse)

        self.addr_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.row_adresse.addItem(self.addr_spacer)


        self.coord_layout.addLayout(self.row_adresse)

        self.row_notes = QHBoxLayout()
        self.row_notes.setSpacing(12)
        self.row_notes.setObjectName(u"row_notes")
        self.coord_key_notes = QLabel(self.coord_box)
        self.coord_key_notes.setObjectName(u"coord_key_notes")
        self.coord_key_notes.setMinimumSize(QSize(100, 0))

        self.row_notes.addWidget(self.coord_key_notes)

        self.coord_val_notes = QLabel(self.coord_box)
        self.coord_val_notes.setObjectName(u"coord_val_notes")
        self.coord_val_notes.setWordWrap(True)

        self.row_notes.addWidget(self.coord_val_notes)

        self.notes_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.row_notes.addItem(self.notes_spacer)


        self.coord_layout.addLayout(self.row_notes)


        self.content_layout.addWidget(self.coord_box)

        self.section_history = QLabel(self.scroll_content)
        self.section_history.setObjectName(u"section_history")

        self.content_layout.addWidget(self.section_history)

        self.history_table = QTableWidget(self.scroll_content)
        if (self.history_table.columnCount() < 5):
            self.history_table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.history_table.setObjectName(u"history_table")
        self.history_table.setMinimumSize(QSize(0, 220))
        self.history_table.setMaximumSize(QSize(16777215, 320))
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.history_table.setShowGrid(False)
        self.history_table.setRowCount(0)
        self.history_table.setColumnCount(5)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.verticalHeader().setDefaultSectionSize(42)

        self.content_layout.addWidget(self.history_table)

        self.scroll_area.setWidget(self.scroll_content)

        self.card_layout.addWidget(self.scroll_area)

        self.footer_frame = QFrame(self.card)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setMinimumSize(QSize(0, 76))
        self.footer_frame.setMaximumSize(QSize(16777215, 76))
        self.footer_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.footer_layout = QHBoxLayout(self.footer_frame)
        self.footer_layout.setSpacing(10)
        self.footer_layout.setObjectName(u"footer_layout")
        self.footer_layout.setContentsMargins(28, -1, 28, -1)
        self.btn_delete = QPushButton(self.footer_frame)
        self.btn_delete.setObjectName(u"btn_delete")
        self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/trash.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_delete.setIcon(icon)
        self.btn_delete.setIconSize(QSize(14, 14))

        self.footer_layout.addWidget(self.btn_delete)

        self.footer_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footer_layout.addItem(self.footer_spacer)

        self.btn_close = QPushButton(self.footer_frame)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.footer_layout.addWidget(self.btn_close)

        self.btn_edit = QPushButton(self.footer_frame)
        self.btn_edit.setObjectName(u"btn_edit")
        self.btn_edit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/edit_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_edit.setIcon(icon1)
        self.btn_edit.setIconSize(QSize(14, 14))

        self.footer_layout.addWidget(self.btn_edit)


        self.card_layout.addWidget(self.footer_frame)


        self.root_layout.addWidget(self.card)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Fiche client \u2014 Nova Pharma", None))
        self.avatar.setText(QCoreApplication.translate("Dialog", u"?", None))
        self.header_name.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.header_numero.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.header_badge.setText(QCoreApplication.translate("Dialog", u"ACTIF", None))
        self.stat_total_label.setText(QCoreApplication.translate("Dialog", u"TOTAL ACHET\u00c9", None))
        self.stat_total_value.setText(QCoreApplication.translate("Dialog", u"0,00 FC", None))
        self.stat_visits_label.setText(QCoreApplication.translate("Dialog", u"NOMBRE DE VISITES", None))
        self.stat_visits_value.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.stat_last_label.setText(QCoreApplication.translate("Dialog", u"DERNI\u00c8RE VISITE", None))
        self.stat_last_value.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.section_coord.setText(QCoreApplication.translate("Dialog", u"COORDONN\u00c9ES", None))
        self.coord_key_phone.setText(QCoreApplication.translate("Dialog", u"Num\u00e9ro", None))
        self.coord_val_phone.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.coord_key_email.setText(QCoreApplication.translate("Dialog", u"Email", None))
        self.coord_val_email.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.coord_key_adresse.setText(QCoreApplication.translate("Dialog", u"Adresse", None))
        self.coord_val_adresse.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.coord_key_notes.setText(QCoreApplication.translate("Dialog", u"Notes", None))
        self.coord_val_notes.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.section_history.setText(QCoreApplication.translate("Dialog", u"HISTORIQUE DES ACHATS", None))
        ___qtablewidgetitem = self.history_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Date", None))
        ___qtablewidgetitem1 = self.history_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"N\u00b0 Facture", None))
        ___qtablewidgetitem2 = self.history_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Article", None))
        ___qtablewidgetitem3 = self.history_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Qt\u00e9", None))
        ___qtablewidgetitem4 = self.history_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Total", None))
        self.btn_delete.setText(QCoreApplication.translate("Dialog", u"Supprimer", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
        self.btn_edit.setText(QCoreApplication.translate("Dialog", u"Modifier", None))
    # retranslateUi

