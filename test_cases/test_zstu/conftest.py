#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx

import re
import time
import pytest

from common.common.logger_wyx import LoggerWyx
log = LoggerWyx('zstp').get_logger()


@pytest.fixture(scope='session')
def log():
    yield log

@pytest.fixture(scope='function')
def ticks_generation_f():
    ticks = re.sub(r'\.', '', str(time.time()))[0:13]
    return ticks


@pytest.fixture(scope='class')
def ticks_generation_c():
    ticks = re.sub(r'\.', '', str(time.time()))[0:13]
    return ticks


@pytest.fixture(scope='module')
def ticks_generation_m():
    ticks = re.sub(r'\.', '', str(time.time()))[0:13]
    return ticks


@pytest.fixture(scope='session')
def ticks_generation_s():
    ticks = re.sub(r'\.', '', str(time.time()))[0:13]
    return ticks


@pytest.fixture(scope='function')
def data_generation(request, ticks_generation_f, ticks_generation_c, ticks_generation_m, ticks_generation_s):
    """
    # 创建测试数据，timestamp为唯一标识
    param request: list
        ticks_type：str 支持传入f/c/m/s f=function c=class m=module s=session
        base_name: list 或者 str单个参数的支持写法如下
        1- [['base_name','ticks_type']]  中英文名字相同
        2- [['base_name_cn, base_name_en','ticks_type']] 中英文名字不同
    return: 多个参数     ---> ticks, label_cn, label_en
    """
    log.info('data_generation 数据已接收~ request为:{}'.format(request.param))
    base_name = request.param[0]
    ticks_type = request.param[1]
    log.info('开始校验传入参数是否符合需求~ ')
    if type(ticks_type) == str and type(base_name) in (list, str):  # 关于两个参数数据类型的校验
        if ticks_type not in ('f', 'c', 'm', 's'):  # ticks_type 参数需要满足条件
            msg = 'data_generation 生成失败，ticks_type:{}的传入类型不在f/c/m/s中!!!!!!!'.format(ticks_type)
            log.error(msg)
            raise TypeError(msg)
        elif type(base_name) == list:
            if len(base_name) == 2:
                if not type(base_name[0]) == str:
                    msg = 'data_generation 生成失败，base_name_list 的第 1 个参数:{}的传入类型不是str中!!!!!!!'.format(base_name[0])
                    log.error(msg)
                    raise TypeError(msg)
                if not type(base_name[0]) == str:
                    msg = 'data_generation 生成失败，base_name_list 的第 2 个参数:{}的传入类型不是str中!!!!!!!'.format(base_name[1])
                    log.error(msg)
                    raise TypeError(msg)
            else:
                msg = 'data_generation 生成失败，base_name_list 长度为{}不等于 2  !!!!!!!'.format(len(base_name))
                log.error(msg)
                raise TypeError(msg)
        log.info('数据校验通过，开始生成数据，ticks_type={},base_name_type ={},base_name:{}'.format(ticks_type, type(base_name), base_name))
        ticks = None
        if ticks_type == 'f':
            ticks = ticks_generation_f
        elif ticks_type == 'c':
            ticks = ticks_generation_c
        elif ticks_type == 'm':
            ticks = ticks_generation_m
        elif ticks_type == 's':
            ticks = ticks_generation_s
        if type(base_name) == str:  # 当base_name为一个字符串时，默认中英文名字相同
            label_cn = label_en = base_name + ticks
        else:
            # print('ticks==', ticks, type(ticks))
            label_cn = base_name[0] + ticks
            label_en = base_name[1] + ticks
        log.info('data_generation 数据生成成功，返回数据：{}'.format(ticks, label_cn, label_en))
        return ticks, label_cn, label_en
    else:
        msg = 'data_generation 生成失败，传入参数的数据类型不符合需求！！！！'
        log.error(msg)
        raise TypeError(msg)


@pytest.fixture()
def mbb_add(request):
    print(request)
