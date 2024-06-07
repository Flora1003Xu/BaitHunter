from Config import Config
import os
from StatRecorder import *

class FileUtils:

    @classmethod
    def save_total_coverage(cls, maxDepth, cal_cov_map):
        file_name = cls.__get_cov_file_path()
        cls.__write_word(file_name, "total coverage")
        for i in range(1, maxDepth + 1):
            if cal_cov_map.get(i, None) is not None:
                cls.__save_atotal_coverage(i,cal_cov_map[i][0], cal_cov_map[i][1], cal_cov_map[i][2])


    @classmethod
    def __save_atotal_coverage(cls, depth, a, b, c):
        file_name = cls.__get_cov_file_path()
        cls.__write_total_cov(file_name, depth, a, b, c)


    @classmethod
    def save_coverage(cls, depth, a, b):
        file_name = cls.__get_cov_file_path()
        cls.__write_cov(file_name, depth, a, b)


    @classmethod
    def save_word(cls, word:str):
        file_name = cls.__get_cov_file_path()
        cls.__write_word(file_name, word)

    @classmethod
    def save_result(cls):
        file_name = cls.__get_cov_file_path()
        sr = StatRecorder.get_instance()
        ans = ""
        ans += f"总共点击的activity个数 {len(sr.stat_activity_set)}\n"
        ans += f"总共点击的Screen个数: {len(sr.stat_screen_set)}\n"
        ans += f"总共点击的组件个数: {sr.total_eles_cnt}\n"
        # ans += f"总共触发的WebView个数: {len(sr.webview_set)}\n"
        cls.__write_res(file_name, ans)


    @staticmethod
    def __get_cov_file_path():
        config_path = Config.get_instance().get_collectDataPath()
        cov_file_name = "coverage.txt"
        return os.path.join(config_path, cov_file_name)

    @staticmethod
    def __write_res(file_path, res):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        fw.write(res)
        fw.close()

    @staticmethod
    def __write_cov(file_path:str, depth, a, b):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        cov = a/b
        fw.write(f"{depth}:{a}/{b}={cov}" + "\n")
        fw.close()

    @staticmethod
    def __write_total_cov(file_path:str, depth, a, b, c):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        cov2 = b/c
        fw.write(f"{depth}:{b}/{c}={cov2}" + "\n")
        fw.close()

    @staticmethod
    def __write_word(file_path:str, word):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        fw.write(word + "\n")
        fw.close()


