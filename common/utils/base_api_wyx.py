#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
import os
import allure
from configs.config_wyx import YamlConf
from common.common import logger_wyx
from common.common.requests_wyx import requestWyx
from common.utils.functions_wyx import get_abspath
from common.utils import mysql_datas

yaml_path = get_abspath(r'configs/api_config.yml')
apiConf = YamlConf(relative_path=yaml_path)


class BaseApiWyx:
    def __init__(self, log=None):
        self.log = log if log is not None else logger_wyx.log

    @allure.step('新增实体')
    def zstp_add_target_st(self, data, **kwargs):
        """
        :param data: dict,需包含内容{
                    # 这四项为必填
                    "elementType": element_type,
                    "labelCn": label_cn,
                    "labelEn": label_en,
                    "frontendEntityId": frontend_entity_id,
                    # 下面4个项目为选填
                    "isCalc": False,
                    "isInited": False,
                    "positionX": 380,
                    "positionY": 320
                }
        :param kwargs:
        :return:
        """
        self.log.info('zstp_add_target 公共函数开始执行，添加目标表')
        api = apiConf.get_data('zstp')['zstp_add_target']['api']
        method = apiConf.get_data('zstp')['zstp_add_target']['method']
        data_ = {
            "data": {
                "isCalc": False,
                "isInited": False,
                "positionX": 380,
                "positionY": 320
                }
            }
        data_["data"].update(data)
        content_type = 'application/json'
        res = requestWyx.request_wyx(method=method, api=api, data=data_, content_type=content_type, **kwargs)
        return res

    @allure.step('删除实体:{frontend_entity_id}')
    def zstp_delete_target(self, frontend_entity_id, **kwargs):
        self.log.info('zstp_delete_target 公共函数开始执行，删除目标表：{}'.format(frontend_entity_id))
        api = apiConf.get_data('zstp')['zstp_delete_target']['api'].format(frontend_entity_id)
        method = apiConf.get_data('zstp')['zstp_delete_target']['method']
        data_ = {}
        content_type = 'application/json'
        res = requestWyx.request_wyx(method=method, api=api, data=data_, content_type=content_type, **kwargs)
        return res

    @allure.step('查询目标表')
    def zstp_select_target(self, **kwargs):
        self.log.info('zstp_select_target 公共函数开始执行，查询知识图谱模块所有目标表')
        api = apiConf.get_data('zstp')['zstp_select_target']['api']
        method = apiConf.get_data('zstp')['zstp_select_target']['method']
        res = requestWyx.request_wyx(method=method, api=api, **kwargs)
        return res

    @allure.step('纳入计算/取消纳入计算')
    def zstp_is_calc_st(self, target_table_id, data=None, **kwargs):
        self.log.info('zstp_is_calc 公共函数开始执行，将id={}的目标表纳入计算')
        api = apiConf.get_data('zstp')['zstp_update_target']['api'].format(target_table_id)
        method = apiConf.get_data('zstp')['zstp_update_target']['method']
        # 在数据库中查询相关信息
        tb = mysql_datas.TargetTable(target_table_id, log=self.log)
        fm = mysql_datas.FrontendMapping(target_table_id=target_table_id, log=self.log)
        fpi = mysql_datas.FrontendPositionInfo(fm.frontend_entity_id)
        data_ ={
            "data": {
                "elementType": tb.element_type(),
                "labelCn": tb.label_cn(),
                "labelEn": tb.label_en(),
                "frontendEntityId": fm.frontend_entity_id(),
                "isCalc": tb.is_calc(),
                "isInited": tb.is_inited(),
                "positionX": fpi.position_x(),
                "positionY": fpi.position_y()
                }
            }
        data_ = data_ if data is None else data_.update(data)
        res = requestWyx.request_wyx(method=method, api=api, data=data_, **kwargs)
        return res

    @allure.step('上传目标表字段')
    def quick_add_target_attrs(self, **kwargs):
        self.log.info('zstp_select_target 公共函数开始执行，查询知识图谱模块所有目标表')
        api = apiConf.get_data('target')['quick_add_target_attrs']['api']
        method = apiConf.get_data('target')['quick_add_target_attrs']['method']
        content_type = 'application/octet-stream'
        res = requestWyx.request_wyx(method=method, api=api, **kwargs)
        return res