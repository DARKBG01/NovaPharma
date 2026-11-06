# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_user_dialogmuQIOe.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QDialog, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)
import Icon_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1080, 800)
        Dialog.setMinimumSize(QSize(960, 700))
        Dialog.setStyleSheet(u"QDialog#Dialog { background: #f0f4f8; }\n"
"QDialog#Dialog QLabel { background: transparent; }")
        self.mainLayout = QVBoxLayout(Dialog)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(Dialog)
        self.header.setObjectName(u"header")
        self.header.setMinimumSize(QSize(0, 88))
        self.header.setMaximumSize(QSize(16777215, 88))
        self.header.setStyleSheet(u"QFrame#header { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #023E8A, stop:1 #0077B6); border: none; }\n"
"QFrame#header QLabel { background: transparent; color: #ffffff; }")
        self.headerLayout = QHBoxLayout(self.header)
        self.headerLayout.setSpacing(16)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(24, -1, 24, -1)
        self.lbl_header_icon = QToolButton(self.header)
        self.lbl_header_icon.setObjectName(u"lbl_header_icon")
        self.lbl_header_icon.setMinimumSize(QSize(44, 44))
        self.lbl_header_icon.setMaximumSize(QSize(44, 44))
        self.lbl_header_icon.setStyleSheet(u"QToolButton { background: rgba(255,255,255,0.15); border-radius: 12px; border: none; padding: 11px; }")
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/user_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.lbl_header_icon.setIcon(icon)
        self.lbl_header_icon.setIconSize(QSize(22, 22))
        self.lbl_header_icon.setAutoRaise(True)

        self.headerLayout.addWidget(self.lbl_header_icon)

        self.headerTitleBox = QVBoxLayout()
        self.headerTitleBox.setSpacing(2)
        self.headerTitleBox.setObjectName(u"headerTitleBox")
        self.lbl_header_title = QLabel(self.header)
        self.lbl_header_title.setObjectName(u"lbl_header_title")
        self.lbl_header_title.setStyleSheet(u"font-size: 18px; font-weight: 800; color: #ffffff; background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_header_title)

        self.lbl_header_sub = QLabel(self.header)
        self.lbl_header_sub.setObjectName(u"lbl_header_sub")
        self.lbl_header_sub.setStyleSheet(u"font-size: 11px; color: rgba(255,255,255,0.75); background: transparent;")

        self.headerTitleBox.addWidget(self.lbl_header_sub)


        self.headerLayout.addLayout(self.headerTitleBox)

        self.headerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerSpacer)

        self.lbl_status_badge = QLabel(self.header)
        self.lbl_status_badge.setObjectName(u"lbl_status_badge")
        self.lbl_status_badge.setVisible(False)
        self.lbl_status_badge.setStyleSheet(u"background: rgba(255,255,255,0.18); color: #ffffff; padding: 6px 12px; border-radius: 10px; font-size: 10px; font-weight: 800; letter-spacing: 1px;")

        self.headerLayout.addWidget(self.lbl_status_badge)


        self.mainLayout.addWidget(self.header)

        self.bodyLayout = QHBoxLayout()
        self.bodyLayout.setSpacing(0)
        self.bodyLayout.setObjectName(u"bodyLayout")
        self.bodyLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QFrame(Dialog)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumSize(QSize(280, 0))
        self.sidebar.setMaximumSize(QSize(280, 16777215))
        self.sidebar.setStyleSheet(u"QFrame#sidebar { background: #ffffff; border-right: 1px solid #e2e8f0; }\n"
"QFrame#sidebar QLabel { background: transparent; }")
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(10)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(24, 24, 24, 24)
        self.lbl_avatar = QLabel(self.sidebar)
        self.lbl_avatar.setObjectName(u"lbl_avatar")
        self.lbl_avatar.setMinimumSize(QSize(96, 96))
        self.lbl_avatar.setMaximumSize(QSize(96, 96))
        self.lbl_avatar.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0077B6, stop:1 #00B4D8); color: #ffffff; border-radius: 48px; font-size: 32px; font-weight: 800;")
        self.lbl_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebarLayout.addWidget(self.lbl_avatar)

        self.lbl_sidebar_name = QLabel(self.sidebar)
        self.lbl_sidebar_name.setObjectName(u"lbl_sidebar_name")
        self.lbl_sidebar_name.setStyleSheet(u"color: #0f172a; font-size: 14px; font-weight: 700;")
        self.lbl_sidebar_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebarLayout.addWidget(self.lbl_sidebar_name)

        self.lbl_sidebar_role = QLabel(self.sidebar)
        self.lbl_sidebar_role.setObjectName(u"lbl_sidebar_role")
        self.lbl_sidebar_role.setStyleSheet(u"color: #64748b; font-size: 11px; font-weight: 600;")
        self.lbl_sidebar_role.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebarLayout.addWidget(self.lbl_sidebar_role)

        self.sidebarSpacerTop = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.sidebarLayout.addItem(self.sidebarSpacerTop)

        self.check_identity = QCheckBox(self.sidebar)
        self.check_identity.setObjectName(u"check_identity")
        self.check_identity.setStyleSheet(u"QCheckBox { color: #475569; font-size: 11px; font-weight: 600; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 10px; spacing: 8px; }\n"
"QCheckBox:checked { background: #dcfce7; border-color: #86efac; color: #15803d; }\n"
"QCheckBox::indicator { width: 16px; height: 16px; }\n"
"QCheckBox::indicator:unchecked { image: url(:/Icon/Icons/circle.svg); }\n"
"QCheckBox::indicator:checked { image: url(:/Icon/Icons/check-circle.svg); }")

        self.sidebarLayout.addWidget(self.check_identity)

        self.check_contact = QCheckBox(self.sidebar)
        self.check_contact.setObjectName(u"check_contact")
        self.check_contact.setStyleSheet(u"QCheckBox { color: #475569; font-size: 11px; font-weight: 600; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 10px; spacing: 8px; }\n"
"QCheckBox:checked { background: #dcfce7; border-color: #86efac; color: #15803d; }\n"
"QCheckBox::indicator { width: 16px; height: 16px; }\n"
"QCheckBox::indicator:unchecked { image: url(:/Icon/Icons/circle.svg); }\n"
"QCheckBox::indicator:checked { image: url(:/Icon/Icons/check-circle.svg); }")

        self.sidebarLayout.addWidget(self.check_contact)

        self.check_role = QCheckBox(self.sidebar)
        self.check_role.setObjectName(u"check_role")
        self.check_role.setStyleSheet(u"QCheckBox { color: #475569; font-size: 11px; font-weight: 600; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 10px; spacing: 8px; }\n"
"QCheckBox:checked { background: #dcfce7; border-color: #86efac; color: #15803d; }\n"
"QCheckBox::indicator { width: 16px; height: 16px; }\n"
"QCheckBox::indicator:unchecked { image: url(:/Icon/Icons/circle.svg); }\n"
"QCheckBox::indicator:checked { image: url(:/Icon/Icons/check-circle.svg); }")

        self.sidebarLayout.addWidget(self.check_role)

        self.check_password = QCheckBox(self.sidebar)
        self.check_password.setObjectName(u"check_password")
        self.check_password.setStyleSheet(u"QCheckBox { color: #475569; font-size: 11px; font-weight: 600; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 10px; spacing: 8px; }\n"
"QCheckBox:checked { background: #dcfce7; border-color: #86efac; color: #15803d; }\n"
"QCheckBox::indicator { width: 16px; height: 16px; }\n"
"QCheckBox::indicator:unchecked { image: url(:/Icon/Icons/circle.svg); }\n"
"QCheckBox::indicator:checked { image: url(:/Icon/Icons/check-circle.svg); }")

        self.sidebarLayout.addWidget(self.check_password)

        self.check_perms = QCheckBox(self.sidebar)
        self.check_perms.setObjectName(u"check_perms")
        self.check_perms.setStyleSheet(u"QCheckBox { color: #475569; font-size: 11px; font-weight: 600; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 10px; spacing: 8px; }\n"
"QCheckBox:checked { background: #dcfce7; border-color: #86efac; color: #15803d; }\n"
"QCheckBox::indicator { width: 16px; height: 16px; }\n"
"QCheckBox::indicator:unchecked { image: url(:/Icon/Icons/circle.svg); }\n"
"QCheckBox::indicator:checked { image: url(:/Icon/Icons/check-circle.svg); }")

        self.sidebarLayout.addWidget(self.check_perms)

        self.sidebarSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarSpacer)

        self.chk_actif = QCheckBox(self.sidebar)
        self.chk_actif.setObjectName(u"chk_actif")
        self.chk_actif.setStyleSheet(u"QCheckBox { color: #0f172a; font-size: 12px; font-weight: 600; background: transparent; }\n"
"QCheckBox::indicator { width: 18px; height: 18px; }")
        self.chk_actif.setChecked(True)

        self.sidebarLayout.addWidget(self.chk_actif)


        self.bodyLayout.addWidget(self.sidebar)

        self.formScroll = QScrollArea(Dialog)
        self.formScroll.setObjectName(u"formScroll")
        self.formScroll.setStyleSheet(u"QScrollArea { background: #f0f4f8; border: none; }")
        self.formScroll.setFrameShape(QFrame.Shape.NoFrame)
        self.formScroll.setWidgetResizable(True)
        self.formContent = QWidget()
        self.formContent.setObjectName(u"formContent")
        self.formContent.setGeometry(QRect(0, 0, 784, 741))
        self.formContent.setStyleSheet(u"QWidget#formContent { background: #f0f4f8; }")
        self.formLayout = QVBoxLayout(self.formContent)
        self.formLayout.setSpacing(14)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(32, 24, 32, 24)
        self.section_identity = QToolButton(self.formContent)
        self.section_identity.setObjectName(u"section_identity")
        self.section_identity.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.section_identity.setStyleSheet(u"QToolButton { color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent; border: none; padding: 0; }")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/user.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.section_identity.setIcon(icon1)
        self.section_identity.setIconSize(QSize(18, 18))
        self.section_identity.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.section_identity.setAutoRaise(True)

        self.formLayout.addWidget(self.section_identity)

        self.grid_identity = QGridLayout()
        self.grid_identity.setObjectName(u"grid_identity")
        self.grid_identity.setHorizontalSpacing(16)
        self.grid_identity.setVerticalSpacing(12)
        self.inp_prenom = QLineEdit(self.formContent)
        self.inp_prenom.setObjectName(u"inp_prenom")
        self.inp_prenom.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.grid_identity.addWidget(self.inp_prenom, 0, 0, 1, 1)

        self.inp_nom = QLineEdit(self.formContent)
        self.inp_nom.setObjectName(u"inp_nom")
        self.inp_nom.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.grid_identity.addWidget(self.inp_nom, 0, 1, 1, 1)

        self.inp_post = QLineEdit(self.formContent)
        self.inp_post.setObjectName(u"inp_post")
        self.inp_post.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.grid_identity.addWidget(self.inp_post, 1, 0, 1, 1)

        self.inp_natio = QComboBox(self.formContent)
        self.inp_natio.setObjectName(u"inp_natio")
        self.inp_natio.setStyleSheet(u"QComboBox { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.grid_identity.addWidget(self.inp_natio, 1, 1, 1, 1)

        self.combo_sexe = QComboBox(self.formContent)
        self.combo_sexe.addItem("")
        self.combo_sexe.addItem("")
        self.combo_sexe.setObjectName(u"combo_sexe")
        self.combo_sexe.setStyleSheet(u"QComboBox { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; min-height: 20px; }\n"
"QComboBox::drop-down { border: none; width: 28px; }\n"
"QComboBox QAbstractItemView { background: #ffffff; color: #0f172a; border: 1px solid #e2e8f0; selection-background-color: #e0f2fe; selection-color: #0f172a; }")

        self.grid_identity.addWidget(self.combo_sexe, 2, 0, 1, 1)

        self.inp_naissance = QDateEdit(self.formContent)
        self.inp_naissance.setObjectName(u"inp_naissance")
        self.inp_naissance.setStyleSheet(u"QDateEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; }")
        self.inp_naissance.setCalendarPopup(True)

        self.grid_identity.addWidget(self.inp_naissance, 2, 1, 1, 1)


        self.formLayout.addLayout(self.grid_identity)

        self.section_contact = QToolButton(self.formContent)
        self.section_contact.setObjectName(u"section_contact")
        self.section_contact.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.section_contact.setStyleSheet(u"QToolButton { color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent; border: none; padding: 0; }")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/phone.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.section_contact.setIcon(icon2)
        self.section_contact.setIconSize(QSize(18, 18))
        self.section_contact.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.section_contact.setAutoRaise(True)

        self.formLayout.addWidget(self.section_contact)

        self.grid_contact = QGridLayout()
        self.grid_contact.setObjectName(u"grid_contact")
        self.grid_contact.setHorizontalSpacing(16)
        self.grid_contact.setVerticalSpacing(12)
        self.inp_email = QLineEdit(self.formContent)
        self.inp_email.setObjectName(u"inp_email")
        self.inp_email.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.grid_contact.addWidget(self.inp_email, 0, 0, 1, 1)

        self.inp_numero = QLineEdit(self.formContent)
        self.inp_numero.setObjectName(u"inp_numero")
        self.inp_numero.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")

        self.grid_contact.addWidget(self.inp_numero, 0, 1, 1, 1)


        self.formLayout.addLayout(self.grid_contact)

        self.section_role = QToolButton(self.formContent)
        self.section_role.setObjectName(u"section_role")
        self.section_role.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.section_role.setStyleSheet(u"QToolButton { color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent; border: none; padding: 0; }")
        icon3 = QIcon()
        icon3.addFile(u":/Icon/Icons/shield.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.section_role.setIcon(icon3)
        self.section_role.setIconSize(QSize(18, 18))
        self.section_role.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.section_role.setAutoRaise(True)

        self.formLayout.addWidget(self.section_role)

        self.combo_role = QComboBox(self.formContent)
        self.combo_role.addItem("")
        self.combo_role.addItem("")
        self.combo_role.addItem("")
        self.combo_role.setObjectName(u"combo_role")
        self.combo_role.setStyleSheet(u"QComboBox { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; min-height: 20px; }\n"
"QComboBox::drop-down { border: none; width: 28px; }\n"
"QComboBox QAbstractItemView { background: #ffffff; color: #0f172a; border: 1px solid #e2e8f0; selection-background-color: #e0f2fe; selection-color: #0f172a; }\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icon/Icons/chevron-down.svg);\n"
"    width: 12px; height: 12px;\n"
"}")

        self.formLayout.addWidget(self.combo_role)

        self.lbl_role_desc = QLabel(self.formContent)
        self.lbl_role_desc.setObjectName(u"lbl_role_desc")
        self.lbl_role_desc.setStyleSheet(u"color: #64748b; font-size: 11px; padding: 8px 12px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;")
        self.lbl_role_desc.setWordWrap(True)

        self.formLayout.addWidget(self.lbl_role_desc)

        self.section_password = QToolButton(self.formContent)
        self.section_password.setObjectName(u"section_password")
        self.section_password.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.section_password.setStyleSheet(u"QToolButton { color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent; border: none; padding: 0; }")
        icon4 = QIcon()
        icon4.addFile(u":/Icon/Icons/lock.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.section_password.setIcon(icon4)
        self.section_password.setIconSize(QSize(18, 18))
        self.section_password.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.section_password.setAutoRaise(True)

        self.formLayout.addWidget(self.section_password)

        self.pwdRow = QHBoxLayout()
        self.pwdRow.setSpacing(8)
        self.pwdRow.setObjectName(u"pwdRow")
        self.inp_pwd = QLineEdit(self.formContent)
        self.inp_pwd.setObjectName(u"inp_pwd")
        self.inp_pwd.setStyleSheet(u"QLineEdit { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; font-size: 12px; color: #0f172a; }\n"
"QLineEdit:focus { border-color: #0077B6; }")
        self.inp_pwd.setEchoMode(QLineEdit.EchoMode.Password)

        self.pwdRow.addWidget(self.inp_pwd)

        self.btn_toggle_pwd = QPushButton(self.formContent)
        self.btn_toggle_pwd.setObjectName(u"btn_toggle_pwd")
        self.btn_toggle_pwd.setMinimumSize(QSize(44, 44))
        self.btn_toggle_pwd.setMaximumSize(QSize(44, 44))
        self.btn_toggle_pwd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_toggle_pwd.setStyleSheet(u"QPushButton { background: #f1f5f9; border: 1.5px solid #e2e8f0; border-radius: 8px; }\n"
"QPushButton:hover { background: #e2e8f0; }")
        icon5 = QIcon()
        icon5.addFile(u":/Icon/Icons/eye.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_toggle_pwd.setIcon(icon5)
        self.btn_toggle_pwd.setIconSize(QSize(18, 18))

        self.pwdRow.addWidget(self.btn_toggle_pwd)

        self.btn_gen_pwd = QPushButton(self.formContent)
        self.btn_gen_pwd.setObjectName(u"btn_gen_pwd")
        self.btn_gen_pwd.setMinimumSize(QSize(0, 44))
        self.btn_gen_pwd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_gen_pwd.setStyleSheet(u"QPushButton { background: #e0f2fe; color: #0077B6; border: 1px solid #bae6fd; border-radius: 8px; font-size: 12px; font-weight: 700; padding: 0 16px; }\n"
"QPushButton:hover { background: #bae6fd; }")

        self.pwdRow.addWidget(self.btn_gen_pwd)


        self.formLayout.addLayout(self.pwdRow)

        self.chk_must_change = QCheckBox(self.formContent)
        self.chk_must_change.setObjectName(u"chk_must_change")
        self.chk_must_change.setStyleSheet(u"QCheckBox { color: #475569; font-size: 11px; background: transparent; }")

        self.formLayout.addWidget(self.chk_must_change)

        self.section_perms = QToolButton(self.formContent)
        self.section_perms.setObjectName(u"section_perms")
        self.section_perms.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.section_perms.setStyleSheet(u"QToolButton { color: #023E8A; font-size: 12px; font-weight: 800; letter-spacing: 1.2px; background: transparent; border: none; padding: 0; }")
        icon6 = QIcon()
        icon6.addFile(u":/Icon/Icons/key.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.section_perms.setIcon(icon6)
        self.section_perms.setIconSize(QSize(18, 18))
        self.section_perms.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.section_perms.setAutoRaise(True)

        self.formLayout.addWidget(self.section_perms)

        self.lbl_perm_info = QLabel(self.formContent)
        self.lbl_perm_info.setObjectName(u"lbl_perm_info")
        self.lbl_perm_info.setStyleSheet(u"color: #64748b; font-size: 11px; padding: 8px 12px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;")
        self.lbl_perm_info.setWordWrap(True)

        self.formLayout.addWidget(self.lbl_perm_info)

        self.perms_container = QWidget(self.formContent)
        self.perms_container.setObjectName(u"perms_container")
        self.perms_container.setStyleSheet(u"QWidget#perms_container { background: transparent; }")
        self.perms_container_layout = QVBoxLayout(self.perms_container)
        self.perms_container_layout.setSpacing(10)
        self.perms_container_layout.setObjectName(u"perms_container_layout")
        self.perms_container_layout.setContentsMargins(0, 0, 0, 0)

        self.formLayout.addWidget(self.perms_container)

        self.formSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.addItem(self.formSpacer)

        self.formScroll.setWidget(self.formContent)

        self.bodyLayout.addWidget(self.formScroll)


        self.mainLayout.addLayout(self.bodyLayout)

        self.footer = QFrame(Dialog)
        self.footer.setObjectName(u"footer")
        self.footer.setMinimumSize(QSize(0, 72))
        self.footer.setMaximumSize(QSize(16777215, 72))
        self.footer.setStyleSheet(u"QFrame#footer { background: #ffffff; border-top: 1px solid #e2e8f0; }")
        self.footerLayout = QHBoxLayout(self.footer)
        self.footerLayout.setSpacing(12)
        self.footerLayout.setObjectName(u"footerLayout")
        self.footerLayout.setContentsMargins(24, -1, 24, -1)
        self.lbl_error = QLabel(self.footer)
        self.lbl_error.setObjectName(u"lbl_error")
        self.lbl_error.setVisible(False)
        self.lbl_error.setStyleSheet(u"color: #DC2626; font-size: 11px; font-weight: 600; background: transparent;")

        self.footerLayout.addWidget(self.lbl_error)

        self.footerSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.footerLayout.addItem(self.footerSpacer)

        self.btn_cancel = QPushButton(self.footer)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setMinimumSize(QSize(0, 42))
        self.btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cancel.setStyleSheet(u"QPushButton { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 10px; font-size: 12px; font-weight: 700; padding: 0 20px; }\n"
"QPushButton:hover { background: #e2e8f0; }")

        self.footerLayout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton(self.footer)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setMinimumSize(QSize(0, 42))
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.setStyleSheet(u"QPushButton { background: #023E8A; color: #ffffff; border: none; border-radius: 10px; font-size: 12px; font-weight: 800; padding: 0 24px; }\n"
"QPushButton:hover { background: #0077B6; }\n"
"QPushButton:disabled { background: #94a3b8; }")

        self.footerLayout.addWidget(self.btn_save)


        self.mainLayout.addWidget(self.footer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Utilisateur \u2014 Nova Pharma", None))
        self.lbl_header_title.setText(QCoreApplication.translate("Dialog", u"Nouvel utilisateur", None))
        self.lbl_header_sub.setText(QCoreApplication.translate("Dialog", u"D\u00e9finissez les informations et les permissions du compte", None))
        self.lbl_status_badge.setText("")
        self.lbl_avatar.setText(QCoreApplication.translate("Dialog", u"?", None))
        self.lbl_sidebar_name.setText(QCoreApplication.translate("Dialog", u"Nouvel utilisateur", None))
        self.lbl_sidebar_role.setText(QCoreApplication.translate("Dialog", u"\u2014", None))
        self.check_identity.setText(QCoreApplication.translate("Dialog", u"Identit\u00e9 compl\u00e8te", None))
        self.check_contact.setText(QCoreApplication.translate("Dialog", u"Email + t\u00e9l\u00e9phone", None))
        self.check_role.setText(QCoreApplication.translate("Dialog", u"R\u00f4le d\u00e9fini", None))
        self.check_password.setText(QCoreApplication.translate("Dialog", u"Mot de passe", None))
        self.check_perms.setText(QCoreApplication.translate("Dialog", u"Au moins 1 permission", None))
        self.chk_actif.setText(QCoreApplication.translate("Dialog", u"Compte actif", None))
        self.section_identity.setText(QCoreApplication.translate("Dialog", u"IDENTIT\u00c9", None))
        self.inp_prenom.setPlaceholderText(QCoreApplication.translate("Dialog", u"Pr\u00e9nom *", None))
        self.inp_nom.setPlaceholderText(QCoreApplication.translate("Dialog", u"Nom de famille *", None))
        self.inp_post.setPlaceholderText(QCoreApplication.translate("Dialog", u"Post-nom (optionnel)", None))
        self.inp_natio.setPlaceholderText(QCoreApplication.translate("Dialog", u"Nationalit\u00e9", None))
        self.combo_sexe.setItemText(0, QCoreApplication.translate("Dialog", u"M \u2014 Masculin", None))
        self.combo_sexe.setItemText(1, QCoreApplication.translate("Dialog", u"F \u2014 F\u00e9minin", None))

        self.inp_naissance.setDisplayFormat(QCoreApplication.translate("Dialog", u"dd/MM/yyyy", None))
        self.section_contact.setText(QCoreApplication.translate("Dialog", u"CONTACT", None))
        self.inp_email.setPlaceholderText(QCoreApplication.translate("Dialog", u"Email * \u2014 ex : jean@pharma.cd", None))
        self.inp_numero.setPlaceholderText(QCoreApplication.translate("Dialog", u"T\u00e9l\u00e9phone * \u2014 ex : +243 800 000 000", None))
        self.section_role.setText(QCoreApplication.translate("Dialog", u"R\u00d4LE", None))
        self.combo_role.setItemText(0, QCoreApplication.translate("Dialog", u"UTILISATEUR", None))
        self.combo_role.setItemText(1, QCoreApplication.translate("Dialog", u"CAISSIER", None))
        self.combo_role.setItemText(2, QCoreApplication.translate("Dialog", u"ADMIN", None))

        self.lbl_role_desc.setText(QCoreApplication.translate("Dialog", u"Un UTILISATEUR peut vendre et consulter les produits et clients.", None))
        self.section_password.setText(QCoreApplication.translate("Dialog", u"MOT DE PASSE", None))
        self.inp_pwd.setPlaceholderText(QCoreApplication.translate("Dialog", u"Min. 8 caract\u00e8res", None))
        self.btn_toggle_pwd.setText("")
        self.btn_gen_pwd.setText(QCoreApplication.translate("Dialog", u"G\u00e9n\u00e9rer", None))
        self.chk_must_change.setText(QCoreApplication.translate("Dialog", u"Forcer le changement \u00e0 la prochaine connexion", None))
        self.section_perms.setText(QCoreApplication.translate("Dialog", u"PERMISSIONS", None))
        self.lbl_perm_info.setText(QCoreApplication.translate("Dialog", u"Les permissions sont pr\u00e9remplies selon le r\u00f4le choisi. Vous pouvez les ajuster individuellement.", None))
        self.lbl_error.setText("")
        self.btn_cancel.setText(QCoreApplication.translate("Dialog", u"Annuler", None))
        self.btn_save.setText(QCoreApplication.translate("Dialog", u"Cr\u00e9er l'utilisateur", None))
    # retranslateUi

