#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import base64
import json
import uuid
from datetime import datetime
import time

def write_result(write_file, result_data):
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

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        # random_name = ''.join([each for each in str(uuid.uuid1()).split('-')])
        image_name = str(datetime.now()).replace(" ", "-").replace(":", "-")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        #with open('1.txt', 'wb') as f:
        #    f.write(self.data_string)
        self.data_string = self.data_string.decode()
        write_result('./result.txt',self.data_string)
        #print("-------------------------",self.data_string )
        obj = json.loads(self.data_string)
        res_base64 = obj.get("identifyPic")
        sysCode = obj.get("sysCode")
        ruleNo = obj.get("ruleNo")
        eqpNo = obj.get("eqpNo")
        image_name = sysCode + '_' + image_name

        alarm = ''
        for info_obj in obj["infos"]['infos']:
            t = info_obj['type']
            illegal = info_obj['illegal']
            if illegal == 2:
                alarm = alarm + t + ' '

        # print(alarm)
        # image_name = image_name + ' ------->' + alarm

        if res_base64 is not None:
            res_image = base64.decodebytes(res_base64.encode('ascii'))
            print("res_image:%s"%image_name)
            with open('res_jpg/%s.jpg'%image_name, 'wb') as f:
                f.write(res_image)
        #else:
            #print("算法识别输出图片base64为空")

        ori_base64 = obj.get('rawPic')
        if ori_base64 is not None:
            ori_image = base64.decodebytes(ori_base64.encode('ascii'))
            print("ori_image:%s"%image_name)
            with open('ori_jpg/%s.jpg'%image_name, 'wb') as f:
                f.write(ori_image)
        #else:
            #print("输出原图base64为空")


        self.send_response(200)
        self.send_header(
            'Content-Type',
            'text/plain; charset=utf-8',
        )
        self.send_header(
            'Last-Modified',
            self.date_time_string(time.time())
        )
        self.end_headers()
        self.wfile.write('Response body\n'.encode('utf-8'))
        print("")
        print("")


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
