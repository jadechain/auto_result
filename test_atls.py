import requests
import json
import os
import time
import base64
import pathlib




def SendData(image):
    with open(image, "rb") as image_file:
        base64_code = base64.b64encode(image_file.read()).decode()
        file_ext = os.path.splitext(image)[1]
        encoded_string = 'data:image/{};base64,{}'.format(file_ext[1:], base64_code)
                #encoded_string = base64.b64encode(image_file.read()).decode()

    filename = pathlib.Path(image).stem
    url = "http://192.168.1.245:9999/api/ImageInference"
    data = {
        "sysCode": "%s"%filename,
        "eqpNo": "test_image",
        "ruleNo": "xxxx",
        "dataType": "remote",
        "rawPic": "%s"%encoded_string,
        "recognize": [{
            "para": [
                    {
                            "type": "helmet_detect",
                            "sampleFre": 0.5,
                            "conf_thresh": 0.2
                    }
            ]
        }],
        "reportInfoType": "111",
        "resultUrl": "192.168.1.103:8080"
    }
    time.sleep(0.1)
    res = requests.post(url, data=json.dumps(data))
    print(res.json())



def SendDir(path):
    images = [file for file in os.listdir(path)]
    for image in images:
        image = os.path.join(path, image)
        image = image.replace("\\", "/")
        SendData(image)


path = "D:/zxl文件/脚本文件/江苏电力/test_data/"
# SendData("D:/zxl文件/脚本文件/江苏电力/test_data/103.jpg")
# exit()

SendDir(path)
exit()

