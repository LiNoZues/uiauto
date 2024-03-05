"""
# File       : exception.py
# Time       ：2022/7/8 15:20
# Author     ：
# email      ：
# Description：封装异常框架
"""


class UserDefineException(Exception):
    """
    Base exception.
    """

    def __init__(self, msg=None, stacktrace=None):
        self.msg = msg
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class ParamError(UserDefineException):
    pass


class NotInRightPage(UserDefineException):
    """
    不在对应界面
    """
    pass


class PageElementUnFindException(UserDefineException):
    """
    页面元素定位失败
    """
    pass


class PageElementError(UserDefineException):
    """
    Raises an error using the PagElement class
    """
    pass


class FindElementTypesError(UserDefineException):
    """
    Find element types Error
    """
    pass


class MethodNotAllowed(UserDefineException):
    """
    方法不被允许
    """
