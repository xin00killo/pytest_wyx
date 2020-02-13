# pytest_wyx
练习用pytest写一套接口框架！ 加油，之后争取能部署到jenkins上去

模块冲突记录！系统初始运行存在如下顺序
1. common.utils.singleton模块不能引用其他模块 
1. configs.configini模块不能引用singleton外的其他模块（初始读取配置文件的） 
1. common.logger模块除以上两个模块外不能引用其他模块

## 环境信息
```
allure-pytest         2.8.6
allure-python-commons 2.8.6
pytest                5.3.3
PyYAML                5.3
requests              2.22.0
pytest-html           2.0.1
PyMySQL               0.9.3
DBUtils               1.3
```
## allure安装
配置allure环境变量  
1. 依赖：pytest 和 allure-pytest
1. 安装jdk，并配置java_home，cmd: java --version 验证
1. 下载allure的zip安装包，下载地址：https://github.com/allure-framework/allure2/releases/
1. 将下载包解压放到安装目录下：python\Lib\site-packages\
1. 添加allure到环境变量path（\安装路径\allure-commandline\bin）
1. cmd执行allure --version验证
## 项目架构

## 项目运行与报告生成
在pycharm-terminal控制台 或者 cmd命令窗口执行命令运行:
1. 切入到test_case目录运行项目：
    cd \pytest_wyx\test_cases
1. 执行命令运行pytest：
    pytest -s --alluredir=..\reports\allure_raw
1. 执行命令生成测试报告：
    allure generate ..\reports\allure_raw -o ..\reports\allure_html --clean
    
查看测试报告： 
1. 在/reports/html下找到index.html文件 
1. 右键open inbrowser，选择浏览器打开即可,推荐Firefox(Chorm浏览器可能会有无法显示数据的情况)

