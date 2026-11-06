# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_userrAbato.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)
import Icon_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 74)
        Form.setStyleSheet(u"QWidget#Form{\n"
"	\n"
"	background-color: rgb(246, 245, 244);\n"
"}")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(56, 56))
        self.label_3.setMaximumSize(QSize(56, 56))
        self.label_3.setStyleSheet(u"QLabel{\n"
"	background-color: rgb(37, 98, 235);\n"
"	color : #ffffff;\n"
"	border : 1px solid transparent;\n"
"	border-radius : 16px;\n"
"	font-weight : bold;\n"
"	font-size : 18px;\n"
"\n"
"}")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_26 = QLabel(Form)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout.addWidget(self.label_26)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(40, 48))
        self.pushButton.setMaximumSize(QSize(40, 48))
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"	icon: url(:/Icon/Icons/key-svgrepo-com.svg);\n"
"	padding-left : 6px;\n"
"	text-align : center;\n"
"	icon-size : 18px 18px;\n"
"	background-color: rgb(255, 255, 255);\n"
"	border : 1px solid transparent;\n"
"	border-radius : 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	icon: url(:/Icon/Icons/key-svgrepo-com copy.svg);\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/key-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(40, 48))
        self.pushButton_2.setMaximumSize(QSize(40, 48))
        self.pushButton_2.setStyleSheet(u"QPushButton{\n"
"	icon: url(:/Icon/Icons/delete-svgrepo-com copy.svg);\n"
"	padding-left : 6px;\n"
"	text-align : center;\n"
"	icon-size : 18px 18px;\n"
"	background-color: rgb(255, 255, 255);\n"
"	border : 1px solid transparent;\n"
"	border-radius : 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	icon: url(:/Icon/Icons/delete-svgrepo-com.svg);\n"
"}\n"
"")
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"DK", None))
        self.label_26.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; color:#0c0909;\">Mr. KABONGO</span><br/><span style=\" font-size:8pt; font-weight:700; color:#94a3b8;\">ADMINISTRATEUR</span></p></body></html>", None))
        self.pushButton.setText("")
        self.pushButton_2.setText("")
    # retranslateUi

