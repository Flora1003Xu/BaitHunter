import unittest
from StateChecker import check_pattern_screen
from RuntimeContent import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        r = RuntimeContent.get_instance()
        r.screen_list = [1,2,1,2,1,2]
        res = check_pattern_screen(3, 2)
        self.assertEqual(res, True)  # add assertion here

        r.state_list = [2,1,2,1]
        res = check_pattern_screen(2, 1)
        self.assertEqual(res, False)



if __name__ == '__main__':
    unittest.main()
