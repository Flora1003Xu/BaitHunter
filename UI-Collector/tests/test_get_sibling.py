from utils.DeviceUtils import *

all_text = []
d = Device()
ele_uid_map = {}

def find_parent(node):
    return node.getparent()

# find all the siblings of a given node
def find_siblings(node):
    parent = find_parent(node)
    siblings = parent.findall('*')
    siblings.remove(node)
    return siblings




node = root = get_dump_hierarchy()
node = root.findall('我的')
siblings = find_siblings(node)
for sibling in siblings:
    print(sibling.tag, sibling.text)