import unittest


class TestCheckScreenList(unittest.TestCase):
    def test_case1(self):
        screen_list = [1, 1, 1, 1, 1, 2]
        self.assertTrue(check_screen_list_order(3, screen_list))
        screen_list = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 6, 6, 6]
        self.assertTrue(check_screen_list_order(3, screen_list))
        self.assertTrue(check_screen_list_order(4, screen_list))
        self.assertTrue(check_screen_list_order(5, screen_list))
        screen_list = [1, 2, 1, 2, 1]
        self.assertFalse(check_screen_list_order(3, screen_list))
        screen_list = [1, 2, 3, 1, 2, 3, 1, 2, 3, 3, 2, 1]
        self.assertTrue(check_screen_list_order(3, screen_list))
        self.assertFalse(check_screen_list_order(4, screen_list))
        screen_list = [1, 2, 2, 1, 1, 2, 1, 2, 1, 2]
        self.assertFalse(check_screen_list_order(2, screen_list))

    def test_case2(self):
        screen_list = [1, 1, 1, 1, 1, 2]
        screen_list.reverse()
        self.assertTrue(check_screen_list_reverse(3, screen_list))
        screen_list = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 6, 6, 6]
        screen_list.reverse()
        self.assertTrue(check_screen_list_reverse(3, screen_list))
        self.assertTrue(check_screen_list_reverse(4, screen_list))
        self.assertTrue(check_screen_list_reverse(5, screen_list))
        screen_list = [1, 2, 1, 2, 1]
        screen_list.reverse()
        self.assertFalse(check_screen_list_reverse(3, screen_list))
        screen_list = [1, 2, 3, 1, 2, 3, 1, 2, 3, 3, 2, 1]
        screen_list.reverse()
        self.assertTrue(check_screen_list_reverse(3, screen_list))
        self.assertFalse(check_screen_list_reverse(4, screen_list))
        screen_list = [1, 2, 2, 1, 1, 2, 1, 2, 1, 2]
        screen_list.reverse()
        self.assertFalse(check_screen_list_reverse(2, screen_list))

    def test_case3(self):
        screen_list = ["b", "a", "a", "a", "a", "a"]
        self.assertTrue(check_screen_list_reverse(3, screen_list))


if __name__ == '__main__':
    unittest.main()
