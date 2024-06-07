from utils.core_functions import *
from utils.ScreenCompareStrategy import *
import unittest


class TestCheckCycle(unittest.TestCase):
    def test_case1(self):
        s1 = ScreenNode()
        s1.ck_eles_text = "1"
        s2 = ScreenNode()
        s2.ck_eles_text = "2"
        s1.add_child(s2)
        s2.add_child(s1)
        lcs_comp = ScreenCompareStrategy(LCSComparator())
        s1.call_map["a"] = s2

        self.assertFalse(check_cycle(s2, s1))

        s2.call_map["aa"] = s1
        self.assertTrue(check_cycle(s1, s2))
        self.assertTrue(check_cycle(s2, s1))

    def test_case2(self):
        s1 = ScreenNode()
        s1.ck_eles_text = "1"
        s2 = ScreenNode()
        s2.ck_eles_text = "2"
        s3 = ScreenNode()
        s3.ck_eles_text = "3"
        s4 = ScreenNode()
        s4.ck_eles_text = "4"
        lcs_comp = ScreenCompareStrategy(LCSComparator())
        s1.add_child(s2)
        s2.add_child(s3)
        s3.add_child(s4)
        s4.add_child(s1)
        s1.call_map["a"] = s2
        s2.call_map["a"] = s3
        s3.call_map["a"] = s4
        s4.call_map["a"] = s1
        self.assertTrue(check_cycle(s1, s4))
        del s4.call_map["a"]
        self.assertFalse(check_cycle(s3, s2))
        self.assertFalse(check_cycle(s2, s1))
        self.assertFalse(check_cycle(s4, s3))


if __name__ == '__main__':
    unittest.main()
