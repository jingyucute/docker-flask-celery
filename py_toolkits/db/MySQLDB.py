#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Description: MySQLDB 工具
Author: jingyu
Date: 2022-01-16 14:23:43
LastEditors: Please set LastEditors
LastEditTime: 2022-01-19 01:05:11
'''

from .BaseDB import BaseDB
import MySQLdb

class MySQLDB(BaseDB):
    def __init__(self, host, port, user, passwd, db, charset='utf8', autocommit=True):
        super().__init__(host, port, user, passwd, db)
        self._db_conf['charset'] = charset
        self.conn = None
        self.cursor = None
        self._autocommit = autocommit
        self._table = None
        self.last_execute_sql = None
        self.conn = self.get_conn()
        self.cursor = self.get_cursor(MySQLdb.cursors.DictCursor)

    def get_conn(self):
        if self.conn is not None:
            self.conn.ping()
            return self.conn
        try:
            self.conn = MySQLdb.connect(**self._db_conf)
        except Exception as e:
            raise e 
        return self.conn

    def get_cursor(self, cursor_type=None):
        if not self.conn:
            self.get_conn()
        else:
            self.conn.ping()
        try:
            self.cursor = self.conn.cursor(cursor_type)
        except Exception as e:
            raise e 
        return self.cursor

    def get_last_sql(self):
        return self.last_execute_sql

    def get_all_tables(self):
        show_sql = "SHOW TABLES"
        tables = self.execute(show_sql)
        return [ v for table in tables for k, v in table.items()]

    '''
        简单实现创建表
        input: 
          {
              "id": "INT UNSIGNED AUTO_INCREMENT PRIMARY KEY",
              "name": "varchar(50) NOT NULL DEFAULT ''"
              ....
          }
    '''
    def create_table(self, table, col_items={}):
        create_sql = ""
        for column, property in col_items.items():
            create_sql += """
                `{column}` {property},""".format(column=column, property=property)
        create_sql = create_sql.strip()[:-1]
        if create_sql:
            create_sql = """
                CREATE TABLE IF NOT EXISTS `{table}` (
                    {create_body}
                )
            """.format(table=table, create_body=create_sql)
            return self.execute(create_sql)

    def drop_table(self, table):
        delete_table_sql = """DROP TABLE IF EXISTS `{table}`""".format(table=table)
        return self.execute(delete_table_sql)

    def get_table_indexes(self, table):
        index_sql = """SHOW INDEX FROM {table}""".format(table=table)
        idxs = self.execute(index_sql)
        exists_index = {}
        for idx in idxs:
            key_name =idx['Key_name']
            index_type = idx['Index_type']
            column = idx['Column_name']
            non_unique = idx['Non_unique']
            if key_name == "PRIMARY":
                type = "PRIMARY"
            elif index_type == "FULLTEXT":
                type = "FULLTEXT"
            elif non_unique == 0:
                type = "UNIQUE"
            else:
                type = "NORMAL"
            if key_name in exists_index:
                exists_index[key_name]['column'].append(column)
            else:
                exists_index[key_name] = {
                    'index_name': key_name,
                    'column': [column],
                    'type': type
                }
        return list(exists_index.values())

    '''
        创建索引
        indexes structure
        [{"index_name": "idx_name", "column": ["column1", ...], "type": "NORMAL"}, ...]
        特别说明
            # 当创建主键时， index_name 的值需为PRIMARY
            type: 
                NORMAL UNIQUE FULLTEXT PRIMARY

        若原表存在相同的索引， 则修改
    '''
    def create_indexes_on_table(self, table, indexes, cover=False):
        if not indexes:
            return
        exists_idx_list = self.get_table_indexes(table)
        exists_indexes = {}
        for idx in exists_idx_list:
            exists_indexes[idx['index_name']] = idx
        index_sql = ""
        for index in indexes:
            idx_name = index['index_name']
            columns = index['column']
            type = index['type']
            column_str = self.format_select_fields(columns) 
            if idx_name in exists_indexes:
                # 原来存在相同的索引
                if cover:
                    # 删除
                    if type == "PRIMARY":
                        index_sql += """
                            DROP INDEX PRIMARY KEY,
                            ADD PRIMARY KEY ({column_str}),""".format(column_str=column_str)
                    else:
                        type_str = ""
                        if type in ["UNIQUE", "FULLTEXT"]:
                            type_str = type
                        index_sql += """
                            DROP INDEX `{idx_name}`,
                            ADD {type_str} INDEX `{idx_name}`({column_str}),""".format(idx_name=idx_name, type_str=type_str,column_str=column_str)
                else:
                    print("索引重复, 且不覆盖: ", table, index)
            else:
                if type == "PRIMARY":
                    index_sql += """
                        ADD PRIMARY KEY ({column_str}),""".format(column_str=column_str)
                else:
                    type_str = ""
                    if type in ["UNIQUE", "FULLTEXT"]:
                        type_str = type
                    index_sql += """
                        ADD {type_str} INDEX `{idx_name}`({column_str}),""".format(idx_name=idx_name, type_str=type_str,column_str=column_str)
        index_sql = index_sql.strip()[:-1]
        if index_sql:
            index_sql = "ALTER TABLE `%s` " % table + index_sql
            return self.execute(index_sql)

    '''
        根据传入的索引名进行删除, 传入空不删除所有的索引
        input:
          ["PRIMARY", 'idx1', .... ],
        说明:
            删除主键需要写定 PRIMARY
    '''
    def drop_indexes_on_table(self, table, indexes):
        if isinstance(indexes, str):
            indexes = [indexes]
        exists_idx_list = self.get_table_indexes(table)
        exists_indexes = {}
        
        for idx in exists_idx_list:
            exists_indexes[idx['index_name']] = idx
        drop_idx_sql = ""
        for idx_name in indexes:
            if idx_name in exists_indexes:
                type = exists_indexes[idx_name]['type']
                if type == "PRIMARY":
                    drop_idx_sql += """
                        DROP PRIMARY KEY,
                    """
                else:
                    drop_idx_sql += """
                        DROP INDEX `{idx_name}`,""".format(idx_name=idx_name)
            else:
                print("%s does not exist index[%s]" % (table, idx_name))
        drop_idx_sql = drop_idx_sql.strip()[:-1]
        if drop_idx_sql:
            drop_idx_sql = "ALTER TABLE %s " % table + drop_idx_sql
            return self.execute(drop_idx_sql)

    # 获取表的字段
    def get_table_fields(self, table):
        try:
            self.cursor.execute("SHOW FIELDS FROM %s" % table)
            fields = list([each['Field'] for each in self.cursor.fetchall()])
            return fields
        except Exception as e:
            raise e

    '''
        格式化投射字段
        input: ['filed1', 'field2 as f2', ....]
        output: `field1`, `field2` as `f2`
    '''
    def format_select_fields(self, fields):
        fields_str = ",".join([
           "`{0}` as `{1}`".format(*field.split(' as ')) if ' as ' in field else "`%s`" % field  for field in fields
        ])
        return fields_str

    '''
        将数据格式化成sql语句需要代替的形式
    '''
    def format_data(self, data, where_data=None, defaults={}, is_many=False):
        if is_many:
            fields = list(data[0].keys())
            fields.sort()
            data_list = []
            if where_data is None:
                where_data = []
            for i, each in enumerate(data):
                cur_where_data = {}
                if 0 <= i < len(where_data):
                    cur_where_data = where_data[i]
                cur_where_keys = list(cur_where_data.keys())
                data_list.append(
                    tuple(
                        [
                            each.get(field) if not self._is_value_empty(each.get(field))
                            else self._deal_default( defaults.get(field) if defaults else None )
                            for field in fields
                        ]
                        + 
                        [
                           cur_where_data.get(key) for key in cur_where_keys
                        ]
                    )
                )
            return data_list
        else:
            fields = list(data.keys())
            fields.sort()
            format_data = [
              data.get(field) if not self._is_value_empty(data.get(field)) 
              else  self._deal_default( defaults.get(field) if defaults else '' )
              for field in fields
            ]
            if where_data:
                # 涉及到索引问题， 保持原配置顺序
                where_keys = list(where_data.keys())
                format_data += [ where_data[key] for key in where_keys ]
            return tuple(format_data)


    '''
        select 查询语句
        input:
          table -> table_name
          fields -> [] or ['col1', 'col2'],
          where_data -> 'where id < 15 limit 3'
    '''
    def select(self, table, fields, where_data=None):
        if fields: 
            fields_str = self.format_select_fields(fields)
        else:
            fields_str = "*"
        if where_data:
            select_sql = "SELECT %s FROM %s %s" % (fields_str, table, where_data)
        else:
            select_sql = "SELECT %s FROM %s " % (fields_str, table)

        return self.execute(select_sql)
    
    '''
        根据封装好的数据格式， 插入数据
        input:
            1. table_name, {"c1": "v1", "c2": "v2"}
            2. table_name, [{"c1": "v1", "c2": "v2"}, {"c1": "v3", "c2": "v4"}, ...]
    '''
    def insert(self, table, insert_data, batch=5000):
        is_many = self._is_data_many(insert_data)
        fields = list(insert_data[0].keys() if is_many else insert_data.keys())
        fields.sort()
        insert_fields_str = self.format_select_fields(fields)
        value_s_str = ",".join(["%s" for i in range(len(fields))])
        format_data = self.format_data(insert_data,is_many=is_many)
        insert_sql = "INSERT INTO `%s`(%s) VALUES(%s)" % (table, insert_fields_str, value_s_str)
        
        try:
            self.last_execute_sql = insert_sql
            if is_many:
                index = 0
                while index < len(insert_data):
                    self.cursor.executemany(insert_sql, format_data[index: index + batch])
                    index += batch
            else:
                self.cursor.execute(insert_sql, format_data)
            if self._autocommit:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
    '''
        更新语句
        input
          1. table_name {set_c1: v1, ...}  {where_c1:w1, ...}
          2. table_name [{set_c1: v11, ...}, {set_c1: v12, ...}] [{where_c1:w11, ...}, {where_c1:w12, ...}]
        关于 default_data:
          在 set_data 复制时， 若字段为None， 可以从default_data中找默认值，并处理
    '''
    def update(self, table, set_data, where_data, default_data={}):
        is_many = self._is_data_many(set_data)
        if not is_many:
            set_data = [set_data]
            where_data = [where_data]
        format_data = self.format_data(set_data, where_data, default_data, is_many=True)
        try:
            for i in range(len(set_data)):
                fields = list(set_data[i].keys())
                fields.sort()
                set_str = ",".join([ "`%s` = %s" % (field, "'%s'" if isinstance(set_data[i].get(field), str) else "%s") for field in fields ])
                where_fields = list(where_data[i].keys())
                where_str = " AND ".join([ "`%s` = %s" % (field, "'%s'" if isinstance(where_data[i].get(field), str) else "%s") for field in where_fields ])
                update_sql = "UPDATE `%s` SET %s WHERE %s" % (table, set_str, where_str)
                update_sql = update_sql % format_data[i]
                self.last_execute_sql = update_sql
                self.cursor.execute(update_sql)
            if self._autocommit:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def delete(self, table, where_data=None):
        if where_data:
            delete_sql = "DELETE FROM `%s` %s " % (table, where_data)
        else:
            delete_sql = "DELETE FROM `%s` " % table
        return self.execute(delete_sql)

    # 执行原生sql
    def execute(self, sql):
        try:
            self.last_execute_sql = sql
            self.cursor.execute(sql)
            if self._autocommit:
                self.conn.commit
            return self.cursor.fetchall()
        except Exception as e:
            raise e

if __name__ == "__main__":
    config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "passwd": "root",
        "db": "msyql_learn"
    }
    db = MySQLDB(**config)
