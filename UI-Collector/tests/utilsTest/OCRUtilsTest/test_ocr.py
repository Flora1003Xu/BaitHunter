from utils.DeviceUtils import *
from utils.OCRUtils import *
from utils.ScreenshotUtils import *
pp_text_dict = get_privacy_policy_ele_dict()
if len(pp_text_dict)>0:
    print(pp_text_dict)
else:
    print("不存在")

path = ScreenshotUtils.screen_shot("aaaa")
print(path)
for pp_text, pp_text_cnt in pp_text_dict.items():
    ans = cal_privacy_ele_loc(path, pp_text, pp_text_cnt)
    print(ans)

