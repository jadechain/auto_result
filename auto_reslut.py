# 调用ias 得到图片json
import requests
from iou import compute_iou2
import os
import time
from get_all_xml_nums import get_total_xml, get_xml_res, get_pic_res
from config import Config
from collections import defaultdict
import base64,shutil
from function import *


alert = defaultdict(int)
# 获取图片返回列表 包括jpg,png
def pics(path):
    return [file for file in os.listdir(path) if
            file.endswith('jpg') or file.endswith('png') or file.endswith('JPG') or file.endswith('PNG')]

img_code=""
# 封装调用http接口
def get_http_ias(pic, pic_with_dir):
    data = {
        'image': (pic, open(pic_with_dir, 'rb'))
    }
    try:
        res_image = requests.post(Config.url, files=data)
        # print(res_image.json())
        # over_write_result(Config.res_file,pic_with_dir, res_image.json())#将返回结果写到文件
        global img_code
        img_code=res_image.json()["buffer"]
        # print("图片编码:{}".format(img_code))
        decode_base64(img_code,Config.img_path,img_name)
        # json_result=get_json_data(res_image,Config.res_json_key)
        alert_flag=get_json_data(res_image,Config.alert_flag)
        print("alert_flag:",alert_flag)
        if alert_flag == 0 or alert_flag == "false":
            alert["alert_true"]=0
            print(alert)
        elif alert_flag == 1 or alert_flag == "true":
            alert["alert_true"]=1
        if res_image.json().get("code") == -1:
            print("------------------算法未授权, 退出-----------------")
            exit(1)
    except Exception as e:
        print("报错的图片{}".format(pic))
        shutil.copyfile("{}{}".format(Config.path,pic),"{}{}".format(Config.error_img_path,pic))#保存报错图片
        shutil.copyfile("{}{}".format(Config.path,pic.replace("jpg","xml")),"{}{}".format(Config.error_img_path,pic.replace("jpg","xml")))#保存报错图片对应xml
        time.sleep(5)
        return None
    else:

        res_index = get_json_data(res_image,Config.res_json_key)
        print("res_index:",res_index)
        return res_index


def over_write_result(write_file,pic_with_dir, res_json):
    """保存算法分析的结果"""
    with open(write_file, "a+", encoding='UTF-8') as f:
        f.write(pic_with_dir + "\n")
        f.write(str(res_json) + "\n")


class Auto_test:
    """自动化测试"""

    def __init__(self):
        # 获取或有的xml种类的数目
        self.xml_total_kinds = get_total_xml(Config.path, Config.xml_kinds)
        self.xml_total = sum(self.xml_total_kinds.values())
        # 创建一个defaultdict字典对象 通过字典方式统计不确定的结果
        self.res_name = {"TP":0, "FP":0,"FN":0, "TN":0}
        self.total_num = 0




    def __del__(self):
        print("当前图片总数{}".format(self.total_num))
        print("当前识别图片情况{}".format(dict(self.res_name)))
        print("当前xml总数{}".format(self.xml_total))


    def xml_pic_judge_res(self, path):
        """提交图片到算法分析 返回获取到的json结果"""
        self.total_num=len(pics(path))
        for pic_file in pics(path):
            # 根据图片名称, 生成带路径的图片 和带路径对应的xml
            pic_with_dir = os.path.join(path + pic_file)
            print("pic_with_dir:{}".format(pic_with_dir))
            xml = pic_file.split('.')[0] + ".xml"
            global img_name
            img_name=pic_file.split('.')[0]
            print("img_name:",img_name)
            xml_with_dir = os.path.join(path + xml)

            # 调用get_http_ias接口 获取
            res_index = get_http_ias(pic_file, pic_with_dir)
            print('get_http_ias返回:{}'.format(res_index))
            # 调用写入结果到txt接口
            over_write_result(Config.res_over_write,pic_with_dir, res_index)



            xml_persons = get_xml_res(xml_with_dir)
            xml_key = []
            for xml_list in xml_persons:
                xml_key.append(xml_list)
            print("xml_key:",xml_key)
            # print("xml_persons:{}".format(xml_persons))
            if alert["alert_true"] :
                flag = False
                for label in Config.label_list:
                    if label in xml_key:
                        flag = True
                        break
                if flag:
                    self.res_name[Config.res_kind_name[0]] += 1#值加1
                else:
                    self.res_name[Config.res_kind_name[1]] += 1#值加1
                    decode_base64(img_code, Config.FP_img_path, img_name)
            else:
                flag = False
                for label in Config.label_list:
                    if label in xml_key:
                        flag = True
                        break
                if flag:
                    self.res_name[Config.res_kind_name[2]] += 1#值加1
                    decode_base64(img_code, Config.FN_img_path, img_name)
                else:
                    self.res_name[Config.res_kind_name[3]] += 1#值加1
            print(self.res_name)
            try:
                precision =  self.res_name["TP"]/(self.res_name["TP"]+self.res_name["FP"])
                recall = self.res_name["TP"]/(self.res_name["TP"]+self.res_name["FN"])
                print("precision：",precision)
                print("recall：",recall)
            except Exception as e:
                print(e)
            decode_base64(img_code,Config.fail_img_path,img_name)
            # shutil.copyfile("{}{}".format(Config.path,img_name + ".jpg"),"{}{}".format(Config.fail_img_path,img_name + ".jpg"))#保存fail图片
            shutil.copyfile("{}{}".format(Config.path,img_name + ".xml"),"{}{}".format(Config.fail_xml_path,img_name + ".xml"))#保存fail图片对应xml

if __name__ == '__main__':
    a = Auto_test()
    a.xml_pic_judge_res(Config.path)