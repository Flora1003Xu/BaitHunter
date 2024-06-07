import sys
sys.path.append("..")
from FSM import *
from utils.core_functions import *


def press_back():
    d.press("back")
    print("进行回退")
    time.sleep(5)
    return

all_text = []
d = Device()
ele_uid_map = {}
press_back()
while True:
    press_back()