#coding=utf-8
# __autor__='wyxces'

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from configs.read_configini import Wyx
from common.wyx_logger import WyxLogger

logger = WyxLogger().logger
wyx = Wyx()

class WyxRequest():
    def __init__(self):
        self.basic_url = wyx.base_url + wyx.url_1

    def wyx_request(self, mothod, api, param=None, data=None, basic_url=None, headers=None, timeout=5, cookies=None, **kwargs):
        # 开始拼接url
        print(basic_url)
        if basic_url is None:
            basic_url = self.basic_url
        url = basic_url + api

        #组装其它参数
        r_dict = {
            'headers': headers,
            'verify': False,
            'timeout': timeout,
            'cookies': cookies
        }
        r_dict.update(kwargs)

        #根据mothod判断调用哪个方法
        logger.info("开始判断request方法：\n\t请求方式为：{}\n\turl:{}\n\tparam:{}\n\tdata:{}\n\tdict:{}\n\t".
                         format(mothod, url, param, data, r_dict))
        if mothod == 'get':
            res = self.get(url=url, param=param, **r_dict)
        elif mothod == 'post':
            res = self.post(url=url, data=data, param=param, **r_dict)
        elif mothod == 'delete':
            res = self.delete(url=url, **r_dict)
        elif mothod == 'put':
            res = self.put(url=url, data=data, **r_dict)
        return res

    def get(self,url,param, **kwargs):
        logger.info("开始执行get 方法")
        res = requests.get(url= url, params= param, **kwargs)
        return res

    def post(self,url, data, param, **kwargs):
        logger.info("开始执行post 方法")
        res = requests.post(url=url, data=data, param=param, **kwargs)
        return res

    def delete(self,url, **kwargs):
        logger.info("开始执行delete 方法")
        res = requests.delete(url= url, **kwargs)
        return res

    def put(self,url, **kwargs):
        logger.info("开始执行 put 方法")
        res = requests.put(url= url, **kwargs)
        return res

if __name__ == '__main__':
    wyxr = WyxRequest()
    url = wyx.base_url
    res = wyxr.wyx_request(mothod='get', api='', basic_url=url)
    print(res.text)