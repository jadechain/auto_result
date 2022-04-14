class Config(object):
    IOU_SET = 0.2
    path_pic_res = r"C:/Users/Administrator/Desktop/test_data/result_dir"
    path_xm_res = r"C:/Users/Administrator/Desktop/test_data/Atlas_testdata"

    xml_kinds = ["fire"]
    pic_res_kinds = ["0"]

    """算法分析结果指标设置"""
    # res_kind_name = ["all_on_right", "all_not_right"]

    # 是否需要开启json转换 txt 不需要开启
    json_to_txt = True
    pic_res_dir = "1.txt"
    algo_choice = False








# class Config(object):
#     # 设置iou面积比
#     IOU_SET = 0.2
#     # 设置算法输出结果txt
#     path_pic_res = r"C:/Users/Administrator/Desktop/test_data/result_dir"
#     path_xm_res = r"C:/Users/Administrator/Desktop/test_data/Atlas_testdata"
#
#     # 设置xml标注值进行比对
#     xml_kinds = ["rentou", "aqm"]
#     # 设置pic结果标签  rentou 0 anquanmao  1   xingren 0
#     pic_res_kinds = ["0", "1"]
#
#     # 设置不需要统计的字段 但是xml里面存在
#     xml_not_kind = "renti"
#
#
#     """算法分析结果指标设置"""
#     #安全帽选择这个    安全帽正确数       未戴安全帽正确数   错误数
#     res_kind_name = ["all_hat_right", "all_head_right", "all_not_right"]
#
#     # 是否需要开启json转换
#     json_to_txt = True
#
#     # 算法结果读取路径  如果是开起了json转换 默认是填写1.txt文件
#     pic_res_dir = "1.txt"
#
#     #安全帽
#     algo_choice = True
#

