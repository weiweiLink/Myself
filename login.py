# -*- coding: utf-8 -*-
import io
import os
import threading
import cv2
import numpy as np
import sys
from SSD.ssd import SSD
from RetinaNet.retinanet import  Retinanet
from FasterRCNN.frcnn import FRCNN
import lucy_rc
from PIL import Image
from PyQt5 import QtSql
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegExp, QRect, QThread, Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QRegExpValidator, QPixmap, QImage
from PyQt5.QtWidgets import *
import mysql

# 在类的开头添加数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'database': 'mydb', 
    'user': 'root',
    'password': '123456'
}

class Ui_MainWindow(QMainWindow):
    result1Ready = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.db = None
        self.init_database()
        self.selected_filename = None
        self.selected_data = None
        # insertion_completed = pyqtSignal()
        self.video_worker = None
    def init_database(self):
        """初始化数据库连接"""
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(DB_CONFIG['host'])
        self.db.setDatabaseName(DB_CONFIG['database']) 
        self.db.setUserName(DB_CONFIG['user'])
        self.db.setPassword(DB_CONFIG['password'])
        
        if self.db.open():
            QMessageBox.information(self, '成功', '连接服务器成功！')
            self.setupUi(self)
        else:
            QMessageBox.warning(self, '失败', f'连接服务器失败: {self.db.lastError().text()}')
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1030, 670)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        MainWindow.setMinimumSize(QtCore.QSize(1030, 670))  # 设置最小尺寸
        MainWindow.setMaximumSize(QtCore.QSize(1030, 670))  # 设置最大尺寸（可根据需要调整）
        MainWindow.setSizeIncrement(QtCore.QSize(0, 0))
        MainWindow.setBaseSize(QtCore.QSize(0, 0))
        MainWindow.setAcceptDrops(False)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("#MainWindow {background-image: url(:/pic/img/08528dc614e93cb78feb1c584ece8534.jpg);}\n"
"")
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(140, 50, 771, 91))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Heavy")
        font.setPointSize(72)
        self.label.setFont(font)
        self.label.setMouseTracking(False)
        self.label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label.setAcceptDrops(False)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("background-color: transparent; \n"
"color: rgb(255, 255, 255);")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setOpenExternalLinks(False)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 250, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(28)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(320, 350, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(28)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_3.setObjectName("label_3")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(270, 490, 591, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self._2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self._2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self._2.setContentsMargins(0, 3, 0, 6)
        self._2.setSpacing(7)
        self._2.setObjectName("_2")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setAutoDefault(True)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self._2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setAutoDefault(True)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self._2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setStyleSheet("")
        self.pushButton_3.setAutoDefault(True)
        self.pushButton_3.setDefault(False)
        self.pushButton_3.setFlat(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self._2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setStyleSheet("")
        self.pushButton_4.setAutoDefault(True)
        self.pushButton_4.setDefault(False)
        self.pushButton_4.setFlat(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self._2.addWidget(self.pushButton_4)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(420, 250, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(26)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit_2.setGeometry(QtCore.QRect(420, 350, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(26)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(260, 610, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_4.setObjectName("label_4")
        self.layoutWidget.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.label_4.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "欢迎登录"))
        self.label.setText(_translate("MainWindow", "头盔佩戴检测系统"))
        self.label_2.setText(_translate("MainWindow", "账号"))
        self.label_3.setText(_translate("MainWindow", "密码"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton_2.setText(_translate("MainWindow", "管理员登录"))
        self.pushButton_3.setText(_translate("MainWindow", "学生注册"))
        self.pushButton_4.setText(_translate("MainWindow", "管理员注册"))
        self.label_4.setText(_translate("MainWindow", "头盔佩戴识别系统v1.0"))
        self.lineEdit_2.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]{16}"), self))
        self.pushButton.clicked.connect(self.gust_login)
        self.pushButton_2.clicked.connect(self.admin_login)
        self.pushButton_3.clicked.connect(self.gust_z)
        self.pushButton_4.clicked.connect(self.admin_z)
    def gust_login(self):
        id = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        
        if not id or not password:
            QMessageBox.warning(self, '登录失败', '账号或密码不能为空！')
            return
        
        # Change ? to %s for PyMySQL parameter placeholder
        sql = "select * from guest where id=%s"
        result = mysql.query(sql, id)
        
        if not result:
            QMessageBox.warning(self, '登录失败', '账号不存在！')
            return
        
        if password == result[0][2]:
            QMessageBox.information(self, '登录成功', '您好，欢迎登录！')
            self.result1Ready.emit(id)
            ui_jiemian.show()
            main.hide()
        else:
            QMessageBox.warning(self, '登录失败', '密码错误！')
    def admin_login(self):
        id = self.lineEdit.text()
        password = self.lineEdit_2.text()
        sql1 = "select * from admin where id=%s"
        result1 = mysql.query(sql1, id)
        if (id and password) == '':
            QMessageBox.warning(self, '登录失败', '账号或密码不能为空！')
        elif result1 == ():
            QMessageBox.warning(self, '登录失败', '账号不存在！')
        elif password == result1[0][2]:
            QMessageBox.information(self, '登录成功', '管理员您好！')

            ui_admin1.show()
            main.hide()
        elif password != result1[0][2]:
            QMessageBox.information(self, '登录失败', '密码错误！')
    def gust_z(self):
        ui_gust.show()
        main.hide()
    def admin_z(self):
        v, k = QInputDialog.getText(self, '管理员', '请输入管理员密码', QLineEdit.Password)
        if k == True:
            if v == '413':
                ui_admin.show()
                main.hide()
            else:
                QMessageBox.warning(self, '警告', '密码错误！！')
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出", "确认是否退出头盔佩戴识别系统",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                               
        if reply == QMessageBox.Yes:
            self.cleanup()
            event.accept()
        else:
            event.ignore()
        
    def cleanup(self):
        """清理资源"""
        if self.video_worker:
            self.video_worker.stop()
            self.video_worker.join()
            self.video_worker = None
        
        # 清理UI
        self.lineEdit.clear()
        self.lineEdit_2.clear() 
        
        # 关闭数据库连接
        if self.db and self.db.isOpen():
            self.db.close()

class guestUi_Dialog(QDialog):
    def __init__(self):
        super(guestUi_Dialog, self).__init__()
        self.setupUi(self)  # 初始化窗体设置
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(715, 669)
        Dialog.setAcceptDrops(True)
        Dialog.setAutoFillBackground(True)
        Dialog.setStyleSheet("#Dialog{background-image: url(:/pic/img/7aa0995c1ddfbd63fe65e9aea65fa9e0.jpg);}")
        self.lineEdit_6 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(270, 210, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_6.setStyleSheet("")
        self.lineEdit_6.setText("")
        self.lineEdit_6.setFrame(False)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_7.setGeometry(QtCore.QRect(270, 290, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_7.setStyleSheet("")
        self.lineEdit_7.setText("")
        self.lineEdit_7.setFrame(False)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_8.setGeometry(QtCore.QRect(270, 370, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_8.setStyleSheet("")
        self.setFixedSize(self.width(), self.height());
        self.lineEdit_8.setText("")
        self.lineEdit_8.setFrame(False)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(200, 550, 131, 51))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(170, 30, 381, 101))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(72)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(210, 210, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(210, 290, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(210, 370, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(210, 460, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.lineEdit_9 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_9.setGeometry(QtCore.QRect(270, 460, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_9.setStyleSheet("")
        self.lineEdit_9.setText("")
        self.lineEdit_9.setFrame(False)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(40, 260, 121, 161))
        self.label_6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(60, 440, 75, 23))
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setEnabled(True)
        self.comboBox.setGeometry(QtCore.QRect(270, 460, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.comboBox.setFont(font)
        self.comboBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.comboBox.setAcceptDrops(True)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(True)
        self.comboBox.setEditable(True)
        self.comboBox.setFrame(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, "大数据学院")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(380, 550, 131, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.retranslateUi(Dialog)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.activated['QString'].connect(self.lineEdit_9.setText)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "学生注册"))
        self.pushButton.setText(_translate("Dialog", "注册"))
        self.label.setText(_translate("Dialog", "学生注册"))
        self.label_2.setText(_translate("Dialog", "姓名"))
        self.label_3.setText(_translate("Dialog", "学号"))
        self.label_4.setText(_translate("Dialog", "密码"))
        self.label_5.setText(_translate("Dialog", "学院"))
        self.comboBox.setItemText(1, _translate("Dialog", "理学院"))
        self.comboBox.setItemText(2, _translate("Dialog", "建规学院"))
        self.pushButton_2.setText(_translate("Dialog", "返回登录"))
        self.pushButton_3.setText(_translate("Dialog", "选择照片"))
        self.pushButton_2.clicked.connect(self.loing)
        self.pushButton.clicked.connect(self.suceess)
        self.pushButton_3.clicked.connect(self.selectImage)
        self.name = self.lineEdit_6.text()
        self.id = self.lineEdit_7.text()
        self.password = self.lineEdit_8.text()
        self.admic = self.lineEdit_9.text()
        self.lineEdit_7.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]{16}"), self))
        self.lineEdit_8.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]{16}"), self))
    def selectImage(self):
        self.thread = ImageSelectionThread()
        self.thread.imageSelected.connect(self.handleImageSelection)
        self.thread.run()
        # Set default image if none selected
        if not hasattr(self, 'selected_filename'):
            self.setDefaultImage()

    def setDefaultImage(self):
        # Assuming you have a default image in your resources
        default_image_path = "no_thing.jpg"  # Update this path
        try:
            with open(default_image_path, 'rb') as file:
                self.selected_data = file.read()
            self.selected_filename = default_image_path
            
            # Display default image
            image = QtGui.QPixmap(default_image_path)
            self.label_6.setPixmap(image)
            self.label_6.setScaledContents(True)
        except Exception as e:
            print(f"Error loading default image: {e}")

    def handleImageSelection(self, filename, data):
        # 在此处处理选择的图片文件，例如显示在界面上
        cover_img = os.path.abspath(filename)
        image = QtGui.QPixmap(cover_img)
        self.label_6.setPixmap(image)
        self.label_6.setScaledContents(True)
        # 将图片数据存储到实例变量中，以便在成功注册时使用
        self.selected_filename = filename
        self.selected_data = data
    def loing(self):
        main.show()
        ui_gust.close()
    def suceess(self):
        name = self.lineEdit_6.text()
        id = self.lineEdit_7.text()
        password = self.lineEdit_8.text()
        admic = self.lineEdit_9.text()
        sql1 = "select * from guest where id=%s"
        result = mysql.query(sql1, id)
        
        if name == "" or id == "" or password == "" or admic == "" == "":
            QMessageBox.warning(self, "失败", '请输入完整信息')
            return
        elif result != ():
            QMessageBox.warning(self, "失败", '该账号已存在！')
            return
        else:
            # Check if image is selected, if not use default
            if not hasattr(self, 'selected_filename'):
                self.setDefaultImage()
        
        # 在新线程中执行数据库插入操作
        thread = threading.Thread(target=self.insert_user_to_database, args=(name, id, password, admic))
        thread.run()
    def insert_user_to_database(self, name, id, password, admic):
        # 使用实例变量的值
        filename = self.selected_filename
        data = self.selected_data
        # 执行用户信息插入操作
        insert_user_query = "INSERT INTO guest (name, id, password, admic,filename,data) VALUES (%s, %s, %s, %s,%s,%s)"
        user_values = (name, id, password, admic,filename,data)
        mysql.exec(insert_user_query, user_values)
        QMessageBox.information(self, "成功", '注册成功！！！')
class ImageSelectionThread(QThread):
    imageSelected = QtCore.pyqtSignal(str, bytes)
    def run(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filename, _ = QFileDialog.getOpenFileName(None, '选择图片文件', '', '图片文件 (*.jpg *.png)', options=options)
        if filename:
            with open(filename, 'rb') as file:
                data = file.read()
            self.imageSelected.emit(filename, data)
            
class admin1Ui_Dialog(QDialog):
    def __init__(self):
        super(admin1Ui_Dialog, self).__init__()
        self.setupUi(self)
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(830, 668)
        Dialog.setStyleSheet("#Dialog{background-image: url(:/pic/img/7aa0995c1ddfbd63fe65e9aea65fa9e0.jpg);}")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 100, 831, 521))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255,0.9);\n"
                                      "selection-background-color: rgb(255, 0, 127);\n"
                                      "")
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 255, 255,0.9);")
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgb(255, 255, 255,0.9);")
        self.pushButton_3.setCheckable(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "学生信息"))
        self.pushButton.setText(_translate("Dialog", "修改学生信息"))
        self.pushButton_2.setText(_translate("Dialog", "查看学生信息"))
        self.pushButton_3.setText(_translate("Dialog", "返回"))
        self.setFixedSize(self.width(), self.height())
        self.pushButton_2.clicked.connect(self.view)
        self.pushButton_3.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.edit)
    def back(self):
        main.show()
        ui_admin1.close()
    def view(self):
        ui_infoview.show()
    def edit(self):
        ui_edit.show()
class adminUi_Dialog(QDialog):
    def __init__(self):
        super(adminUi_Dialog, self).__init__()
        self.setupUi(self)  # 初始化窗体设置
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(715, 669)
        Dialog.setAcceptDrops(True)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("#Dialog{background-image: url(:/pic/img/7aa0995c1ddfbd63fe65e9aea65fa9e0.jpg);}")
        self.lineEdit_6 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_6.setGeometry(QtCore.QRect(270, 210, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_6.setStyleSheet("")
        self.lineEdit_6.setText("")
        self.lineEdit_6.setFrame(False)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_7.setGeometry(QtCore.QRect(270, 290, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_7.setStyleSheet("")
        self.lineEdit_7.setText("")
        self.lineEdit_7.setFrame(False)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_8.setGeometry(QtCore.QRect(270, 370, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_8.setStyleSheet("")
        self.lineEdit_8.setText("")
        self.lineEdit_8.setFrame(False)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(200, 550, 131, 51))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 30, 471, 101))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(72)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(210, 210, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(210, 290, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(210, 370, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(210, 460, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_5.setObjectName("label_5")
        self.lineEdit_9 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_9.setGeometry(QtCore.QRect(270, 460, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(22)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit_9.setStyleSheet("")
        self.lineEdit_9.setText("")
        self.lineEdit_9.setFrame(False)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setEnabled(True)
        self.comboBox.setGeometry(QtCore.QRect(270, 460, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(9)
        self.comboBox.setFont(font)
        self.comboBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.comboBox.setAcceptDrops(True)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(True)
        self.comboBox.setEditable(True)
        self.comboBox.setFrame(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, "大数据学院")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(380, 550, 131, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.retranslateUi(Dialog)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.activated['QString'].connect(self.lineEdit_9.setText) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "管理员注册"))
        self.pushButton.setText(_translate("Dialog", "注册"))
        self.label.setText(_translate("Dialog", "管理员注册"))
        self.label_2.setText(_translate("Dialog", "姓名"))
        self.label_3.setText(_translate("Dialog", "学号"))
        self.label_4.setText(_translate("Dialog", "密码"))
        self.label_5.setText(_translate("Dialog", "学院"))
        self.comboBox.setItemText(1, _translate("Dialog", "理学院"))
        self.comboBox.setItemText(2, _translate("Dialog", "建规学院"))
        self.pushButton_2.setText(_translate("Dialog", "返回登录"))
        self.lineEdit_7.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]{16}"), self))
        self.lineEdit_8.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]{16}"), self))
        self.pushButton_2.clicked.connect(self.login)
        self.pushButton.clicked.connect(self.sueess)
        self.setFixedSize(self.width(), self.height())
    def login(self):
        main.show()
        ui_admin.close()
    def sueess(self):
        name = self.lineEdit_6.text()
        id = self.lineEdit_7.text()
        password = self.lineEdit_8.text()
        admic = self.lineEdit_9.text()
        sql1 = "select * from admin where id=%s"
        result = mysql.query(sql1, id)
        if (name and id and password and admic) == "":
            QMessageBox.warning(self, "失败", '请输入完整信息')
        elif result!=():
            QMessageBox.warning(self, "失败", '该账号已存在！')
        else:
            # 执行更新操作
            sql = "insert into admin(name,id,password,admic) values(%s, %s, %s, %s)"
            mysql.exec(sql, (name, id, password, admic))
            sql1='INSERT into guest(name,id,password,admic) SELECT *FROM admin where id=%s'
            mysql.exec(sql1, id)
            QMessageBox.information(self, "成功", '注册成功！！！')
class infoview(QMainWindow):
    def __init__(self):
        super(infoview, self).__init__()
        self.setupUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(784, 600)
        MainWindow.setStyleSheet("#label{background-image: url(:/pic/img/36aff965c35636526d572abd7363ba30.jpg);}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 821, 121))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(48)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("\n"
                                 "color: rgb(255, 255, 255);")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(-5, 121, 791, 481))
        self.tableView.setObjectName("tableView")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(-6, 100, 81, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setFixedSize(self.width(), self.height())
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.tableView.horizontalHeader().setFont(font)  # 重新设置表头的字体
        self.model = QtSql.QSqlTableModel()
        self.tableView.setModel(self.model)
        self.model.setTable('guest')
         # 查询所有数据 # 设置数据模型的数据表
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        # 设置表格头
        self.model.select()
        self.tableView.hideColumn(4)  # 隐藏第4列，索引从0开始
        self.tableView.hideColumn(5)  # 隐藏第5列
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, '姓名')
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, '学号')
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, '密码')
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, '学院')
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "查看学生信息"))
        self.label.setText(_translate("MainWindow", "学生信息"))
        self.pushButton.setText(_translate("MainWindow", "刷新"))
        self.pushButton.clicked.connect(self.updata)
    def updata(self):
        self.model.select()
class editinfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(931, 600)
        MainWindow.setStyleSheet("#label{background-image: url(:/pic/img/36aff965c35636526d572abd7363ba30.jpg);}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 931, 121))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(48)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("\n"
"color: rgb(255, 255, 255);")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(780, 180, 151, 91))
        self.pushButton.setStyleSheet("font: 22pt \"Agency FB\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(780, 330, 151, 91))
        self.pushButton_2.setStyleSheet("font: 22pt \"Agency FB\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(780, 470, 151, 91))
        self.pushButton_3.setStyleSheet("font: 22pt \"Agency FB\";")
        self.pushButton_3.setObjectName("pushButton_3")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(-5, 121, 791, 481))
        self.tableView.setObjectName("tableView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setFixedSize(self.width(), self.height())
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        # self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.tableView.horizontalHeader().setFont(font)  # 重新设置表头的字体
        self.model = QtSql.QSqlTableModel()
        self.tableView.setModel(self.model)
        self.model.setTable('guest')  # 设置数据模型的数据表
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)  # 允许字段更改
        self.model.select()  # 查询所有数据
        self.tableView.hideColumn(4)
        self.tableView.hideColumn(5)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, '姓名')
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, '学号')
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, '密码')
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, '学院')
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "管理信息"))
        self.label.setText(_translate("MainWindow", "管理学生信息"))
        self.pushButton.setText(_translate("MainWindow", "添加信息"))
        self.pushButton_2.setText(_translate("MainWindow", "删除信息"))
        self.pushButton_3.setText(_translate("MainWindow", "保存"))
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.dele)
        self.pushButton_3.clicked.connect(self.save)

    def dele(self):
        current_index = self.tableView.currentIndex().row()
        if self.model and current_index >= 0:
            self.model.removeRow(current_index)
            if not self.model.submitAll():
                QMessageBox.warning(self, 'Error', 'Failed to delete the record.')
            self.model.select()

    def add(self):
        if self.model:
            new_row_index = self.model.rowCount()
            self.model.insertRow(new_row_index)

            # Initialize fields with default values if needed
            self.model.setData(self.model.index(new_row_index, 0), "")
            self.model.setData(self.model.index(new_row_index, 1), "")
            self.model.setData(self.model.index(new_row_index, 2), "")
            self.model.setData(self.model.index(new_row_index, 3), "")
            # Add more fields as necessary

            if not self.model.submitAll():
                QMessageBox.warning(self, 'Error', f'Failed to add the record. Error: {self.model.lastError().text()}')
            self.model.select()

    def save(self):
        if self.model.submitAll():
            QMessageBox.information(self, 'Success', '保存成功！！')
        else:
            QMessageBox.warning(self, 'Error', 'Failed to save the changes.')
        self.model.select()
class jiemian(QMainWindow):
    def __init__(self):
        self.detector = MyDetection()
        super().__init__()
        self.setupUi(self)
        self.video_worker = None
        self.signals = WorkerSignals()
        self.signals.update_frame.connect(self.update_frame_display)
        self.signals.error.connect(self.display_error)
        self.model_name = None
        self.signals.clear_ui.connect(self.clear_label_9)
        self.db = None
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1131, 853)
        MainWindow.setStyleSheet(
            "#MainWindow{background-image: url(:/pic/img/896b9d3f8c7ebdf3ce07347e0ed68912.jpeg);}\n"
            "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(780, 640, 781, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(900, 470, 121, 41))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 22pt \"Agency FB\";")
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(960, 560, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255,0);\n"
                                      "color: rgb(255, 255, 255);")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(880, 510, 21, 141))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(790, 690, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("\n"
                                   "font: 20pt \"Agency FB\";\n"
                                   "color: rgb(255, 255, 255);")
        self.label_8.setObjectName("label_8")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(770, 0, 20, 851))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 0, 451, 71))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(48)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "font: 48pt \"Agency FB\";")
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(900, 560, 61, 31))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 20pt \"Agency FB\";")
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(960, 600, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lineEdit_3.setMouseTracking(True)
        self.lineEdit_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_3.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEdit_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "background-color: rgb(255, 255, 255,0);\n"
                                      "font: 20pt \"Agency FB\";")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setFrame(False)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(900, 520, 54, 32))
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 20pt \"Agency FB\";")
        self.label_5.setObjectName("label_5")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(780, 500, 781, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(900, 600, 61, 31))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 20pt \"Agency FB\";")
        self.label_2.setObjectName("label_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(780, 510, 111, 141))
        self.label_7.setStyleSheet("background-color: rgb(255, 255, 255,0);")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(960, 520, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lineEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.lineEdit.setStyleSheet("\n"
                                    "background-color: rgb(255, 255, 255,0);\n"
                                    "color: rgb(255, 255, 255);")
        self.lineEdit.setText("")
        self.lineEdit.setFrame(False)
        self.lineEdit.setObjectName("lineEdit")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(780, 190, 351, 281))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 224, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(184, 184, 184))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 224, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 251, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 251, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 224, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(242, 224, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        self.calendarWidget.setPalette(palette)
        self.calendarWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calendarWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.calendarWidget.setStyleSheet("color: rgb(0, 0, 255);\n"
                                          "background-image: url(:/pic/img/634f6678718c91d689c6d4e4058fe5cc.jpeg);")
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setSelectionMode(QtWidgets.QCalendarWidget.NoSelection)
        self.calendarWidget.setObjectName("calendarWidget")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(-10, 70, 791, 791))
        self.label_9.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_9.setObjectName("label_9")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(0, 0, 111, 31))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(900, 820, 151, 31))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(790, 790, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(850, 790, 251, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(920, 650, 161, 131))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(860, 10, 221, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(25)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("font: 25pt \"Agency FB\";\n"
                                    "color: rgb(255, 255, 255);")
        self.label_10.setObjectName("label_10")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(790, 80, 101, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(900, 80, 101, 61))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(1010, 80, 101, 61))
        self.pushButton_8.setObjectName("pushButton_8")
        self.layoutWidget.raise_()
        self.line_4.raise_()
        self.label_3.raise_()
        self.lineEdit_2.raise_()
        self.line_5.raise_()
        self.label_8.raise_()
        self.label.raise_()
        self.label_4.raise_()
        self.lineEdit_3.raise_()
        self.label_5.raise_()
        self.line_3.raise_()
        self.label_2.raise_()
        self.label_7.raise_()
        self.lineEdit.raise_()
        self.calendarWidget.raise_()
        self.label_9.raise_()
        self.line_2.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.label_6.raise_()
        self.lineEdit_4.raise_()
        self.label_10.raise_()
        self.pushButton_4.raise_()
        self.pushButton_7.raise_()
        self.pushButton_8.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "头盔佩戴检测系统"))
        self.label_3.setText(_translate("MainWindow", "个人信息"))
        self.label_8.setText(_translate("MainWindow", "输入方式"))
        self.label.setText(_translate("MainWindow", "实时检测画面"))
        self.label_4.setText(_translate("MainWindow", "学号"))
        self.label_5.setText(_translate("MainWindow", "姓名"))
        self.label_2.setText(_translate("MainWindow", "学院"))
        self.label_9.setText(_translate("MainWindow", "TextLabel"))
        self.pushButton_5.setText(_translate("MainWindow", "返回"))
        self.pushButton_6.setText(_translate("MainWindow", "网络摄像头"))
        self.label_6.setText(_translate("MainWindow", "IP地址"))
        self.pushButton_3.setText(_translate("MainWindow", "图片文件"))
        self.pushButton_2.setText(_translate("MainWindow", "视频文件"))
        self.pushButton.setText(_translate("MainWindow", "内置摄像头"))
        self.label_10.setText(_translate("MainWindow", "选择网络模型"))
        self.pushButton_4.setText(_translate("MainWindow", "SSD"))
        self.pushButton_7.setText(_translate("MainWindow", "RetinaNet"))
        self.pushButton_8.setText(_translate("MainWindow", "FasterRCNN"))
        self.pushButton_5.clicked.connect(self.back)
        self.pushButton_3.clicked.connect(self.photos)
        self.pushButton_2.clicked.connect(self.video_file)
        self.pushButton.clicked.connect(self.video_strme)
        self.pushButton_6.clicked.connect(self.get_ip)
        self.pushButton_4.clicked.connect(self.SSD_model)
        self.pushButton_7.clicked.connect(self.RetinaNet_model)
        self.pushButton_8.clicked.connect(self.FasterRCNN_model)
    def stop_video(self):
        self.signals.clear_ui.emit()
        if self.video_worker is not None:
            self.video_worker.stop()
            self.video_worker.join()
            self.video_worker = None
        self.signals.clear_ui.emit()

    def clear_label_9(self):
        self.label_9.clear()
    def SSD_model(self):
        self.stop_video()
        self.model_name = "SSD"
        self.detector = MyDetection(self.model_name)
        QMessageBox.information(self, '成功', '加载SSD网络成功！')
    def RetinaNet_model(self):
        self.stop_video()
        self.model_name = "RetinaNet"
        self.detector =MyDetection(self.model_name)
        QMessageBox.information(self, '成功', '加载RetinaNet网成功！')
    def FasterRCNN_model(self):
        self.stop_video()
        self.model_name = "FasterRCNN"
        self.detector =MyDetection(self.model_name)
        QMessageBox.information(self, '成功', '加载FasterRCNN网络成功！')
    def back(self):
        if self.video_worker is not None:
            self.video_worker.stop()
            self.video_worker.join()
            self.video_worker = None
        ui_jiemian.close()
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.label_9.clear()
        self.label_7.clear()
        main.show()
    def info(self,id):
        sql1 = "select * from guest where id=%s"
        result1 = mysql.query(sql1, id)
        self.lineEdit.setText(result1[0][0])
        self.lineEdit_2.setText(result1[0][1])
        self.lineEdit_3.setText(result1[0][3])
        if result1[0][5]!=None:
            image = Image.open(io.BytesIO(result1[0][5]))
            image = image.convert("RGBA")
            data = image.tobytes("raw", "RGBA")
            qimage = QPixmap.fromImage(
                QImage(data, image.size[0], image.size[1], QImage.Format_RGBA8888))
            self.label_7.setPixmap(qimage)
            self.label_7.setScaledContents(True)

    def photos(self):
        if self.model_name == None:
            QMessageBox.warning(self, '警告', '请加载网络模型！')
        else:
            if self.video_worker is not None:
                self.video_worker.stop()
                self.video_worker.join()
                self.video_worker = None
            file_name, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Image files (*.jpg *.png)')
            if file_name:
                self.load_and_process_image(file_name)

    def load_and_process_image(self, file_name):
        try:
            result_image = self.detector.process_image(file_name)
            if result_image:
                result_image = result_image.convert('RGB')
                qim = QImage(result_image.tobytes(), result_image.width, result_image.height, result_image.width * 3,
                             QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qim)
                self.label_9.setPixmap(
                    pixmap.scaled(self.label_9.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            print(f"处理图片时出错: {e}")
    def get_ip(self):
        ip = self.lineEdit_4.text()
        if ip:
            self.video_net(ip)
    def video_net(self,ip):
        if self.model_name == None:
            QMessageBox.warning(self, '警告', '请加载网络模型！')
        else:
            if ip:
                if self.video_worker is not None:
                    self.video_worker.stop()
                    self.video_worker.join()
                self.video_worker = VideoWorker(self.detector, ip, self.signals)
                self.video_worker.start()

    def update_frame_display(self, pixmap):
        self.label_9.setPixmap(pixmap.scaled(self.label_9.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

    def display_error(self, message):
        QMessageBox.warning(self, '错误', message)

    def video_strme(self):
        if self.model_name == None:
            QMessageBox.warning(self, '警告', '请加载网络模型！')
        else:
            if self.video_worker is not None:
                self.video_worker.stop()
                self.video_worker.join()
            self.video_worker = VideoWorker(self.detector, 0, self.signals)
            self.video_worker.start()

    def video_file(self):
        if self.model_name == None:
            QMessageBox.warning(self, '警告', '请加载网络模型！')
        else:
            file_name, _ = QFileDialog.getOpenFileName(self, '选择视频', '', 'Video files (*.mp4 *.avi)')
            if file_name:
                if self.video_worker is not None:
                    self.video_worker.stop()
                    self.video_worker.join()
                self.video_worker = VideoWorker(self.detector, file_name, self.signals)
                self.video_worker.start()
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出", "确认是否退出头盔佩戴识别系统",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                               
        if reply == QMessageBox.Yes:
            self.cleanup()
            event.accept()
        else:
            event.ignore()
        
    def cleanup(self):
        """清理资源"""
        if self.video_worker:
            self.video_worker.stop()
            self.video_worker.join()
            self.video_worker = None
        
        # 清理UI
        self.lineEdit.clear()
        self.lineEdit_2.clear() 
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.label_9.clear()
        
        # 关闭数据库连接
        if self.db and self.db.isOpen():
            self.db.close()

class MyDetection:
    def __init__(self,model_name=None):
        self.model = None
        if model_name == "SSD":
            self.model = SSD()
        elif model_name == "RetinaNet":
            self.model = Retinanet()
        elif model_name == "FasterRCNN":
            self.model = FRCNN()
    def process_image(self, image_path):
        try:
            image = Image.open(image_path)
            result_image = self.model.detect_image(image)
            return result_image
            # result_image.show()
        except IOError:
            print('打开错误！请再试一次，并确保图片路径正确。')

    def process_video(self, video_source):
        capture = cv2.VideoCapture(video_source)
        if not capture.isOpened():
            print(f'打开视频源错误：{video_source}')
            return

        try:
            while True:
                ret, frame = capture.read()
                if not ret:
                    print('没有帧可读')
                    break
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(np.uint8(frame))
                frame = np.array(self.model.detect_image(frame))
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                yield frame
        finally:
            capture.release()
            
    def convert_to_pixmap(self, frame):
        qt_frame = QImage(frame.data, frame.shape[1], frame.shape[0], 
                         frame.strides[0], QImage.Format_BGR888)
        return QPixmap.fromImage(qt_frame)
        
    def stop(self):
        self.running.clear()

class WorkerSignals(QObject):
    update_frame = pyqtSignal(QPixmap)
    error = pyqtSignal(str)
    clear_ui = pyqtSignal()
class VideoWorker(threading.Thread):
    def __init__(self, detector, video_source, signals):
        super().__init__()
        self.detector = detector
        self.video_source = video_source
        self.signals = signals
        self.running = threading.Event()
        self.running.set()

    def run(self):
        capture = cv2.VideoCapture(self.video_source)
        if not capture.isOpened():
            self.signals.error.emit(f'无法打开视频源：{self.video_source}')
            return
            
        try:
            while self.running.is_set():
                ret, frame = capture.read()
                if not ret:
                    break
                    
                # 处理帧
                frame = self.process_frame(frame)
                
                # 转换为Qt图像并发送
                pixmap = self.convert_to_pixmap(frame)
                self.signals.update_frame.emit(pixmap)
                
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            capture.release()
            
    def process_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(np.uint8(frame))
        frame = np.array(self.detector.model.detect_image(frame))
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
    def convert_to_pixmap(self, frame):
        qt_frame = QImage(frame.data, frame.shape[1], frame.shape[0], 
                         frame.strides[0], QImage.Format_BGR888)
        return QPixmap.fromImage(qt_frame)
        
    def stop(self):
        self.running.clear()

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    main =Ui_MainWindow()
    ui_gust = guestUi_Dialog()
    ui_admin = adminUi_Dialog()
    ui_admin1 = admin1Ui_Dialog()
    ui_infoview = infoview()
    ui_edit = editinfo()
    ui_jiemian = jiemian()
    main.result1Ready.connect(ui_jiemian.info)
    main.show()
    sys.exit(app.exec_())