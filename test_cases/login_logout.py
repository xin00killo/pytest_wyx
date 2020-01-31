#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx

import re
import requests

from configs.config_wyx import projectConf
from common.common.logger_wyx import log
from common.common.requests_wyx import requestWyx


# 定义登录
def login_wyx():
    #  获取项目的基本信息
    user = projectConf.user
    pwd = projectConf.pwd

    # 输入网址 禁止自动重定向 获取重定向地址(用户管理系统地址)
    res_project = requestWyx.request_wyx('get', allow_redirects=False)
    ehr_url = res_project.headers['Location']
    log.debug('res_base: location:{}'.format(ehr_url))
    __set_jsessionid(res_project, 'pro')

    # 请求用户管理的地址 获取execution 和 ehr_jsessionid值 用于后续登录
    res_ehr = requestWyx.request_wyx('get', base_url=ehr_url)
    res_ehr_str = res_ehr.text
    pattern = re.compile('execution" value="(.*?)"')
    execution = pattern.findall(res_ehr_str)[0]
    log.debug('execution:{}'.format(execution))
    __set_jsessionid(res_ehr, 'ehr')

    # 在用户管理系统登录  限制重定向
    data = {
        'username': user,
        'password': pwd,
        'execution': execution,
        '_eventId': 'submit'
    }
    headers = {'Cookie': 'JSESSIONID={}'.format(projectConf.get_ehr_jsessionid())}
    res_ehr_login = requestWyx.request_wyx('post', data=data, base_url=ehr_url, headers=headers, allow_redirects=False)
    project_login_url = res_ehr_login.headers['Location']
    log.debug('res_base: location:{}'.format(project_login_url))

    # 项目登录
    requestWyx.request_wyx('get', base_url=project_login_url)


# 定义登出
def logout_wyx():
    # project 登出
    api = '/logout'
    res_project = requestWyx.request_wyx(method='get', api=api, allow_redirects=False)
    status_code = res_project.status_code
    ehr_url = res_project.json()['data'] if status_code == 200 else res_project.headers['Location']

    # ehr 登出
    headers = {'Cookie': 'JSESSIONID={}'.format(projectConf.get_ehr_jsessionid())}
    requestWyx.request_wyx('get', base_url=ehr_url, headers=headers, allow_redirects=False)


# 设置jsessionid信息
def __set_jsessionid(res, key):
    try:
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        log.debug('cookies:{}'.format(cookies))
        jsessionid = cookies['JSESSIONID']
        log.debug('key:{},jsessionid:{}'.format(key, jsessionid))
    except Exception as msg:
        log.error('获取jsessionid错误：{}'.format(msg))
    else:
        if key == 'pro':
            projectConf.set_pro_jsessionid(jsessionid)
        elif key == 'ehr':
            projectConf.set_ehr_jsessionid(jsessionid)
        else:
            log.error('key：{}错误，不在key[pro, ehr]中'.format(key))
            raise AttributeError


if __name__ == '__main__':
    logout_wyx()
    login_wyx()
    logout_wyx()
