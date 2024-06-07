from utils.DeviceUtils import *

all_text = []
d = Device()
ele_uid_map = {}


cur_ck_eles = get_clickable_elements()
print(len(cur_ck_eles))
for idx, ele_id in enumerate(cur_ck_eles):
    print(f"{idx}--{ele_id}")
cur_ck_eles = remove_dup(cur_ck_eles)
cur_ck_eles = merged_clickable_elements(cur_ck_eles)
print(len(cur_ck_eles))
for idx, ele_id in enumerate(cur_ck_eles):
    print(f"{idx}--{ele_id}")