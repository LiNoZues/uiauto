"""
# File       : driver.py
# Time       ：2022/7/11 15:37
# Author     ：
# email      ：
# Description：
"""
import time

from appium import webdriver
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException, InvalidElementStateException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from appium.options.android import UiAutomator2Options
from gstore import GSTORE
import allure
import os
from loguru import logger as log

from libs.page_object.element import Element


class PageDriver:
    env = GSTORE['env']

    def __init__(self, driver: WebDriver = None):
        self.driver = driver if driver is not None else GSTORE['driver']
        self.caps = self.driver.caps
        self.width, self.height = self.get_x_y()

    def is_toast_exist(self, timeout=5, poll_frequency=0.1):
        """
        判断toast是否存在，是则返回True，否则返回False
        """
        try:
            toast_loc = (AppiumBy.XPATH, '//*[@class="android.widget.Toast"]')
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                ec.presence_of_element_located(toast_loc)
            )
            return True
        except TimeoutException:
            return False

    def get_toast_text(self, timeout=5, poll_frequency=0.1):
        """
        定位toast元素，获取text属性
        """

        toast_loc = (AppiumBy.XPATH, '//*[@class="android.widget.Toast"]')
        try:
            toast = WebDriverWait(self.driver, timeout, poll_frequency).until(
                ec.presence_of_element_located(toast_loc)
            )
            toast_text = toast.get_attribute('text')
        except Exception as e:
            return e
        else:
            return toast_text

    def press_keycode(self, key: int):
        """
        模拟按键点击
        :param key:
        :return:
        """
        log.info(f'模拟点击按键「{key}」')
        self.driver.press_keycode(key)

    @property
    def current_package(self) -> str:
        return self.driver.current_package

    @property
    def page_source(self) -> str:
        """
        获取页面元素
        :return:
        """
        return self.driver.page_source

    def tap(self, pos):
        """
        根据坐标点击
        暂时只支持一个一个坐标点点击
        :param pos:(x,y)
        :return:
        """
        log.info(f'点击坐标:『{pos}』')
        try:
            self.driver.tap(positions=[pos])
        except InvalidElementStateException as e:
            log.warning(e.msg)

    def screenshot(self, path) -> bool:
        """
        截图
        :param path:
        :return:
        """
        log.info(f'截图保存路径:{path}')
        return self.driver.get_screenshot_as_file(path)

    def save_capture(self, file_name):
        """
        截图保存到allure
        :param file_name: 保存的文件名
        :return:
        """
        path = os.path.join(GSTORE['SSP'], file_name + '.png')
        if self.screenshot(path):
            allure.attach.file(path, file_name, attachment_type=allure.attachment_type.PNG)
        else:
            log.warning(f'{file_name}截图保存失败')

    '''获取屏幕宽高'''

    def get_x_y(self):
        """
        :return: 宽 高
        """
        size = self.driver.get_window_size()
        w, h = size['width'], size['height']
        return w, h

    def swipe(self, start_x, start_y, end_x, end_y, duration):
        log.info(f'滑动：「({start_x},{start_y})->({end_x},{end_y})」,持续时间:{duration}')
        self.driver.swipe(int(start_x), int(start_y), int(end_x), int(end_y), duration)

    def swipe_right(self, start_x_percent=0.25, end_x_percent=0.75, start_y_percent=0.5, end_y_percent=0.5,
                    duration=800):
        """
        右滑
        :param :
        :return:
        """
        self.swipe(self.width * start_x_percent, self.height * start_y_percent, self.width * end_x_percent,
                   self.height * end_y_percent, duration=duration)

    def swipe_left(self, start_x_percent=0.75, end_x_percent=0.25, start_y_percent=0.5, end_y_percent=0.5,
                   duration=800):
        """
        左滑
        :return:
        """
        self.swipe(self.width * start_x_percent, self.height * start_y_percent, self.width * end_x_percent,
                   self.height * end_y_percent, duration=duration)

    def swipe_up(self, start_y_percent=0.6, end_y_percent=0.25, start_x_percent=0.0, end_x_percent=0.0,
                 duration=800):
        """
        上滑
        :return:
        """
        self.swipe(self.width * start_x_percent, self.height * start_y_percent, self.width * end_x_percent,
                   self.height * end_y_percent, duration=duration)

    def swipe_down(self, start_y_percent=0.25, end_y_percent=0.6, start_x_percent=0.0, end_x_percent=0.0,
                   duration=800):
        """
        下滑
        :return:
        """
        self.swipe(self.width * start_x_percent, self.height * start_y_percent, self.width * end_x_percent,
                   self.height * end_y_percent, duration=duration)

    def swipe_to_end(self, start_xp=0.5, start_yp=0.6, end_xp=0.5, end_yp=0.25, duration=800):
        while 1:
            before = self.driver.page_source
            self.swipe_up(start_x_percent=start_xp, start_y_percent=start_yp, end_x_percent=end_xp,
                          end_y_percent=end_yp, duration=duration)
            tmp = self.driver.page_source
            if tmp == before:
                break

    def press_swipe(self, start_el: Element, end_el: Element):
        """
        从长按一个元素滑到另外一个元素
        :param start_el: 起始元素
        :param end_el: 结束元素
        :return:
        """
        ActionChains(self.driver).click(start_el.web_element).move_to_element(end_el.web_element).perform()

    def scroll(self, start_el: Element, end_el: Element):
        """
        从一个元素滑到另外一个元素，直到页面自动停止  有滑动惯性
        :param start_el: 起始元素
        :param end_el: 结束元素
        :return:
        """
        log.debug(f'从元素：{start_el.desc}滑动到 元素：{end_el.desc}')
        self.driver.scroll(start_el.web_element, end_el.web_element)

    def quit(self):
        """
        退出
        :return:
        """
        log.info("关闭Driver")
        self.driver.quit()

    def start_activity(self):
        """
        启动app
        :return:
        """
        if self.caps.get('appPackage'):
            log.info(f'启动app-{self.caps["appPackage"]}')
            os.system(f'adb shell am start -W -n {self.caps["appPackage"]}/{self.caps["appActivity"]}')
            # self.driver.start_activity(self.caps['appPackage'], self.caps['appActivity'])
        else:
            #  appPackage: global.longbridge.android.debug
            #  appActivity: global.longbridge.android.LaunchActivity
            # self.driver.start_activity('global.longbridge.android.debug',
            #                            'global.longbridge.android.LaunchActivity')
            os.system(f'adb shell am start -W -n {self.caps["appPackage"]}/{self.caps["appActivity"]}')
        time.sleep(2)

    def close_app(self):
        """
        关闭app
        :return:
        :rtype:
        """
        self.driver.close_app()

    def drag(self, origin_el: Element, destination_el: Element):
        """
        元素拖拽到指定元素位置
        :param origin_el: 起始元素
        :param destination_el: 目标位置元素
        :return:
        """
        org = origin_el.web_element
        des = destination_el.web_element
        log.debug(f'元素：「{origin_el.desc}」 拖拽至 元素：「{destination_el.desc}」')
        self.driver.drag_and_drop(org, des)


def init_driver(port: int, caps: dict) -> WebDriver:
    """
    :param port: 端口
    :param caps:
    :return:
    """
    log.info(f'Appium Server Port : {port}')
    try:
        log.info(caps)
        options = UiAutomator2Options().load_capabilities(caps)
        driver = webdriver.Remote(f'http://localhost:{port}/wd/hub', options = options)
    except Exception as e:
        log.error(e)
        raise e
    driver.implicitly_wait(10)
    GSTORE['driver'] = driver
    GSTORE['page_driver'] = PageDriver(driver)
    return GSTORE['driver']

