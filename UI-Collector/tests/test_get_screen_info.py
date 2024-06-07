import sys 
sys.path.append("..")
from utils.DeviceUtils import *



all_text = []
d = Device()
current_screen = d.app_current()
umap = {}
pkg_name, act_name, all_text = get_screen_info()
print(all_text)