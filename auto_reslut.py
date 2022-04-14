def get_json_result(pics):
    for pic in pics:
        pic_json = pic.split('.')[0] + ".json"
        pic_json_dir = os.path.join(Config.path_pic_res, pic_json)
        with open(pic_json_dir, 'r', encoding="utf-8") as f:
            file_results = json.load(f)
            with open("1.txt", 'a') as f:
                f.write(pic + ' ')
            for pic_res in Config.pic_res_kinds:
                if str(pic_res) == "0":
                    pic_res = "rentou"
                if str(pic_res) == "1":
                    pic_res = "aqm"
                file_result = file_results.get(pic_res)
                for file in file_result:
                    xmin = file.get('xmin')
                    ymin = file.get('ymin')
                    xmax = file.get('xmax')
                    ymax = file.get('ymax')
                    res = f"{xmin},{ymin},{xmax},{ymax}" +',' + pic_res
                    with open("1.txt", 'a') as f:
                        f.write(" " +str(res) + '')
            with open("1.txt", 'a') as f:
                f.write("\n")



def get_txt_result(file):
    with open(file, 'r', encoding="utf-8") as f:
        pic_json_res = []
        file_results = f.read().splitlines()
        for result in file_results:
            results = result.split(" ")
            while '' in results:
                results.remove('')
            if len(results) > 0 :
                pic_json_res.append(results)

        return pic_json_res

def pics(path):
    return [file for file in os.listdir(path) if
            file.endswith('jpg') or file.endswith('png') or file.endswith('JPG') or file.endswith('PNG')]


def over_write_result(pic_with_dir, res_json):
    with open(Config.res_over_write, "a+", encoding='UTF-8') as f:
        f.write(pic_with_dir + "\n")
        f.write(str(res_json) + "\n")






class Auto_test:
    def __init__(self):
        if os.path.isfile('1.txt'):
            os.remove('1.txt')
        self.xml_total_kinds = get_total_xml(Config.path_xm_res, Config.xml_kinds)
        self.xml_total = sum(self.xml_total_kinds.values())
        self.res_name = defaultdict(int)

    def __del__(self):
        print("当前xml总数{}".format(self.xml_total))
        print("当前xml种类数目{}".format(self.xml_total_kinds))
        print("当前识别图片情况{}".format(dict(self.res_name)))


    def xml_pic_judge_res(self, path):
        if Config.json_to_txt:
            get_json_result(pics(path))

        pic_res = get_txt_result(Config.pic_res_dir)
        for pic_re in pic_res:
            pic_name = pic_re[0]

            xml_with_dir = os.path.join(Config.path_xm_res, pic_name.split('.')[0]+'.xml')
            xml_persons = get_xml_res(xml_with_dir)
            total_xml_num = len(xml_persons)
            for i in range(1, len(pic_re)):
                pic_which_kind = pic_re[i].split(",")[-1]
                pic_coordinate = pic_re[i].split(",")[0:4]
                for j in range(1, len(xml_persons)):
                    try:
                        xml_which_kind = xml_persons[i].split(",")[-1]
                        xml_coordinate = xml_persons[i].split(",")[0:4]
                    except:
                        pass
                    iou = compute_iou2(pic_coordinate, xml_coordinate)
                    if Config.algo_choice :
                        if iou > Config.IOU_SET:
                            # if xml_which_kind == pic_which_kind and pic_which_kind == "aqm":
                            self.res_name[Config.res_kind_name[0]] += 1
                    #             break
                    #         if xml_which_kind == pic_which_kind and xml_which_kind == "rentou":
                    #             self.res_name[Config.res_kind_name[1]] += 1
                    #             break
                    #     else:
                    #         # 识别错误的数目
                    #         self.res_name[Config.res_kind_name[2]] += 1
                    #         break
                    # else:
                    #     if iou > Config.IOU_SET:
                    #         if xml_which_kind == pic_which_kind and pic_which_kind == "renti":
                    #             self.res_name[Config.res_kind_name[0]] += 1
                    #             break
                        else:
                            # 识别错误的数目
                            self.res_name[Config.res_kind_name[2]] += 1
                            break


a = Auto_test()
a.xml_pic_judge_res(Config.path_xm_res)
