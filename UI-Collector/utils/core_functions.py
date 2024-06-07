from ScreenNode import ScreenNode
from utils.DeviceUtils import get_cur_screen_node_from_context
from utils.ScreenCompareStrategy import *
from RuntimeContent import *
from utils.LogUtils import *
from Config import *
from utils.ScreenCompareUtils import *

# 检测多层环
def check_cycle(cur_node: ScreenNode, last_node: ScreenNode):
    sim_flag = is_text_similar(cur_node.ck_eles_text, last_node.ck_eles_text)
    if sim_flag:
        return True

    # if cur_node.children is None or len(cur_node.children) == 0:
    #     return False
    if cur_node.call_map is None or len(cur_node.call_map) == 0 or cur_node.call_map is {}:
        return False
    # for child in cur_node.children:
    #     if screen_compare_strategy.compare_screen(child.all_text, last_node.all_text)[0] == True:
    #         return True
    #     else:
    #         res = check_cycle(child, last_node, screen_compare_strategy)
    #         if res == True:
    #             return True
    for child in cur_node.call_map.values():
        sim_flag = is_text_similar(child.ck_eles_text, last_node.ck_eles_text)
        if sim_flag:
            return True
        else:
            res = check_cycle(child, last_node)
            if res:
                return True
    return False


def is_non_necessary_click(cur_clickable_ele_dict):
    # if cur_clickable_ele_dict.get("resource-id") == "com.alibaba.android.rimet:id/toolbar":
    #     return True
    # if cur_clickable_ele_dict.get("resource-id") == "com.alibaba.android.rimet:id/back_layout":
    #     return True

    text = cur_clickable_ele_dict.get("text")

    # TODO 暂时忽略钉钉创建团队的场景
    non_necessary_list = ["相机", "照片", "拍照", "手机文件", "相册", "相片", "拍摄", "关注", "粉丝", "退出登陆", "注销", "付款",
                          "退出登录", "退出当前账号", "下载", "分享", "浏览器", "安装", "浮窗", "更新", "升级", "支付", "预订", "评论", "换一换",
                          "image", 'Image', "photo", "Photo", "视频", "语音", "直播", "购买", "开通", "下单"]
    for non_necessary_str in non_necessary_list:
        if non_necessary_str in text:
            return True

    return False


def print_screen_info(content, type):
    cur_screen_node = get_cur_screen_node_from_context(content)
    LogUtils.log_info("*" * 100)
    if type == 1:
        LogUtils.log_info(f"该screen为新: {cur_screen_node.ck_eles_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
        if cur_screen_node.diff_clickable_elements is not None:
            LogUtils.log_info(f"差分后的数量为 {len(cur_screen_node.diff_clickable_elements)}")

    elif type == 0:
        LogUtils.log_info(f"该screen已存在: {cur_screen_node.ck_eles_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
        if cur_screen_node.diff_clickable_elements is not None:
            LogUtils.log_info(f"差分后的数量为 {len(cur_screen_node.diff_clickable_elements)}")

    elif type == 2:
        LogUtils.log_info(
            f"该screen是弹框: {cur_screen_node.ck_eles_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
        if cur_screen_node.diff_clickable_elements is not None:
            LogUtils.log_info(f"差分后的数量为 {len(cur_screen_node.diff_clickable_elements)}")
    LogUtils.log_info("*" * 100)



def get_two_clickable_eles_diff(cur_eles, last_eles):
    if last_eles is None or cur_eles is None or len(last_eles) == 0 or len(cur_eles) == 0:
        return None
    # if cur_activity != last_activity:
    #     return None
    # if len(cur_eles) <= len(last_eles):
    #     return False, None

    # union_eles = union(d, cur_eles, cur_activity, last_eles, last_activity)
    diff_eles = list(set(cur_eles).difference(last_eles))
    LogUtils.log_info(f"出现了重叠,可能为框,差分之后数量为{len(diff_eles)}")
    return diff_eles






