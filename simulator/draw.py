import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import numpy as np
import json
from dateutil import parser
import matplotlib as mpl
import pandas as pd
from datetime import datetime
# mpl.rcParams['figure.dpi'] = 300
plt.rcParams["font.sans-serif"]=["Arial Unicode MS"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

# 读取CSV文件
file_path1 = 'satellite_orbit_group_load.csv'  # 替换为您的CSV文件路径
data1 = pd.read_csv(file_path1)

file_path2 = 'satellite_random_group_load.csv'
data2 = pd.read_csv(file_path2)

# 确保'Timestamp'列是datetime类型
data1['Timestamp'] = pd.to_datetime(data1['Timestamp'])
data2['Timestamp'] = pd.to_datetime(data2['Timestamp'])
def to_percent(y, position):
    return '{:.0f}%'.format(100 * y)


plt.rcParams.update({'font.size': 14})
smoothed_data1 = data1['Overall Load STD'].rolling(window=10).mean()
plt.plot(data1['Timestamp'], smoothed_data1, label='orbit')  # 绘制折线图

smoothed_data2 = data2['Overall Load STD'].rolling(window=10).mean()
plt.plot(data2['Timestamp'], smoothed_data2, label='random')

plt.title('Overall Load Standard Deviation Over Time')  # 添加标题
plt.xlabel('Timestamp')  # 添加X轴标签
plt.ylabel('Standard Deviation of Load')  # 添加Y轴标签
# plt.xticks(rotation=45)  # 旋转X轴标签，以便更好地显示

# 设置x轴主要刻度定位器为每两小时一个刻度
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
# 设置x轴主要刻度格式器显示小时和分钟
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

# 旋转日期标记，以便它们不会重叠
plt.xticks(rotation=45)

# 自动调整x轴标签，防止重叠
plt.gcf().autofmt_xdate()

# 显示图表
plt.show()

# def draw(file_path):
#     file_path = file_path
#     data = pd.read_csv(file_path)
#
#     # 确保'Timestamp'列是datetime类型
#     data['Timestamp'] = pd.to_datetime(data['Timestamp'])
#
#     plt.title('Overall Load Standard Deviation Over Time')  # 添加标题
#     plt.xlabel('Timestamp')  # 添加X轴标签
#     plt.ylabel('Standard Deviation of Load')  # 添加Y轴标签
#     # plt.xticks(rotation=45)  # 旋转X轴标签，以便更好地显示
#     # 设置x轴主要刻度定位器为每两小时一个刻度
#     plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=2))
#     # 设置x轴主要刻度格式器显示小时和分钟
#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#
#     # 旋转日期标记，以便它们不会重叠
#     plt.xticks(rotation=45)
#
#     # 自动调整x轴标签，防止重叠
#     plt.gcf().autofmt_xdate()
#
#     # 显示图表
#     plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
#
# # 假设您有一些数据
# x = np.linspace(0, 10, 100)
# y1 = np.cos(x) + 1
# y2 = np.sin(x)
# y3 = np.log(x + 1)
#
# # 绘制图表
# plt.figure(figsize=(10, 6))
#
# # 使用不同的线型、颜色和标记绘制线条
# plt.plot(x, y1, linestyle='-', color='blue', linewidth=2, marker='o', label='cos(x)+1')
# plt.plot(x, y2, linestyle='--', color='orange', linewidth=2, marker='x', label='sin(x)')
# plt.plot(x, y3, linestyle='-.', color='green', linewidth=2, marker='s', label='log(x+1)')
#
# # 添加图例
# plt.legend()
#
# # 添加标题和轴标签
# plt.title('Beautiful Line Plots')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
#
# # 显示网格
# plt.grid(True)
#
# # 显示图表
# plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
#
# # 假设您有一些数据
# x = np.linspace(0, 10, 100)
# y1 = np.cos(x)
# y2 = np.sin(x)
# y3 = np.log(x + 1)
#
# # 绘制图表
# plt.figure(figsize=(10, 6))
#
# # 使用更细的线条绘制线条，并省略标记
# plt.plot(x, y1, linestyle='-', color='blue', linewidth=1, label='cos(x)')
# plt.plot(x, y2, linestyle='--', color='orange', linewidth=1, label='sin(x)')
# plt.plot(x, y3, linestyle='-.', color='green', linewidth=1, label='log(x+1)')
#
# # 添加图例
# plt.legend()
#
# # 添加标题和轴标签
# plt.title('Smooth and Fine Line Plots')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
#
# # 显示网格
# plt.grid(True)
#
# # 显示图表
# plt.show()

# def plot_load_value(time, load_values):
#     plt.rcParams.update({'font.size': 14})
#     for name, load in load_values.items():
#         plt.plot(time, load, label=name)
#         average = np.mean(load)
#         plt.axhline(y=average, color=plt.gca().get_lines()[-1].get_color(), linestyle='--')
#         plt.annotate('{:.4f}'.format(average), xy=(time[10], average), xytext=(time[10], average))
#     # fmt = mtick.FuncFormatter(to_percent)
#     # plt.gca().yaxis.set_major_formatter(fmt)
#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#     plt.legend(loc='lower right')
#     plt.xlabel('时间')
#     plt.xticks(rotation=45)
#     plt.ylabel('集群负载标准差')
#     plt.show()
#
# def gen_average_load(filename):
#     with open(f'results/{filename}.json', 'r') as f:
#         data = json.load(f)
#         name = data['summary']['scheduler']+'-'+data['summary']['group']
#         time = [parser.parse(t) for t in data['time']]
#         data = data['cluster']
#         load_values = [cluster['load'] for cluster in data.values()]
#
#         load_values = [[d[0]*0.5+d[1]*0.5 for d in load] for load in load_values]
#         # average_loads=load_values[0]
#         # average_loads = [np.std([load[i] for load in load_values])/np.mean([load[i] for load in load_values]) for i in range(len(load_values[0]))]
#         average_loads = [np.std([load[i] for load in load_values]) for i in range(len(load_values[0]))]
#         return name, time[30:], average_loads[30:]
def plot_load_value(time, load_values):
    plt.rcParams.update({'font.size': 14})
    for name, load in load_values.items():
        plt.plot(time, load, label=name)
        average = np.mean(load)
        # plt.axhline(y=average, color=plt.gca().get_lines()[-1].get_color(), linestyle='--')
        # plt.annotate('{:.2f}%'.format(average*100), xy=(time[5], average+0.01), xytext=(time[5], average+0.01))
    fmt = mtick.FuncFormatter(to_percent)
    plt.gca().yaxis.set_major_formatter(fmt)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    plt.legend(loc='lower right')
    plt.xlabel('时间')
    plt.ylabel('集群负载均值')
    plt.show()