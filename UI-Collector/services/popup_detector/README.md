# 功能:识别弹窗
1. 输入：
![200017](https://github.com/MayBiscuit/popUpRecognition/assets/92511471/904ffa14-26d9-4cbc-8514-6673e82e1170)
![200018](https://github.com/MayBiscuit/popUpRecognition/assets/92511471/a934c11b-e465-4d68-abd4-6a9f5b4ee4c4)

2. 输出：
![200017_drawn](https://github.com/MayBiscuit/popUpRecognition/assets/92511471/296a18b9-872a-4b16-9792-77c45fa03e75)
![200018_drawn](https://github.com/MayBiscuit/popUpRecognition/assets/92511471/e47f9d03-1f58-48a0-87ba-bf98d996fa93)


# 训练方式
1. 将标注数据放置于data_train文件夹内
2. 修改路径并运行 python .\utils\image_preprocess.py
3. 运行 python train.py --batch-size 2 --epochs 200 --data data_train/pop_ups.yaml --weights weight/yolov5m.pt

# 使用方式
1. 将待识别图片保存在 data_detect\images_origin 文件夹下
2. 修改文件内路径并运行 python .\utils\image_preprocess.py
3. 运行 python .\detect.py --source .\data\images_pop_ups --weights .\runs\train\exp15\weights\best.pt --save-txt --save-conf
4. 修改文件内路径并运行 python .\utils\redraw.py
5. 结果保存在 data_detect\images_detected下

# 其他
1. 权重文件在.\runs\train\exp15\weights\best.pt下
2. 标注数据结构：
![image](https://github.com/MayBiscuit/popUpRecognition/assets/92511471/587d871f-6ff5-49c8-8430-34315fa5d078)
