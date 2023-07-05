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
import ListDevices
import CreateCommand
import shebeidemo
import interface

user_now=''

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)#消除周边的框框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #设置阴影

        #设置跳转
        self.ui.pushButton_Login.clicked.connect(lambda :self.ui.stackedWidget_2.setCurrentIndex((0)))
        self.ui.pushButton_Register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex((1)))
        #确定按钮设置
        self.ui.pushButton_Lsure.clicked.connect(self.login_in)
        self.ui.pushButton_Rsure.clicked.connect(self.regist_in)
        self.show()

    # 按钮功能
    def login_in(self):
        account  = self.ui.lineEdit_Laccount.text()
        password = self.ui.lineEdit_Lpassword.text()
        obj = MysqlSearch()
        result = obj.get_userinfo()
        ulist = []
        plist = []
        for item in result:
            ulist.append(item['username'])
            plist.append(item['passwd'])
        for i in range(len(ulist)):
            if account == ulist[i] and password == plist[i]:
                self.win = interface.MainWindow()
                self.close()
                break
        else:
            QMessageBox.information(self, '提示', '用户密码错误')
        # if account== "11" and password=="12356":
        #     self.win = MainWindow();
        #     self.close()
        # else:
        #     print("出错了")
    def regist_in(self):
        account = self.ui.lineEdit_Raccount.text()
        password0 = self.ui.lineEdit_Rpassword.text()
        password1 = self.ui.lineEdit_Rpassword2.text()
        if len(account) == 0 or len(password0) == 0 or len(password1) == 0:
            QMessageBox.information(self, '提示', '用户与密码不得为空')
        elif password0 != password1:
            QMessageBox.information(self, '提示', '两次密码不一样')
        elif len(password0) < 6 or not re.search(r'\d', password0) or not re.search(r'[a-zA-Z]', password0):
            QMessageBox.information(self, '提示', '密码必须大于6位且包含数字和字母')
        else:
            obj = MysqlSearch()
            result = obj.get_userinfo()
            username_list = [item['username'] for item in result]

            if account in username_list:
                QMessageBox.information(self, '提示', '用户名已存在')
            else:
                conn = pymysql.connect(host="localhost", user="root", passwd="42003717", db="zhou")
                # 获取游标
                cursor = conn.cursor()
                cursor.execute(f"insert into login (username, passwd) values ('{account}','{password1}')")
                conn.commit()
                conn.close()
                QMessageBox.information(self, '恭喜', '注册成功')



#数据库连接
class MysqlSearch(object):

    # 数据库操作功能
    def __init__(self):
        self.get_conn()

    # 获取连接
    def get_conn(self):
        try:
            self.conn = pymysql.connect(host="localhost", user="root", passwd="42003717", db="zhou")
        except pymysql.Error as e:
            print('Error: %s' % e)
        return None

    def close_conn(self):
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print('Error: %s' % e)

        return None

    def get_userinfo(self):
        sql = 'SELECT * FROM login'
        # 使用cursor()方法获取操作游标
        cursor = self.conn.cursor()
        cursor.execute(sql)
        # 使用fetchall()方法获取全部数据
        result = cursor.fetchall()
        result = [dict(zip([k[0] for k in cursor.description], row)) for row in result]
        cursor.close()
        self.close_conn()
        return result

    def insert_data(self, table, data):
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
            self.conn.commit()
            cursor.close()
        except pymysql.Error as e:
            print('Error: %s' % e)
        finally:
            self.close_conn()

class YushiForm(QWidget, Ui_YushiForm):
    def __init__(self):  # 用于初始化类,定义了 __init__() 方法后，类的实例化操作会自动调用该方法。
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 消除周边的框框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self.currentValue()
        # 创建定时器，并连接到报警函数
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkSensorData)
        self.timer.start(10000)  # 每5秒触发一次定时器
        # 创建定时器，并连接到更新数据函数
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.currentValue)
        self.timer.start(1000)  # 每秒更新一次数据
        self.pushButton.clicked.connect(self.warn)

    def currentValue(self):
        value = yvfs.getvalue()
        print(value)
        wen = value[0] if len(value) > 0 else 0
        shidu = value[1] if len(value) > 0 else 0
        guangzhao = value[2] if len(value) > 0 else 0
        shuiwen = value[3] if len(value) > 0 else 0
        shengying = value[4] if len(value) > 0 else 0

        # 设置lcdNumber_shuiwen的字体颜色
        palette = self.lcdNumber_shuiwen.palette()
        if shuiwen > 60:
            palette.setColor(QPalette.WindowText, QColor("red"))
            self.textBrowser_reshuiqi.setText("ON")
        else:
            palette.setColor(QPalette.WindowText, QColor("green"))
            self.textBrowser_reshuiqi.setText("OFF")
        self.lcdNumber_shuiwen.setPalette(palette)

        # 设置lcdNumber_wen的字体颜色
        palette = self.lcdNumber_wen.palette()
        if wen > 30:
            palette.setColor(QPalette.WindowText, QColor("red"))
        else:
            palette.setColor(QPalette.WindowText, QColor("green"))
        self.lcdNumber_wen.setPalette(palette)

        # 设置lcdNumber_shidu的字体颜色
        palette = self.lcdNumber_shidu.palette()
        if shidu > 70:
            palette.setColor(QPalette.WindowText, QColor("red"))
        else:
            palette.setColor(QPalette.WindowText, QColor("green"))
        self.lcdNumber_shidu.setPalette(palette)

        # 设置lcdNumber_shengying的字体颜色
        palette = self.lcdNumber_shengying.palette()
        if shengying > 80:
            palette.setColor(QPalette.WindowText, QColor("red"))
        else:
            palette.setColor(QPalette.WindowText, QColor("green"))
        self.lcdNumber_shengying.setPalette(palette)

        # 设置lcdNumber_shengying的字体颜色
        palette = self.lcdNumber_guangzhao.palette()
        if guangzhao < 70:
            palette.setColor(QPalette.WindowText, QColor("red"))
        else:
            palette.setColor(QPalette.WindowText, QColor("green"))
        self.lcdNumber_guangzhao.setPalette(palette)

        self.lcdNumber_wen.display(wen)
        self.lcdNumber_shidu.display(shidu)
        self.lcdNumber_guangzhao.display(guangzhao)
        self.lcdNumber_shuiwen.display(shuiwen)
        self.lcdNumber_shengying.display(shengying)

        if shuiwen > 60:
            # 执行报警逻辑，例如弹出消息框或触发警报器等
            QMessageBox.warning(self, '警告', '水温超过60度！')
            self.insertData(value)  # 在获取到数据后调用插入方法

        if shengying > 80 and guangzhao < 70:
            self.textBrowser_deng.setText("ON")
            QMessageBox.warning(self, '警告', '浴室灯光已开')
            self.insertData(value)  # 在获取到数据后调用插入方法
        else:
            self.textBrowser_deng.setText("OFF")

        if wen > 30 and shidu > 70:
            self.textBrowser_tongfeng.setText("ON")
            QMessageBox.warning(self, '警告', '温度和湿度都超过正常范围！通风系统即将打开')
            self.insertData(value)  # 在获取到数据后调用插入方法
        else:
            self.textBrowser_tongfeng.setText("OFF")


    def checkSensorData(self):
        value = yvfs.getvalue()
        wen = value[0] if len(value) > 0 else 0
        shidu = value[1] if len(value) > 0 else 0
        guangzhao = value[2] if len(value) > 0 else 0
        shuiwen = value[3] if len(value) > 0 else 0
        shengying = value[4] if len(value) > 0 else 0

        if shuiwen > 60 or shengying > 80 or guangzhao < 70 or wen > 30 or shidu > 70:
            CreateCommand.CreateCommand()
            try:
                self.insertData(value)

                if shuiwen > 60:
                    QMessageBox.warning(self, '警告', '水温超过60度！')

                if shengying > 80 and guangzhao < 70:
                    QMessageBox.warning(self, '警告', '浴室灯光已开')

                if wen > 30 and shidu > 70:
                    QMessageBox.warning(self, '警告', '温度和湿度都超过正常范围！通风系统即将打开')

            except Exception as e:
                print(f"Error inserting data into the database: {str(e)}")

    def insertData(self, data):
        conn = pymysql.connect(host="localhost", user="root", passwd="42003717", db="zhou")
        cursor = conn.cursor()
        # 在这里执行插入数据的SQL语句，将data中的数据插入到数据库中
        sql = "INSERT INTO yushi (wendu, guangzhao, shidu, shuiwen, shengyin) VALUES (%s, %s, %s, %s,%s)"
        cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4]))
        conn.commit()
        cursor.close()
        conn.close()
    def warn(self):
        CreateCommand.CreateCommand();

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec_())
