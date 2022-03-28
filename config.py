class Config(object):
    # 设置iou面积比
    IOU_SET = 0.5
    confidence=0.3
    # 设置图片位置
    base_path = "D:/test_data/lying-and-sitting/"
    path = base_path + 'lie_sit_20210706_test_data/'
    # path = base_path + 'test/'
    # path = base_path + 'no_uniform/'

    #设置ROI
    roi_area='{"roi":["POLYGON((0.01 0.01,0.98 0.01,0.98 0.98,0.01 0.98))"]}'

    # 设置ias请求路径
    base_url = "http://192.168.1.103:{}/api/analysisImage"
    # wellcover_url = "http://192.168.1.103:{}/api/analysisImage"
    # url = wellcover_url.format(32773)
    url = base_url.format(32947)

    #图片保存路径
    # img_path="./out_pic/baby_car/other/{}_out.jpg"
    img_path="./out_pic/lying-and-sitting/{}_out.jpg"
    FN_img_path="./out_pic/FN/{}_out.jpg"
    FP_img_path="./out_pic/FP/{}_out.jpg"


    error_img_path="./error_pic/"#报错图片保存路径
    fail_img_path="./fail_pic/{}_out.jpg"#fail图片保存路径
    fail_xml_path="./fail_pic/"#fail图片对应的xml保存路径
    resize_path = "./resize_img/"


    fail_out_img_path="./fail_pic/{}_out.jpg"#fail图片保存路径
    fail_sources_img_path="./fail_sources_pic/"#fail图片原图保存路径
    confidence_path="./out_pic/confidence_pic/"#fail图片对应的xml保存路径
    confidence_out_path="./out_pic/confidence_out_pic/{}_out.jpg"#fail图片对应的xml保存路径

    FN_out_path="./out_pic/fn_out_pic/{}_out.jpg"#fail图片对应的xml保存路径
    FN_path="./out_pic/fn_pic/"#fail图片对应的xml保存路径


    # 设置xml标注值进行比对
    xml_kinds = ["sitting_on_ground","lying_on_ground"]
    # xml_kinds = ["no_safety_person"]
    # 设置pic结果比对

    #幸福西饼
    # pic_kinds = ["no_safety_person"]
    # pic_kinds = ["dog","dog_rope","person"]
    # pic_kinds = ["reading","tag_code","bar_code","ocr"]
    pic_kinds = ["sitting_on_ground","lying_on_ground"]

    #xml中的标注与返回json中的name需要建立对应关系，例如xml为seeper，json返回Wet
    pic_k=dict(zip(xml_kinds,pic_kinds))


    #告警标签
    # label_list=["other_clothes","other_clothes"]
    alert_label_list=["sitting_on_ground","lying_on_ground"]


    """算法分析结果指标设置"""
    # 正样本正确   # 负样本正确  # 误识别数目
    # res_kind_name = ["all_on_right", "all_off_right", "all_not_right"]
    res_kind_name = ["all_on_right", "all_not_right"]

    """算法分析json key提取"""
    # 算法返回json示例{'code': 0, 'result': {'report_num_mask': 0, 'alert_flag': 0, 'mask_info': []}}
    # res_json_key = ["result", "alert_info"]#非机动车
    res_json_key = ["result","model_data","objects"]

    #是否报警返回数据提取
    alert_flag = ["result","algorithm_data","is_alert"]

    # 除了坐标还存在类型的话
    extra = "motor_people"#???

    res_json_name = ""

    # 默认为1 该值是配置坐标类型 1 为x,y,width,heigth 2 为 xmin, ymin, xmax, ymax
    xmax_or_width = 1


    """指定保存算法那的结果路径"""
    res_over_write = "./res_json.txt"
    res_file = "./res_data.txt"
    result_path = "./result.txt"


