#coding=utf-8
# __autor__='wyxces'

import pytest

from common.wyx_logger import WyxLogger

logger = WyxLogger().logger

@pytest.fixture(scope='session', autouse=True)
def login():
    print('||||||wyxces conftest.py scope=session')
