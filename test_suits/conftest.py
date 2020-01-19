#coding=utf-8
# __autor__='wyxces'

import pytest
@pytest.fixture(scope='session', autouse=True)
def login():
    print('||||||wyxces conftest.py scope=session')
