#coding=utf-8
# __autor__='wyxces'

import threading
from functools import wraps


# 单例装饰器
def singleton(cls):
    # 创建外层函数，可以传入类
    cls._instance_lock = threading.Lock()
    _instance = {}  # 创建一个instances字典用来保存单例

    @wraps(cls)
    def getSingleton(*args, **kargs): # 创建一个内层函数来获得单例
        # 判断instances字典中是否含有单例，如果没有就创建单例并保存到instances字典中，然后返回该单例
        if cls not in _instance:
            with cls._instance_lock:  #线程锁
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return getSingleton # 返回内层函数get_instance

