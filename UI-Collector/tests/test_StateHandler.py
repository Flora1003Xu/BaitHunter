import unittest
from StateHandler import StateHandler

class TestStateHandler(unittest.TestCase):
    def test_print_state(self):
        StateHandler.print_state(3)
        StateHandler.print_state(4)

if __name__ == "__main__":
    unittest.main()