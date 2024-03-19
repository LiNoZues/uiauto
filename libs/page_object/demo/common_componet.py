"""
# File       : common_componet.py
# Time       ：2024/2/28 18:00
# Author     ：
# email      ：
# Description：
"""
from libs.page_object.element import Elements, Element
from libs.page_object.driver import PageDriver
from libs.util_back.pytest_utils import *
from libs.util_back.exception import *


class BottomNavigation(PageDriver):
    if PageDriver.env != 'ios':
        navigation = Elements(describe='底部导航栏', id_='container')
        home = Element(describe='首页', id_='container', index=0)
        trends = Element(describe='动态', id_='container', index=1)
        release = Element(describe='发布', id_='container', index=2)
        vip = Element(describe='会员购', id_='container', index=3)
        user = Element(describe='我的', id_='container', index=3)
    else:
        pass
