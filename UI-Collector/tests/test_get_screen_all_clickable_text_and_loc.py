import sys
sys.path.append("..")
from uiautomator2 import Device
from utils.DeviceUtils import get_screen_all_clickable_text_and_loc

all_text = []
d = Device()
umap = {}
print(get_screen_all_clickable_text_and_loc(d))