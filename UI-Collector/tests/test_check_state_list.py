import unittest


class TestCheckStateList(unittest.TestCase):
    def test_case1(self):
        state_list = [4, 4, 1, 2, 3, 4, 4, 4, 4, 4]
        self.assertTrue(check_state_list_reverse(5, state_list, 4))
        self.assertTrue(check_state_list_reverse(4, state_list, 4))
        state_list = [1,2,3,4,5]
        self.assertFalse(check_state_list_reverse(6, state_list, 3))
        state_list = [1, 2, 3, 4, 4, 4, 4, 4, 1, 4, 4]
        self.assertFalse(check_state_list_reverse(3, state_list, 4))
        self.assertFalse(check_state_list_reverse(4, state_list, 4))

if __name__ == '__main__':
    unittest.main()
