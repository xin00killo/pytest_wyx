#coding=utf-8
# __autor__='wyxces'
import os
import traceback

from configs.read_configini import baseConf
from common.logger_wyx import log


# 获取全路径的方法
def get_abspath(relative_path):
    log.info('开始拼接路径 relative_path = {}'.format(relative_path))
    base_path = baseConf.get_base_path()
    abs_path = os.path.join(base_path,relative_path)
    log.info('路径拼接完成 abs_path = {}'.format(abs_path))
    return abs_path


# 对文件的操作封装
class FilesOps:
    def __init__(self, relative_path):
        self.path = get_abspath(relative_path)
        try:
            self.all_files = os.listdir(self.path)
            log.debug('路径下的文件列表：{}'.format(self.all_files))
        except NotADirectoryError as msg:
            log.error('传入的路径不是文件夹：{}'.format(msg))
            raise
        except Exception as msg:
            log.error('遇到不可控错误：{}'.format(msg))
            raise

    # 统计路径下文件类型 及 数目   包括总数
    def count_by_types(self):
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
        log.info('统计完毕，该路径{}下文件数目为：{}'.format(self.path, type_dict))
        return type_dict

        # 统计路径下文件类型 及 数目   包括总数
    def count_all(self):
        count_all = len(self.all_files)
        log.info('统计完毕，该路径{}下文件总数为：{}'.format(self.path, count_all))
        return count_all

    # 计算当前文件夹下面所有文件的大小
    def size_all(self):
        size_dict = dict()
        for each_file in self.all_files:
            # 判断我们的这个each_file是否是文件 (如果是文件夹 则不统计）
            if os.path.isfile(each_file):
                file_size = os.path.getsize(each_file)
                size_dict.setdefault(each_file, 0)
                size_dict.setdefault('all', 0)
                size_dict[each_file] = file_size
                size_dict['all'] += file_size
        log.info('统计完毕，该路径{}下文件大小为：{}'.format(self.path, size_dict))
        return size_dict

    # 将文件根据列表时间升序排序
    def asc_by_time(self):
        asc_time_files= sorted(self.all_files, key=lambda file: os.path.getmtime(os.path.join(self.path, file))
            if not os.path.isdir(os.path.join(self.path, file)) else 0)
        log.info('排序完毕，该路径{}下按时间升序排序后的文件为：{}'.format(self.path, asc_time_files))
        return asc_time_files

    # 将文件根据列表大小升序排序
    def asc_by_size(self):
        asc_size_files= sorted(self.all_files, key=lambda file: os.path.getsize(os.path.join(self.path, file))
            if not os.path.isdir(os.path.join(self.path, file)) else 0)
        log.info('排序完毕，该路径{}下按大小升序排序后的文件为：{}'.format(self.path, asc_size_files))
        return asc_size_files


    """
    # 清理文件夹中的文件  
        num:保留的文件数量 
        key:支持按时间大小升序删除time  和  按文件大小升序删除 size , 默认按时间大小 从时间小的开始删除
        list_
    """
    def clear_files(self, num, key='time'):
        key = key.lower()
        len_list = len(self.all_files)
        log.debug('总数:{}，保留:{}'.format(len_list, num))
        if num >= len_list:
            log.warning('未执行清理，该路径{}下剩余文件数{}小于待保留文件数{}，请关注保留数据是否设置正确！！！'.
                        format(self.path, len_list, num))
        elif key not in ['time', 'size']:
            log.warning('未执行清理，key{}错误，不在(time/size)范围内，请关注key传参是否设置正确！！！'.format(key))
        else:
            log.info('开始执行清理，该路径{}下待清理文件数{}'.format(self.path, len_list-num))
            if key == 'time':
                self.all_files = self.asc_by_time()
                for i in range(0, len_list-num):
                    log.debug('开始删除第{}个文件，当前文件列表为：{}'.format(i+1, self.all_files))
                    os.remove(os.path.join(self.path, self.all_files[0]))
                    del self.all_files[0]
            elif key == 'size':
                self.all_files = self.asc_by_size()
                for i in range(len_list - num):
                    log.debug('开始删除第{}个文件，当前文件列表为：{}'.format(i, self.all_files))
                    os.remove(os.path.join(self.path, self.all_files[0]))
                    del self.all_files[i]
            log.info('清理完毕，该路径{}清理后剩余文件为：{}'.format(self.path, self.all_files))


if __name__ == '__main__':
    list11 = [i for i in range(0, 35)]
    log.debug('[i for i in range(0, 35)] :{}'.format(list11))
    relapath = r'common/requests_wyx.py'
    print(get_abspath(relapath))
    # log_path = r'D:\code\pytest_wyx\logs'
    log_path = os.curdir
    __fops = FilesOps(log_path)
    print(__fops.count_all())
    print('大小'.center(20, '-'))
    for size in __fops.size_all().items():
        print(size[0], size[1])
    print('数目'.center(20, '-'))
    for count in __fops.count_by_types().items():
        print(count[0],count[1])
    print('排序 时间'.center(20, '-'))
    for each in __fops.asc_by_time():
        print(each)
    print('排序2 全部'.center(20, '-'))
    for each in __fops.all_files:
        print(each)
    print('排序3 大小'.center(20, '-'))
    for each in __fops.asc_by_size():
        print(each)
    __fops.clear_files(num=8)
    print('排序4 全部'.center(20, '-'))
    for each in __fops.all_files:
        print(each)
