#!/usr/bin/env python3
# -*-coding:utf-8 -*-
from sample.aipass_client import execute
from data import *

if __name__ == '__main__':
    # 程序启动的时候设置APPID
    request_data['header']['app_id'] = APPId
    execute(request_url, request_data, "POST", APPId, APIKey, APISecret)
