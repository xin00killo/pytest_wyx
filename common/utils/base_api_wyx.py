#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
import allure

from common.common.logger_wyx import log
from common.common.requests_wyx import requestWyx
from configs.config_wyx import yamlConf


@allure.step('添加目标表')
def add_mbb(data, **kwargs):
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
    log.info('add_mbb 公共函数开始执行，添加目标表')
    api = yamlConf.get_data('add_mbb')['api']
    method = yamlConf.get_data('add_mbb')['method']
    data_ = {
            "data": {
                "isCalc": False,
                "isInited": False,
                "positionX": 380,
                "positionY": 320
            }
        }.update({"data": data})
    content_type = 'application/json'
    res = requestWyx.request_wyx(method=method, api=api, data=data_, content_type=content_type, **kwargs)
    return res


@allure.step('删除目标表')
def delete_mbb(frontend_entity_id, **kwargs):
    log.info('delete_mbb 公共函数开始执行，删除目标表')
    api = yamlConf.get_data('delete_mbb')['api'].format(frontend_entity_id)
    method = yamlConf.get_data('delete_mbb')['method']
    data_ = {}
    content_type = 'application/json'
    res = requestWyx.request_wyx(method=method, api=api, data=data_, content_type=content_type, **kwargs)
    return res


@allure.step('查询目标表')
def select_mbb(**kwargs):
    log.info('select_mbb 公共函数开始执行，删除目标表')
    api = yamlConf.get_data('select_mbb')['api']
    method = yamlConf.get_data('select_mbb')['method']
    res = requestWyx.request_wyx(method=method, api=api, **kwargs)
    return res
