from utils.DeviceUtils import get_clickable_eles_tree
from utils.DeviceUtils import get_dump_hierarchy
from uiautomator2 import Device
import unittest


class TestElesTree(unittest.TestCase):
    def test_case1(self):
        d = Device()
        xml_root = get_dump_hierarchy()
        res_list = []
        text_list = []
        get_clickable_eles_tree(xml_root, "", res_list, text_list)
        for text in text_list:
            print(text)
            print("*"*100)







if __name__ == '__main__':
    unittest.main()
