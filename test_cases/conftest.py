#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
from configs import global_wyx
from configs.config_wyx import baseConf, projectConf
from common.common.email_wyx import emailWyx
from common.common.mysql_wyx import MysqlWyx
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
    log.info('开始前，先清理数据： 如果之前有bug导致未能退出，所以先调用一次登出方法')
    logout_wyx()
    log.info('开始前，先清理数据： log数据')
    fops = FilesOps('logs')
    fops.clear_files(baseConf.log_num)
    log.info('开始初始化登录信息，调用login方法')
    login_wyx()
    yield
    log.info('项目运行完毕，退出登录，调用logout方法')
    logout_wyx()
    log.info('开始发送邮件~')
    emailWyx.send_email()


# 初始化以元组的方式返回查询结果的数据库连接
@pytest.fixture(scope='function')
def mysql_tuple():
    db = MysqlWyx('t')
    yield db
    db.dispose()

# 初始化以字典的方式返回查询结果的数据库连接
@pytest.fixture(scope='function')
def mysql_dict():
    db = MysqlWyx()
    yield db
    log.debug('这里是yield处开始执行哈')
    db.dispose()


def pytest_sessionstart(session):
    session.results = dict()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    if result.when == 'call':
        item.session.results[item] = result
        # 将结果写入global中
        if result.passed:
            global_wyx.set_passed_amount(global_wyx.get_passed_amount()+1)
        else:  # 不通过时 记录
            global_wyx.set_failed_amount(global_wyx.get_failed_amount()+1)
            global_wyx.set_run_result_dict(item, f'{item.function.__doc__}\t{result.nodeid}')
        print(f'item :{item},type:{type(item)},item.session:{item.session} ')
        print(f'report.nodeid:{result.nodeid},type{type(result.nodeid)}')
        print('function', item.function)
        print(f'__doc__, {item.function.__doc__},type:{type(item.function.__doc__)}')
        print(f'{item.function.__doc__}\t{result.nodeid}')


# 存储测试结果集合
def pytest_sessionfinish(session, exitstatus):
    print()
    print('run status code:', exitstatus)
    passed_amount = sum(1 for result in session.results.values() if result.passed)
    failed_amount = sum(1 for result in session.results.values() if result.failed)
    all_amount = passed_amount + failed_amount
    run_result = f'总执行用例数： {all_amount} ,there are {passed_amount} passed and {failed_amount} failed tests'
    print(run_result)
    for key,value in session.results.items():
        print(key,value)
