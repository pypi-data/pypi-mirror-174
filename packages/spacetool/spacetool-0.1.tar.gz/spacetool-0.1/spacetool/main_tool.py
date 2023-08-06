# -*- coding:utf-8 -*-
import requests, json, time
from urllib import parse

def requests_post(url, payload):
    headers = {"content-type": "application/json", "Accept": "*/*"}
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    return res

def requests_get(url, params):
    headers = {"content-type": "application/json", "Accept": "*/*"}
    res = requests.get(url, params=params, headers=headers)
    return res

class DataTool:
    """
    获取停车场信息；
    上传停车场信息；
    获取停车场采集记录信息；
    上传停车场采集记录信息；
    """
    def __init__(self, name, code, host="http://192.168.0.155:8000/"):
        self.name = name               # 用户name
        self.code = code               # 用户code
        self.uid = None                # 用户ID
        # self.temp_carparking_name = "carparking_name"
        # self.temp_unique_time_string = "unique_time_string"
        self.host = host               # api Domain

        # assert self.temp_carparking_name, "请携带正确的停车场名称"
        # assert self.host, "请携带api host"

        self.car_parking_serial_id_url = parse.urljoin(self.host, "ods/car_parking_serial_id_handler/")
        self.collection_record_serial_id_url = parse.urljoin(self.host, "ods/collection_record_serial_id_handler/")
        self.check_code_url = parse.urljoin(self.host, "ods/check_code/")
        self.update_code_url = parse.urljoin(self.host, "ods/update_code/")
        self.car_parking_serial_id = None
        self.collection_record_serial_id = None
        self.check_code()              # 用户校验

    def check_code(self):
        # 用户校验
        res = requests_post(self.check_code_url, {"name": self.name, "code": self.code})
        assert res.status_code == 200, f"请求有错，errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        self.uid = json_data['data']['uid']
        return json_data['data']

    def update_code(self, new_code):
        # 用户更新code
        assert 4 <= len(new_code) <= 10, "请输入长度为4～10的新code"
        res = requests_post(self.update_code_url, {"name": self.name, "code": self.code, "new_code": new_code})
        assert res.status_code == 200, f"请求有错，errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        self.uid = json_data['data']['uid']
        return json_data['data']

    def upload_car_parking_info(self, carparking_name, city="城市", district="区", address="地址", update=False):
        carparking_name = carparking_name.strip()
        if not carparking_name.endswith("停车场"):
            carparking_name = carparking_name + "停车场"
        res = requests_post(self.car_parking_serial_id_url, {
            "carparking_name": carparking_name,
            "city": city,
            "district": district,
            "address": address,
            "uid": self.uid
        })
        assert res.status_code == 200, f"请求有错，errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        return json_data

    def get_car_parking_info(self, carparking_name):
        carparking_name = carparking_name.strip()
        if not carparking_name.endswith("停车场"):
            carparking_name = carparking_name + "停车场"
        res = requests_get(self.car_parking_serial_id_url, {"carparking_name": carparking_name})
        assert res.status_code == 200, f"请求有错，errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        return json_data

    def upload_carparking_collection_record_info(self, carparking_serial, unique_time_string, other_data={}):
        payload = {
            "carparking_serial": carparking_serial,
            "unique_time_string": unique_time_string,
            "uid": self.uid
        }
        payload.update(other_data)
        res = requests_post(self.collection_record_serial_id_url, payload)
        assert res.status_code == 200, f"请求有错，errmsg【{res.reason}】"
        json_data = json.loads(res.text)
        return json_data

    def get_carparking_collection_record_info(self, carparking_serial, unique_time_string):
        res = requests_get(self.collection_record_serial_id_url, {
            "carparking_serial": carparking_serial,
            "unique_time_string": unique_time_string,
            # "uid": self.uid
        })
        json_data = json.loads(res.text)
        return json_data




"""
import sys,os,json
pp2 = os.path.abspath(".")
sys.path.append(pp2)
from spacetool import main_tool
d = main_tool.DataTool(name="leo", code="space666!")

# 测试上传停车场信息
d.upload_car_parking_info("虹桥时代广场", "上海", "青浦区", "高光路与高泾支路交叉口")
d.upload_car_parking_info("进博会P17停车场", "上海", "青浦区", "诸光路与卫家角交叉口")
d.upload_car_parking_info("久事西郊名墅")

d.get_car_parking_info("虹桥时代广场")
d.get_car_parking_info("进博会P17停车场")
d.get_car_parking_info("空")

d.upload_carparking_collection_record_info("P10eQQrhfa", "20220828-11-55-44", {"update": True, "record_type": "bevs"})
d.upload_carparking_collection_record_info("P10eQQrhfa", "20220821-16-25-14")
d.upload_carparking_collection_record_info("P10eQQrhfa", "20220820-16-25-14")
d.upload_carparking_collection_record_info("P10eQQrhfa", "20220819-16-25-14", {"record_type": "bevs"})

d.get_carparking_collection_record_info("P10eQQrhfa", "20220828-11-55-44")
d.get_carparking_collection_record_info("P10eQQrhfa", "20220821-16-25-14")
d.get_carparking_collection_record_info("P10eQQrhfa", "20220820-16-25-14")
d.get_carparking_collection_record_info("P10eQQrhfa", "20220819-16-25-14")
# 测试


"""































