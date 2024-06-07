import os
import random
import threading, time
from queue import Queue

lock = threading.Lock()

from services.popup_detector.utils.redraw import Redraw

from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


class QueryService(threading.Thread):
    def __init__(self, t_name: str, req_queue: Queue, resp_queue: Queue, daemon: bool, source: str):
        threading.Thread.__init__(self, name=t_name, daemon=daemon)
        self.req_queue = req_queue
        self.resp_queue = resp_queue
        self.source = source

    def getImage(self, index):

        image_folder = self.source
        image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder)]

        # 从文件夹中拿出图片返回
        if index < len(image_paths):
            return image_paths[index]
        else:
            return False

    def run(self):
        index = 0  # 图片索引
        time_out = 0  # 计时器

        while True:
            try:
                image_path = self.getImage(index)
                index += 1

                # 将每个图片路径放入队列中
                if image_path:
                    # 清空计时器
                    time_out = 0

                    # 将图片放到请求队列, 如果队满则阻塞, 阻塞时长timeout则异常
                    self.req_queue.put(image_path, block=True, timeout=5)
                    print(f"{self.name} put {image_path} into req_queue")

                    # 从响应队列获取结果, 如果空则阻塞, 阻塞时长timeout则异常
                    data = self.resp_queue.get(block=True, timeout=5)
                    print(f"{self.name} get {data} from resp_queue")

                    # 休眠1s
                    time.sleep(2)

                else:
                    time.sleep(2)
                    time_out += 1
                    # 空文件夹超时时间
                    if time_out >= 5:
                        break

            except Exception as e:
                print(e)
                break

        print(f"{self.name} exit....")
