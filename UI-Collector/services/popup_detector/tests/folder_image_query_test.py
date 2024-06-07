from queue import Queue

from services.popup_detector import detect_queue
from services.popup_detector.yolo_service import YoloService

import os

if __name__ == '__main__':
    opt = vars(detect_queue.parse_opt())  # <class 'argparse.Namespace'>
    image_folder = "G:\AppUIAutomator2Navigation\collectData\com.alibaba.aliyun-20231129-210548\Screenshot\ScreenshotPicture"
    req_queue = Queue(1)
    resp_queue = Queue(1)
    consumer = YoloService('YoloDetectPopupService', req_queue, resp_queue, True, opt)
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder)]
    consumer.start()
    for img_path in image_paths:
        # 将图片放到请求队列, 如果队满则阻塞, 阻塞时长timeout则异常
        req_queue.put(img_path, block=True)
        print(f"put {img_path} into req_queue")

        # 从响应队列获取结果, 如果空则阻塞, 阻塞时长timeout则异常
        data = resp_queue.get(block=True)
        print(f"get {data} from resp_queue")

    consumer.join()
    print('All threads terminate!')
