# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uart_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(652, 515)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setEnabled(False)

        self.verticalLayout.addWidget(self.textBrowser)

        self.textEntryWidget = QWidget(Form)
        self.textEntryWidget.setObjectName(u"textEntryWidget")
        self.horizontalLayout = QHBoxLayout(self.textEntryWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.textEntryWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.configButton = QPushButton(self.textEntryWidget)
        self.configButton.setObjectName(u"configButton")

        self.horizontalLayout.addWidget(self.configButton)


        self.verticalLayout.addWidget(self.textEntryWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.configButton.setText(QCoreApplication.translate("Form", u"Configure", None))
    # retranslateUi

