import os,json
import requests


video_list=["test_8.MP4","test_9.MP4"]
container_id = "19e06e1c55f4"
for video in video_list:
    try:
        os.system('docker exec -it {} bash -c "/usr/local/ev_sdk/bin/test-ji-api -f 4 -i /usr/local/ev_sdk/data/{} -o /usr/local/ev_sdk/data/{} -l /usr/local/vas/license.txt"'.format(container_id,video,video[:video.index(".")]+"out"+video[video.index("."):]))
    except Exception as e :
        print(e)


def get_image(path):
    '''获取图片'''
    image_list=[]
    images=os.listdir(path)
    for image in images:
        if ".jpg" or "JPG" or "png" or "PNG" in image:
            image_list.append(image)
    return image_list

def get_text(path):
    '''获取文本文档'''
    txt_list=[]
    text=os.listdir(path)
    for t in text:
        if ".txt" in t:
            txt_list.append(t)
    return txt_list

def read_and_write_config(file,old_str,new_str):
    '''读写文件'''
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
       for line in f:
           if old_str in line:
              line = new_str
           file_data += line
       f.close()
    with open(file,"w",encoding="utf-8") as f:
       f.write(file_data)
       f.close()

def get_license(file,text):
    '''提取license'''
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
       for line in f:
           if text in line:
               file_data += line[1:line.index(',')+1]
       f.close()
       return file_data

def get_txt_info(file,text):
    '''提取license'''
    file_data = {"{}_0".format(text):0,"{}_1".format(text):0,"{}_2".format(text):0,"{}_3".format(text):0}
    with open(file, "r", encoding="utf-8") as f:
       for line in f:
           if text in line:
               type_num = line[line.index(':')+2:line.index(':')+3]
               if type_num=='1':
                  file_data["{}_1".format(text)]+=1
               elif type_num=="2":
                   file_data["{}_2".format(text)]+=1
               elif type_num=="3":
                   file_data["{}_3".format(text)]+=1
               elif type_num=="0":
                   file_data["{}_0".format(text)]+=1
               print(line)
       print(file_data)
       f.close()
       return file_data

# str1='    "license":"d859a8093eec027057fe18709444ae8e633ecaabe6a4b17b79efa279040be142cebd2c339551d0e904060af85ae300d894a56c5db0d2825571f4e56089c794d404c0167f5f64fd4deeea1a0a4ba3be24881a93778aea61280f6d16ffa4ef3420d32d9bc624dc19f1aa95f1314f5acb5baf479d051bbe83534ebdc3d4a1bc492f",\n'
# read_and_write_config('./config.json','"license":',str1)

# license=get_license('./license.txt','"license"')
# print(license)
get_txt_info('./19_out.avi.txt','enterprise_type')

def get_result(path,text):
    '''获取结果'''
    result_data=get_text(path)
    for text_path in result_data:
        get_txt_info(text_path,text)


image_list=get_image('/usr/local/ev_sdk/data/test_images/')
for i in range(2):
    for img in image_list:
        os.system('/usr/local/ev_sdk/bin/test-ji-api -f 1 -i /usr/local/ev_sdk/data/test_images/{} -l /usr/local/ev_sdk/license.txt'.format(img))



def get_license1(file,text):
    '''提取license'''
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
       for line in f:
           if text in line:
              if 'license' in line:
                   file_data += line[line.index('{}'.format(text))+len(text)+1:line.index('",')]
              elif 'version' in line:
                  file_data += line[line.index('{}'.format(text))+len(text)+1:line.index('}')]
       print(file_data)
       return file_data


'cd /usr/local/ev_sdk/bin/ && ./test-ji-api -f 1 -i /usr/local/1.jpg -a "{"roi":["POLYGON((0.47424242424242424 0.515,0.4636363636363636 0.0825,0.9272727272727272 0.095,0.9272727272727272 0.5525))"]}" -o /usr/local/1_out.jpg -l /usr/local/ev_sdk/license.txt'


#!/usr/bin/python # -*- coding: UTF-8 -*-
import os


video_list=["2.mp4","3.mp4","4.mp4","5.mp4"]
container_id = "9d47fcb2ec4a"
def over_write_result(write_file, result_data):
    """保存结果"""
    if  type(result_data) is list:
        for content in result_data:
            with open(write_file, "a+", encoding='UTF-8') as f:
                f.write(str(content) + "\n")
            f.close()
    else:
        with open(write_file, "a+", encoding='UTF-8') as f:
            f.write(str(result_data) + "\n")
        f.close()


