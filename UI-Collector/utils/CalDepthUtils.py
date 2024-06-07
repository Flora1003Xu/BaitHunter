import json
from collections import deque
from utils.ScreenCompareUtils import *


class CalDepthUtils:
    @classmethod
    def calDepth(cls, target_uid):
        try:
            depth = cls.bfs("root", target_uid)
            if depth is None:
                depth = Config.get_instance().UndefineDepth
            else:
                depth = depth + 1
        except Exception as e:
            print(e)
            raise Exception
        return depth



    @classmethod
    def bfs(cls, start_uid, target_uid) -> int:
        """
        使用BFS算法遍历邻接表，并计算每个节点的层数
        """
        # 创建一个队列，并将起始节点加入队列中
        queue = deque([(start_uid, 0)])

        # 创建一个集合，用于记录已经访问过的节点
        visited = set()

        while queue:
            # 从队列中取出一个节点
            uid, level = queue.popleft()

            # 如果这个节点已经被访问过了，则跳过
            if uid in visited:
                continue

            # 将这个节点标记为已访问
            visited.add(uid)

            # 输出这个节点的层数
            sim_flag = is_text_similar(uid, target_uid)
            # if uid == target_uid:
            if sim_flag:
                return level

            # 遍历这个节点的所有邻居，并将它们加入队列中
            target_screen = CalDepthUtils.indexScreen(uid)
            for key, value in target_screen.call_map.items():
                queue.append((value.ck_eles_text, level + 1))

        return None


    @classmethod
    def indexScreen(cls, target_uid):
        res_node = get_screennode_from_screenmap_by_similarity(target_uid)
        if res_node is None:
            raise Exception("indexScreen func: node为空")
        return res_node

