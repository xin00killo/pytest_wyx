#coding=utf-8
# __autor__='projectces'

import configparser
import os
import re

from common.utils_wyx import singleton


"""
# 读取项目文件信息 及 基本的配置信息 和 方法
BaseConf 可以对外提供以下信息：
get_base：获取base信息的方法
get_conf：获取configparser对象的方法
set_conf：写入配置文件的方法
"""
@singleton
class BaseConf:
    def __init__(self):
        self.__base_path = re.search(".*pytest_wyx", os.getcwd())[0]  # 获取跟目录信息
        self.__conf_path = os.path.join(self.__base_path, r'configs/config.ini')  # 文件路径
        self.__conf = configparser.ConfigParser()
        self.__conf.read(self.__conf_path, encoding="utf-8-sig")  # 读取文件
        self.__set_value('base_path', self.__base_path)  # 首次调用config时存储跟目录信息,后续只要 获取base_path + 相对路径就可以啦~
        self.log_num = self.get_value('log_num')

    # 设置config文件的方法
    def _set_conf_file(self, section, option, value):
        self.__conf.set(section, option, value)
        with open(self.__conf_path, 'w') as fh:
            self.__conf.write(fh)

    # 设置获取conf对象的方法
    def get_conf(self):
        return self.__conf

    def get_base_path(self):
        return self.__base_path

    def get_value(self, option):
        return self.__conf.get('base', option)

    def __set_value(self, option, value):
        self._set_conf_file('base', option, value)

# 读取项目文件信息
@singleton
class ProjectConf():
    def __init__(self):
        self.__cf = baseConf.get_conf()
        self.project_name = self.get_value('project_name')
        self.base_url = self.get_value('base_url')
        self.user = self.get_value('user')
        self.pwd = self.get_value('pwd')

    def get_pro_jsessionid(self):
        return self.get_value('pro_jsessionid')

    def set_pro_jsessionid(self, value):
        self.__set_value('pro_jsessionid', value)

    def get_uums_jsessionid(self):
        return self.get_value('uums_jsessionid')

    def set_uums_jsessionid(self, value):
        self.__set_value('uums_jsessionid', value)

    def get_value(self, option):
        return self.__cf.get('project', option)

    def __set_value(self, option, value):
        baseConf._set_conf_file('project', option, value)

# 读取log文件配置信息
@singleton
class LogConf:
    def __init__(self):
        self.__cf = baseConf.get_conf()
        self.relative_path = self.get_value('relative_path')
        self.log_path = os.path.join(baseConf.get_base_path(), self.relative_path)
        self.max_bytes_each = eval(self.get_value('max_bytes_each'))
        # print('self.max_bytes_each', self.max_bytes_each, type(self.max_bytes_each))
        self.backup_count = eval(self.get_value('backup_count'))
        self.fmt_logfile = self.get_value('fmt_logfile')
        self.fmt_console = self.get_value('fmt_console')
        self.logger_name = self.get_value('logger_name')
        self.log_level_in_console = eval(self.get_value('log_level_in_console'))
        self.log_level_in_logfile = eval(self.get_value('log_level_in_logfile'))
        self.console_log_on = eval(self.get_value('console_log_on'))
        self.logfile_log_on = eval(self.get_value('logfile_log_on'))

    def get_value(self, option):
        return self.__cf.get('log', option)

    def __set_value(self, option, value):
        baseConf._set_conf_file('log', option, value)


baseConf = BaseConf()
projectConf = ProjectConf()
logConf = LogConf()

if __name__ == '__main__':
    print(projectConf.base_url)
    print('1:', projectConf.get_pro_jsessionid())
    projectConf.set_pro_jsessionid('1223ss4')
    print('2:', projectConf.get_pro_jsessionid())
    print('log_path 信息', logConf.log_path)


