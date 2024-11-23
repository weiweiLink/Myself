import pymysql

# 打开数据库连接
def open():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='123456',
                         database='mydb',
                         port=3306)
    return db
def exec(sql,values):
    db=open() # 连接数据库
    cursor = db.cursor() # 使用cursor()方法获取操作游标
    try:
        cursor.execute(sql,values) # 执行增删改的SQL语句
        db.commit() # 提交数据
        return 1 # 执行成功
    except:
        db.rollback() # 发生错误时回滚
        return 0 # 执行失败
    finally:
        cursor.close() # 关闭游标
        db.close() # 关闭数据库连接
def exec1(sql):
    db=open() # 连接数据库
    cursor = db.cursor() # 使用cursor()方法获取操作游标
    try:
        cursor.execute(sql)
        db.commit() # 提交数据
        print('OK')
        return 1 # 执行成功
    except Exception as e:
        db.rollback()  # 发生错误时回滚
        print("执行失败:", str(e))
        return 0  # 执行失败
    finally:
        cursor.close() # 关闭游标
        db.close() # 关闭数据库连接
def query(sql,*key):
    db = open()  # 连接数据库
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    cursor.execute(sql,key)  # 执行查询SQL语句
    result = cursor.fetchall()  # 记录查询结果
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接
    return result  # 返回查询结果
def query1(sql):
    db = open()  # 连接数据库
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    cursor.execute(sql)  # 执行查询SQL语句
    result = cursor.fetchall()  # 记录查询结果
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接
    return result  # 返回查询结果
def updata():
    db=open()
    cursor = db.cursor()
    cursor.close()  # 关闭游标
    db.close()  # 关闭数据库连接