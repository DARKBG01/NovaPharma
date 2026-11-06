# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_serveurMjDiKm.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_PharmacieServerWidget(object):
    def setupUi(self, PharmacieServerWidget):
        if not PharmacieServerWidget.objectName():
            PharmacieServerWidget.setObjectName(u"PharmacieServerWidget")
        PharmacieServerWidget.resize(1102, 919)
        PharmacieServerWidget.setStyleSheet(u"/* Global Reset */\n"
"QWidget#PharmacieServerWidget {\n"
"    background-color: #f8fafc; /* Gris tr\u00e8s clair pour le fond */\n"
"}\n"
"\n"
"QLabel {\n"
"    font-family: \"Inter\", \"Segoe UI\", sans-serif;\n"
"    color: #334155;\n"
"}\n"
"\n"
"/* En-t\u00eate */\n"
"QLabel#titleLabel {\n"
"    font-size: 26px;\n"
"    font-weight: 800;\n"
"    color: #0f172a;\n"
"    padding-bottom: 5px;\n"
"}\n"
"\n"
"QLabel#serverStatusBadge {\n"
"    background-color: #dcfce7;\n"
"    color: #15803d;\n"
"    padding: 6px 12px;\n"
"    border-radius: 15px;\n"
"    font-weight: bold;\n"
"    border: 1px solid #bbf7d0;\n"
"}\n"
"\n"
"/* Sections / Panels */\n"
"QFrame.ControlPanel {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 12px;\n"
"}\n"
"\n"
"QLabel.SectionHeader {\n"
"    font-size: 12px;\n"
"    font-weight: 800;\n"
"    color: #64748b;\n"
"    text-transform: uppercase;\n"
"    letter-spacing: 1.2px;\n"
"    margin-bottom: 5px;\n"
"}\n"
"\n"
"/* Boutons */\n"
"QPus"
                        "hButton {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    padding: 8px 16px;\n"
"    font-weight: 600;\n"
"    color: #475569;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #f1f5f9;\n"
"    border-color: #cbd5e1;\n"
"}\n"
"\n"
"QPushButton#btnToggleServer {\n"
"    background-color: #2563eb;\n"
"    color: white;\n"
"    border: none;\n"
"    font-size: 13px;\n"
"    letter-spacing: 0.5px;\n"
"}\n"
"\n"
"QPushButton#btnToggleServer:hover {\n"
"    background-color: #1d4ed8;\n"
"}\n"
"\n"
"QPushButton#btnKick {\n"
"    color: #dc2626;\n"
"    border: 1px solid #fecaca;\n"
"}\n"
"\n"
"QPushButton#btnKick:hover {\n"
"    background-color: #fef2f2;\n"
"}\n"
"\n"
"/* Inputs (IP Address) */\n"
"QLineEdit {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"    background: #ffffff;\n"
"    selection-background-color: #93c5fd;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #3b82f6;\n"
"}\n"
"\n"
""
                        "/* Moniteur de logs */\n"
"QTextEdit#logMonitor {\n"
"    background-color: #0f172a;\n"
"    color: #38bdf8;\n"
"    font-family: \"Consolas&quot\",\"Monaco&quot\",\"monospace\";\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"/* Listes */\n"
"QListWidget#listConnected, QListWidget#listWidget {\n"
"    border: 1px solid #e2e8f0;\n"
"    border-radius: 8px;\n"
"    background-color: #ffffff;\n"
"    outline: none;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    padding: 10px;\n"
"    border-bottom: 1px solid #f1f5f9;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: #eff6ff;\n"
"    color: #2563eb;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* Footer */\n"
"QLabel#lblFoot {\n"
"    color: #94a3b8;\n"
"    font-style: italic;\n"
"}")
        self.mainLayout = QVBoxLayout(PharmacieServerWidget)
        self.mainLayout.setSpacing(20)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(30, 30, 30, 30)
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName(u"headerLayout")
        self.titleLabel = QLabel(PharmacieServerWidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.headerLayout.addWidget(self.titleLabel)

        self.horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.horizontalSpacer)

        self.serverStatusBadge = QLabel(PharmacieServerWidget)
        self.serverStatusBadge.setObjectName(u"serverStatusBadge")
        self.serverStatusBadge.setStyleSheet(u"color: #10b981; font-weight: bold;")

        self.headerLayout.addWidget(self.serverStatusBadge)


        self.mainLayout.addLayout(self.headerLayout)

        self.topConfigRow = QHBoxLayout()
        self.topConfigRow.setSpacing(20)
        self.topConfigRow.setObjectName(u"topConfigRow")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, 9, -1)
        self.groupBox_2 = QGroupBox(PharmacieServerWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 2, 1, 1, 1)

        self.progressBar = QProgressBar(self.groupBox_2)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)

        self.progressBar_2 = QProgressBar(self.groupBox_2)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(24)

        self.gridLayout.addWidget(self.progressBar_2, 3, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.controlBox = QFrame(PharmacieServerWidget)
        self.controlBox.setObjectName(u"controlBox")
        self.vControl = QVBoxLayout(self.controlBox)
        self.vControl.setObjectName(u"vControl")
        self.lblCtrl = QLabel(self.controlBox)
        self.lblCtrl.setObjectName(u"lblCtrl")

        self.vControl.addWidget(self.lblCtrl)

        self.btnToggleServer = QPushButton(self.controlBox)
        self.btnToggleServer.setObjectName(u"btnToggleServer")

        self.vControl.addWidget(self.btnToggleServer)

        self.lblIp = QLabel(self.controlBox)
        self.lblIp.setObjectName(u"lblIp")

        self.vControl.addWidget(self.lblIp)

        self.horizontalFrame_ip = QFrame(self.controlBox)
        self.horizontalFrame_ip.setObjectName(u"horizontalFrame_ip")
        self.horizontalFrame_ip.setStyleSheet(u"QLineEdit{\n"
"	font-weight: bold; \n"
"	color: #2563eb;\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.horizontalFrame_ip)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit = QLineEdit(self.horizontalFrame_ip)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.lineEdit)

        self.label = QLabel(self.horizontalFrame_ip)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit_2 = QLineEdit(self.horizontalFrame_ip)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.lineEdit_2)

        self.label_2 = QLabel(self.horizontalFrame_ip)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_3 = QLineEdit(self.horizontalFrame_ip)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.lineEdit_3)

        self.label_3 = QLabel(self.horizontalFrame_ip)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.lineEdit_4 = QLineEdit(self.horizontalFrame_ip)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.lineEdit_4)

        self.label_4 = QLabel(self.horizontalFrame_ip)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.lineEdit_5 = QLineEdit(self.horizontalFrame_ip)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.lineEdit_5)


        self.vControl.addWidget(self.horizontalFrame_ip)

        self.vControl.setStretch(3, 1)

        self.verticalLayout_3.addWidget(self.controlBox)

        self.verticalLayout_3.setStretch(0, 1)

        self.topConfigRow.addLayout(self.verticalLayout_3)

        self.usersBox = QFrame(PharmacieServerWidget)
        self.usersBox.setObjectName(u"usersBox")
        self.vUsers = QVBoxLayout(self.usersBox)
        self.vUsers.setObjectName(u"vUsers")
        self.lblUsers = QLabel(self.usersBox)
        self.lblUsers.setObjectName(u"lblUsers")

        self.vUsers.addWidget(self.lblUsers)

        self.userListLayout = QHBoxLayout()
        self.userListLayout.setObjectName(u"userListLayout")
        self.listConnected = QListWidget(self.usersBox)
        QListWidgetItem(self.listConnected)
        QListWidgetItem(self.listConnected)
        QListWidgetItem(self.listConnected)
        self.listConnected.setObjectName(u"listConnected")

        self.userListLayout.addWidget(self.listConnected)

        self.userActions = QVBoxLayout()
        self.userActions.setObjectName(u"userActions")
        self.btnKick = QPushButton(self.usersBox)
        self.btnKick.setObjectName(u"btnKick")

        self.userActions.addWidget(self.btnKick)

        self.vsU = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.userActions.addItem(self.vsU)


        self.userListLayout.addLayout(self.userActions)

        self.userListLayout.setStretch(0, 1)

        self.vUsers.addLayout(self.userListLayout)


        self.topConfigRow.addWidget(self.usersBox)

        self.frame = QFrame(PharmacieServerWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.listWidget = QListWidget(self.frame)
        self.listWidget.setObjectName(u"listWidget")

        self.horizontalLayout_2.addWidget(self.listWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, 9, 9)
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.topConfigRow.addWidget(self.frame)

        self.topConfigRow.setStretch(0, 1)
        self.topConfigRow.setStretch(1, 1)
        self.topConfigRow.setStretch(2, 1)

        self.mainLayout.addLayout(self.topConfigRow)

        self.lblLog = QLabel(PharmacieServerWidget)
        self.lblLog.setObjectName(u"lblLog")

        self.mainLayout.addWidget(self.lblLog)

        self.logMonitor = QTextEdit(PharmacieServerWidget)
        self.logMonitor.setObjectName(u"logMonitor")
        self.logMonitor.setReadOnly(True)

        self.mainLayout.addWidget(self.logMonitor)

        self.footer = QHBoxLayout()
        self.footer.setObjectName(u"footer")
        self.lblFoot = QLabel(PharmacieServerWidget)
        self.lblFoot.setObjectName(u"lblFoot")
        self.lblFoot.setStyleSheet(u"color: #94a3b8; font-size: 10px;")

        self.footer.addWidget(self.lblFoot)

        self.hsF = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footer.addItem(self.hsF)

        self.btnClearLogs = QPushButton(PharmacieServerWidget)
        self.btnClearLogs.setObjectName(u"btnClearLogs")

        self.footer.addWidget(self.btnClearLogs)


        self.mainLayout.addLayout(self.footer)


        self.retranslateUi(PharmacieServerWidget)

        QMetaObject.connectSlotsByName(PharmacieServerWidget)
    # setupUi

    def retranslateUi(self, PharmacieServerWidget):
        PharmacieServerWidget.setWindowTitle(QCoreApplication.translate("PharmacieServerWidget", u"Console Serveur - Gestion Officine", None))
        self.titleLabel.setText(QCoreApplication.translate("PharmacieServerWidget", u"\U0001f5a5\U0000fe0f Console Centrale du Serveur", None))
        self.serverStatusBadge.setText(QCoreApplication.translate("PharmacieServerWidget", u"\u25cf Serveur Op\u00e9rationnel", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("PharmacieServerWidget", u"PERFORMANCE", None))
        self.label_6.setText(QCoreApplication.translate("PharmacieServerWidget", u"Cpu", None))
        self.label_9.setText(QCoreApplication.translate("PharmacieServerWidget", u"15%", None))
        self.label_8.setText(QCoreApplication.translate("PharmacieServerWidget", u"Ram", None))
        self.label_7.setText(QCoreApplication.translate("PharmacieServerWidget", u"12%", None))
        self.controlBox.setProperty(u"className", QCoreApplication.translate("PharmacieServerWidget", u"ControlPanel", None))
        self.lblCtrl.setText(QCoreApplication.translate("PharmacieServerWidget", u"Contr\u00f4le Flux", None))
        self.lblCtrl.setProperty(u"className", QCoreApplication.translate("PharmacieServerWidget", u"SectionHeader", None))
        self.btnToggleServer.setText(QCoreApplication.translate("PharmacieServerWidget", u"D\u00c9MARRER LE SERVEUR", None))
        self.lblIp.setText(QCoreApplication.translate("PharmacieServerWidget", u"Adresse IP Locale :", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("PharmacieServerWidget", u"XXX", None))
        self.label.setText(QCoreApplication.translate("PharmacieServerWidget", u".", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("PharmacieServerWidget", u"XXX", None))
        self.label_2.setText(QCoreApplication.translate("PharmacieServerWidget", u".", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("PharmacieServerWidget", u"XXX", None))
        self.label_3.setText(QCoreApplication.translate("PharmacieServerWidget", u".", None))
        self.lineEdit_4.setPlaceholderText(QCoreApplication.translate("PharmacieServerWidget", u"XXX", None))
        self.label_4.setText(QCoreApplication.translate("PharmacieServerWidget", u":", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("PharmacieServerWidget", u"XXXX", None))
        self.usersBox.setProperty(u"className", QCoreApplication.translate("PharmacieServerWidget", u"ControlPanel", None))
        self.lblUsers.setText(QCoreApplication.translate("PharmacieServerWidget", u"Comptes Connect\u00e9s (Sessions Actives)", None))
        self.lblUsers.setProperty(u"className", QCoreApplication.translate("PharmacieServerWidget", u"SectionHeader", None))

        __sortingEnabled = self.listConnected.isSortingEnabled()
        self.listConnected.setSortingEnabled(False)
        ___qlistwidgetitem = self.listConnected.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("PharmacieServerWidget", u"\U0001f464 Pharmacien Titulaire (Poste 01)", None));
        ___qlistwidgetitem1 = self.listConnected.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("PharmacieServerWidget", u"\U0001f464 Pr\U000000e9parateur - Sophie (Poste 02)", None));
        ___qlistwidgetitem2 = self.listConnected.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("PharmacieServerWidget", u"\U0001f464 Caisse - Marc (Tablette A)", None));
        self.listConnected.setSortingEnabled(__sortingEnabled)

        self.btnKick.setText(QCoreApplication.translate("PharmacieServerWidget", u"D\u00e9connecter", None))
        self.label_5.setText(QCoreApplication.translate("PharmacieServerWidget", u"Demande de connexions", None))
        self.pushButton.setText(QCoreApplication.translate("PharmacieServerWidget", u"Accorder", None))
        self.lblLog.setText(QCoreApplication.translate("PharmacieServerWidget", u"Journal des Requ\u00eates Clients (Live)", None))
        self.lblLog.setProperty(u"className", QCoreApplication.translate("PharmacieServerWidget", u"SectionHeader", None))
        self.logMonitor.setHtml(QCoreApplication.translate("PharmacieServerWidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Consolas&amp;quot','Monaco&amp;quot','monospace'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Monaco','monospace';\">[14:20:01] CLIENT 192.168.1.12 : Connect\u00e9 </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Monaco','monospace';\">[14:20:05] GET /api/v1/stocks/amoxicilline - 200 OK "
                        "</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Monaco','monospace';\">[14:20:12] POST /api/v1/ventes/nouvelle - Enregistrement r\u00e9ussi </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Monaco','monospace';\">[14:21:45] CLIENT 192.168.1.15 : Demande de synchronisation inventaire </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas','Monaco','monospace'; color:#facc15;\">[14:22:10] WARN : Latence r\u00e9seau d\u00e9tect\u00e9e sur Poste 02</span><span style=\" font-family:'Consolas','Monaco','monospace';\"> </span></p></body></html>", None))
        self.lblFoot.setText(QCoreApplication.translate("PharmacieServerWidget", u"Version Serveur 2.4.0-STABLE", None))
        self.btnClearLogs.setText(QCoreApplication.translate("PharmacieServerWidget", u"Effacer les logs", None))
    # retranslateUi

