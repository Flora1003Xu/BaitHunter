
class ScreenNode:
    def __init__(self):
        # 包名 + activity + 可点击组件的内部文本
        # self.sig = ""
        # 所有可点击组件的文本和位置
        self.ck_eles_text = ""
        # # 当前screen的上一个screen
        # self.parent = None
        # 当前screen的下一个screen
        self.children = []
        # 记录着当前screen的所有可点击组件uid
        self.clickable_elements = None
        self.diff_clickable_elements = None
        self.merged_diff = -1
        self.pkg_name = ""
        self.activity_name = ""
        # 所有组件的文本,包括不可点击组件的文本
        self.screen_text = ""
        # call_map:{key:widget_uuid, value: next_screen_node}
        # call_map主要记录哪些组件能到达下一个Screen
        self.call_map = {}
        # 记录是否是WebView
        self.isWebView = False
        # cycle_set记录了哪些组件产生回边
        self.cycle_set = set()
        # 记录哪些候选的随机点击组件
        self.candidate_random_clickable_eles = []
        # 记录每个组件的uid的点击次数 {key:cur_clickable_ele_uid, val:cnt}
        self.ele_uid_cnt_map = {}
        # 记录组件是否有被点击过 {key:cur_clickable_ele_uid, val:true/false}
        self.ele_vis_map = {}
        # 记录当前screen已经被点击过的组件个数, 遍历层数增加时会重置
        self.already_clicked_cnt = 0
        # 记录当前screen已经被点击过的组件个数, 不会重置
        self.total_clicked_cnt = 0
        # 最近一次到达当前界面所点击的上一个界面的组件uid
        self.last_ck_ele_uid_list = []


    def update_callmap_item(self, ele_uid:str) -> bool:
        if ele_uid in self.call_map:
            del self.call_map[ele_uid]
            return True
        else:
            return False

    def append_last_ck_ele_uid_list(self, uid):
        self.last_ck_ele_uid_list.append(uid)

    def get_last_ck_ele_uid_list(self):
        return self.last_ck_ele_uid_list


    def build_candidate_random_clickable_eles(self):
        for key, val in self.call_map.items():
            self.candidate_random_clickable_eles.append(key)
        for item in self.cycle_set:
            self.candidate_random_clickable_eles.append(item)
        return self.candidate_random_clickable_eles


    def get_diff_or_clickable_eles(self):
        if self.diff_clickable_elements is None:
            return self.clickable_elements
        else:
            return self.diff_clickable_elements

    def get_exactly_clickable_eles(self):
        return self.clickable_elements

    # 判断当前Screen是否点完了
    def is_screen_clickable_finished(self):
        if self.clickable_elements is None:
            raise Exception
        if self.diff_clickable_elements is None:
            if self.already_clicked_cnt == len(self.clickable_elements):
                return True
            else:
                return False
        else:
            if self.already_clicked_cnt == len(self.diff_clickable_elements):
                return True
            else:
                return False
    
    def add_child(self, child):
        # child.parent = self
        if child not in self.children:
            self.children.append(child)

    
    # def find_ancestor(self, target_screen_all_text):
    #     cur = self
    #     par = cur.parent
    #     while par is not None:
    #         if par.all_text == target_screen_all_text:
    #             return True
    #         cur = par
    #         par = cur.parent
    #     # print(cur.value)
    #     return False

    
    # 只检测level1的children是否全部完成
    # def is_cur_callmap_finish(self, target_screen_all_text):
    #     if self is None:
    #         return True
    #     # for child_node in self.children:
    #     #     if screen_compare_strategy.compare_screen(child_node.all_text, target_screen_all_text)[0] == True:
    #     #     # if child_node.all_text == target_screen_all_text:
    #     #         if child_node.already_clicked_cnt == len(child_node.clickable_elements):
    #     #             return True
    #     #         else:
    #     #             return False
    #     # return True
    #     # 根据call_map来找,其实call_map和children差不多,区别就是children有回边,call_map没有
    #     #TODO
    #     for child_node in self.call_map.values():
    #         sim = compare_sreen_similarity(child_node.ck_eles_text, target_screen_all_text)
    #         if sim >= Config.get_instance().screen_similarity_threshold:
    #         # if child_node.all_text == target_screen_all_text:
    #         #     if child_node.already_clicked_cnt == len(child_node.clickable_elements):
    #             if child_node.is_screen_clickable_finished():
    #                 return True
    #             else:
    #                 return False
    #     return True

    def set_isWebView(self, flag):
        self.isWebView = flag

    def get_isWebView(self):
        return self.isWebView

    def __hash__(self):
        return hash((self.ck_eles_text))

    def __eq__(self, other):
        return self.ck_eles_text == other.ck_eles_text


            