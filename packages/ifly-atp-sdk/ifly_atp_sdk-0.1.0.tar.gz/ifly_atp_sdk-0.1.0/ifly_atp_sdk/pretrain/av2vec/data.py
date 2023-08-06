APPId = "4CC5779A"
APIKey = "94a179ef19bd9f8c5c5a3ac1060016f7"
APISecret = "HY7xfGGKO3ilByAE9MHDGS9ByvsNg0gO"

# 请求数据
request_data = {
	"header":{
		"app_id":"123456",
		"uid":"39769795890",
		"did":"SR082321940000200",
		"imei":"8664020318693660",
		"imsi":"4600264952729100",
		"mac":"6c:92:bf:65:c6:14",
		"net_type":"wifi",
		"net_isp":"CMCC",
		"status":3,
		"res_id":""
	},
	"parameter":{
		"s338aa6ff":{
			"feature":{
				"encoding":"utf8",
				"compress":"raw",
				"format":"plain"
			},
			"fea_image":{
				"encoding":"jpg"
			}
		}
	},
	"payload":{
		"audio":{
			"encoding":"raw",
			"sample_rate":16000,
			"channels":1,
			"bit_depth":16,
			"status":3,
			"audio":"./resource/input/audio/test.wav",
			"frame_size":0
		},
		"video":{
			"encoding":"h264",
			"frame_rate":0,
			"width":0,
			"height":0,
			"video":"./resource/input/video/test.MOV",
			"status":3
		}
	}
}

# 请求地址
request_url = "https://cn.api.xf-yun.com/v1/private/s338aa6ff"

# 用于快速定位响应值

response_path_list = ['$..payload.fea_image', '$..payload.feature', ]