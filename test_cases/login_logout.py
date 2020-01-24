#coding=utf-8
# __autor__='wyxces'
import re

import requests

from configs.read_configini import projectConf
from common.logger_wyx import log
from common.requests_wyx import requestWyx


# 定义登录
def wyx_login():
    #  获取项目的基本信息
    user = projectConf.user
    pwd = projectConf.pwd

    # 输入网址 禁止自动重定向 获取重定向地址(用户管理系统地址)
    res_project = requestWyx.request_wyx('get', allow_redirects=False)
    uums_url = res_project.headers['Location']
    log.debug('res_base: location:{}'.format(uums_url))
    __set_jsessionid(res_project, 'pro')


    # 请求用户管理的地址 获取execution 和 uums_jsessionid值 用于后续登录
    res_uums = requestWyx.request_wyx('get', base_url=uums_url)
    res_uums_str = res_uums.text
    pattern = re.compile('execution" value="(.*?)"')
    execution = pattern.findall(res_uums_str)[0]
    log.debug('execution:{}'.format(execution))
    __set_jsessionid(res_uums, 'uums')


    # 在用户管理系统登录  不限制重定向
    data = {
        'username': user,
        'password': pwd,
        'execution': execution,
        '_eventId': 'submit'
    }
    header = {
        'Cookie': 'JSESSIONID={}'.format(projectConf.get_uums_jsessionid())
    }
    requestWyx.request_wyx('post', data=data, base_url=uums_url, headers=header)

# 定义登出
def wyx_logout():
    # project 登出
    api = '/logout'
    res_project = requestWyx.request_wyx(method='get', api=api, allow_redirects=False)
    status_code = res_project.status_code
    if status_code == 200:
        uums_url = res_project.json()
    elif status_code == 302:
        uums_url = res_project.headers['Location']

    # uums 登出
    header = {
        'Cookie': 'JSESSIONID={}'.format(projectConf.get_uums_jsessionid())
    }
    requestWyx.request_wyx('get',base_url=uums_url, headers=header, allow_redirects=False)


# 设置jsessionid信息
def __set_jsessionid(res, key):
    cookies = requests.utils.dict_from_cookiejar(res.cookies)
    log.debug('cookies:{}'.format(cookies))
    jsessionid = cookies['JSESSIONID']
    log.debug('key:{},jsessionid:{}'.format(key, jsessionid))
    if key == 'pro':
        projectConf.set_pro_jsessionid(jsessionid)
    elif key == 'uums':
        projectConf.set_uums_jsessionid(jsessionid)
    else:
        log.error('key：{}错误，不在key[pro, uums]中'.format(key))
        raise AttributeError


if __name__ == '__main__':
    wyx_logout()
    wyx_login()
    wyx_logout()
