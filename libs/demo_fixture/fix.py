"""
# File       : fix.py
# Time       ：2024/3/5 15:53
# Author     ：
# email      ：
# Description：
"""
from libs.util_back.decorate import fail_to_main
from libs.page_object.demo.main_page.bus import MainPageBus
from libs.page_object.demo.search_page.bus import SearchPageBus
from loguru import logger as log


@fail_to_main(cls_func=False)
def main_enter_search_setup() -> SearchPageBus:
    """
    主页进搜索页
    """
    search_bus = MainPageBus().turn_to_search()
    return search_bus


@fail_to_main(cls_func=False)
def main_enter_search_teardown(search_bus: SearchPageBus):
    """
    从搜索页回到主界面
    :param search_bus:
    :return:
    """
    log.info('从搜索页回到主界面')
    search_bus.search_back_to_main()
