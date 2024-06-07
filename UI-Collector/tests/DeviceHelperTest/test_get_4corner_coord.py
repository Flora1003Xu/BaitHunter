import unittest
from unittest.mock import patch
from utils.DeviceUtils import get_4corner_coord

class TestGetCornerCoord(unittest.TestCase):
    @patch("utils.DeviceUtils.yolowxyh_to_uiautoxywh")
    def test_get_4corner_coord(self, yolowxyh_to_uiautoxywh_mock):
        yolowxyh_to_uiautoxywh_mock.return_value = [540.0, 1131.0, 540.0, 1131.0]
        res = get_4corner_coord([0.5, 0.5, 0.5, 0.5])
        ans = {'left_top': [540.0, 1131.0], 'right_top': [1080.0, 1131.0], 'left_bot': [540.0, 2262.0], 'right_bot': [1080.0, 2262.0]}
        self.assertEqual(res, ans)
        yolowxyh_to_uiautoxywh_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()