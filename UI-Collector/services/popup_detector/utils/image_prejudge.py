import cv2
import numpy as np
import os

class Prejude:
    def __init__(self, image):
        # self.data_folder = data_folder
        self.image = image

    def has_brightness_layers(self, image_path):
        image = cv2.imread(image_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        mean_value = np.mean(binary)
        if mean_value < 200:
            # print(image_path, "图像中有明暗度分层，可能存在弹窗界面。")
            return True
        else:
            # print(image_path, "图像中没有明暗度分层，可能没有弹窗界面.")
            return False

    def process_images(self):
        # all_files = os.listdir(self.data_folder)

        # for file_name in all_files:
        #     if file_name.lower().endswith(".png"):
        #         image_path = os.path.join(self.data_folder, file_name)
        #         self.has_brightness_layers(image_path)

        result = self.has_brightness_layers(self.image)

        return result










