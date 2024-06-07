from constant.DefException import *
from utils.core_functions import *
from StatRecorder import *
import random
from services.mislead_detector.get_mislead_eles import get_mislead_eles
from StateChecker import *
from utils.DeviceUtils import *
from utils.LogUtils import *
from utils.ScreenCompareUtils import *


class StateHandler(object):
    @classmethod
    def click_one_ele(cls, content):
        # 遍历cur_screen的所有可点击组件
        cur_screen_node = get_cur_screen_node_from_context(content)
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()


        screenshot_path = content["screenshot_path"]

        clickable_ele_idx = cur_screen_node.already_clicked_cnt
        while clickable_ele_idx < len(cur_screen_node_clickable_eles):
            cur_clickable_ele_uid = cur_screen_node_clickable_eles[clickable_ele_idx]

            # TODO 仅调试使用
            # if clickable_ele_idx <= 4:
            #     cur_screen_node.already_clicked_cnt += 1
            #     clickable_ele_idx+=1
            #     continue
            cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)

            # loc_x, loc_y = get_location(cur_clickable_ele_dict)
            # if loc_x >= 60 and loc_x <= 70 and loc_y == 162:
            #     cur_screen_node.already_clicked_cnt += 1
            #     RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
            #     clickable_ele_idx += 1
            #     continue
            # if loc_x >= 998 and loc_x <= 1010 and loc_y >= 155 and loc_y <= 165:
            #     cur_screen_node.already_clicked_cnt += 1
            #     RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
            #     clickable_ele_idx += 1
            #     continue

            # for clickable_ele_idx, cur_clickable_ele_uid in enumerate(cur_screen_node_clickable_eles):
            # --------------------------------------
            # 判断当前组件是否需要访问
            # 1.如果没访问过，即vis_map[uid]=False，就直接访问
            # 2.如果访问过了，即vis_map[uid]=True,还得判断该组件是否是
            # 当前callmap的，如果是还需要递归判断该组件对应的call_map里面的节点(screen)
            # 的所有组件是否访问完毕

            # 表示该组件已经访问过
            # +1是因为下标从0开始
            # cur_screen_node.already_clicked_cnt = clickable_ele_idx + 1
            # uid = get_uid(cur_clickable_ele, d, umap, cur_activity)
            cur_screen_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
            if is_non_necessary_click(cur_screen_ele_dict):
                cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
                if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
                else:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1
                LogUtils.log_info(f"省略组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                LogUtils.log_info("\n")
                clickable_ele_idx += 1
                cur_screen_node.already_clicked_cnt += 1
                RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                continue

            if cur_screen_node.ele_vis_map.get(cur_clickable_ele_uid, False) == False:
                # 拿到该组件的坐标x, y
                cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
                loc_x, loc_y = get_location(cur_clickable_ele_dict)
                cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
                # 点击该组件
                LogUtils.log_info(f"正常点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                StatRecorder.get_instance().inc_total_ele_cnt()
                RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
                RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)

                RuntimeContent.get_instance().set_last_screenshot_path(screenshot_path)

                if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
                else:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1

                # 标识点击过的组件
                cls.__click(loc_x, loc_y)
                return

            else:
                # if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid) is not None and cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid) > Config.get_instance().get_CLICK_MAX_CNT():
                #     LogUtils.log_info(f"该组件点击次数过多不点了&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                #     cur_screen_node.already_clicked_cnt += 1
                #     clickable_ele_idx += 1
                if cur_screen_node.call_map.get(cur_clickable_ele_uid, None) is not None:
                    next_screen_node = cur_screen_node.call_map.get(cur_clickable_ele_uid, None)
                    next_screen_all_text = next_screen_node.ck_eles_text

                    if check_is_error_clickable_ele(cur_clickable_ele_uid) == True:
                        LogUtils.log_info(
                            f"该组件会触发error screen因此跳过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue
                    if check_is_errorscreen(next_screen_all_text) == True:
                        LogUtils.log_info(
                            f"该组件会触发error screen因此跳过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue
                    if next_screen_node.pkg_name != Config.get_instance().get_target_pkg_name():
                        LogUtils.log_info(
                            f"clickmap--next界面非本app本包名&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue

                    res_sim, res_depth = get_max_sim_from_screen_depth_map(next_screen_all_text)
                    if res_sim >= Config.get_instance().screen_similarity_threshold and res_depth == Config.get_instance().UndefineDepth:
                        LogUtils.log_info(
                            f"clickmap--next界面是UndefineDepth&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue

                    if res_sim >= Config.get_instance().screen_similarity_threshold and res_depth > Config.get_instance().curDepth:
                        LogUtils.log_info(
                            f"clickmap--next界面是超过限制层数的&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue

                    # if next_screen_node.get_isWebView():
                    #     LogUtils.log_info(
                    #         f"clickmap--next界面是WebView&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    #     cur_screen_node.already_clicked_cnt += 1
                    #     RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                    #     clickable_ele_idx += 1
                    #     continue

                    if next_screen_node.is_screen_clickable_finished():
                        LogUtils.log_info(f"clickmap--next界面点击完成&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue
                    else:
                        # TODO
                        # if cur_screen_node.is_cur_callmap_finish(next_screen_all_text, ScreenCompareStrategy(LCSComparator())) == False:
                        # click_map指示存在部分没完成
                        cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(
                            cur_clickable_ele_uid)
                        loc_x, loc_y = get_location(cur_clickable_ele_dict)
                        LogUtils.log_info(f"clickmap没完成点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        StatRecorder.get_instance().inc_total_ele_cnt()
                        RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
                        RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)

                        RuntimeContent.get_instance().set_last_screenshot_path(screenshot_path)

                        if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                            cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 0
                        else:
                            cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1

                        cls.__click(loc_x, loc_y)

                        return
                else:
                    LogUtils.log_info(f"已点击过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    cur_screen_node.already_clicked_cnt += 1
                    RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                    clickable_ele_idx += 1

    @classmethod
    def random_click_ele(cls, content):
        cur_screen_node = get_cur_screen_node_from_context(content)
        cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()
        choose = random.randint(0, len(cur_screen_node_clickable_eles) - 1)
        cur_clickable_ele_uid = cur_screen_node_clickable_eles[choose]
        cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
        loc_x, loc_y = get_location(cur_clickable_ele_dict)
        cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
        # 点击该组件
        LogUtils.log_info(f"随机点击组件&{choose}: {cur_clickable_ele_uid}")
        StatRecorder.get_instance().inc_total_ele_cnt()
        # 弹框不需要设置last
        # RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
        # RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)
        cls.__click(loc_x, loc_y)

    @classmethod
    def random_click_backpath_ele(cls, content):
        # TODO
        LogUtils.log_info("可能产生了不可去掉的框")
        cur_screen_node = get_cur_screen_node_from_context(content)

        cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)

        screenshot_path = content["screenshot_path"]

        # TODO
        candidate = None
        if cur_screen_node.candidate_random_clickable_eles is None or len(
                cur_screen_node.candidate_random_clickable_eles) == 0:
            candidate = cur_screen_node.build_candidate_random_clickable_eles()
        else:
            candidate = cur_screen_node.candidate_random_clickable_eles

        if candidate is None or len(candidate) == 0:
            return

        choose = random.randint(0, len(cur_screen_node.candidate_random_clickable_eles) - 1)
        cur_clickable_ele_uid = cur_screen_node.candidate_random_clickable_eles[choose]

        cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
        loc_x, loc_y = get_location(cur_clickable_ele_dict)
        cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
        # 点击该组件
        LogUtils.log_info(f"随机点击组件&{choose}: {cur_clickable_ele_uid}")
        StatRecorder.get_instance().inc_total_ele_cnt()
        RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
        RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)

        RuntimeContent.get_instance().set_last_screenshot_path(screenshot_path)

        cls.__click(loc_x, loc_y)



    @classmethod
    def __add_call_graph(cls, cur_screen_node):
        # 将cur_screen加入到last_screen的子节点
        last_screen_node = RuntimeContent.get_instance().get_last_screen_node()
        if last_screen_node is not None:
            last_screen_node.add_child(cur_screen_node)
        last_clickable_ele_uid = RuntimeContent.get_instance().get_last_clickable_ele_uid()
        if last_clickable_ele_uid is not None and last_clickable_ele_uid != "":
            cur_screen_node.append_last_ck_ele_uid_list(last_clickable_ele_uid)
        if last_screen_node is not None:
            if last_screen_node.ck_eles_text == cur_screen_node.ck_eles_text:
                LogUtils.log_info("回到自己")
                last_screen_node.update_callmap_item(RuntimeContent.get_instance().get_last_clickable_ele_uid())
                pass
            elif check_cycle(cur_screen_node, last_screen_node) == True:
                # 产生了回边
                last_screen_node.cycle_set.add(RuntimeContent.get_instance().get_last_clickable_ele_uid())
                LogUtils.log_info("产生回边")
                last_screen_node.update_callmap_item(RuntimeContent.get_instance().get_last_clickable_ele_uid())
                pass
            else:
                last_screen_node.call_map[RuntimeContent.get_instance().get_last_clickable_ele_uid()] = cur_screen_node

    @classmethod
    def create_new_screen(cls, content):
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        screen_text = get_screen_text_from_context(content)
        # 初始化cur_screen_node信息
        cur_screen_node = ScreenNode()
        cur_screen_node.pkg_name = cur_screen_pkg_name
        cur_screen_node.screen_text = screen_text
        cur_screen_node.activity_name = cur_activity
        cur_ck_eles = content["cur_ck_eles"]
        merged_diff = content["merged_diff"]
        sim = content.get("sim", None)
        most_similar_screen_node = content.get("most_similar_screen_node", None)
        if sim is not None and sim >= 0.60:
            # TODO
            most_sim_clickable_elements = most_similar_screen_node.get_exactly_clickable_eles()
            diff_list = get_two_clickable_eles_diff(cur_ck_eles, most_sim_clickable_elements)
            cur_screen_node.diff_clickable_elements = diff_list
        #     cur_screen_node.clickable_elements = clickable_eles
        #     # diff_text = get_screen_all_text_from_dict(diff_list, ele_uid_map)
        #     # ck_eles_text = diff_text
        #     cur_screen_node.all_text = ck_eles_text
        #     screen_map[ck_eles_text] = cur_screen_node
        # else:
        cur_screen_node.clickable_elements = cur_ck_eles
        cur_screen_node.ck_eles_text = ck_eles_text
        cur_screen_node.merged_diff = merged_diff

        # 将cur_screen加入到全局记录的screen_map
        RuntimeContent.get_instance().put_screen_map(ck_eles_text, cur_screen_node)
        return cur_screen_node

    @classmethod
    def get_exist_screen(cls, content):
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        cur_screen_node = get_cur_screen_node_from_context(content)
        return cur_screen_node

    @classmethod
    def get_system_permission_screen(cls, content):
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        screen_text = get_screen_text_from_context(content)
        # 初始化cur_screen_node信息
        cur_screen_node = ScreenNode()
        cur_screen_node.pkg_name = cur_screen_pkg_name
        cur_screen_node.screen_text = screen_text
        cur_screen_node.activity_name = cur_activity
        cur_ck_eles = content["cur_ck_eles"]
        cur_screen_node.clickable_elements = cur_ck_eles
        cur_screen_node.ck_eles_text = ck_eles_text
        # 不需要cur_screen加入到全局记录的screen_map
        # 不需要将cur_screen加入到last_screen的子节点
        # ...
        return cur_screen_node

    @classmethod
    def get_special_screen(cls, content):
        screen_map = RuntimeContent.get_instance().get_screen_map()
        ck_eles_text = content["ck_eles_text"]
        resnode = get_screennode_from_screenmap_by_similarity(ck_eles_text)
        if resnode is not None:
            cur_screen_node = resnode
        else:
            cur_screen_node = cls.create_new_screen(content)
        return cur_screen_node

    @classmethod
    def get_exceed_screen(cls, content):
        screen_map = RuntimeContent.get_instance().get_screen_map()
        ck_eles_text = content["ck_eles_text"]
        resnode = get_screennode_from_screenmap_by_similarity(ck_eles_text)
        if resnode is not None:
            cur_screen_node = resnode
        else:
            # 如果满足条件, 添加cliakable=false 的隐私政策权的组件
            cur_screen_node = cls.create_new_screen(content)
            if Config.get_instance().isSearchPrivacyPolicy:
                cls.insert_privacy_eles(content, cur_screen_node)
            # 加入误导组件
            cls.insert_mislead_eles(content, cur_screen_node)
        return cur_screen_node

    @classmethod
    def handle_kill_other_app(cls, content):
        non_pkg_name = content["cur_screen_pkg_name"]
        d = Config.get_instance().get_device()
        d.app_stop(non_pkg_name)
        time.sleep(3)
        start_pkg_name = Config.get_instance().get_target_pkg_name()
        d.app_start(start_pkg_name)
        time.sleep(3)


    @classmethod
    def handle_exist_screen(cls, content):
        cur_screen_node = cls.get_exist_screen(content)
        # 将cur_screen加入到last_screen的子节点
        cls.__add_call_graph(cur_screen_node)
        print_screen_info(content, 0)
        cls.click_one_ele(content)

    @classmethod
    def handle_exceed_screen(cls, content):
        # 获取exceed_screen
        cur_screen_node = cls.get_exceed_screen(content)
        cls.__add_call_graph(cur_screen_node)
        # cur_screen_node.set_isWebView(True)
        content["cur_screen_node"] = cur_screen_node
        # print_screen_info(content, True)
        pre_ck_eles_text = content["ck_eles_text"]
        cls.__press_back()
        LogUtils.log_info("进行回退")
        RuntimeContent.get_instance().set_last_screen_node(None)
        RuntimeContent.get_instance().set_last_clickable_ele_uid("")

        RuntimeContent.get_instance().set_last_screenshot_path("")

        after_ck_eles_text = get_screen_content()["ck_eles_text"]

        # 如果不一样说明文本变化了, 说明一次back即可回退
        sim_flag = is_text_similar(pre_ck_eles_text, after_ck_eles_text)
        if not sim_flag:
            return

        # 如果没变化, 尝试double_press_back
        LogUtils.log_info("一次回退失败, 二次回退")

        cls.__double_press_back()
        after_ck_eles_text = get_screen_content()["ck_eles_text"]
        # 如果不一样说明文本变化了, 说明两次back即可回退
        sim_flag = is_text_similar(pre_ck_eles_text, after_ck_eles_text)
        if not sim_flag:
            return
        # 上述方法都失效,重启
        # RuntimeContent.get_instance().append_error_screen_list(pre_ck_eles_text)
        # cur_screen_node = content.get("cur_screen_node", None)
        # if cur_screen_node is not None:
        #     last_ck_ele_uid_list = cur_screen_node.get_last_ck_ele_uid_list()
        #     RuntimeContent.get_instance().append_more_error_ck_ele_uid_list(last_ck_ele_uid_list)
        LogUtils.log_info("二次回退失败, 重启")
        raise RestartException("重启机制")

    @classmethod
    def handle_new_screen(cls, content):
        cur_screen_node = cls.create_new_screen(content)
        # 加入隐私组件
        if Config.get_instance().isSearchPrivacyPolicy:
            cls.insert_privacy_eles(content, cur_screen_node)
        # 加入误导组件
        cls.insert_mislead_eles(content, cur_screen_node)
        # 将cur_screen加入到last_screen的子节点
        cls.__add_call_graph(cur_screen_node)
        content["cur_screen_node"] = cur_screen_node
        print_screen_info(content, 1)
        cls.click_one_ele(content)

    @classmethod
    def handle_popup(cls, content):
        ltrb = content["ltrb"]
        popup_map = RuntimeContent.get_instance().get_popup_map()
        ck_eles_text = content["ck_eles_text"]

        resnode = get_max_similarity_popup_node(ck_eles_text)
        if resnode is not None:
            LogUtils.log_info("弹框已存在")
            cur_popup_node = resnode
        else:
            LogUtils.log_info("创建新弹框")
            cur_popup_node = cls.create_popup(content)
            # 删除不在弹框范围内的组件
            cls.__remove_eles_notin_popup(cur_popup_node, ltrb)
            # 移除没必要点击的组件
            cls.__remove_noneed_eles(cur_popup_node)
            # 加入隐私组件
            if Config.get_instance().isSearchPrivacyPolicy:
                cls.insert_privacy_eles(content, cur_popup_node)
            # 加入误导组件
            cls.insert_mislead_eles(content, cur_popup_node)
        content["cur_screen_node"] = cur_popup_node
        print_screen_info(content, 2)

        if cur_popup_node.is_screen_clickable_finished():
            LogUtils.log_info("弹框已经点完所有组件")
            cur_screen_node = get_cur_screen_node_from_context(content)
            cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()

            # 如果弹框已经点击完, 但是再出现弹框, 80%机会随机点, 20%机会back
            # random click是为了应对重复的弹框
            # random back是为了应对误报
            probability = random.random()
            if len(cur_screen_node_clickable_eles) > 0 and probability <= 0.8:
                cls.random_click_ele(content)
            else:
                cls.handle_popup_finish(content)
        else:
            cls.click_popup_eles(content)

    @classmethod
    def handle_popup_finish(cls, content):

        cur_screen_node = cls.get_exist_screen(content)
        pre_ck_eles_text = content["ck_eles_text"]
        cls.__press_back()
        LogUtils.log_info("进行回退")

        # 弹框不需要设置last
        # RuntimeContent.get_instance().set_last_screen_node(None)
        # RuntimeContent.get_instance().set_last_clickable_ele_uid("")

        after_ck_eles_text = get_screen_content()["ck_eles_text"]
        # 如果不一样说明文本变化了, 说明一次back即可回退, 弹框需要完全一样
        sim_flag = is_exactly_text_similar(pre_ck_eles_text, after_ck_eles_text)
        if not sim_flag:
            return
        # 如果没变化, 尝试double_press_back
        LogUtils.log_info("一次回退失败, 二次回退")

        cls.__double_press_back()
        after_ck_eles_text = get_screen_content()["ck_eles_text"]
        # 如果不一样说明文本变化了, 说明两次back即可回退, 弹框需要完全一样
        sim_flag = is_exactly_text_similar(pre_ck_eles_text, after_ck_eles_text)
        if not sim_flag:
            return
        LogUtils.log_info("二次回退失败, 重启")
        raise RestartException("重启机制")


    @classmethod
    def insert_privacy_eles(cls, content, screen_node:ScreenNode):
        screenshot_path = content["screenshot_path"]
        cur_screen_pkg_name = content["cur_screen_pkg_name"]
        cur_activity = content["cur_activity"]

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
                            clickable_elements = screen_node.get_diff_or_clickable_eles()
                            clickable_elements.insert(0, pp_ele_uid)
                            LogUtils.log_info(f"OCR到{pp_text}")
                        else:
                            LogUtils.log_info(f"没有OCR到{pp_text}")
                else:
                    LogUtils.log_info(f"没有OCR到{pp_text}")
        else:
            LogUtils.log_info(f"没有找到隐私政策文本")


    @classmethod
    def insert_mislead_eles(cls, content, screen_node:ScreenNode):
        screenshot_path = content["screenshot_path"]
        cur_screen_pkg_name = content["cur_screen_pkg_name"]
        cur_activity = content["cur_activity"]

        mislead_list = get_mislead_eles(screenshot_path)
        for mislead_ele in mislead_list:
            text = mislead_ele["text"]
            xywh = mislead_ele["xywh"]

            x,y,w,h = int(xywh[0]),int(xywh[1]),int(xywh[2]),int(xywh[3])

            pp_ele_dict = {
                'class': '',
                'resource-id': '',
                'package': cur_screen_pkg_name,
                'text': text,
                'bounds': "[" + str(x) + "," + str(y) + "][" + str(x+w) + "," + str(y+h) + "]"
            }
            mislead_uid = get_unique_id(pp_ele_dict, cur_activity)
            RuntimeContent.get_instance().put_ele_uid_map(mislead_uid, pp_ele_dict)
            clickable_elements = screen_node.get_diff_or_clickable_eles()
            clickable_elements.insert(0, mislead_uid)
            RuntimeContent.get_instance().add_mislead_eles_set(mislead_uid)




    @classmethod
    def click_popup_eles(cls, content):
        # 遍历cur_screen的所有可点击组件
        cur_screen_node = get_cur_screen_node_from_context(content)
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()

        screenshot_path = content["screenshot_path"]

        clickable_ele_idx = cur_screen_node.already_clicked_cnt
        while clickable_ele_idx < len(cur_screen_node_clickable_eles):
            cur_clickable_ele_uid = cur_screen_node_clickable_eles[clickable_ele_idx]

            # TODO 仅调试使用
            # if clickable_ele_idx <= 4:
            #     cur_screen_node.already_clicked_cnt += 1
            #     clickable_ele_idx+=1
            #     continue
            cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)

            # loc_x, loc_y = get_location(cur_clickable_ele_dict)
            # if loc_x >= 60 and loc_x <= 70 and loc_y == 162:
            #     cur_screen_node.already_clicked_cnt += 1
            #     RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
            #     clickable_ele_idx += 1
            #     continue
            # if loc_x >= 998 and loc_x <= 1010 and loc_y >= 155 and loc_y <= 165:
            #     cur_screen_node.already_clicked_cnt += 1
            #     RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
            #     clickable_ele_idx += 1
            #     continue

            # for clickable_ele_idx, cur_clickable_ele_uid in enumerate(cur_screen_node_clickable_eles):
            # --------------------------------------
            # 判断当前组件是否需要访问
            # 1.如果没访问过，即vis_map[uid]=False，就直接访问
            # 2.如果访问过了，即vis_map[uid]=True,还得判断该组件是否是
            # 当前callmap的，如果是还需要递归判断该组件对应的call_map里面的节点(screen)
            # 的所有组件是否访问完毕

            # 表示该组件已经访问过
            # +1是因为下标从0开始
            # cur_screen_node.already_clicked_cnt = clickable_ele_idx + 1
            # uid = get_uid(cur_clickable_ele, d, umap, cur_activity)
            cur_screen_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
            if is_non_necessary_click(cur_screen_ele_dict):
                cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
                if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
                else:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1
                LogUtils.log_info(f"省略组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                LogUtils.log_info("\n")
                clickable_ele_idx += 1
                cur_screen_node.already_clicked_cnt += 1
                RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                continue

            if cur_screen_node.ele_vis_map.get(cur_clickable_ele_uid, False) == False:
                # 拿到该组件的坐标x, y
                cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
                loc_x, loc_y = get_location(cur_clickable_ele_dict)
                cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
                # 点击该组件
                LogUtils.log_info(f"正常点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                StatRecorder.get_instance().inc_total_ele_cnt()
                # 弹框不需要set last node
                # RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
                RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)

                RuntimeContent.get_instance().set_last_screenshot_path(screenshot_path)

                if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
                else:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1

                # 标识点击过的组件
                cls.__click(loc_x, loc_y)
                return

            else:
                # if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid) is not None and cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid) > Config.get_instance().get_CLICK_MAX_CNT():
                #     LogUtils.log_info(f"该组件点击次数过多不点了&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                #     cur_screen_node.already_clicked_cnt += 1
                #     clickable_ele_idx += 1
                if cur_screen_node.call_map.get(cur_clickable_ele_uid, None) is not None:
                    next_screen_node = cur_screen_node.call_map.get(cur_clickable_ele_uid, None)
                    next_screen_all_text = next_screen_node.ck_eles_text

                    if check_is_error_clickable_ele(cur_clickable_ele_uid) == True:
                        LogUtils.log_info(
                            f"该组件会触发error screen因此跳过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue
                    if check_is_errorscreen(next_screen_all_text) == True:
                        LogUtils.log_info(
                            f"该组件会触发error screen因此跳过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue
                    if next_screen_node.pkg_name != Config.get_instance().get_target_pkg_name():
                        LogUtils.log_info(
                            f"clickmap--next界面非本app本包名&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue

                    res_sim, res_depth = get_max_sim_from_screen_depth_map(next_screen_all_text)
                    if res_sim >= Config.get_instance().screen_similarity_threshold and res_depth == Config.get_instance().UndefineDepth:
                        LogUtils.log_info(
                            f"clickmap--next界面是UndefineDepth&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue

                    if res_sim >= Config.get_instance().screen_similarity_threshold and res_depth > Config.get_instance().curDepth:
                        LogUtils.log_info(
                            f"clickmap--next界面是超过限制层数的&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue

                    # if next_screen_node.get_isWebView():
                    #     LogUtils.log_info(
                    #         f"clickmap--next界面是WebView&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    #     cur_screen_node.already_clicked_cnt += 1
                    #     RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                    #     clickable_ele_idx += 1
                    #     continue

                    if next_screen_node.is_screen_clickable_finished():
                        LogUtils.log_info(f"clickmap--next界面点击完成&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                        clickable_ele_idx += 1
                        continue
                    else:
                        # TODO
                        # if cur_screen_node.is_cur_callmap_finish(next_screen_all_text, ScreenCompareStrategy(LCSComparator())) == False:
                        # click_map指示存在部分没完成
                        cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(
                            cur_clickable_ele_uid)
                        loc_x, loc_y = get_location(cur_clickable_ele_dict)
                        LogUtils.log_info(f"clickmap没完成点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        StatRecorder.get_instance().inc_total_ele_cnt()
                        # 弹框不需要set last node
                        # RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
                        RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)

                        RuntimeContent.get_instance().set_last_screenshot_path(screenshot_path)

                        if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                            cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 0
                        else:
                            cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1

                        cls.__click(loc_x, loc_y)

                        return
                else:
                    LogUtils.log_info(f"已点击过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    cur_screen_node.already_clicked_cnt += 1
                    RuntimeContent.get_instance().already_click_eles.add(cur_clickable_ele_uid)
                    clickable_ele_idx += 1

    @classmethod
    def __remove_eles_notin_popup(cls, cur_node:ScreenNode, ltrb):
        cur_ck_eles = cur_node.clickable_elements
        after_ck_eles = []
        for ele_uid in cur_ck_eles:
            cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(ele_uid)
            loc_x, loc_y = get_location(cur_clickable_ele_dict)
            l,t,r,b=ltrb[0],ltrb[1],ltrb[2],ltrb[3]
            if loc_x > l and loc_x < r and loc_y > t and loc_y < b:
                after_ck_eles.append(ele_uid)
        if len(after_ck_eles) <=0:
            cur_node.clickable_elements = cur_ck_eles
            LogUtils.log_info("在弹框范围内的组件为空")
        else:
            cur_node.clickable_elements = after_ck_eles

    @classmethod
    def __remove_noneed_eles(cls, cur_node:ScreenNode):
        # 移除掉没必要点击的组件
        cur_ck_eles = cur_node.clickable_elements
        after_ck_eles = []
        for ele_uid in cur_ck_eles:
            cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(ele_uid)
            if not is_non_necessary_click(cur_clickable_ele_dict):
                after_ck_eles.append(ele_uid)

        cur_node.clickable_elements = after_ck_eles

    @classmethod
    def create_popup(cls, content):
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        screen_text = get_screen_text_from_context(content)
        # 初始化cur_screen_node信息
        cur_screen_node = ScreenNode()
        cur_screen_node.pkg_name = cur_screen_pkg_name
        cur_screen_node.screen_text = screen_text
        cur_screen_node.activity_name = cur_activity
        cur_ck_eles = content["cur_ck_eles"]
        merged_diff = content["merged_diff"]
        cur_screen_node.clickable_elements = cur_ck_eles
        cur_screen_node.ck_eles_text = ck_eles_text
        cur_screen_node.merged_diff = merged_diff
        # 将cur_screen加入到全局记录的screen_map
        RuntimeContent.get_instance().put_popup_map(ck_eles_text, cur_screen_node)
        return cur_screen_node



    @classmethod
    def handle_system_permission_screen(cls, content):
        LogUtils.log_info("点击系统权限框")
        permission_pattern1 = "com.android.packageinstaller:id/permission_allow_button"
        permission_pattern2 = "com.android.permissioncontroller:id/permission_allow_button"
        if Config.get_instance().device(resourceId=permission_pattern1).exists:
            Config.get_instance().device(resourceId=permission_pattern1).click()
            time.sleep(Config.get_instance().get_sleep_time_sec())
        elif Config.get_instance().device(resourceId=permission_pattern2).exists:
            Config.get_instance().device(resourceId=permission_pattern2).click()
            time.sleep(Config.get_instance().get_sleep_time_sec())
        else:
            cur_screen_node = cls.get_system_permission_screen(content)
            content["cur_screen_node"] = cur_screen_node
            cur_screen_node = get_cur_screen_node_from_context(content)
            cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()
            if len(cur_screen_node_clickable_eles)>0:
                cls.random_click_ele(content)
            else:
                cls.handle_popup_finish(content)

    @classmethod
    def handle_inputmethod(cls, content):
        cls.__press_back()
        # 输入法不需要处理
        # RuntimeContent.get_instance().set_last_screen_node(None)
        # RuntimeContent.get_instance().set_last_clickable_ele_uid("")

    @classmethod
    def handle_double_press(cls, content):
        cls.__double_press_back()
        RuntimeContent.get_instance().set_last_screen_node(None)
        RuntimeContent.get_instance().set_last_clickable_ele_uid("")
        RuntimeContent.get_instance().set_last_screenshot_path("")

    @classmethod
    def handle_back(cls, content):
        cur_screen_node = cls.get_special_screen(content)
        cls.__add_call_graph(cur_screen_node)
        # cur_screen_node.set_isWebView(True)
        content["cur_screen_node"] = cur_screen_node
        # print_screen_info(content, True)
        pre_ck_eles_text = content["ck_eles_text"]
        cls.__press_back()
        LogUtils.log_info("进行回退")
        RuntimeContent.get_instance().set_last_screen_node(None)
        RuntimeContent.get_instance().set_last_clickable_ele_uid("")
        RuntimeContent.get_instance().set_last_screenshot_path("")

        after_ck_eles_text = get_screen_content()["ck_eles_text"]

        # 如果不一样说明文本变化了, 说明一次back即可回退
        sim_flag = is_text_similar(pre_ck_eles_text, after_ck_eles_text)
        if not sim_flag:
            return

        # 如果没变化, 尝试double_press_back
        LogUtils.log_info("一次回退失败, 二次回退")

        cls.__double_press_back()
        after_ck_eles_text = get_screen_content()["ck_eles_text"]
        # 如果不一样说明文本变化了, 说明两次back即可回退
        sim_flag = is_text_similar(pre_ck_eles_text, after_ck_eles_text)
        if not sim_flag:
            return

        # 上述方法都失效,重启
        # RuntimeContent.get_instance().append_error_screen_list(pre_ck_eles_text)
        # cur_screen_node = content.get("cur_screen_node", None)
        # if cur_screen_node is not None:
        #     last_ck_ele_uid_list = cur_screen_node.get_last_ck_ele_uid_list()
        #     RuntimeContent.get_instance().append_more_error_ck_ele_uid_list(last_ck_ele_uid_list)

        LogUtils.log_info("二次回退失败, 重启")
        raise RestartException("重启机制")

    @classmethod
    def handle_exit_app(cls, content):
        cur_screen_node = cls.get_special_screen(content)
        cls.__add_call_graph(cur_screen_node)
        content["cur_screen_node"] = cur_screen_node
        cls.__press_back()
        RuntimeContent.get_instance().set_last_screen_node(None)
        RuntimeContent.get_instance().set_last_clickable_ele_uid("")
        RuntimeContent.get_instance().set_last_screenshot_path("")

    @classmethod
    def handle_finish_screen(cls, content):
        cur_screen_node = cls.get_exist_screen(content)
        # 将cur_screen加入到last_screen的子节点
        cls.__add_call_graph(cur_screen_node)
        pre_ck_eles_text = content["ck_eles_text"]
        cls.__press_back()
        LogUtils.log_info("进行回退")
        RuntimeContent.get_instance().set_last_screen_node(None)
        RuntimeContent.get_instance().set_last_clickable_ele_uid("")
        RuntimeContent.get_instance().set_last_screenshot_path("")

        after_ck_eles_text = get_screen_content()["ck_eles_text"]
        # 如果不一样说明文本变化了, 说明一次back即可回退
        sim_flag = is_text_similar(pre_ck_eles_text, after_ck_eles_text)
        if not sim_flag:
            return

        # 如果没变化, 尝试double_press_back
        LogUtils.log_info("一次回退失败, 二次回退")

        cls.__double_press_back()
        after_ck_eles_text = get_screen_content()["ck_eles_text"]
        # 如果不一样说明文本变化了, 说明两次back即可回退
        sim_flag = is_text_similar(pre_ck_eles_text, after_ck_eles_text)
        if not sim_flag:
            return

        # 上述方法都失效,重启
        # RuntimeContent.get_instance().append_error_screen_list(pre_ck_eles_text)
        # cur_screen_node = content.get("cur_screen_node", None)
        # if cur_screen_node is not None:
        #     last_ck_ele_uid_list = cur_screen_node.get_last_ck_ele_uid_list()
        #     RuntimeContent.get_instance().append_more_error_ck_ele_uid_list(last_ck_ele_uid_list)

        LogUtils.log_info("二次回退失败, 重启")
        raise RestartException("重启机制")

    @classmethod
    def handle_stuck_restart(cls, content):
        cur_screen_node = cls.get_special_screen(content)
        cls.__add_call_graph(cur_screen_node)
        content["cur_screen_node"] = cur_screen_node

        cur_screen_ck_eles_text = content["ck_eles_text"]
        RuntimeContent.get_instance().append_error_screen_list(cur_screen_ck_eles_text)
        # TODO 应该把所有last_clickable_ele_uid加进来
        last_ck_ele_uid = RuntimeContent.get_instance().get_last_clickable_ele_uid()
        if last_ck_ele_uid is not None and last_ck_ele_uid != "":
            RuntimeContent.get_instance().append_error_clickable_ele_uid_list(last_ck_ele_uid)
        cur_screen_node = content.get("cur_screen_node", None)
        if cur_screen_node is not None:
            last_ck_ele_uid_list = cur_screen_node.get_last_ck_ele_uid_list()
            RuntimeContent.get_instance().append_more_error_ck_ele_uid_list(last_ck_ele_uid_list)

        raise RestartException("重启机制")

    @classmethod
    def handle_terminate(cls, content):
        raise TerminateException("完成")

    @classmethod
    def handle_homes_screen_restart(cls, content):
        raise RestartException("重启机制")

    @classmethod
    def __press_back(cls):
        d = Config.get_instance().get_device()
        d.press("back")
        time.sleep(Config.get_instance().get_sleep_time_sec())
        return

    @classmethod
    def __double_press_back(cls):
        d = Config.get_instance().get_device()
        d.press("back")
        d.press("back")
        time.sleep(Config.get_instance().get_sleep_time_sec())
        return

    @classmethod
    def __click(cls, x, y):
        d = Config.get_instance().get_device()
        d.click(x, y)
        time.sleep(Config.get_instance().get_sleep_time_sec())
        return
