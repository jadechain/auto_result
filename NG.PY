import os
import sys
import random

files = os.listdir(sys.argv[1])
jpgs = [item for item in files if item.endswith("jpg")]
random.shuffle(jpgs)

#alert_label = ["airplane","automobile"]
label = ["brid","cat","deer","dog"]
total_num = 0
total_true_positive = 0
total_true_negative = 0
total_false_positive = 0
total_false_negative = 0

for jpg in jpgs:
    jpg_file = os.path.join(sys.argv[1], jpg)
    xml_file = os.path.join(sys.argv[1], jpg[:-3]+"xml")
    if not os.path.exists(jpg_file):
        continue
    if not os.path.exists(xml_file):
        continue
    #run_cmd = "./test-api -f 1 -i "+jpg_file+" -l ../authorization/license.txt >tmp.txt 2>&1"
    run_cmd = "darknet classifier train cfg/cifar.data cfg/cifar_small.cfg -dont_show"
    os.system(run_cmd)
    check_label_cmd1 = "grep -r \<name\>"+label[0]+" "+xml_file
    check_label_cmd2 = "grep -r \<name\>"+label[1]+" "+xml_file
    check_label_cmd3 = "grep -r \<name\>"+label[2]+" "+xml_file
    print(check_label_cmd)
    check_label_out1 = os.system(check_label_cmd1)
    check_label_out2 = os.system(check_label_cmd2)
    check_label_out3 = os.system(check_label_cmd3)
    if check_label_out1 != 0 and check_label_out2 != 0 and check_label_out3 != 0:
        print("no label:", xml_file)
        continue
    total_num += 1
    check_code_cmd = "grep -r \"code: 0\" tmp.txt"  # code: 0：算法检测出目标
    check_code_out = os.system(check_code_cmd)
    check_xml_cmd1 = "grep -r \""+alert_label[0]+"\" "+xml_file
    # check_xml_cmd2 = "grep -r \""+alert_label[1]+"\" "+xml_file
    check_xml_out1 = os.system(check_xml_cmd1)
    # print(check_xml_cmd1)
    # check_xml_out2 = os.system(check_xml_cmd2)
    # print(check_xml_cmd2)

    ground_truth = 0
    if check_xml_out1 == 0:
        print("positive:", xml_file)
        ground_truth = 1
    else:
        print("negative:", jpg_file)
        pass
    if check_code_out == 0 and ground_truth == 1:
        total_true_positive += 1
    elif check_code_out == 256 and ground_truth == 1:
        total_false_negative += 1
    elif check_code_out == 0 and ground_truth == 0:
        total_false_positive += 1
    elif check_code_out == 256 and ground_truth == 0:
        total_true_negative += 1
    break

print("total_true_positive:", total_true_positive)
print("total_true_negative:", total_true_negative)

print("total_false_positive:", total_false_positive)
print("total_false_negative:", total_false_negative)
print("total_num:", total_num)
if (total_true_positive + total_false_positive) != 0:
    print(" alert precision:", total_true_positive / (total_true_positive + total_false_positive))
if (total_true_positive + total_false_negative) != 0:
    print("alert recall:", total_true_positive / (total_true_positive + total_false_negative))
#if (total_true_negative + total_false_positive) != 0:
#    print("no alert precision:", total_true_negative / (total_true_negative + total_false_positive))
#if (total_true_negative + total_false_negative) != 0:
#    print("no alert recall:", total_true_negative / (total_true_negative + total_false_negative))*/
