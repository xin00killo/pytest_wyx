#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx

import configparser
import os
import re

import yaml

from common.common.singleton_wyx import singleton


# 初始化Conf
@singleton
class Conf:
    def __init__(self):
        self.__base_path = re.search(".*pytest_wyx", os.getcwd())[0]  # 获取根目录信息
        self.__conf_path = os.path.join(self.__base_path, r'configs/config.ini')  # 文件路径
        self.__conf = configparser.ConfigParser()
        self.__conf.read(self.__conf_path)  # 读取文件
        self.set_conf_file('base', 'base_path', self.__base_path)  # 首次调用config时存储跟目录信息

    # 设置config文件的方法
    def set_conf_file(self, section, option, value):
        self.__conf.set(section, option, value)
        with open(self.__conf_path, 'w') as fh:
            self.__conf.write(fh)

    # 设置获取conf对象的方法
    def get_conf(self):
        return self.__conf


@singleton
class BaseConf:
    def __init__(self):
        self.__cf = conf.get_conf()
        self.base_path = self.get_value('base_path')  # 获取跟目录信息
        self.log_num = eval(self.get_value('log_num'))
        self.testers = self.get_value('testers')
        self.department = self.get_value('department')

    def get_value(self, option):
        return self.__cf.get('base', option)

# 读取项目文件信息
@singleton
class ProjectConf:
    def __init__(self):
        self.__cf = conf.get_conf()
        self.project_name = self.get_value('project_name')
        self.base_url = self.get_value('base_url')
        self.user = self.get_value('user')
        self.pwd = self.get_value('pwd')

    def get_pro_jsessionid(self):
        return self.get_value('pro_jsessionid')

    def set_pro_jsessionid(self, value):
        self.__set_value('pro_jsessionid', value)

    def get_ehr_jsessionid(self):
        return self.get_value('ehr_jsessionid')

    def set_ehr_jsessionid(self, value):
        self.__set_value('ehr_jsessionid', value)

    def get_value(self, option):
        return self.__cf.get('project', option)

    @staticmethod
    def __set_value(option, value):
        conf.set_conf_file('project', option, value)

# 读取log文件配置信息
@singleton
class LogConf:
    def __init__(self):
        self.__cf = conf.get_conf()
        self.relative_path = self.get_value('relative_path')
        self.log_path = os.path.join(baseConf.base_path, self.relative_path)
        self.max_bytes_each = eval(self.get_value('max_bytes_each'))
        self.backup_count = eval(self.get_value('backup_count'))
        self.fmt_logfile = self.get_value('fmt_logfile')
        self.fmt_console = self.get_value('fmt_console')
        self.logger_name = self.get_value('logger_name')
        self.log_level_in_console = eval(self.get_value('log_level_in_console'))
        self.log_level_in_logfile = eval(self.get_value('log_level_in_logfile'))
        self.console_log_on = eval(self.get_value('console_log_on'))
        self.logfile_log_on = eval(self.get_value('logfile_log_on'))
        self.dist_log_on = eval(self.get_value('dist_log_on'))

    def get_value(self, option):
        return self.__cf.get('log', option)


@singleton
class MysqlConf:
    def __init__(self):
        self.__cf = conf.get_conf()
        self.host = self.get_value('host')
        self.port = eval(self.get_value('port'))
        self.user = self.get_value('user')
        self.pwd = self.get_value('pwd')
        self.db = self.get_value('db')
        self.charset = self.get_value('charset')
        self.mincached = eval(self.get_value('mincached'))
        self.maxcached = eval(self.get_value('maxcached'))
        self.maxconnections = eval(self.get_value('maxconnections'))
        self.blocking = self.get_value('blocking')

    def get_value(self, option):
        return self.__cf.get('mysql', option)


@singleton
class EmailConf:
    def __init__(self):
        self.__cf = conf.get_conf()
        self.host = self.get_value('host')
        self.port = eval(self.get_value('port'))
        self.user = self.get_value('user')
        self.pwd = self.get_value('pwd')
        self.sender = self.get_value('sender')
        self.receivers = self.get_value('receivers')
        self.cc = self.get_value('cc')
        self.bcc = self.get_value('bcc')
        self.subject = self.get_value('subject')
        self.test_user = self.get_value('test_user')
        self.content = self.get_value('content').format('\t')
        self.on_off = eval(self.get_value('on_off'))
        self.add_dist_log = eval(self.get_value('add_dist_log'))

    def get_value(self, option):
        return self.__cf.get('email', option)


@singleton
class JiraConf:
    def __init__(self):
        self.__cf = conf.get_conf()
        self.user = self.get_value('user')
        self.pwd = self.get_value('pwd')
        self.login_api = self.get_value('login_api')
        self.base_url = self.get_value('base_url')
        self.project_name = self.get_value('project_name')
        self.version_name = self.get_value('version_name')
        self.cycle_name = self.get_value('cycle_name')

    def get_value(self, option):
        return self.__cf.get('jira', option)


# 读取yaml文件
class YamlConf:
    def __init__(self, relative_path):
        # self.relative_path = r'configs/api_config.yml' if relative_path is None else relative_path
        self.path = os.path.join(baseConf.base_path, relative_path)

    # 获取yaml文件中的数据
    def get_data(self, key=None):
        with open(self.path, 'r',  encoding="utf-8") as f:
            cf = yaml.load(f, Loader=yaml.FullLoader)
        if key is None:  # 读取信息的key,不传默认获取所有数据
            return cf  # 返回所有数据
        else:
            return cf.get(key)  # 获取键为key的值


conf = Conf()
baseConf = BaseConf()
projectConf = ProjectConf()
logConf = LogConf()
mysqlConf = MysqlConf()
emailConf = EmailConf()
jiraConf = JiraConf()


if __name__ == '__main__':
    print(projectConf.base_url)
    print('1:', projectConf.get_pro_jsessionid())
    projectConf.set_pro_jsessionid('1223ss4')
    print('2:', projectConf.get_pro_jsessionid())
    print('log_path 信息', logConf.log_path)
    print('content', emailConf.content)
