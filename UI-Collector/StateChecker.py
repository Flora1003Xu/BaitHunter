from utils.ScreenCompareUtils import *
from Config import *


def check_is_errorscreen(ck_eles_text: str) -> bool:
    error_screen_list = RuntimeContent.get_instance().get_error_screen_list()
    for err_ck_eles_text in error_screen_list:
        sim_flag = is_text_similar(ck_eles_text, err_ck_eles_text)
        if sim_flag:
            return True
    return False


def check_is_error_clickable_ele(clickable_ele_uid):
    error_clickable_ele_uid_list = RuntimeContent.get_instance().get_error_clickable_ele_uid_list()
    for err_ele_uid in error_clickable_ele_uid_list:
        if err_ele_uid == clickable_ele_uid:
            return True
    return False


def check_screen_list(screen_list):
    if screen_list is None:
        return False
    if len(screen_list) >= 5:
        last_text = screen_list[-1]
        if screen_list[-2] == last_text and \
                screen_list[-3] == last_text and \
                screen_list[-4] == last_text and \
                screen_list[-5] == last_text:
            return True
    else:
        return False


def check_state_list_reverse(k, state_list, target) -> bool:
    if k > len(state_list):
        return False
    for i in range(k):
        if state_list[len(state_list) - 1 - i] != target:
            return False
    return True


def check_pattern_state(k: int, pattern_list: list) -> bool:
    """ 检查state_list是否有连续k个子列表(从最后一个元素开始算起)为pattern_list
    :return: 返回state_list是否为pattern_state
    """
    state_list = RuntimeContent.get_instance().get_state_list()
    if k * len(pattern_list) > len(state_list):
        return False
    for i in range(k):
        is_ex = True
        for j in range(len(pattern_list)):
            if state_list[len(state_list) - 1 - i * len(pattern_list) - j] != pattern_list[j]:
                is_ex = False
                break
        if not is_ex:
            return False
    return True


def check_pattern_state2(k, exception_states) -> bool:
    state_list = RuntimeContent.get_instance().get_state_list()
    if k > len(state_list):
        return False
    for i in range(k):
        is_ex = False
        for ex in exception_states:
            if state_list[len(state_list) - 1 - i] == ex:
                is_ex = True
                break
        if not is_ex:
            return False
    return True


def check_screen_list_reverse(k) -> bool:
    screen_list = RuntimeContent.get_instance().get_screen_list()
    if k <= 1:
        return False
    if screen_list is None or len(screen_list) == 0:
        return False
    if len(screen_list) < 3 * k:
        return False
    # step为1, 2, 3
    for step in range(1, 4, 1):
        res = check_screen_list_by_pattern_reverse(k, screen_list, step)
        if res is True:
            return True
    return False


def check_pattern_screen(k: int, step: int) -> bool:
    """ 检查screen_list是否有连续k个子列表(从最后一个元素开始算起)为pattern_screen_list
        pattern_screen_list为screen_list倒数的step个元素
    :return: 返回screen_list是否为pattern_screen
    """
    screen_list = RuntimeContent.get_instance().get_screen_list()
    if k * step > len(screen_list):
        return False
    pattern_screen_list = []
    for i in range(step):
        pattern_screen_list.append(screen_list[len(screen_list) - 1 - i])
    for i in range(k):
        is_ex = True
        for j in range(len(pattern_screen_list)):
            if screen_list[len(screen_list) - 1 - i * len(pattern_screen_list) - j] != pattern_screen_list[j]:
                is_ex = False
                break
        if not is_ex:
            return False
    return True


def check_screen_list_by_pattern_reverse(k, screen_list, step) -> bool:
    l = 0
    for i in range(step):
        l += 1
    for cnt in range(0, k - 1, 1):
        for i in range(step):
            if l >= len(screen_list):
                return False
            elif screen_list[len(screen_list) - 1 - l] != screen_list[len(screen_list) - 1 - i]:
                return False
            else:
                l += 1
    return True


def check_screen_list_order(k, screen_list) -> bool:
    if k <= 1:
        raise Exception
    if screen_list is None or len(screen_list) == 0:
        raise Exception
    if len(screen_list) < k:
        return False
    # step为1, 2, 3
    for step in range(1, 4, 1):
        res = check_screen_list_by_pattern_order(k, screen_list, step)
        if res is True:
            return True
    return False


def check_screen_list_by_pattern_order(k, screen_list, step) -> bool:
    l = 0
    for i in range(step):
        l += 1
    for cnt in range(0, k - 1, 1):
        for i in range(step):
            if l >= len(screen_list):
                return False
            elif screen_list[l] != screen_list[i]:
                return False
            else:
                l += 1
    return True


def check_is_inputmethod_in_cur_screen():
    d = Config.get_instance().get_device()
    # 小米的输入法
    if d(packageName="com.sohu.inputmethod.sogou.xiaomi").exists():
        return True
    elif d(packageName="com.miui.securityinputmethod").exists():
        return True
    elif d(packageName="com.baidu.input_mi").exists():
        return True
    # pixel的输入法
    elif d(packageName="com.google.android.inputmethod.latin").exists():
        return True
    else:
        return False


def check_is_first_scrren_finish():
    first_scrren_ck_eles_text = RuntimeContent.get_instance().get_first_screen_ck_eles_text()
    first_screen_node = RuntimeContent.get_instance().get_screen_map().get(first_scrren_ck_eles_text, None)
    if first_screen_node is not None and first_screen_node.is_screen_clickable_finished():
        return True
    return False


def check_is_layer_finish(layer: int):
    pass


def check_is_in_home_screen(cur_screen_pkg_name):
    # 小米的home screen
    if cur_screen_pkg_name == "com.miui.home":
        return True
    # pixel的home screen
    if cur_screen_pkg_name == "com.google.android.apps.nexuslauncher":
        return True
    # pixel类安卓原生lineage os的home screen
    if cur_screen_pkg_name == "com.android.launcher3":
        return True
    return False


def check_is_permisson_screen(cur_screen_pkg_name):
    if cur_screen_pkg_name == "com.android.permissioncontroller":
        return True
    if cur_screen_pkg_name == "com.android.packageinstaller":
        return True
    if cur_screen_pkg_name == "com.google.android.permissioncontroller":
        return True
    if cur_screen_pkg_name == "com.google.android.packageinstaller":
        return True
    if cur_screen_pkg_name == "com.miui.securitycenter":
        return True
    if cur_screen_pkg_name == "com.lbe.security.miui":
        return True
    return False


def check_is_in_webview(cur_activity: str) -> bool:
    d = Config.get_instance().get_device()
    if d(className="android.webkit.WebView").exists():
        return True
    # if "WebView" in cur_activity or "webview" in cur_activity:
    #     return True
    else:
        return False
