from utils.DeviceUtils import get_clickable_eles_tree
from utils.DeviceUtils import get_xml_root
from utils.DeviceUtils import build_hierarchy
from uiautomator2 import Device
import unittest
from utils.DeviceUtils import print_ui_root

class TestElesTree(unittest.TestCase):
    def test_case2(self):
        text_list = ["b", "c&", "ab&cd", "a&bc", "ab&d", "a&d&a", "a&d&z&"]
        ui_root = build_hierarchy(text_list)
        print_ui_root(ui_root, 1)

    def test_case1(self):
        d = Device()
        xml_root = get_xml_root()
        res_list = []
        text_list = []
        get_clickable_eles_tree(xml_root, "", res_list, text_list)
        # print(res_list)
        for text in text_list:
            print(text)
            print("*"*100)
        # print(len(text_list))
        ui_root = build_hierarchy(text_list)
        print_ui_root(ui_root, 1)

if __name__ == '__main__':
    unittest.main()
