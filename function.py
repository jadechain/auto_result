import json
import base64


def get_json_data(actual_result,key_list):
        '''提取返回结果数据'''
        extract_data=json.loads(actual_result.content)
        for key in key_list:
            extract_data=extract_data.get(key)
        return extract_data

def decode_base64(base64_data,save_path,img_name):
        '''图片解码'''
        with open(save_path.format(img_name),'wb') as file:
            img = base64.b64decode(base64_data)
            file.write(img)
