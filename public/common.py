import json
import time


# 读取json文件
def get_json_data(file_path):
    with(open(file_path, "r", encoding='UTF-8')) as f:
        json_data = json.loads(f.read())
    return json_data


# 获取时间戳，默认返回格式为2021-07-21 12:12:12
def get_now_str(form='%Y-%m-%d %H:%M:%S'):
    return time.strftime(form, time.localtime())


