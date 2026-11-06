# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_user_infoPCHZkn.ui'
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
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(840, 720)
        Dialog.setStyleSheet(u"QDialog#Dialog { background: #f0f4f8; }\n"
"QDialog#Dialog QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(Dialog)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(Dialog)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 120))
        self.header.setMaximumSize(QSize(16777215, 120))
        self.header.setStyleSheet(u"QFrame#header { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #023E8A, stop:1 #0077B6); border: none; }\n"
"QFrame#header QLabel { background: transparent; color: #ffffff; }")
        self.headerLayout = QHBoxLayout(self.header)
        self.headerLayout.setSpacing(16)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(24, -1, 24, -1)
        self.lbl_avatar = QLabel(self.header)
        self.lbl_avatar.setObjectName(u"lbl_avatar")
        self.lbl_avatar.setMinimumSize(QSize(72, 72))
        self.lbl_avatar.setMaximumSize(QSize(72, 72))
        self.lbl_avatar.setStyleSheet(u"background: rgba(255,255,255,0.2); color: #ffffff; border-radius: 36px; font-size: 24px; font-weight: 800;")
        self.lbl_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.headerLayout.addWidget(self.lbl_avatar)

        self.headerInfoBox = QVBoxLayout()
        self.headerInfoBox.setSpacing(4)
        self.headerInfoBox.setObjectName(u"headerInfoBox")
        self.lbl_name = QLabel(self.header)
        self.lbl_name.setObjectName(u"lbl_name")
        self.lbl_name.setStyleSheet(u"font-size: 20px; font-weight: 800; color: #ffffff; background: transparent;")

        self.headerInfoBox.addWidget(self.lbl_name)

        self.lbl_email = QLabel(self.header)
        self.lbl_email.setObjectName(u"lbl_email")
        self.lbl_email.setStyleSheet(u"font-size: 11px; color: rgba(255,255,255,0.8); background: transparent;")

        self.headerInfoBox.addWidget(self.lbl_email)


        self.headerLayout.addLayout(self.headerInfoBox)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.headerBadgesBox = QVBoxLayout()
        self.headerBadgesBox.setSpacing(6)
        self.headerBadgesBox.setObjectName(u"headerBadgesBox")
        self.lbl_role_badge = QLabel(self.header)
        self.lbl_role_badge.setObjectName(u"lbl_role_badge")
        self.lbl_role_badge.setStyleSheet(u"background: rgba(255,255,255,0.2); color: #ffffff; padding: 4px 12px; border-radius: 10px; font-size: 10px; font-weight: 800; letter-spacing: 1px;")
        self.lbl_role_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.headerBadgesBox.addWidget(self.lbl_role_badge)

        self.lbl_status_badge = QLabel(self.header)
        self.lbl_status_badge.setObjectName(u"lbl_status_badge")
        self.lbl_status_badge.setStyleSheet(u"background: #dcfce7; color: #15803d; padding: 4px 12px; border-radius: 10px; font-size: 10px; font-weight: 800; letter-spacing: 1px;")
        self.lbl_status_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.headerBadgesBox.addWidget(self.lbl_status_badge)


        self.headerLayout.addLayout(self.headerBadgesBox)


        self.mainLayout.addWidget(self.header)

        self.tabs = QTabWidget(Dialog)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setStyleSheet(u"QTabWidget::pane { background: #f0f4f8; border: none; }\n"
"QTabBar { background: #ffffff; }\n"
"QTabBar::tab { background: #ffffff; color: #64748b; padding: 12px 20px; font-size: 12px; font-weight: 700; border: none; border-bottom: 3px solid transparent; }\n"
"QTabBar::tab:selected { color: #023E8A; border-bottom: 3px solid #023E8A; }\n"
"QTabBar::tab:hover:!selected { color: #0077B6; }")
        self.tab_infos = QWidget()
        self.tab_infos.setObjectName(u"tab_infos")
        self.tab_infos.setStyleSheet(u"QWidget#tab_infos { background: #f0f4f8; }")
        self.tabInfosLayout = QVBoxLayout(self.tab_infos)
        self.tabInfosLayout.setSpacing(12)
        self.tabInfosLayout.setObjectName(u"tabInfosLayout")
        self.tabInfosLayout.setContentsMargins(24, 20, 24, 20)
        self.info_card = QFrame(self.tab_infos)
        self.info_card.setObjectName(u"info_card")
        self.info_card.setStyleSheet(u"QFrame#info_card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }\n"
"QFrame#info_card QLabel { background: transparent; }")
        self.infoGrid = QGridLayout(self.info_card)
        self.infoGrid.setObjectName(u"infoGrid")
        self.infoGrid.setHorizontalSpacing(24)
        self.infoGrid.setVerticalSpacing(16)
        self.infoGrid.setContentsMargins(20, 20, 20, 20)
        self.lbl_k_prenom = QLabel(self.info_card)
        self.lbl_k_prenom.setObjectName(u"lbl_k_prenom")
        self.lbl_k_prenom.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_prenom, 0, 0, 1, 1)

        self.val_prenom = QLabel(self.info_card)
        self.val_prenom.setObjectName(u"val_prenom")
        self.val_prenom.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_prenom, 0, 1, 1, 1)

        self.lbl_k_nom = QLabel(self.info_card)
        self.lbl_k_nom.setObjectName(u"lbl_k_nom")
        self.lbl_k_nom.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_nom, 1, 0, 1, 1)

        self.val_nom = QLabel(self.info_card)
        self.val_nom.setObjectName(u"val_nom")
        self.val_nom.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_nom, 1, 1, 1, 1)

        self.lbl_k_email = QLabel(self.info_card)
        self.lbl_k_email.setObjectName(u"lbl_k_email")
        self.lbl_k_email.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_email, 2, 0, 1, 1)

        self.val_email = QLabel(self.info_card)
        self.val_email.setObjectName(u"val_email")
        self.val_email.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_email, 2, 1, 1, 1)

        self.lbl_k_numero = QLabel(self.info_card)
        self.lbl_k_numero.setObjectName(u"lbl_k_numero")
        self.lbl_k_numero.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_numero, 3, 0, 1, 1)

        self.val_numero = QLabel(self.info_card)
        self.val_numero.setObjectName(u"val_numero")
        self.val_numero.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_numero, 3, 1, 1, 1)

        self.lbl_k_sexe = QLabel(self.info_card)
        self.lbl_k_sexe.setObjectName(u"lbl_k_sexe")
        self.lbl_k_sexe.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_sexe, 4, 0, 1, 1)

        self.val_sexe = QLabel(self.info_card)
        self.val_sexe.setObjectName(u"val_sexe")
        self.val_sexe.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_sexe, 4, 1, 1, 1)

        self.lbl_k_ddn = QLabel(self.info_card)
        self.lbl_k_ddn.setObjectName(u"lbl_k_ddn")
        self.lbl_k_ddn.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_ddn, 5, 0, 1, 1)

        self.val_ddn = QLabel(self.info_card)
        self.val_ddn.setObjectName(u"val_ddn")
        self.val_ddn.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_ddn, 5, 1, 1, 1)

        self.lbl_k_natio = QLabel(self.info_card)
        self.lbl_k_natio.setObjectName(u"lbl_k_natio")
        self.lbl_k_natio.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_natio, 6, 0, 1, 1)

        self.val_natio = QLabel(self.info_card)
        self.val_natio.setObjectName(u"val_natio")
        self.val_natio.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_natio, 6, 1, 1, 1)

        self.lbl_k_created = QLabel(self.info_card)
        self.lbl_k_created.setObjectName(u"lbl_k_created")
        self.lbl_k_created.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_created, 7, 0, 1, 1)

        self.val_created = QLabel(self.info_card)
        self.val_created.setObjectName(u"val_created")
        self.val_created.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_created, 7, 1, 1, 1)

        self.lbl_k_last = QLabel(self.info_card)
        self.lbl_k_last.setObjectName(u"lbl_k_last")
        self.lbl_k_last.setStyleSheet(u"color: #94a3b8; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.infoGrid.addWidget(self.lbl_k_last, 8, 0, 1, 1)

        self.val_last = QLabel(self.info_card)
        self.val_last.setObjectName(u"val_last")
        self.val_last.setStyleSheet(u"color: #0f172a; font-size: 13px; font-weight: 600;")

        self.infoGrid.addWidget(self.val_last, 8, 1, 1, 1)


        self.tabInfosLayout.addWidget(self.info_card)

        self.infosSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tabInfosLayout.addItem(self.infosSpacer)

        self.tabs.addTab(self.tab_infos, "")
        self.tab_perms = QWidget()
        self.tab_perms.setObjectName(u"tab_perms")
        self.tab_perms.setStyleSheet(u"QWidget#tab_perms { background: #f0f4f8; }")
        self.tabPermsLayout = QVBoxLayout(self.tab_perms)
        self.tabPermsLayout.setSpacing(12)
        self.tabPermsLayout.setObjectName(u"tabPermsLayout")
        self.tabPermsLayout.setContentsMargins(24, 20, 24, 20)
        self.lbl_perms_info = QLabel(self.tab_perms)
        self.lbl_perms_info.setObjectName(u"lbl_perms_info")
        self.lbl_perms_info.setStyleSheet(u"color: #64748b; font-size: 11px; padding: 8px 12px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;")
        self.lbl_perms_info.setWordWrap(True)

        self.tabPermsLayout.addWidget(self.lbl_perms_info)

        self.perms_scroll = QScrollArea(self.tab_perms)
        self.perms_scroll.setObjectName(u"perms_scroll")
        self.perms_scroll.setStyleSheet(u"QScrollArea { background: transparent; border: none; }")
        self.perms_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.perms_scroll.setWidgetResizable(True)
        self.perms_scroll_content = QWidget()
        self.perms_scroll_content.setObjectName(u"perms_scroll_content")
        self.perms_scroll_content.setGeometry(QRect(0, 0, 792, 399))
        self.perms_scroll_content.setStyleSheet(u"QWidget#perms_scroll_content { background: transparent; }")
        self.permsListLayout = QVBoxLayout(self.perms_scroll_content)
        self.permsListLayout.setSpacing(8)
        self.permsListLayout.setObjectName(u"permsListLayout")
        self.perms_scroll.setWidget(self.perms_scroll_content)

        self.tabPermsLayout.addWidget(self.perms_scroll)

        self.tabs.addTab(self.tab_perms, "")
        self.tab_history = QWidget()
        self.tab_history.setObjectName(u"tab_history")
        self.tab_history.setStyleSheet(u"QWidget#tab_history { background: #f0f4f8; }")
        self.tabHistoryLayout = QVBoxLayout(self.tab_history)
        self.tabHistoryLayout.setSpacing(12)
        self.tabHistoryLayout.setObjectName(u"tabHistoryLayout")
        self.tabHistoryLayout.setContentsMargins(24, 20, 24, 20)
        self.history_table = QTableWidget(self.tab_history)
        if (self.history_table.columnCount() < 3):
            self.history_table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.history_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.history_table.setObjectName(u"history_table")
        self.history_table.setStyleSheet(u"QTableWidget { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; gridline-color: transparent; color: #0f172a; }\n"
"QTableWidget::item { padding: 6px; }\n"
"QHeaderView::section { background: #f8fafc; color: #64748b; padding: 8px; border: none; border-bottom: 1px solid #e2e8f0; font-size: 10px; font-weight: 800; }")
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.tabHistoryLayout.addWidget(self.history_table)

        self.tabs.addTab(self.tab_history, "")

        self.mainLayout.addWidget(self.tabs)

        self.footer = QFrame(Dialog)
        self.footer.setObjectName(u"footer")
        self.footer.setMinimumSize(QSize(0, 72))
        self.footer.setMaximumSize(QSize(16777215, 72))
        self.footer.setStyleSheet(u"QFrame#footer { background: #ffffff; border-top: 1px solid #e2e8f0; }")
        self.footerLayout = QHBoxLayout(self.footer)
        self.footerLayout.setSpacing(12)
        self.footerLayout.setObjectName(u"footerLayout")
        self.footerLayout.setContentsMargins(24, -1, 24, -1)
        self.btn_delete = QPushButton(self.footer)
        self.btn_delete.setObjectName(u"btn_delete")
        self.btn_delete.setMinimumSize(QSize(0, 42))
        self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_delete.setStyleSheet(u"QPushButton { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 20px; }\n"
"QPushButton:hover { background: #fee2e2; }")
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/x-circle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_delete.setIcon(icon)
        self.btn_delete.setIconSize(QSize(16, 16))

        self.footerLayout.addWidget(self.btn_delete)

        self.btn_reset_pwd = QPushButton(self.footer)
        self.btn_reset_pwd.setObjectName(u"btn_reset_pwd")
        self.btn_reset_pwd.setMinimumSize(QSize(0, 42))
        self.btn_reset_pwd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_reset_pwd.setStyleSheet(u"QPushButton { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 20px; }\n"
"QPushButton:hover { background: #fef3c7; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/key.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_reset_pwd.setIcon(icon1)
        self.btn_reset_pwd.setIconSize(QSize(16, 16))

        self.footerLayout.addWidget(self.btn_reset_pwd)

        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerLayout.addItem(self.footerSpacer)

        self.btn_close = QPushButton(self.footer)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMinimumSize(QSize(0, 42))
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.setStyleSheet(u"QPushButton { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 24px; }\n"
"QPushButton:hover { background: #e2e8f0; }")

        self.footerLayout.addWidget(self.btn_close)

        self.btn_edit = QPushButton(self.footer)
        self.btn_edit.setObjectName(u"btn_edit")
        self.btn_edit.setMinimumSize(QSize(0, 42))
        self.btn_edit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_edit.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 24px; }\n"
"QPushButton:hover { background: #0077B6; }")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/edit_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_edit.setIcon(icon2)
        self.btn_edit.setIconSize(QSize(16, 16))

        self.footerLayout.addWidget(self.btn_edit)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(Dialog)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Fiche utilisateur \u2014 Nova Pharma", None))
        self.lbl_avatar.setText(QCoreApplication.translate("Dialog", u"?", None))
        self.lbl_name.setText(QCoreApplication.translate("Dialog", u"Nom Pr\u00e9nom", None))
        self.lbl_email.setText(QCoreApplication.translate("Dialog", u"email@exemple.com", None))
        self.lbl_role_badge.setText(QCoreApplication.translate("Dialog", u"ADMIN", None))
        self.lbl_status_badge.setText(QCoreApplication.translate("Dialog", u"ACTIF", None))
        self.lbl_k_prenom.setText(QCoreApplication.translate("Dialog", u"PR\u00c9NOM", None))
        self.val_prenom.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_nom.setText(QCoreApplication.translate("Dialog", u"NOM", None))
        self.val_nom.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_email.setText(QCoreApplication.translate("Dialog", u"EMAIL", None))
        self.val_email.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_numero.setText(QCoreApplication.translate("Dialog", u"T\u00c9L\u00c9PHONE", None))
        self.val_numero.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_sexe.setText(QCoreApplication.translate("Dialog", u"SEXE", None))
        self.val_sexe.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_ddn.setText(QCoreApplication.translate("Dialog", u"DATE DE NAISSANCE", None))
        self.val_ddn.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_natio.setText(QCoreApplication.translate("Dialog", u"NATIONALIT\u00c9", None))
        self.val_natio.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_created.setText(QCoreApplication.translate("Dialog", u"CR\u00c9\u00c9 LE", None))
        self.val_created.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.lbl_k_last.setText(QCoreApplication.translate("Dialog", u"DERNI\u00c8RE CONNEXION", None))
        self.val_last.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_infos), QCoreApplication.translate("Dialog", u"Informations", None))
        self.lbl_perms_info.setText(QCoreApplication.translate("Dialog", u"Permissions actives pour cet utilisateur (lecture seule).", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_perms), QCoreApplication.translate("Dialog", u"Permissions", None))
        ___qtablewidgetitem = self.history_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"DATE", None))
        ___qtablewidgetitem1 = self.history_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"ACTION", None))
        ___qtablewidgetitem2 = self.history_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"D\u00c9TAILS", None))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_history), QCoreApplication.translate("Dialog", u"Historique", None))
        self.btn_delete.setText(QCoreApplication.translate("Dialog", u"D\u00e9sactiver", None))
        self.btn_reset_pwd.setText(QCoreApplication.translate("Dialog", u"R\u00e9initialiser mot de passe", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
        self.btn_edit.setText(QCoreApplication.translate("Dialog", u"Modifier", None))
    # retranslateUi

