import sys 
sys.path.append("..")
from uiautomator2 import Device

all_text = []
d = Device()
umap = {}

temp_screen_pkg, temp_activity, temp_all_text, temp_screen_info = get_screen_info(d)

clickable_eles, _ = get_merged_clickable_elements(d, umap, temp_activity)


# print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}")


# x, y = get_location(clickable_eles[8])
# d.click(x, y)
print(len(clickable_eles))
for idx, ele in enumerate(clickable_eles):
    uid = get_unique_id(d, ele, temp_activity)
    print(uid) 
    if idx == 6:
        print(uid) 
        x, y = get_location(ele)
        print(x, y)
        d.click(x, y)
        # time.sleep(3)