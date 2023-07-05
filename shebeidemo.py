import sys

import pymysql

from shebeiUi import *
from PyQt5.QtWidgets import *
import ListDevices

class shebeiDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setup_ui()
        self.ui = Ui_ManageWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 消除周边的框框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_load.clicked.connect(self.load)
        self.ui.pushButton_clear.clicked.connect(self.clear)
        self.ui.pushButton_chaxun.clicked.connect(self.search)
        # 自动调整列宽为填满表格
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget.setAlternatingRowColors(True)  # 使表格颜色交错显示

    def clear(self):
        self.ui.tableWidget.clearContents()  # 清除单元格内容

    def load(self):
        # 获取解析后的设备列表
        result = ListDevices.getallDevice()

        # 设置表格行数和列数
        row_count = len(result)
        column_count = 5  # 设备ID和状态两列
        self.ui.tableWidget.setRowCount(row_count)
        self.ui.tableWidget.setColumnCount(column_count)
        column_names = ['设备号', '产品名称', 'node_id', '设备名称', '状态']  # 数据库中的列名
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)


        # 填充表格数据
        for row, item in enumerate(result):
            device_id = item["device_id"]
            status = item["status"]
            node_id = item["node_id"]
            device_name = item["device_name"]
            product_name = item["product_name"]

            device_id_item = QTableWidgetItem(device_id)
            node_id_item = QTableWidgetItem(node_id)
            device_name_item = QTableWidgetItem(device_name)
            product_name_item = QTableWidgetItem(product_name)
            status_item = QTableWidgetItem(status)

            self.ui.tableWidget.setItem(row, 0, device_id_item)
            self.ui.tableWidget.setItem(row, 1, node_id_item)
            self.ui.tableWidget.setItem(row, 2, device_name_item)
            self.ui.tableWidget.setItem(row, 3, product_name_item)
            self.ui.tableWidget.setItem(row, 4, status_item)

        # 调整列宽以填充表格
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def search(self):
        # 获取要查询的设备编号
        keyword = self.ui.lineEdit_chaxun.text()

        # 打开数据库连接
        conn = pymysql.connect(host="localhost", user="root", passwd="42003717", db="zhou")
        # 获取游标
        cursor = conn.cursor()
        # 模糊查询匹配设备编号
        sql = "SELECT device_id,device_name,product_name,node_id,status FROM shebei WHERE device_id LIKE %s"
        # 在关键词前后添加通配符%
        keyword_with_wildcard = f"%{keyword}%"
        cursor.execute(sql, (keyword_with_wildcard,))
        # 取得记录个数，用于设置表格的行数
        row_count = cursor.rowcount
        column_names = ['设备号', '设备名称', '产品名称', 'node_id']  # 数据库中的列名
        self.ui.tableWidget.setHorizontalHeaderLabels(column_names)
        # 如果没有找到相应记录，则弹出消息框提示用户
        if row_count == 0:
            QMessageBox.warning(self, '警告', '未找到该设备！')
            return
        # 将查找结果显示在表格中
        rows = cursor.fetchall()
        vol = len(rows[0])
        self.ui.tableWidget.setRowCount(row_count)
        for i in range(row_count):
            for j in range(vol):
                temp_data = rows[i][j]
                data = QTableWidgetItem(str(temp_data))
                self.ui.tableWidget.setItem(i, j, data)
        print("成功")
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywindow1 = shebeiDemo()
    mywindow1.show()
    sys.exit(app.exec_())
