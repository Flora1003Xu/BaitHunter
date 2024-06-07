from ScreenNode import ScreenNode
import unittest

class TestUpdateCallMap(unittest.TestCase):
    def test_case1(self):
        A = ScreenNode()
        B = ScreenNode()
        C = ScreenNode()
        A.call_map["a"] = B
        A.call_map["c"] = C
        print(A.call_map)
        A.update_callmap_item("a")
        print(A.call_map)

if __name__ == '__main__':
    unittest()
