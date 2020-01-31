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
import sys

import pytest

from common.utils.assert_wyx import Assert
from common.common.logger_wyx import LoggerWyx
from common.utils.base_api_wyx import *
log = LoggerWyx('zstp').get_logger()


@allure.epic('知识图谱模块')
@allure.feature('查询目标表')
class TestSelectMbb:

    @allure.story('正向用例')
    @allure.title('查询所有目标表')
    @allure.severity('blocker')
    @pytest.mark.p0
    def test_select_mbb_0000(self):
        """
        正常添加
        # 校验包括 状态码校验 返回的message信息校验  数据库入库校验 涉及3个数据库表-要校验每个表的内容是否正确
        """
        res = select_mbb()
        a = Assert(res)
        log.info('\n\t{}-res:{}'.format(sys._getframe().f_code.co_name, res.json()))
        a.assert_states_code()
        a.assert_content_type()
        print(res.json())
