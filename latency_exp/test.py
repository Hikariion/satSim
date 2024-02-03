import numpy as np

list1 = [1, 2, 3, 4, 5]
list2 = [2, 3, 4, 5, 6]

list = []

list.append(list1)
list.append(list2)

all = np.concatenate(list)  # 将所有距离列表合并为一个数组
average_list = np.mean(list, axis=0)
  # 计算合并后数组的平均值

print(average_list)