from StateHandler import *
from utils.CalDepthUtils import *
from utils.FileUtils import FileUtils
import threading
from constant.DefException import RestartException
from queue import Queue
from traceback import format_exc
from services.mislead_detector.save_mislead_file import save_mislead_file
import filecmp

class FSM(threading.Thread):

    def __init__(self, t_name, data: Queue, req_que: Queue, resp_que: Queue, pp_que):#把末尾的, pp_que删了
        threading.Thread.__init__(self, name=t_name)
        self.data = data
        self.req_queue = req_que
        self.resp_queue = resp_que

        self.exit_code = 0
        self.exception = None
        self.exc_traceback = ''
        # 新增一个处理隐私政策的queue
        #self.pp_queue = pp_que

    # state_map = {
    #     1: "不是当前要测试的app,即app跳出了测试的app",
    #     2: "发现当前界面有文本输入法框",
    #     3: "当前Screen已经存在",
    #     4: "当前Screen已经点完",
    #     5: "当前Screen不存在,新建Screen",
    #     6: "出现了不可回退的框, 启用随机点",
    #     7: "出现了不可回退的框, 需要重启?",
    #     8: "出现了不可回退的框, 启用double_press_back",
    #     9: "出现了系统权限页面",
    #     10: "出现了系统外不可回退的框",
    #     11: "当前Screen为WebView",
    #     12: "当前Screen为error不该点",
    #     100: "完成"
    # }

    reverse_state_map = {
        1: "STATE_ExitApp",
        2: "STATE_InputMethod",
        3: "STATE_ExistScreen",
        4: "STATE_FinishScreen",
        5: "STATE_NewScreen",
        7: "STATE_StuckRestart",
        8: "STATE_DoublePress",
        9: "STATE_PermissonScreen",
        10: "STATE_OutsystemSpecialScreen",
        11: "STATE_WebViewScreen",
        12: "STATE_ErrorScreen",
        13: "STATE_HomeScreenRestart",
        14: "STATE_ExceedDepth",
        15: "STATE_UndefineDepth",
        16: "STATE_KillOtherApp",
        17: "STATE_Back",
        18: "STATE_Popup",
        100: "STATE_Terminate"
    }

    STATE_ExitApp = 1
    STATE_InputMethod = 2
    STATE_ExistScreen = 3
    STATE_FinishScreen = 4
    STATE_NewScreen = 5
    STATE_StuckRestart = 7
    STATE_DoublePress = 8
    STATE_PermissonScreen = 9
    STATE_OutsystemSpecialScreen = 10
    STATE_WebViewScreen = 11
    STATE_ErrorScreen = 12
    STATE_HomeScreenRestart = 13
    STATE_ExceedDepth = 14
    STATE_UndefineDepth = 15
    STATE_KillOtherApp = 16
    STATE_Back = 17
    STATE_PopUp = 18
    STATE_Terminate = 100

    def query_popup_info(self, img_path):
        # 将图片放到请求队列, 如果队满则阻塞, 阻塞时长timeout则异常
        self.req_queue.put(img_path, block=True)
        # 从响应队列获取结果, 如果空则阻塞, 阻塞时长timeout则异常
        data = self.resp_queue.get(block=True)
        return data

    def update_stat(self, cur_activity, ck_eles_text):
        StatRecorder.get_instance().add_stat_stat_activity_set(cur_activity)
        StatRecorder.get_instance().add_stat_screen_set(ck_eles_text)

    def do_transition(self, state, content):
        if state == self.STATE_ExitApp:
            StateHandler.handle_exit_app(content)
        elif state == self.STATE_InputMethod:
            StateHandler.handle_inputmethod(content)
        elif state == self.STATE_ExistScreen:
            StateHandler.handle_exist_screen(content)
        elif state == self.STATE_FinishScreen:
            StateHandler.handle_finish_screen(content)
        elif state == self.STATE_NewScreen:
            StateHandler.handle_new_screen(content)
        elif state == self.STATE_StuckRestart:
            # TODO 重启机制
            StateHandler.handle_stuck_restart(content)
        elif state == self.STATE_DoublePress:
            StateHandler.handle_double_press(content)
        elif state == self.STATE_PermissonScreen:
            StateHandler.handle_system_permission_screen(content)
        elif state == self.STATE_HomeScreenRestart:
            StateHandler.handle_homes_screen_restart(content)
        elif state == self.STATE_KillOtherApp:
            StateHandler.handle_kill_other_app(content)
        elif state == self.STATE_Terminate:
            StateHandler.handle_terminate(content)
        elif state == self.STATE_ExceedDepth:
            StateHandler.handle_exceed_screen(content)
        elif state == self.STATE_Back:
            StateHandler.handle_back(content)
        elif state == self.STATE_PopUp:
            StateHandler.handle_popup(content)
        else:
            raise Exception("意外情况")

    def get_state(self):
        content = get_screen_content()
        cur_activity = content["cur_activity"]
        cur_screen_pkg_name = content["cur_screen_pkg_name"]
        cur_ck_eles_text = content["ck_eles_text"]
        screenshot_path = content["screenshot_path"]
        screen_text = content["screen_text"]

        StatRecorder.get_instance().add_stat_stat_activity_set(cur_activity)
        StatRecorder.get_instance().add_stat_screen_set(cur_ck_eles_text)

        # LogUtils.log_info(f"当前Screen为: {screen_text}")
        RuntimeContent.get_instance().append_screen_list(cur_ck_eles_text)

        last_clickable_ele_uid = RuntimeContent.get_instance().last_clickable_ele_uid
        if RuntimeContent.get_instance().is_in_mislead_eles_set(last_clickable_ele_uid):
            LogUtils.log_info(f"{last_clickable_ele_uid} 是诱导组件")
            last_screenshot_path = RuntimeContent.get_instance().get_last_screenshot_path()
            click_xy = get_location(RuntimeContent.get_instance().get_ele_uid_map_by_uid(last_clickable_ele_uid))
            mislead_text = RuntimeContent.get_instance().get_ele_uid_map_by_uid(last_clickable_ele_uid)["text"]
            if not filecmp.cmp(last_screenshot_path, screenshot_path):
                save_mislead_file(Config.get_instance().get_collectDataPath(), last_screenshot_path, screenshot_path, click_xy, mislead_text)


        if Config.get_instance().curDepth > Config.get_instance().maxDepth:
            return self.STATE_Terminate, content

        if cur_screen_pkg_name != Config.get_instance().get_target_pkg_name():
            if check_is_in_home_screen(cur_screen_pkg_name):
                return self.STATE_HomeScreenRestart, content
            if check_is_permisson_screen(cur_screen_pkg_name):
                return self.STATE_PermissonScreen, content
            else:
                if check_pattern_state(2, [self.STATE_ExitApp]):
                    return self.STATE_KillOtherApp, content
                else:
                    return self.STATE_ExitApp, content

        if check_is_inputmethod_in_cur_screen() == True:
            return self.STATE_InputMethod, content

        # 对界面组件判断, 如果未覆盖全部则是弹框
        screen_ltrb = check_cover_full_screen(Config.get_instance().get_device())
        if screen_ltrb is not None:
            content["ltrb"] = screen_ltrb
            return self.STATE_PopUp, content

        # 如果置信度>=75%则认为是弹框, 进行弹框处理
        popup_info = self.query_popup_info(screenshot_path)
        LogUtils.log_info(popup_info)
        if popup_info["conf"] >= 0.75:
            xywh = popup_info["xywh"]
            ltrb = get_4corner_coord(xywh)
            content["ltrb"] = ltrb
            return self.STATE_PopUp, content

        screen_depth_map = RuntimeContent.get_instance().screen_depth_map
        last_screen_node = RuntimeContent.get_instance().last_screen_node

        cur_screen_depth = Config.get_instance().UndefineDepth
        # 从cache中得到当前界面的层数结果
        res_sim, most_similar_screen_node = get_max_similarity_screen_node(cur_ck_eles_text)
        # res_sim, res_depth = get_max_sim_from_screen_depth_map(ck_eles_text)
        if res_sim >= Config.get_instance().screen_similarity_threshold:
            if screen_depth_map.get(most_similar_screen_node.ck_eles_text, False):
                cur_screen_depth = screen_depth_map.get(most_similar_screen_node.ck_eles_text)

        # 直接计算当前界面的层数结果
        if last_screen_node is not None and last_screen_node.ck_eles_text != cur_ck_eles_text:
            if last_screen_node.ck_eles_text == "root":
                cal_depth = 1
            else:
                cal_depth = CalDepthUtils.calDepth(RuntimeContent.get_instance().last_screen_node.ck_eles_text)
            cur_screen_depth = min(cur_screen_depth, cal_depth)

        # 将最新最小的结果写入screen_depth_map
        if res_sim >= Config.get_instance().screen_similarity_threshold:
            # 说明当前界面已经存在, 则用之前已经存在的界面的ck_eles_text
            screen_depth_map[most_similar_screen_node.ck_eles_text] = cur_screen_depth
        else:
            # 说明当前界面为全新界面, 由于当前界面还没new出来, 因此用ck_eles_text
            screen_depth_map[cur_ck_eles_text] = cur_screen_depth

        if cur_screen_depth == Config.get_instance().UndefineDepth:
            LogUtils.log_info("Undefine")
            return self.STATE_Back, content

        LogUtils.log_info(f"当前层数为: {cur_screen_depth}")
        if cur_screen_depth > Config.get_instance().curDepth:
            LogUtils.log_info("ExceedDepth")
            return self.STATE_ExceedDepth, content

        content["cur_screen_node"] = most_similar_screen_node
        content["most_similar_screen_node"] = most_similar_screen_node
        content["sim"] = res_sim
        content["cur_screen_depth"] = cur_screen_depth

        # if cur_screen_node is not None:
        if res_sim >= Config.get_instance().screen_similarity_threshold:
            cur_screen_node = most_similar_screen_node
            RuntimeContent.get_instance().put_screen_map(cur_ck_eles_text, cur_screen_node)

            if check_is_errorscreen(cur_ck_eles_text):
                LogUtils.log_info("ErrorScreen")
                return self.STATE_Back, content

            # 说明已经点完, press_back
            if cur_screen_node.is_screen_clickable_finished():
                return self.STATE_FinishScreen, content
            # 3说明未点完, 触发点一个组件
            else:
                return self.STATE_ExistScreen, content
        else:
            return self.STATE_NewScreen, content

    def print_state(self, state):
        # Logger.get_instance().print(f"状态为{self.reverse_state_map[state]} {self.state_map[state]}")
        LogUtils.log_info(f"状态为{self.reverse_state_map[state]}")

    def __run(self):
        stat_map = {}
        while True:
            if len(StatRecorder.get_instance().get_stat_screen_set()) % 10 == 0 and stat_map.get(
                    len(StatRecorder.get_instance().get_stat_screen_set()), False) is False:
                stat_map[len(StatRecorder.get_instance().get_stat_screen_set())] = True
                StatRecorder.get_instance().print_result()

            StatRecorder.get_instance().count_time()
            state, content = self.get_state()
            RuntimeContent.get_instance().append_state_list(state)
            # LogUtils.log_info("\n")
            # LogUtils.log_info("-" * 50)
            self.print_state(state)

            # BFS动态增加层数的条件是: 当前发现pattern_state和pattern_screen, 表示无法再继续增长
            cur_depth = Config.get_instance().curDepth
            cal_cov_map = StatRecorder.get_instance().get_coverage(cur_depth)
            StatRecorder.get_instance().print_coverage(cal_cov_map)
            dq = RuntimeContent.get_instance().cov_mono_que
            cov = 0
        
            
            # 如果当前节点为homescreen进来的第一个界面并且该界面所有组件已经点完，则可以动态增加当前层数
            if state == self.STATE_FinishScreen and RuntimeContent.get_instance().last_screen_node is not None and RuntimeContent.get_instance().last_screen_node.ck_eles_text == "root":
            # if state == self.STATE_FinishScreen and content.get("cur_screen_depth", None) is not None and content.get("cur_screen_depth")==1:
            # if cov == 1 or (len(RuntimeContent.get_instance().cov_mono_que) >= 4 and dq[-1][1] == self.STATE_FinishScreen and dq[-2][1] == self.STATE_FinishScreen and dq[-3][1] == self.STATE_FinishScreen and dq[-4][1] == self.STATE_FinishScreen):

                RuntimeContent.get_instance().cov_mono_que.clear()

                LogUtils.log_info(f"动态增加当前层数{cur_depth}-->层数{cur_depth + 1}")
                Config.get_instance().curDepth += 1

                if cal_cov_map.get(cur_depth, None) is not None:
                    # 追加保存覆盖率结果
                    FileUtils.save_coverage(cur_depth, cal_cov_map[cur_depth][1], cal_cov_map[cur_depth][2])

                # 重置screenNode的点击下标already_click_cnt
                screen_depth_map = RuntimeContent.get_instance().screen_depth_map
                screen_uid_list = screen_depth_map.keys()
                for screen_uid in screen_uid_list:
                    depth = screen_depth_map.get(screen_uid)
                    if depth > cur_depth:
                        continue
                    screen_node = RuntimeContent.get_instance().get_screen_map().get(screen_uid)
                    #  在重置already_clicked_cnt前将记录保存在total_clicked_cnt
                    screen_node.total_clicked_cnt = max(screen_node.total_clicked_cnt, screen_node.already_clicked_cnt)
                    screen_node.already_clicked_cnt = 0

            self.do_transition(state, content)

            LogUtils.log_info("-" * 50)
            LogUtils.log_info("\n")

    def run(self):
        try:
            self.__run()
        except RestartException as e:
            self.exit_code = 1
            self.exception = e
            self.exc_traceback = format_exc()
        except TerminateException as e:
            self.exit_code = 2
            self.exception = e
            self.exc_traceback = format_exc()
        except TimeLimitException as e:
            self.exit_code = 3
            self.exception = e
            self.exc_traceback = format_exc()
        except Exception as e:
            self.exit_code = 4
            self.exception = e
            self.exc_traceback = format_exc()
