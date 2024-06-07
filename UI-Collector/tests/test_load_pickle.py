from utils.SavedInstanceUtils import *
from RuntimeContent import *
from uiautomator2 import Device

file = "../SavedInstance/com.cainiao.wireless_restart0activity2&screen4&time77.61s.pickle"
runtime = SavedInstanceUtils.load_pickle(file)
screen_map = runtime.get_screen_map()
first_screen_text = runtime.get_instance().get_first_screen_ck_eles_text()
first_screen_node = screen_map.get(first_screen_text)
# node_list = []
# for text, node in screen_map.items():
#     if "钱包" in text:
#         node_list.append(screen_map[text])
# print(first_screen_node.screen_text)
# call_map = first_screen_node.call_map
# for key, value in call_map.items():
#     print(value.already_clicked_cnt)
# print(first_screen_node.already_clicked_cnt)
