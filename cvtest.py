import cv2
import json
from typing import List, Union

# img_path = 'D:/Users/chenyulian/Desktop/MSP5005115959205P0023_MSP5005115959205P0024_20220801093059.CHK/Img19.jpg'
img_path = 'D:/Users/chenyulian/Desktop/vs/data/guanjie/real_data/C985P0A-PLTVLWA51XXB4-AA0/C985P0A-PLTVLWA51XXB4-AA0/errlog0/LSP4306115959045P0055 LSP4306115959045P0056_20220801094114.CHK/Img3.jpg'
model_img_path = 'D:/Users/chenyulian/Desktop/vs/data/guanjie/9856P0A-PLTVLQ321XAHC-AA0/9856P0A-PLTVLQ321XAHC-AA0/Img3.jpg'
# model_img_path = 'D:/Users/chenyulian/Desktop/vs/data/guanjie/9856P0A-PLTVLQ321XAHC-AA0/9856P0A-PLTVLQ321XAHC-AA0 - 副本/Img3.jpg'
json_file = './preview.json'
lst, pt_top, pt_bottom = [], [], []
img = cv2.imread(img_path)


def full_rectangle(preview_jpg: str, label: str) -> List:
    with open(json_file) as f:
        data = json.load(f)
    for index, i in enumerate(data[preview_jpg]['Objects']):
        if i['DetailLabel'] == label:
            lst.append(i['Box'])
            print(index)
    print(len(lst), lst, sep='\n')
    try:
        top = (min(items['X'] for items in lst), min(items['Y'] for items in lst))
        bottom = (max(items['X'] + items['Width'] for items in lst), max(items['Y'] + items['Height'] for items in lst))
        print(top, bottom, sep='\n')
        single_rectangle(top, bottom, (20, 246, 50))
    except ValueError as e:
        print(e)
    for m in range(len(lst)):
        pt_top.append((lst[m]['X'], lst[m]['Y']))
        pt_bottom.append((lst[m]['X'] + lst[m]['Width'], lst[m]['Y'] + lst[m]['Height']))
    print(pt_top, pt_bottom, sep='\n')
    return lst


def single_rectangle(top: Union[tuple, List], bottom: Union[tuple, List], colour: tuple) -> str:
    if type(top) == tuple:
        cv2.rectangle(img, top, bottom, colour, 2)
        cv2.imwrite('22.jpg', img)
    else:
        for i in range(int(len(top))):
            cv2.rectangle(img, top[i], bottom[i], colour, 2)
            cv2.imwrite('22.jpg', img)
    return 'mission success'


def model_rectangle(label, file):
    model = cv2.imread(model_img_path)
    with open(file) as f:
        data = json.load(f)
    for index, i in enumerate(data['shapes']):
        if i['label'] == label:
            cv2.rectangle(model, tuple(map(int, i['points'][0][:])), tuple(map(int, i['points'][1][:])), (0, 255, 0), 4)
            cv2.imwrite('21.jpg', model)
            print(tuple(map(int, i['points'][1][:])), tuple(map(int, i['points'][1][:])))
    return 'success'


print(full_rectangle('LSP4306115959045P0055_LSP4306115959045P0056_20220801094114_Img3.jpg', 'D9101'))
print(single_rectangle(pt_top, pt_bottom, (0, 255, 0)))
model_rectangle('lianxi/D9101',
                'D:/Users/chenyulian/Desktop/vs/data/guanjie/9856P0A-PLTVLQ321XAHC-AA0/9856P0A-PLTVLQ321XAHC-AA0/Img3.json')
