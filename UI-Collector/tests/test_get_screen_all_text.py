import sys 
sys.path.append("..")
from uiautomator2 import Device

all_text = []
d = Device()
umap = {}
print(get_screen_all_clickable_text(d))
