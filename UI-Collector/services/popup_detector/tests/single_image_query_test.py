from queue import Queue
from utils.DeviceUtils import *
from services.popup_detector import detect_queue
from services.popup_detector.yolo_service import YoloService

import os

if __name__ == '__main__':
    req_queue = Queue(1)
    resp_queue = Queue(1)
    consumer = YoloService('YoloDetectPopupService', req_queue, resp_queue, True)
    consumer.start()
    img_path = "G:\AppUIAutomator2Navigation\collectData\com.cainiao.wireless-20231120-110057\Screenshot\ProcessedScreenshotPicture\BTFWhqpsXASzfETiBYAWeCR2LzTkCf_Or26p6hCJLWc=.png"
    # img_path = "G:\AppUIAutomator2Navigation\collectData\com.taobao.taobao-20231026-195435\Screenshot\ScreenshotPicture\iQEcAqNqcGcDAQTNBDgFzQlgBtoAI4QBpCEIeOwCqnFkhm25U4EO3VoDzwAAAYuo-uEDBM4Ann_NBwAIAAoE.jpg_720x720q90.jpg"
    # 将图片放到请求队列, 如果队满则阻塞, 阻塞时长timeout则异常
    req_queue.put(img_path, block=True)
    print(f"put {img_path} into req_queue")

    # 从响应队列获取结果, 如果空则阻塞, 阻塞时长timeout则异常
    data = resp_queue.get(block=True)
    print(f"get {data} from resp_queue")

    coord_dict = get_4corner_coord(data['xywh'])
    print(coord_dict)
    consumer.join()
    print('All threads terminate!')
