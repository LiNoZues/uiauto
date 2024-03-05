"""
# File       : bus.py
# Time       ：2024/3/5 14:56
# Author     ：
# email      ：
# Description：
"""
import time

import allure

from .page import *


class SearchPageBus:
    def __init__(self, ):
        self.page = SearchPage()

    def search(self, text: str = '你好'):
        """
        搜索
        """
        with allure.step(f"输入搜索内容-「{text}」"):
            self.page.search_text.send_keys(text)
        with allure.step(f'点击搜索按钮'):
            self.page.search_btn.click()
        return self

    def search_back_to_main(self):
        """
        搜索页面返回首页
        """
        while self.page.back_btn.exist:
            # 需要刷新back_btn获取
            self.page.back_btn.refresh_el.click()

    def check_search_result(self, text: str):
        """
        校验搜索结果
        """
        CHECK('校验搜索后的顶部tab栏是否存在', condition=self.page.res_top_bar.exist)
        res_texts = self.page.res_desc_group.texts()
        check = False
        for item in res_texts:
            if text in item:
                check = True
                break
        CHECK(f'校验搜索后的页面视频描述存在「{text}」', condition=check)
