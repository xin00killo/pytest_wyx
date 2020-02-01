#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor

from configs.config_wyx import mysqlConf
from common.common.logger_wyx import log


class MysqlWyx:
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self, data_type='dict'):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        log.info('创建数据库连接和游标-{}'.format('dict' if data_type == 'dict' else 'tuple'))
        self._conn = self.__get_conn()
        if data_type == 'dict':
            self._cursor = self._conn.cursor(cursor=DictCursor)
        else:
            self._cursor = self._conn.cursor()

    # 创建数据库连接池
    @staticmethod
    def __get_conn():
        if MysqlWyx.__pool is None:  # 保证只有一个连接池
            log.info('mysql 数据库连接池初始化')
            __pool = PooledDB(
                creator=pymysql,  # 使用链接数据库的模块
                mincached=1,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached=1,  # 链接池中最多闲置的链接，0和None不限制
                maxconnections=8,  # 连接池允许的最大连接数，0和None表示不限制连接数
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                host=mysqlConf.host,
                port=mysqlConf.port,
                user=mysqlConf.user,
                passwd=mysqlConf.pwd,
                db=mysqlConf.db,
                use_unicode=True,
                charset=mysqlConf.charset
            )
            return __pool.connection()

    # 执行查询，并取出所有结果集
    def select_all(self, sql, param=None):
        """
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        log.info('select_all ：sql"{}",param"{}"'.format(sql, param))
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = False
        return result

    # 执行查询，并取出第一条
    def select_one(self, sql, param=None):
        """
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        log.info('select_one ：sql"{}",param"{}"'.format(sql, param))
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    # 执行查询，并取出num条结果
    def select_many(self, sql, num, param=None):
        """
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        log.info('select_many ：sql"{}",param"{}"'.format(sql, param))
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    # 向数据表插入多条记录
    def insert_many(self, sql, values):
        """
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        log.info('insert_many ：sql"{}",values"{}"'.format(sql, values))
        count = self._cursor.executemany(sql, values)
        return count

    # 插入/删除/更新等的公用语句
    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        log.info('update ：sql"{}",param"{}"'.format(sql, param))
        return self.__query(sql, param)

    def insert(self, sql, param=None):
        """
        @summary: 插入数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要插入的  值 tuple/list
        @return: count 受影响的行数
        """
        log.info('insert ：sql"{}",param"{}"'.format(sql, param))
        return self.__query(sql, param)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        log.info('delete ：sql"{}",param"{}"'.format(sql, param))
        return self.__query(sql, param)

    # 开启自动提交
    def open_autocommit(self):
        log.info('开启自动提交,设置 autocommit = 0')
        self._conn.autocommit(1)

    # 关闭自动提交
    def close_autocommit(self):
        log.info('关闭自动提交,设置 autocommit = 0')
        self._conn.autocommit(0)

    # 结束事务
    def end(self, option='commit'):
        log.info('结束事务:提交更新 / 删除的数据')
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    # 释放连接池资源，并提交更新 / 删除的数据
    def dispose(self, is_end=1):
        log.info('cursor 和 conn 清理开始')
        if is_end == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()
        log.info('cursor 和 conn 清理完成')


if __name__ == '__main__':
    db = MysqlWyx()
    sql_str = 'select * from belong_db'
    sql_str2 = 'select * from target_attr'
    result0 = db.select_all(sql_str)
    print(type(result0), result0)
    print(str(result0))
    result1 = db.select_one(sql_str)
    print(type(result1), result1)
    print(str(result1))
    db2 = MysqlWyx('t')
    result3 = db2.select_all(sql_str)
    print(type(result3), result3)
    print(str(result3))
    result4 = db2.select_one(sql_str)
    print(type(result4), result4)
    print(str(result4))
    db2.dispose()
    db.dispose()
