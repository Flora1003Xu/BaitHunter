import unittest

from RuntimeContent import RuntimeContent
from StateChecker import check_pattern_state

class MyTestCase(unittest.TestCase):
    def test_something(self):
        r = RuntimeContent.get_instance()
        r.state_list = [1,2]
        res = check_pattern_state(2, [1,2])
        self.assertEqual(res, False)  # add assertion here

        r.state_list = [2,1,2,1]
        res = check_pattern_state(2, [1, 2])
        self.assertEqual(res, True)



if __name__ == '__main__':
    unittest.main()
