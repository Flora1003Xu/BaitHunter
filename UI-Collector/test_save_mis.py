import sys
# sys.path.append('C:\\Codelife\\ui')
from utils.ScreenshotUtils import *
from Config import *
import time
from services.mislead_detector.save_mislead_file import save_mislead_file

# abs_path = "collectData\com.alibaba.aliyun-20231202-003938\Screenshot\ScreenshotPicture"
# from_img = "0IfqneiOmh6xX4VulvUwX41EwIHFKt4C7TNY3BWX53o=.png"
# to_img = "0UGIAyuB3G077ow6mMUnRMnQyYLdmz2ZHFhLjUi1prY=.png"
# click_xy = (255, 255)
# res = save_mislead_file.save_mislead_file(abs_path, from_img, to_img, click_xy)

# abs_path = "collectData\com.xyn.wskai-20231215-180448"
# from_img = "collectData\com.xyn.wskai-20231215-180448\Screenshot\ScreenshotPicture\RUD64XKqKj-ETda_HzVx5zIXZG8YOVusZ38MWYX58TM=.png"
# abs_path = "collectData\com.xyn.wskai-20231215-174746"
# from_img = "collectData\com.xyn.wskai-20231215-174746\Screenshot\ScreenshotPicture\RUD64XKqKj-ETda_HzVx5zIXZG8YOVusZ38MWYX58TM=.png"
# to_img = from_img
# click_xy = (255, 255)
# res = save_mislead_file.save_mislead_file(abs_path, from_img, to_img, click_xy)

ck_eles_text = "fuaaa"
screenshot_path = ScreenshotUtils.screen_shot(ck_eles_text)
time.sleep(10)
save_mislead_file(Config.get_instance().get_collectDataPath(), screenshot_path, screenshot_path, (1, 2))

# assert res is not None