#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
from configs.config_wyx import baseConf
from common.common.logger_wyx import log
from common.utils.functions_wyx import FilesOps
from test_cases.login_logout import login_wyx, logout_wyx

import pytest
import sys
sys.dont_write_bytecode = True
log.debug('总目录下的log呀~')


@pytest.fixture(scope='session', autouse=True)
# @pytest.fixture(scope='session')
def start_end():
    log.info('测试用例开始运行，这里是 test_cases.conftest 文件')
    log.info('开始前，先清理数据： log数据')
    fops = FilesOps('logs')
    fops.clear_files(baseConf.log_num)
    log.info('开始初始化登录信息，调用login方法')
    login_wyx()

    yield
    log.info('项目运行完毕，退出登录，调用logout方法')
    logout_wyx()

#
# @pytest.fixture(scope='function', autouse=True)
# def read_data():
#     # 预计用来获取测试数据哒~   读取yaml文件啥的哈~
#     # print('-----------------------试试看，如果等于function的话~')
#     # log.debug('根目录下的function修饰的方法来一枚')
#     pass
