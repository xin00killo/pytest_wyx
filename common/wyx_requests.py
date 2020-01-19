#coding=utf-8
# __autor__='wyxces'

import requests

from configs.read_configini import wyx
from common.wyx_logger import WyxLogger

class WyxRequest():
    def __init__(self):
        self.logger = WyxLogger()
        self.basic_url = wyx.base_url + wyx.url_1

    def wyx_request(self, mothod, api, param=None, data=None, basic_url= None, header=None, timeout=5, cookie=None, **kwargs):
        if basic_url is None:
            basic_url = self.basic_url
        url = basic_url + api
        r_dict = {
            'header': header,
            'verify': False,
            'timeout': timeout,
            'cookie': cookie
        }
        r_dict.update(kwargs)

        self.logger.info("开始执行request方法，请求方式为{}，url:{}，param:{},data:{}, dict:{}".
                         format(mothod, url, param, data, r_dict))
        if mothod == 'get':
            res = self.wyx_get(url=url, param= param, **r_dict)
        elif mothod == 'post':
            res = self.wyx_post(url=url, data= data, param= param, **r_dict)
        elif mothod == 'delete':
            res = self.wyx_delete(url=url, data= data, param= param, **r_dict)
        elif mothod == 'put':
            res = self.wyx_delete(url=url, data= data, **r_dict)
        return res

    def  wyx_get(self,url,param, **kwargs):
        self.logger.info("开始执行 wyx_get 方法")
        res = requests.get(url= url, params= param, **kwargs)
        return res

    def  wyx_post(self,url, data, param, **kwargs):
        self.logger.info("开始执行 wyx_post 方法")
        res = requests.post('https://www.baidu.com/')
        return res

    def  wyx_delete(self,url, **kwargs):
        self.logger.info("开始执行 wyx_delete 方法")
        res = requests.delete(url= url, **kwargs)
        return res

    def  wyx_put(self,url, **kwargs):
        self.logger.info("开始执行 wyx_put 方法")
        res = requests.put(url= url, **kwargs)
        return res