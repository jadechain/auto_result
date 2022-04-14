import requests

heard_data={
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC8xMC4xLjEwLjBcL2FwaVwvbG9naW4iLCJpYXQiOjE2MjMwNTE2NDcsImV4cCI6MTYyMzEzODA0NywibmJmIjoxNjIzMDUxNjQ3LCJqdGkiOiJhejBsZjMwNUZ6RGlVbmliIiwic3ViIjoxMCwicHJ2IjoiMTNlOGQwMjhiMzkxZjNiN2I2M2YyMTkzM2RiYWQ0NThmZjIxMDcyZSJ9.crlug0JKtrzyCUC8B0Xtd0HSU7UNTMSJuebNOcdDLLI"
}
data ={
    "licenses":[{"algo_type":"video",
    "algorithm_id":10078,
    "algorithm_name":"安全绳背心识别(10078)",
    "contract":"12",
    "desc":"12",
    "machine_detail":"{\"version\":7,\"reference\":\"4d52cf68645b5a1dbba838201cb2794e2c0f1333eb62f7c147f6837873201f89\",\"disk_serial\":\"S3YLNX0K533123P\"}",
    "qps":"25",
    "remark":"12",
    "type":"probation",
    "unit":"month",
    "validity":"1"}]
}
url ="http://infer_bg.extremevision.com.cn/api/authorization/license"
# res_license = requests.post(url=url,heard=heard_data,data=data)
res_license = requests.post(url=url,headers=heard_data,data=data)
print(res_license.content)