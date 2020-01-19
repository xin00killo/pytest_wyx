#coding=utf-8
# __autor__='wyxces'

import configparser
import os

conf = configparser.ConfigParser()


def getConf(*args, **kwargs):
        conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')  # 文件路径
        print(conf_path)
        conf.read(conf_path, encoding="utf-8-sig")  # 读取文件
        return conf

# 读取项目文件信息
class Wyx():
    def __init__(self):
        self.cf = getConf()
        self.base_url = self.get_value('base_url')
        self.url_1 = self.get_value('url_1')
        self.user = self.get_value('user')
        self.pwd = self.get_value('pwd')

    def get_value(self, name):
        return self.cf.get('wyx', name)



wyx = Wyx()