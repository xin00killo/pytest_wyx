#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
import operator

import allure
import requests

from common.utils.functions_wyx import has_key_get_value


# 封装断言requests 请求 和 response方法
class Assert:
    def __init__(self, res=requests.models.Response()):
        self._res = res
        assert res, 'requests请求是失败的，直接返回了False信息！'

    # 断言状态码 默认判断200
    @allure.step('断言状态码是否为{exp}')
    def assert_states_code(self, exp=200):
        actual = self._res.status_code
        assert actual == exp, 'response状态码实际值{}与预期值{}不一致'.format(actual, exp)

    # 断言返回的headers中是否有某属性信息，默认判断'Content-Type'
    @allure.step('断言请求头信息包含的{exp}属性')
    def assert_has_header(self, exp='Content-Type'):
        actual = self._res.headers
        assert exp in actual, '返回的headers中无"{}"属性'.format(exp)

    # 断言返回Content-Type类型是否为预期类型  默认判断json
    @allure.step('断言Content-Type信息与预期{exp}是否一致')
    def assert_content_type(self, exp='application/json'):
        if 'Content-Type' in self._res.headers:
            actual = self._res.headers['Content-Type'].split(';')[0]
            assert exp in actual, '返回的Content-Type"{}"与预期"{}"不一致'.format(actual, exp)
        else:
            assert False, '返回的headers中无"Content-Type"属性'

    # 判断返回response_body内容是否包含关键字
    @allure.step('断言response_body内容是否包含预期信息')
    def assert_response_body_include(self, exp):
        actual = self._res.text
        assert exp in actual, '返回的response_body中未包含期望值"{}"'.format(exp)

    # 判断返回response_body内容是否包含关键字
    @allure.step('断言response_body内容是否与预期一致')
    def assert_response_body_equal(self, exp):
        actual = self._res.text
        assert exp == actual, '返回的response_body"{}"与期望值"{}"不一致'.format(actual, exp)

    @allure.step('断言返回的message中是否包含预期信息')
    def assert_message_include(self, exp, key='message', loop=0, condition=None):
        """
        当返回数据为json时，适用
        :param exp: 期望值
        :param key: 默认 message， 有可能字符串中message字符串不存在或叫其他名字时，传值
        :param loop: 默认为0，只判断第一层的数据，如果为其他值，则循环判断最多loop次数或查找到符合条件的key
        :param condition: 默认没有条件， 此参数适用于当多个子串中都包含某个key时，使用同级别子串儿来判断当前key是否满足条件
                        参数规范： {key1:value1, key2:value2}
        """
        actual = has_key_get_value(str_=self._res.json(), key=key, loop=loop, condition=condition)[1]
        assert exp in actual, '返回的message未包含期望值"{}"'.format(exp)

    @allure.step('断言返回的message信息与预期是否一致')
    def assert_message_equal(self, exp, key='message', loop=0, condition=None):
        """
        当返回数据为json时，适用，参数同  assert_message_include
        """
        actual = has_key_get_value(str_=self._res.json(), key=key, loop=loop, condition=condition)[1]
        assert exp == actual, '返回的message与期望值"{}"不一致'.format(exp)

    @allure.step('断言返回的{key}数据列表个数')
    def assert_data_list_len(self, exp, key='data', loop=0, condition=None):
        """
        当返回数据为json时，适用，参数同  assert_message_include
        """
        data_list = has_key_get_value(str_=self._res.json(), key=key, loop=loop, condition=condition)[1]
        actual = len(data_list)
        assert exp == actual, '返回的data列表数据个数"{}"与期望值"{}"不一致'.format(actual, exp)

    @allure.step('断言返回的{key}数据列表中{assert_value}元素的值与预期是否完全一致')
    def assert_data_list_dict_element(self, element_key, exp=None, key='data', loop=0, condition=None):
        """
        当返回数据为json 且data_list 的数据为结构详图的dict时，适用 （批量查询适用）
        :param element_key: data_list中需要校验的列表中元素的key值
                eg- 返回数据data的targetTableId/labelEn值
                {'statusCode': 200,'message': '','data': [
                                        {'targetTableId': 2,'labelEn': 'che01'},
                                        {'targetTableId': 3,'labelEn': 'ren0102'}]}
        :param exp: list 期望值
        :param key: data 或其他列表数据的key值
        :param loop: 同 assert_message_include
        :param condition: 同 assert_message_include
        :return:
        """
        data_list = has_key_get_value(str_=self._res.json(), key=key, loop=loop, condition=condition)[1]
        actual = []
        for d in data_list:
            actual.append(d[element_key])
        actual.sort(), exp.sort()
        assert (actual > exp)-(actual < exp) == 0, '返回的data列表字典元素"{}"与期望值"{}"不一致'.format(actual, exp)

    @staticmethod
    @allure.step('断言实际值列表与预期列表是否一致')
    def assert_list_equal(actual, exp):
        actual.sort()
        exp.sort()
        assert actual == exp, 'response返回的结果列表{}与预期列表{}不一致'.format(actual, exp)


# a = Assert()
