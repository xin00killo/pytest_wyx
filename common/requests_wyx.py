#coding=utf-8
# __autor__='wyxces'



"""
本模块的接口规范如下：
request_wyx(self, method, api='', data=None, base_url=None, content_type=None, timeout=5, **kwargs)
method 必填,请求方法, 支持get post put delete
api 默认值'',接收 二级前缀+接口名称 , 以 '/'开头
data 默认是None  ,用于传入 get的param参数 或者 post 的 data/json 值 或者 delete的data值 等  json参数用data传入,请求头设置为"application/json"
base_url 默认值为 config文件中配置的 [HTTP].cona_url  ,选填
content_type 默认是None ,选填  不需要传utf-8
timeout 默认值为5  ,选填
header  默认是{} ,建议传入 Cookie和content-tyoe外的请求头信息

返回:
如数据校验不通过 或 请求出现错误 则返回 False , 正常请求返回 response信息  (如 方法错误,api格式不符合要求,content_tyoe 错误)
建议使用if判断后再取数
    if res:
        print(res.text)
    else:
        print('res 返回 false 用例失败')
"""

import re
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from configs.read_configini import baseConf, projectConf
from common.logger_wyx import log


class RequestWyx:
    def __init__(self):
        self.base_url = projectConf.base_url
        self.content_type_list = ["text/html", "text/plain", "text/xml", "image/gif", "image/jpeg", "image/png",
                                  "application/xhtml+xml", "application/xml", "application/atom+xml",
                                  "application/json", "application/pdf", "application/msword",
                                  "application/octet-stream", "application/x-www-form-urlencoded",
                                  "multipart/form-data"]

    def request_wyx(self, method, api='', data=None, base_url=None,
                     content_type=None, timeout=5, headers={}, **kwargs):
        log.debug('调用request_wyx方法，传入参数method-{}, api-{}, data-{}, base_url-{}, content_type-{}, '
                     'headers-{}'.format(method, api, data, base_url, content_type, headers))

        # 数据提前处理  包括大小写转换 和 base_url的确定
        method = method.lower()
        if content_type is not None:
            content_type = content_type.lower()
        if base_url is None:
            base_url = self.base_url

        # 数据校验 如果不通过，直接返回 False
        data_check_dict = {
            'method': method,
            'url': [base_url, api],
            'content_type': content_type
        }
        log.info('开始校验入参数据，待校验内容：{}'.format(data_check_dict))
        if self.data_check(data_check_dict):
            log.info('数据校验失败，返回False')
            return False

        # 参数组装 url 和 header
        url = base_url + api
        header = {'Cookie': "JSESSIONID={}".format(projectConf.get_pro_jsessionid())}
        if content_type is not None:  # 如果存在content_type 则组装到header中
            if 'charset' not in content_type:  # 如果没传默认字符集 才添加charset为utf-8
                content_type = content_type + ';charset=UTF-8'
            header['Content-Type'] = content_type
        header.update(headers)
        r_dict = {
            'headers': header,
            'verify': False,
            'timeout': timeout
        }
        r_dict.update(kwargs)

        # 根据method判断调用哪个方法
        log.info("开始匹配request方法：\n\t请求方式为：{}\n\turl:{}\n\tdata:{}\n\tdict:{}".
                    format(method, url, data, r_dict))
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
        log.info("开始执行get 方法")
        try:
            res = requests.get(url=url, params=param, **kwargs)
            if self.response_check(res):
                return res
        except BaseException as msg:
            log.error('request get请求异常：{}'.format(msg))
            raise
        return False

    def __post_(self, url, data, **kwargs):
        log.info("开始执行post 方法")
        log.debug("** keywargs:", kwargs)
        try:
            if 'Content-Type' in kwargs['headers'].keys():
                if 'json' in kwargs['headers']['Content-Type'] and data is not None:
                    data = json.dump(data)
            res = requests.post(url=url, data=data, **kwargs)
            if self.response_check(res):
                return res
        except BaseException as msg:
            log.error('request post请求异常：{}'.format(msg))
            raise
        return False

    def __delete_(self, url, data, **kwargs):
        log.info("开始执行delete 方法")
        try:
            res = requests.delete(url=url, data=data, **kwargs)
            if self.response_check(res):
                return res
        except BaseException as msg:
            log.error('request delete请求异常：{}'.format(msg))
            raise
        return False

    def __put_(self, url, data, **kwargs):
        log.info("开始执行 put 方法")
        try:
            res = requests.put(url=url, data=data, **kwargs)
            if self.response_check(res):
                return res
        except BaseException as msg:
            log.error('request put请求异常：{}'.format(msg))
            raise
        return False

    def __request_(self, method, url, data, **kwargs):
        log.info("开始执行 requests.{}方法".format(method))
        try:
            res = requests.request(method=method, url=url, data=data, **kwargs)
            if self.response_check(res):
                return res
        except BaseException as msg:
            log.error('request {} 请求异常：{}'.format(method, msg))
            raise
        return False

    # 入参数据校验
    def data_check(self, molds):
        for key, value in molds.items():

            if key == 'method':
                log.info('开始校验 method:{}'.format(value))
                if value not in ['get', 'post', 'put', 'delete']:
                    log.warning("请求方法：{},不在预处理['get', 'post', 'put', 'delete']列表中,"
                                   "requests方法执行后可能报错!!!".format(value))

            if key == 'url':
                log.info('开始校验 url: base_url={},api={}'.format(value[0], value[1]))
                if value[1] == '':
                    continue
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
                    if re.search('charset', value):
                        log.debug('charset-{}'.format(value))
                        value = value.split(';')[0]
                        log.debug('value{}'.format(value))
                    if value not in self.content_type_list:
                        log.error('content_type:{} 不在已知道列表,当前程序无法解析!!!'.format(value))
                        return True
        log.info('入参数据校验完成')
        return False

    # response返回数据校验
    def response_check(self, res):
        log.info('request请求结束,response_check开始对response做校验')
        try:
            log.info('数据请求正确response 数据为:{}'.format(res.content))
        except AttributeError as msg:
            log.error('response返回异常,返回数据无 content属性:{}'.format(msg))
            raise
        except BaseException as msg:
            log.error('response返回异常：{}'.format(msg))
            raise
        else:
            return True


requestWyx = RequestWyx()
if __name__ == '__main__':
    wyx = RequestWyx()
    # url = projectConf.base_url
    res = wyx.request_wyx(method='get', api='')