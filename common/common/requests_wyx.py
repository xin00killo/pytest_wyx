#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
from common.common.singleton_wyx import singleton
from configs.config_wyx import projectConf
from common.common.logger_wyx import log

import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""
本模块的接口规范如下：
request_wyx(self, method, api='', data=None, base_url=None, content_type=None, timeout=5, **kwargs)
method 必填,请求方法, 支持get post put delete
api 默认值'',接收 二级前缀+接口名称 , 以 '/'开头
data 默认是None  ,用于传入 get的param参数 或者 post 的 data/json 值 或者 delete的data值 等  json参数用data传入,请求头设置为"application/json"
base_url 默认值为 config文件中配置的 [HTTP].cona_url  ,选填
content_type 默认是None ,选填  不需要传utf-8
timeout 默认值为5  ,选填
header  默认是None ,选填，建议传入 Cookie和content-type外的请求头信息

返回:
如数据校验不通过 或 请求出现错误 则返回 False , 正常请求返回 response信息  (如 方法错误,api格式不符合要求,content_tyoe 错误)
建议使用if判断后再取数
    if res:
        print(res.text)
    else:
        print('res 返回 false 用例失败')
"""


@singleton
class RequestWyx:
    def __init__(self):
        self.__base_url = projectConf.base_url
        self.content_type_list = ["text/html", "text/plain", "text/xml", "image/gif", "image/jpeg", "image/png",
                                  "application/xhtml+xml", "application/xml", "application/atom+xml",
                                  "application/json", "application/pdf", "application/msword",
                                  "application/octet-stream", "application/x-www-form-urlencoded",
                                  "multipart/form-data"]

    def request_wyx(self, method, api='', data=None, base_url=None,
                    content_type=None, timeout=5, headers=None, **kwargs):
        log.debug('调用request_wyx方法，传入参数：method:{}, api:{}, base_url:{}, content_type:{}, headers:{}, data:{}'.
                  format(method, api, base_url, content_type, headers, data))
        # 数据处理  包括大小写转换 和 base_url的确定
        method = method.lower()
        content_type = content_type.lower() if content_type is not None else content_type
        base_url = self.__base_url if base_url is None else base_url

        # 数据校验 如果不通过，直接返回 False
        __data_check_dict = {
            'method': method,
            'url': [base_url, api],
            'content_type': content_type
        }
        log.info('开始校验入参数据，待校验内容：{}'.format(__data_check_dict.keys()))
        if self.__data_check(__data_check_dict):
            log.info('数据校验失败，返回False')
            return False

        # 参数组装 url 和 header
        url = base_url + api
        header = {'Cookie': "JSESSIONID={}".format(projectConf.get_pro_jsessionid()),
                  'Connection': 'keep-alive'
                  }
        if content_type is not None:  # 如果存在content_type 则组装到header中
            if 'charset' not in content_type:  # 如果没传默认字符集 才添加charset为utf-8
                content_type = content_type + ';charset=UTF-8'
            header['Content-Type'] = content_type
        if headers is not None:
            header.update(headers)
        r_dict = {
            'headers': header,
            'verify': False,
            'timeout': timeout
        }
        r_dict.update(kwargs)

        # 根据method判断调用哪个方法
        # log.info("开始匹配request方法：\n\t请求方式为：{}\n\turl:{}\n\tdata:{}\n\tdict:{}".format(method, url, data, r_dict))
        log.info("开始匹配request方法，请求方式为：{}".format(method))
        if method == 'get':
            log.info('method 匹配=get')
            return self.__get_(url=url, param=data, **r_dict)
        elif method == 'post':
            log.info('method 匹配=post')
            return self.__post_(url=url, data=data, **r_dict)
        elif method == 'delete':
            log.info('method 匹配=delete')
            return self.__delete_(url=url, data=data, **r_dict)
        elif method == 'put':
            log.info('method 匹配=put')
            return self.__put_(url=url, data=data, **r_dict)
        else:
            log.info('method 匹配失败,执行 requests.request(method=method, url=url, data=data, **r_dict) 方案,结果未知')
            return self.__request_(method=method, url=url, data=data, **r_dict)

    def __get_(self, url, param, **kwargs):
        log.info("开始执行request方法：\n\tget url:{}\n\tparam:{}\n\tdict:{}".format(url, param, kwargs))
        try:
            res = requests.get(url=url, params=param, **kwargs)
        except Exception as msg:
            log.error('request get请求异常：{}'.format(msg))
            return False
        else:
            log.info('res')
            return res if self.__response_check(res) else False

    def __post_(self, url, data, **kwargs):
        log.info("开始执行request方法：\n\tpost url:{}\n\tdata:{}\n\tkwargs:{}".format(url, data, kwargs))
        res = False
        try:
            if 'Content-Type' in kwargs['headers'].keys():
                # log.debug("\n\t |\n\t if 'Content-Type' in kwargs['headers'].keys(): |\n\t")
                if 'json' in kwargs['headers']['Content-Type'] and data is not None:
                    # log.debug("\n\t |\n\t if 'json' in kwargs['headers']['Content-Type'] and data is not None: |\n\t")
                    res = requests.post(url=url, json=data, **kwargs)
            else:
                res = requests.post(url=url, data=data, **kwargs)
        except Exception as msg:
            log.error('request post请求异常：{}'.format(msg))
            return False
        else:
            return res if self.__response_check(res) else False

    def __delete_(self, url, data, **kwargs):
        log.info("开始执行request方法：\n\tdelete url:{}\n\tdata:{}\n\tkwargs:{}".format(url, data, kwargs))
        try:
            res = requests.delete(url=url, data=data, **kwargs)
        except Exception as msg:
            log.error('request delete请求异常：{}'.format(msg))
            return False
        else:
            return res if self.__response_check(res) else False

    def __put_(self, url, data, **kwargs):
        log.info("开始执行request方法：\n\tput url:{}\n\tdata:{}\n\tkwargs:{}".format(url, data, kwargs))
        try:
            res = requests.put(url=url, data=data, **kwargs)
        except Exception as msg:
            log.error('request put请求异常：{}'.format(msg))
            return False
        else:
            return res if self.__response_check(res) else False

    def __request_(self, method, url, data, **kwargs):
        log.info("开始执行 requests.{}方法：\n\turl:{}\n\tdata:{}\n\tkwargs:{}".format(method, url, data, kwargs))
        try:
            res = requests.request(method=method, url=url, data=data, **kwargs)
        except Exception as msg:
            log.error('request {} 请求异常：{}'.format(method, msg))
            return False
        else:
            return res if self.__response_check(res) else False

    # 入参数据校验
    def __data_check(self, molds):
        for key, value in molds.items():
            if key == 'method':
                log.info('开始校验 method:{}'.format(value))
                if value not in ['get', 'post', 'put', 'delete']:
                    log.warning("请求方法：{},不在预处理['get', 'post', 'put', 'delete']列表中,requests方法执行后可能报错!!!".format(value))
            if key == 'url':
                log.info('开始校验 url [ base_url={},api={} ]'.format(value[0], value[1]))
                if value[1] == '':
                    continue
                elif re.findall('//', value[1]):
                    log.error('api 格式错误,不应该存在 //')
                    return True
                if re.search("/$", value[0]):
                    log.debug('base_url 末尾匹配到/')
                    if re.match('/', value[1]):
                        log.debug('api 开头匹配到/')
                        log.error('组成的url 格式错误, base_url与api组合后,存在 //')
                        return True
                elif not re.match('/', value[1]):
                    log.error('base_url末尾无/, api:{}格式错误,未以/开头，无法拼接'.format(value[1]))
                    return True
            if key == 'content_type':
                log.info('开始校验 content_type:{}'.format(value))
                if value is None:
                    continue
                if value == '':
                    log.warning('content_type 为 "" ,可能会引发错误')
                else:
                    value = value.split(';')[0] if re.search('charset', value) else value
                    if value not in self.content_type_list:
                        log.error('content_type:{} 不在已知道列表,当前程序无法解析!!!'.format(value))
                        return True
        log.info('入参数据校验完成')
        return False

    # response返回数据校验
    @staticmethod
    def __response_check(res):
        log.info('request请求结束, response_check开始对response做校验')
        try:
            log.info('response返回数据正确:\n\tstatus_code:{}, content 为:{}'.format(
                res.status_code, res.content))
        except AttributeError as msg:
            log.error('response返回异常,返回数据无content属性:{}'.format(msg))
            return False
        except Exception as msg:
            log.error('response返回异常：{}'.format(msg))
            return False
        else:
            return True


requestWyx = RequestWyx()
if __name__ == '__main__':
    wyx = RequestWyx()
    # url = projectConf.base_url
    res_ = wyx.request_wyx(method='get', api='')
    log.debug(res_)
