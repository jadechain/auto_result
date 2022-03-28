# 调用ias 得到图片json
import requests
from iou import compute_iou2
import time
from config import Config
from collections import defaultdict
import base64,shutil
import unittest
from function import *




class BaseAlgorithm(object):
    """业务相关的基类"""


    def __init__(self,*args, **kwargs):
        # 获取或有的xml种类的数目
        self.xml_total_kinds = get_total_xml(Config.path, Config.xml_kinds,"object")
        self.xml_total = sum(self.xml_total_kinds.values())
        self.label_dict = defaultdict(int)
        self.label_dict = init_dict(self.label_dict,Config.xml_kinds)
        print("label_dict:",self.label_dict)
        # 创建一个defaultdict字典对象 通过字典方式统计不确定的结果
        self.res_name = {"TP":0, "FP":0,"FN":0, "TN":0}
        # self.total_num = 0
        self.total_num = self.total_num = len(get_pictures_list(Config.path))
        self.alert = defaultdict(int)

    def __del__(self,*args, **kwargs):
        print("当前图片总数{}".format(self.total_num))
        print("当前xml种类数目{}".format(self.xml_total_kinds))
        print("当前xml总数{}".format(self.xml_total))
        print("当前识别图片结果{}".format(dict(self.res_name)))
        print("当前识别图片结果{}".format(self.label_dict))


    def get_alert_flag(self,result,key_list):
        """获取报警标志"""
        alert_flag=get_json_data(result,key_list)
        if alert_flag == 0 or alert_flag == "false":
            self.alert["alert_true"]=0
        elif alert_flag == 1 or alert_flag == "true":
            self.alert["alert_true"]=1

    def compare_alert(self,alert_flag,label_list,xml_key_list):
        """报警标志与xml文件比较,并统计TP,FP,FN,TN"""
        #label_list:需要验证的告警标签，xml_key_list：xml中的标签
        if alert_flag["alert_true"] :
                flag = False
                for label in label_list:
                    if label in xml_key_list:
                        flag = True
                        break
                if flag:
                    self.res_name["TP"] += 1#值加1
                else:
                    self.res_name["FP"] += 1#值加1
                    decode_base64(self.img_code,Config.FP_img_path,self.img_name)
        else:
            flag = False
            for label in label_list:
                if label in xml_key_list:
                    flag = True
                    break
            if flag:
                self.res_name["FN"] += 1#值加1
                decode_base64(self.img_code, Config.FN_img_path,self.img_name)
            else:
                self.res_name["TN"] += 1#值加1

    def calculate_alert_precision(self):
        '''计算告警准确率'''
        try:
            precision =  self.res_name["TP"]/(self.res_name["TP"]+self.res_name["FP"])
            recall = self.res_name["TP"]/(self.res_name["TP"]+self.res_name["FN"])
            print("precision：{}%\nrecall：{}%".format(round(precision*100,2),round(recall*100,2)))
        except Exception as e:
            print(e)

    def select_image_result(self,image_result):
        '''从结果中筛选需要的标位置'''
        res_data = []
        for value in image_result:
            if list(value.keys())[0] in list(Config.pic_k.values()):
                res_data.append(value)
        print("识别的图片json筛选结果{}".format(res_data))
        return res_data

    def get_image_and_xml_path(self,path,image):
        '''获取图片和xml路径'''
        image_path = path + image
        image_name = image.split('.')[0]
        xml_name = image_name.split('.')[0] + ".xml"
        xml_path = path + xml_name
        return image_path,xml_path,image_name

    def calculate_precision(self,label_list):
        '''计算准确率/召回率'''
        for label in label_list:
            try:
                precision =self.label_dict[label + "_TP"]/(self.label_dict[label + "_TP"] + self.label_dict[label + "_FP"])
                recall=self.label_dict[label + "_TP"]/self.xml_total_kinds[label]
                print('{}准确率/召回率：\nprecision:{}%\nrecall:{}%'.format(label,round(precision*100,2),round(recall*100,2)))
                over_write_result(Config.result_path,'{}准确率/召回率：\nprecision:{}%\nrecall:{}%'.format(label,round(precision*100,2),round(recall*100,2)))
            except Exception as e:
                print("{}准确率/召回率：\n{}除数不能为0".format(label,e))
                continue

    def calculate_precision_overall(self):
        '''计算准确率/召回率,整体'''
        try:
            precision =self.res_name["TP"]/(self.res_name["TP"] + self.res_name["FP"])
            recall=self.res_name["TP"]/self.xml_total
            f1_score = 2*precision*recall/(precision+recall)
            print('precision:{}%\nrecall:{}%\nf1_score:{}%'.format(round(precision*100,2),round(recall*100,2),round(f1_score*100,2)))
            over_write_result(Config.result_path,'precision:{}%\nrecall:{}%'.format(round(precision*100,2),round(recall*100,2)))
        except Exception as e:
            print(e)

    def compare_image_and_xml_eletric(self,image_result,xml_data,image_code,img_name):
        '''对比电表算法输出图片返回读数和xml读数'''
        for image_json in image_result:
            image_label = (list(image_json.keys())[0])
            image_coordinate = image_json.get(image_label)# 获取图片返回值
            found_flag = False
            for xml in xml_data:
                xml_label = (list(xml.keys())[0]).lower()
                xml_coordinate = xml.get(xml_label) #获取xml值
                if image_coordinate == xml_coordinate:
                    self.label_dict[xml_label + "_TP"] += 1
                    found_flag = True
                    break
            if not found_flag:        #iou不满足条件，类型相同FP+1
                self.label_dict[list(Config.pic_k.keys())[list(Config.pic_k.values()).index(image_label)] + "_FP"] += 1       #根据值获取键
                # decode_base64(image_code,Config.fail_img_path,img_name)

    def compare_image_and_xml(self,image_result,xml_data,image_code,img_name):
        '''对比算法输出图片坐标和xml坐标'''
        for image_json in image_result:
            image_label = (list(image_json.keys())[0])
            image_coordinate = image_json.get(image_label)# 获取图片坐标
            found_flag = False
            for xml in xml_data:
                xml_label = (list(xml.keys())[0]).lower()
                xml_coordinate = xml.get(xml_label) #获取xml位置
                if image_label == "ocr":
                    if xml_label == "ocr" :
                        if image_coordinate == xml_coordinate:
                            self.label_dict[xml_label + "_TP"] += 1
                            continue
                        else:
                            self.label_dict[xml_label + "_FP"] += 1
                            continue
                    else:
                        continue
                elif xml_label == "ocr":
                        continue
                iou = compute_iou2(image_coordinate, xml_coordinate)
                if iou > Config.IOU_SET:
                    if xml_label in Config.xml_kinds:
                        if  Config.pic_k[xml_label] ==image_label:  #实际返回结果name与xml不完全相同时建立对应关系
                            self.label_dict[xml_label + "_TP"] += 1 #IOU与类型都满足条件TP1
                            found_flag = True
                            break
            if not found_flag:        #iou不满足条件，类型相同FP+1
                self.label_dict[list(Config.pic_k.keys())[list(Config.pic_k.values()).index(image_label)] + "_FP"] += 1       #根据值获取键
                # decode_base64(image_code,Config.fail_img_path,img_name)

    def compare_image_and_xml_overall(self,image_result,xml_data,image_code,img_name):
        '''对比算法输出图片坐标和xml坐标,整体'''
        for image_json in image_result:
            image_label = (list(image_json.keys())[0])
            image_coordinate = image_json.get(image_label)# 获取图片坐标
            found_flag = False
            for xml in xml_data:
                xml_label = (list(xml.keys())[0]).lower()
                xml_coordinate = xml.get(xml_label) #获取xml位置
                iou = compute_iou2(image_coordinate, xml_coordinate)
                if iou > Config.IOU_SET:
                        if xml_label in Config.xml_kinds:
                            if  Config.pic_k[xml_label] ==image_label:  #实际返回结果name与xml不完全相同时建立对应关系
                                self.res_name["TP"] += 1                        #IOU与类型都满足条件TP1
                                found_flag = True
            if not found_flag:        #iou不满足条件，类型相同FP+1
                self.res_name["FP"] += 1
                # decode_base64(image_code,Config.fail_img_path,img_name)
                shutil.copyfile("{}{}".format(Config.path,img_name + ".xml"),"{}{}".format(Config.fail_xml_path,img_name + ".xml"))#保存fail图片对应xml


    def get_ias_api(self,image_name,image_path,roi_area):
        '''调用ias http接口'''
        data = {
            # 'image': (image_name, open(image_path, 'rb')),
            'image': (image_name, open(image_path, 'rb')),
            'args': roi_area
        }
        try:
            result = requests.post(Config.url, files=data)
            if result.json().get("code") == -1:
                print("------------------算法未授权, 退出-----------------")
                exit(1)
        except Exception as e:
            print("报错的图片{}".format(image_name))
            save_picture_and_xml(Config.path,Config.error_img_path,image_name)
            return None
        else:
            return result

    def get_resize_image_and_xml_path(self,path,resize_path,image,size):
        '''修改图片并返回修改后图片、xml路径'''
        image_resize_one(path,resize_path,image,(1280, 720))
        image_path = resize_path + image
        image_name = image.split('.')[0]
        xml_name = image_name.split('.')[0] + ".xml"
        xml_path = path + xml_name
        return image_path,xml_path,image_name

    def electric_precision(self,path):
        '''电表准确率/召回率'''
        # image_resize(path,Config.resize_path,(1280, 720))
        for image in get_pictures_list(path):
            print("image:",image)
            image_path,xml_path,image_name  = self.get_image_and_xml_path(path,image)
            result = self.get_ias_api(image,image_path,Config.roi_area)
            json_data = get_json_data(result,Config.res_json_key)
            image_code=json.loads(result.content)["buffer"]
            # decode_base64(image_code,Config.img_path,image_name)
            if json_data == [] or json_data is None or json_data == "Null" or json_data == "null":
                continue
            res_index  = get_eletric_result(json_data,"name",Config.pic_kinds)
            xml_data = get_eletric_xml_res(xml_path,"object")
            self.compare_image_and_xml_eletric(res_index,xml_data,image_code,image_name)
        self.calculate_precision(Config.xml_kinds)


    def compare_iou_more_label(self,path):
        '''多目标准确率/召回率'''
        # image_resize(path,Config.resize_path,(1280, 720))
        for image in get_pictures_list(path):
            print("image:",image)
            image_path,xml_path,image_name  = self.get_image_and_xml_path(path,image)
            result = self.get_ias_api(image,image_path,Config.roi_area)
            json_data = get_json_data(result,Config.res_json_key)
            image_code=json.loads(result.content)["buffer"]
            # decode_base64(image_code,Config.img_path,image_name)
            if json_data == [] or json_data is None or json_data == "Null" or json_data == "null":
                continue
            res_index  = get_picture_result(json_data,"name")
            image_result = self.select_image_result(res_index)
            xml_data = get_xml_res(xml_path,"object")
            self.compare_image_and_xml(image_result,xml_data,image_code,image_name)
        self.calculate_precision(Config.xml_kinds)


    def compare_label_iou_overall(self,path):
        """比较iou计算准确率召回率,多目标整体(dog)"""
        for image in get_pictures_list(path):
            print("image:",image)
            image_path,xml_path,image_name  = self.get_image_and_xml_path(path,image)
            result = self.get_ias_api(image, image_path,Config.roi_area)
            json_data = get_json_data(result,Config.res_json_key)
            image_code=json.loads(result.content)["buffer"]
            # decode_base64(image_code,Config.img_path,image_name)
            if json_data == [] or json_data is None or json_data == "Null" or json_data == "null":
                continue
            res_index  = get_picture_result(json_data,"name")
            image_result = self.select_image_result(res_index)
            xml_data = get_xml_res(xml_path,"object")
            self.compare_image_and_xml_overall(image_result,xml_data,image_code,image_name)
        self.calculate_precision_overall()



    def compare_alert_result(self,path):
        """告警准确率，json中告警信息存在于xml中"""
        for image in get_pictures_list(path):
            image_path,xml_path,image_name = self.get_image_and_xml_path(path,image)
            json_data = self.get_ias_api(image, image_path,Config.roi_area)
            result_data=get_json_data(json_data,Config.res_json_key)
            get_output_picture(json_data,Config.img_path,image_name,["buffer"])
            self.img_code=get_json_data(json_data,["buffer"])
            self.get_alert_flag(json_data,Config.alert_flag)
            print('image:{}'.format(image))
            print('get_http_ias返回:{}'.format(result_data))
            xml_data = get_xml_res(xml_path,'object')
            key_list=get_dict_key(xml_data)
            self.img_name=image_name
            self.compare_alert(self.alert,Config.alert_label_list,key_list)
        self.calculate_alert_precision()

    def get_ias_result_pictures(self,path):
        """只跑图片，获取结果图，不需要带xml"""
        for image in get_pictures_list(path):
            image_path,xml_path,image_name  = self.get_image_and_xml_path(path,image)
            result = self.get_ias_api(image, image_path,Config.roi_area)
            json_data = get_json_data(result,Config.res_json_key)
            image_code=json.loads(result.content)["buffer"]
            decode_base64(image_code,Config.img_path,image_name)
            print("json_data:",json_data)


class AutoTest(BaseAlgorithm,unittest.TestCase):
    """自动化测试"""

    # def __init__(self,*args, **kwargs):
    #     super().__init__(*args, **kwargs)
    def setUp(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def tearDown(self,*args, **kwargs):
        super().__del__(*args, **kwargs)
    # def __del__(self,*args, **kwargs):
    #     super().__del__(*args, **kwargs)

    def test_seeper_alert(self):
        """积水报警测试"""
        self.compare_alert_result(Config.path)

if __name__ == '__main__':
    # unittest.main()
    test=BaseAlgorithm()
    test.compare_alert_result(Config.path)
    # test.filter_image(Config.path)
    # test.get_ias_result_pictures(Config.path)
    # test.compare_iou_more_label(Config.path)
    # test.compare_label_iou_overall(Config.path)
    # test.electric_precision(Config.path)

