import threading, time
from queue import Queue

import os
import sys
from pathlib import Path
import detect_queue

from services.popup_detector.utils.image_preproccess import Preproccess
from services.popup_detector.utils.redraw import Redraw
from services.popup_detector.utils.image_prejudge import Prejude

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


from services.popup_detector.utils.general import check_requirements

lock = threading.Lock()


class YoloService(threading.Thread):
    def __init__(
            self,
            t_name: str,
            req_queue: Queue,
            resp_queue: Queue,
            daemon: bool,
            opt= {
                'weights': ROOT / 'runs/train/exp15/weights/best.pt',  # model path or triton URL
                'source': ROOT / 'data_detect/images_origin',  # file/dir/URL/glob/screen/0(webcam)
                'data': ROOT / 'data/coco128.yaml',  # dataset.yaml path
                'imgsz': (640, 640),  # inference size (height, width)
                'conf_thres': 0.5,  # confidence threshold
                'iou_thres': 0.45,  # NMS IOU threshold
                'max_det': 1000,  # maximum detections per image
                'device': '',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
                'view_img': False,  # show results
                'save_txt': True,  # save results to *.txt
                'save_csv': False,  # save results in CSV format
                'save_conf': True,  # save confidences in --save-txt labels
                'save_crop': False,  # save cropped prediction boxes
                'nosave': True,  # do not save images/videos
                'classes': None,  # filter by class: --class 0, or --class 0 2 3
                'agnostic_nms': False,  # class-agnostic NMS
                'augment': False,  # augmented inference
                'visualize': False,  # visualize features
                'update': False,  # update all models
                'project': ROOT / 'runs/detect',  # save results to project/name
                'name': 'exp',  # save results to project/name
                'exist_ok': False,  # existing project/name ok, do not increment
                'line_thickness': 3,  # bounding box thickness (pixels)
                'hide_labels': False,  # hide labels
                'hide_conf': False,  # hide confidences
                'half': False,  # use FP16 half-precision inference
                'dnn': False,  # use OpenCV DNN for ONNX inference
                'vid_stride': 1,  # video frame-rate stride):
            }
    ):  # opt是字典类型
        threading.Thread.__init__(self, name=t_name, daemon=daemon)
        self.req_queue = req_queue
        self.resp_queue = resp_queue
        self.opt = opt

        check_requirements(ROOT / 'requirements.txt', exclude=('tensorboard', 'thop'))

        device, model, stride, names, pt, imgsz = detect_queue.load_model(opt['weights'], opt['device'], opt['dnn'],
                                                                          opt['data'], opt['half'], opt['imgsz'])

        self.device, self.model, self.stride, self.names, self.pt, self.imgsz = device, model, stride, names, pt, imgsz

    #    save_img, screenshot, save_dir, webcam = detect_queue.input_save(self.opt['source'], self.opt['save_txt'], self.opt['nosave'], self.opt['project'], self.opt['name'], self.opt['exist_ok'])

    #    self.save_img, self.screenshot, self.save_dir, self.webcam = save_img, screenshot, save_dir, webcam

    def processImage(self, image):

        source = image

        prejude_instance = Prejude(image)
        Prejude_result = prejude_instance.process_images()
        print("Prejude_result = " + str(Prejude_result))

        xywh = []
        conf = 0

        # 有分层现象
        if  Prejude_result:
            save_img, screenshot, save_dir, webcam = detect_queue.input_save(image, self.opt['save_txt'],
                                                                            self.opt['nosave'], self.opt['project'],
                                                                            self.opt['name'], self.opt['exist_ok'])

            # 图片预处理
            ImagePre = Preproccess(image)
            get_prepro_pic_path = ImagePre.preproccess()
            source = get_prepro_pic_path

            # 图片检测
            bs, dataset, vid_path, vid_writer = detect_queue.data_loader(False, source, self.imgsz, self.stride, self.pt,
                                                                        self.opt['vid_stride'], False)
            self.bs, self.dataset, self.vid_path, self.vid_writer = bs, dataset, vid_path, vid_writer
            self.save_img, self.screenshot, self.save_dir, self.webcam = save_img, screenshot, save_dir, webcam

            seen, dt, xywh, conf = detect_queue.run_inference(
                self.model,
                self.pt,
                bs,
                self.imgsz,
                dataset,
                self.opt['augment'],
                self.opt['conf_thres'],
                self.opt['iou_thres'],
                self.opt['classes'],
                self.opt['agnostic_nms'],
                self.opt['max_det'],
                self.save_dir,
                self.webcam,
                self.opt['save_crop'],
                self.opt['line_thickness'],
                self.names,
                self.opt['hide_conf'],
                self.opt['view_img'],
                self.save_img,
                vid_path,
                vid_writer,
                self.opt['save_txt'],
                self.opt['save_conf'],
                self.opt['hide_labels'],
                self.opt['save_csv'],
                self.opt['visualize'])

        # 无分层现象
        else:
            xywh = []
            conf = 0

        return xywh, conf

    def run(self):
        while True:
            try:
                # 从请求队列得到图片
                image = self.req_queue.get(block=True)
                print(f"{self.name} get {image} from req_queue")

                # 处理逻辑
                print(f"{self.name} process.....")
                xywh, conf = self.processImage(image)
                result = {'xywh': xywh, 'conf': conf}

                # 将处理后的结果放到响应队列
                self.resp_queue.put(result, block=True)
                print(f"{self.name} put {result} into resp_queue")

                # 在原图上绘制结果
                redraw = Redraw(image, xywh, conf)
                redraw.redraw()

                # # 休眠1s
                # time.sleep(2)

            except Exception as e:
                print(e)
                break
        print(f"{self.name} exit....")
