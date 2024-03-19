"""
# File       : conftest.py
# Time       ：2022/3/28 6:01 PM
# Author     ：A_zz
# email      ：chenzhe12320@163.com
# Description：
"""
import time

import pytest
from _pytest.nodes import Item
from gstore import GSTORE
from libs.page_object.driver import init_driver
from libs.util_back.common import read_config
from libs.util_back.logger import init_log
from libs.demo_fixture.fix import *


def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default='test', help="将命令行参数 ’--cmdopt' 添加到 pytest 配置中，传执行方式")
    parser.addoption("--caps", action="store", default='test', help="将命令行参数 ’--caps' 添加到 pytest 配置中，传设备参数")


@pytest.fixture(scope="session", autouse=True)
def main_control(request, worker_id):
    opt = request.config.getoption("--cmdopt")
    init_log()
    # 启动appium服务
    match int(opt):
        case 0:
            log.info('单发')
            caps = eval(request.config.getoption('--caps'))
            # 启动 server
            # sv = ServiceManager(caps)
            # GSTORE['server'] = sv
            # sv.start_appium_server()

            # 获取 driver
            init_driver(caps['port'], caps['desired_caps'])
        case 1:
            # test code
            log.info(f'分布式：{worker_id}')
            read_config()
            GSTORE['env'] = f'ios-{worker_id}'
            GSTORE['driver'] = worker_id
    yield
    # teardown
    GSTORE['driver'].quit()
    # sv.stop_appium_server()


@pytest.fixture()
def enter_search() -> SearchPageBus:
    search_bus = main_enter_search_setup()
    yield search_bus
    main_enter_search_teardown(search_bus)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item):
    # 获取钩子方法的调用结果
    # 3. 从钩子方法的调用结果中获取测试报告
    report = (yield).get_result()
    # """
    if report.when == 'setup' and report.failed:
        name = f'{item.name}-{report.when}失败截图'
        # GSTORE['page_driver'].save_capture(name)
        log.info(name)
    # 执行结束就截图
    elif report.when == "call":
        if report.failed:
            name = f'{item.name}-{report.when}失败截图'
            GSTORE['page_driver'].save_capture(name)
            log.info(name)
        else:
            name = f'{item.name}-用例执行成功截图'
            GSTORE['page_driver'].save_capture(name)


# 解决用例输出中文名显示为unicode编码的问题
def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    # pass
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
