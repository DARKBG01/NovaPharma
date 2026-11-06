# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Interface_mainZDlrMm.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QToolButton, QVBoxLayout,
    QWidget)

from widget_animation import AnimatedStackedWidget
import Icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModality.WindowModal)
        MainWindow.resize(1240, 926)
        MainWindow.setMinimumSize(QSize(1100, 700))
        icon = QIcon()
        icon.addFile(u":/Icon/Icons/1758107223736.jpg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"/*\n"
"                ==================================================================\n"
"                NOVA PHARMA \u2014 DESIGN SYSTEM v2\n"
"                ------------------------------------------------------------------\n"
"                Palette\n"
"                Fond app : #eef2f7 -> #f7f9fc (d\u00e9grad\u00e9 tr\u00e8s l\u00e9ger)\n"
"                Cartes : #ffffff / bordure #e6ebf2\n"
"                Primaire : #2563eb (hover #1d4ed8, pressed #1e40af)\n"
"                Sidebar : #0b1220 -> #111c33 (navy profond)\n"
"                Texte : #0f172a / #475569 / #94a3b8\n"
"                Succ\u00e8s #16a34a \u00b7 Danger #dc2626 \u00b7 Warning #d97706\n"
"                Rayons : cartes 18px \u00b7 contr\u00f4les 10-12px \u00b7 boutons nav 12px\n"
"                ================================================================== */\n"
"\n"
"                /* ---------------------------- BASE ---------------------------- */\n"
"                QMainWindow {\n"
"                backgrou"
                        "nd-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.35, y2:1,\n"
"                stop:0 #eef2f7, stop:1 #f8fafc);\n"
"                }\n"
"\n"
"                QWidget {\n"
"                background-color: #f8fafc;\n"
"                color: #0f172a;\n"
"                font-family: \"Segoe UI\", \"Inter\", \"Roboto\",\n"
"                \"Helvetica Neue\", sans-serif;\n"
"                font-size: 13px;\n"
"                outline: none;\n"
"                selection-background-color: #bfdbfe;\n"
"                selection-color: #0f172a;\n"
"                }\n"
"\n"
"                #centralwidget { background-color: transparent; }\n"
"\n"
"                QToolTip {\n"
"                background-color: #0f172a;\n"
"                color: #f8fafc;\n"
"                border: 1px solid #334155;\n"
"                border-radius: 6px;\n"
"                padding: 6px 10px;\n"
"                font-size: 12px;\n"
"                }\n"
"\n"
"                QLabel { background-color: transparent; bord"
                        "er: none; }\n"
"\n"
"                /* S\u00e9parateurs (QLine) */\n"
"                QFrame[frameShape=\"4\"], QFrame[frameShape=\"5\"] {\n"
"                color: #e2e8f0;\n"
"                background-color: #e2e8f0;\n"
"                max-width: 1px;\n"
"                max-height: 1px;\n"
"                }\n"
"\n"
"                /* ------------------------- BARRE LAT\u00c9RALE ------------------------- */\n"
"                #frm_nav {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.6, y2:1,\n"
"                stop:0 #0b1220, stop:1 #16233d);\n"
"                border: none;\n"
"                border-right: 1px solid rgba(255, 255, 255, 18);\n"
"                }\n"
"                #frm_nav > QWidget { background-color: transparent; }\n"
"                #frm_nav QLabel { background-color: transparent; color: #e2e8f0; }\n"
"                #frm_nav QFrame { background-color: transparent; border: none; }\n"
"\n"
"                /* Logo */\n"
"                "
                        "#frame_2 { background-color: transparent; border: none; }\n"
"\n"
"                #label {\n"
"                background-color: transparent;\n"
"                color: #f8fafc;\n"
"                font-size: 15px;\n"
"                font-weight: 700;\n"
"                }\n"
"\n"
"                /* Caption de section */\n"
"                #lbl_nav_section {\n"
"                background-color: transparent;\n"
"                color: #64748b;\n"
"                font-size: 10px;\n"
"                font-weight: 700;\n"
"                letter-spacing: 2px;\n"
"                padding-left: 14px;\n"
"                padding-bottom: 2px;\n"
"                }\n"
"\n"
"                /* Boutons de navigation */\n"
"                #frm_nav QPushButton {\n"
"                background-color: transparent;\n"
"                border: none;\n"
"                border-radius: 12px;\n"
"                min-height: 22px;\n"
"                padding: 11px 14px;\n"
"                margin: 2px 0px;\n"
"             "
                        "   color: #cbd5e1;\n"
"                font-size: 13px;\n"
"                font-weight: 600;\n"
"                text-align: left;\n"
"                }\n"
"                #frm_nav QPushButton:hover {\n"
"                background-color: rgba(255, 255, 255, 20);\n"
"                color: #ffffff;\n"
"                }\n"
"                #frm_nav QPushButton:pressed { background-color: rgba(255, 255, 255, 32); }\n"
"                #frm_nav QPushButton:checked {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"                stop:0 #2563eb, stop:1 #3b82f6);\n"
"                color: #ffffff;\n"
"                border-left: 4px solid #bfdbfe;\n"
"                padding-left: 10px;\n"
"                }\n"
"                #frm_nav QPushButton:checked:hover {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"                stop:0 #1d4ed8, stop:1 #2f74e8);\n"
"                }\n"
"                #frm_nav QPushButto"
                        "n:disabled { color: #475569; }\n"
"\n"
"                /* Carte profil utilisateur */\n"
"                #frame_3 {\n"
"                background-color: rgba(255, 255, 255, 14);\n"
"                border: 1px solid rgba(255, 255, 255, 22);\n"
"                border-radius: 16px;\n"
"                margin: 6px 0px;\n"
"                padding: 4px;\n"
"                }\n"
"                #label_26 { background-color: transparent; color: #f1f5f9; }\n"
"\n"
"                /* ---------------------------- HEADER ---------------------------- */\n"
"                #frame_4 {\n"
"                background-color: rgba(255, 255, 255, 245);\n"
"                border: none;\n"
"                border-bottom: 1px solid #e6ebf2;\n"
"                border-radius: 0px;\n"
"                padding: 4px;\n"
"                }\n"
"\n"
"                #lbl_titre_change {\n"
"                background-color: transparent;\n"
"                font-size: 21px;\n"
"                font-weight: 800;\n"
"                "
                        "color: #0f172a;\n"
"                letter-spacing: -0.2px;\n"
"                }\n"
"\n"
"                #lbl_temps { background-color: transparent; color: #64748b; }\n"
"\n"
"                #edit_recheche_rapide {\n"
"                background-color: #f1f5f9;\n"
"                border: 1px solid transparent;\n"
"                border-radius: 999px;\n"
"                padding: 9px 18px;\n"
"                min-height: 20px;\n"
"                color: #0f172a;\n"
"                font-size: 13px;\n"
"                selection-background-color: #bfdbfe;\n"
"                }\n"
"                #edit_recheche_rapide:hover { background-color: #e8eef6; }\n"
"                #edit_recheche_rapide:focus {\n"
"                background-color: #ffffff;\n"
"                border: 1px solid #2563eb;\n"
"                }\n"
"\n"
"                /* ---------------------- CONTENUS / SCROLL ---------------------- */\n"
"                QStackedWidget, QStackedWidget > QWidget, QScrollArea,\n"
"                QSc"
                        "rollArea > QWidget > QWidget, #scrollAreaWidgetContents {\n"
"                background-color: transparent;\n"
"                border: none;\n"
"                }\n"
"                #page, #page_2, #page_3, #page_4, #page_5, #page_6,\n"
"                #page_7, #page_8, #page_9, #page_10, #page_11, #page_12 {\n"
"                background-color: transparent;\n"
"                }\n"
"\n"
"                /* --------------------------- BOUTONS --------------------------- */\n"
"                QPushButton {\n"
"                background-color: #ffffff;\n"
"                color: #334155;\n"
"                border: 1px solid #dbe3ec;\n"
"                border-radius: 12px;\n"
"                padding: 10px 18px;\n"
"                min-height: 20px;\n"
"                font-size: 13px;\n"
"                font-weight: 600;\n"
"                }\n"
"                QPushButton:hover { background-color: #f8fafc; border-color: #c3cedd; color:\n"
"                #0f172a; }\n"
"                QPushButton:pr"
                        "essed { background-color: #eef2f7; }\n"
"                QPushButton:disabled { background-color: #f1f5f9; color: #a3aec0; border-color:\n"
"                #e6ebf2; }\n"
"                QPushButton:checked { background-color: #eff6ff; border-color: #93c5fd; color:\n"
"                #1d4ed8; }\n"
"\n"
"                /* Primaire (bleu) */\n"
"                #btn_nouvelle_vente, #btn_ajouter_produit, #btn_ajouter_caissier,\n"
"                #btn_add_produit_for_facture, #btn_recheche_person_facture,\n"
"                #btn_blf_new_order, #switch_btn, #btn_generer_pdf, #btn_sauvegarder_imprimer {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                stop:0 #3b82f6, stop:1 #2563eb);\n"
"                color: #ffffff;\n"
"                border: 1px solid #1d4ed8;\n"
"                border-radius: 12px;\n"
"                padding: 11px 20px;\n"
"                font-weight: 700;\n"
"                }\n"
"                #btn_nouvelle_vente:hover, #"
                        "btn_ajouter_produit:hover, #btn_ajouter_caissier:hover,\n"
"                #btn_add_produit_for_facture:hover, #btn_recheche_person_facture:hover,\n"
"                #btn_blf_new_order:hover, #switch_btn:hover, #btn_generer_pdf:hover,\n"
"                #btn_sauvegarder_imprimer:hover {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                stop:0 #2f74e8, stop:1 #1d4ed8);\n"
"                border-color: #1e40af;\n"
"                color: #ffffff;\n"
"                }\n"
"                #btn_nouvelle_vente:pressed, #btn_ajouter_produit:pressed,\n"
"                #btn_ajouter_caissier:pressed,\n"
"                #btn_add_produit_for_facture:pressed, #btn_recheche_person_facture:pressed,\n"
"                #btn_blf_new_order:pressed, #switch_btn:pressed, #btn_generer_pdf:pressed,\n"
"                #btn_sauvegarder_imprimer:pressed {\n"
"                background-color: #1e40af;\n"
"                border-color: #1e3a8a;\n"
"                pad"
                        "ding-top: 12px;\n"
"                }\n"
"\n"
"                /* Bouton blanc sur le hero (gradient) */\n"
"                #frame_5 #btn_nouvelle_vente {\n"
"                background-color: #ffffff;\n"
"                color: #1d4ed8;\n"
"                border: 1px solid #ffffff;\n"
"                font-weight: 800;\n"
"                }\n"
"                #frame_5 #btn_nouvelle_vente:hover { background-color: #eff6ff; border-color:\n"
"                #eff6ff; }\n"
"                #frame_5 #btn_nouvelle_vente:pressed { background-color: #dbeafe; padding-top: 11px;\n"
"                }\n"
"\n"
"                #frame_5 #btn_voir_inventaire {\n"
"                background-color: rgba(255, 255, 255, 38);\n"
"                color: #ffffff;\n"
"                border: 1px solid rgba(255, 255, 255, 120);\n"
"                font-weight: 700;\n"
"                }\n"
"                #frame_5 #btn_voir_inventaire:hover {\n"
"                background-color: rgba(255, 255, 255, 66);\n"
"                bo"
                        "rder-color: rgba(255, 255, 255, 180);\n"
"                color: #ffffff;\n"
"                }\n"
"                #frame_5 #btn_voir_inventaire:pressed { background-color: rgba(255, 255, 255, 90); }\n"
"                /* Succ\u00e8s (vert) */\n"
"                #btn_register_new_client {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                stop:0 #22c55e, stop:1 #16a34a);\n"
"                color: #ffffff;\n"
"                border: 1px solid #15803d;\n"
"                border-radius: 12px;\n"
"                padding: 11px 20px;\n"
"                font-weight: 700;\n"
"                }\n"
"                #btn_register_new_client:hover {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                stop:0 #16a34a, stop:1 #15803d);\n"
"                color: #ffffff;\n"
"                }\n"
"                #btn_register_new_client:pressed { background-color: #166534; padding-top: 12px; }\n"
"\n"
""
                        "                /* Avertissement (jaune) */\n"
"                #btn_modifier_stock {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                stop:0 #facc15, stop:1 #eab308);\n"
"                color: #422006;\n"
"                border: 1px solid #ca8a04;\n"
"                }\n"
"                #btn_modifier_stock:hover {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                stop:0 #eab308, stop:1 #ca8a04);\n"
"                color: #422006;\n"
"                }\n"
"                #btn_modifier_stock:pressed { background-color: #ca8a04; }\n"
"\n"
"                /* Danger (rouge doux) */\n"
"                #btn_voir_rupture_produit {\n"
"                background-color: #ffffff;\n"
"                color: #dc2626;\n"
"                border: 1px solid #fecaca;\n"
"                }\n"
"                #btn_voir_rupture_produit:hover { background-color: #fef2f2; border-color: #fca5a5;\n"
"    "
                        "            color: #b91c1c; }\n"
"                #btn_voir_rupture_produit:pressed { background-color: #fee2e2; }\n"
"\n"
"                /* Secondaire / ghost */\n"
"                #btn_voir_inventaire, #btn_voir_tout_produit, #btn_generer_csv,\n"
"                #btn_blf_new_supplier {\n"
"                background-color: #ffffff;\n"
"                color: #475569;\n"
"                border: 1px solid #dbe3ec;\n"
"                }\n"
"                #btn_voir_tout_produit:hover, #btn_generer_csv:hover, #btn_blf_new_supplier:hover {\n"
"                background-color: #f8fafc;\n"
"                border-color: #c3cedd;\n"
"                color: #0f172a;\n"
"                }\n"
"\n"
"                /* Lien texte (Annuler la saisie) */\n"
"                #btn_clear_table_facture {\n"
"                background-color: transparent;\n"
"                border: none;\n"
"                color: #94a3b8;\n"
"                font-weight: 600;\n"
"                padding: 6px;\n"
"                }\n"
""
                        "                #btn_clear_table_facture:hover { color: #2563eb; background-color: transparent;\n"
"                border: none; }\n"
"\n"
"                /* Impression (sombre) */\n"
"                #btn_print_facture {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                stop:0 #1e293b, stop:1 #0f172a);\n"
"                color: #ffffff;\n"
"                border: 1px solid #0b1220;\n"
"                border-radius: 12px;\n"
"                padding: 12px 18px;\n"
"                font-weight: 700;\n"
"                }\n"
"                #btn_print_facture:hover {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,\n"
"                stop:0 #334155, stop:1 #1e293b);\n"
"                color: #ffffff;\n"
"                }\n"
"                #btn_print_facture:pressed { background-color: #0b1220; }\n"
"\n"
"                /* --------------------------- CHAMPS --------------------------- */\n"
"          "
                        "      QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QDateTimeEdit, QTextEdit,\n"
"                QPlainTextEdit {\n"
"                background-color: #ffffff;\n"
"                border: 1px solid #dbe3ec;\n"
"                border-radius: 11px;\n"
"                padding: 8px 12px;\n"
"                min-height: 20px;\n"
"                color: #0f172a;\n"
"                selection-background-color: #bfdbfe;\n"
"                selection-color: #0f172a;\n"
"                }\n"
"                QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover,\n"
"                QDateEdit:hover, QDateTimeEdit:hover { border-color: #b9c6d8; }\n"
"                QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus,\n"
"                QDateEdit:focus, QDateTimeEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {\n"
"                border: 1px solid #2563eb;\n"
"                background-color: #ffffff;\n"
"                }\n"
"                QLineEdit:disabled, QS"
                        "pinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {\n"
"                background-color: #f1f5f9;\n"
"                color: #94a3b8;\n"
"                border-color: #e6ebf2;\n"
"                }\n"
"                QLineEdit:read-only, QSpinBox:read-only { background-color: #f8fafc; color: #475569;\n"
"                }\n"
"                QLineEdit[readOnly=\"true\"] { background-color: #f8fafc; color: #475569; }\n"
"                QComboBox::drop-down { border: none; width: 26px; }\n"
"                QComboBox QAbstractItemView {\n"
"                background-color: #ffffff;\n"
"                border: 1px solid #e6ebf2;\n"
"                border-radius: 10px;\n"
"                padding: 6px;\n"
"                selection-background-color: #eff6ff;\n"
"                selection-color: #1d4ed8;\n"
"                outline: none;\n"
"                }\n"
"\n"
"                QCheckBox, QRadioButton { background-color: transparent; color: #334155; spacing:\n"
"                8px; }\n"
"  "
                        "              QCheckBox::indicator, QRadioButton::indicator {\n"
"                width: 18px; height: 18px;\n"
"                border: 1px solid #cbd5e1;\n"
"                background-color: #ffffff;\n"
"                border-radius: 5px;\n"
"                }\n"
"                QRadioButton::indicator { border-radius: 9px; }\n"
"                QCheckBox::indicator:hover, QRadioButton::indicator:hover { border-color: #2563eb; }\n"
"                QCheckBox::indicator:checked, QRadioButton::indicator:checked {\n"
"                background-color: #2563eb;\n"
"                border-color: #2563eb;\n"
"                }\n"
"\n"
"                QProgressBar {\n"
"                background-color: #eef2f7;\n"
"                border: 1px solid #e6ebf2;\n"
"                border-radius: 8px;\n"
"                height: 14px;\n"
"                text-align: center;\n"
"                color: #475569;\n"
"                font-size: 10px;\n"
"                font-weight: 700;\n"
"                }\n"
"      "
                        "          QProgressBar::chunk {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\n"
"                stop:0 #3b82f6, stop:1 #2563eb);\n"
"                border-radius: 7px;\n"
"                }\n"
"\n"
"                QGroupBox {\n"
"                background-color: #ffffff;\n"
"                border: 1px solid #e6ebf2;\n"
"                border-radius: 14px;\n"
"                margin-top: 14px;\n"
"                padding-top: 8px;\n"
"                font-weight: 700;\n"
"                color: #0f172a;\n"
"                }\n"
"                QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0px 6px; }\n"
"                QTabWidget::pane { background-color: #ffffff; border: 1px solid #e6ebf2;\n"
"                border-radius: 14px; top: -1px; }\n"
"                QTabBar::tab {\n"
"                background-color: transparent;\n"
"                color: #64748b;\n"
"                padding: 9px 18px;\n"
"                border: none;\n"
""
                        "                border-bottom: 2px solid transparent;\n"
"                font-weight: 700;\n"
"                }\n"
"                QTabBar::tab:hover { color: #2563eb; }\n"
"                QTabBar::tab:selected { color: #2563eb; border-bottom: 2px solid #2563eb; }\n"
"\n"
"                /* --------------------------- CARTES --------------------------- */\n"
"                #frame, #frame_6, #frame_12, #frame_13, #frame_14, #frame_15, #frame_16,\n"
"                #frame_17, #frame_18, #frame_20, #frame_21, #frame_22, #frame_11,\n"
"                #frame_blf_header, #frame_blf_table,\n"
"                #frame_blf_stat1, #frame_blf_stat2, #frame_blf_stat3,\n"
"                #frame_7, #frame_8, #frame_9, #frame_10 {\n"
"                background-color: #ffffff;\n"
"                border: 1px solid #e6ebf2;\n"
"                border-radius: 18px;\n"
"                }\n"
"\n"
"                /* Conteneurs transparents (ne pas cartonner) */\n"
"                #frame_17, #frame_14, #frame_6, #frame_"
                        "blf_stats {\n"
"                background-color: transparent;\n"
"                border: none;\n"
"                }\n"
"\n"
"                /* Cartes de statistiques \u2014 effet de survol */\n"
"                #frame_7, #frame_8, #frame_9, #frame_10 { border-radius: 20px; }\n"
"                #frame_7:hover, #frame_8:hover, #frame_9:hover, #frame_10:hover {\n"
"                border: 1px solid #bfdbfe;\n"
"                background-color: #fdfeff;\n"
"                }\n"
"\n"
"                /* Pastilles d'ic\u00f4nes des cartes */\n"
"                #label_9, #label_12, #label_15, #label_18 {\n"
"                background-color: #eff6ff;\n"
"                border: 1px solid #dbeafe;\n"
"                border-radius: 16px;\n"
"                padding: 10px;\n"
"                }\n"
"                #frame_9 #label_15 { background-color: #fef2f2; border: 1px solid #fee2e2; }\n"
"\n"
"                /* Libell\u00e9s des cartes */\n"
"                #label_10, #label_13, #label_16, #label_19 {\n"
""
                        "                background-color: transparent;\n"
"                color: #94a3b8;\n"
"                font-size: 10px;\n"
"                font-weight: 800;\n"
"                letter-spacing: 1.2px;\n"
"                }\n"
"                #label_11, #label_14, #label_17, #label_20 {\n"
"                background-color: transparent;\n"
"                color: #0f172a;\n"
"                font-size: 27px;\n"
"                font-weight: 800;\n"
"                letter-spacing: -0.5px;\n"
"                }\n"
"                #frame_9 #label_17 { color: #dc2626; }\n"
"\n"
"                /* Hero d'accueil */\n"
"                #frame_5 {\n"
"                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,\n"
"                stop:0 #1d4ed8, stop:0.5 #2563eb, stop:1 #4f46e5);\n"
"                border: 1px solid #1e40af;\n"
"                border-radius: 24px;\n"
"                }\n"
"                #frame_5 QLabel { background-color: transparent; color: #ffffff; }\n"
"           "
                        "     #label_5 { background-color: transparent; color: #ffffff; }\n"
"\n"
"                /* Titres de sections / cartes */\n"
"                #label_4, #label_8, #label_24, #label_37, #label_6, #label_33, #label_34, #label_40\n"
"                {\n"
"                background-color: transparent;\n"
"                color: #0f172a;\n"
"                font-size: 17px;\n"
"                font-weight: 800;\n"
"                letter-spacing: -0.2px;\n"
"                }\n"
"                #label_6 { font-size: 12px; letter-spacing: 1.6px; color: #475569; }\n"
"                #lbl_blf_table_title {\n"
"                background-color: transparent;\n"
"                color: #0f172a;\n"
"                font-size: 12px;\n"
"                font-weight: 800;\n"
"                letter-spacing: 1.4px;\n"
"                }\n"
"\n"
"                /* Champs de formulaire : libell\u00e9s */\n"
"                #label_7, #label_21, #label_22, #label_27, #label_31, #label_38, #label_39 {\n"
"                bac"
                        "kground-color: transparent;\n"
"                color: #64748b;\n"
"                font-size: 11px;\n"
"                font-weight: 700;\n"
"                letter-spacing: 0.4px;\n"
"                padding-bottom: 2px;\n"
"                }\n"
"\n"
"                /* Totaux de la facture */\n"
"                #label_25, #label_28 { background-color: transparent; color: #0f172a; font-weight:\n"
"                800; }\n"
"                #lbl_totale_calc, #lbl_total_nbr_produit {\n"
"                background-color: transparent;\n"
"                color: #16a34a;\n"
"                font-size: 19px;\n"
"                font-weight: 800;\n"
"                }\n"
"\n"
"                /* Num\u00e9ro de facture */\n"
"                #label_23 { background-color: transparent; color: #0f172a; }\n"
"\n"
"                /* --------------------------- TABLEAUX --------------------------- */\n"
"                QTableWidget, QTableView, QTreeWidget, QTreeView, QListWidget, QListView {\n"
"                backg"
                        "round-color: #ffffff;\n"
"                alternate-background-color: #fbfcfe;\n"
"                border: 1px solid #e6ebf2;\n"
"                border-radius: 14px;\n"
"                gridline-color: #f1f5f9;\n"
"                outline: none;\n"
"                color: #334155;\n"
"                }\n"
"                #frame_17 QTableWidget, #frame_14 QTableWidget,\n"
"                #frame_blf_table QTableWidget, #frame_20 QTableWidget {\n"
"                border: none;\n"
"                border-radius: 0px;\n"
"                background-color: transparent;\n"
"                }\n"
"\n"
"                QTableWidget::item, QTableView::item, QTreeWidget::item, QListWidget::item {\n"
"                padding: 10px 8px;\n"
"                border: none;\n"
"                border-bottom: 1px solid #f1f5f9;\n"
"                color: #334155;\n"
"                }\n"
"                QTableWidget::item:hover, QTableView::item:hover,\n"
"                QTreeWidget::item:hover, QListWidget::item:hover { b"
                        "ackground-color: #f8fafc; }\n"
"                QTableWidget::item:selected, QTableView::item:selected,\n"
"                QTreeWidget::item:selected, QListWidget::item:selected {\n"
"                background-color: #eff6ff;\n"
"                color: #1d4ed8;\n"
"                }\n"
"\n"
"                QHeaderView { background-color: transparent; border: none; }\n"
"                QHeaderView::section {\n"
"                background-color: #f8fafc;\n"
"                color: #94a3b8;\n"
"                padding: 12px 10px;\n"
"                border: none;\n"
"                border-bottom: 1px solid #e6ebf2;\n"
"                font-size: 10px;\n"
"                font-weight: 800;\n"
"                letter-spacing: 1px;\n"
"                }\n"
"                QHeaderView::section:first { border-top-left-radius: 14px; }\n"
"                QHeaderView::section:last { border-top-right-radius: 14px; }\n"
"                QTableCornerButton::section { background-color: #f8fafc; border: none; }\n"
"\n"
""
                        "                /* Liste \u00ab Top M\u00e9dicaments \u00bb */\n"
"                #listWidget { background-color: transparent; border: none; }\n"
"                #listWidget::item {\n"
"                background-color: #f8fafc;\n"
"                border: 1px solid #eef2f7;\n"
"                border-radius: 12px;\n"
"                padding: 12px;\n"
"                margin: 3px 0px;\n"
"                color: #334155;\n"
"                }\n"
"                #listWidget::item:hover { background-color: #eff6ff; border-color: #dbeafe; color:\n"
"                #1d4ed8; }\n"
"                #listWidget::item:selected { background-color: #dbeafe; border-color: #93c5fd;\n"
"                color: #1e40af; }\n"
"\n"
"                /* ------------------------- GRAPHIQUES ------------------------- */\n"
"                #graphicsView {\n"
"                background-color: transparent;\n"
"                border: none;\n"
"                border-radius: 12px;\n"
"                }\n"
"\n"
"                /*"
                        " ------------------------- SCROLLBARS ------------------------- */\n"
"                QScrollBar:vertical { border: none; background: transparent; width: 10px; margin:\n"
"                2px; }\n"
"                QScrollBar::handle:vertical { background: #cbd5e1; min-height: 32px; border-radius:\n"
"                5px; }\n"
"                QScrollBar::handle:vertical:hover { background: #94a3b8; }\n"
"                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px;\n"
"                background: transparent; border: none; }\n"
"                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background:\n"
"                transparent; }\n"
"                QScrollBar:horizontal { border: none; background: transparent; height: 10px; margin:\n"
"                2px; }\n"
"                QScrollBar::handle:horizontal { background: #cbd5e1; min-width: 32px; border-radius:\n"
"                5px; }\n"
"                QScrollBar::handle:horizontal:hover { background"
                        ": #94a3b8; }\n"
"                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px;\n"
"                background: transparent; border: none; }\n"
"                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background:\n"
"                transparent; }\n"
"\n"
"                /* ------------------------ MENUS / STATUS ------------------------ */\n"
"                QMenuBar {\n"
"                background-color: #ffffff;\n"
"                color: #475569;\n"
"                border: none;\n"
"                border-bottom: 1px solid #e6ebf2;\n"
"                padding: 2px 8px;\n"
"                font-weight: 600;\n"
"                }\n"
"                QMenuBar::item { background-color: transparent; padding: 6px 12px; border-radius:\n"
"                8px; }\n"
"                QMenuBar::item:selected { background-color: #eff6ff; color: #1d4ed8; }\n"
"                QMenu {\n"
"                background-color: #ffffff;\n"
"                border:"
                        " 1px solid #e6ebf2;\n"
"                border-radius: 12px;\n"
"                padding: 6px;\n"
"                }\n"
"                QMenu::item { padding: 8px 22px; border-radius: 8px; color: #334155; }\n"
"                QMenu::item:selected { background-color: #eff6ff; color: #1d4ed8; }\n"
"                QMenu::separator { height: 1px; background-color: #eef2f7; margin: 5px 8px; }\n"
"                QStatusBar {\n"
"                background-color: #ffffff;\n"
"                color: #64748b;\n"
"                border-top: 1px solid #e6ebf2;\n"
"                font-size: 11px;\n"
"                }\n"
"                QStatusBar::item { border: none; }\n"
"\n"
"                /* --------------------- PAGE BLF / FOURNISSEURS --------------------- */\n"
"                #lbl_blf_title { background-color: transparent; color: #0f172a; font-size: 19px;\n"
"                font-weight: 800; letter-spacing: -0.2px; }\n"
"                #lbl_blf_subtitle {\n"
"                background-color: transpar"
                        "ent;\n"
"                color: #2563eb;\n"
"                font-size: 9px;\n"
"                font-weight: 800;\n"
"                letter-spacing: 2.4px;\n"
"                }\n"
"                #lbl_blf_stat1_label, #lbl_blf_stat2_label, #lbl_blf_stat3_label {\n"
"                background-color: transparent;\n"
"                color: #64748b;\n"
"                font-size: 10px;\n"
"                font-weight: 700;\n"
"                letter-spacing: 0.4px;\n"
"                }\n"
"                #lbl_blf_stat1_value, #lbl_blf_stat2_value, #lbl_blf_stat3_value {\n"
"                background-color: transparent;\n"
"                color: #0f172a;\n"
"                font-size: 22px;\n"
"                font-weight: 800;\n"
"                }\n"
"                #lbl_blf_stat1_icon { background-color: #dbeafe; color: #1d4ed8; border: 1px solid\n"
"                #bfdbfe; border-radius: 16px; }\n"
"                #lbl_blf_stat2_icon { background-color: #dcfce7; color: #15803d; border: 1px solid\n"
""
                        "                #bbf7d0; border-radius: 16px; }\n"
"                #lbl_blf_stat3_icon { background-color: #fee2e2; color: #b91c1c; border: 1px solid\n"
"                #fecaca; border-radius: 16px; }\n"
"\n"
"                /* Ic\u00f4ne de la page courante (header) */\n"
"                #lbl_ico_change {\n"
"                background-color: #eff6ff;\n"
"                image: url(:/Icon/Icons/home-svgrepo-com3.svg);\n"
"                border: 1px solid #dbeafe;\n"
"                border-radius: 13px;\n"
"                padding: 8px;\n"
"                }\n"
"\n"
"                /* \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n"
"                SIDEBAR \u2014 Ic\u00f4nes altern"
                        "\u00e9es selon l'\u00e9tat\n"
"                (normal = ic\u00f4ne bleue \u00b7 coch\u00e9/hover = ic\u00f4ne blanche)\n"
"                \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 */\n"
"\n"
"                /* \u2500\u2500 Accueil \u2500\u2500 */\n"
"                QPushButton#btn_onglet_accueil {\n"
"                icon: url(:/Icon/Icons/home.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_accueil:hover,\n"
"                QPushButton#btn_onglet_accueil:checked {\n"
"                icon: url(:/Icon/Icons/home_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Tableau de bord \u2500\u2500 */\n"
"                QPushButton#btn_ongle"
                        "t_tableau_bord {\n"
"                icon: url(:/Icon/Icons/activity.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_tableau_bord:hover,\n"
"                QPushButton#btn_onglet_tableau_bord:checked {\n"
"                icon: url(:/Icon/Icons/activity_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Articles \u2500\u2500 */\n"
"                QPushButton#btn_onglet_article {\n"
"                icon: url(:/Icon/Icons/pill.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_article:hover,\n"
"                QPushButton#btn_onglet_article:checked {\n"
"                icon: url(:/Icon/Icons/pill_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Clients \u2500\u2500 */\n"
"                QPushButton#btn_onglet_client {\n"
"                icon: url(:/Icon/Icons/users.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_client:hover,\n"
"                QPushButton#btn_onglet_client:checked {\n"
"  "
                        "              icon: url(:/Icon/Icons/users_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Facturation \u2500\u2500 */\n"
"                QPushButton#btn_onglet_facturation {\n"
"                icon: url(:/Icon/Icons/receipt.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_facturation:hover,\n"
"                QPushButton#btn_onglet_facturation:checked {\n"
"                icon: url(:/Icon/Icons/receipt_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 BLF \u2500\u2500 */\n"
"                QPushButton#btn_onglet_blf {\n"
"                icon: url(:/Icon/Icons/truck.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_blf:hover,\n"
"                QPushButton#btn_onglet_blf:checked {\n"
"                icon: url(:/Icon/Icons/truck_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Historique \u2500\u2500 */\n"
"                QPushButton#btn_onglet_historique {\n"
"                icon: "
                        "url(:/Icon/Icons/history.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_historique:hover,\n"
"                QPushButton#btn_onglet_historique:checked {\n"
"                icon: url(:/Icon/Icons/history_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Alerte \u2500\u2500 */\n"
"                QPushButton#btn_onglet_alertes {\n"
"                icon : url(:/Icon/Icons/alert-triangle.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_alertes:hover,\n"
"                QPushButton#btn_onglet_alertes:checked {\n"
"                icon : url(:/Icon/Icons/alert-triangle_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Rapports \u2500\u2500 */\n"
"                QPushButton#btn_onglet_rapport {\n"
"                icon: url(:/Icon/Icons/file-text.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_rapport:hover,\n"
"                QPushButton#btn_onglet_rapport:checked {\n"
"                icon: u"
                        "rl(:/Icon/Icons/file-text_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Audit \u2500\u2500 */\n"
"                QPushButton#btn_onglet_audit {\n"
"                icon: url(:/Icon/Icons/shield-check.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_audit:hover,\n"
"                QPushButton#btn_onglet_audit:checked {\n"
"                icon: url(:/Icon/Icons/shield-check_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Surveillance \u2500\u2500 */\n"
"                QPushButton#btn_onglet_surveillance {\n"
"                icon: url(:/Icon/Icons/shield-alert.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_surveillance:hover,\n"
"                QPushButton#btn_onglet_surveillance:checked {\n"
"                icon: url(:/Icon/Icons/shield-alert_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Utilisateurs \u2500\u2500 */\n"
"                QPushButton#btn_onglet_utilisateur {\n"
""
                        "                icon: url(:/Icon/Icons/user-check.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_utilisateur:hover,\n"
"                QPushButton#btn_onglet_utilisateur:checked {\n"
"                icon: url(:/Icon/Icons/user-check_white.svg);\n"
"                }\n"
"\n"
"                /* \u2500\u2500 Param\u00e8tres \u2500\u2500 */\n"
"                QPushButton#btn_onglet_parametre {\n"
"                icon: url(:/Icon/Icons/settings.svg);\n"
"                }\n"
"                QPushButton#btn_onglet_parametre:hover,\n"
"                QPushButton#btn_onglet_parametre:checked {\n"
"                icon: url(:/Icon/Icons/settings_white.svg);\n"
"                }")
        MainWindow.setDockOptions(QMainWindow.DockOption.AllowTabbedDocks|QMainWindow.DockOption.AnimatedDocks)
        self.action_new_facture = QAction(MainWindow)
        self.action_new_facture.setObjectName(u"action_new_facture")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Icons/invoice.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_new_facture.setIcon(icon1)
        self.action_new_client = QAction(MainWindow)
        self.action_new_client.setObjectName(u"action_new_client")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Icons/user-plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_new_client.setIcon(icon2)
        self.action_new_produit = QAction(MainWindow)
        self.action_new_produit.setObjectName(u"action_new_produit")
        icon3 = QIcon()
        icon3.addFile(u":/Icon/Icons/plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_new_produit.setIcon(icon3)
        self.action_export_db = QAction(MainWindow)
        self.action_export_db.setObjectName(u"action_export_db")
        icon4 = QIcon()
        icon4.addFile(u":/Icon/Icons/download.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_export_db.setIcon(icon4)
        self.action_restore_db = QAction(MainWindow)
        self.action_restore_db.setObjectName(u"action_restore_db")
        icon5 = QIcon()
        icon5.addFile(u":/Icon/Icons/upload.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_restore_db.setIcon(icon5)
        self.action_logout = QAction(MainWindow)
        self.action_logout.setObjectName(u"action_logout")
        icon6 = QIcon()
        icon6.addFile(u":/Icon/Icons/log-out.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_logout.setIcon(icon6)
        self.action_quit = QAction(MainWindow)
        self.action_quit.setObjectName(u"action_quit")
        self.action_quit.setIcon(icon6)
        self.action_actualiser = QAction(MainWindow)
        self.action_actualiser.setObjectName(u"action_actualiser")
        icon7 = QIcon()
        icon7.addFile(u":/Icon/Icons/refresh.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_actualiser.setIcon(icon7)
        self.action_search = QAction(MainWindow)
        self.action_search.setObjectName(u"action_search")
        icon8 = QIcon()
        icon8.addFile(u":/Icon/Icons/search.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_search.setIcon(icon8)
        self.action_clear_panier = QAction(MainWindow)
        self.action_clear_panier.setObjectName(u"action_clear_panier")
        self.action_demarrer_vente = QAction(MainWindow)
        self.action_demarrer_vente.setObjectName(u"action_demarrer_vente")
        icon9 = QIcon()
        icon9.addFile(u":/Icon/Icons/shopping-cart.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_demarrer_vente.setIcon(icon9)
        self.action_ventes_jour = QAction(MainWindow)
        self.action_ventes_jour.setObjectName(u"action_ventes_jour")
        icon10 = QIcon()
        icon10.addFile(u":/Icon/Icons/calendar-check.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_ventes_jour.setIcon(icon10)
        self.action_derniere_facture = QAction(MainWindow)
        self.action_derniere_facture.setObjectName(u"action_derniere_facture")
        icon11 = QIcon()
        icon11.addFile(u":/Icon/Icons/receipt.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_derniere_facture.setIcon(icon11)
        self.action_voir_produits = QAction(MainWindow)
        self.action_voir_produits.setObjectName(u"action_voir_produits")
        icon12 = QIcon()
        icon12.addFile(u":/Icon/Icons/pill.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_voir_produits.setIcon(icon12)
        self.action_ruptures = QAction(MainWindow)
        self.action_ruptures.setObjectName(u"action_ruptures")
        icon13 = QIcon()
        icon13.addFile(u":/Icon/Icons/alert-triangle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_ruptures.setIcon(icon13)
        self.action_new_blf = QAction(MainWindow)
        self.action_new_blf.setObjectName(u"action_new_blf")
        icon14 = QIcon()
        icon14.addFile(u":/Icon/Icons/package.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_new_blf.setIcon(icon14)
        self.action_new_fournisseur = QAction(MainWindow)
        self.action_new_fournisseur.setObjectName(u"action_new_fournisseur")
        icon15 = QIcon()
        icon15.addFile(u":/Icon/Icons/truck.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_new_fournisseur.setIcon(icon15)
        self.action_voir_blf = QAction(MainWindow)
        self.action_voir_blf.setObjectName(u"action_voir_blf")
        icon16 = QIcon()
        icon16.addFile(u":/Icon/Icons/list.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_voir_blf.setIcon(icon16)
        self.action_rapport_ventes = QAction(MainWindow)
        self.action_rapport_ventes.setObjectName(u"action_rapport_ventes")
        icon17 = QIcon()
        icon17.addFile(u":/Icon/Icons/chart-line.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_rapport_ventes.setIcon(icon17)
        self.action_rapport_equipe = QAction(MainWindow)
        self.action_rapport_equipe.setObjectName(u"action_rapport_equipe")
        icon18 = QIcon()
        icon18.addFile(u":/Icon/Icons/users.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_rapport_equipe.setIcon(icon18)
        self.action_rapport_operations = QAction(MainWindow)
        self.action_rapport_operations.setObjectName(u"action_rapport_operations")
        icon19 = QIcon()
        icon19.addFile(u":/Icon/Icons/activity.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_rapport_operations.setIcon(icon19)
        self.action_export_pdf = QAction(MainWindow)
        self.action_export_pdf.setObjectName(u"action_export_pdf")
        self.action_export_excel = QAction(MainWindow)
        self.action_export_excel.setObjectName(u"action_export_excel")
        self.action_export_csv = QAction(MainWindow)
        self.action_export_csv.setObjectName(u"action_export_csv")
        self.action_users = QAction(MainWindow)
        self.action_users.setObjectName(u"action_users")
        self.action_users.setIcon(icon18)
        self.action_new_user = QAction(MainWindow)
        self.action_new_user.setObjectName(u"action_new_user")
        self.action_new_user.setIcon(icon2)
        self.action_audit = QAction(MainWindow)
        self.action_audit.setObjectName(u"action_audit")
        icon20 = QIcon()
        icon20.addFile(u":/Icon/Icons/history.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_audit.setIcon(icon20)
        self.action_backup_now = QAction(MainWindow)
        self.action_backup_now.setObjectName(u"action_backup_now")
        icon21 = QIcon()
        icon21.addFile(u":/Icon/Icons/save.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_backup_now.setIcon(icon21)
        self.action_manage_backups = QAction(MainWindow)
        self.action_manage_backups.setObjectName(u"action_manage_backups")
        icon22 = QIcon()
        icon22.addFile(u":/Icon/Icons/folder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_manage_backups.setIcon(icon22)
        self.action_parametres = QAction(MainWindow)
        self.action_parametres.setObjectName(u"action_parametres")
        icon23 = QIcon()
        icon23.addFile(u":/Icon/Icons/settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_parametres.setIcon(icon23)
        self.action_guide = QAction(MainWindow)
        self.action_guide.setObjectName(u"action_guide")
        icon24 = QIcon()
        icon24.addFile(u":/Icon/Icons/book-open.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_guide.setIcon(icon24)
        self.action_shortcuts = QAction(MainWindow)
        self.action_shortcuts.setObjectName(u"action_shortcuts")
        icon25 = QIcon()
        icon25.addFile(u":/Icon/Icons/key.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_shortcuts.setIcon(icon25)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        icon26 = QIcon()
        icon26.addFile(u":/Icon/Icons/info.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action_about.setIcon(icon26)
        self.icon_search = QAction(MainWindow)
        self.icon_search.setObjectName(u"icon_search")
        icon27 = QIcon()
        icon27.addFile(u":/Icon/Icons/search-alt-2-svgrepo-com.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.icon_search.setIcon(icon27)
        self.icon_search.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frm_nav = QFrame(self.centralwidget)
        self.frm_nav.setObjectName(u"frm_nav")
        self.frm_nav.setMinimumSize(QSize(238, 0))
        self.frm_nav.setMaximumSize(QSize(238, 16777215))
        self.frm_nav.setFrameShape(QFrame.Shape.NoFrame)
        self.frm_nav.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frm_nav)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(14, 16, 14, 14)
        self.frame_2 = QFrame(self.frm_nav)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setStyleSheet(u"#frame_2{\n"
"                                            background-color : transparent;\n"
"                                            border : none;\n"
"                                            }")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 0, 0, 6)
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(42, 42))
        self.label_2.setMaximumSize(QSize(42, 42))
        self.label_2.setStyleSheet(u"QLabel{\n"
"                                                        image: url(:/Icon/Icons/1758107223736.png);\n"
"                                                        background-color:\n"
"                                                        qlineargradient(spread:pad, x1:0, y1:0,\n"
"                                                        x2:1, y2:1, stop:0 #3b82f6, stop:1 #2563eb);\n"
"                                                        border : 1px solid rgba(255,255,255,40);\n"
"                                                        border-radius : 14px;\n"
"                                                        padding : 6px;\n"
"                                                        }")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"QLabel{\n"
"                                                        background-color : transparent;\n"
"                                                        }")

        self.horizontalLayout_2.addWidget(self.label)


        self.verticalLayout.addWidget(self.frame_2)

        self.verticalSpacer_7 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_7)

        self.lbl_nav_section = QLabel(self.frm_nav)
        self.lbl_nav_section.setObjectName(u"lbl_nav_section")

        self.verticalLayout.addWidget(self.lbl_nav_section)

        self.btn_onglet_accueil = QPushButton(self.frm_nav)
        self.btn_onglet_accueil.setObjectName(u"btn_onglet_accueil")
        icon28 = QIcon()
        icon28.addFile(u":/Icon/Icons/home.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_onglet_accueil.setIcon(icon28)
        self.btn_onglet_accueil.setIconSize(QSize(20, 20))
        self.btn_onglet_accueil.setCheckable(True)
        self.btn_onglet_accueil.setChecked(True)

        self.verticalLayout.addWidget(self.btn_onglet_accueil)

        self.btn_onglet_tableau_bord = QPushButton(self.frm_nav)
        self.btn_onglet_tableau_bord.setObjectName(u"btn_onglet_tableau_bord")
        self.btn_onglet_tableau_bord.setIcon(icon19)
        self.btn_onglet_tableau_bord.setIconSize(QSize(20, 20))
        self.btn_onglet_tableau_bord.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_tableau_bord)

        self.btn_onglet_article = QPushButton(self.frm_nav)
        self.btn_onglet_article.setObjectName(u"btn_onglet_article")
        self.btn_onglet_article.setIcon(icon12)
        self.btn_onglet_article.setIconSize(QSize(20, 20))
        self.btn_onglet_article.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_article)

        self.btn_onglet_client = QPushButton(self.frm_nav)
        self.btn_onglet_client.setObjectName(u"btn_onglet_client")
        self.btn_onglet_client.setIcon(icon18)
        self.btn_onglet_client.setIconSize(QSize(20, 20))
        self.btn_onglet_client.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_client)

        self.btn_onglet_facturation = QPushButton(self.frm_nav)
        self.btn_onglet_facturation.setObjectName(u"btn_onglet_facturation")
        self.btn_onglet_facturation.setIcon(icon11)
        self.btn_onglet_facturation.setIconSize(QSize(20, 20))
        self.btn_onglet_facturation.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_facturation)

        self.btn_onglet_blf = QPushButton(self.frm_nav)
        self.btn_onglet_blf.setObjectName(u"btn_onglet_blf")
        self.btn_onglet_blf.setIcon(icon15)
        self.btn_onglet_blf.setIconSize(QSize(20, 20))
        self.btn_onglet_blf.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_blf)

        self.btn_onglet_historique = QPushButton(self.frm_nav)
        self.btn_onglet_historique.setObjectName(u"btn_onglet_historique")
        self.btn_onglet_historique.setIcon(icon20)
        self.btn_onglet_historique.setIconSize(QSize(20, 20))
        self.btn_onglet_historique.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_historique)

        self.btn_onglet_alertes = QPushButton(self.frm_nav)
        self.btn_onglet_alertes.setObjectName(u"btn_onglet_alertes")
        self.btn_onglet_alertes.setIcon(icon13)
        self.btn_onglet_alertes.setIconSize(QSize(20, 20))
        self.btn_onglet_alertes.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_alertes)

        self.btn_onglet_rapport = QPushButton(self.frm_nav)
        self.btn_onglet_rapport.setObjectName(u"btn_onglet_rapport")
        icon29 = QIcon()
        icon29.addFile(u":/Icon/Icons/file-text.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_onglet_rapport.setIcon(icon29)
        self.btn_onglet_rapport.setIconSize(QSize(20, 20))
        self.btn_onglet_rapport.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_rapport)

        self.btn_onglet_audit = QPushButton(self.frm_nav)
        self.btn_onglet_audit.setObjectName(u"btn_onglet_audit")
        icon30 = QIcon()
        icon30.addFile(u":/Icon/Icons/shield-check.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_onglet_audit.setIcon(icon30)
        self.btn_onglet_audit.setIconSize(QSize(20, 20))
        self.btn_onglet_audit.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_audit)

        self.btn_onglet_surveillance = QPushButton(self.frm_nav)
        self.btn_onglet_surveillance.setObjectName(u"btn_onglet_surveillance")
        icon31 = QIcon()
        icon31.addFile(u":/Icon/Icons/shield-alert.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_onglet_surveillance.setIcon(icon31)
        self.btn_onglet_surveillance.setIconSize(QSize(20, 20))
        self.btn_onglet_surveillance.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_surveillance)

        self.btn_onglet_utilisateur = QPushButton(self.frm_nav)
        self.btn_onglet_utilisateur.setObjectName(u"btn_onglet_utilisateur")
        icon32 = QIcon()
        icon32.addFile(u":/Icon/Icons/user-check.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_onglet_utilisateur.setIcon(icon32)
        self.btn_onglet_utilisateur.setIconSize(QSize(20, 20))
        self.btn_onglet_utilisateur.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_utilisateur)

        self.btn_onglet_parametre = QPushButton(self.frm_nav)
        self.btn_onglet_parametre.setObjectName(u"btn_onglet_parametre")
        self.btn_onglet_parametre.setIcon(icon23)
        self.btn_onglet_parametre.setIconSize(QSize(20, 20))
        self.btn_onglet_parametre.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_onglet_parametre)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.line = QFrame(self.frm_nav)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"QFrame{\n"
"                                            background-color: rgba(255,255,255,25);\n"
"                                            border : none;\n"
"                                            max-height : 1px;\n"
"                                            }")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.frame_3 = QFrame(self.frm_nav)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(42, 42))
        self.label_3.setMaximumSize(QSize(42, 42))
        self.label_3.setStyleSheet(u"QLabel{\n"
"                                                        background-color:\n"
"                                                        qlineargradient(spread:pad, x1:0, y1:0,\n"
"                                                        x2:1, y2:1, stop:0 #60a5fa, stop:1 #2563eb);\n"
"                                                        color : #ffffff;\n"
"                                                        border : 1px solid rgba(255,255,255,60);\n"
"                                                        border-radius : 14px;\n"
"                                                        font-weight : bold;\n"
"                                                        font-size : 13px;\n"
"                                                        }")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.label_26 = QLabel(self.frame_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setStyleSheet(u"QLabel{\n"
"                                                        background-color : transparent;\n"
"                                                        }\n"
"                                                    ")

        self.horizontalLayout_3.addWidget(self.label_26)

        self.btn_logout = QToolButton(self.frame_3)
        self.btn_logout.setObjectName(u"btn_logout")
        self.btn_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_logout.setStyleSheet(u"QToolButton {\n"
"                                                        background: transparent;\n"
"                                                        border: none;\n"
"                                                        border-radius: 8px;\n"
"                                                        padding: 6px;\n"
"                                                        }\n"
"                                                        QToolButton:hover {\n"
"                                                        background: rgba(255,255,255,0.15);\n"
"                                                        }")
        icon33 = QIcon()
        icon33.addFile(u":/Icon/Icons/log-out_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_logout.setIcon(icon33)
        self.btn_logout.setIconSize(QSize(18, 18))

        self.horizontalLayout_3.addWidget(self.btn_logout)


        self.verticalLayout.addWidget(self.frame_3)


        self.horizontalLayout.addWidget(self.frm_nav)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 72))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setSpacing(14)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(22, 12, 22, 12)
        self.lbl_ico_change = QLabel(self.frame_4)
        self.lbl_ico_change.setObjectName(u"lbl_ico_change")
        self.lbl_ico_change.setMinimumSize(QSize(40, 44))
        self.lbl_ico_change.setMaximumSize(QSize(40, 44))
        self.lbl_ico_change.setStyleSheet(u"#lbl_ico_change{\n"
"                                                    background-color: rgb(239, 246, 255);\n"
"                                                    image: url(:/Icon/Icons/home-svgrepo-com3.svg);\n"
"                                                    border : 1px solid rgb(219, 234, 254);\n"
"                                                    border-radius : 13px;\n"
"                                                    padding : 8px;\n"
"\n"
"                                                    }")

        self.horizontalLayout_5.addWidget(self.lbl_ico_change)

        self.lbl_titre_change = QLabel(self.frame_4)
        self.lbl_titre_change.setObjectName(u"lbl_titre_change")
        self.lbl_titre_change.setStyleSheet(u"QLabel{\n"
"                                                    background-color : transparent;\n"
"                                                    font-size : 21px;\n"
"                                                    font-weight : 800;\n"
"                                                    color : #0f172a;\n"
"                                                    }\n"
"                                                ")

        self.horizontalLayout_5.addWidget(self.lbl_titre_change)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.edit_recheche_rapide = QLineEdit(self.frame_4)
        self.edit_recheche_rapide.setObjectName(u"edit_recheche_rapide")
        self.edit_recheche_rapide.setMinimumSize(QSize(240, 40))
        self.edit_recheche_rapide.setClearButtonEnabled(True)

        self.horizontalLayout_5.addWidget(self.edit_recheche_rapide)

        self.line_4 = QFrame(self.frame_4)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setStyleSheet(u"QFrame{\n"
"                                                    background-color: #e6ebf2;\n"
"                                                    border : none;\n"
"                                                    max-width : 1px;\n"
"                                                    }")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_5.addWidget(self.line_4)

        self.lbl_temps = QLabel(self.frame_4)
        self.lbl_temps.setObjectName(u"lbl_temps")
        self.lbl_temps.setStyleSheet(u"QLabel{\n"
"                                                    background-color : transparent;\n"
"                                                    }")

        self.horizontalLayout_5.addWidget(self.lbl_temps)

        self.horizontalLayout_5.setStretch(2, 1)

        self.verticalLayout_2.addWidget(self.frame_4)

        self.stackedWidget = AnimatedStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(9, -1, 9, -1)
        self.scrollArea = QScrollArea(self.page)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 982, 773))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(50, -1, 50, -1)
        self.frame_6 = QFrame(self.scrollAreaWidgetContents)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setStyleSheet(u"#frame_6{\n"
"                                                                        background-color:\n"
"                                                                        transparent;\n"
"                                                                        border : none;\n"
"                                                                        }")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_6)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.frame_6)

        self.verticalLayout_5.setStretch(0, 7)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"\n"
"\n"
"                                            #frame_15{\n"
"                                            background-color: #ffffff;\n"
"                                            border: 1px solid #e6ebf2;\n"
"                                            border-radius: 18px;\n"
"                                            }\n"
"\n"
"                                            #frame_16{\n"
"                                            background-color: #ffffff;\n"
"                                            border: 1px solid #e6ebf2;\n"
"                                            border-radius: 18px;\n"
"                                            }\n"
"\n"
"                                            QLabel{\n"
"                                            background-color : transparent;\n"
"                                            }")
        self.horizontalLayout_6 = QHBoxLayout(self.page_2)
        self.horizontalLayout_6.setSpacing(20)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(20, 20, 20, 20)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_17 = QVBoxLayout(self.page_3)
        self.verticalLayout_17.setSpacing(20)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(20, 20, 20, 20)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(10)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.btn_voir_tout_produit = QPushButton(self.page_3)
        self.btn_voir_tout_produit.setObjectName(u"btn_voir_tout_produit")
        self.btn_voir_tout_produit.setMinimumSize(QSize(0, 42))

        self.horizontalLayout_7.addWidget(self.btn_voir_tout_produit)

        self.btn_voir_rupture_produit = QPushButton(self.page_3)
        self.btn_voir_rupture_produit.setObjectName(u"btn_voir_rupture_produit")
        self.btn_voir_rupture_produit.setMinimumSize(QSize(140, 42))
        self.btn_voir_rupture_produit.setStyleSheet(u"QPushButton{\n"
"                                                                icon :\n"
"                                                                url(:/Icon/Icons/exclamation-mark-triangle-f-svgrepo-com.svg);\n"
"                                                                padding-left : 6px;\n"
"                                                                text-align : left;\n"
"                                                                icon-size : 18px 18px;\n"
"                                                                }")

        self.horizontalLayout_7.addWidget(self.btn_voir_rupture_produit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.btn_ajouter_produit = QPushButton(self.page_3)
        self.btn_ajouter_produit.setObjectName(u"btn_ajouter_produit")
        self.btn_ajouter_produit.setMinimumSize(QSize(180, 44))
        self.btn_ajouter_produit.setStyleSheet(u"QPushButton{\n"
"                                                                icon :\n"
"                                                                url(:/Icon/Icons/add-svgrepo-com.svg);\n"
"                                                                padding-left : 6px;\n"
"                                                                text-align : left;\n"
"                                                                icon-size : 18px 18px;\n"
"                                                                }\n"
"\n"
"                                                                QPushButton:pressed{\n"
"                                                                background-color: rgb(30, 64, 175);\n"
"                                                                }")

        self.horizontalLayout_7.addWidget(self.btn_ajouter_produit)

        self.btn_modifier_stock = QPushButton(self.page_3)
        self.btn_modifier_stock.setObjectName(u"btn_modifier_stock")
        self.btn_modifier_stock.setMinimumSize(QSize(140, 42))
        self.btn_modifier_stock.setStyleSheet(u"QPushButton{\n"
"                                                                icon :\n"
"                                                                url(:/Icon/Icons/edit.svg);\n"
"                                                                padding-left : 6px;\n"
"                                                                text-align : left;\n"
"                                                                icon-size : 18px 18px;\n"
"                                                                background-color:\n"
"                                                                qlineargradient(spread:pad, x1:0,\n"
"                                                                y1:0, x2:0, y2:1, stop:0 #facc15,\n"
"                                                                stop:1 #eab308);\n"
"                                                                color: #422006;\n"
"                                                                border-radius: 12px;\n"
"                       "
                        "                                         padding: 10px 24px;\n"
"                                                                font-weight: bold;\n"
"                                                                border: 1px solid #ca8a04;\n"
"                                                                }\n"
"\n"
"                                                                QPushButton:hover{\n"
"                                                                background-color :\n"
"                                                                qlineargradient(spread:pad, x1:0,\n"
"                                                                y1:0, x2:0, y2:1, stop:0 #eab308,\n"
"                                                                stop:1 #ca8a04);\n"
"                                                                }\n"
"\n"
"                                                                QPushButton:pressed{\n"
"                                                                background-c"
                        "olor : rgb(161, 98, 7);\n"
"                                                                }")

        self.horizontalLayout_7.addWidget(self.btn_modifier_stock)

        self.btn_supprimer_produit = QPushButton(self.page_3)
        self.btn_supprimer_produit.setObjectName(u"btn_supprimer_produit")
        self.btn_supprimer_produit.setMinimumSize(QSize(140, 42))
        self.btn_supprimer_produit.setStyleSheet(u"QPushButton{\n"
"                                                                icon : url(:/Icon/Icons/trash.svg);\n"
"                                                                padding-left : 6px;\n"
"                                                                text-align : left;\n"
"                                                                icon-size : 18px 18px;\n"
"                                                                background-color : #ffffff;\n"
"                                                                color : #dc2626;\n"
"                                                                border : 1px solid #fecaca;\n"
"                                                                border-radius : 12px;\n"
"                                                                padding : 10px 24px;\n"
"                                                                font-weight : bold;\n"
"                                                                }\n"
"\n"
"                   "
                        "                                             QPushButton:hover{\n"
"                                                                background-color : #fef2f2;\n"
"                                                                border-color : #fca5a5;\n"
"                                                                color : #b91c1c;\n"
"                                                                }\n"
"\n"
"                                                                QPushButton:pressed{\n"
"                                                                background-color : #fee2e2;\n"
"                                                                }")

        self.horizontalLayout_7.addWidget(self.btn_supprimer_produit)


        self.verticalLayout_17.addLayout(self.horizontalLayout_7)

        self.frame_17 = QFrame(self.page_3)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setStyleSheet(u"#frame_17{\n"
"                                                        background-color: #ffffff;\n"
"                                                        border : 1px solid #e6ebf2;\n"
"                                                        border-radius : 18px;\n"
"                                                        }\n"
"\n"
"                                                        #frame_17 QTableWidget{\n"
"                                                        background-color : transparent;\n"
"                                                        border : none;\n"
"                                                        border-radius : 0px;\n"
"                                                        }")
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_17)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.tbw_voir_produit = QTableWidget(self.frame_17)
        if (self.tbw_voir_produit.columnCount() < 9):
            self.tbw_voir_produit.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tbw_voir_produit.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.tbw_voir_produit.setObjectName(u"tbw_voir_produit")
        self.tbw_voir_produit.setStyleSheet(u"QTableWidget{\n"
"                                                                    background-color : transparent;\n"
"                                                                    border : none;\n"
"                                                                    }\n"
"\n"
"                                                                    QHeaderView::section {\n"
"                                                                    font-size : 8px;\n"
"                                                                    }")
        self.tbw_voir_produit.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tbw_voir_produit.setAlternatingRowColors(True)
        self.tbw_voir_produit.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tbw_voir_produit.setShowGrid(False)
        self.tbw_voir_produit.setRowCount(0)
        self.tbw_voir_produit.setColumnCount(9)
        self.tbw_voir_produit.horizontalHeader().setVisible(True)
        self.tbw_voir_produit.verticalHeader().setVisible(False)
        self.tbw_voir_produit.verticalHeader().setMinimumSectionSize(60)
        self.tbw_voir_produit.verticalHeader().setDefaultSectionSize(60)

        self.verticalLayout_16.addWidget(self.tbw_voir_produit)


        self.verticalLayout_17.addWidget(self.frame_17)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_27 = QVBoxLayout(self.page_4)
        self.verticalLayout_27.setSpacing(0)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.horizontalLayout_10 = QHBoxLayout(self.page_5)
        self.horizontalLayout_10.setSpacing(20)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(20, 20, 20, 20)
        self.stackedWidget.addWidget(self.page_5)
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.page_9.setStyleSheet(u"/* ===========================\n"
"                                            PAGE 9 - BLF / FOURNISSEURS\n"
"                                            =========================== */\n"
"\n"
"                                            QWidget#page_9 {\n"
"                                            background-color: transparent;\n"
"                                            }\n"
"\n"
"                                            QLabel{\n"
"                                            background-color : transparent;\n"
"                                            }\n"
"\n"
"                                            /* Cartes principales */\n"
"                                            #frame_blf_header,\n"
"                                            #frame_blf_table {\n"
"                                            background-color: #ffffff;\n"
"                                            border: 1px solid #e6ebf2;\n"
"                                            border-radius: 18px;\n"
"              "
                        "                              }\n"
"\n"
"                                            /* Bande des stats : fond transparent, cartes internes\n"
"                                            arrondies */\n"
"                                            #frame_blf_stats {\n"
"                                            background-color: transparent;\n"
"                                            border: none;\n"
"                                            }\n"
"\n"
"                                            #frame_blf_stat1,\n"
"                                            #frame_blf_stat2,\n"
"                                            #frame_blf_stat3 {\n"
"                                            background-color: #ffffff;\n"
"                                            border: 1px solid #e6ebf2;\n"
"                                            border-radius: 18px;\n"
"                                            }\n"
"\n"
"                                            #frame_blf_stat1:hover,\n"
"            "
                        "                                #frame_blf_stat2:hover,\n"
"                                            #frame_blf_stat3:hover {\n"
"                                            border: 1px solid #bfdbfe;\n"
"                                            }\n"
"\n"
"                                            /* Titres du header */\n"
"                                            #lbl_blf_title {\n"
"                                            font-size: 19px;\n"
"                                            font-weight: 800;\n"
"                                            color: #0f172a;\n"
"                                            }\n"
"\n"
"                                            #lbl_blf_subtitle {\n"
"                                            font-size: 9px;\n"
"                                            font-weight: 800;\n"
"                                            text-transform: uppercase;\n"
"                                            letter-spacing: 0.22em;\n"
"                               "
                        "             color: #2563eb;\n"
"                                            }\n"
"\n"
"                                            /* Champ de recherche */\n"
"                                            QLineEdit#edit_blf_search {\n"
"                                            background-color: #f1f5f9;\n"
"                                            border-radius: 999px;\n"
"                                            border: 1px solid transparent;\n"
"                                            padding: 8px 16px;\n"
"                                            font-size: 12px;\n"
"                                            font-weight: 600;\n"
"                                            color: #334155;\n"
"                                            }\n"
"\n"
"                                            QLineEdit#edit_blf_search:hover {\n"
"                                            background-color: #e8eef6;\n"
"                                            }\n"
"\n"
"                                   "
                        "         QLineEdit#edit_blf_search:focus {\n"
"                                            border: 1px solid #2563eb;\n"
"                                            background-color: #ffffff;\n"
"                                            }\n"
"\n"
"                                            /* Bouton : nouveau partenaire */\n"
"                                            QPushButton#btn_blf_new_supplier {\n"
"                                            background-color: #ffffff;\n"
"                                            border: 1px solid #dbe3ec;\n"
"                                            border-radius: 999px;\n"
"                                            padding: 8px 18px;\n"
"                                            font-size: 11px;\n"
"                                            font-weight: 700;\n"
"                                            color: #334155;\n"
"                                            }\n"
"\n"
"                                            QPushButton#btn_blf_new_sup"
                        "plier:hover {\n"
"                                            background-color: #f8fafc;\n"
"                                            border-color: #c3cedd;\n"
"                                            color: #0f172a;\n"
"                                            }\n"
"\n"
"                                            /* Bouton : passer une commande */\n"
"                                            QPushButton#btn_blf_new_order {\n"
"                                            background-color: qlineargradient(spread:pad, x1:0,\n"
"                                            y1:0, x2:0, y2:1, stop:0 #3b82f6, stop:1 #2563eb);\n"
"                                            border-radius: 999px;\n"
"                                            padding: 8px 18px;\n"
"                                            font-size: 11px;\n"
"                                            font-weight: 800;\n"
"                                            color: #ffffff;\n"
"                                            bord"
                        "er: 1px solid #1d4ed8;\n"
"                                            }\n"
"\n"
"                                            QPushButton#btn_blf_new_order:hover {\n"
"                                            background-color: qlineargradient(spread:pad, x1:0,\n"
"                                            y1:0, x2:0, y2:1, stop:0 #2f74e8, stop:1 #1d4ed8);\n"
"                                            }\n"
"\n"
"                                            /* Ic\u00f4nes des stats */\n"
"                                            #lbl_blf_stat1_icon,\n"
"                                            #lbl_blf_stat2_icon,\n"
"                                            #lbl_blf_stat3_icon {\n"
"                                            font-size: 12px;\n"
"                                            font-weight: 800;\n"
"                                            }\n"
"\n"
"                                            /* Texte des stats */\n"
"                                            #lbl_blf_stat1_labe"
                        "l,\n"
"                                            #lbl_blf_stat2_label,\n"
"                                            #lbl_blf_stat3_label {\n"
"                                            font-size: 10px;\n"
"                                            font-weight: 700;\n"
"                                            color: #64748b;\n"
"                                            }\n"
"\n"
"                                            /* Valeurs des stats */\n"
"                                            #lbl_blf_stat1_value,\n"
"                                            #lbl_blf_stat2_value,\n"
"                                            #lbl_blf_stat3_value {\n"
"                                            font-size: 22px;\n"
"                                            font-weight: 800;\n"
"                                            color: #0f172a;\n"
"                                            }\n"
"\n"
"                                            /* Titre de la table principale */\n"
"           "
                        "                                 #lbl_blf_table_title {\n"
"                                            font-size: 12px;\n"
"                                            font-weight: 800;\n"
"                                            text-transform: uppercase;\n"
"                                            letter-spacing: 0.14em;\n"
"                                            color: #0f172a;\n"
"                                            }\n"
"\n"
"                                            /* TABLE BLF */\n"
"                                            QTableWidget#tbw_blf_lignes {\n"
"                                            background-color: transparent;\n"
"                                            border: none;\n"
"                                            gridline-color: #f1f5f9;\n"
"                                            outline: none;\n"
"                                            }\n"
"\n"
"                                            QTableWidget#tbw_blf_lignes::item {\n"
"          "
                        "                                  padding: 10px;\n"
"                                            border-bottom: 1px solid #f1f5f9;\n"
"                                            color: #334155;\n"
"                                            font-size: 12px;\n"
"                                            font-weight: 500;\n"
"                                            }\n"
"\n"
"                                            QTableWidget#tbw_blf_lignes::item:hover {\n"
"                                            background-color: #f8fafc;\n"
"                                            }\n"
"\n"
"                                            QTableWidget#tbw_blf_lignes::item:selected {\n"
"                                            background-color: #eff6ff;\n"
"                                            color: #1d4ed8;\n"
"                                            }\n"
"\n"
"                                            /* En-t\u00eate du tableau */\n"
"                                            QHeaderView"
                        "::section {\n"
"                                            background-color: rgba(248, 250, 252, 0.9);\n"
"                                            color: #94a3b8;\n"
"                                            padding: 12px;\n"
"                                            border: 0px solid transparent;\n"
"                                            border-bottom: 1px solid #e6ebf2;\n"
"                                            font-weight: 800;\n"
"                                            text-transform: uppercase;\n"
"                                            font-size: 10px;\n"
"                                            letter-spacing: 0.16em;\n"
"                                            }\n"
"\n"
"                                            QTableWidget#tbw_blf_lignes::corner {\n"
"                                            background-color: #f8fafc;\n"
"                                            border: none;\n"
"                                            }\n"
"\n"
"                  "
                        "                          /* Scrollbars */\n"
"                                            QScrollBar:vertical {\n"
"                                            border: none;\n"
"                                            background: transparent;\n"
"                                            width: 10px;\n"
"                                            margin: 2px;\n"
"                                            }\n"
"\n"
"                                            QScrollBar::handle:vertical {\n"
"                                            background: #cbd5e1;\n"
"                                            min-height: 32px;\n"
"                                            border-radius: 5px;\n"
"                                            }\n"
"\n"
"                                            QScrollBar::handle:vertical:hover {\n"
"                                            background: #94a3b8;\n"
"                                            }\n"
"\n"
"                                            QScrollB"
                        "ar::add-line:vertical,\n"
"                                            QScrollBar::sub-line:vertical {\n"
"                                            height: 0px;\n"
"                                            }\n"
"\n"
"                                            QScrollBar:horizontal {\n"
"                                            border: none;\n"
"                                            background: transparent;\n"
"                                            height: 10px;\n"
"                                            }\n"
"\n"
"                                            QScrollBar::handle:horizontal {\n"
"                                            background: #cbd5e1;\n"
"                                            min-width: 32px;\n"
"                                            border-radius: 5px;\n"
"                                            }")
        self.verticalLayout_blf = QVBoxLayout(self.page_9)
        self.verticalLayout_blf.setSpacing(18)
        self.verticalLayout_blf.setObjectName(u"verticalLayout_blf")
        self.verticalLayout_blf.setContentsMargins(20, 20, 20, 20)
        self.frame_blf_stats = QFrame(self.page_9)
        self.frame_blf_stats.setObjectName(u"frame_blf_stats")
        self.frame_blf_stats.setStyleSheet(u"#frame_blf_stats{\n"
"                                                        background-color : transparent;\n"
"                                                        border : none;\n"
"                                                        }")
        self.frame_blf_stats.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_blf_stats.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_blf_stats = QHBoxLayout(self.frame_blf_stats)
        self.horizontalLayout_blf_stats.setSpacing(20)
        self.horizontalLayout_blf_stats.setObjectName(u"horizontalLayout_blf_stats")
        self.horizontalLayout_blf_stats.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_blf.addWidget(self.frame_blf_stats)

        self.frame_blf_table = QFrame(self.page_9)
        self.frame_blf_table.setObjectName(u"frame_blf_table")
        self.frame_blf_table.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_blf_table.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_blf_table = QVBoxLayout(self.frame_blf_table)
        self.verticalLayout_blf_table.setObjectName(u"verticalLayout_blf_table")
        self.verticalLayout_blf_table.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_blf.addWidget(self.frame_blf_table)

        self.stackedWidget.addWidget(self.page_9)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.page_6.setStyleSheet(u"#frame_20{\n"
"                                            background-color: #ffffff;\n"
"                                            border: 1px solid #e6ebf2;\n"
"                                            border-radius: 18px;\n"
"                                            }\n"
"\n"
"                                            #frame_20 QTableWidget{\n"
"                                            background-color : transparent;\n"
"                                            border : none;\n"
"                                            border-top : 1px solid #eef2f7;\n"
"                                            border-radius : 0px;\n"
"                                            }\n"
"\n"
"                                            QLabel{\n"
"                                            background-color : transparent;\n"
"                                            }")
        self.verticalLayout_22 = QVBoxLayout(self.page_6)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(20, 20, 20, 20)
        self.stackedWidget.addWidget(self.page_6)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.horizontalLayout_11 = QHBoxLayout(self.page_7)
        self.horizontalLayout_11.setSpacing(20)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(20, 20, 20, 20)
        self.stackedWidget.addWidget(self.page_7)
        self.page_13 = QWidget()
        self.page_13.setObjectName(u"page_13")
        self.verticalLayout_20 = QVBoxLayout(self.page_13)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.stackedWidget.addWidget(self.page_13)
        self.page_alertes = QWidget()
        self.page_alertes.setObjectName(u"page_alertes")
        self.verticalLayout_page_alertes = QVBoxLayout(self.page_alertes)
        self.verticalLayout_page_alertes.setObjectName(u"verticalLayout_page_alertes")
        self.verticalLayout_page_alertes.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_alertes)
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.verticalLayout_26 = QVBoxLayout(self.page_8)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(20, 20, 20, 20)
        self.frame_22 = QFrame(self.page_8)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setStyleSheet(u"#frame_22{\n"
"                                                        background-color: #ffffff;\n"
"                                                        border: 1px solid #e6ebf2;\n"
"                                                        border-radius: 18px;\n"
"                                                        }\n"
"\n"
"                                                        #frame_22 QFrame{\n"
"                                                        background-color : transparent;\n"
"                                                        border : none;\n"
"                                                        }\n"
"\n"
"                                                        QLabel{\n"
"                                                        background-color : transparent;\n"
"                                                        }")
        self.frame_22.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.frame_22)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(14)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(24, 22, 24, 20)
        self.label_30 = QLabel(self.frame_22)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setStyleSheet(u"QLabel{\n"
"                                                                            background-color:\n"
"                                                                            transparent;\n"
"                                                                            }")

        self.horizontalLayout_12.addWidget(self.label_30)

        self.btn_ajouter_caissier = QPushButton(self.frame_22)
        self.btn_ajouter_caissier.setObjectName(u"btn_ajouter_caissier")
        self.btn_ajouter_caissier.setMinimumSize(QSize(0, 44))

        self.horizontalLayout_12.addWidget(self.btn_ajouter_caissier, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_25.addLayout(self.horizontalLayout_12)

        self.line_3 = QFrame(self.frame_22)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setStyleSheet(u"QFrame{\n"
"                                                                    background-color : #eef2f7;\n"
"                                                                    border : none;\n"
"                                                                    max-height : 1px;\n"
"                                                                    }")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_25.addWidget(self.line_3)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(18)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(24, 20, 24, 20)

        self.verticalLayout_25.addLayout(self.gridLayout_2)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_9)

        self.verticalLayout_25.setStretch(3, 1)

        self.verticalLayout_26.addWidget(self.frame_22)

        self.stackedWidget.addWidget(self.page_8)
        self.page_12 = QWidget()
        self.page_12.setObjectName(u"page_12")
        self.verticalLayout_38 = QVBoxLayout(self.page_12)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.stackedWidget.addWidget(self.page_12)
        self.page_surveillance = QWidget()
        self.page_surveillance.setObjectName(u"page_surveillance")
        self.verticalLayout_3 = QVBoxLayout(self.page_surveillance)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.stackedWidget.addWidget(self.page_surveillance)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1240, 34))
        self.menu_fichier = QMenu(self.menubar)
        self.menu_fichier.setObjectName(u"menu_fichier")
        self.menu_edition = QMenu(self.menubar)
        self.menu_edition.setObjectName(u"menu_edition")
        self.menu_ventes = QMenu(self.menubar)
        self.menu_ventes.setObjectName(u"menu_ventes")
        self.menu_stock = QMenu(self.menubar)
        self.menu_stock.setObjectName(u"menu_stock")
        self.menu_rapports = QMenu(self.menubar)
        self.menu_rapports.setObjectName(u"menu_rapports")
        self.menu_admin = QMenu(self.menubar)
        self.menu_admin.setObjectName(u"menu_admin")
        self.menu_aide = QMenu(self.menubar)
        self.menu_aide.setObjectName(u"menu_aide")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_fichier.menuAction())
        self.menubar.addAction(self.menu_edition.menuAction())
        self.menubar.addAction(self.menu_ventes.menuAction())
        self.menubar.addAction(self.menu_stock.menuAction())
        self.menubar.addAction(self.menu_rapports.menuAction())
        self.menubar.addAction(self.menu_admin.menuAction())
        self.menubar.addAction(self.menu_aide.menuAction())
        self.menu_fichier.addAction(self.action_new_facture)
        self.menu_fichier.addSeparator()
        self.menu_fichier.addAction(self.action_new_client)
        self.menu_fichier.addAction(self.action_new_produit)
        self.menu_fichier.addSeparator()
        self.menu_fichier.addAction(self.action_export_db)
        self.menu_fichier.addAction(self.action_restore_db)
        self.menu_fichier.addAction(self.action_logout)
        self.menu_fichier.addSeparator()
        self.menu_fichier.addAction(self.action_quit)
        self.menu_edition.addAction(self.action_actualiser)
        self.menu_edition.addAction(self.action_search)
        self.menu_edition.addSeparator()
        self.menu_edition.addAction(self.action_clear_panier)
        self.menu_ventes.addAction(self.action_demarrer_vente)
        self.menu_ventes.addAction(self.action_ventes_jour)
        self.menu_ventes.addSeparator()
        self.menu_ventes.addAction(self.action_derniere_facture)
        self.menu_stock.addAction(self.action_voir_produits)
        self.menu_stock.addAction(self.action_ruptures)
        self.menu_stock.addSeparator()
        self.menu_stock.addAction(self.action_new_blf)
        self.menu_stock.addAction(self.action_new_fournisseur)
        self.menu_stock.addAction(self.action_voir_blf)
        self.menu_rapports.addAction(self.action_rapport_ventes)
        self.menu_rapports.addAction(self.action_rapport_equipe)
        self.menu_rapports.addAction(self.action_rapport_operations)
        self.menu_rapports.addSeparator()
        self.menu_rapports.addAction(self.action_export_pdf)
        self.menu_rapports.addAction(self.action_export_excel)
        self.menu_rapports.addAction(self.action_export_csv)
        self.menu_admin.addAction(self.action_users)
        self.menu_admin.addAction(self.action_new_user)
        self.menu_admin.addSeparator()
        self.menu_admin.addAction(self.action_audit)
        self.menu_admin.addSeparator()
        self.menu_admin.addAction(self.action_backup_now)
        self.menu_admin.addAction(self.action_manage_backups)
        self.menu_admin.addSeparator()
        self.menu_admin.addAction(self.action_parametres)
        self.menu_admin.addSeparator()
        self.menu_aide.addAction(self.action_guide)
        self.menu_aide.addAction(self.action_shortcuts)
        self.menu_aide.addSeparator()
        self.menu_aide.addAction(self.action_about)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Nova Pharma", None))
        self.action_new_facture.setText(QCoreApplication.translate("MainWindow", u"Nouvelle facture", None))
#if QT_CONFIG(shortcut)
        self.action_new_facture.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.action_new_client.setText(QCoreApplication.translate("MainWindow", u"Nouveau client", None))
#if QT_CONFIG(shortcut)
        self.action_new_client.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+C", None))
#endif // QT_CONFIG(shortcut)
        self.action_new_produit.setText(QCoreApplication.translate("MainWindow", u"Nouveau produit", None))
#if QT_CONFIG(shortcut)
        self.action_new_produit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+P", None))
#endif // QT_CONFIG(shortcut)
        self.action_export_db.setText(QCoreApplication.translate("MainWindow", u"Exporter la base\u2026", None))
        self.action_restore_db.setText(QCoreApplication.translate("MainWindow", u"Restaurer une sauvegarde\u2026", None))
        self.action_logout.setText(QCoreApplication.translate("MainWindow", u"Se d\u00e9connecter", None))
#if QT_CONFIG(shortcut)
        self.action_logout.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_quit.setText(QCoreApplication.translate("MainWindow", u"Quitter", None))
#if QT_CONFIG(shortcut)
        self.action_quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_actualiser.setText(QCoreApplication.translate("MainWindow", u"Actualiser", None))
#if QT_CONFIG(shortcut)
        self.action_actualiser.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.action_search.setText(QCoreApplication.translate("MainWindow", u"Recherche globale\u2026", None))
#if QT_CONFIG(shortcut)
        self.action_search.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.action_clear_panier.setText(QCoreApplication.translate("MainWindow", u"Annuler la saisie", None))
#if QT_CONFIG(shortcut)
        self.action_clear_panier.setShortcut(QCoreApplication.translate("MainWindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.action_demarrer_vente.setText(QCoreApplication.translate("MainWindow", u"D\u00e9marrer une vente", None))
#if QT_CONFIG(shortcut)
        self.action_demarrer_vente.setShortcut(QCoreApplication.translate("MainWindow", u"F2", None))
#endif // QT_CONFIG(shortcut)
        self.action_ventes_jour.setText(QCoreApplication.translate("MainWindow", u"Ventes du jour", None))
#if QT_CONFIG(shortcut)
        self.action_ventes_jour.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+J", None))
#endif // QT_CONFIG(shortcut)
        self.action_derniere_facture.setText(QCoreApplication.translate("MainWindow", u"Voir la derni\u00e8re facture", None))
        self.action_voir_produits.setText(QCoreApplication.translate("MainWindow", u"Voir tous les produits", None))
#if QT_CONFIG(shortcut)
        self.action_voir_produits.setShortcut(QCoreApplication.translate("MainWindow", u"F3", None))
#endif // QT_CONFIG(shortcut)
        self.action_ruptures.setText(QCoreApplication.translate("MainWindow", u"Produits en rupture", None))
#if QT_CONFIG(shortcut)
        self.action_ruptures.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.action_new_blf.setText(QCoreApplication.translate("MainWindow", u"Nouveau BLF", None))
#if QT_CONFIG(shortcut)
        self.action_new_blf.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+B", None))
#endif // QT_CONFIG(shortcut)
        self.action_new_fournisseur.setText(QCoreApplication.translate("MainWindow", u"Nouveau fournisseur", None))
        self.action_voir_blf.setText(QCoreApplication.translate("MainWindow", u"Voir les BLF", None))
        self.action_rapport_ventes.setText(QCoreApplication.translate("MainWindow", u"Rapport Ventes", None))
#if QT_CONFIG(shortcut)
        self.action_rapport_ventes.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+1", None))
#endif // QT_CONFIG(shortcut)
        self.action_rapport_equipe.setText(QCoreApplication.translate("MainWindow", u"Rapport \u00c9quipe", None))
#if QT_CONFIG(shortcut)
        self.action_rapport_equipe.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+2", None))
#endif // QT_CONFIG(shortcut)
        self.action_rapport_operations.setText(QCoreApplication.translate("MainWindow", u"Rapport Op\u00e9rations", None))
#if QT_CONFIG(shortcut)
        self.action_rapport_operations.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+3", None))
#endif // QT_CONFIG(shortcut)
        self.action_export_pdf.setText(QCoreApplication.translate("MainWindow", u"Export PDF", None))
        self.action_export_excel.setText(QCoreApplication.translate("MainWindow", u"Export Excel", None))
        self.action_export_csv.setText(QCoreApplication.translate("MainWindow", u"Export CSV", None))
        self.action_users.setText(QCoreApplication.translate("MainWindow", u"Utilisateurs", None))
        self.action_new_user.setText(QCoreApplication.translate("MainWindow", u"Nouvel utilisateur", None))
        self.action_audit.setText(QCoreApplication.translate("MainWindow", u"Journal d'audit", None))
        self.action_backup_now.setText(QCoreApplication.translate("MainWindow", u"Sauvegarder maintenant", None))
        self.action_manage_backups.setText(QCoreApplication.translate("MainWindow", u"G\u00e9rer les archives\u2026", None))
        self.action_parametres.setText(QCoreApplication.translate("MainWindow", u"Param\u00e8tres", None))
        self.action_guide.setText(QCoreApplication.translate("MainWindow", u"Guide utilisateur", None))
#if QT_CONFIG(shortcut)
        self.action_guide.setShortcut(QCoreApplication.translate("MainWindow", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.action_shortcuts.setText(QCoreApplication.translate("MainWindow", u"Raccourcis clavier", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"\u00c0 propos de Nova Pharma", None))
        self.icon_search.setText(QCoreApplication.translate("MainWindow", u"icon_search", None))
#if QT_CONFIG(tooltip)
        self.icon_search.setToolTip(QCoreApplication.translate("MainWindow", u"Lancer une recherche", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\n"
"                                                        <html><head/><body><p><span\n"
"                                                        style=\" font-size:14pt;\n"
"                                                        font-weight:700;\n"
"                                                        color:#ffffff;\">Nova\n"
"                                                        Pharma<br/></span><span\n"
"                                                        style=\" font-size:7pt; font-weight:700;\n"
"                                                        color:#60a5fa;\n"
"                                                        letter-spacing:2px;\">LOGICIEL DE\n"
"                                                        GESTION</span></p></body></html>", None))
        self.lbl_nav_section.setText(QCoreApplication.translate("MainWindow", u"MENU", None))
        self.btn_onglet_accueil.setText(QCoreApplication.translate("MainWindow", u"Accueil", None))
        self.btn_onglet_tableau_bord.setText(QCoreApplication.translate("MainWindow", u"Tableau de bord", None))
        self.btn_onglet_article.setText(QCoreApplication.translate("MainWindow", u"Articles", None))
        self.btn_onglet_client.setText(QCoreApplication.translate("MainWindow", u"Clients", None))
        self.btn_onglet_facturation.setText(QCoreApplication.translate("MainWindow", u"Facturation", None))
        self.btn_onglet_blf.setText(QCoreApplication.translate("MainWindow", u"BLF & Fournisseurs", None))
        self.btn_onglet_historique.setText(QCoreApplication.translate("MainWindow", u"Historique", None))
        self.btn_onglet_alertes.setText(QCoreApplication.translate("MainWindow", u"Alertes", None))
        self.btn_onglet_rapport.setText(QCoreApplication.translate("MainWindow", u"Rapports", None))
        self.btn_onglet_audit.setText(QCoreApplication.translate("MainWindow", u"Audit & S\u00e9curit\u00e9", None))
        self.btn_onglet_surveillance.setText(QCoreApplication.translate("MainWindow", u"Surveillance", None))
        self.btn_onglet_utilisateur.setText(QCoreApplication.translate("MainWindow", u"Utilisateurs", None))
        self.btn_onglet_parametre.setText(QCoreApplication.translate("MainWindow", u"Param\u00e8tres", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"DK", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:9pt; font-weight:700; color:#f8fafc;\">Mr. XXXXX</span><span style=\" font-size:11pt;\"><br/></span><span style=\" font-size:7pt; font-weight:700; color:#60a5fa;\">ADMINISTRATEUR</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.btn_logout.setToolTip(QCoreApplication.translate("MainWindow", u"Se d\u00e9connecter", None))
#endif // QT_CONFIG(tooltip)
        self.lbl_ico_change.setText("")
        self.lbl_titre_change.setText(QCoreApplication.translate("MainWindow", u"Accueil", None))
        self.edit_recheche_rapide.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Recherche rapide\u2026", None))
        self.lbl_temps.setText(QCoreApplication.translate("MainWindow", u"\n"
"                                                    <html><head/><body><p\n"
"                                                    align=\"right\"><span style=\"\n"
"                                                    font-size:11pt; font-weight:700;\n"
"                                                    color:#0f172a;\">18:47:22<br/></span><span\n"
"                                                    style=\" font-size:7pt; font-weight:600;\n"
"                                                    color:#94a3b8;\n"
"                                                    letter-spacing:1px;\">DIMANCHE 18\n"
"                                                    JANVIER</span></p></body></html>", None))
        self.btn_voir_tout_produit.setText(QCoreApplication.translate("MainWindow", u"Toutes les cat\u00e9gories", None))
        self.btn_voir_rupture_produit.setText(QCoreApplication.translate("MainWindow", u"En rupture", None))
        self.btn_ajouter_produit.setText(QCoreApplication.translate("MainWindow", u"Ajouter un article", None))
        self.btn_modifier_stock.setText(QCoreApplication.translate("MainWindow", u"Modifier", None))
        self.btn_supprimer_produit.setText(QCoreApplication.translate("MainWindow", u"Supprimer", None))
        ___qtablewidgetitem = self.tbw_voir_produit.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"CODE REF", None))
        ___qtablewidgetitem1 = self.tbw_voir_produit.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"PRODUIT", None))
        ___qtablewidgetitem2 = self.tbw_voir_produit.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"CATEGORIE", None))
        ___qtablewidgetitem3 = self.tbw_voir_produit.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"QUANTITE", None))
        ___qtablewidgetitem4 = self.tbw_voir_produit.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"PRIX D'ACHAT", None))
        ___qtablewidgetitem5 = self.tbw_voir_produit.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"PRIX DE VENTE", None))
        ___qtablewidgetitem6 = self.tbw_voir_produit.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"PRIX UNITAIRE", None))
        ___qtablewidgetitem7 = self.tbw_voir_produit.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"EXP", None))
        ___qtablewidgetitem8 = self.tbw_voir_produit.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"DATE D'AJOUT", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"\n"
"                                                                            <html><head/><body><p><span\n"
"                                                                            style=\"\n"
"                                                                            font-size:18pt;\n"
"                                                                            font-weight:700;\n"
"                                                                            color:#0f172a;\">GESTION\n"
"                                                                            D'EQUIPE<br/></span><span\n"
"                                                                            style=\"\n"
"                                                                            font-size:10pt;\n"
"                                                                            color:#94a3b8;\">Contr\u00f4lez\n"
"                                                                            les acc\u00e8s et les\n"
"                    "
                        "                                                        permissions du\n"
"                                                                            personnel</span></p></body></html>", None))
        self.btn_ajouter_caissier.setText(QCoreApplication.translate("MainWindow", u"+ Nouvel Utilisateur", None))
        self.menu_fichier.setTitle(QCoreApplication.translate("MainWindow", u"Fichier", None))
        self.menu_edition.setTitle(QCoreApplication.translate("MainWindow", u"\u00c9dition", None))
        self.menu_ventes.setTitle(QCoreApplication.translate("MainWindow", u"Ventes", None))
        self.menu_stock.setTitle(QCoreApplication.translate("MainWindow", u"Stock", None))
        self.menu_rapports.setTitle(QCoreApplication.translate("MainWindow", u"Rapports", None))
        self.menu_admin.setTitle(QCoreApplication.translate("MainWindow", u"Administration", None))
        self.menu_aide.setTitle(QCoreApplication.translate("MainWindow", u"?", None))
    # retranslateUi

