"""
# File       : decorate.py
# Time       ：2022/5/23 11:14 AM
# Author     ：A_zz
# email      ：chenzhe12320@163.com
# Description：
"""
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.common.exceptions import TimeoutException

from gstore import GSTORE
from loguru import logger as log
from libs.page_object.demo.main_page.bus import MainPageBus
from functools import wraps
import traceback


def back_to_main(package: str):
    """
    回到主页
    :param package:
    :return:
    """
    main_bus = MainPageBus()
    count = 0
    while 1:
        count += 1
        try:
            main_bus.is_main_page()
        except Exception:
            main_bus.page.press_keycode(AndroidKey.BACK)
            if main_bus.page.current_package != package or count > 8:
                GSTORE['driver'].start_activity()
                #app_init()
                break
        else:
            break


def recover_page(tab_name: str):
    """
    恢复初始页面
    :param tab_name:需要恢复到指定页面
    :return:
    """
    log.error(traceback.format_exc())
    log.info('开始恢复初始状态')
    main_bus = MainPageBus()
    package = main_bus.page.caps.get('appPackage', GSTORE['package_id'].replace('/',''))
    if main_bus.page.current_package != package:
        GSTORE['driver'].start_activity()
        #app_init()
    back_to_main(package)
    if tab_name:
        match tab_name:
            case '动态':
                # 进入动态页面
                pass
            case _:
                pass


"""
fail_to_main 装饰器
tab_name表示（从主页）进入到某个界面
tab_name 配合 retry使用可以实现如：恢复初始状态后，先进入搜索界面 ，再重跑进入某个股票的函数
retry：不配合tab_name的话，都设置成False
teardown 不用重跑，retry设置为False
setup -> 从A 进入 B 那么 对应的teardown只做从 B 返回 A 
"""


def fail_to_main(tab_name=None, cls_func=True, retry=False):
    """
    失败恢复到主界面
    :param retry: 失败重新执行  True 重新执行，False 抛出异常
    :param cls_func: True: Test 类里面的setup、teardown , False 普通函数
    :param tab_name: 初始页面为 关注 or 市场 or 搜索等等
    :return:
    """

    def outer(func):
        @wraps(func)
        def inner_self(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                recover_page(tab_name)
                if retry:
                    return func(self, *args, **kwargs)
                else:
                    raise e

        @wraps(func)
        def inner_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                recover_page(tab_name)
                if retry:
                    return func(*args, **kwargs)
                else:
                    raise e

        return inner_self if cls_func else inner_func

    return outer
