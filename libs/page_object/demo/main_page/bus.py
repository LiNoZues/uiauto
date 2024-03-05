"""
# File       : bus.py
# Time       ：2024/2/28 18:32
# Author     ：
# email      ：
# Description：
"""
from libs.page_object.demo.main_page.page import *
from libs.page_object.demo.search_page.bus import *


class MainPageBus:
    def __init__(self):
        self.page = MainPage()

    def turn_to_search(self):
        """
        搜索操作
        """
        self.page.search_text.click()
        return SearchPageBus()

    def is_main_page(self):
        """
        判断是否在首页
        """
        if self.page.home.exist:
            return self
        else:
            raise PageElementError("当前不在主界面")