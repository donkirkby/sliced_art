# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_open_art = QAction(MainWindow)
        self.action_open_art.setObjectName(u"action_open_art")
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.actionDetails = QAction(MainWindow)
        self.actionDetails.setObjectName(u"actionDetails")
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_sort = QAction(MainWindow)
        self.action_sort.setObjectName(u"action_sort")
        self.action_sort.setCheckable(True)
        self.action_sort.setChecked(True)
        self.action_shuffle = QAction(MainWindow)
        self.action_shuffle.setObjectName(u"action_shuffle")
        self.action_shuffle.setCheckable(True)
        self.action_open_words = QAction(MainWindow)
        self.action_open_words.setObjectName(u"action_open_words")
        self.action_save_png = QAction(MainWindow)
        self.action_save_png.setObjectName(u"action_save_png")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.art = QWidget()
        self.art.setObjectName(u"art")
        self.gridLayout_3 = QGridLayout(self.art)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.art_view = QGraphicsView(self.art)
        self.art_view.setObjectName(u"art_view")

        self.gridLayout_3.addWidget(self.art_view, 0, 0, 1, 1)

        self.tabWidget.addTab(self.art, "")
        self.words = QWidget()
        self.words.setObjectName(u"words")
        self.gridLayout_2 = QGridLayout(self.words)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.word_scroll = QScrollArea(self.words)
        self.word_scroll.setObjectName(u"word_scroll")
        self.word_scroll.setWidgetResizable(True)
        self.word_content = QWidget()
        self.word_content.setObjectName(u"word_content")
        self.word_content.setGeometry(QRect(0, 0, 758, 487))
        self.word_scroll.setWidget(self.word_content)

        self.gridLayout_2.addWidget(self.word_scroll, 0, 0, 1, 1)

        self.tabWidget.addTab(self.words, "")
        self.symbols = QWidget()
        self.symbols.setObjectName(u"symbols")
        self.verticalLayout_2 = QVBoxLayout(self.symbols)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.symbols_view = QGraphicsView(self.symbols)
        self.symbols_view.setObjectName(u"symbols_view")

        self.verticalLayout_2.addWidget(self.symbols_view)

        self.tabWidget.addTab(self.symbols, "")
        self.options = QWidget()
        self.options.setObjectName(u"options")
        self.gridLayout_4 = QGridLayout(self.options)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.columns_label = QLabel(self.options)
        self.columns_label.setObjectName(u"columns_label")

        self.gridLayout_4.addWidget(self.columns_label, 1, 0, 1, 1, Qt.AlignRight)

        self.columns = QSpinBox(self.options)
        self.columns.setObjectName(u"columns")
        self.columns.setMinimum(1)
        self.columns.setMaximum(10)
        self.columns.setValue(4)

        self.gridLayout_4.addWidget(self.columns, 1, 1, 1, 1)

        self.rows = QSpinBox(self.options)
        self.rows.setObjectName(u"rows")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rows.sizePolicy().hasHeightForWidth())
        self.rows.setSizePolicy(sizePolicy)
        self.rows.setMinimum(1)
        self.rows.setMaximum(10)
        self.rows.setValue(6)

        self.gridLayout_4.addWidget(self.rows, 0, 1, 1, 1)

        self.rows_label = QLabel(self.options)
        self.rows_label.setObjectName(u"rows_label")

        self.gridLayout_4.addWidget(self.rows_label, 0, 0, 1, 1, Qt.AlignRight)

        self.groupBox = QGroupBox(self.options)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.word_clues_radio = QRadioButton(self.groupBox)
        self.word_clues_radio.setObjectName(u"word_clues_radio")
        self.word_clues_radio.setChecked(True)

        self.verticalLayout.addWidget(self.word_clues_radio)

        self.symbol_clues_radio = QRadioButton(self.groupBox)
        self.symbol_clues_radio.setObjectName(u"symbol_clues_radio")

        self.verticalLayout.addWidget(self.symbol_clues_radio)


        self.gridLayout_4.addWidget(self.groupBox, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.tabWidget.addTab(self.options, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.action_open_art)
        self.menuFile.addAction(self.action_open_words)
        self.menuFile.addAction(self.action_save)
        self.menuFile.addAction(self.action_save_png)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_exit)
        self.menuView.addAction(self.action_sort)
        self.menuView.addAction(self.action_shuffle)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_open_art.setText(QCoreApplication.translate("MainWindow", u"&Open Image...", None))
#if QT_CONFIG(shortcut)
        self.action_open_art.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"&Save as PDF...", None))
#if QT_CONFIG(shortcut)
        self.action_save.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionDetails.setText(QCoreApplication.translate("MainWindow", u"Details", None))
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
        self.action_sort.setText(QCoreApplication.translate("MainWindow", u"So&rt", None))
#if QT_CONFIG(shortcut)
        self.action_sort.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.action_shuffle.setText(QCoreApplication.translate("MainWindow", u"Shu&ffle", None))
#if QT_CONFIG(shortcut)
        self.action_shuffle.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.action_open_words.setText(QCoreApplication.translate("MainWindow", u"Open &Word File...", None))
#if QT_CONFIG(whatsthis)
        self.action_open_words.setWhatsThis(QCoreApplication.translate("MainWindow", u"Download from https://github.com/donkirkby/vograbulary/blob/master/core/assets/wordlist.txt", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(shortcut)
        self.action_open_words.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+W", None))
#endif // QT_CONFIG(shortcut)
        self.action_save_png.setText(QCoreApplication.translate("MainWindow", u"Save as &Image...", None))
#if QT_CONFIG(shortcut)
        self.action_save_png.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.art), QCoreApplication.translate("MainWindow", u"Art", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.words), QCoreApplication.translate("MainWindow", u"Words", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.symbols), QCoreApplication.translate("MainWindow", u"Symbols", None))
        self.columns_label.setText(QCoreApplication.translate("MainWindow", u"Columns:", None))
        self.rows_label.setText(QCoreApplication.translate("MainWindow", u"Rows:", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Clue Type:", None))
        self.word_clues_radio.setText(QCoreApplication.translate("MainWindow", u"Words", None))
        self.symbol_clues_radio.setText(QCoreApplication.translate("MainWindow", u"Symbols", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.options), QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
    # retranslateUi

