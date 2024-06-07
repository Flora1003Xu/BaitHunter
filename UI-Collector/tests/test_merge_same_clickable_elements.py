import sys 
sys.path.append("..")
from uiautomator2 import Device

# k = 6
# clickable_eles = [1,2,3,4,4,4,5,5,5,7,7,7,7,7,7,7,7,7,10,10,10,2,3,3,3,3,3,3,3,3,3,3,1]
# res = merge_same_clickable_elements(k, clickable_eles)
# print(res)


# k = 2
# clickable_eles = [1,2,3,4,4,4,5,5,5,7,7,7,7,7,7,7,7,7,10,10,10,2,3,3,3,3,3,3,3,3,3,3,1]
# res = merge_same_clickable_elements(k, clickable_eles)
# print(res)


# k = 2
# clickable_eles = [1,2,3,4,4,5,5,7,7,7,7,7,7,7,7,7,10,10,10,2,3,3,3,3,3,3,3,3,3,3,1]
# res = merge_same_clickable_elements(k, clickable_eles)
# print(res)


all_text = []
d = Device()
umap = {}

temp_screen_pkg, temp_activity, temp_all_text, temp_screen_info = self.target_pkg_name(d)

clickable_eles = get_clickable_elements(d, umap, temp_activity)
# print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}")

for ele in clickable_eles:
    print(ele)



merged_clickable_eles, diff = get_merged_clickable_elements(d, umap, temp_activity)
print("*"*100)
print(f"合并后减少了{diff}")
for ele in merged_clickable_eles:
    print(ele)