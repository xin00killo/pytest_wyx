#coding=utf-8
# __autor__='wyxces'

import logging
import os
import time

from common.wyx_utils import singleton

@singleton
class WyxLogger():
    def __init__(self):
        # 创建一个logging对象
        self.logger =logging.getLogger("wyx")
        #  设置log文件监控的级别
        self.logger.setLevel(logging.DEBUG)

        # 创建log文件 及 输出日志到log文件
        log_time = time.strftime('%Y%m%d_%H%M%S ',time.localtime())
        log_path = os.path.join(os.path.dirname(os.getcwd()), 'logs/')
        # print(os.getcwd(),log_path)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_name = log_path + 'wyxces' + log_time + '.log'
        fh =logging.FileHandler(log_name,encoding='utf-8') # 以utf-8的方式，将内容输出到 log文件中
        fh.setLevel(logging.INFO)  # 在日志捕获的基础上，日志输出到 log文件的级别

        # 输出日志到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '%(asctime)s-%(name)s-%(levelname)s-%(module)s-%(lineno)s-%(message)s---%(filename)s---%(funcName)s')
        ch.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger 添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)



if __name__ == '__main__':
    l = WyxLogger()
    l3 = WyxLogger()
    l4 = WyxLogger()
    l5 = WyxLogger()

