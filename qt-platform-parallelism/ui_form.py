# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1135, 686)
        MainWindow.setMaximumSize(QSize(1920, 1080))
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_23 = QLabel(self.centralwidget)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setMaximumSize(QSize(16777215, 150))
        self.label_23.setAutoFillBackground(True)
        self.label_23.setTextFormat(Qt.RichText)
        self.label_23.setPixmap(QPixmap(u"img/asiga-logo.png"))
        self.label_23.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_23)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_22 = QLabel(self.centralwidget)
        self.label_22.setObjectName(u"label_22")
        font = QFont()
        font.setPointSize(14)
        self.label_22.setFont(font)
        self.label_22.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_22)

        self.label_24 = QLabel(self.centralwidget)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font)
        self.label_24.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_24)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.data1 = QLabel(self.centralwidget)
        self.data1.setObjectName(u"data1")
        self.data1.setMinimumSize(QSize(100, 100))
        font1 = QFont()
        font1.setPointSize(20)
        self.data1.setFont(font1)
        self.data1.setAutoFillBackground(False)
        self.data1.setFrameShape(QFrame.StyledPanel)
        self.data1.setFrameShadow(QFrame.Raised)
        self.data1.setAlignment(Qt.AlignCenter)
        self.data1.setMargin(-6)

        self.horizontalLayout_2.addWidget(self.data1)

        self.data2 = QLabel(self.centralwidget)
        self.data2.setObjectName(u"data2")
        self.data2.setMinimumSize(QSize(100, 100))
        self.data2.setFont(font1)
        self.data2.setFrameShape(QFrame.StyledPanel)
        self.data2.setFrameShadow(QFrame.Raised)
        self.data2.setLineWidth(5)
        self.data2.setMidLineWidth(5)
        self.data2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.data2)

        self.data3 = QLabel(self.centralwidget)
        self.data3.setObjectName(u"data3")
        self.data3.setMinimumSize(QSize(100, 100))
        self.data3.setFont(font1)
        self.data3.setFrameShape(QFrame.StyledPanel)
        self.data3.setFrameShadow(QFrame.Raised)
        self.data3.setLineWidth(5)
        self.data3.setMidLineWidth(5)
        self.data3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.data3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.data4 = QLabel(self.centralwidget)
        self.data4.setObjectName(u"data4")
        self.data4.setMinimumSize(QSize(100, 100))
        self.data4.setFont(font1)
        self.data4.setFrameShape(QFrame.StyledPanel)
        self.data4.setFrameShadow(QFrame.Raised)
        self.data4.setLineWidth(5)
        self.data4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.data4)

        self.data5 = QLabel(self.centralwidget)
        self.data5.setObjectName(u"data5")
        self.data5.setMinimumSize(QSize(100, 100))
        self.data5.setFont(font1)
        self.data5.setFrameShape(QFrame.StyledPanel)
        self.data5.setFrameShadow(QFrame.Raised)
        self.data5.setLineWidth(5)
        self.data5.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.data5)

        self.data6 = QLabel(self.centralwidget)
        self.data6.setObjectName(u"data6")
        self.data6.setMinimumSize(QSize(100, 100))
        self.data6.setFont(font1)
        self.data6.setFrameShape(QFrame.StyledPanel)
        self.data6.setFrameShadow(QFrame.Raised)
        self.data6.setLineWidth(5)
        self.data6.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.data6)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.data7 = QLabel(self.centralwidget)
        self.data7.setObjectName(u"data7")
        self.data7.setMinimumSize(QSize(100, 100))
        self.data7.setFont(font1)
        self.data7.setFrameShape(QFrame.StyledPanel)
        self.data7.setFrameShadow(QFrame.Raised)
        self.data7.setLineWidth(5)
        self.data7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.data7)

        self.data8 = QLabel(self.centralwidget)
        self.data8.setObjectName(u"data8")
        self.data8.setMinimumSize(QSize(100, 100))
        self.data8.setFont(font1)
        self.data8.setFrameShape(QFrame.StyledPanel)
        self.data8.setFrameShadow(QFrame.Raised)
        self.data8.setLineWidth(5)
        self.data8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.data8)

        self.data9 = QLabel(self.centralwidget)
        self.data9.setObjectName(u"data9")
        self.data9.setMinimumSize(QSize(100, 100))
        self.data9.setFont(font1)
        self.data9.setFrameShape(QFrame.StyledPanel)
        self.data9.setFrameShadow(QFrame.Raised)
        self.data9.setLineWidth(5)
        self.data9.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.data9)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)

        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.vert_divider = QFrame(self.centralwidget)
        self.vert_divider.setObjectName(u"vert_divider")
        self.vert_divider.setMinimumSize(QSize(3, 0))
        self.vert_divider.setMaximumSize(QSize(3, 16777215))
        self.vert_divider.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.vert_divider.setFrameShape(QFrame.Shape.VLine)
        self.vert_divider.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.vert_divider)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.serialport_title1 = QGroupBox(self.centralwidget)
        self.serialport_title1.setObjectName(u"serialport_title1")
        self.gridLayout_2 = QGridLayout(self.serialport_title1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.serialport_select1 = QComboBox(self.serialport_title1)
        self.serialport_select1.setObjectName(u"serialport_select1")
        self.serialport_select1.setMaximumSize(QSize(3000, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Calibri Light"])
        font2.setPointSize(12)
        self.serialport_select1.setFont(font2)

        self.gridLayout_2.addWidget(self.serialport_select1, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.serialport_title1)

        self.button_test = QPushButton(self.centralwidget)
        self.button_test.setObjectName(u"button_test")
        self.button_test.setMinimumSize(QSize(200, 50))
        self.button_test.setMaximumSize(QSize(3000, 50))
        font3 = QFont()
        font3.setFamilies([u"Cascadia Code"])
        font3.setPointSize(12)
        font3.setBold(True)
        self.button_test.setFont(font3)

        self.verticalLayout_3.addWidget(self.button_test)

        self.grade = QGroupBox(self.centralwidget)
        self.grade.setObjectName(u"grade")
        self.gridLayout_4 = QGridLayout(self.grade)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.grade_data = QLabel(self.grade)
        self.grade_data.setObjectName(u"grade_data")
        font4 = QFont()
        font4.setPointSize(30)
        self.grade_data.setFont(font4)
        self.grade_data.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.grade_data, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.grade)

        self.parallelism = QGroupBox(self.centralwidget)
        self.parallelism.setObjectName(u"parallelism")
        self.gridLayout = QGridLayout(self.parallelism)
        self.gridLayout.setObjectName(u"gridLayout")
        self.parallelism_data = QLabel(self.parallelism)
        self.parallelism_data.setObjectName(u"parallelism_data")
        self.parallelism_data.setFont(font4)
        self.parallelism_data.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.parallelism_data, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.parallelism)

        self.identifier = QGroupBox(self.centralwidget)
        self.identifier.setObjectName(u"identifier")
        self.gridLayout_6 = QGridLayout(self.identifier)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.identifier_data = QLabel(self.identifier)
        self.identifier_data.setObjectName(u"identifier_data")
        self.identifier_data.setFont(font4)
        self.identifier_data.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.identifier_data, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.identifier)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.button_clear = QPushButton(self.centralwidget)
        self.button_clear.setObjectName(u"button_clear")
        self.button_clear.setMinimumSize(QSize(100, 50))
        self.button_clear.setMaximumSize(QSize(16777215, 50))
        font5 = QFont()
        font5.setFamilies([u"Cascadia Code"])
        font5.setPointSize(15)
        font5.setBold(True)
        self.button_clear.setFont(font5)

        self.horizontalLayout_6.addWidget(self.button_clear)

        self.button_connect_scanner = QPushButton(self.centralwidget)
        self.button_connect_scanner.setObjectName(u"button_connect_scanner")
        self.button_connect_scanner.setMinimumSize(QSize(100, 50))
        self.button_connect_scanner.setMaximumSize(QSize(250, 50))
        self.button_connect_scanner.setFont(font5)
        self.button_connect_scanner.setAutoDefault(False)

        self.horizontalLayout_6.addWidget(self.button_connect_scanner)

        self.button_save = QPushButton(self.centralwidget)
        self.button_save.setObjectName(u"button_save")
        self.button_save.setMinimumSize(QSize(100, 50))
        self.button_save.setMaximumSize(QSize(16777215, 50))
        self.button_save.setFont(font5)
        self.button_save.setAutoDefault(False)

        self.horizontalLayout_6.addWidget(self.button_save)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(2, 2)
        self.verticalLayout_3.setStretch(3, 2)
        self.verticalLayout_3.setStretch(4, 2)

        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 8)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_23.setText("")
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Build Platform Parallelism Measurement Machine", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"CHOOSE: USB Single Serial", None))
        self.data1.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.data2.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.data3.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.data4.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.data5.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.data6.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.data7.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.data8.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.data9.setText(QCoreApplication.translate("MainWindow", u"float", None))
        self.serialport_title1.setTitle(QCoreApplication.translate("MainWindow", u"Data Serial Port", None))
        self.button_test.setText(QCoreApplication.translate("MainWindow", u"TEST PLATFORM", None))
        self.grade.setTitle(QCoreApplication.translate("MainWindow", u"Grade", None))
        self.grade_data.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.parallelism.setTitle(QCoreApplication.translate("MainWindow", u"Parallelism (<= 30 micron for pass)", None))
        self.parallelism_data.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.identifier.setTitle(QCoreApplication.translate("MainWindow", u"Build Platform Identifier Code", None))
        self.identifier_data.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.button_clear.setText(QCoreApplication.translate("MainWindow", u"CLEAR", None))
        self.button_connect_scanner.setText(QCoreApplication.translate("MainWindow", u"CONNECT SCANNER", None))
        self.button_save.setText(QCoreApplication.translate("MainWindow", u"SAVE RESULT", None))
    # retranslateUi

