from ScreenNode import ScreenNode
import unittest

class TestBuildCandidate(unittest.TestCase):
    def test_case1(self):
        A = ScreenNode()
        B = ScreenNode()
        A.cycle_set.add("aa")
        A.call_map["ab"] = B
        A.cycle_set.add("ac")
        res = A.build_candidate_random_clickable_eles()
        print(res)



if __name__ == "__main__":
    unittest.main()