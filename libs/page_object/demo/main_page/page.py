"""
# File       : page.py
# Time       ：2024/2/28 18:25
# Author     ：
# email      ：
# Description：
"""
from libs.page_object.demo.common_componet import *


class MainPage(BottomNavigation):
    """
    主界面
    """
    if PageDriver.env != 'ios':
        search_text = Element(describe='导航栏文本框', id_='search_text', timeout=6)
    else:
        search_text = Element(describe='导航栏文本框', ios_predicate='name == "搜索栏"')
