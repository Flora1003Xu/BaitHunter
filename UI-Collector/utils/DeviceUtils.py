import xml.etree.ElementTree as ET
import re
from RuntimeContent import *
from RuntimeContent import RuntimeContent
from UITreeNode import *
from Config import *
from utils.LogUtils import LogUtils
from utils.OCRUtils import cal_privacy_ele_loc
from utils.ScreenshotUtils import *
from services.mislead_detector.check_is_mislead import check_is_mislead_text

system_view = [
    "com.android.systemui",
    "com.android.launcher",
    "com.google.android.apps.nexuslauncher",
    "com.android.settings",
    "com.google.android.googlequicksearchbox",
    "com.google.android.gms",
    "com.google.android.inputmethod.latin",
    "com.android.chrome"
]


def get_screen_content():
    cur_screen_pkg_name = get_screen_package()
    cur_activity = get_screen_activity()
    screen_text = get_screen_text()

    # 防止页面变化过快没有提取到界面元素
    retry_cnt = 3
    for i in range(0, retry_cnt):
        cur_ck_eles = get_clickable_elements()
        if cur_ck_eles is not None and len(cur_ck_eles) > 0:
            break

    pre_len = len(cur_ck_eles)
    cur_ck_eles = remove_false_loc(cur_ck_eles)
    cur_ck_eles = remove_dup(cur_ck_eles)
    cur_ck_eles = merged_clickable_elements(cur_ck_eles)
    after_len = len(cur_ck_eles)

    if Config.get_instance().ScreenUidRep == "textloc":
        ck_eles_text = to_textloc_ck_eles(cur_ck_eles)
    elif Config.get_instance().ScreenUidRep == "loc":
        ck_eles_text = to_loc_ck_eles(cur_ck_eles)
    else:
        raise Exception("ScreenUid表示方式输入有误")

    # 截图
    screenshot_path = ScreenshotUtils.screen_shot(ck_eles_text)

    # if RuntimeContent.get_instance().get_first_screen_ck_eles_text() is None:
    #     RuntimeContent.get_instance().set_first_screen_ck_ele_text(ck_eles_text)
    last_screen_node = RuntimeContent.get_instance().get_last_screen_node()
    if last_screen_node is not None and last_screen_node.ck_eles_text == "root":
        RuntimeContent.get_instance().set_first_screen_ck_ele_text(ck_eles_text)

    content = {}
    content["cur_screen_pkg_name"] = cur_screen_pkg_name
    content["cur_activity"] = cur_activity
    content["ck_eles_text"] = ck_eles_text
    content["screen_text"] = screen_text
    content["cur_ck_eles"] = cur_ck_eles
    content["merged_diff"] = pre_len - after_len
    content["screenshot_path"] = screenshot_path
    return content


def get_ck_eles_hierarchy() -> list:
    xml_root = get_dump_hierarchy()
    text_list = []
    get_clickable_eles_tree(xml_root, "", text_list)
    ui_root = build_hierarchy(text_list)
    res = to_string_hierarchy(ui_root, 1)
    return res


def get_dump_hierarchy():
    d = Config.get_instance().get_device()
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    return root


def get_clickable_eles_tree(node, text, text_list: list):
    if node is None:
        return
    if text:
        text += "&"
    if node.get("class"):
        text += node.get("class")
    if node.get("resource-id"):
        text += node.get("resource-id")

    if node.get('clickable') == 'true' and node.get("package") not in system_view and is_child_clickable(node) == False:
        temp_text = node.get("text")
        if not temp_text:
            temp_text = traverse_tree(node)
        text += "@" + temp_text
        text_list.append(text)
        return
    for child in node:
        get_clickable_eles_tree(child, text, text_list)


def build_hierarchy(text_list) -> UITreeNode:
    root = UITreeNode("root")
    root.isDir = True
    tmp = ""
    for text in text_list:
        cur = root
        for i in range(len(text) + 1):
            if i < len(text) and text[i] == "&":
                flag = False
                for child in cur.childs:
                    if child.name == tmp and child.isDir:
                        cur = child
                        flag = True
                        break
                if not flag:
                    newChild = UITreeNode(tmp)
                    newChild.isDir = True
                    cur.childs.append(newChild)
                    cur = newChild
                tmp = ""
            elif i == len(text):
                if tmp != "":
                    newChild = UITreeNode(tmp)
                    newChild.isDir = False
                    cur.childs.append(newChild)
                tmp = ""
            else:
                tmp += text[i]
    return root


def to_string_hierarchy(root: UITreeNode, level=1) -> str:
    if root is None:
        return ""
    str = ""
    for i in range(level - 1):
        str += "  "
    str += "--"
    str += root.name + "\n"
    root.childs = sorted(root.childs)
    for child in root.childs:
        str += to_string_hierarchy(child, level + 1)
    return str


def print_ui_root(root: UITreeNode, level=1):
    if root is None:
        return
    for i in range(level - 1):
        print("  ", end="")
    print("--", end="")
    print(root.name)
    root.childs = sorted(root.childs)
    for child in root.childs:
        print_ui_root(child, level + 1)


# screen_info = package_name + activity_name + screen_all_text
def get_screen_info():
    d = Config.get_instance().get_device()
    current_screen = d.current_app()
    pkg_name = current_screen['package']
    act_name = current_screen['activity']
    ck_eles_text = get_screen_all_clickable_text_and_loc(d)
    return pkg_name, act_name, ck_eles_text


def get_device_info():
    d = Config.get_instance().get_device()
    return d.info


def get_screen_wh():
    d = Config.get_instance().get_device()
    wsize = d.window_size()
    screen_w, screen_h = wsize[0], wsize[1]
    return screen_w, screen_h


def get_display_screen_wh():
    d = Config.get_instance().get_device()
    screen_w, screen_h = d.info['displayWidth'], d.info['displayHeight']
    return screen_w, screen_h


def yolowxyh_to_uiautoxywh(xywh):
    screen_w, screen_h = get_screen_wh()
    ui_x = screen_w * xywh[0]
    ui_w = screen_w * xywh[2]
    ui_y = screen_h * xywh[1]
    ui_h = screen_h * xywh[3]
    return [ui_x, ui_y, ui_w, ui_h]


def get_4corner_coord(xywh):
    ui_xywh = yolowxyh_to_uiautoxywh(xywh)
    LogUtils.log_info(f"xywh转换前{xywh}--->转换后: {ui_xywh}")
    l, top = ui_xywh[0] - ui_xywh[2] / 2, ui_xywh[1] - ui_xywh[3] / 2
    r, bottom = ui_xywh[0] + ui_xywh[2] / 2, ui_xywh[1] + ui_xywh[3] / 2
    return l, top, r, bottom


# 获取当前界面所有的可点击组件的文本内容，如果该节点可点但没有文本
# 那大概率文本存在其子节点上
def get_screen_all_clickable_text(d):
    text = ""
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                temp_text = element.get("text")
                if temp_text:
                    text += temp_text + " "
                    # print(temp_text)
                else:
                    text += traverse_tree(element)
    return text


def check_cover_full_screen(d):
    dw, dh = get_display_screen_wh()
    first_layer_eles = d(className="android.widget.FrameLayout", instance=0)
    first_layer = first_layer_eles.info['visibleBounds']
    # 打印第一层元素的信息
    l, top, r, bottom = first_layer['left'], first_layer['top'], first_layer['right'], first_layer['bottom']
    if dw == r and dh == bottom and l==0 and top==0:
        return None
    return l, top, r, bottom



# 递归遍历节点的所有子节点
def traverse_tree(node):
    text = ""
    if node is None:
        return text
    if node.get("text"):
        text += node.get("text")
        # print(node.get("text"))
        return text
    for child in node:
        text += traverse_tree(child)
    return text


def get_screen_all_clickable_text_and_loc(d):
    text = ""
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                if is_child_clickable(element) == True:
                    continue
                temp_text = element.get("text")
                loc_x, loc_y = get_location_from_xmlele(element)
                if temp_text:
                    # 只取前10个字符，节省LCS算法计算的时间
                    if len(temp_text) > 10:
                        temp_text = temp_text[0:10]
                    text += "&" + temp_text + " " + str(loc_x) + " " + str(loc_y)
                    # print(temp_text)
                else:
                    text += "&" + traverse_tree_text_and_loc(element) + " " + str(loc_x) + " " + str(loc_y)
    return text


def traverse_tree_text_and_loc(node):
    text = ""
    if node is None:
        return text
    temp_text = node.get("text")
    if temp_text:
        if len(temp_text) > 10:
            temp_text = temp_text[0:10]
        # loc_x, loc_y = get_location_from_xmlele(node)
        # text += "--" + temp_text + " " + str(loc_x) + " " + str(loc_y)
        text += temp_text
        return text
    for child in node:
        text += traverse_tree_text_and_loc(child)
    return text


def to_textloc_ck_eles(ck_eles) -> str:
    text = ""
    for ele_uid in ck_eles:
        ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(ele_uid)
        temp_text = ele_dict.get("text")
        if len(temp_text) > 10:
            temp_text = temp_text[0:10]
        loc_x, loc_y = get_location(ele_dict)
        text += "&" + temp_text + " " + str(loc_x) + " " + str(loc_y)
    return text


def to_loc_ck_eles(ck_eles) -> str:
    text = ""
    for ele_uid in ck_eles:
        ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(ele_uid)
        loc_x, loc_y = get_location(ele_dict)
        text += str(loc_x) + " " + str(loc_y) + "-"
    return text


# 获取当前界面所有可点击的组件
def get_clickable_elements():
    activity_name = get_screen_activity()
    root = get_dump_hierarchy()
    clickable_elements = []
    # cnt = 0
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                if is_child_clickable(element) == True:
                    continue
                clickable_ele_dict = get_dict_clickable_ele(element, activity_name)
                uid = get_unique_id(clickable_ele_dict, activity_name)
                RuntimeContent.get_instance().put_ele_uid_map(uid, clickable_ele_dict)

                # 把误导性组件增加到前面
                clickable_elements.append(uid)

                # # 把有隐私的组件增加到前面
                # if is_privacy_information_in_ele_dict(clickable_ele_dict):
                #     clickable_elements.insert(0, uid)
                # else:
                #     clickable_elements.append(uid)
    return clickable_elements


def remove_false_loc(cur_ck_eles):
    w, h = get_display_screen_wh()
    ans = []
    for uid in cur_ck_eles:
        cur_screen_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(uid)
        loc_x, loc_y = get_location(cur_screen_ele_dict)
        if loc_x >=0 and loc_x<=w and loc_y>=0 and loc_y<=h:
            ans.append(uid)
    return ans


def remove_dup(old_list) -> list:
    return list(dict.fromkeys(old_list))


# 只有可点的最细化节点可以当成clickable_ele
def is_child_clickable(node) -> bool:
    if node is None:
        return False
    for child in node:
        if child.get('clickable') == 'true':
            return True
        if is_child_clickable(child) == True:
            return True
    return False


# 进行合并,对于选择国家和地区的场景,进行优化
def merged_clickable_elements(clickable_eles):
    k = 6
    if len(clickable_eles) < 6:
        return clickable_eles
    merged_clickable_eles = merge_same_clickable_elements_col(k, clickable_eles)
    merged_clickable_eles = merge_same_clickable_elements_row(k, merged_clickable_eles)

    return merged_clickable_eles

def is_mislead_text_in_ele_dict(clickable_ele_dict):
    text = clickable_ele_dict["text"]
    if text == "" or len(text) == 0:
        return False
    return check_is_mislead_text(text)


def is_privacy_information_in_ele_dict(clickable_ele_dict):
    text = clickable_ele_dict["text"]
    single_word_privacy_information = ["我", "我的", "编辑资料", "编辑材料", "隐私政策", "隐私权政策"]
    for sip_info in single_word_privacy_information:
        if sip_info == text:
            return True

    privacy_information = ["设置", "账号", "个人", "认证", "我的", "隐私", "用户", "登录"]
    for p_info in privacy_information:
        if p_info in text:
            return True
    return False


# 优化: 若clickable_eles中存在连续k个相同的ele,合并为1个,不用每个都点击
def merge_same_clickable_elements_col(k, clickable_eles: list) -> list:
    l = 0
    r = 0
    cnt = 0
    res = []
    while l < len(clickable_eles):
        cnt = 1
        r = l + 1
        while r < len(clickable_eles):
            if is_same_two_clickable_eles_col(clickable_eles[l], clickable_eles[r]):
                cnt += 1
                r += 1
            else:
                break
        if cnt > k:
            res.append(clickable_eles[l])
        else:
            for i in range(cnt):
                res.append(clickable_eles[l])
                l += 1
        l = r
    return res


def merge_same_clickable_elements_row(k, clickable_eles: list) -> list:
    l = 0
    r = 0
    cnt = 0
    res = []
    while l < len(clickable_eles):
        cnt = 1
        r = l + 1
        while r < len(clickable_eles):
            if is_same_two_clickable_eles_row(clickable_eles[l], clickable_eles[r]):
                cnt += 1
                r += 1
            else:
                break
        if cnt > k:
            res.append(clickable_eles[l])
        else:
            for i in range(cnt):
                res.append(clickable_eles[l])
                l += 1
        l = r
    return res


def is_same_two_clickable_eles_row(ele1_uid, ele2_uid) -> bool:
    if isinstance(ele1_uid, int) and isinstance(ele2_uid, int):
        return ele1_uid == ele2_uid
    else:
        ele1_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(ele1_uid)
        ele2_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(ele2_uid)

        class_name1 = ele1_dict.get("class")
        res_id1 = ele1_dict.get("resource-id")
        pkg_name1 = ele1_dict.get("package")
        loc_x1, loc_y1 = get_location(ele1_dict)

        class_name2 = ele2_dict.get("class")
        res_id2 = ele2_dict.get("resource-id")
        pkg_name2 = ele2_dict.get("package")
        loc_x2, loc_y2 = get_location(ele2_dict)

        if class_name1 == class_name2 and \
                res_id1 == res_id2 and pkg_name1 == pkg_name2 and loc_y1 == loc_y2:
            return True
        else:
            return False


def is_same_two_clickable_eles_col(ele1_uid, ele2_uid) -> bool:
    if isinstance(ele1_uid, int) and isinstance(ele2_uid, int):
        return ele1_uid == ele2_uid
    else:
        ele1_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(ele1_uid)
        ele2_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(ele2_uid)

        class_name1 = ele1_dict.get("class")
        res_id1 = ele1_dict.get("resource-id")
        pkg_name1 = ele1_dict.get("package")
        loc_x1, loc_y1 = get_location(ele1_dict)

        class_name2 = ele2_dict.get("class")
        res_id2 = ele2_dict.get("resource-id")
        pkg_name2 = ele2_dict.get("package")
        loc_x2, loc_y2 = get_location(ele2_dict)

        if class_name1 == class_name2 and \
                res_id1 == res_id2 and pkg_name1 == pkg_name2 and loc_x1 == loc_x2:
            return True
        else:
            return False


# get uid from element(dict)
def get_unique_id(ele_dict, activity_name):
    class_name = ele_dict.get("class")
    res_id = ele_dict.get("resource-id")
    pkg_name = ele_dict.get("package")
    text = ele_dict.get("text")
    loc_x, loc_y = get_location(ele_dict)
    uid = activity_name + "-" + pkg_name + "-" + class_name + "-" + res_id + "-" + "(" + str(loc_x) + "," + str(
        loc_y) + ")" + "-" + text
    return uid


def get_dict_clickable_ele(clickable_ele, activity_name):
    clickable_ele_dict = {}
    clickable_ele_dict["class"] = clickable_ele.get("class")
    clickable_ele_dict["resource-id"] = clickable_ele.get("resource-id")
    clickable_ele_dict["package"] = clickable_ele.get("package")

    temp_text = clickable_ele.get("text")
    if temp_text:
        clickable_ele_dict["text"] = temp_text
    else:
        temp_text = traverse_tree(clickable_ele)
        if temp_text:
            clickable_ele_dict["text"] = temp_text
        else:
            clickable_ele_dict["text"] = clickable_ele.get("content-desc")
    clickable_ele_dict["bounds"] = clickable_ele.get('bounds')
    return clickable_ele_dict


# def get_uid(ele, d, umap, cur_activity):
#     uid = get_unique_id(ele, d, cur_activity)
#     cnt = umap.get(uid)
#     uid = uid + "&&&" + str(cnt)
#     return uid

# def get_uid_cnt(uid):
#     # print(uid)
#     start = uid.find("&&&")
#     res = ""
#     if start != -1:
#         res = uid[start+3 : ]
#     return int(res)

# 获取页面的坐标
def get_location(ele_dict: dict):
    bounds = ele_dict.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2
    return x, y


def get_location_from_xmlele(element):
    bounds = element.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2
    return x, y


# 不全，没有resoure-id
def print_current_window_all_clickable_elements(d):
    clickable_elements = d(clickable=True)
    for ele in clickable_elements:
        print(ele.info.get('text'))


def get_screen_package():
    d = Config.get_instance().get_device()
    current_app = d.current_app()
    return current_app['package']


def get_screen_activity():
    d = Config.get_instance().get_device()
    current_app = d.current_app()
    return current_app["activity"]


def get_top_activity(d):
    output = d.shell("dumpsys window | grep mCurrentFocus").output
    pattern = r"{(.*)}"
    # Using re.search() to find the first occurrence of the pattern in the string
    match = re.search(pattern, output)

    # If a match is found, print the matched substring
    if match:
        return match.group(1)
    else:
        return None


def print_current_window_detailed_elements(d):
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    clickable_elements = []
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                clickable_elements.append(element)
    for element in clickable_elements:
        print(ET.tostring(element))
        print("*" * 100)
    print("*" * 100)
    print(len(clickable_elements))
    bounds = element.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2


def get_screen_text():
    """
    Get all text of the current Screen, including the non-clickable and clickable elements
    :return: all text of current Screen
    """
    # root = get_dump_hierarchy()
    # text = ""
    # for element in root.findall('.//node'):
    #     if element.get("package") in system_view:
    #         continue
    #     temp_text = element.get("text")
    #     if temp_text:
    #         if text == "":
    #             text += temp_text
    #         else:
    #             text += "," + temp_text
    # return text
    return ""


def get_privacy_policy_ele_dict():
    """
    :return: 隐私政策文本关键词出现的个数dict, dict{key:关键词, val:出现的个数}
    """
    root = get_dump_hierarchy()
    pp_text_list = Config.get_instance().privacy_policy_text_list
    res_pp_dict = dict()
    for element in root.findall('.//node'):
        if element.get("package") in system_view:
            continue
        # 不需要clickable=True, 因为即使为True也可能产生位置偏移导致点不到的问题
        # if element.get('clickable') == 'true':
        #     continue
        temp_text = element.get("text")
        if not temp_text:
            continue
        for pp_text in pp_text_list:
            if pp_text in temp_text:
                if not res_pp_dict.get(pp_text, False):
                    res_pp_dict[pp_text] = 1
                else:
                    res_pp_dict[pp_text] += 1

    return res_pp_dict


# # 对screen_info进行sha256签名,生成消息摘要
# def get_signature(screen_info):
#     signature = hashlib.sha256(screen_info.encode()).hexdigest()
#     return signature


# uid
# activity + pkg + class + resourceId + text
# get uid from element(object)
# def get_unique_id(d, ele, activity_name):
#     class_name = ele.get("class")
#     res_id = ele.get("resource-id")
#     pkg_name = ele.get("package")
#     text = ""
#     temp_text = ele.get("text")
#     if temp_text:
#         text = temp_text
#     else:
#         text = traverse_tree(ele)
#
#     loc_x, loc_y = get_location(ele)
#     uid = activity_name + "-" +pkg_name + "-" + class_name + "-" +res_id + "-" + "(" + str(loc_x) + "," + str(loc_y) + ")" + "-" + text
#     return uid
def get_cur_screen_node_from_context(content):
    cur_screen_node = content["cur_screen_node"]
    return cur_screen_node


def get_screen_text_from_context(content):
    return content["screen_text"]


def get_screen_info_from_context(content):
    cur_screen_pkg_name = content["cur_screen_pkg_name"]
    cur_activity = content["cur_activity"]
    ck_eles_text = content["ck_eles_text"]

    return cur_screen_pkg_name, cur_activity, ck_eles_text


def add_if_privacy_eles(content):
    # 如果已经找到了隐私政策url
    cur_activity = content["cur_activity"]
    cur_screen_pkg_name = content["cur_screen_pkg_name"]
    screenshot_path = content["screenshot_path"]

    if RuntimeContent.get_instance().is_found_privacy_url:
        return
    # 如果当前界面存在且当前界面加过
    # TODO
    pp_text_dict = get_privacy_policy_ele_dict()
    if len(pp_text_dict) > 0:
        for pp_text, pp_text_cnt in pp_text_dict.items():
            loc_list = cal_privacy_ele_loc(screenshot_path, pp_text, pp_text_cnt)
            if loc_list is not None:
                for loc_tuple in loc_list:
                    if loc_tuple is not None:
                        pp_x, pp_y, w, h = loc_tuple[0], loc_tuple[1], loc_tuple[2], loc_tuple[3]
                        pp_ele_dict = {
                            'class': '',
                            'resource-id': '',
                            'package': cur_screen_pkg_name,
                            'text': pp_text,
                            'bounds': "[" + str(pp_x) + "," + str(pp_y) + "][" + str(w) + "," + str(h) + "]"
                        }
                        pp_ele_uid = get_unique_id(pp_ele_dict, cur_activity)
                        RuntimeContent.get_instance().put_ele_uid_map(pp_ele_uid, pp_ele_dict)
                        clickable_elements = content["cur_ck_eles"]
                        clickable_elements.insert(0, pp_ele_uid)
                        content["is_add_privacy_eles"] = True
                        LogUtils.log_info(f"OCR到{pp_text}")
                    else:
                        LogUtils.log_info(f"没有OCR到{pp_text}")
            else:
                LogUtils.log_info(f"没有OCR到{pp_text}")
    else:
        LogUtils.log_info(f"没有找到隐私政策文本")
