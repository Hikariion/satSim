import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.sans-serif"]=["simsun"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
# 字号大小
plt.rcParams["font.size"] = 13

# 数据
data1 = [82.1598, 81.8145, 81.3362, 82.1294, 83.8214]
data2 = [86.6607, 89.7636, 94.0779, 92.9659, 91.9882]

# 数据的长度，用于确定柱状图的位置
n_groups = len(data1)

# 创建一个numpy数组，包含每个组的x位置
index = np.arange(n_groups)

# 调整y轴范围
y_min = min(min(data1), min(data2)) - 5
y_max = max(max(data1), max(data2)) + 5

# 创建折线图
plt.plot(index, data1, label='Group by ours', marker='o')
plt.plot(index, data2, label='Group by random', marker='o')

# 添加图表标题和坐标轴标签
plt.xlabel('分组数')
plt.ylabel('平均负载标准差')
plt.title('不同分组数下的平均负载标准差对比')

# 设置y轴的范围
plt.ylim(y_min, y_max)

# 添加图例
plt.legend()

# 优化x轴的标签显示
plt.xticks(index, ['20', '30', '40', '50', '60'])

# 显示图表
plt.show()





