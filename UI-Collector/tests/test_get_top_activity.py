import sys 
sys.path.append("..")
from uiautomator2 import Device

d = Device()

top = get_top_activity(d)
cur = get_current_activity(d)
print(top)
print(cur)
print(cur in top)