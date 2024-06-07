import sys
sys.path.append("..")
from uiautomator2 import Device

all_text = []
d = Device()
ele_uid_map = {}

temp_screen_pkg, temp_activity, temp_all_text, temp_screen_info = get_screen_info(d)

clickable_eles = get_clickable_elements(d, ele_uid_map, temp_activity)


print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}")


for idx, ele_id in enumerate(clickable_eles):
    ele_dict = ele_uid_map[ele_id]
    text = ele_dict.get("text")
    print(f"{idx} - {text}")

#
# x, y = get_location(ele_uid_map[clickable_eles[1]])

d.press("back")
# d.press("back")