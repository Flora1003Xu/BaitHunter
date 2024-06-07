import configparser
import signal
import subprocess
import platform
from stop_and_run_uiautomator import rerun_uiautomator2

def get_OS_type():
    sys_platform = platform.platform().lower()
    os_type = ''
    if "windows" in sys_platform:
        os_type = 'win'
    elif "darwin" in sys_platform or 'mac' in sys_platform:
        os_type = 'mac'
    elif "linux" in sys_platform:
        os_type = 'linux'
    else:
        print('Unknown OS,regard as linux...')
        os_type = 'linux'
    return os_type


def clear_app_cache(app_package_name):
    print('正在清除应用包名为{}的数据。。。'.format(app_package_name))
    execute_cmd_with_timeout('adb shell pm clear {}'.format(app_package_name))
    print('清除完毕。')


def execute_cmd_with_timeout(cmd, timeout=600):
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)
    try:
        p.wait(timeout)
    except subprocess.TimeoutExpired:
        p.send_signal(signal.SIGINT)
        p.wait()


def get_config_settings(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    pairs = []
    for section in config.sections():
        pairs.extend(config.items(section))
    dic = {}
    for key, value in pairs:
        dic[key] = value
    return dic


if __name__ == '__main__':
    config_settings = get_config_settings('config.ini')

    with open('apk_pkgName.txt', 'r', encoding='utf-8') as f:
        content = f.readlines()
    pkgName_appName_list = [item.rstrip('\n') for item in content]
    os_type = get_OS_type()
   
    # 遍历txt文件中的所有包
    for pkgName_appName in pkgName_appName_list:
        # print(pkgName_appName)
        if pkgName_appName.startswith('#'):
            print(pkgName_appName + 'is ignored,continue...')
            continue
        try:
            pkgName, appName = pkgName_appName.split(' | ')
            appName = appName.strip('\'')
            if config_settings['clear_cache'] == 'true':
                clear_app_cache(pkgName)
            if config_settings['rerun_uiautomator2'] == 'true':
                rerun_uiautomator2()
            print('analysis {} : {}now...'.format(pkgName, appName))
            if os_type in ['linux', 'mac']:
                execute_cmd_with_timeout(
                    'python3 run.py {} {} {} {} {} {} {}'.format(pkgName, appName, config_settings['dynamic_ui_depth'],
                    config_settings['dynamic_run_time'],config_settings['searchprivacypolicy'],config_settings['drawappcallgraph'],
                    config_settings['screenuidrep']),timeout=int(config_settings['dynamic_run_time']) + 120)
                # kill current app
            elif os_type == 'win':
                # 运行了python run.py并且动态地传入与相应应用有关的参数<pkgName>, <appName>, <dynamic_ui_depth>, <dynamic_run_time>, <searchprivacypolicy>, <drawappcallgraph>, <screenuidrep>
                    execute_cmd_with_timeout(
                    'python run.py {} {} {} {} {} {} {}'.format(pkgName, appName, config_settings['dynamic_ui_depth'],
                    config_settings['dynamic_run_time'],config_settings['searchprivacypolicy'],config_settings['drawappcallgraph'],
                    config_settings['screenuidrep']),timeout=int(config_settings['dynamic_run_time']) + 120)
            print(f'kill {pkgName} in try...')
            execute_cmd_with_timeout(f'adb shell am force-stop {pkgName}')

        except Exception as e:
            print(e)
            print('error occurred, continue...')
            print(f'kill {pkgName} in exception...')
            execute_cmd_with_timeout(f'adb shell am force-stop {pkgName}')
