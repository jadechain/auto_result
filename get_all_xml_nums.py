import os
from bs4 import BeautifulSoup
from config import Config
from collections import defaultdict


def get_total_xml(path, xml_kinds):
    xml_name = defaultdict(int)
    xmls = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('xml')]
    for xml in xmls:
        with open(xml, 'r', encoding="UTF-8") as f:
            soup_xml = BeautifulSoup(f, "lxml")
            objects = soup_xml.find_all("object")
            for obj in objects:
                # 获取xml中的标签类型
                # kinds = list(obj.children)[0].get_text()
                kinds = obj.find_all("name")[0].string
                for i in range(len(xml_kinds)):
                    if kinds == xml_kinds[i]:
                        xml_name[xml_kinds[i]] += 1
    return dict(xml_name)


def get_xml_res(xml_with_dir):
    xml_persons = []
    pic_name = xml_with_dir.split('\\')[-1].split('.')[0] + ".jpg"
    xml_persons.append(pic_name)
    with open(xml_with_dir, 'r', encoding="UTF-8") as f:
        soup = BeautifulSoup(f, 'lxml')
        objects = soup.find_all("object")
        for obj in objects:
            kinds = obj.find_all("name")[0].string
            if kinds == Config.xml_not_kind:
                continue
            xmin = obj.bndbox.xmin.get_text()
            ymin = obj.bndbox.ymin.get_text()
            xmax = int(obj.bndbox.xmax.get_text())
            ymax = int(obj.bndbox.ymax.get_text())
            res = f"{xmin},{ymin},{xmax},{ymax}" + ',' + kinds
            xml_persons.append(res)
    return xml_persons

