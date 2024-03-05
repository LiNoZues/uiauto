"""
# File       : gstore.py
# Time       ：2022/3/24 11:20 AM
# Author     ：A_zz
# email      ：chenzhe12320@163.com
# Description：
"""
import os
import time
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # 把带','的数字转换成 正常的数字
base_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(base_dir, 'imgs')
mp4_dir = os.path.join(base_dir, 'mp4')
log_dir = os.path.join(base_dir, 'log')
report_dir = os.path.join(base_dir, 'report')

GSTORE = {
    'conf': None,  # 当前任务获取到的配置文件
    'task_name': None,  # 当前任务名 设备号+时间
    'SSP': os.path.join(img_dir, 'test'),  # 当前任务截图保存路径 screen—shot—path
    'time': time.strftime("%Y-%m-%d-%H%M%S", time.localtime(time.time())),  # 程序执行时间
    'env': None,
    'package_id': 'tv.danmaku.bili:id/',
}
