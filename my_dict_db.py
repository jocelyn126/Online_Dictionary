"""
M 负责数据库处理
"""
import pymysql

class DataBase:
    def __init__(self):
        self.db = pymysql.connect(host="localhost",
                             port=3306,
                             user="root",
                             password="123456",
                             database="dict",
                             charset="utf8")


        self.cur = self.db.cursor()

    def close(self):
        self.cur.close()
        self.db.close()

    def do_register(self,name,password):
        sql = "select name from user where name=%s;"
        self.cur.execute(sql,[name])
        result = self.cur.fetchone()
        if result:
            return False
        sql="insert into user (name,passwd) values (%s,%s);"
        try:
            self.cur.execute(sql,[name,password])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def do_matchname(self, uname):
        sql = "select name from user where name=%s;"
        self.cur.execute(sql, [uname])
        result = self.cur.fetchone()
        if result:
            return True

    def do_matchpsw(self, upsw):
        sql = "select passwd from user where passwd=%s;"
        self.cur.execute(sql, [upsw])
        result = self.cur.fetchone()
        if result:
            return True

    def do_query(self,word):
        sql="select meaning from words where word=%s;"
        self.cur.execute(sql, [word])
        result = self.cur.fetchone() #这里直接取切片就不行， 如果返回值是空就会报错。
        if result:
            return result[0]

    def insert_history(self, name, word):
        sql="select id from user where name=%s;"
        self.cur.execute(sql,[name])
        uid=self.cur.fetchone()[0]

        sql="insert into hist (word,user_id) values (%s,%s);"
        try:
            self.cur.execute(sql,[word,uid])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def do_history(self, name):
        sql="select name, word, time from user left join hist on user.id=hist.user_id where name=%s order by time desc limit 10;"
        self.cur.execute(sql,[name])
        return self.cur.fetchall() #返回结果为元组嵌套元组



