import os,shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom

def fun(x):
    x = x.split(',')
    return str(int(float(x[0])))+','+str(int(float(x[1])))

imgroot = 'D:\sot\XSfjdc\img'
xmlpath = 'D:\sot\XSfjdc\XSnon_vehicles20201230test_data.XML'

savepath = 'D:/sot/Sfjdc/data'
if os.path.exists(savepath):
    shutil.rmtree(savepath)
os.makedirs(savepath)

tree = ET.parse(xmlpath)
root = tree.getroot()
images = root.findall('image')
for img in images:
    dic = img.attrib
    imgname = dic['name']

    dom = minidom.Document()
    root_node = dom.createElement('annotation')
    dom.appendChild(root_node)

    for box in img.findall('box'):
        object_node = dom.createElement('object')
        root_node.appendChild(object_node)
        dic = box.attrib

        name_node = dom.createElement('class')
        object_node.appendChild(name_node)
        name_text = dom.createTextNode(dic['label'])
        name_node.appendChild(name_text)

        bndbox_node = dom.createElement('bndbox')
        object_node.appendChild(bndbox_node)

        xmin_node = dom.createElement('xmin')
        bndbox_node.appendChild(xmin_node)
        xmin_text = dom.createTextNode(str(int(float(dic['xtl']))))
        xmin_node.appendChild(xmin_text)

        ymin_node = dom.createElement('ymin')
        bndbox_node.appendChild(ymin_node)
        ymin_text = dom.createTextNode(str(int(float(dic['ytl']))))
        ymin_node.appendChild(ymin_text)

        xmax_node = dom.createElement('xmax')
        bndbox_node.appendChild(xmax_node)
        xmax_text = dom.createTextNode(str(int(float(dic['xbr']))))
        xmax_node.appendChild(xmax_text)

        ymax_node = dom.createElement('ymax')
        bndbox_node.appendChild(ymax_node)
        ymax_text = dom.createTextNode(str(int(float(dic['ybr']))))
        ymax_node.appendChild(ymax_text)
        # class_label = [(a.attrib['name'], a.text) for a in attrs]
        # print(attrs)

    for polygon in img.findall('polygon'):
        object_node = dom.createElement('polygon')
        root_node.appendChild(object_node)
        dic = polygon.attrib

        name_node = dom.createElement('class')
        object_node.appendChild(name_node)
        name_text = dom.createTextNode(dic['label'])
        name_node.appendChild(name_text)

        name_node = dom.createElement('points')
        object_node.appendChild(name_node)
        s = dic['points'].split(';')
        s = list(map(fun, s))
        s = ';'.join(s)
        name_text = dom.createTextNode(s)
        name_node.appendChild(name_text)

    xml_save_path = os.path.join(savepath, os.path.splitext(os.path.basename(imgname))[0]+'.xml')
    with open(xml_save_path, 'w', encoding='UTF-8') as fh:
        dom.writexml(fh, indent='', addindent='  ', newl='\n', encoding='UTF-8')
    shutil.copy(os.path.join(imgroot, os.path.basename(imgname)), savepath)