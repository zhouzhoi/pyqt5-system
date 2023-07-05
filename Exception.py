import sys
from datetime import datetime

import pymysql
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QHeaderView
from PyQt5 import QtCore, QtGui, QtWidgets
from ExceptionUi import Ui_ExceptionWindow
from PyQt5.QtChart import QChartView, QChart, QLineSeries, QCategoryAxis, QValueAxis


class ExceptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ExceptionWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.load)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 消除周边的框框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 自动调整列宽为填满表格
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.setAlternatingRowColors(True)  # 使表格颜色交错显示

        # 创建图表和图表视图
        self.chart = QChart()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        layout = QtWidgets.QVBoxLayout(self.ui.graphicsView)
        layout.addWidget(self.chart_view)

    def load(self):
        try:
            conn = pymysql.connect(host="localhost", user="root", passwd="42003717", db="zhou")
            cursor = conn.cursor()
            # 执行查询语句，获取所有数据
            cursor.execute("SELECT * FROM yushi")
            data = cursor.fetchall()
            # 清空表格
            self.ui.tableWidget.clear()
            self.ui.tableWidget.setRowCount(0)
            # 设置表格的列数和列名
            self.ui.tableWidget.setColumnCount(len(data[0]))  # 假设数据的每行具有相同的列数
            column_names = ['温度', '光照', '湿度', '水温', '声音']  # 数据库中的列名
            self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
            # 填充数据到表格
            for row_number, row_data in enumerate(data):
                self.ui.tableWidget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.ui.tableWidget.setItem(row_number, column_number, item)
            # 创建多个折线系列
            series_list = []
            for column_number in range(5):  # 假设有5个变量
                series = QLineSeries()
                series_list.append(series)
            # 将数据添加到折线系列
            for row_number, row_data in enumerate(data):
                x_value = row_number  # 直接使用行数作为横轴值
                for column_number, column_data in enumerate(row_data[:5]):  # 假设只绘制前5个变量
                    y_value = float(column_data)  # 将字符串转换为浮点数
                    if y_value is not None:
                        point = QtCore.QPointF(x_value, y_value)
                        series_list[column_number].append(point)
            # 将系列添加到图表
            for series in series_list:
                self.chart.addSeries(series)
            # 设置图表标题和轴标签
            self.chart.setTitle("多变量折线图")
            self.chart.setAnimationOptions(QChart.AllAnimations)
            self.chart.createDefaultAxes()
            self.chart.axisX().setTitleText("计数")
            self.chart.axisY().setTitleText("数值")
        except Exception as e:
            print(e)
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExceptionWindow()
    window.show()
    sys.exit(app.exec_())