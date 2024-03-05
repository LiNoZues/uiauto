"""
# File       : page.py
# Time       ：2024/3/5 14:56
# Author     ：
# email      ：
# Description：
"""

from libs.page_object.demo.common_componet import *


class SearchPage(BottomNavigation):
    """
    搜索界面
    """
    if PageDriver.env != 'ios':
        search_text = Element(describe='导航栏文本框', id_='search_src_text')
        search_btn = Element(describe='搜索按钮', id_='action_search')
        res_top_bar = Element(describe='搜索结果顶部分类栏', id_='top_appbar')
        back_btn = Element(describe='返回按钮', id_='iv_back_arrow', retry=1)
        res_desc_group = Elements(describe='搜索结果中的文本描述', id_='title')
    else:
        pass
