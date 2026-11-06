# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_add_fournisseur_produitVCtaxd.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)
import Icon_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(440, 60)
        Form.setMinimumSize(QSize(0, 50))
        Form.setMaximumSize(QSize(16777215, 60))
        Form.setStyleSheet(u"#Form{\n"
"	background-color: rgb(255, 255, 255);\n"
"	border : 1px solid transparent;\n"
"	border-radius : 24px;\n"
"}\n"
"\n"
"#frame{\n"
"	background-color: rgb(255, 255, 255);\n"
"	border : 1px solid transparent;\n"
"	border-radius : 12px;\n"
"}\n"
"\n"
"#frame:hover{\n"
"	border-color: rgb(59, 130, 246);\n"
"}\n"
"\n"
"\n"
"\n"
"QLabel{\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QSpinBox {\n"
"    background-color: rgba(248, 250, 252, 0.8);\n"
"    border: 1px solid rgba(226, 232, 240, 1);\n"
"    border-radius: 8px;\n"
"    padding: 2px 5px;\n"
"    font-weight: bold;\n"
"    font-style: italic;\n"
"    font-size: 14pt;\n"
"    color: rgb(37, 99, 235);\n"
"}\n"
"\n"
"QSpinBox:focus {\n"
"    border: 1px solid rgb(59, 130, 246);\n"
"    background-color: white;\n"
"}\n"
"\n"
"QSpinBox::up-button, QSpinBox::down-button {\n"
"    width: 0px; \n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 0, -1, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 50))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, -1, 9, 9)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 50))
        self.label_2.setStyleSheet(u"font-size:16pt; \n"
"font-weight:700;\n"
"background-color: transparent;")

        self.horizontalLayout.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignLeft)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label)

        self.priceSpinBox = QSpinBox(self.frame)
        self.priceSpinBox.setObjectName(u"priceSpinBox")
        self.priceSpinBox.setMaximumSize(QSize(100, 16777215))
        self.priceSpinBox.setStyleSheet(u"")
        self.priceSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.priceSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.priceSpinBox.setMaximum(1000000)

        self.verticalLayout_3.addWidget(self.priceSpinBox)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(24, 24))
        self.pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton.setStyleSheet(u"icon : url(:/Icon/Icons/delete-svgrepo-com.svg);\n"
"background-color : white;\n"
"border : none;")
        self.pushButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.pushButton, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.doubleSpinBox = QDoubleSpinBox(self.frame)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setMaximumSize(QSize(90, 16777215))
        self.doubleSpinBox.setStyleSheet(u"background-color : white;\n"
"color : black;\n"
"border : none;")
        self.doubleSpinBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBox.setDecimals(2)
        self.doubleSpinBox.setMaximum(9999999999.989999771118164)

        self.verticalLayout_4.addWidget(self.doubleSpinBox)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Doliprane 500 mg", None))
        self.label.setText(QCoreApplication.translate("Form", u"Quantit\u00e9", None))
        self.pushButton.setText("")
    # retranslateUi

