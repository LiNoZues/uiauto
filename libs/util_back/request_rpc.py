"""
# File       : request_rpc.py
# Time       ：2022/3/25 4:21 PM
# Author     ：A_zz
# email      ：chenzhe12320@163.com
# Description：
"""
from json import JSONDecodeError

import requests
from loguru import logger as log
from requests import Response

from gstore import GSTORE
from libs.util_back.common import read_config


class RequestManager:
    def __new__(cls, *args, **kwargs):
        if not GSTORE.get('conf'):
            read_config()
        return super(RequestManager,cls).__new__(cls)

    def __init__(self):
        self.url = GSTORE['conf']['common']['rpc_url']
        self.account_open = GSTORE['conf']['common']['account_open']

    @staticmethod
    def _log_response(rsp: Response):
        log.info(f"响应状态码:{rsp.status_code}\t"
                 f"响应时间:{rsp.elapsed.microseconds/1000}ms")
        message = None
        if isinstance(rsp,dict):
            log.info(f'响应结果：{rsp}')
        else:
            try:
                message = rsp.json()
            except JSONDecodeError:
                message = rsp.text
            finally:
                log.info(f'响应结果：{message}')

    def post(self, url_params=None, url_headers=None, url_body=None):
        """
        :param url_headers: 请求头 无则为None
        :param url_body: 请求体 无则为Nobe  多种请求体类型情况会在
        :param url_params:url参数
        :return:均已json转换过的响应体
        """
        rpc_header = {
            'Content-Type': 'application/json',
            'account-open': self.account_open,  # 是否开户，不用填写代表未开户
            'timeout': '20'
        }
        api_url = self.url
        if url_params:
            api_url = '{}/{}'.format(self.url, url_params)
        try:
            if url_headers:
                rpc_header.update(url_headers)
            res = requests.post(api_url, headers=rpc_header,
                                json=url_body)
        except requests.ConnectionError:
            raise Exception('连接rpc失败，请检查跳板机服务')
        self._log_response(res)
        try:
            json_data = res.json()
        except JSONDecodeError:
            raise Exception(f'{url_body}-返回结果不是json格式')
        else:
            return json_data


req = RequestManager()

