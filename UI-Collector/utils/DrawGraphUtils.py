# 介绍:
# 根据邻接表(图的数据结构表示)建立App界面之间的跳转图, 比如界面A点击了某个按钮跳转到了界面B, 则表示A->B
# privacy_policy/dumpjson 目录下的每个json文件表示一个App界面之间跳转的邻接表
# 以app.podcast.cosmos_restart0activity41&screen248&time2844.76s文件举例, 该文件表示的是App包名为app.podcast.cosmos(该App为小宇宙)的界面跳转图
# 观察其json结构, ck_eles_text表示的是该界面的screen_uid(可点击组件的文本和位置信息),即通过这个screen_uid我们可以唯一标识这个界面
# nextlist表示的是从某个界面出发, 能到达的其他界面(注意其他界面也以screen_uid表示)
# call_map同样表示从某个界面触发能到达的其他界面, 是一个map{key, value}, 表示通过点击某个按钮(key:clickable_ele_uid)到达的其他界面(value:screen_uid)
# call_map和nextlist还有不同的地方就是nextlist可能存在环, 比如A->B->C->A, call_map是无环图

# 此外, 另外一个同学在做的是将界面截图收集起来, 并且将界面的screen_uid进行encode, 界面截图的文件命名为encode(screen_uid)
# ScreenshotUtils.py还会提供函数进行decode, 使得decode(encode(screen_uid)) = screen_uid

# 任务:根据App界面截图和json邻接表, 建立一个App界面之间的跳转图, 并且可视化出来

import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from PIL import Image
from utils.ScreenshotUtils import *

class DrawGraphUtils:

    @staticmethod
    def draw_callgraph(package):
        result = DrawGraphUtils.load_data(package)
        num_objects, graph, pos = result

        # 获取截图
        screenShotFilePath = os.path.join("./collectData", package, "Screenshot", "ScreenshotPicture")
        screenshot_folder = os.path.abspath(screenShotFilePath)
        screenshot_files = {node: os.path.join(screenshot_folder, f'{ScreenshotUtils.encode_screen_uid(node)}.png') for node in graph.nodes}
        nx.set_node_attributes(graph, screenshot_files, 'image')

        # 画图
        fig, ax = plt.subplots(figsize=(100, 150))
        plt.axis('off')

        node_size = 1000
        length_to_width_ratio = 1.5

        # 调整截图位置和比例
        for node in graph.nodes:
            x, y = pos[node]
            img_path = graph.nodes[node]['image']
            img = Image.open(img_path)
            resized_img = img.resize((node_size, int(node_size * length_to_width_ratio)))
            img_width, img_height = img.size

            x -= img_width / 2
            y -= img_height / 2
            ax.imshow(resized_img, extent=(x, x + img_width, y, y + img_height), zorder=2, interpolation='nearest')

        # 画边
        nx.draw_networkx_edges(graph, pos, ax=ax, width=1.5, edge_color='gray', arrows=False, alpha=0.1)
        for edge in graph.edges():
            start_node = edge[0]
            end_node = edge[1]
            x_start, y_start = pos[start_node]
            x_end, y_end = pos[end_node]
            arrow_pos_x = (x_start + x_end) / 2
            arrow_pos_y = (y_start + y_end) / 2

            cl = graph.edges[edge]['color']
            l_w = -0.015 * num_objects + 5.5
            m_s = -0.25 * num_objects + 85

            arrow_connection = ConnectionPatch((x_start, y_start), (arrow_pos_x, arrow_pos_y),
                                               "data", "data", arrowstyle='->', color=cl, alpha=0.8, linewidth=l_w, mutation_scale=m_s)
            next_connection = ConnectionPatch((arrow_pos_x, arrow_pos_y), (x_end, y_end),
                                              "data", "data", arrowstyle='-', color=cl, alpha=0.8, linewidth=l_w, mutation_scale=m_s)
            ax.add_artist(arrow_connection)
            ax.add_artist(next_connection)

        DrawGraphUtils.save_data(package)

    @staticmethod
    def load_data(package):
        # 读取json文件，返回界面数量、跳转关系和画图位置
        jsonFilePath = os.path.join("./collectData", package, "Dumpjson")
        jsonFilePath = os.path.abspath(jsonFilePath)
        files = os.listdir(jsonFilePath)
        for file in files:
            if file.endswith('.json'):
                json_file_name = file
                break
        jsonFilePath = os.path.join(jsonFilePath, json_file_name)

        with open(jsonFilePath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            num_objects = len(data)

            graph = nx.DiGraph()
            pos = {}

            record_pos = {}
            x_root = 0
            y_root = 0
            x_space = 3000
            y_space = 6000
            virtual_root_flag = 1
            root_flag = 1
            root_count = 0
            edge_color = 'orange'

            for obj in data:
                ck_eles_text = obj["ck_eles_text"]
                nextlist = obj["nextlist"]
                call_map = obj["call_map"]

                # 虚拟根节点
                if virtual_root_flag:
                    virtual_root_flag = 0
                    continue

                # 初始根节点
                if root_flag and not virtual_root_flag:
                    graph.add_node(ck_eles_text)
                    pos[ck_eles_text] = (x_root, y_root)
                    record_pos[y_root] = x_root
                    root_flag = 0

                # 遍历完一支后新的根节点
                if not graph.has_node(ck_eles_text):
                    graph.add_node(ck_eles_text)
                    root_count += 1

                    if len(nextlist) > 0 and graph.has_node(nextlist[0]) and nextlist[0] in pos:
                        _, y_nxt = pos[nextlist[0]]
                        # y:放置在后续第一个子节点的上方y_space/2处
                        y_new = y_nxt + y_space / 2
                        # x:放置在y高度线上最右边节点的旁边
                        x_record = [x for y, x in record_pos.items() if y == y_nxt]
                        if len(x_record) > 0:
                            max_x_record = max(x_record)
                            x_new = max_x_record + x_space
                        else:
                            x_new = x_root + root_count * x_space

                        record_pos[y_nxt] = x_new
                    else:
                        y_new = y_root

                        x_record = [x for y, x in record_pos.items() if y == y_root]
                        if len(x_record) > 0:
                            max_x_record = max(x_record)
                            x_new = max_x_record + x_space

                        record_pos[y_root] = x_new

                    pos[ck_eles_text] = (x_new, y_new)

                x_parent, y_parent = pos[ck_eles_text]
                num = len(nextlist)
                x_first = x_parent - num * x_space / 2
                order = 0

                if edge_color == 'orange':
                    edge_color = 'cyan'
                else:
                    edge_color = 'orange'

                # 子节点
                for nxt in nextlist:
                    if not graph.has_node(nxt):
                        graph.add_node(nxt)
                        # x: 在父节点正下方散开
                        x_child = x_first + order * x_space
                        order += 1
                        # y：放在父节点下方y_space处
                        y_child = y_parent - y_space

                        pos[nxt] = (x_child, y_child)
                        record_pos[y_child] = x_child

                    if nxt is not None and ck_eles_text != nxt:
                        graph.add_edge(ck_eles_text, nxt, color=edge_color)

                for _, target in call_map.items():
                    if target is not None and ck_eles_text != target:
                        graph.add_edge(ck_eles_text, target, color=edge_color)

        return num_objects, graph, pos

    @staticmethod
    def save_data(package):
        # 保存svg图像，图像与文件夹同名
        svgSaveFilePath = os.path.join("./collectData", package, "AppCallGraph")
        svg_save_folder = os.path.abspath(svgSaveFilePath)

        if not os.path.exists(svg_save_folder):
            os.makedirs(svg_save_folder)

        svg_save_name = package + ".svg"
        plt.savefig(os.path.join(svg_save_folder, svg_save_name), bbox_inches='tight', dpi=300)