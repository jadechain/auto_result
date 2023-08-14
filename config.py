class Config(object):
    # 设置iou面积比
    IOU_SET = 0.5
    # 设置图片位置
    base_path = "D:/test_data/dregs_mound/HWHYsoil20210707test_data/"
    path = base_path + 'dregs_mound/'

    #设置ROI
    POLYGON = "POLYGON((0 0,0 1,1 1,1 0))"

    # 设置ias请求路径
    # url_pol = "http://192.168.1.103:{}/api/analysisImage?args={}".format(32852,POLYGON)
    base_url = "http://192.168.1.103:{}/api/analysisImage"
    url = base_url.format(32933)

    #图片保存路径
    img_path="./out_pic/dregs_mound/{}_out.jpg"
    FN_img_path="./out_pic/FN/{}_out.jpg"
    FP_img_path="./out_pic/FP/{}_out.jpg"


    error_img_path="./error_pic/"#报错图片保存路径

    fail_img_path="./fail_pic/{}_out.jpg"#fail图片保存路径
    fail_xml_path="./fail_pic/"#fail图片对应的xml保存路径

    # 设置xml标注值进行比对

    xml_kinds = ["soil"]
    # xml_kinds = ["equipment"]  #
    # xml_kinds = ["motor_people"]#非机动车占道


    # 设置pic结果比对
    # pic_kinds = ["mask", "mid_mask", "back", "head"]

    pic_kinds = ["soil"]
    pic_k={"soil":"soil"}
    label_list=["soil"]#报警时用到3

    """算法分析结果指标设置"""
    # 正样本正确   # 负样本正确  # 误识别数目
    # res_kind_name = ["all_on_right", "all_off_right", "all_not_right"]
    # res_kind_name = ["all_on_right", "all_not_right"]
    res_kind_name = ["TP","FP","FN","TN"]

    """算法分析json key提取"""
    # 算法返回json示例{'code': 0, 'result': {'report_num_mask': 0, 'alert_flag': 0, 'mask_info': []}}

    res_json_key = ["result","model_data","objects"]

    #是否报警返回数据提取
    alert_flag = ["result","algorithm_data","is_alert"]
    # alert_flag = ["result","algorithm_data","is_alert"]

    # 除了坐标还存在类型的话
    # extra = "motor_people"#???

    res_json_name = ""

    # 默认为1 该值是配置坐标类型 1 为x,y,width,heigth 2 为 xmin, ymin, xmax, ymax
    xmax_or_width = 1


    """指定保存算法那的结果路径"""
    res_over_write = "./res_json.txt"
    res_file = "./res_data.txt"


