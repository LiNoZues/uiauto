"""
# File       : command.py
# Time       ：2022/3/25 3:49 PM
# Author     ：A_zz
# email      ：chenzhe12320@163.com
# Description：一些需要控制台执行的命令
"""


# 暂时不考虑系统差异，到时候有需求再改
# # win
# start /b appium -a 127.0.0.1 -p 4723  --log xxx.log --local-timezone
# # mac
# appium -a 127.0.0.1 -p 4723  --log xxx.log --local-timezone
class Command:
    # 启动appium-server
    appium_server_command = 'appium -a 127.0.0.1 -p {} -U {} -g {} --local-timezone'
    # 查看端口占用情况 返回进程号
    get_pid_command = "lsof -i:%d|awk '{print $2}'|sed -n '2p'"
    kill_command = 'kill -9 {}'
