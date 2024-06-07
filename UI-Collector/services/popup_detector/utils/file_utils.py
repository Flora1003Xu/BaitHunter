import os

# 修改文件名，格式为六位数
# 0开头是训练正样本，1开头是训练负样本，2开头是待预测图片
def change_filename(path, prefix):
    image_folder = path
    start_index = prefix

    for index, file in enumerate(sorted(os.listdir(image_folder))):
        if file.endswith(".jpg") or file.endswith(".png"):
            file_extension = os.path.splitext(file)[1]

            new_filename = f"{start_index + index + 1}.jpg"

            original_file_path = os.path.join(image_folder, file)
            new_file_path = os.path.join(image_folder, new_filename)
            os.rename(original_file_path, new_file_path)

# 为每个负样本图片生成空txt
def make_empty_txt(in_path, out_path):
    image_folder = in_path
    txt_folder = out_path

    os.makedirs(txt_folder, exist_ok=True)

    for file in os.listdir(image_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            image_filename = os.path.splitext(file)[0]
            txt_filename = f"{txt_folder}/{image_filename}.txt"

            with open(txt_filename, "w") as f:
                pass

name_unchanged_file_folder = "../data_detect/images_origin"
name_prefix = 200000
negative_image_folder = "./pop_up_data_negative"
negative_txt_folder = "./pop_up_data_negative"

change_filename(name_unchanged_file_folder, name_prefix)
# make_empty_txt(negative_image_folder, negative_txt_folder)

