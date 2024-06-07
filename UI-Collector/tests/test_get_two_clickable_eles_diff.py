import sys
sys.path.append("..")
from utils.core_functions import *
import unittest


class TestGetTwoClickableElesDiff(unittest.TestCase):
    # csdn testcase1
    def test_case1(self):
        all_text = []
        d = Device()
        ele_uid_map = {}

        temp_screen_pkg, temp_activity, temp_all_text, temp_screen_info = get_screen_info(d)

        # print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}")
        last_eles, diff_len = get_merged_clickable_elements(d, ele_uid_map, temp_activity)
        print("last" + "*" * 50)
        print(len(last_eles))
        for idx, ele_id in enumerate(last_eles):
            # ele_dict = ele_uid_map[ele_id]
            # text = ele_dict.get("text")
            # print(f"{idx} - {text}")
            print(ele_id)
        # print(len(clickable_eles))
        # x, y = get_location(ele_uid_map[clickable_eles[27]])
        # d.click(x, y)

        d.press("back")
        time.sleep(3)
        cur_eles, diff_len = get_merged_clickable_elements(d, ele_uid_map, temp_activity)
        print("cur" + "*" * 50)
        print(len(cur_eles))
        for idx, ele_id in enumerate(cur_eles):
            # ele_dict = ele_uid_map[ele_id]
            # text = ele_dict.get("text")
            # print(f"{idx} - {text}")
            print(ele_id)

        isoverlap, diff_list = get_two_clickable_eles_diff(cur_eles, temp_activity, last_eles, temp_activity)
        print("diff" + "*" * 50)
        print(isoverlap)
        if isoverlap:
            print(len(diff_list))
            for idx, ele_id in enumerate(diff_list):
                # ele_dict = ele_uid_map[ele_id]
                # text = ele_dict.get("text")
                # print(f"{idx} - {text}")
                print(ele_id)

    # csdn testcase2
    # def test_case2(self):
    #     all_text = []
    #     d = Device()
    #     ele_uid_map = {}
    #
    #     temp_screen_pkg, temp_activity, temp_all_text, temp_screen_info = get_screen_info(d)
    #
    #     # print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}")
    #     last_eles, diff_len = get_merged_clickable_elements(d, ele_uid_map, temp_activity)
    #     print("last" + "*" * 50)
    #     print(len(last_eles))
    #     for idx, ele_id in enumerate(last_eles):
    #         ele_dict = ele_uid_map[ele_id]
    #         text = ele_dict.get("text")
    #         print(f"{idx} - {text}")
    #     # print(len(clickable_eles))
    #
    #     x, y = get_location(ele_uid_map[last_eles[3]])
    #     d.click(x, y)
    #     time.sleep(3)
    #     # d.press("back")
    #     cur_eles, diff_len = get_merged_clickable_elements(d, ele_uid_map, temp_activity)
    #     print("cur" + "*" * 50)
    #     print(len(cur_eles))
    #     for idx, ele_id in enumerate(cur_eles):
    #         ele_dict = ele_uid_map[ele_id]
    #         text = ele_dict.get("text")
    #         print(f"{idx} - {text}")
    #
    #     isoverlap, diff_list = get_two_clickable_eles_diff(cur_eles, temp_activity, last_eles, temp_activity)
    #     print("diff" + "*" * 50)
    #     print(isoverlap)
    #     if isoverlap:
    #         print(len(diff_list))
    #         for idx, ele_id in enumerate(diff_list):
    #             ele_dict = ele_uid_map[ele_id]
    #             text = ele_dict.get("text")
    #             print(f"{idx} - {text}")


if __name__ == '__main__':
    unittest.main()

