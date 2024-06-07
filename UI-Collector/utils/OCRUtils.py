from PIL import Image
import pytesseract
from PIL import ImageEnhance
from collections import OrderedDict


def cal_privacy_ele_loc(img_path: str, privacy_text: str, pp_text_cnt:int) -> tuple():
    """
    :param img_path: 截图的路径
    :return: "隐私权政策"文本的坐标
    """
    img = Image.open(img_path)
    # 二值化
    img = img.convert('L')  # 这里也可以尝试使用L
    # 修改图片的灰度
    # img = img.convert('RGB')  # 这里也可以尝试使用L
    # enhancer = ImageEnhance.Color(img)
    # enhancer = enhancer.enhance(0)
    # enhancer = ImageEnhance.Brightness(enhancer)
    # enhancer = enhancer.enhance(2)
    # enhancer = ImageEnhance.Contrast(enhancer)
    # enhancer = enhancer.enhance(8)
    # enhancer = ImageEnhance.Sharpness(enhancer)
    # img = enhancer.enhance(20)

    # config = 'tessedit_char_whitelist=隐私权政策'
    # text = pytesseract.image_to_string(img, lang='chi_sim')
    # print(text)

    data = pytesseract.image_to_data(img, output_type='dict', lang='chi_sim')
    if len(data) < len(privacy_text):
        return None
    loc_list = __get_privacy_loc_list(data, privacy_text)
    if loc_list is None or len(loc_list) == 0:
        return None
    group = __get_group_by_row(loc_list)
    sel_group = __select_group(group, privacy_text, pp_text_cnt)

    sel_loc_list = __get_group_loc_list(sel_group)
    return sel_loc_list



def __get_group_by_row(loc_list):
    """ 将位于相同行的关键字放在一组
    :param loc_list: 一个存放隐私关键字信息(字符, 位置x, 位置y)的列表
    :return: 由相同行划分的组
    """
    idx = 0
    group = []
    temp_height = loc_list[0][2]
    # 当两个关键词的位置y信息相差不超过阈值, 则认为是同一行
    col_diff_threshold = 8
    group_cnt = 0
    while idx < len(loc_list):
        if abs(loc_list[idx][2] - temp_height) < col_diff_threshold:
            if len(group) <= group_cnt:
                group.append([])
            group[group_cnt].append(loc_list[idx])
        else:
            group_cnt += 1
            temp_height = loc_list[idx][2]
            idx -= 1
        idx += 1
    return group


def __select_group(group, privacy_text, pp_text_cnt):
    """ 将同一行内或者相邻行内大于阈值个数的隐私关键字放在一起
    :param pp_text_cnt:
    """
    res_group = []
    match_threshold = len(privacy_text) - 1
    i = 0
    temp_group = []
    while i < len(group):
    # for i in range(len(group)):
        # 同一行内
        if match_threshold <= len(group[i]) <= len(privacy_text):
            res_group.append(group[i])
        # 相邻行内
        elif i != len(group) - 1 and match_threshold <= len(group[i]) + len(group[i + 1]) <= len(privacy_text):
            res_group.append(group[i] + group[i + 1])
            i += 1
        else:
            temp_group.append(group[i])
        i += 1

    # 如果没有填充到指定的pp_text_cnt个数, 就都把剩下的关键词都加上去
    if len(res_group) < pp_text_cnt:
        for temp_item in temp_group:
            res_group.append(temp_item)
    return res_group


def __get_group_loc_list(sel_group):
    """ 算出item的坐标信息
    """
    loc_list = []
    for group_item in sel_group:
        mid_idx = __get_mid_index(group_item)
        x, y, w, h = int(2*group_item[mid_idx][1]), int(2*group_item[mid_idx][2]), int(0), int(0)
        # 此处的变换是为了迎合ele_dict
        loc_list.append((x, y, w, h))
    return loc_list

def __get_mid_index(llist):
    return len(llist)//2

def __is_privacy_related(content: str, pp_text: str):
    for c in pp_text:
        if content == c:
            return True
    return False


def __get_privacy_loc_list(data, pp_text):
    boxes = len(data['level'])
    loc_list = []
    for i in range(boxes):
        if data['text'][i] != '' and __is_privacy_related(data['text'][i], pp_text):
            x1 = data['left'][i]
            y1 = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]
            x = x1 + width / 2
            y = y1 + height / 2
            loc_list.append((data['text'][i], x, y))
    return loc_list


def __get_first_privacy_loc(loc_list, privacy_text: str):
    index = -1
    for i in range(len(loc_list) - len(privacy_text) + 1):
        flag = True
        for j in range(len(privacy_text)):
            if loc_list[i + j][0] != privacy_text[j]:
                flag = False
                break
        if flag:
            index = i
            break
    return index



