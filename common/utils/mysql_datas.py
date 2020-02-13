#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx

from common.common.mysql_wyx import MysqlWyx
from common.common import logger_wyx

'''
将所有常用的数据库库表字段取 根据id取值 每次执行只能取出条数据的值）
'''


class TargetTable:
    def __init__(self, target_table_id, log=None):
        """
        目标表数据
        :param target_table_id: 目标表id  查询条件
        :param log: 传入log  可以将谁调用此模块就记录到那个logname中
        """
        self.log = log if log is not None else logger_wyx.log
        self.target_table_id = target_table_id

    def __get_value(self, key):
        mysql = MysqlWyx('t')
        sql_str = 'select {} from target_table_id where target_table_id={} limit 1'.format(key, self.target_table_id)
        value = mysql.select_one(sql_str)[0]
        mysql.dispose()
        return value

    def frontend_position_info_id(self):
        return self.__get_value('frontend_position_info_id')

    def label_en(self):
        return self.__get_value('label_en')

    def label_cn(self):
        return self.__get_value('label_cn')

    def frontend_entity_type(self):
        return self.__get_value('frontend_entity_type')

    def version(self):
        return self.__get_value('version')

    def merge_type(self):
        return self.__get_value('merge_type')

    def belong_db_en(self):
        return self.__get_value('belong_db_en')

    def element_type(self):
        return self.__get_value('element_type')

    def category(self):
        return self.__get_value('category')

    def label_type(self):
        return self.__get_value('label_type')

    def subject_label_id(self):
        return self.__get_value('subject_label_id')

    def object_label_id(self):
        return self.__get_value('object_label_id')

    def is_inited(self):  # 是否初始化
        return self.__get_value('is_inited')

    def is_calc(self):  # 是否纳入计算
        return self.__get_value('is_calc')

    def is_standard(self):
        return self.__get_value('is_standard')

    def description(self):
        return self.__get_value('description')

    def update_flag(self):  # 标识是否有更新
        return self.__get_value('update_flag')

    def created_at(self):
        return self.__get_value('created_at')

    def updated_at(self):
        return self.__get_value('updated_at')

class FrontendMapping:
    def __init__(self, target_table_id=None, frontend_entity_id=None, log=None):
        """
        前端映射表
        :param target_table_id: 目标表id  查询条件
        :param frontend_entity_id: 实体映射id  查询条件
        :param log: 传入log  可以将谁调用此模块就记录到那个logname中
        """
        self.log = log if log is not None else logger_wyx.log
        if target_table_id is None and frontend_entity_id is None:
            raise AttributeError('参数错误！target_table_id 和 frontend_entity_id 不能同时为None')
        elif target_table_id is None and frontend_entity_id is not None:
            self.frontend_entity_id = frontend_entity_id
            __sql_str = 'select target_table_id from target_table_id where frontend_entity_id = {}'.\
                format(self.frontend_entity_id)
            self.target_table_id = self.__get_value('target_table_id', __sql_str)
        elif target_table_id is not None and frontend_entity_id is None:
            self.target_table_id = target_table_id
            self.frontend_entity_id = self.__get_value('frontend_entity_id')
        else:
            self.target_table_id = target_table_id
            self.frontend_entity_id = frontend_entity_id

    def __get_value(self, key, sql_str=None):
        mysql = MysqlWyx('t')
        sql_str = 'select {} from target_table_id where target_table_id={} limit 1'.\
            format(key, self.target_table_id) if sql_str is None else sql_str
        value = mysql.select_one(sql_str)[0]
        mysql.dispose()
        return value

    def frontend_position_info_id(self):
        return self.__get_value('frontend_position_info_id')

    def frontend_mapping_id(self):
        return self.__get_value('frontend_mapping_id')

    def frontend_subject_id(self):
        return self.__get_value('frontend_subject_id')

    def frontend_object_id(self):
        return self.__get_value('frontend_object_id')

    def frontend_entity_type(self):
        return self.__get_value('frontend_entity_type')

    def icon_name(self):
        return self.__get_value('icon_name')

    def description(self):
        return self.__get_value('description')

    def update_flag(self):
        return self.__get_value('update_flag')

    def created_at(self):
        return self.__get_value('created_at')

    def updated_at(self):
        return self.__get_value('updated_at')


class FrontendPositionInfo:
    def __init__(self, frontend_entity_id, log=None):
        """
        前端坐标信息
        :param frontend_entity_id: 目标表id  查询条件
        :param log: 传入log  可以将谁调用此模块就记录到那个logname中
        """
        self.log = log if log is not None else logger_wyx.log
        self.frontend_entity_id = frontend_entity_id

    def __get_value(self, key):
        mysql = MysqlWyx('t')
        sql_str = 'select {} from target_table_id where target_table_id={} limit 1'.format(key, self.frontend_entity_id)
        value = mysql.select_one(sql_str)[0]
        mysql.dispose()
        return value

    def frontend_position_info_id(self):
        return self.__get_value('frontend_position_info_id')

    def position_x(self):
        return self.__get_value('position_x')

    def position_y(self):
        return self.__get_value('position_y')

    def description(self):
        return self.__get_value('description')

    def update_flag(self):
        return self.__get_value('update_flag')
