#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author  : wyx
import re
import time
from jira import JIRA

from common.common.singleton_wyx import singleton
from configs.config_wyx import jiraConf
from common.common.logger_wyx import log
from common.common.requests_wyx import RequestWyx
requestJira = RequestWyx(jiraConf.base_url)


@singleton
class JiraWyx:
    def __init__(self):
        log.info('jira模块初始化开始！！！')
        # 自定义常量
        self.RESULT_DICT = {
            'pass': 1,
            'fail': 2,
            'wip': 3,
            'blocked': 4,
            'unexecuted': -1
        }
        # 从配置文件读取
        self.__user = jiraConf.user
        self.__pwd = jiraConf.pwd
        self.__login_api = jiraConf.login_api
        self.__base_url = jiraConf.base_url
        self.__project_name = jiraConf.project_name
        self.__version_name = jiraConf.version_name
        self.__cycle_name = jiraConf.cycle_name
        # 通过函数获得
        self.jira = self.__get_jira()
        self.headers = self.__get_headers()
        self.project_id = self.__get_project_id()
        self.version_id = self.__get_version_id()
        self.cycle_id = self.__get_cycle_id()
        self.folders = self.__get_folders()
        self.case_execs = self.__get_case_execs()
        self.case_steps = self.__get_case_steps()

    def __get_jira(self):
        log.info('jira-jira初始化！！')
        myjira = JIRA(server=self.__base_url, basic_auth=(self.__user, self.__pwd))
        return myjira
    
    def close_jira(self):
        log.info('关闭jira对象！！！')
        self.jira.close()

    # post登录jira  获取jsessionid
    def __get_jsessionid(self):
        log.info('获取jsessionid')
        data = f'os_username={self.__user}&os_password={self.__pwd}&os_destination=&user_role=&atl_token=&login=Log+In'
        content_type = 'application/x-www-form-urlencoded;charset=UTF-8'
        res = requestJira.request_wyx(method='post', api=self.__login_api, data=data, content_type=content_type,
                                      allow_redirects=False)
        jsessionid = re.findall(r'(JSESSIONID.*?);', res.headers['Set-Cookie'])[0]
        return jsessionid

    # get登录jira  获取token_lin, zEncKeyFld, zEncKeyVal  --> headers
    def __get_headers(self):
        log.info('get登录jira 获取token_lin 初始化系统 --> headers')
        jsessionid = self.__get_jsessionid()
        headers = {'Cookie': jsessionid}
        res = requestJira.request_wyx(method='get', headers=headers)
        token = re.findall(r'atlassian.xsrf.token.*?;', res.headers['Set-Cookie'])[0]
        res_text = res.text
        zEncKeyFld = re.findall('zEncKeyFld = "(.*?)"', res_text)[0]
        zEncKeyVal = re.findall('zEncKeyVal = "(.*?)"', res_text)[0]
        headers = {
            'Cookie': token + jsessionid,
            zEncKeyFld: zEncKeyVal
        }
        print(self.headers)
        log.debug(f'项目 headers: {self.headers}')
        return headers

    # 获取项目id
    def __get_project_id(self):
        log.info(f'初始化项目 project_id，project_name:{self.__project_name}')
        projects = self.jira.projects()
        project_id = [project.id for project in projects if project.name == self.__project_name][0]
        log.debug(f'项目 project_id:{project_id}')
        return project_id

    # 获取版本id
    def __get_version_id(self):
        log.info(f'初始化项目 version_id，version_name:{self.__version_name}')
        versions = self.jira.project(self.project_id).versions
        version_id = [version.id for version in versions if version.name == self.__version_name][0]
        log.debug(f'项目 version_id:{version_id}')
        return version_id

    # 获取问题id
    def __get_issue_id(self, issue_key):
        log.info(f'获取issue_id，issue_key:{issue_key}')
        issue = self.jira.issue(issue_key)
        issue_id = issue.id
        log.debug(f'得到 issue_id:{issue_id}')
        return issue_id

    # 获取 cycle_id
    def __get_cycle_id(self):
        log.info(f'初始化项目 cycle_id，cycle_name:{self.__cycle_name}')
        api = "/rest/zephyr/latest/cycle"
        params = {
            'projectId': self.project_id,
            'versionId': self.version_id,
            'offset': 0,
            'expand': 'executionSummaries',
            '_': re.sub(r'\.', '', str(time.time()))[0:13]
        }
        res = requestJira.request_wyx(method='get', api=api, data=params, headers=self.headers)
        cycles = res.json()
        cycle_id = [key for key in cycles if key != 'recordsCount' and cycles[key]['name'] == self.__cycle_name][0]
        log.debug(f'项目 cycle_id:{cycle_id}')
        return cycle_id

    # 获取 folders{id,name}
    def __get_folders(self):
        log.info(f'初始化项目 folders !!!')
        api = f"/rest/zephyr/latest/cycle/{self.cycle_id}/folders"
        params = {
            'projectId': self.project_id,
            'versionId': self.version_id,
            'limit': 100,
            'offset': 0,
            '_': re.sub(r'\.', '', str(time.time()))[0:13]
        }
        res = requestJira.request_wyx(method='get', api=api, data=params, headers=self.headers)
        folders = [{'id': folder['folderId'], 'name': folder['folderName']}for folder in res.json()]
        log.debug(f'项目 folders:{folders}')
        return folders

    # 获取本轮测试中所有的可执行用例集合 case_execs
    def __get_case_execs(self):
        log.info(f'初始化项目 case_execs 可执行用例_用例id映射集合 !!!')
        api = "/rest/zephyr/latest/execution"
        case_execs = {}
        for folder in self.folders:
            params = {
                'cycleId': self.cycle_id,
                'action': 'expand',
                'projectId': self.project_id,
                'versionId': self.version_id,
                'folderId': folder['id'],
                'offset': 0,
                'expand': 'executionSummaries',
                'sorter': 'OrderId:ASC',
                '_': re.sub(r'\.', '', str(time.time()))[0:13]
            }
            res = requestJira.request_wyx(method='get', api=api, data=params, headers=self.headers)
            cur_execs = {cur_exec['issueKey']: {'folder_id': folder['id'],
                                                'exec_id': cur_exec['id'],
                                                'exec_order_id': cur_exec['orderId']}
                         for cur_exec in res.json()['executions']}
            case_execs.update(cur_execs)
        log.debug(f'项目 case_execs:{case_execs}')
        return case_execs

    # 获取本轮测试中所有的可执行用例集中步骤集合 case_steps
    def __get_case_steps(self):
        log.info(f'初始化项目 case_steps 可执行用例_步骤映射集合 !!!')
        case_steps = {}
        for issue_key in self.case_execs:
            issue_id = self.__get_issue_id(issue_key)
            api = f'/rest/zephyr/latest/teststep/{issue_id}'
            params = {'_': re.sub(r'\.', '', str(time.time()))[0:13]}
            res = requestJira.request_wyx(method='get', api=api, data=params, headers=self.headers)
            cur_steps = {step['orderId']: step['id'] for step in res.json()}
            log.debug(f'cur_steps:{cur_steps}')
            case_steps[issue_key] = cur_steps
        log.debug(f'项目 case_steps:{case_steps}')
        return case_steps

    # 获取用例-步骤的当前结果
    def __get_step_result(self, issue_key, step, log_):
        log_.info(f'获取 step_result，issue_key:{issue_key}，step:{step}')
        api = '/rest/zephyr/latest/stepResult'
        execution_id = self.case_execs[issue_key]['exec_id']
        params = {
            'executionId': execution_id,
            'expand': 'executionStatus',
            '_': re.sub(r'\.', '', str(time.time()))[0:13]
        }
        res = requestJira.request_wyx(method='get', api=api, data=params, headers=self.headers)
        step_id = self.case_steps[issue_key][step]
        step_result = [result for result in res.json() if result['stepId'] == step_id][0]
        log_.debug(f'得到 step_result，step_result:{step_result}')
        return step_result

    # 执行用例步骤-设置步骤的结果
    def exec_step(self, issue_key, step, result, log_=None):
        log_ = log if log_ is None else log_
        log_.info(f'开始执行 用例:{issue_key}，step:{step}，result{result}')
        step_result = self.__get_step_result(issue_key, step, log_)
        result_id = step_result['id']
        content_type = 'application/json'
        result.lower()
        step_result['status'] = self.RESULT_DICT[result.lower()]
        api = f'/rest/zephyr/latest/stepResult/{result_id}'
        requestJira.request_wyx(method='put', api=api, data=step_result,
                                content_type=content_type, headers=self.headers)

    # 执行用例-设置整个用例的结果
    def exec_case(self, issue_key, result, log_=None):
        log_ = log if log_ is None else log_
        log_.info(f'开始执行 用例:{issue_key}，result{result}')
        exec_id = self.case_execs[issue_key]['exec_id']
        api = f'/rest/zephyr/latest/execution/{exec_id}/execute'
        content_type = 'application/json'
        result.lower()
        result = self.RESULT_DICT[result]
        data = {"status": result, "changeAssignee": False}
        requestJira.request_wyx(method='put', api=api, data=data,
                                content_type=content_type, headers=self.headers)


jiraWyx = JiraWyx()
if __name__ == '__main__':
    issue_key_ = 'CONA-2146'
    step_id_ = 1
    # result_ = 'pass'
    result_ = 'fail'
    # jiraWyx.exec_step(issue_key_, step_id_, result_)
    jiraWyx.exec_case(issue_key_, result_)
    jiraWyx.close_jira()
