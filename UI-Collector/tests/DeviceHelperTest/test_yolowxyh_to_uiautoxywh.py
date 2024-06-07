import unittest
from unittest.mock import patch
from utils.DeviceUtils import yolowxyh_to_uiautoxywh

class TestYoloxywh(unittest.TestCase):
    @patch("utils.DeviceUtils.get_screen_wh")
    def test_yolowxyh_to_uiautoxywh(self, get_screen_wh_mock):
        get_screen_wh_mock.return_value = (1080, 2262)
        xywh = [0.5, 0.5, 0.5, 0.5]
        res = yolowxyh_to_uiautoxywh(xywh)
        self.assertEqual(res, [540.0, 1131.0, 540.0, 1131.0])
        get_screen_wh_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()