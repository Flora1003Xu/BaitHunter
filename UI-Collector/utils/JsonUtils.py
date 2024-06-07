import json
from RuntimeContent import *
from Config import *
from StatRecorder import *
import os

class JsonUtils:
    @classmethod
    def dump_screen_map_to_json(cls):
        file_name = cls.__get_json_file_path()
        screen_map = RuntimeContent.get_instance().get_screen_map()
        res_list = cls.__get_res_list_from_screenmap(screen_map)
        cls.__dump_to_json(file_name, res_list)

    @staticmethod
    def __get_json_file_path():
        config_path = Config.get_instance().get_collectDataPath()
        json_path = "Dumpjson"
        json_file_name = Config.get_instance().get_target_pkg_name() + StatRecorder.get_instance().to_string_result() + ".json"
        return os.path.join(config_path, json_path, json_file_name)

    @staticmethod
    def __dump_to_json(file_path:str, res_list:list):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'w', encoding='utf-8')
        json.dump(res_list, fw, ensure_ascii = False)
        fw.close()

    @classmethod
    def __get_res_list_from_screenmap(cls, screen_map) -> list:
        res_list = []
        for ck_eles_text, screen_node in screen_map.items():
            json_dict = {}
            json_dict["screen_text"] = screen_node.screen_text
            json_dict["ck_eles_text"] = screen_node.ck_eles_text
            json_dict["pkg_name"] = screen_node.pkg_name
            json_dict["activity_name"] = screen_node.activity_name
            if screen_node.get_diff_or_clickable_eles() is None:
                json_dict["len_clicked_cnt"] = 0
            else:
                json_dict["len_clicked_cnt"] = len(screen_node.get_diff_or_clickable_eles())
            json_dict["already_clicked_cnt"] = screen_node.already_clicked_cnt
            json_dict["max_clicked_cnt"] = screen_node.total_clicked_cnt
            json_dict["nextlist"] = cls.__get_nextlist(screen_node)
            # json_dict["call_map_list"] = cls.__get_callmap_list(screen_node)
            json_dict["call_map"] = cls.__get_callmap(screen_node)
            res_list.append(json_dict)
        # print(res_list)
        return res_list

    @staticmethod
    def __get_callmap_list(screen_node: ScreenNode)-> list:
        call_map_list = []
        for clickable_ele_uuid, call_screen_node in screen_node.call_map.items():
            call_map_list.append(call_screen_node.ck_eles_text)
        # print(call_map_list)
        return call_map_list

    @staticmethod
    def __get_callmap(screen_node: ScreenNode) -> dict:
        res_call_map = {}
        for ck_ele_uid, call_screen_node in screen_node.call_map.items():
            res_call_map[ck_ele_uid] = call_screen_node.ck_eles_text
        return res_call_map

    @staticmethod
    def __get_nextlist(screen_node: ScreenNode) -> list:
        nextlist = []
        for next in screen_node.children:
            nextlist.append(next.ck_eles_text)
        # print(nextlist)
        return nextlist

