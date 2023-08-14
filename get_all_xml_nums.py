import os
from bs4 import BeautifulSoup
from config import Config
from collections import defaultdict


def get_total_xml(path, xml_kinds):
    """获取各种xml类型个数"""
    # 该函数作用就是构建一个字典来接收传入的值,
    xml_name = defaultdict(int)
    xmls = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('xml')]
    for xml in xmls:
        print(xml)
        with open(xml, 'r', encoding="UTF-8") as f:
            soup_xml = BeautifulSoup(f, "lxml")
            objects = soup_xml.find_all("object")
            for obj in objects:
                # 获取xml中的标签类型
                kinds = list(obj.children)[1].get_text()
                for i in range(len(xml_kinds)):
                    if kinds == xml_kinds[i]:
                        xml_name[xml_kinds[i]] += 1
    print("xml_name:%s"%xml_name)
    return dict(xml_name)


def get_xml_res(xml_with_dir):
    """获取xml中的类型和坐标:paramer  传入xml绝对路径 以列表返回每个xml文件内容"""
    xml_persons = []
    with open(xml_with_dir, 'r', encoding="UTF-8") as f:
        soup = BeautifulSoup(f, 'lxml')
        objects = soup.find_all("polygon")
        # objects = soup.find_all("object")
        # polygon = soup.find_all("polygon")
        # polygon_name=polygon[0].get_text()
        # print("polygon_name:",polygon_name)
        # print("objects:",objects)
        # print("polygon:",polygon)
        # for plo in polygon:
        #     plo_kind = list(plo.children)[1].get_text()
        #     points = plo.points.get_text()
        #     print("plo_kind:",plo_kind)
        #     print("points:",points)

        for obj in objects:
            # if obj.bndbox is None:
            #     continue
            kinds = list(obj.children)[1].get_text()
            # xmin = int(float(obj.bndbox.xmin.get_text()))
            # ymin = int(float(obj.bndbox.ymin.get_text()))
            # xmax = int(float(obj.bndbox.xmax.get_text()))
            # ymax = int(float(obj.bndbox.ymax.get_text()))
            xml_persons.append(kinds)
    return xml_persons


def get_pic_res(res_indexs):
    """获取图片分析json的类型以及坐标"""
    pic_json_res = []
    # 根据用户传入的结果坐标类型选择不同的坐标类型方式
    if Config.xmax_or_width == 1:
        for res in res_indexs:
            x = res.get('x')
            y = res.get('y')
            xmax = res.get('width') + x
            ymax = res.get('height') + y
            name = res.get("name")#取算法输出的结果中的name
            status = res.get("status")#取算法输出的结果中的status
            # 这个需要根据输出的json1在调整
            if not Config.pic_kinds:
                pic_json_res.append({Config.extra: (int(x), int(y), int(xmax), int(ymax))})
            else:
                pic_json_res.append({name: (int(x), int(y), int(xmax), int(ymax))})
                pic_json_res.append({status: (int(x), int(y), int(xmax), int(ymax))})
        print("pic_json_res:{}".format(pic_json_res))
        return pic_json_res
    if Config.xmax_or_width == 2:
        for res in res_indexs:
            xmin = res.get('xmin')
            ymin = res.get('ymin')
            xmax = res.get('xmax')
            ymax = res.get('ymax')
            # 这个需要根据输出的json1在调整
            name = res.get(Config.res_json_name)
            # 这个需要根据输出的json1在调整
            if not Config.pic_kinds:
                pic_json_res.append({Config.extra: (int(xmin), int(ymin), int(xmax), int(ymax))})
            else:
                pic_json_res.append({name: (int(xmin), int(ymin), int(xmax), int(ymax))})
        return pic_json_res

