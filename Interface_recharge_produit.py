# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_recharge_produitxpRtRC.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)
import Icon_rc
import Icon_rc
import Icon_rc
import Icon_rc
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1041, 800)
        Dialog.setStyleSheet(u"/* Fond g\u00e9n\u00e9ral */\n"
"QDialog#Dialog {\n"
"    background-color: #f8fafc;\n"
"    font-family: \"Segoe UI\", \"Plus Jakarta Sans\", sans-serif;\n"
"}\n"
"\n"
"/* Forcer couleurs ind\u00e9pendantes du th\u00e8me syst\u00e8me */\n"
"QWidget {\n"
"    background-color: #f8fafc;\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"/* HEADER - Glass card effect */\n"
"QWidget#headerWidget {\n"
"    background: rgba(255, 255, 255, 0.9);\n"
"    border-bottom: 1px solid rgba(241, 245, 249, 1);\n"
"    min-height: 80px;\n"
"    max-height: 80px;\n"
"}\n"
"\n"
"/* Bouton fermer */\n"
"QPushButton#pushButton_close {\n"
"    border-radius: 12px;\n"
"    background-color: #f1f5f9;\n"
"    border: none;\n"
"    color: #94a3b8;\n"
"    min-width: 40px;\n"
"    min-height: 40px;\n"
"    max-width: 40px;\n"
"    max-height: 40px;\n"
"    font-size: 16px;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"QPushButton#pushButton_close:hover {\n"
"    background-color: #fee2e2;\n"
"    color: #ef4444;\n"
"}\n"
"\n"
"/* Titre principal */\n"
""
                        "QLabel#label_title {\n"
"    color: #0f172a;\n"
"    font-size: 25px;\n"
"    font-weight: 900;\n"
"    letter-spacing: -0.02em;\n"
"    text-transform: uppercase;\n"
"    font-style: italic;\n"
"}\n"
"\n"
"/* Sous-titre */\n"
"QLabel#label_subtitle {\n"
"    color: #2563eb;\n"
"    font-size: 9px;\n"
"    font-weight: 700;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.2em;\n"
"}\n"
"\n"
"/* Date label */\n"
"QLabel#label_dateTitle {\n"
"    color: #94a3b8;\n"
"    font-size: 9px;\n"
"    font-weight: 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.1em;\n"
"}\n"
"\n"
"QLabel#label_currentDate {\n"
"    color: #0f172a;\n"
"    font-size: 14px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"/* Badge ID */\n"
"QLabel#label_orderId {\n"
"    background-color: #0f172a;\n"
"    color: #ffffff;\n"
"    border-radius: 12px;\n"
"    padding: 8px 20px;\n"
"    font-size: 10px;\n"
"    font-weight: 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.1em;\n"
"}\n"
"\n"
"/* S\u00e9p"
                        "arateur vertical */\n"
"QFrame#separator_vertical {\n"
"    background-color: #e2e8f0;\n"
"    min-width: 1px;\n"
"    max-width: 1px;\n"
"    min-height: 32px;\n"
"}\n"
"\n"
"/* LEFT PANEL - Fond gris clair */\n"
"QWidget#leftPanel {\n"
"    background-color: rgba(248, 250, 252, 0.5);\n"
"}\n"
"\n"
"/* GroupBox Fournisseur - Glass card */\n"
"QGroupBox#groupBox_supplier {\n"
"    background: rgba(255, 255, 255, 0.9);\n"
"    border: 1px solid rgba(241, 245, 249, 1);\n"
"    border-radius: 32px;\n"
"    padding: 24px;\n"
"    margin-top: 0px;\n"
"}\n"
"\n"
"QGroupBox#groupBox_supplier::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0px;\n"
"    color: transparent;\n"
"    font-size: 0px;\n"
"}\n"
"\n"
"/* Label fournisseur */\n"
"QLabel#label_supplierTitle {\n"
"    color: #94a3b8;\n"
"    font-size: 9px;\n"
"    font-weight: 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.1em;\n"
"}\n"
"\n"
"/* ComboBox fournisseur */\n"
"QComboBox#comboBox"
                        "_supplier {\n"
"    border: none;\n"
"    background: transparent;\n"
"    padding: 0px;\n"
"    font-size: 18px;\n"
"    font-weight: 900;\n"
"    color: #0f172a;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"QComboBox#comboBox_supplier::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"}\n"
"\n"
"QComboBox#comboBox_supplier QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    color: #0f172a;\n"
"    border: 1px solid #e5e7eb;\n"
"    border-radius: 12px;\n"
"    padding: 8px;\n"
"    selection-background-color: #dbeafe;\n"
"}\n"
"\n"
"\n"
"/* GroupBox Catalogue - Glass card */\n"
"QGroupBox#groupBox_catalogue {\n"
"    background: rgba(255, 255, 255, 0.9);\n"
"    border: 1px solid #ffffff;\n"
"    border-radius: 40px;\n"
"    padding: 0px;\n"
"    margin-top: 0px;\n"
"}\n"
"\n"
"QGroupBox#groupBox_catalogue::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0px;\n"
"    color: transparent;\n"
"    font-size: 0px;\n"
"}\n"
"\n"
"/* Barre de rec"
                        "herche */\n"
"QWidget#searchWidget {\n"
"    background: transparent;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"    padding: 24px;\n"
"}\n"
"\n"
"QLineEdit#lineEdit_search {\n"
"    border-radius: 24px;\n"
"    border: none;\n"
"    padding: 16px 24px 16px 48px;\n"
"    background-color: rgba(241, 245, 249, 0.5);\n"
"    color: #0f172a;\n"
"    font-size: 12px;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLineEdit#lineEdit_search:focus {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid rgba(37, 99, 235, 0.2);\n"
"}\n"
"\n"
"/* Ic\u00f4ne recherche */\n"
"QLabel#label_searchIcon {\n"
"    color: #94a3b8;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"/* ScrollArea catalogue */\n"
"QScrollArea#scrollArea_catalogue {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QScrollArea#scrollArea_catalogue QWidget#scrollAreaWidgetContents {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 5px;\n"
"    border: none;\n"
"}\n"
"\n"
""
                        "QScrollBar::handle:vertical {\n"
"    background: #cbd5e1;\n"
"    border-radius: 10px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #94a3b8;\n"
"}\n"
"\n"
"/* RIGHT PANEL */\n"
"QWidget#rightPanel {\n"
"    background: rgba(255, 255, 255, 0.9);\n"
"    border-left: 1px solid #f1f5f9;\n"
"}\n"
"\n"
"/* Header panier */\n"
"QWidget#cartHeaderWidget {\n"
"    background: transparent;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"    padding: 32px;\n"
"}\n"
"\n"
"QLabel#label_cartTitle {\n"
"    color: #0f172a;\n"
"    font-size: 14px;\n"
"    font-weight: 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: -0.02em;\n"
"    font-style: italic;\n"
"}\n"
"\n"
"QLabel#label_cartIcon {\n"
"    color: #2563eb;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLabel#label_priceEditable {\n"
"    background-color: #dbeafe;\n"
"    color: #3b82f6;\n"
"    border-radius: 4px;\n"
"    padding: 4px 8px;\n"
"    font-size: 8px;\n"
"    font-weight: 700;\n"
"    text-tran"
                        "sform: uppercase;\n"
"}\n"
"\n"
"/* ScrollArea panier */\n"
"QScrollArea#scrollArea_cart {\n"
"    border: none;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QScrollArea#scrollArea_cart QWidget#scrollAreaWidgetContents_cart {\n"
"    background: transparent;\n"
"}\n"
"\n"
"/* Footer Totaux - Fond noir */\n"
"QWidget#totalsWidget {\n"
"    background-color: #0f172a;\n"
"    border-top-left-radius: 48px;\n"
"    border-top-right-radius: 48px;\n"
"    padding: 32px;\n"
"}\n"
"\n"
"QLabel#label_subtotalTitle,\n"
"QLabel#label_taxTitle {\n"
"    color: rgba(148, 163, 184, 1);\n"
"    font-size: 10px;\n"
"    font-weight: 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.1em;\n"
"}\n"
"\n"
"QLabel#label_subtotal,\n"
"QLabel#label_tax {\n"
"    color: rgba(148, 163, 184, 1);\n"
"    font-size: 10px;\n"
"    font-weight: 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.1em;\n"
"}\n"
"\n"
"QLabel#label_totalTitle {\n"
"    color: #60a5fa;\n"
"    font-size: 10px;\n"
"    font-weight:"
                        " 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.1em;\n"
"}\n"
"\n"
"QLabel#label_total {\n"
"    color: #ffffff;\n"
"    font-size: 36px;\n"
"    font-weight: 900;\n"
"    font-style: italic;\n"
"    letter-spacing: -0.02em;\n"
"}\n"
"\n"
"QFrame#separator_totals {\n"
"    background-color: rgba(255, 255, 255, 0.1);\n"
"    min-height: 1px;\n"
"    max-height: 1px;\n"
"    margin: 16px 0px;\n"
"}\n"
"\n"
"/* Bouton Sauvegarder */\n"
"QPushButton#pushButton_save {\n"
"    border-radius: 24px;\n"
"    background-color: rgba(255, 255, 255, 0.05);\n"
"    border: 1px solid rgba(255, 255, 255, 0.1);\n"
"    color: #ffffff;\n"
"    padding: 16px;\n"
"    font-size: 10px;\n"
"    font-weight: 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.1em;\n"
"}\n"
"\n"
"QPushButton#pushButton_save:hover {\n"
"    background-color: rgba(255, 255, 255, 0.1);\n"
"}\n"
"\n"
"/* Bouton Confirmer - Gradient bleu */\n"
"QPushButton#pushButton_confirm {\n"
"    background: qlineargradient(x1:0, y1:0"
                        ", x2:1, y2:1, stop:0 #2563eb, stop:1 #1d4ed8);\n"
"    border-radius: 24px;\n"
"    border: none;\n"
"    color: #ffffff;\n"
"    padding: 16px;\n"
"    font-size: 10px;\n"
"    font-weight: 900;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 0.1em;\n"
"}\n"
"\n"
"QPushButton#pushButton_confirm:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1d4ed8, stop:1 #1e40af);\n"
"}\n"
"\n"
"/* Tous les autres labels */\n"
"QLabel {\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"/* ComboBox g\u00e9n\u00e9ral */\n"
"QComboBox {\n"
"    border-radius: 12px;\n"
"    border: 1px solid #e5e7eb;\n"
"    padding: 4px 10px;\n"
"    background-color: #ffffff;\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"/* LineEdit g\u00e9n\u00e9ral */\n"
"QLineEdit {\n"
"    border-radius: 12px;\n"
"    border: 1px solid #e5e7eb;\n"
"    padding: 6px 10px;\n"
"    background-color: #f8fafc;\n"
"    color: #0f172a;\n"
""
                        "}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #2563eb;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"/* TableWidget */\n"
"QTableWidget {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e5e7eb;\n"
"    border-radius: 14px;\n"
"    gridline-color: #e5e7eb;\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #f1f5f9;\n"
"    padding: 6px 8px;\n"
"    border: 1px solid #e5e7eb;\n"
"    font-weight: 600;\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    color: #0f172a;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: #dbeafe;\n"
"    color: #1e293b;\n"
"}")
        self.verticalLayout_main = QVBoxLayout(Dialog)
        self.verticalLayout_main.setSpacing(0)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(0, 9, 0, 0)
        self.horizontalLayout_header = QHBoxLayout()
        self.horizontalLayout_header.setSpacing(24)
        self.horizontalLayout_header.setObjectName(u"horizontalLayout_header")
        self.horizontalLayout_header.setContentsMargins(32, 0, 32, 0)
        self.horizontalLayout_headerLeft = QHBoxLayout()
        self.horizontalLayout_headerLeft.setSpacing(24)
        self.horizontalLayout_headerLeft.setObjectName(u"horizontalLayout_headerLeft")
        self.pushButton_close = QPushButton(Dialog)
        self.pushButton_close.setObjectName(u"pushButton_close")

        self.horizontalLayout_headerLeft.addWidget(self.pushButton_close)

        self.verticalLayout_title = QVBoxLayout()
        self.verticalLayout_title.setSpacing(2)
        self.verticalLayout_title.setObjectName(u"verticalLayout_title")
        self.label_title = QLabel(Dialog)
        self.label_title.setObjectName(u"label_title")

        self.verticalLayout_title.addWidget(self.label_title)

        self.label_subtitle = QLabel(Dialog)
        self.label_subtitle.setObjectName(u"label_subtitle")

        self.verticalLayout_title.addWidget(self.label_subtitle)


        self.horizontalLayout_headerLeft.addLayout(self.verticalLayout_title)


        self.horizontalLayout_header.addLayout(self.horizontalLayout_headerLeft)

        self.horizontalSpacer_header = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_header.addItem(self.horizontalSpacer_header)

        self.horizontalLayout_headerRight = QHBoxLayout()
        self.horizontalLayout_headerRight.setSpacing(24)
        self.horizontalLayout_headerRight.setObjectName(u"horizontalLayout_headerRight")
        self.verticalLayout_date = QVBoxLayout()
        self.verticalLayout_date.setSpacing(2)
        self.verticalLayout_date.setObjectName(u"verticalLayout_date")
        self.label_dateTitle = QLabel(Dialog)
        self.label_dateTitle.setObjectName(u"label_dateTitle")
        self.label_dateTitle.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_date.addWidget(self.label_dateTitle)

        self.label_currentDate = QLabel(Dialog)
        self.label_currentDate.setObjectName(u"label_currentDate")

        self.verticalLayout_date.addWidget(self.label_currentDate)


        self.horizontalLayout_headerRight.addLayout(self.verticalLayout_date)

        self.separator_vertical = QFrame(Dialog)
        self.separator_vertical.setObjectName(u"separator_vertical")
        self.separator_vertical.setMinimumSize(QSize(3, 34))
        self.separator_vertical.setMaximumSize(QSize(3, 32))
        self.separator_vertical.setFrameShape(QFrame.Shape.VLine)
        self.separator_vertical.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_headerRight.addWidget(self.separator_vertical)

        self.label_orderId = QLabel(Dialog)
        self.label_orderId.setObjectName(u"label_orderId")

        self.horizontalLayout_headerRight.addWidget(self.label_orderId)


        self.horizontalLayout_header.addLayout(self.horizontalLayout_headerRight)


        self.verticalLayout_main.addLayout(self.horizontalLayout_header)

        self.horizontalLayout_central = QHBoxLayout()
        self.horizontalLayout_central.setSpacing(0)
        self.horizontalLayout_central.setObjectName(u"horizontalLayout_central")
        self.horizontalLayout_central.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_left = QVBoxLayout()
        self.verticalLayout_left.setSpacing(24)
        self.verticalLayout_left.setObjectName(u"verticalLayout_left")
        self.verticalLayout_left.setContentsMargins(24, 24, 24, 24)
        self.groupBox_supplier = QGroupBox(Dialog)
        self.groupBox_supplier.setObjectName(u"groupBox_supplier")
        self.horizontalLayout_supplier = QHBoxLayout(self.groupBox_supplier)
        self.horizontalLayout_supplier.setSpacing(24)
        self.horizontalLayout_supplier.setObjectName(u"horizontalLayout_supplier")
        self.label_truckIcon = QLabel(self.groupBox_supplier)
        self.label_truckIcon.setObjectName(u"label_truckIcon")
        self.label_truckIcon.setStyleSheet(u"#label_truckIcon {\n"
"    background-color: #2563eb;\n"
"    color: #ffffff;\n"
"    border-radius: 16px;\n"
"	padding : 8px;\n"
"    min-width: 32px;\n"
"    min-height: 32px;\n"
"    max-width: 32px;\n"
"    max-height: 32px;\n"
"}")
        self.label_truckIcon.setPixmap(QPixmap(u":/Icon/Icons/truck-svgrepo-com(1).svg"))
        self.label_truckIcon.setScaledContents(True)

        self.horizontalLayout_supplier.addWidget(self.label_truckIcon)

        self.verticalLayout_supplier = QVBoxLayout()
        self.verticalLayout_supplier.setSpacing(4)
        self.verticalLayout_supplier.setObjectName(u"verticalLayout_supplier")
        self.label_supplierTitle = QLabel(self.groupBox_supplier)
        self.label_supplierTitle.setObjectName(u"label_supplierTitle")

        self.verticalLayout_supplier.addWidget(self.label_supplierTitle)

        self.comboBox_supplier = QComboBox(self.groupBox_supplier)
        self.comboBox_supplier.addItem("")
        self.comboBox_supplier.addItem("")
        self.comboBox_supplier.addItem("")
        self.comboBox_supplier.setObjectName(u"comboBox_supplier")

        self.verticalLayout_supplier.addWidget(self.comboBox_supplier)


        self.horizontalLayout_supplier.addLayout(self.verticalLayout_supplier)


        self.verticalLayout_left.addWidget(self.groupBox_supplier)

        self.groupBox_catalogue = QGroupBox(Dialog)
        self.groupBox_catalogue.setObjectName(u"groupBox_catalogue")
        self.verticalLayout_catalogue = QVBoxLayout(self.groupBox_catalogue)
        self.verticalLayout_catalogue.setSpacing(0)
        self.verticalLayout_catalogue.setObjectName(u"verticalLayout_catalogue")
        self.horizontalLayout_search = QHBoxLayout()
        self.horizontalLayout_search.setSpacing(16)
        self.horizontalLayout_search.setObjectName(u"horizontalLayout_search")
        self.horizontalLayout_search.setContentsMargins(24, 24, 24, 24)
        self.label_searchIcon = QLabel(self.groupBox_catalogue)
        self.label_searchIcon.setObjectName(u"label_searchIcon")
        self.label_searchIcon.setMaximumSize(QSize(20, 20))
        self.label_searchIcon.setPixmap(QPixmap(u"../../../../../../../../../../.designer/Icons/search-alt-2-svgrepo-com.svg"))
        self.label_searchIcon.setScaledContents(True)

        self.horizontalLayout_search.addWidget(self.label_searchIcon)

        self.lineEdit_search = QLineEdit(self.groupBox_catalogue)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        self.lineEdit_search.setClearButtonEnabled(True)

        self.horizontalLayout_search.addWidget(self.lineEdit_search)


        self.verticalLayout_catalogue.addLayout(self.horizontalLayout_search)

        self.tableWidget = QTableWidget(self.groupBox_catalogue)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setStyleSheet(u"QTableWidget {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 15px;\n"
"    gridline-color: #f1f5f9;\n"
"    outline: none; /* Enl\u00e8ve les pointill\u00e9s de s\u00e9lection */\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding: 8px;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"    color: #334155;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #eff6ff; /* Blue 50 */\n"
"    color: #1d4ed8; /* Blue 700 */\n"
"}\n"
"\n"
"/* En-t\u00eate du tableau */\n"
"QHeaderView::section {\n"
"    background-color: rgb(248, 250, 252); /* Slate 50 */\n"
"    color: rgb(148, 163, 184); /* Slate 500 */\n"
"    padding: 12px;\n"
"    border: 2px solid transparent;\n"
"    border-bottom: 2px solid #e2e8f0;\n"
"	border-top-left-radius : 15px;\n"
"	border-top-right-radius : 15px;\n"
"    font-weight: bold;\n"
"    text-transform: uppercase;\n"
"    font-size: 11px;\n"
"    letter-spacing: 1px;\n"
"}\n"
"\n"
"QTableWidget::corner {\n"
"    background-color: #"
                        "f8fafc;\n"
"    border: none;\n"
"}\n"
"\n"
"/* --- SCROLLBARS (Style fin et moderne) --- */\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 8px;\n"
"    margin: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #cbd5e1; /* Slate 300 */\n"
"    min-height: 20px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #94a3b8; /* Slate 400 */\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: transparent;\n"
"    height: 8px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: #cbd5e1;\n"
"    min-width: 20px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QLineEdit , QSpinBox{\n"
"	background-color: transparent;\n"
"	border : none;\n"
"	padding-left : 8px;\n"
"    color: #1e293b;\n"
"    font-weight: 500;\n"
"	text-align : center;\n"
"}\n"
"")
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(150)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(40)
        self.tableWidget.verticalHeader().setDefaultSectionSize(44)

        self.verticalLayout_catalogue.addWidget(self.tableWidget)


        self.verticalLayout_left.addWidget(self.groupBox_catalogue)


        self.horizontalLayout_central.addLayout(self.verticalLayout_left)

        self.rightPanel = QFrame(Dialog)
        self.rightPanel.setObjectName(u"rightPanel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightPanel.sizePolicy().hasHeightForWidth())
        self.rightPanel.setSizePolicy(sizePolicy)
        self.rightPanel.setMaximumSize(QSize(16777215, 16777215))
        self.rightPanel.setStyleSheet(u"QFrame#rightPanel{\n"
"	background-color: rgba(255, 255, 255, 0.9);\n"
"\n"
"}")
        self.verticalLayout_right = QVBoxLayout(self.rightPanel)
        self.verticalLayout_right.setSpacing(0)
        self.verticalLayout_right.setObjectName(u"verticalLayout_right")
        self.cartHeaderWidget = QFrame(self.rightPanel)
        self.cartHeaderWidget.setObjectName(u"cartHeaderWidget")
        self.horizontalLayout_cartHeader = QHBoxLayout(self.cartHeaderWidget)
        self.horizontalLayout_cartHeader.setSpacing(8)
        self.horizontalLayout_cartHeader.setObjectName(u"horizontalLayout_cartHeader")
        self.horizontalLayout_cartHeader.setContentsMargins(32, 32, 32, 32)
        self.label_cartIcon = QLabel(self.cartHeaderWidget)
        self.label_cartIcon.setObjectName(u"label_cartIcon")
        self.label_cartIcon.setMaximumSize(QSize(16, 16))
        self.label_cartIcon.setPixmap(QPixmap(u"../../../../../../../../../../.designer/Icons/shopping-bag-svgrepo-com.svg"))
        self.label_cartIcon.setScaledContents(True)

        self.horizontalLayout_cartHeader.addWidget(self.label_cartIcon)

        self.label_cartTitle = QLabel(self.cartHeaderWidget)
        self.label_cartTitle.setObjectName(u"label_cartTitle")

        self.horizontalLayout_cartHeader.addWidget(self.label_cartTitle)

        self.horizontalSpacer_cartHeader = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_cartHeader.addItem(self.horizontalSpacer_cartHeader)

        self.label_priceEditable = QLabel(self.cartHeaderWidget)
        self.label_priceEditable.setObjectName(u"label_priceEditable")

        self.horizontalLayout_cartHeader.addWidget(self.label_priceEditable)


        self.verticalLayout_right.addWidget(self.cartHeaderWidget)

        self.scrollArea_cart = QScrollArea(self.rightPanel)
        self.scrollArea_cart.setObjectName(u"scrollArea_cart")
        self.scrollArea_cart.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_cart.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea_cart.setWidgetResizable(True)
        self.scrollAreaWidgetContents_cart = QWidget()
        self.scrollAreaWidgetContents_cart.setObjectName(u"scrollAreaWidgetContents_cart")
        self.scrollAreaWidgetContents_cart.setGeometry(QRect(0, 0, 426, 192))
        self.verticalLayout_cartItems = QVBoxLayout(self.scrollAreaWidgetContents_cart)
        self.verticalLayout_cartItems.setSpacing(0)
        self.verticalLayout_cartItems.setObjectName(u"verticalLayout_cartItems")
        self.verticalLayout_cartItems.setContentsMargins(15, 0, 15, 0)
        self.scrollArea_cart.setWidget(self.scrollAreaWidgetContents_cart)

        self.verticalLayout_right.addWidget(self.scrollArea_cart)

        self.totalsWidget = QFrame(self.rightPanel)
        self.totalsWidget.setObjectName(u"totalsWidget")
        self.totalsWidget.setStyleSheet(u"QLabel{\n"
"	background-color : transparent;\n"
"}\n"
"\n"
"QPushButton{\n"
"	border-radius : 16px;\n"
"}\n"
"")
        self.verticalLayout_totals = QVBoxLayout(self.totalsWidget)
        self.verticalLayout_totals.setSpacing(24)
        self.verticalLayout_totals.setObjectName(u"verticalLayout_totals")
        self.verticalLayout_totals.setContentsMargins(32, 32, 32, 32)
        self.verticalLayout_totalsDetails = QVBoxLayout()
        self.verticalLayout_totalsDetails.setSpacing(12)
        self.verticalLayout_totalsDetails.setObjectName(u"verticalLayout_totalsDetails")
        self.horizontalLayout_subtotal = QHBoxLayout()
        self.horizontalLayout_subtotal.setObjectName(u"horizontalLayout_subtotal")
        self.label_subtotalTitle = QLabel(self.totalsWidget)
        self.label_subtotalTitle.setObjectName(u"label_subtotalTitle")

        self.horizontalLayout_subtotal.addWidget(self.label_subtotalTitle)

        self.horizontalSpacer_subtotal = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_subtotal.addItem(self.horizontalSpacer_subtotal)

        self.label_subtotal = QLabel(self.totalsWidget)
        self.label_subtotal.setObjectName(u"label_subtotal")

        self.horizontalLayout_subtotal.addWidget(self.label_subtotal)


        self.verticalLayout_totalsDetails.addLayout(self.horizontalLayout_subtotal)

        self.horizontalLayout_tax = QHBoxLayout()
        self.horizontalLayout_tax.setObjectName(u"horizontalLayout_tax")
        self.label_taxTitle = QLabel(self.totalsWidget)
        self.label_taxTitle.setObjectName(u"label_taxTitle")

        self.horizontalLayout_tax.addWidget(self.label_taxTitle)

        self.horizontalSpacer_tax = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_tax.addItem(self.horizontalSpacer_tax)

        self.label_tax = QLabel(self.totalsWidget)
        self.label_tax.setObjectName(u"label_tax")

        self.horizontalLayout_tax.addWidget(self.label_tax)


        self.verticalLayout_totalsDetails.addLayout(self.horizontalLayout_tax)

        self.separator_totals = QFrame(self.totalsWidget)
        self.separator_totals.setObjectName(u"separator_totals")
        self.separator_totals.setFrameShape(QFrame.Shape.HLine)
        self.separator_totals.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_totalsDetails.addWidget(self.separator_totals)

        self.horizontalLayout_total = QHBoxLayout()
        self.horizontalLayout_total.setObjectName(u"horizontalLayout_total")
        self.verticalLayout_totalLabels = QVBoxLayout()
        self.verticalLayout_totalLabels.setSpacing(4)
        self.verticalLayout_totalLabels.setObjectName(u"verticalLayout_totalLabels")
        self.label_totalTitle = QLabel(self.totalsWidget)
        self.label_totalTitle.setObjectName(u"label_totalTitle")

        self.verticalLayout_totalLabels.addWidget(self.label_totalTitle)

        self.label_total = QLabel(self.totalsWidget)
        self.label_total.setObjectName(u"label_total")

        self.verticalLayout_totalLabels.addWidget(self.label_total)


        self.horizontalLayout_total.addLayout(self.verticalLayout_totalLabels)

        self.horizontalSpacer_total = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_total.addItem(self.horizontalSpacer_total)


        self.verticalLayout_totalsDetails.addLayout(self.horizontalLayout_total)


        self.verticalLayout_totals.addLayout(self.verticalLayout_totalsDetails)

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setSpacing(16)
        self.horizontalLayout_buttons.setObjectName(u"horizontalLayout_buttons")
        self.pushButton_save = QPushButton(self.totalsWidget)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout_buttons.addWidget(self.pushButton_save)

        self.pushButton_confirm = QPushButton(self.totalsWidget)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")

        self.horizontalLayout_buttons.addWidget(self.pushButton_confirm)


        self.verticalLayout_totals.addLayout(self.horizontalLayout_buttons)


        self.verticalLayout_right.addWidget(self.totalsWidget)

        self.verticalLayout_right.setStretch(1, 1)

        self.horizontalLayout_central.addWidget(self.rightPanel)

        self.horizontalLayout_central.setStretch(0, 6)
        self.horizontalLayout_central.setStretch(1, 4)

        self.verticalLayout_main.addLayout(self.horizontalLayout_central)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Nouvel approvisionnement", None))
#if QT_CONFIG(tooltip)
        self.pushButton_close.setToolTip(QCoreApplication.translate("Dialog", u"Fermer", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"\u2715", None))
        self.label_title.setText(QCoreApplication.translate("Dialog", u"NOUVEL APPROVISIONNEMENT", None))
        self.label_subtitle.setText(QCoreApplication.translate("Dialog", u"BON DE COMMANDE \u00c9LECTRONIQUE", None))
        self.label_dateTitle.setText(QCoreApplication.translate("Dialog", u"DATE DE CR\u00c9ATION", None))
        self.label_currentDate.setText(QCoreApplication.translate("Dialog", u"--/--/----", None))
        self.label_orderId.setText(QCoreApplication.translate("Dialog", u"ID: BC-2024-089", None))
        self.groupBox_supplier.setTitle("")
        self.label_truckIcon.setText("")
        self.label_supplierTitle.setText(QCoreApplication.translate("Dialog", u"S\u00c9LECTIONNER UN FOURNISSEUR", None))
        self.comboBox_supplier.setItemText(0, QCoreApplication.translate("Dialog", u"PharmaDistri (Grossiste National)", None))
        self.comboBox_supplier.setItemText(1, QCoreApplication.translate("Dialog", u"Medilab SA (Laboratoire)", None))
        self.comboBox_supplier.setItemText(2, QCoreApplication.translate("Dialog", u"BioTech Solutions", None))

        self.groupBox_catalogue.setTitle("")
        self.label_searchIcon.setText("")
        self.lineEdit_search.setPlaceholderText(QCoreApplication.translate("Dialog", u"Rechercher une r\u00e9f\u00e9rence ou un m\u00e9dicament...", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"D\u00e9signation", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Qt\u00e9", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"P.U", None));
        self.label_cartIcon.setText("")
        self.label_cartTitle.setText(QCoreApplication.translate("Dialog", u"PANIER DE COMMANDE", None))
        self.label_priceEditable.setText(QCoreApplication.translate("Dialog", u"PRIX MODIFIABLES", None))
        self.label_subtotalTitle.setText(QCoreApplication.translate("Dialog", u"SOUS-TOTAL HT", None))
        self.label_subtotal.setText(QCoreApplication.translate("Dialog", u"0.00 Fc", None))
        self.label_taxTitle.setText(QCoreApplication.translate("Dialog", u"TVA (20%)", None))
        self.label_tax.setText(QCoreApplication.translate("Dialog", u"0.00 Fc", None))
        self.label_totalTitle.setText(QCoreApplication.translate("Dialog", u"TOTAL NET \u00c0 PAYER", None))
        self.label_total.setText(QCoreApplication.translate("Dialog", u"0.00 Fc", None))
        self.pushButton_save.setText(QCoreApplication.translate("Dialog", u"SAUVEGARDER", None))
        self.pushButton_confirm.setText(QCoreApplication.translate("Dialog", u"CONFIRMER && ENVOYER", None))
    # retranslateUi

