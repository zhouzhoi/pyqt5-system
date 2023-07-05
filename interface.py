from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPalette

from LoginUi import  *
from interfaceUi import  *
from smoke_gui import *
from PyQt5.QtWidgets import *
from shebeiUi import *
from yushi import Ui_YushiForm
import pymysql
import sys
import re
import yushi_value_from_shadow as yvfs
import Exception
import shebeidemo
import yushi
import Frist


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.setup_ui()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 消除周边的框框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 设置阴影

        # 设置跳转
        self.ui.pushButton_shebei.clicked.connect(self.shebei)
        self.ui.pushButton_jiance.clicked.connect(self.jiance)
        self.ui.pushButton_data.clicked.connect(self.data)
        self.ui.pushButton_logout.clicked.connect(self.log_out)
        self.show()

    def jiance(self):
        # self.close()
        self.yushi = Frist.YushiForm()
        self.yushi.show()

    def shebei(self):
        # self.close()
        self.shebei = shebeidemo.shebeiDemo()
        self.shebei.show()

    def data(self):
        self.data = Exception.ExceptionWindow()
        self.data.show()

    def setup_ui(self):
        self.setupUi(self)
        # self.setdate()
        self.currentSmokeValue()

    def log_out(self):
        global user_now
        self.close()
        self.login = Frist.LoginWindow()
        user_now=''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow1 = MainWindow()
    mywindow1.show()
    sys.exit(app.exec_())
