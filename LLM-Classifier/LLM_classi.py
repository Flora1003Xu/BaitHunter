from http import HTTPStatus
import dashscope
import os
import json
import time

dashscope.api_key = '******' # your api_key
prompt_file = 'prompt_COT.txt'

def read_json(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return json.load(file)

def read_and_replace_prompt(json_content1, json_content2, a_name, b_name):
    with open(prompt_file, 'r', encoding='utf-8') as file:
        content = file.read()
        content = content.replace("{json1}", json.dumps(json_content1, ensure_ascii=False))
        content = content.replace("{json2}", json.dumps(json_content2, ensure_ascii=False))
        content = content.replace("{fff_uuu}", a_name)
        content = content.replace("{ttt_uuu}", b_name)
        return content


def write_result(folder_path, result):
    start_index = result.find('{')
    end_index = result.rfind('}')
    if start_index != -1 and end_index != -1:
        json_content = result[start_index:end_index + 1]
        result_path = os.path.join(folder_path, 'result.json')
        with open(result_path, 'w', encoding='utf-8') as file:
            file.write(json_content)
    else:
        print("Invalid JSON format",folder_path)


def write_error_result(folder_path, response):
    result_path = os.path.join(folder_path, 'error_result.txt')
    with open(result_path, 'w', encoding='utf-8') as file:
        file.write(response.code)
        file.write(response.message)


def process_folder(folder_path,before_name,after_name):
    json_content1 = None
    json_content2 = None
    a_name = ""
    b_name = ""

    # A and beforeJump_A.json
    for item in os.listdir(folder_path):
        if item.startswith('beforeJump_') and item.endswith('.json') and item[11:-5]==before_name:
            json_content1 = read_json(os.path.join(folder_path, item),encoding='gb2312')
        if item.endswith('.json') and item[:-5]==before_name:
            json_content2 = read_json(os.path.join(folder_path, item), encoding='gb2312')


    if json_content1 and json_content2 and a_name and b_name:
        prompt = read_and_replace_prompt(json_content1, json_content2, a_name, b_name)
        print(prompt)
        response = dashscope.Generation.call(
            model='qwen-max-longcontext',
            prompt=prompt,
            temperature=1.5
        )
        if response.status_code == HTTPStatus.OK:
            result = response.output["text"]
            write_result(folder_path, result)
        else:
            print(response.code)  # The error code.
            print(response.message)  # The error message.
            exit()
    else:
        print("prompt error")


def LLM(folder_path, before_name, after_name):
    process_folder(folder_path,before_name,after_name)