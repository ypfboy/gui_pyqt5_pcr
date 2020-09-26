# -*- coding:utf8 -*-

import random
import sqlite3
import sys
import traceback
from os.path import dirname, abspath, join, normpath


class ConnectSqlite(object):
    def __init__(self):

        self.conn = sqlite3.connect(normpath(join(dirname(dirname(abspath(__file__))), "data/prc.db")))
        self.machine_fields = ["id", "machine_num", "machine_type"]
        self.kit_fields = ["id", "pipe", "ret", "FAM", "VIC", "ROX", "HEX", "CY5", "kit_type"]

    def select(self, sql):
        c = self.conn.cursor()
        c.execute(sql)
        ret = c.fetchall()
        c.close()
        return ret


    def update(self, sql):
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
            c.close()
        except:
            traceback.print_exc()


    def create_table(self, create_table_str):
        c = self.conn.cursor()
        c.execute(create_table_str)
        self.conn.commit()
        c.close()

    def creat_kits_from_kits_def(self, key_type):
        self.update("delete from kits where kit_type='%s'" % key_type)
        # self.create_table(self.create_table_str()[1])
        ret = self.select("select * from kits_def where kit_type='%s'" % key_type)
        sql_str = ""
        for i in ret:
            sql_str += str(i) + ","
        self.update("insert into kits values%s" % sql_str[:-1])

    def create_table_str(self):
        machines_str = """
                create table machines(
                    id integer primary key autoincrement,
                    machine_num varchar(50),
                    machine_type varchar(30)
                )
                
        """

        kits_str = """
                create table kits(
                    id integer primary key autoincrement,
                    pipe varchar(50),
                    ret varchar(30),
                    FAM varchar(10),
                    VIC varchar(10),
                    ROX varchar(10),
                    HEX varchar(10),
                    CY5 varchar(10),
                    kit_type varchar(20)
                )
            
        """
        kits_def_str = """
                create table kits_def(
                    id integer primary key autoincrement,
                    pipe varchar(50),
                    ret varchar(30),
                    FAM varchar(10),
                    VIC varchar(10),
                    ROX varchar(10),
                    HEX varchar(10),
                    CY5 varchar(10),
                    kit_type varchar(20)
                )

        """
        return [machines_str, kits_str, kits_def_str]

    def test_machine(self):
        c = self.conn.cursor()
        for i in range(30):
            # 写入数据
            a = random.randint(1000, 9000)
            c.execute("insert into machines values(null , '%s-%s', '7500,7600')" % (random.choice(["7500", "7600"]), a))
        self.conn.commit()
        c.execute('select * from machines')
        # print(c.fetchall())
        c.close()


    def test_kit(self):
        g = self.conn.cursor()
        for i in range(50):
            # 写入数据
            a = random.choice(["A", "B", "C"])
            b = random.choice(["阴性", "阳性"])
            c = [random.randint(10, 50) for i in range(5)]
            d = random.choice(["新冠_达安", "新冠_硕世", "新冠_伯杰", "新冠_卓诚惠"])
            g.execute("insert into kits values(null , '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (a, b, *c, d))
        self.conn.commit()
        g.execute('select * from kits')
        ret = g.fetchall()
        # print(ret)
        g.close()
        return ret


if __name__ == '__main__':
    prc = ConnectSqlite()
    # 测试
    # conn = prc.conn
    # # a = prc.create_table("create table user(id int unsigle primary key, name varchar(20))")
    # c = conn.cursor()
    # c.execute("insert into user values('aa', 'ssssss'), ('aaa', 'ddd')")
    # c.execute('select * from user')
    # print(c.fetchall())
    # c.execute('select name from sqlite_master where type="table"')
    # print(c.fetchall())
    # c.close()

    # 创建表
    # prc.create_table(prc.create_table_str()[0])
    # prc.create_table(prc.create_table_str()[1])
    # prc.create_table(prc.create_table_str()[2])
    # prc.test_machine()
    # prc.test_kit()

    # 备份默认
    # ret = prc.select("select * from kits")
    # print(ret)
    # sql_str = ""
    # for i in ret:
    #     sql_str += str(i) + ","
    # prc.update("insert into kits_def values%s" % sql_str[:-1])

    # print(prc.select("select * from kits"))
    # print(prc.select("select * from kits_def"))

    # 查询
    # print(prc.select("select count(*) from kits where kit_type='新冠_达安'"))
    # print(prc.select("select max(id) from kits where kit_type='新冠_达安'"))

    # 恢复默认
    # print(prc.select("select * from kits"))
    # prc.creat_kits_from_kits_def()
    print(len(prc.select("select * from kits where kit_type='新冠_达安'")))

