"""
# File       : common.py
# Time       ：2022/3/24 11:18 AM
# Author     ：A_zz
# email      ：chenzhe12320@163.com
# Description：
"""
import time

import yaml, os, json
from typing import Union
from gstore import GSTORE, base_dir
from functools import lru_cache
from loguru import logger as log
from decimal import Decimal
import easyocr


def get_pos_by_ocr(image_path) -> dict:
    """
    使用ocr获取对应的文字坐标
    :param image_path:
    :return: {'文字a':(中心点x坐标,中心点y坐标)}
    """
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
    # allowlist - 允许识别的字符串集
    res = reader.readtext(image_path, text_threshold=0.7, mag_ratio=1.5)
    position_dict = dict()
    for item in res:
        key = item[1]
        rect = item[0]
        min_x = rect[0][0]
        min_y = rect[0][1]
        max_x = rect[2][0]
        max_y = rect[2][1]
        center_pos = [int((min_x + max_x) / 2), int((min_y + max_y) / 2)]  # 中心坐标点
        position_dict[key] = center_pos
    log.info(f'键盘坐标字典:{position_dict}')
    return position_dict


def read_yaml(path: str):
    with open(path) as f:
        return yaml.safe_load(f)


def read_json(path: str):
    with open(path) as f:
        return json.loads(f.read())


@lru_cache
def read_app_config():
    json_config = read_json(f'{base_dir}/app_config.json')
    return json_config


@lru_cache
def read_config() -> Union[dict, list]:
    # 读yaml配置文件
    config = read_yaml(f"{base_dir}/config.yaml")
    GSTORE['conf'] = config
    return config


def create_file(path):
    if not os.path.exists(path):
        log.info(f"创建文件夹-{path}")
        os.makedirs(path)


def l_round(value, digit):
    """
    自定义保留的几位小数函数
    :param value:
    :param digit:
    :return:
    """
    return Decimal(value).quantize(Decimal(f"0.{'0' * digit}"))


def transition_code(code: str):
    """
    转换代码 港股需要 去0
    :param code:
    :return:
    """
    tag_index = 0
    if code.startswith('0'):
        for index, char in enumerate(code):
            if char != '0':
                tag_index = index
                break
    return ''.join(code[tag_index:])


if __name__ == '__main__':
    # quote_tag
    rsp = get_pos_by_ocr('../../imgs/temp.png')
    print(rsp)
