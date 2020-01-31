#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
"""
添加实体功能测试
----------------------------
正常添加
与已存在的中文名重复
与已存在的英文名重复
中文名称超过64字
英文名称超过64字
英文名称输入非法字符（规定只能是字母和数字）
缺少必要参数
完全相同的参数重复提交
并发提交密等测试(？)
"""

import allure
import pytest

from common.utils.assert_wyx import Assert
from common.common.requests_wyx import requestWyx
from common.common.logger_wyx import LoggerWyx
log = LoggerWyx('zstp').get_logger()


@allure.epic('知识图谱模块')
@allure.feature('添加目标表-实体')
class TestAddST:

    @allure.story('正向用例')
    @allure.title('正常添加(基础功能验证)')
    @allure.severity('blocker')
    @pytest.mark.p0
    @pytest.mark.parametrize('data_generation', [[['实体', 'entity'], 's']], indirect=True)
    @pytest.mark.parametrize('element_type', ['entity'])
    def test_add_st_0000(self, element_type,  data_generation):
        """
        正常添加
        # 校验包括 状态码校验 返回的message信息校验  数据库入库校验 涉及3个数据库表-要校验每个表的内容是否正确
        """
        ticks, label_cn, label_en = data_generation
        api = '/target_tables'
        param = {'isFrontend': True}
        data = {
            "data": {
                "elementType": element_type,
                "labelCn": label_cn,
                "labelEn": label_en,
                "isCalc": False,
                "isInited": False,
                "frontendEntityId": ticks,
                "positionX": 380,
                "positionY": 320
            }
        }
        print(data)
        log.debug('\n\t\n\tres:{}\n\t\n\t'.format(data))
        content_type = 'application/json'
        res = requestWyx.request_wyx('post', api=api, data=data, content_type=content_type, params=param)
        a = Assert(res)
        log.debug('\n\t\n\tres:{}\n\t\n\t'.format(res.text))
        a.assert_states_code()
        a.assert_content_type()


    @allure.story('反向用例')
    @allure.title('添加实体(中文名称重复添加)')
    @pytest.mark.parametrize('data_generation', [[['实体', 'entity1'], 's']], indirect=True)
    @pytest.mark.parametrize('element_type', ['entity'])
    def test_add_st_0100(self, element_type, data_generation):
        ticks, label_cn, label_en = data_generation
        api = '/target_tables'
        param = {'isFrontend': True}
        data = {
            "data": {
                "elementType": element_type,
                "labelCn": label_cn,
                "labelEn": label_en,
                "isCalc": False,
                "isInited": False,
                "frontendEntityId": ticks,
                "positionX": 380,
                "positionY": 320
            }
        }
        print(data)
        log.debug('\n\t\n\tres:{}\n\t\n\t'.format(data))
        content_type = 'application/json'
        # res = requestWyx.request_wyx('post', api=api, data=data, content_type=content_type, params=param)
        # 校验包括 状态码校验 返回的message信息校验  数据库入库校验 涉及3个数据库表-要校验每个表的内容是否正确

            # log.debug('\n\t\n\tres:{}\n\t\n\t'.format(res.text))
            # a = Assert(res)
            # a.assert_states_code()
            # a.assert_content_type('aaa')


            # 设置测试用例状态(jira)


    @allure.story('反向用例')
    @allure.title('添加实体(英文名称重复添加)')
    @pytest.mark.parametrize('data_generation', [[['实体1', 'entity'], 's']], indirect=True)
    @pytest.mark.parametrize('element_type', ['entity'])
    def test_add_st_0200(self, element_type, data_generation):
        ticks, label_cn, label_en = data_generation
        api = '/target_tables'
        param = {'isFrontend': True}
        data = {
            "data": {
                "elementType": element_type,
                "labelCn": label_cn,
                "labelEn": label_en,
                "isCalc": False,
                "isInited": False,
                "frontendEntityId": ticks,
                "positionX": 380,
                "positionY": 320
            }
        }
        # print(data)
        log.debug('\n\t\n\tres:{}\n\t\n\t'.format(data))
        content_type = 'application/json'
        # res = requestWyx.request_wyx('post', api=api, data=data, content_type=content_type, params=param)
        # 校验包括 状态码校验 返回的message信息校验  数据库入库校验 涉及3个数据库表-要校验每个表的内容是否正确
        # 可以总结部分功能校验 包括 状态码校验
        # if res:
        #     log.debug('\n\t\n\tres:{}\n\t\n\t'.format(res.text))
