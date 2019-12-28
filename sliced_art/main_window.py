# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionAction = QAction(MainWindow)
        self.actionAction.setObjectName(u"actionAction")
        self.actionOther = QAction(MainWindow)
        self.actionOther.setObjectName(u"actionOther")
        self.actionDetails = QAction(MainWindow)
        self.actionDetails.setObjectName(u"actionDetails")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuTest = QMenu(self.menubar)
        self.menuTest.setObjectName(u"menuTest")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuTest.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuTest.addAction(self.actionAction)
        self.menuTest.addAction(self.actionOther)
        self.menuHelp.addAction(self.actionDetails)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionAction.setText(QCoreApplication.translate("MainWindow", u"Action", None))
        self.actionOther.setText(QCoreApplication.translate("MainWindow", u"Other", None))
        self.actionDetails.setText(QCoreApplication.translate("MainWindow", u"Details", None))
        self.menuTest.setTitle(QCoreApplication.translate("MainWindow", u"Test", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

