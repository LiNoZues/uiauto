"""
# File       : appium_service_manager.py
# Time       ：2022/3/25 11:21 AM
# Author     ：A_zz
# email      ：chenzhe12320@163.com
# Description：
"""
from gstore import *
from libs.util_back.common import create_file
from libs.util_back.command import Command
from loguru import logger as log


class ServiceManager:
    def __init__(self, conf: dict):
        self.conf = conf

    def start_appium_server(self):
        port, uid = self.check_config()
        # 并行交给pytest来操作就行了 -cmdopt传设备的配置
        GSTORE['task_name'] = f'{uid}-{GSTORE["time"]}'
        if isinstance(port, int):
            self.listen_port(port)
            # 创建设备对应保存截图的文件夹、当前任务截图文件夹
            img_uid_path = os.path.join(img_dir, uid)
            screen_shot_path = os.path.join(img_uid_path, GSTORE['task_name'])
            GSTORE['SSP'] = screen_shot_path
            for p in [img_uid_path, screen_shot_path]:
                create_file(p)
            # 拼接appium—log路径
            appium_log_path = os.path.join(log_dir,f'{GSTORE["time"]}-{uid}-appium_log.log')

            command = Command.appium_server_command.format(port, uid, appium_log_path)
            log.info(command)
            os.popen(command)
            time.sleep(3)
            log.info(f'appium-{port}启动成功')

    def check_config(self) -> [int, str]:
        """
        :param :
        :return:
            port： appium启动端口
            uid:   设备号
        """
        conf = self.conf
        port = conf['port']
        uid = conf['desired_caps']['udid']

        return port, uid

    @staticmethod
    def listen_port(port):
        command = Command.get_pid_command % port
        rsp = os.popen(command).read()
        # 端口被占用就杀进程
        if rsp:
            os.system(Command.kill_command.format(rsp))

    def stop_appium_server(self):
        port = self.conf['port']
        self.listen_port(port)
        log.info(f"关闭端口--{port}")


if __name__ == '__main__':
    import os
    # from appium_test import test
    import time
    # print(os.popen('cat ~/.bash_profile').read())
    os.environ.setdefault('JAVA_HOME', '/Library/Java/JavaVirtualMachines/jdk1.8.0_321.jdk/Contents/home')
    os.environ.setdefault('ANDROID_HOME', '/Users/cz/Library/Android/sdk')
    os.popen('appium -a 127.0.0.1 -p 4723  -g xxx.log --local-timezone')
    time.sleep(3)
    # test()   # run test code
