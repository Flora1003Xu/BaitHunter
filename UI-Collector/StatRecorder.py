import time

from utils.LogUtils import *
from RuntimeContent import *
from constant.DefException import TimeLimitException
class StatRecorder(object):
    def __init__(self):
        self.total_eles_cnt = 0
        self.stat_screen_set = set()
        self.stat_activity_set = set()
        self.start_time = -1
        self.end_time = -1
        self.restart_cnt = 0
        self.webview_set = set()

    def __new__(cls, *args, **kwargs):
        if not hasattr(StatRecorder, "_instance"):
            StatRecorder._instance = object.__new__(cls)
        return StatRecorder._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(StatRecorder, '_instance'):
            StatRecorder._instance = StatRecorder(*args, **kwargs)
        return StatRecorder._instance

    def set_start_time(self):
        self.start_time = time.time()

    def inc_total_ele_cnt(self):
        self.total_eles_cnt +=1

    def add_stat_screen_set(self, ck_eles_text:str):
        self.stat_screen_set.add(ck_eles_text)

    def add_webview_set(self, webview_text:str):
        self.webview_set.add(webview_text)

    def add_stat_stat_activity_set(self, cur_activity):
        self.stat_activity_set.add(cur_activity)

    def count_time(self):
        self.end_time = time.time()
        if self.end_time - self.start_time > Config.get_instance().test_time:
            raise TimeLimitException("超时")

    def print_result(self):
        LogUtils.log_info(f"总共点击的activity个数 {len(self.stat_activity_set)}")
        LogUtils.log_info(f"总共点击的Screen个数: {len(self.stat_screen_set)}")
        LogUtils.log_info(f"总共点击的组件个数: {self.total_eles_cnt}")
        # LogUtils.log_info(f"总共触发的WebView个数: {len(self.webview_set)}")
        self.end_time = time.time()
        LogUtils.log_info(f"时间为 {self.end_time - self.start_time}")

    def get_total_coverage(self):
        screen_depth_map = RuntimeContent.get_instance().screen_depth_map
        # screen_uid_list = [screen_uid for screen_uid, depth in sorted(screen_depth_map.items(), key=lambda x: x[1])]
        screen_uid_list = screen_depth_map.keys()
        cal_cov_map = {}
        snode_set = set()
        for screen_uid in screen_uid_list:
            screen_node = RuntimeContent.get_instance().get_screen_map().get(screen_uid)
            if screen_node is not None:
                clickable_eles = screen_node.get_diff_or_clickable_eles()
                if clickable_eles is None or len(clickable_eles) == 0:
                    # print(f"深度{depth}: {screen_uid} 没有可点击组件")
                    continue
                snode_set.add(screen_node)

        for screen_node in snode_set:
            depth = screen_depth_map.get(screen_node.ck_eles_text)
            if cal_cov_map.get(depth, None) is None:
                cal_cov_map[depth] = [0, 0, 0]
            total_cnt = len(screen_node.get_diff_or_clickable_eles())
            click_cnt = screen_node.total_clicked_cnt

            candidate_click_cnt = 0
            for ele in screen_node.get_diff_or_clickable_eles():
                if ele in RuntimeContent.get_instance().already_click_eles:
                    candidate_click_cnt +=1

            cal_cov_map[depth][0] += click_cnt
            cal_cov_map[depth][1] += candidate_click_cnt
            cal_cov_map[depth][2] += total_cnt
        return cal_cov_map



    def get_coverage(self, cur_depth:int):
        screen_depth_map = RuntimeContent.get_instance().screen_depth_map
        # screen_uid_list = [screen_uid for screen_uid, depth in sorted(screen_depth_map.items(), key=lambda x: x[1])]
        screen_uid_list = screen_depth_map.keys()
        cal_cov_map = {}
        snode_set = set()
        for screen_uid in screen_uid_list:
            depth = screen_depth_map.get(screen_uid)
            if depth != cur_depth:
                continue
            screen_node = RuntimeContent.get_instance().get_screen_map().get(screen_uid)
            if screen_node is not None:
                clickable_eles = screen_node.get_diff_or_clickable_eles()
                if clickable_eles is None or len(clickable_eles) == 0:
                    # print(f"深度{depth}: {screen_uid} 没有可点击组件")
                    continue
                snode_set.add(screen_node)

        for screen_node in snode_set:
            depth = screen_depth_map.get(screen_node.ck_eles_text)
            if cal_cov_map.get(depth, None) is None:
                cal_cov_map[depth] = [0, 0, 0]
            total_cnt = len(screen_node.get_diff_or_clickable_eles())
            click_cnt = screen_node.already_clicked_cnt

            candidate_click_cnt = 0
            for ele in screen_node.get_diff_or_clickable_eles():
                if ele in RuntimeContent.get_instance().already_click_eles:
                    candidate_click_cnt +=1

            cal_cov_map[depth][0] += click_cnt
            cal_cov_map[depth][1] += candidate_click_cnt
            cal_cov_map[depth][2] += total_cnt
        return cal_cov_map

    def print_coverage(self, cal_cov_map):
        depth_list = [depth for depth, cov_pair in sorted(cal_cov_map.items(), key=lambda x:x[0])]
        for depth in depth_list:
            LogUtils.log_info(f"层数{depth} 组件为个数 {cal_cov_map[depth][0]} {cal_cov_map[depth][1]} {cal_cov_map[depth][2]}覆盖率为 {cal_cov_map[depth][1]/cal_cov_map[depth][2]}")
        return cal_cov_map


    def to_string_result(self):
        assert (self.end_time != -1)
        diff_time = self.end_time - self.start_time
        return f"_restart{self.restart_cnt}activity{len(self.stat_activity_set)}&screen{len(self.stat_screen_set)}&time{round(diff_time, 2)}s"

    def get_stat_screen_set(self):
        return self.stat_screen_set

    def get_stat_activity_set(self):
        return self.stat_activity_set

    def get_total_eles_cnt(self):
        return self.total_eles_cnt

    def inc_restart_cnt(self):
        self.restart_cnt +=1

    def get_webview_set(self):
        return self.webview_set


