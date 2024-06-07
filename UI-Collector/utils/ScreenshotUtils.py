import base64
import os
import hashlib
import json
from Config import *

# 实现一个屏幕截图功能, 注: uiautomator2具有截图功能
# 要求实现截图, 并且将截图命名为encode_screen_uid(screen_uid),即编码当前界面信息的字符串,并且将文件保存在Screenshot目录下(目录不存在则程序自动创建)
# 并且encode_screen_uid(screen_uid)能够进行解码回screen_uid, 即decode_screen_uid(encode_screen_uid(screen_uid)) = screen_uid
# 编码解码格式可以自行选择
# 测试可以在test/ScreenshotUtils_test.py上进行测试, 不需要跑其他文件
class ScreenshotUtils:
    @staticmethod
    def screen_shot(screen_uid:str) -> str:
        # 连接设备
        d = Config.get_instance().get_device()

        # 创建及写入映射json
        ScreenshotUtils.create_json_file('screenshot_map')
        ScreenshotUtils.write_mapping_to_json('screenshot_map', ScreenshotUtils.encode_screen_uid(screen_uid), screen_uid)

        # 获取屏幕截图
        screenshot = d.screenshot()



        config_path = Config.get_instance().get_collectDataPath()
        print(config_path)
        # if not os.path.exists(config_path):
        #     os.makedirs(config_path)

        screenshot_dir = "Screenshot"
        # 创建保存截图和json的目录（如果不存在）
        screenshot_dir = os.path.join(config_path, screenshot_dir)
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # 构造截图文件名，并保存截图
        filename = ScreenshotUtils.encode_screen_uid(screen_uid)
        screenshot_dir_picture = 'ScreenshotPicture'
        savepath = os.path.join(screenshot_dir, screenshot_dir_picture)
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        filepath = os.path.join(savepath, filename+'.png')
        # filepath = savepath + '/' + filename + '.png'
        screenshot.save(filepath)
        return filepath

    @staticmethod
    def encode_screen_uid(screen_uid: str) -> str:
        hashed_data = hashlib.sha256(screen_uid.encode('utf-8')).digest()
        encoded_bytes = base64.urlsafe_b64encode(hashed_data).decode('utf-8')
        return encoded_bytes

    @staticmethod
    def decode_screen_uid(encode_str: str) -> str:
        file_path = "Screenshot/" + "screenshot_map.json"
        with open(file_path, 'r') as file:
            data = json.load(file)

        value = data.get(encode_str)
        return value

    @staticmethod
    def create_json_file(name):
        # 创建保存 JSON 文件的目录（如果不存在）
        config_path = Config.get_instance().get_collectDataPath()
        screenshot_dir = "Screenshot"
        dir_path = os.path.join(config_path, screenshot_dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        dir_path_json = 'ScreenshotJson'
        dir_path = os.path.join(dir_path, dir_path_json)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 构建文件路径
        file_path = os.path.join(dir_path, f"{name}.json")

        # 检查文件是否存在
        if not os.path.exists(file_path):
            # 创建空的 JSON 数据
            data = {}
            # 写入 JSON 文件
            with open(file_path, 'w') as file:
                json.dump(data, file)

    @staticmethod
    def write_mapping_to_json(name, key, value):
        config_path = Config.get_instance().get_collectDataPath()
        screenshot_dir = "Screenshot"
        screenshot_json_dir = "ScreenshotJson"
        json_name = f"{name}.json"
        file_path = os.path.join(config_path, screenshot_dir, screenshot_json_dir, json_name)
        # 读取 JSON 文件
        with open(file_path, 'r') as file:
            data = json.load(file)

        # 添加映射关系
        data[key] = value

        # 写入 JSON 文件
        with open(file_path, 'w') as file:
            json.dump(data, file)




