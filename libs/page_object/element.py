import os
import time
from time import sleep

from appium.webdriver import WebElement
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait

from gstore import img_dir, GSTORE
from libs.util_back.common import get_pos_by_ocr
from libs.util_back.exception import FindElementTypesError, PageElementUnFindException, MethodNotAllowed, \
    PageElementError
from loguru import logger as log

LOCATOR_LIST = {
    # appium
    'id_': AppiumBy.ID,
    'name': AppiumBy.CLASS_NAME,
    'xpath': AppiumBy.XPATH,
    'ios_uiautomation': AppiumBy.IOS_UIAUTOMATION,
    'ios_predicate': AppiumBy.IOS_PREDICATE,
    'ios_class_chain': AppiumBy.IOS_CLASS_CHAIN,
    'android_uiautomator': AppiumBy.ANDROID_UIAUTOMATOR,
    'android_viewtag': AppiumBy.ANDROID_VIEWTAG,
    'android_data_matcher': AppiumBy.ANDROID_DATA_MATCHER,
    'android_view_matcher': AppiumBy.ANDROID_VIEW_MATCHER,
    'windows_uiautomation': AppiumBy.WINDOWS_UI_AUTOMATION,
    'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
    'image': AppiumBy.IMAGE,
    'custom': AppiumBy.CUSTOM,
    # uiautomator

}


def tip(func):
    def inner(*args, **kwargs):
        self = args[0]

        name = self.__class__.__name__
        if name == 'Elements':
            log.debug(f'获取元素集合中-{self.desc} | timeout:「{self.timeout}」 | retry: 「{self.retry}」')
        else:
            log.debug(f'获取单个元素中-{self.desc} | timeout:「{self.timeout}」 | retry: 「{self.retry}」')
        return func(*args, **kwargs)

    return inner


def not_allowed(is_set):
    """
    判断方法能不能在元素集合使用
    :param is_set: True代表是集合
    :return:
    """

    def outer(func):
        def inner(*args, **kwargs):
            self = args[0]
            if is_set:
                # 元素集合不允许

                if (self.child is not None and self.child[3]) or (self.child is None and self.is_set):
                    raise MethodNotAllowed(f"元素集合不允许使用此方法「{func.__name__}」")
            elif is_set is None:
                pass
            else:
                # 单个元素不允许
                if not self.is_set and (self.child is not None and self.child[2] is not None):
                    raise MethodNotAllowed(f"该元素不允许使用此方法「{func.__name__}」")

            return func(*args, **kwargs)

        return inner

    return outer


class Element:
    """
    Returns an element object
    """

    def __init__(self, retry: int = 2, timeout: int = 5, describe: str = "", index: int = None,
                 child: tuple = None, **kwargs):
        """
        :param is_set: 是否是元素集合 （如果有child字段，这里的is_set不生效，index有效-参考「__find_element」函数中的描述）
        :param retry: 重试定位次数
        :param timeout: 定位超时时间
        :param describe: 元素描述
        :param index: 下标 （查找元素集合）
        :param kwargs:
        :param child: 子元素定位方式
        :type child : tuple  (way,path,index) 查找子元素集合 （way=xx,path=xx,index=None,is_set=None）
                        way ：定位方式
                        path：定位路径
                        index：元素下标
        """
        self.retry = retry
        self.timeout = timeout
        self.index = index
        self.desc = describe
        self.child = child
        if not kwargs:
            raise ValueError("请指定定位方式和路径")
        if len(kwargs) > 1:
            raise ValueError("只允许单一路径定位")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST.keys():
            raise FindElementTypesError(f"暂不支持定位方式-{self.k}")
        self.el = None
        self.refresh = False  # 默认操作都是不刷新获取元素

    def __get__(self, instance, owner):
        if instance is None:
            return None
        self.driver = instance.driver
        return self

    def __elements(self, key, value, driver=None):
        if key == 'id':
            value = GSTORE['package_id'] + value
        elems = WebDriverWait(self.driver if driver is None else driver, timeout=self.timeout,
                              poll_frequency=0.5).until(
            lambda d: d.find_elements(key, value)
        )
        return elems

    @tip
    def __find_element(self, locator: tuple):
        """
        Find if the element exists.
        :param locator: 定位
        :type locator: tuple = (定位方式,定位路径)
        :description:
            如果🈚️子元素就按照正常方式去查找，返回单个元素
            有子元素的情况下，只会根据index找到对应的父元素接着查找子元素并返回单个子元素
        :return:
        """
        if self.child is None:
            for i in range(self.retry):
                try:
                    elems = self.__elements(*locator)
                except TimeoutException:
                    log.info(f" ❌  {self.desc} |元素第「{i + 1}」次查找失败:: {locator[0]}={locator[1]}.")
                    sleep(1)
                    continue
                else:
                    if len(elems) == 1:
                        log.info(f"🔍  {self.desc} | 查找到元素: {locator[0]}={locator[1]}.")
                        return elems[0]
                    else:
                        # 返回的是元素集合
                        if self.index is None:
                            raise PageElementError("查找到的是元素集合，请使用Elements")
                        log.info(f"🔍  {self.desc} | 查找到 {len(elems)} 个元素: {locator[0]}={locator[1]}.")
                        return elems[self.index]
            error_msg = f'❌ 元素查找失败: {locator[0]}={locator[1]}. {self.desc}'
        else:
            # (way,path,index)
            child_way = LOCATOR_LIST.get(self.child[0], None)
            if self.child[2] is None:
                _index = 0
            else:
                _index = self.child[2]
            for i in range(self.retry):
                try:
                    parent_el = self.__elements(*locator)[self.index]
                    child_els = self.__elements(child_way, self.child[1], parent_el)
                except TimeoutException:
                    sleep(1)
                    log.info(f" ❌  {self.desc} |元素第「{i + 1}」次查找失败:: {child_way}={self.child[1]}.")
                    continue
                else:
                    if len(child_els) == 1:
                        log.info(f"🔍  {self.desc} | 查找到元素: {child_way}={self.child[1]}.")
                        return child_els[0]
                    else:
                        # 返回的是元素集合
                        if self.child[3] is None:
                            raise PageElementError("查找到的是元素集合，请使用Elements")
                        log.info(f"🔍  {self.desc} | 查找到 {len(child_els)} 个元素: {child_way}={self.child[1]}")
                        return child_els[_index]
            error_msg = f'❌ {self.desc}| 元素查找失败: {child_way}={self.child[1]}.'
        log.warning(error_msg)
        raise PageElementUnFindException(error_msg)

    def __get_element(self, by, value):
        """
        判断定位方式 查找返回元素
        :param by:
        :param value:
        :return:
        """
        if self.refresh or self.el is None:
            self.el = self.__find_element((LOCATOR_LIST[by], value))
        return self.el

    # region 封装的方法

    @property
    def refresh_el(self):
        self.refresh = True
        return self

    @property
    def exist(self) -> bool:
        """
        元素是否存在
        :return:
        """
        try:
            self.__get_element(self.k, self.v)
        except PageElementUnFindException:
            log.info(f"❌ {self.desc}|下标:{self.index} | 元素不存在.")
            return False
        else:
            log.info(f"✅ {self.desc}|下标:{self.index} | 元素存在.")
            return True

    def clear(self):
        """Clears the text if it's a text entry element."""
        elem = self.__get_element(self.k, self.v)
        elem.clear()
        log.info(f"✅ {self.desc} | 内容清空.")

    def send_keys(self, value, clear=False, click=False) -> None:
        """
        如果 click / clear 设置为True那就会在文本输入前执行对应的操作
        """
        elem = self.__get_element(self.k, self.v)
        if click:
            elem.click()
        if clear:
            elem.clear()
            sleep(0.5)
        elem.send_keys(value)
        log.info(f"✅ {self.desc} | 按键输入 ('{value}').")

    def click(self, check=False, times=1) -> None:
        """
        Clicks the element.
        """
        elem = self.__get_element(self.k, self.v)
        time.sleep(0.25)  # 点击前 等待
        for i in range(times):
            elem.click()
        log.info(f"✅ {self.desc} | 点击.")
        time.sleep(0.5)
        if check:
            time.sleep(1)
            if self.exist:
                log.info(f"✅ {self.desc}未消失 | 二次点击.")
                elem.click()
            else:
                log.info(f"✅ {self.desc}已消失")

    @property
    def tag_name(self) -> str:
        """This element's ``tagName`` property."""
        elem = self.__get_element(self.k, self.v)
        tag_name = elem.tag_name
        log.info(f"✅ {self.desc} | tag_name: {tag_name}.")
        return tag_name

    @property
    def text(self) -> str:
        """所有获取的文本原样 去除两边空格"""
        elem = self.__get_element(self.k, self.v)
        text = elem.text.strip()
        log.info(f"✅ {self.desc} 获取无间隔文本: {text}.")
        return text

    @property
    def real_text(self) -> str:
        """所有获取的文本都去除空格"""
        elem = self.__get_element(self.k, self.v)
        text = elem.text.strip().replace(' ', '')
        log.info(f"✅ {self.desc} 获取真实文本: {text}.")
        return text

    @property
    def size(self) -> dict:
        """The size of the element."""
        elem = self.__get_element(self.k, self.v)
        size = elem.size
        log.info(f"✅{self.desc} | size: {size}.")
        return size

    def get_property(self, name) -> str:
        """
        Gets the given property of the element.
        """
        elem = self.__get_element(self.k, self.v)
        value = elem.get_property(name)
        log.info(f"✅{self.desc} | get_property('{name}') -> {value}.")
        return value

    def get_attribute(self, name) -> str:
        """
        Gets the given attribute or property of the element.
        """
        elem = self.__get_element(self.k, self.v)
        value = elem.get_attribute(name)
        log.info(f"✅ {self.desc} | get_attribute('{name}') -> {value}.")
        return value

    def is_displayed(self) -> bool:
        """Whether the element is visible to a user."""
        elem = self.__get_element(self.k, self.v)
        display = elem.is_displayed()
        log.info(f"✅ {self.desc} | is_displayed() -> {display}.")
        return display

    def is_selected(self) -> bool:
        """
        Returns whether the element is selected.

        Can be used to check if a checkbox or radio button is selected.
        """
        elem = self.__get_element(self.k, self.v)
        select = elem.is_selected()
        log.info(f"✅ {self.desc} | is_selected() -> {select}.")
        return select

    def is_enabled(self) -> bool:
        """Returns whether the element is enabled."""
        elem = self.__get_element(self.k, self.v)
        enable = elem.is_enabled()
        log.info(f"✅{self.desc} | is_enabled() -> {enable}.")
        return enable

    def is_checked(self) -> bool:
        """
        判断元素checked属性
        :return:
        """
        status = self.get_attribute('checked')
        log.info(f"✅{self.desc} | is_checked() -> {status}.")
        return True if status == 'true' else False

    def set_text(self, text):
        """
        appium API
        Sends text to the element.
        """
        elem = self.__get_element(self.k, self.v)
        elem.set_text(text)
        log.info(f"✅{self.desc} | 文本输入('{text}').")
        return self

    @property
    def location_in_view(self):
        """
        appium API
        Gets the location of an element relative to the view.
        Returns:
            dict: The location of an element relative to the view
        """
        elem = self.__get_element(self.k, self.v)
        location = elem.location_in_view()
        log.info(f"✅ {self.desc} | location_in_view -> {location}.")
        return location

    @property
    def location(self) -> dict:
        """
        返回xy坐标
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        location = elem.location
        log.info(f"✅ {self.desc} | location -> {location}.")
        return location

    @property
    def rect(self) -> dict:
        """
        返回元素 宽高和xy坐标
        :return: {'x':aaa,'y':bbb,'height':ccc,'width':ddd}
        """
        elem = self.__get_element(self.k, self.v)
        location = elem.rect
        log.info(f"✅ {self.desc} | rect -> {location}.")
        return location

    def element_screenshot(self, filename):
        """
        元素控件截图
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        elem.screenshot(filename)
        return self

    def element_ocr_click_by_text(self, text):
        """
        元素ocr点击
        :param text: 要点击的文本
        :return:
        """
        save_path = os.path.join(img_dir, f'{self.desc.replace("/", "|")}.png')
        rect = self.element_screenshot(save_path).rect
        rsp = get_pos_by_ocr(save_path)
        os.remove(save_path)
        ocr_pos = rsp.get(text)
        if not ocr_pos:
            raise Exception(f'图像识别失败,响应结果{rsp}')
        pos = [ocr_pos[0] + rect['x'], ocr_pos[1] + rect['y']]
        self.driver.tap([pos])

    def set_value(self, value: str):
        """
        appium API
        Set the value on this element in the application
        """
        elem = self.__get_element(self.k, self.v)
        elem.set_value(value)
        log.info(f"✅ set_value('{value}').")
        return self

    def swipe_args(self, start_x_percent: float = 0.0, end_x_percent: float = 0.0, start_y_percent: float = 0.0,
                   end_y_percent: float = 0.0, duration=1000):
        """
        获取元素滑动的坐标信息（在元素组件中滑动）
        :param start_x_percent:
        :param end_x_percent:
        :param start_y_percent:
        :param end_y_percent:
        :param duration:
        :return:
        """
        rect = self.rect
        x_left, x_right = rect['x'], rect['x'] + rect['width']
        y_low, y_high = rect['y'], rect['y'] + rect['height']
        start_x = int(x_left + (x_right - x_left) * start_x_percent)
        end_x = int(x_left + (x_right - x_left) * end_x_percent)
        start_y = int(y_low + (y_high - y_low) * start_y_percent)
        end_y = int(y_low + (y_high - y_low) * end_y_percent)
        return start_x, start_y, end_x, end_y, duration

    @property
    def web_element(self) -> WebElement:
        """
        返回webElement类型元素（用于拖拽）
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        return elem
    # endregion


class Elements:
    def __init__(self, retry: int = 2, timeout: int = 5, describe: str = "", index: int = None,
                 child: tuple = None, **kwargs):
        """
        :param retry: 重试定位次数
        :param timeout: 定位超时时间
        :param describe: 元素描述
        :param index: 下标 （查找元素集合）
        :param kwargs:
        :param child: 子元素定位方式
        :type child : tuple  (way,path,index) 查找子元素集合 （way=xx,path=xx,index=None,is_set=None）
                        way ：定位方式
                        path：定位路径
                        index：元素下标
        """
        self.retry = retry
        self.timeout = timeout
        self.index = index
        self.desc = describe
        self.child = child
        if not kwargs:
            raise ValueError("请指定定位方式和路径")
        if len(kwargs) > 1:
            raise ValueError("只允许单一路径定位")
        self.kwargs = kwargs
        self.k, self.v = next(iter(kwargs.items()))

        if self.k not in LOCATOR_LIST.keys():
            raise FindElementTypesError(f"暂不支持定位方式-{self.k}")
        self.els = None
        self.refresh = False  # 默认操作都是不刷新获取元素

    def __get__(self, instance, owner):
        if instance is None:
            return None
        self.driver = instance.driver
        return self

    def __elements(self, key, value, driver=None):
        if key == 'id':
            value = GSTORE['package_id'] + value
        elems = WebDriverWait(self.driver if driver is None else driver, timeout=self.timeout,
                              poll_frequency=0.5).until(
            lambda d: d.find_elements(key, value)
        )
        return elems

    @tip
    def __find_element(self, locator: tuple):
        """
        Find if the element exists.
        :param locator: 定位
        :type locator: tuple = (定位方式,定位路径)
        :description:
            如果🈚️子元素就按照正常方式去查找，返回元素集合
            有子元素的情况下 会根据index找到对应的父元素接着查找子元素集合
        :return:
        """
        if self.child is None:
            for i in range(self.retry):
                try:
                    elems = self.__elements(*locator)
                except TimeoutException:
                    log.info(f" ❌  {self.desc} |元素第「{i + 1}」次查找失败:: {locator[0]}={locator[1]}.")
                    sleep(1)
                    continue
                else:
                    if len(elems) == 1:
                        log.info(f"🔍  {self.desc} | 查找到元素: {locator[0]}={locator[1]}.")
                    else:
                        log.info(f"🔍  {self.desc} | 查找到 {len(elems)} 个元素: {locator[0]}={locator[1]}.")
                    return elems
            error_msg = f'❌ 元素查找失败: {locator[0]}={locator[1]}. {self.desc}'
        else:
            # (way,path,index)
            child_way = LOCATOR_LIST.get(self.child[0], None)
            if self.child[2] is not None:
                raise PageElementError("查找单个元素，请使用Element")
            for i in range(self.retry):
                try:
                    parent_el = self.__elements(*locator)[self.index]
                    child_els = self.__elements(child_way, self.child[1], parent_el)
                except TimeoutException:
                    sleep(1)
                    log.info(f" ❌  {self.desc} |元素第「{i + 1}」次查找失败:: {child_way}={self.child[1]}.")
                    continue
                else:
                    if len(child_els) == 1:
                        log.info(f"🔍  {self.desc} | 查找到元素: {child_way}={self.child[1]}.")
                    else:
                        log.info(f"🔍  {self.desc} | 查找到 {len(child_els)} 个元素: {child_way}={self.child[1]}")
                    return child_els
            error_msg = f'❌ {self.desc}| 元素查找失败: {child_way}={self.child[1]}.'
        log.warning(error_msg)
        raise PageElementUnFindException(error_msg)

    def __get_element(self, by, value):
        """
        判断定位方式 查找返回元素
        :param by:
        :param value:
        :return:
        """
        if self.refresh or self.els is None:
            self.els = self.__find_element((LOCATOR_LIST[by], value))
        return self.els

    @property
    def refresh_el(self):
        self.refresh = True
        return self

    def get_element(self, index):
        """
        获取单个元素
        """
        if self.child is not None:
            child_back = list(self.child)
            child_back.append(index)
            return Element(retry=self.retry, timeout=self.timeout, describe=self.desc, child=tuple(child_back)
                           , **self.kwargs)
        else:
            return Element(retry=self.retry, timeout=self.timeout, describe=self.desc, index=index, **self.kwargs)

    def elem_click_by_index(self, index: int):
        """
        元素集合匹配下标点击
        :param index: 下标
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        elem[index].click()
        log.info(f"✅ {self.desc} | 点击元素集合第{index + 1}元素")

    def elem_click_by_text(self, target_text: str) -> None:
        """
        元素集合中匹配对应的元素文本点击
        :param target_text: 目标文本
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        for el in elem:
            if el.text.strip() == target_text:
                el.click()
                break
        log.info(f"✅ {self.desc} | 点击{target_text}元素")

    def elem_is_select(self) -> str:
        """
        元素集合匹配被选中的元素并返回文本
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        for el in elem:
            if el.get_attribute('selected') == 'true':
                text = el.text
                log.info(f"✅ {self.desc} | 元素{text}被选中")
                return text
        raise PageElementUnFindException('界面不存在被选中的元素')

    def texts(self) -> list:
        """
        只支持元素集合获取文本
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        text_list = list()
        for el in elem:
            text_list.append(el.text.strip())
        log.info(f"✅ {self.desc} | 获取元素集合文本 : {text_list}")
        return text_list

    @property
    def count(self) -> int:
        """
        统计元素个数
        :return:
        """
        elem = self.__get_element(self.k, self.v)
        return len(elem)
