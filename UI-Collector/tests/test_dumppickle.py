from utils.SavedInstanceUtils import *
from RuntimeContent import *
from uiautomator2 import Device

a = RuntimeContent.get_instance()
a.set_first_screen_ck_ele_text("nihao")
a.device = Device()
SavedInstanceUtils.dump_pickle(a)
print(RuntimeContent.get_instance())
b = SavedInstanceUtils.load_pickle()
print(b)
print(b.first_screen_ck_eles_text)
# print(RuntimeContent.get_instance())
# print(a)
# print()
# print(b)