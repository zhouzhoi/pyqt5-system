import pymysql
#打开数据库连接
conn = pymysql.connect(host="localhost",user = "root",passwd = "42003717",db = "zhou")
#获取游标
cursor=conn.cursor()
print(cursor)

#创建user表
cursor.execute('drop table if exists login')
sql1= """CREATE TABLE login(
     name VARCHAR(128) NOT NULL, 
     passwd VARCHAR(256) NOT NULL,  
     PRIMARY KEY(name)
 )  ; """
sql2="insert into login values(%s,%s)"
cursor.execute(sql1)
# inser one way 1
cursor.execute("insert into login values('admin','123456')")
# insert one way 2
cursor.execute(sql2,('admin2','123456'))
# insert some way3
cursor.executemany(sql2,[('admin3','123456'),('admin4','123456')])

cursor.close()#先关闭游标
conn.commit()
conn.close()#再关闭数据库连接
print('创建数据表成功')