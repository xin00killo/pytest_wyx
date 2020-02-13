#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
import os
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from configs import global_wyx
from configs.config_wyx import emailConf, projectConf, logConf
from common.common.singleton_wyx import singleton
from common.common.logger_wyx import log


@singleton
class EmailWyx:
    def __init__(self):
        log.info('发送邮件模块初始化开始')
        self.__host = emailConf.host
        self.__port = emailConf.port
        self.__user = emailConf.user
        self.__pwd = emailConf.pwd
        self.__sender = emailConf.sender
        self.__receivers = emailConf.receivers
        self.__cc = emailConf.cc
        self.__bcc = emailConf.bcc
        self.__subject = emailConf.subject
        self.__content = emailConf.content
        self.__test_user = emailConf.test_user
        self.__on_off = emailConf.on_off
        self.__add_dist_log = emailConf.add_dist_log
        self.__msg_obj = self.__create_msg()

    # 创建消息对象根容器
    def __create_msg(self):
        log.info('初始消息对象根容器')
        msg_obj = MIMEMultipart('related')
        msg_obj['From'] = self.__sender
        msg_obj['To'] = self.__receivers
        msg_obj['Cc'] = self.__cc
        msg_obj['Bcc'] = self.__bcc
        msg_obj['Subject'] = self.__subject.format(projectConf.project_name,
                                                   time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        return msg_obj

    # 添加邮件附件
    def add_attach(self, file):
        """
        :param file: 需要传入文件的绝对路径
        """
        log.info('添加邮件附件儿：{}'.format(file))
        filename = os.path.basename(file)
        att_obj = MIMEApplication(open(file, 'rb').read())
        att_obj.add_header('Content-Disposition', 'attachment', filename=filename)
        self.__msg_obj.attach(att_obj)

    # 发送邮件的方法  在所有测试用例执行后运行
    def send_email(self):
        if not self.__on_off:  # 如果发送邮件功能配置为关闭，则不发送邮件
            log.warning('发送邮件功能已关闭，不发送邮件~~~')
            return
        else:
            log.info('邮件功能已开启，开始添加log和html~~~')
        # 默认添加log附件儿
        self.__add_log_files()
        # 添加html测试报告到邮件中
        self.__add_content()
        log.info('开始创建发送邮件对象 smtp_obj 并发送邮件~~~')
        smtp_obj = smtplib.SMTP()
        try:
            smtp_obj.connect(host=self.__host, port=self.__port)
            smtp_obj.login(user=self.__user, password=self.__pwd)
            smtp_obj.sendmail(from_addr=self.__sender,
                              to_addrs=self.__receivers.split(','),
                              msg=self.__msg_obj.as_string())
        except smtplib.SMTPException as msg:
            log.exception('发送邮件失败,SMTPException：{}'.format(msg))
        except Exception as msg:
            log.error('发送邮件失败,Exception：{}'.format(msg))
            raise
        else:
            log.info('发送邮件成功!!')
        finally:
            smtp_obj.quit()

    # 自动添加本次生成的log文件，到邮件中
    def __add_log_files(self):
        if logConf.logfile_log_on:  # 如果开启了日志则添加
            file = global_wyx.get_log_file()
            log.info('log已开启，添加log到邮件')
            self.add_attach(file)
        if self.__add_dist_log and logConf.dist_log_on:  # 如果开启了分块儿日志 并且 配置添加分块日志则添加
            log.info('dist-log已开启，添加dist-log到邮件')
            for name, file in global_wyx.get_log_dict().items():
                if name == projectConf.project_name:
                    continue
                self.add_attach(file)

    # 获取本次生成的html测试报告中的summary部分
    def __add_content(self):
        log.info('开始组装并添加report信息到邮件content')
        passed_amount = global_wyx.get_passed_amount()
        failed_amount = global_wyx.get_failed_amount()
        all_amount = passed_amount + failed_amount
        result = f'\n\t总运行用例数:{all_amount},成功:{passed_amount},失败:{failed_amount},其中失败的用例包括:\n'
        self.__content += result
        for value in global_wyx.get_run_result_dict().values():
            self.__content += value
        print(f'self.__content\n{self.__content}')
        self.__msg_obj.attach(MIMEText(self.__content, 'plain', 'utf-8'))


emailWyx = EmailWyx()


if __name__ == '__main__':
    # emailWyx.add_attach(r'D:\code\pytest_wyx\logs\wyxces_20200202132647.log')
    emailWyx.send_email()
