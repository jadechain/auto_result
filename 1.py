import fnmatch
import os

for file in os.listdir('C:/天龙小蜜/角色配置'):
    if fnmatch.fnmatch(file, '*.ini'):
        print(file)
for j in os.listdir('C:/天龙小蜜/角色配置'):
    if fnmatch.fnmatch(j, '*.txt'):
        print(j)

def compare(list1, list2):
    error = []
    error_index = []
    if len(list1) == len(list2):
        for i in range(0, len(list1)):
    #两个列表对应元素相同，则直接过
            if list1[i] == list2[i]:
             pass
    else:#两个列表对应元素不同，则输出对应的索引
        error.append(abs(list1[i]-list2[i]))
    # print(i)
    error_index.append(i)
    print(error)
    print(error_index)

