#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
import os
import json
from configs.config_wyx import baseConf
from common.common.logger_wyx import log
"""
封装一些公共函数
---------------------------
当前已有功能函数
get_abspath：获取绝对路径 参数 relative_path  传入相对路径，返回绝对路径
is_json ：判断是否为标准json格式 参数 json_ , flag json_为待校验字符串，flag标识 是串儿还是文件 默认为str 0表示文件
has_key_get_value: 返回json串儿中是否有某个key 以及 该key的值（无key时值为None）
get_element_list: 获取字典列表中某元素的value组成的list  如：mysql查询结果字典列表
---------------------------
当前已有功能类及其功能函数
FilesOps 对路径下文件的操作，参数 relative_path 需传入相对路径
    count_by_types  根据文件类型统计 返回文件夹、总数、后缀类型 对应数量的字典
    count_all 只统计路径下的总文件数量  返回数字(不区分文件夹/文件)
    size_all 统计路径下每个文件 及 总文件的大小 返回字典（不包含文件夹及文件夹下的文件）
    sort_by_time 按照最后修改时间对目录下的文件进行排序并返回排序后列表（（不包含文件夹及文件夹下的文件）
    sort_by_size 按照文件大小排序 并返回排序后的列表
    clear_files 清理文件的方法
DictOPS 封装对json串儿的一些操作, 参数 json_str , json_file 可以传入json串儿 默认为None
"""


# 获取全路径的方法
def get_abspath(relative_path):
    """
    :param relative_path:
    :return: str  全路径
    """
    base_path = baseConf.base_path
    log.info('开始拼接路径base_path={},relative_path = {}'.format(base_path, relative_path))
    abs_path = os.path.join(base_path, relative_path)
    log.info('路径拼接完成 abs_path = {}'.format(abs_path))
    return abs_path


# 对文件的操作封装
class FilesOps:
    def __init__(self, relative_path):
        """
        :param relative_path: 相对路径
        """
        self.__path = get_abspath(relative_path)
        try:
            self.all_files = os.listdir(self.__path)
            log.debug('路径下的文件列表：{}'.format(self.all_files))
        except NotADirectoryError as msg:
            log.error('传入的路径不是文件夹：{}'.format(msg))
            raise
        except Exception as msg:
            log.error('遇到不可控错误：{}'.format(msg))
            raise

    def count_by_types(self):
        """
        # 统计路径下文件类型 及 数目   包括总数
        :return: dict
        """
        type_dict = dict()
        for each_file in self.all_files:
            # 如果说我们的each_file是文件夹
            if os.path.isdir(each_file):
                type_dict.setdefault("folders", 0)
                type_dict["folders"] += 1
            else:
                # 如果不是文件夹，而是文件，统计我们的文件
                ext = os.path.splitext(each_file)[1]  # 获取到文件的后缀
                type_dict.setdefault(ext, 0)
                type_dict.setdefault('files', 0)
                type_dict[ext] += 1
                type_dict['files'] += 1
            type_dict.setdefault('all', 0)
            type_dict['all'] += 1
        log.info('统计完毕，该路径下文件数目为：{}'.format(type_dict))
        return type_dict

    def count_all(self):
        """
        # 统计路径下文件类型 及 数目   包括总数
        :return: 数字
        """
        count_all = len(self.all_files)
        log.info('统计完毕，该路径下文件总数为：{}'.format(count_all))
        return count_all

    def size_all(self):
        """
        # 计算当前文件夹下面所有文件的大小
        :return: dict
        """
        size_dict = dict()
        for each_file in self.all_files:
            # 判断我们的这个each_file是否是文件 (如果是文件夹 则不统计）
            if os.path.isfile(each_file):
                file_size = os.path.getsize(each_file)
                size_dict.setdefault(each_file, 0)
                size_dict.setdefault('all', 0)
                size_dict[each_file] = file_size
                size_dict['all'] += file_size
        log.info('统计完毕，该路径下文件大小为：{}'.format(size_dict))
        return size_dict

    def sort_by_time(self, key='asc'):
        """
        # 将文件根据修改时间排序  默认升序
        :param key: 'asc','desc'
        :return: list
        """
        sort_time_files = sorted(self.all_files, key=lambda file: os.path.getmtime(os.path.join(self.__path, file))
                                 if not os.path.isdir(os.path.join(self.__path, file)) else 0)
        if key == 'asc':
            pass
        elif key == 'desc':
            sort_time_files.reverse()
        else:
            log.warning('传入的key值{}不在[asc, desc]中，执行默认 asc 升序排序'.format(key))
        log.info('{}排序完毕，该路径下按时间升序排序后的文件为：{}'.format(key, sort_time_files))
        return sort_time_files

    def sort_by_size(self, key='asc'):
        """
        # 将文件根据列表大小排序 默认升序
        :param key: 'asc','desc'
        :return: list
        """
        sort_size_files = sorted(self.all_files, key=lambda file: os.path.getsize(os.path.join(self.__path, file))
                                 if not os.path.isdir(os.path.join(self.__path, file)) else 0)
        if key == 'asc':
            pass
        elif key == 'desc':
            sort_size_files.reverse()
        else:
            log.warning('传入的key值{}不在[asc, desc]中，执行默认 asc 升序排序'.format(key))
        log.info('{}排序完毕，该路径{}下按大小升序排序后的文件为：{}'.format(key, self.__path, sort_size_files))
        return sort_size_files

    # 文件清理
    def clear_files(self, num, key='time'):
        """
        # 清理文件夹中的文件
        :param num: 保留的文件数量
        :param key: 支持按时间大小升序删除time  和  按文件大小升序删除 size , 默认按时间大小 从时间小的开始删除
        :return:无
        """
        key = key.lower()
        self.all_files = [file for file in self.all_files if not os.path.isdir(os.path.join(self.__path, file))]
        len_list = len(self.all_files)
        log.debug('总数:{}，保留:{}, 路径：{}'.format(len_list, num, self.__path))
        if num >= len_list:
            log.warning('未执行清理，该路径下剩余文件数{}小于待保留文件数{}，请关注保留数据是否设置正确！！！'.
                        format(len_list, num))
        elif key not in ['time', 'size']:
            log.warning('未执行清理，key{}错误，不在(time/size)范围内，请关注key传参是否设置正确！！！'.format(key))
        else:
            log.info('-----开始执行清理，该路径下待清理文件数{}'.format(len_list-num))
            if key == 'time':
                self.all_files = self.sort_by_time()
                for i in range(0, len_list-num):
                    log.debug('开始删除第{}个文件:{}'.format(i+1, self.all_files[0]))
                    os.remove(os.path.join(self.__path, self.all_files[0]))
                    del self.all_files[0]
            elif key == 'size':
                self.all_files = self.sort_by_size()
                for i in range(len_list - num):
                    log.debug('开始删除第{}个文件:{}'.format(i, self.all_files[0]))
                    os.remove(os.path.join(self.__path, self.all_files[0]))
                    del self.all_files[i]
            log.info('-----清理完毕-----------------------')


# 判断字符串儿是否为合法的json串儿
def is_json(json_, flag=1):
    """
    :param json_:
    :param flag: 默认为1， 1 /其他数字代表为str  0代表为file
    :return: 是否为json  bool
    """
    if flag:  # 如果为str
        try:
            json.loads(json_)
        except Exception:
            return False
    else:  # 为file
        try:
            json.load(json_)
        except Exception:
            return False
    return True


# 判断dict字典串儿是否存在 某个key 并返回对应值
def has_key_get_value(str_, key, loop=0, condition=None):
    """
    :param str_: 待查找的json串儿(dict)
    :param key: 待查找的key值
    :param loop: 默认为0，只判断第一层的数据，如果为其他值，则循环判断最多loop次数或查找到符合条件的key
    :param condition: 默认没有条件， 此参数适用于当多个子串中都包含某个key时，使用同级别子串儿来判断当前key是否满足条件
                    参数规范： {key1:value1, key2:value2}
    :return:list[true/false key对应的value值/None]
    """
    result = [False, None]
    if loop:  # 传进来的串儿可能是 str、int、dict、list  int和str可以忽略不进行拆分 continue
        if type(str_) == dict:  # 当当前字符串为字典时的判断方法
            if key in str_:  # 如果已经查到了，则直接返回True 否则进入循环哇~
                result = [True, str_[key]]
                if condition is not None:  # 如果定位条件不为空，则校验条件通过返回true 否则返回false
                    for k, v in condition.items():
                        if k in str_ and str_[k] == v:
                            continue
                        else:
                            result = [False, None]
                            break
                return result
            else:  # 如果key没找到，就继续判断
                for new_str in str_.values():
                    if type(new_str) in (dict, list):
                        result = has_key_get_value(str_=new_str, key=key, loop=loop-1, condition=condition)
                        if result[0]:
                            return result
                    else:
                        continue
        elif type(str_) == list:  # 当前字符串为列表时的判断方法
            for new_str in str_:
                if type(new_str) in (dict, list):
                    result = has_key_get_value(str_=new_str, key=key, loop=loop - 1, condition=condition)
                    if result[0]:
                        return result
                else:
                    continue
    else:
        # 传过来的可能是list 或者 dict 到这里肯定是最后一次了 因为loop已经是0了  不需要考虑更深了
        # 如果判断到满足条件，则不再继续了，开始返回 ， 否则就看循环的情况呗~
        if key in str_ and type(str_) == dict:
            result = [True, str_[key]]
            if condition is not None:
                for k, v in condition.items():
                    if k in str_ and str_[k] == v:
                        continue
                    else:
                        result = [False, None]
                        break
    return result


# 获取字典列表中某元素的value组成的list  如：mysql查询结果字典列表
def get_element_list(data_list, element_key):
    element_list = []
    for data in data_list:
        element_list.append(data[element_key])
    return element_list


# 对字典/映射的操作
class JsonOps:
    def __init__(self, str_=None, json_file=None):
        """
        初始化  两个同时只允许存在一种！！
        :param str_: 传入json串儿
        :param json_file: 传入json文件地址即可？
        """
        if str_ is not None and json_file is None:
            self.str_ = str_
        elif str_ is None and json_file is not None:
            self.str_ = json_file
        elif str_ is None and json_file is None:
            raise AttributeError('str_ 和 json_file 不允许同时为None')
        else:
            raise AttributeError('str_ 和 json_file 不允许同时存在')
        if is_json(self.str_):  # 如果传来的是标准json串儿格式，则需要解码为dict，再操作
            self.str_ = json.loads(self.str_)

    # 判断json串儿中是否有某个key值
    def is_has_key(self, str_=None, key='message', loop=0, condition=None):
        """
        :param str_: 默认值None时取值self.str_， 如果需要查找其他key 则需传入
        :param key: 默认 message， 如果需要查找其他key 则需传入
        :param loop: 默认为0，只判断第一层的数据，如果为其他值，则循环判断最多loop次数或查找到符合条件的key
        :param condition: 默认没有条件， 此参数适用于当多个子串中都包含某个key时，使用同级别子串儿来判断当前key是否满足条件
                        参数规范： {key1:value1, key2:value2}
        :return:true/false
        """
        str_ = self.str_ if str_ is None else str_
        result = has_key_get_value(str_=str_, key=key, loop=loop, condition=condition)[0]
        return result

    # 返回json串儿中是否有某个key对应的value值
    def get_json_value(self, str_=None, key='message', loop=0, condition=None):
        """
        :param str_: 默认值None时取值self.str_， 如果需要查找其他key 则需传入
        :param key: 默认 message， 如果需要查找其他key 则需传入
        :param loop: 默认为0，只判断第一层的数据，如果为其他值，则循环判断最多loop次数或查找到符合条件的key
        :param condition: 默认没有条件， 此参数适用于当多个子串中都包含某个key时，使用同级别子串儿来判断当前key是否满足条件
                        参数规范： {key1:value1, key2:value2}
        :return: key对应的value值
        """
        str_ = self.str_ if str_ is None else str_
        result = has_key_get_value(str_=str_, key=key, loop=loop, condition=condition)[1]
        return result


if __name__ == '__main__':
    j_str = {

    }
    jops = JsonOps()

    # api = 'target_tables'
    # uri = get_abspath(api)
    # print(uri)

    # list11 = [i for i in range(0, 35)]
    # log.debug('[i for i in range(0, 35)] :{}'.format(list11))
    # relapath = r'common/requests_wyx.py'
    # print(get_abspath(relapath))
    # # log_path = r'D:\code\pytest_wyx\logs'
    # log_path = os.curdir
    # __fops = FilesOps(log_path)
    # print(__fops.count_all())
    # print('大小'.center(20, '-'))
    # for size in __fops.size_all().items():
    #     print(size[0], size[1])
    # print('数目'.center(20, '-'))
    # for count in __fops.count_by_types().items():
    #     print(count[0], count[1])
    # print('排序 时间'.center(20, '-'))
    # for each in __fops.sort_by_time():
    #     print(each)
    # print('排序2 全部'.center(20, '-'))
    # for each in __fops.all_files:
    #     print(each)
    # print('排序3 大小'.center(20, '-'))
    # for each in __fops.sort_by_size():
    #     print(each)
    # __fops.clear_files(num=8)
    # print('排序4 全部'.center(20, '-'))
    # for each in __fops.all_files:
    #     print(each)
