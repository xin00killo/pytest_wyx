#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx

import pytest

from common.utils.assert_wyx import Assert
from common.utils.base_api_wyx import *


@allure.epic('知识图谱模块')
@allure.feature('删除目标表-实体')
class TestAddST:

    @allure.story('删除实体')
    @allure.title('删除(未纳入计算、无映射关系等依赖的数据)')
    @allure.severity('blocker')
    @pytest.mark.p0
    def test_delete_st_0000(self):
        """
        删除(未纳入计算、无映射关系等依赖的数据
        # 校验包括 状态码校验 返回的message信息校验  数据库入库校验 涉及3个数据库表-要校验每个表的内容是否正确
        """
        frontend_entity_id = 1580390429428
        res = delete_mbb(frontend_entity_id)
        a = Assert(res)
        a.assert_states_code()
        a.assert_message_equal(exp='删除成功')
