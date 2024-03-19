import pytest
from loguru import logger as log
from libs.util_back.common import create_file, read_config
from gstore import *

os.environ.setdefault('JAVA_HOME', '/Library/Java/JavaVirtualMachines/jdk1.8.0_321.jdk/Contents/home')
os.environ.setdefault('ANDROID_HOME', '/Users/cz/Library/Android/sdk')


def run(code):
    # '--instafail','--tb=line'
    pytest.main([] + code + ['-sv', '--alluredir=./allure_data','--clean-alluredir'])
    log.info("-- 执行完成 --")
    # 生成报告
    os.system(f'allure generate -c -o {GSTORE["report_path"]} ./allure_data')
    # 打开报告
    # os.system('allure open ./allure-report')
    # os.system('allure serve allure')


if __name__ == '__main__':
    log.info('创建初始化文件夹')
    for p in [log_dir, img_dir, mp4_dir, report_dir]:
        create_file(p)
    report_path = os.path.join(report_dir, f'report_{GSTORE["time"]}')
    GSTORE['report_path'] = report_path
    create_file(report_path)
    log.info("-- 开始测试 --")
    log.info("-- 读取config.yaml配置文件 --")
    conf = read_config()
    run_id = conf['common']['run_id']  # 可以是列表
    devices = conf['devices']
    match conf['way']:
        case 0:
            # 单发
            caps = devices[run_id]
            # cmd = ['--cmdopt=0', '--caps={}'.format(caps), '-m', 'dev']  # 调试命令
            cmd = ['--cmdopt=0', '--caps={}'.format(caps)]
            GSTORE['env'] = caps['env']
            log.warning(GSTORE['env'])
            run(cmd)
        case 1:  # 多进程  # 暂时不能够支持 安卓/ios同时多进程
            # cmd = ['--cmdopt=1', '-n', '2']
            cmd = ['--cmdopt=1', '-n', '3', '-m', 'xdist_dev']
            run(cmd)
        case _:
            raise Exception('way参数配置错误')
    log.info("-- 结束测试 --")
