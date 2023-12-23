import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

plt.rcParams["font.sans-serif"]=["Arial Unicode MS"]  # 设置字体
plt.rcParams["axes.unicode_minus"]=False  # 该语句解决图像中的“-”负号的乱码问题

# 读取CSV文件
file_path = 'satellite_orbit_group_load.csv'  # 替换为您的CSV文件路径
data = pd.read_csv(file_path)

plt.rcParams.update({'font.size': 14})
plt.plot(data['Timestamp'], data['Overall Load STD'])  # 绘制折线图

plt.title('Overall Load Standard Deviation Over Time')  # 添加标题
plt.xlabel('Timestamp')  # 添加X轴标签
plt.ylabel('Standard Deviation of Load')  # 添加Y轴标签

# 隐藏X轴标签
plt.xticks([])


# 显示图表
plt.show()
