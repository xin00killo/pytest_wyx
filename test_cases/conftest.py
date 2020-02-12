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
from py._xmlgen import html
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


# 修改Environment信息
def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = "wyxces"
    config._metadata['接口地址'] = 'http://povm4.po.mlamp.cn:19198/cona-web/api/v1'
    # 删除默认信息
    config._metadata.pop("JAVA_HOME")
    config._metadata.pop("Platform")
    config._metadata.pop("Packages")
    config._metadata.pop("Plugins")
    config._metadata.pop("Python")

# 添加Summary用例描述的信息
@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("项目名称: {}".format(projectConf.project_name))])
    prefix.extend([html.p("接口地址: {}".format(projectConf.base_url))])
    prefix.extend([html.p("所属部门: {}".format(baseConf.department))])
    prefix.extend([html.p("测试人员: {}".format(baseConf.testers))])

# 修改result 表头
@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))  # 添加description列
    cells.pop(-1)  # 删除link列

# 修改result 信息内容
@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.pop(-1)  # 删除link列
    if report.passed:  # 如果测试通过，不写入html中
        del cells[:]

# 删除table_html内容  就是点击隐藏/展开中的 log日志
@pytest.mark.optionalhook
def pytest_html_results_table_html(data):
    del data[:]


# 为description列获取用例描述
@pytest.mark.hookwrapper
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()
    result.description = str(item.function.__doc__)
    if result.when == 'call':
        item.session.results[item] = result
        # 将结果写入global中
        global_wyx.set_run_result_dict(item, result)


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
