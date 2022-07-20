#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Description: MongoDB 
Author: jingyu
References:
   https://pymongo.readthedocs.io/en/stable/api/index.html
Date: 2022-01-16 16:05:56
LastEditors: Please set LastEditors
LastEditTime: 2022-01-18 23:52:30
'''


from .BaseDB import BaseDB
import pymongo
import bson

class MongoDB(BaseDB):
    def __init__(self, host, port, user, passwd, db):
        super().__init__(host, port, user, passwd, db)
        self.conn = None
        self.conn= self.get_conn()

    def get_conn(self):
        if self.conn is not None:
            return self.conn
        try:
            client = pymongo.MongoClient(
                host=self._db_conf['host'],
                port=self._db_conf['port'],
                authSource=self._db_conf['db'],
                username=self._db_conf['user'],
                password=self._db_conf['passwd'],
            )
            self.conn = client[self._db_conf['db']]
            self.conn._command
        except Exception as e:
            print('建立连接失败！！！')
            raise e 
        return self.conn
    
    def get_last_sql(self):
        print("mongo get last sql is not finished now")
        return ''

    def get_all_tables(self):
        return self.conn.list_collection_names()

    def create_table(self, table):
        print("mongo db does not need to create table explicitly")
        pass

    def drop_table(self, table):
        try:
            self.conn.get_collection(table).drop()
        except Exception as e:
            print("table %s not exists" % table)

    '''
        返回索引结构
        [{xxx:1}, {xxx:1, xxx: -1}]
    '''
    def get_table_indexes(self, table):
        indexes = []
        table_idx_cursors = self.conn.get_collection(table).list_indexes()
        for cursor in table_idx_cursors:
            idx_dict = {}
            for k, v in cursor['key'].items():
                if k == '_id':
                    continue
                idx_dict[k] = int(v)
            if idx_dict:
                indexes.append(idx_dict)
        return indexes

    '''
        indexes structure
        1. {xxx: 1, xxx: -1}
        2. [{xxx: 1}, {xxx: 1, xxx: -1}]
    '''
    def create_indexes_on_table(self, table, indexes):
        index_list = []
        if indexes:
            if isinstance(indexes, dict):
                index_compound = []
                for k, v in indexes.items():
                    index_compound.append((k, v))
                index_list.append(pymongo.IndexModel(index_compound))
            elif (isinstance(indexes, list) or isinstance(indexes, tuple)) and isinstance(indexes[0], dict) :
                for index in indexes:
                    index_compound = []
                    for k, v in index.items():
                        index_compound.append((k, v))
                    index_list.append(pymongo.IndexModel(index_compound))
        if index_list:
            try:
                self.conn.get_collection(table).create_indexes(index_list)
                return True
            except Exception as e:
                print("create index failed")
                return False
        return False
                
        
    def drop_indexes_on_table(self, table, indexes):
        index_list = []
        if isinstance(indexes, dict):
            t = []
            for k, v in indexes.items():
                t.append((k, v))
            if t :
                index_list.append(t)
        elif (isinstance(indexes, list) or isinstance(indexes, tuple)) and isinstance(indexes[0], dict) :
            for index in indexes:
                t = []
                for k, v in index.items():
                    t.append((k, v))
                index_list.append(t)
        
        for index in index_list:
            try:
                self.conn.get_collection(table).drop_index(index)
            except Exception as e:
                print("drop indexes 失败, ", index)
    
    def _format_select_fileds(self, fields):
        format_fields = {}
        if fields:
            format_fields["_id"] = 0
            for field in fields:
                format_fields[field] = 1
        return format_fields

    def select(self, table, fields=[], where_data={}, offset=0, limit=None):
        if not table and not isinstance(table, str):
            raise "collection name is not str"
        format_fields = self._format_select_fileds(fields)
        try:
            if limit:
                if format_fields:
                    datas = self.conn.get_collection(table).find(where_data, format_fields).skip(offset).limit(limit)
                else:
                    datas = self.conn.get_collection(table).find(where_data).skip(offset).limit(limit)
            else:
                if format_fields:
                    datas = self.conn.get_collection(table).find(where_data, format_fields).skip(offset)
                else:
                    datas = self.conn.get_collection(table).find(where_data).skip(offset)
            results = tuple(data for data in datas)
            return results
        except Exception as e:
            raise e        

    '''
        insert_data 
        1. {a:1,b:2}
        2. [{a:1}, {a:1, b:2}]
    '''
    def insert(self, table, insert_data, batchs=5000):
        is_many = self._is_data_many(insert_data)
        if not is_many:
            # the data is dict
            insert_data = [insert_data]
        try:
            index = 0
            while index < len(insert_data):
                self.conn.get_collection(table).insert_many(insert_data[index: index+batchs])
                index += batchs
        except Exception as e:
            raise e

    '''
        简单的实现update, where中复杂的逻辑没有实现,
        可以批量实现update
        统一采用$set操作（加减操作需要自己处理好值）
    '''
    def update(self, table, set_data, where_data, default_data={}, onlyOne=False):
        is_many = self._is_data_many(set_data)
        data_list = []
        if not is_many:
            set_data = [set_data]
            if not self._is_data_many(where_data):
                where_data = [where_data]
        for i, each in enumerate(set_data):
            set_dict= {}
            # set_fields = list(each.keys())
            for k, v in each.items():
                if not self._is_value_empty(v):
                    set_dict[k] = v
                elif k in default_data and default_data[k]:
                    set_dict[k] = default_data.get(k)
                else:
                    set_dict[k] = ""
            data_list.append({
                "where": where_data[i],
                "set": {"$set": set_dict}
            })            
                    
        try:
            for data in data_list:
                if not onlyOne:
                    self.conn.get_collection(table).update_many(data['where'], data['set'], False)
                else:
                    self.conn.get_collection(table).update_one(data['where'], data['set'], False)
        except Exception as e:
            raise e 

    def delete(self, table, where_data={}, onlyOne=False):
        try:
            if onlyOne:
                self.conn.get_collection(table).delete_one(where_data)
            else:
                self.conn.get_collection(table).delete_many(where_data)
        except Exception as e:
            raise e     

    def create_object_id(self):
        return bson.ObjectId()
     
if __name__ == "__main__":
    config = {
        "host": 'localhost',
        "port": 27022,
        "user": "BerryAdmin",
        "passwd": "secret",
        "db": "xromate_mandel"
    }
    db = MongoDB(**config)
    print(db.get_all_tables())
    print(db.create_object_id())