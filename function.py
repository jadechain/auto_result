import base64,logging
import os,sys,json,shutil
from config import Config
from bs4 import BeautifulSoup
from collections import defaultdict
import cv2


def get_json_data(actual_result,key_list):
    """提取返回结果数据"""
    if actual_result:
        extract_data=json.loads(actual_result.content)
        for key in key_list:
            extract_data=extract_data.get(key)
        # print("json结果：",extract_data)
        return extract_data
    else:
        print("json结果：",actual_result)
        return ""

def decode_base64(base64_data,save_path,img_name):
    """图片解码"""
    if base64_data:
        with open(save_path.format(img_name),'wb') as file:
            img = base64.b64decode(base64_data)
            file.write(img)

# 定义日志函数
def init_log():
    logger = None
    logger = logging.getLogger()
    datefmt = "%Y-%m-%d %H:%M:%S"
    format_str = "[%(asctime)s]: %(levelname)s - %(message)s"
    formatter = logging.Formatter(format_str,datefmt)
    stream_handler = logging.StreamHandler()
    logger.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return [logger,stream_handler]


def log_info(err_msg, level=logging.INFO):
    logger,stream_handler = init_log()
    logger.info(err_msg)
    stream_handler.flush()  # 确保所有的日志输出已经被刷新
    logger.removeHandler( stream_handler)  # 去掉log继承

def over_write_result(write_file, result_data):
    """保存算法分析的结果"""
    if  type(result_data) is list:
        for content in result_data:
            with open(write_file, "a+", encoding='UTF-8') as f:
                f.write(str(content) + "\n")
            f.close()
    else:
        with open(write_file, "a+", encoding='UTF-8') as f:
            f.write(str(result_data) + "\n")
        f.close()


def image_resize(img_path,out_path,size):
    '''调整图片大小'''
    imgs = os.listdir(img_path)
    imgs=[ img for img in imgs if img.endswith('jpg'or 'png' or 'JPG' or 'PNG') ]
    for img in imgs:
        image=cv2.imread(os.path.join(img_path+img))
        image2 = cv2.resize(image, size) #resize 1280x720，宽x高
        out = os.path.join(out_path, img)
        cv2.imwrite(out,image2)
        print("save resized img:", out)
        # cv2.imshow('', image2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

def image_resize_one(img_path,out_path,img_name,size):
    '''调整图片大小'''
    imgs = os.listdir(img_path)
    imgs=[ img for img in imgs if img.endswith('jpg'or 'png' or 'JPG' or 'PNG') ]
    image=cv2.imread(os.path.join(img_path+img_name))
    image2 = cv2.resize(image, size) #resize 1280x720，宽x高
    out = os.path.join(out_path, img_name)
    cv2.imwrite(out,image2)
    print("save resized img:", out)
    # cv2.imshow('', image2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def get_pictures_list(path):
    """获取图片返回列表包括jpg,png"""
    return [file for file in os.listdir(path) if
            file.endswith('jpg') or file.endswith('png') or file.endswith('JPG') or file.endswith('PNG')]

def save_picture_and_xml(source_path,save_path,file_name):
    """保存图片和xml文件"""
    shutil.copyfile("{}{}".format(source_path,file_name),"{}{}".format(save_path,file_name))#保存报错图片
    shutil.copyfile("{}{}".format(source_path,file_name.replace("jpg","xml")),"{}{}".format(save_path,file_name.replace("jpg","xml")))#保存报错图片对应xml

def get_output_picture(json_data,img_path,img_name,key_list):
    """获取返回图片并保存"""
    img_code=get_json_data(json_data,key_list)
    decode_base64(img_code,img_path,img_name)

def remove_file(file_path):
    '''删除文件'''
    os.remove(file_path)

def get_dict_key(xml_dict):
    """提取字典键"""
    key_list = []
    for xml_list in xml_dict:
        key_list.append(list(xml_list.keys())[0])
    return key_list


def get_total_xml(xml_path,xml_kinds,xml_attr):
    """获取各种xml类型个数"""
    # 该函数作用就是构建一个字典来接收传入的值,
    xml_name = defaultdict(int)
    xmls = [os.path.join(xml_path, file) for file in os.listdir(xml_path) if file.endswith('xml')]
    for xml in xmls:
        with open(xml, 'r', encoding="UTF-8") as f:
            soup_xml = BeautifulSoup(f, "lxml")
            objects = soup_xml.find_all(xml_attr)
            # 获取xml中的标签类型
            for obj in objects:
                kinds = list(obj.children)[1].get_text()
                # kinds = list(obj.children)[0].get_text()
                for i in range(len(xml_kinds)):
                    if kinds == xml_kinds[i]:
                        if kinds=="else_hat":
                            xml_name["hat"] += 1
                        else:
                            xml_name[xml_kinds[i]] += 1
    return dict(xml_name)

def get_xml_res(xml_with_dir,xml_attr):
    """获取xml中的类型和坐标:paramer 传入xml绝对路径 以列表返回每个xml文件内容"""
    #例如xml_attr="object"
    xml_persons = []
    with open(xml_with_dir, 'r', encoding="UTF-8") as f:
        soup = BeautifulSoup(f, 'lxml')
        objects = soup.find_all(xml_attr)
        for obj in objects:
            if obj.bndbox is None:
                continue
            kinds = list(obj.children)[1].get_text()
            # kinds = list(obj.children)[0].get_text()
            if kinds == "else_hat":
                kinds = "hat"
            elif kinds == "ocr":
                ocr = obj.bndbox.ocrvalue.get_text()
                xml_persons.append({kinds: ocr})
                continue
            xmin = int(float(obj.bndbox.xmin.get_text()))
            ymin = int(float(obj.bndbox.ymin.get_text()))
            xmax = int(float(obj.bndbox.xmax.get_text()))
            ymax = int(float(obj.bndbox.ymax.get_text()))
            xml_persons.append({kinds: (int(xmin), int(ymin), int(xmax), int(ymax))})
    print("xml_data:",xml_persons)
    return xml_persons

def get_eletric_xml_res(xml_with_dir,xml_attr):
    """获取电表xml读数"""
    xml_persons = []
    with open(xml_with_dir, 'r', encoding="UTF-8") as f:
        soup = BeautifulSoup(f, 'lxml')
        objects = soup.find_all(xml_attr)
        for obj in objects:
            if obj.bndbox is None:
                continue
            kinds = list(obj.children)[1].get_text()
            try:
                value = obj.bndbox.ocrvalue.get_text()
            except:
                continue
            xml_persons.append({kinds: value})
    print("xml_data:",xml_persons)
    return xml_persons

def get_points_data(xml_path,xml_attr):
    """提取points"""
    points = []
    with open(xml_path, 'r', encoding="UTF-8") as f:
        soup = BeautifulSoup(f, 'lxml')
        polygon = soup.find_all(xml_attr)
        for plo in polygon:
            points = plo.points.get_text()
    return points

def init_dict(dict,key_list):
    for key in key_list:
        for rate in ["TP", "FP","FN", "TN"]:
            dict["{}_{}".format(key,rate)]+=0
    return dict

def get_picture_result(res_indexs,name):
    """获取图片分析json的类型以及坐标"""
    pic_json_res = []
    for res in res_indexs:
        result_name = res.get(name)#取算法输出的结果中的name
        try:
            xmin = res.get('x')
            ymin = res.get('y')
            xmax = res.get('width') + xmin
            ymax = res.get('height') + ymin
            confidence = res.get('confidence')
        except:
            xmin = res.get('xmin')
            ymin = res.get('ymin')
            xmax = res.get('xmax')
            ymax = res.get('ymax')
            confidence = res.get('confidence')
        if not Config.pic_kinds:
            pic_json_res.append({Config.extra: (int(xmin), int(ymin), int(xmax), int(ymax)),"confidence":confidence})
        else:
            pic_json_res.append({result_name: (int(xmin), int(ymin), int(xmax), int(ymax)),"confidence":confidence})
    return pic_json_res

def get_eletric_result(res_indexs,name,key_list):
    """获取电表图片分析json的类型以及坐标"""
    pic_json_res = []
    for res in res_indexs:
        for key in key_list:
            if key in res.keys():
                value =  res.get(key)
                pic_json_res.append({key: value})
    return pic_json_res
