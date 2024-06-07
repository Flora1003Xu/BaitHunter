from OCR_client import ocr
import os
import time


if __name__ == '__main__':
    for root, dirs, files in os.walk("./data/", topdown=False):
        for name in dirs:
            folder_path = os.path.join(root, name)
            print("running data from",folder_path)
            beforeJump_name = input("Please enter the file name before the jump:")
            afterJump_name = input("Please enter the file name after the jump:")
            print("Please enter your click coordinates")
            click_x = input("Enter click_x value: ")
            click_y = input("Enter click_y value: ")

            ocr(folder_path,click_x, click_y,beforeJump_name, afterJump_name)
            time.sleep(50)  # [optional] to avoid QPS limits

