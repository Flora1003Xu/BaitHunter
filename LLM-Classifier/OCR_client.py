import json
import os
import requests
from LLM_classi import LLM

def ocr(folder_path,click_x, click_y,beforeJump_name, afterJump_name):
    for files in os.listdir(folder_path):
        for file in files:
            if not file.endswith('png') and not file.endswith('jpg'):
                continue
            filename = file.split('.')[0]
            process = 0
            if filename == beforeJump_name or filename == afterJump_name:
                process+=1
                file_path = os.path.join(folder_path, file)
                with open(file_path, 'rb') as img1:
                    file_resq = {
                        "file": img1
                    }
                    res = requests.post("http://172.16.108.178:2020/ocr", files=file_resq)
                    output_path = os.path.join(folder_path, filename + ".json")
                    with open(output_path, "w") as f:
                        json.dump(res.json(), f, ensure_ascii=False, indent=4)

                    if filename != beforeJump_name:
                        continue
                    with open(output_path, 'r') as f:
                        ocr_data = json.load(f)
                    file_resq = {
                        "file": img1
                    }
                    ocr_data_json = json.dumps(ocr_data)

                    data = {
                        "click_x": click_x,
                        "click_y": click_y,
                        "ocr": ocr_data_json
                    }

                    res = requests.post("http://172.16.108.178:8888/yolo", files=file_resq, data=data)
                    print(res.text)
                    output_cv_path = os.path.join(folder_path, 'beforeJump_'+filename + ".json")
                    with open(output_cv_path, "w",
                              encoding='gb2312') as f:
                        json.dump(res.json(), f, ensure_ascii=False, indent=4)

            if process==2:
                LLM(folder_path,beforeJump_name,afterJump_name)
