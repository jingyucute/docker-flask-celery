#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Description: 
Author: jingyu
Date: 2022-01-16 13:33:25
LastEditors: Please set LastEditors
LastEditTime: 2022-01-18 23:53:13
'''

from abc import ABCMeta, abstractmethod

class BaseDB(metaclass=ABCMeta):
    def __init__(self, host, port, user, passwd, db):
        self._db_conf = {
            'host': host,
            'port': port,
            'user': user,
            'passwd': passwd,
            'db' : db
        }

    @abstractmethod
    def get_conn(self):
        pass

    '''
        获取最后执行的sql语句
    '''
    def get_last_sql(self):
        return ''

    '''
        获取该数据库下的所有表
    '''
    @abstractmethod
    def get_all_tables(self):
        pass

    '''
        在该数据库下创建表
    '''
    @abstractmethod
    def create_table(self, table):
        pass

    '''
        删除数据库下的表
    '''
    @abstractmethod
    def drop_table(self, table):
        pass

    @abstractmethod
    def get_table_indexes(self, table):
        pass
    
    '''
        在对应表格上创建索引
    '''
    @abstractmethod
    def create_indexes_on_table(self, table, indexes):
        pass
    
    '''
        删除对应表格上的索引
    '''
    @abstractmethod
    def drop_indexes_on_table(self, table, indexes):
        pass

    @abstractmethod
    def insert(self, table, insert_data, batch=5000):
        pass

    @abstractmethod
    def delete(self, table, where_data):
        pass
    
    @abstractmethod
    def select(self, table, fields, where_data):
        pass
    
    @abstractmethod
    def update(self, table, set_data, where_data, default_data={}):
        pass

    '''
        格式化投射字段
    '''
    def format_select_fields(self, fields):
        pass

    '''
        the data requementes
        1. must be list or turple
        2. the data element must be dict
    '''
    def _is_data_many(self, data):
        if (isinstance(data, list) or isinstance(data, tuple)) and isinstance(data[0], dict):
            return True
        elif isinstance(data, dict):
            return False
        raise Exception("data type error", "data must is a dict list or dict turple")

    # 处理默认值为 ''
    def _deal_default(self, default_value):
        if default_value is None:
            return ''
        else:
            return default_value
 
    '''
        判断值是否为None 或 ''
    '''
    def _is_value_empty(self, value):
        if value is None:
            return True
        if value is '':
            return True 
        return False


