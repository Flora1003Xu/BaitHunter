from StatRecorder import StatRecorder
import unittest

class TestStatRecorder(unittest.TestCase):
    def test_case1(self):
        A = StatRecorder.get_instance()
        B = StatRecorder.get_instance()
        C = StatRecorder.get_instance()
        self.assertTrue(A is B)
        self.assertTrue(A is C)
        self.assertTrue(B is C)

    def test_case2(self):
        A = StatRecorder.get_instance()
        B = StatRecorder.get_instance()
        A.inc_total_ele_cnt()
        A.set_start_time()
        A.add_stat_stat_activity_set("ac1")
        A.add_stat_stat_activity_set("ac2")
        A.add_stat_screen_set("sc1")
        A.add_stat_screen_set("sc2")
        self.assertEqual(1, A.get_total_eles_cnt())
        self.assertEqual({"sc1", "sc2"}, A.get_stat_screen_set())
        self.assertEqual({"ac1", "ac2"}, A.get_stat_activity_set())
        B.print_result()


if __name__ == "__main__":
    unittest.main()