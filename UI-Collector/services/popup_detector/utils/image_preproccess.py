import cv2 as cv
import os
import numpy as np

class Preproccess:
    def __init__(self, input_image):
        self.input_image = input_image
        self.pic_name = os.path.basename(input_image)

        # 解析输入路径
        path_parts = input_image.split("/")
        symbol = "/"
        folder_path = symbol.join(path_parts[:-2])

        # 构建输出路径
        output_folder = "PreprocessedPicture"
        output_dir = folder_path + "/" + output_folder
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.output_dir = output_dir   # 处理后放入的文件夹


    def enhance_edge(self, image):
        # 边缘检测
        blurred = cv.GaussianBlur(image, (3, 3), 0)
        gray = cv.cvtColor(blurred, cv.COLOR_RGB2GRAY)
        edge_output = cv.Canny(gray, 50, 150)
        dst = cv.bitwise_and(image, image, mask=edge_output)
        return dst

    def enhance_contrast(self, image, brightness_factor, contrast_factor):
        # 调整亮度
        brightened = cv.convertScaleAbs(image, alpha=brightness_factor)
        # 调整对比度
        lab = cv.cvtColor(brightened, cv.COLOR_BGR2LAB)
        lab_planes = list(cv.split(lab))
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab_planes[0] = clahe.apply(lab_planes[0])
        lab = cv.merge(lab_planes)
        contrasted = cv.cvtColor(lab, cv.COLOR_LAB2BGR)

        return contrasted

# 训练时
# input_dir = "../data/train/images"
# output_dir = "../data/train/images"
#
# input_dir = "../data/valid/images"
# output_dir = "../data/valid/images"
    def preproccess(self):
        # 检测时
        input_image = self.input_image
        output_dir = self.output_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        image = cv.imread(input_image)
        image_canny = self.enhance_edge(image)
        kernel = np.ones((1,1), np.uint8)
        image_canny = cv.erode(image_canny, kernel)
        brightness_factor = 1
        contrast_factor = 1.
        output_image = self.enhance_contrast(image_canny, brightness_factor, contrast_factor)
        output_path = os.path.join(output_dir, self.pic_name)
        cv.imwrite(output_path, output_image)

        return output_path





