from queue import Queue
from query_service import QueryService
from services.popup_detector import detect_queue
from services.popup_detector.yolo_service import YoloService

def main(opt):
    req_queue = Queue(1)
    resp_queue = Queue(1)
    producer = QueryService('QueryImagePopupService', req_queue, resp_queue, False, opt['source'])
    consumer = YoloService('YoloDetectPopupService', req_queue, resp_queue, True, opt)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
    print('All threads terminate!')

if __name__ == '__main__':
    opt = detect_queue.parse_opt()   # <class 'argparse.Namespace'>
    main(vars(opt))
