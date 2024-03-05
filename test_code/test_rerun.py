"""
# File       : test_rerun.py
# Time       ：2024/2/27 10:58
# Author     ：
# email      ：
# Description：
"""
from libs.util_back.pytest_utils import *
import pytest

pytest.mark = [
    pytest.mark.demo
]


class TestDemo:
    def test_search(self, enter_search):
        search = enter_search
        search.search('大G').check_search_result('大G')
