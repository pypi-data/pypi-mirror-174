#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: config
@time: 2022/10/31
@contact: ybyang7@iflytek.com
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import copy

VOICE2VEC = "sd6a98146"
AV2VEC = "s338aa6ff"

AV2VEC_URL = "https://cn.api.xf-yun.com/v1/private/s338aa6ff"
VOICE2VEC_URL = "https://cn-huadong-1.xf-yun.com/v1/private/sd6a98146"

VOICE2VEC_INPUT_TPL = {
    "header": {
        "app_id": "123456",
        "uid": "39769795890",
        "did": "SR082321940000200",
        "imei": "8664020318693660",
        "imsi": "4600264952729100",
        "mac": "6c:92:bf:65:c6:14",
        "net_type": "wifi",
        "net_isp": "CMCC",
        "status": 3,
        "res_id": ""
    },
    "parameter": {
        "sd6a98146": {
            "fea_image": {
                "encoding": "jpg"
            },
            "fea": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain"
            },
            "fbank_image": {
                "encoding": "jpg"
            }
        }
    },
    "payload": {
        "data": {
            "encoding": "raw",
            "sample_rate": 16000,
            "channels": 1,
            "bit_depth": 16,
            "status": 3,
            "audio": "./resource/input/audio/阳光总在风雨后.speex-wb",
            "frame_size": 0
        }
    }
}

AV2VEC_INPUT_TPL = {
    "header": {
        "app_id": "123456",
        "uid": "39769795890",
        "did": "SR082321940000200",
        "imei": "8664020318693660",
        "imsi": "4600264952729100",
        "mac": "6c:92:bf:65:c6:14",
        "net_type": "wifi",
        "net_isp": "CMCC",
        "status": 3,
        "res_id": ""
    },
    "parameter": {
        "s338aa6ff": {
            "feature": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain"
            },
            "fea_image": {
                "encoding": "jpg"
            }
        }
    },
    "payload": {
        "audio": {
            "encoding": "raw",
            "sample_rate": 16000,
            "channels": 1,
            "bit_depth": 16,
            "status": 3,
            "audio": "./resource/input/audio/test.wav",
            "frame_size": 0
        },
        "video": {
            "encoding": "h264",
            "frame_rate": 0,
            "width": 0,
            "height": 0,
            "video": "./resource/input/video/test.MOV",
            "status": 3
        }
    }
}


class InputData:
    def __init__(self, model):
        self.model = model

    def prepare(self, **kwargs):
        if self.model == VOICE2VEC:
            if "audio" not in kwargs:
                raise Exception("you should specify audio")
            data = kwargs.get("audio")
            tpl = copy.deepcopy(VOICE2VEC_INPUT_TPL)
            tpl['payload']['data']['audio'] = data
            return tpl
        elif self.model == AV2VEC:
            if "audio" not in kwargs and "video" not in kwargs:
                raise Exception("you should specify audio and video this model")
            audio = kwargs.get("audio")
            video = kwargs.get("video")
            tpl = copy.deepcopy(AV2VEC_INPUT_TPL)
            tpl['payload']['audio']['audio'] = audio
            tpl['payload']['video']['video'] = video
            return tpl
        else:
            raise Exception("not support this model")
