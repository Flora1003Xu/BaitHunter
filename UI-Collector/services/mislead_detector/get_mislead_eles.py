import json
import requests

def get_mislead_eles(img_path:str):
    img1=open(img_path,'rb')
    file_resq={
        "file":img1
    }
    res=requests.post("http://172.16.108.178:5185/ocr",files=file_resq)
    print(res.text)
    res_dict = json.loads(res.text)
    # for ele in res_dict["res"]:
    #     print(ele["text"], " ", ele["xywh"])
    return res_dict["res"]


