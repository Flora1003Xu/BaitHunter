import sys
sys.path.append("..")
from uiautomator2 import Device
import xml.etree.ElementTree as ET

def get_screen_all_clickable_text(d):
    text = ""
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            temp_text = element.get("text")
            if temp_text:
                text += temp_text + " "
                # print(temp_text)
            else:
                print(element.get("content-desc"))
    return text

all_text = []
d = Device()
umap = {}
get_screen_all_clickable_text(d)
