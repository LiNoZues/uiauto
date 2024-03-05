"""
# File       : pytest_utils.py
# Time       ：2022/4/1 2:46 PM
# Author     ：A_zz
# email      ：chenzhe12320@163.com
# Description： 封装了一些pytest 配合allure常用的方法
"""

import allure
from pytest_assume.plugin import assume
from gstore import GSTORE
from loguru import logger as log



def CHECK(desc: str, condition: bool, fail_skip: bool = False, fail_screenshot=True,screen_shot=False):
    """
    :param screen_shot: 检查点截图
    :param fail_screenshot: 失败截图
    :param fail_skip: 失败继续执行
    :param desc: 检查点描述
    :param condition: 检查点结果值
    :return:
    """
    if screen_shot:
        GSTORE['page_driver'].save_capture(f"{desc}-检查点截图")

    allure.attach('{}-{}'.format(
        desc,
        'PASS' if condition else 'FAIL'
    ), f'检查点：{desc}-{"PASS" if condition else "FAIL"}')
    if not condition and fail_screenshot:
        log.info('断言失败截图')
        GSTORE['page_driver'].save_capture(f"{desc}-断言失败截图")
    if fail_skip:
        # 软断言，断言失败后还能继续执行
        with assume:
            assert condition, desc
    else:
        assert condition, desc


def INFO(title: str, info: str):
    """
    添加辅助信息
    :param title:显示标题
    :param info: 显示内容
    :return:
    """
    allure.attach(info, f'INFO-{title}')


class Assert:
    @staticmethod
    def assert_equal(actual_result, except_result, description=None) -> bool:
        """
        校验相等
        :param actual_result:实际值
        :param except_result:期望值
        :param description:
        :return:
        """
        INFO(f'{description if description is not None else "条件情况"}', f"实际：{actual_result}|期望：{except_result}")
        return actual_result == except_result

    @staticmethod
    def assert_in(c1, c2, description=None) -> bool:
        """
        校验 条件1 在 条件2 中 （一般用于文本判断）
        :param c1:
        :param c2:
        :param description:
        :return:
        """
        INFO(f'{description if description is not None else "条件情况"}', f"{c1}|{c2}")
        return c1 in c2

    @staticmethod
    def assert_greater(actual_result, except_result, description=None) -> bool:
        """
        实际 大于 期望
        :param actual_result:
        :param except_result:
        :param description:
        :return:
        """
        INFO(f'{description if description is not None else "条件情况"}', f"实际：{actual_result}|期望：{except_result}")
        return actual_result > except_result

    @staticmethod
    def assert_less(actual_result, except_result, description=None) -> bool:
        """
        实际 小于 期望
        :param actual_result:
        :param except_result:
        :param description:
        :return:
        """
        INFO(f'{description if description is not None else "条件情况"}', f"实际：{actual_result}|期望：{except_result}")
        return actual_result < except_result

    @staticmethod
    def assert_dif(actual_result, except_result, description=None) -> bool:
        """
        实际 != 期望
        :param actual_result:
        :param except_result:
        :param description:
        :return:
        """
        if isinstance(actual_result, list) and isinstance(except_result, list):
            actual_result.sort()
            except_result.sort()
        INFO(f'{description if description is not None else "条件情况"}',
             f"实际：{str(actual_result)}|期望：{str(except_result)}")
        return actual_result != except_result


""" SUITE
@allure.epic(epic) # 行情
@allure.feature(feature) # 盘口
"""

""" CASE
@allure.story(story) 用户场景用例
@allure.testcase(test_case, '用例链接')
@allure.issue(issue, 'issue链接')
@allure.link(link)
@allure.title(title)
@allure.description(desc)
@allure.severity(severity)
"""
