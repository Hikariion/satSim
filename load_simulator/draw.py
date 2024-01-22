import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime

# 设置字体和图表属性
plt.rcParams["font.sans-serif"]=['simsun']  # 设置字体
plt.rcParams["axes.unicode_minus"]=False  # 解决负号乱码问题
plt.rcParams.update({'font.size': 14})

# 文件路径列表
file_paths = [
    # 'satellite_orbit_group_load_12H_suit.csv',
    'random_group_20_experiments_avg_load_12H.csv',
    'dynamic_group_20_experiments_avg_load_12H.csv'
]

# 标签列表
labels = [
    # 'grouped by orbit',

    'grouped by random',

    'grouped by dynamic'

]

# 读取并绘制每个文件的数据
for file_path, label in zip(file_paths, labels):
    data = pd.read_csv(file_path)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])

    # 平滑数据
    smoothed_data = data['Overall Load STD'].rolling(window=10).mean()
    average = np.mean(data['Overall Load STD'])

    plt.plot(data['Timestamp'], smoothed_data, label=label)  # 绘制折线图
    plt.axhline(y=average, color=plt.gca().get_lines()[-1].get_color(), linestyle='--')
    # if label == 'grouped by LCASC':
    #     plt.annotate('{:.4f}'.format(average), xy=(data['Timestamp'][10], average), xytext=(data['Timestamp'][10], average - 6))
    # else:
    #     plt.annotate('{:.4f}'.format(average), xy=(data['Timestamp'][10], average), xytext=(data['Timestamp'][10], average))
    plt.annotate('{:.4f}'.format(average), xy=(data['Timestamp'][10], average), xytext=(data['Timestamp'][10], average))

# 设置图表元素
plt.xlabel('时间')
plt.ylabel('卫星分组负载标准差')
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)
plt.gcf().autofmt_xdate()
plt.legend()
plt.title('卫星分组负载标准差（20组）')

# 显示图表
plt.show()
