from StateChecker import check_pattern_state2
import unittest

class TestCheckFinishState(unittest.TestCase):
    def test_case1(self):
        k = 10
        exception_states = [4, 6, 8]
        state_list = [4, 6, 8, 4, 6, 8, 4, 6, 8, 4, 6, 8]
        self.assertTrue(check_pattern_state2(k, exception_states))

        state_list = [4, 6, 8, 4, 6, 8, 4, 6, 8, 1, 4, 6, 8]
        self.assertFalse(check_pattern_state2(k, exception_states))

        state_list = [4, 6, 8, 4, 6, 8, 4, 4, 4, 4, 4, 4, 4, 8]
        self.assertTrue(check_pattern_state2(k, exception_states))


if __name__ == "__main__":
    unittest.main()
