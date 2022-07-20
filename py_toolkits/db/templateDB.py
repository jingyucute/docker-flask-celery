'''
Description: 
Author: jingyu
Date: 2022-01-16 14:46:13
LastEditors: Please set LastEditors
LastEditTime: 2022-01-16 23:34:21
'''

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .BaseDB import BaseDB

class TemplateDB(BaseDB):
    def __init__(self, host, port, user, passwd, db, charset='utf8', autocommit=True):
        super().__init__(host, port, user, passwd, db)
        self._db_conf['charset'] = charset
        self.conn = None
        self.conn = self.get_conn()

    def get_conn(self):
        print("get conn")

    def get_last_sql(self):
        print("last execute sql")

    def get_all_tables(self):
        print("get all tables")

    def create_table(self, table):
        print("create new table: " % table)

    def drop_table(self, table):
        print("drop table ")

    def get_table_indexes(self, table):
        print("get table indexes")

    def create_indexes_on_table(self, table, indexes):
        print("create index on table")

    def drop_indexes_on_table(self, table, indexes):
        print("drop index on table")

    def select(self, table, fields, where_data):
        print("execute select sql")

    def insert(self, table, insert_data, batch=5000):
        print("execute insert sql")

    def update(self, table, set_data, where_data, default_data={}):
        print("execute update sql")

    def delete(self, table, where_data):
        print("execute delete sql")

if __name__ == "__main__":
    config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": "db_jingyu",
        "db": "test"
    }
    db = TemplateDB(**config)
    db.insert("test", "datas")
    print(db._db_conf)