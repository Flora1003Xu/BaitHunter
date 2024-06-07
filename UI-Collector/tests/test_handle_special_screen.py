import sys
sys.path.append("..")
from FSM import  *

def handle_special_screen():
    #TODO
    print("可能产生了不可去掉的框")
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info()
    clickable_eles, res_merged_diff = merged_clickable_elements()
    choose = random.randint(0, len(clickable_eles) - 1)
    cur_clickable_ele_uid = clickable_eles[choose]
    cur_clickable_ele_dict = ele_uid_map[cur_clickable_ele_uid]
    loc_x, loc_y = get_location(cur_clickable_ele_dict)
    d.click(loc_x, loc_y)

if __name__ == "__main__":
    d = Device()
    ele_uid_map = {}
    handle_special_screen()
