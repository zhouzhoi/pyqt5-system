import pymysql
import ListDevices

#打开数据库连接
conn = pymysql.connect(host="localhost",user = "root",passwd = "42003717",db = "zhou")
#获取游标
cursor=conn.cursor()
# print(cursor)
# 获取数据列表
data_list = ListDevices.getallDevice()
# 遍历数据列表并插入数据库
for item in data_list:
    device_id = item["device_id"]
    node_id = item["node_id"]
    device_name = item["device_name"]
    product_name = item["product_name"]
    status = item["status"]
    # 执行插入语句
    sql = f"INSERT INTO shebei (device_id, status,device_name,product_name,node_id) VALUES ('{device_id}', '{status}','{device_name}', '{product_name}','{node_id}')"
    cursor.execute(sql)

# 提交更改到数据库
conn.commit()

# 关闭游标和数据库连接
cursor.close()
conn.close()
