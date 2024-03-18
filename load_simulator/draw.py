import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import matplotlib as mpl
from datetime import datetime, timedelta

# 设置字体和图表属性
mpl.rcParams['figure.dpi'] = 200
plt.rcParams["font.sans-serif"]=['simsun']  # 设置字体
plt.rcParams["axes.unicode_minus"]=False  # 解决负号乱码问题
plt.rcParams.update({'font.size': 8})

# 文件路径列表
file_paths = [
    'datas/satellite_orbit_group_load_12H_suit.csv',
    'datas/fixed_group_16_experiments_avg_load_12H.csv',
    'datas/random_group_16_experiments_avg_load_12H.csv',
    'datas/dynamic_group_16_experiments_avg_load_12H.csv',
    'datas/dynamic_genetics_16_experiments_avg_load_12H.csv',


]

# 标签列表
labels = [
    'Orbit',

    'Fixed',

    'Random',

    'Greedy',

    'SLFDG',
    

]

# 读取并绘制每个文件的数据
for file_path, label in zip(file_paths, labels):
    data = pd.read_csv(file_path)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    smoothed_data = data['Overall Load STD'].rolling(window=10).mean()
    average = np.mean(smoothed_data)
    peak = smoothed_data.max()

    plt.plot(data['Timestamp'], smoothed_data, label=label)  # 绘制折线图
    plt.axhline(y=average, color=plt.gca().get_lines()[-1].get_color(), linestyle='--')
    # plt.axhline(y=peak, color=plt.gca().get_lines()[-1].get_color(), linestyle='--')
    # if label == 'grouped by LCASC':
    #     plt.annotate('{:.4f}'.format(average), xy=(data['Timestamp'][10], average), xytext=(data['Timestamp'][10], average - 6))
    # else:
    #     plt.annotate('{:.4f}'.format(average), xy=(data['Timestamp'][10], average), xytext=(data['Timestamp'][10], average))
    # 平均
    if label == 'greedy':
        plt.annotate('{:.4f}'.format(average), xy=(data['Timestamp'][10], average), xytext=(data['Timestamp'][10], average - 6))
    else:
        plt.annotate('{:.4f}'.format(average), xy=(data['Timestamp'][10], average), xytext=(data['Timestamp'][10], average))

    # 峰值
    # plt.annotate('{:.4f}'.format(peak), xy=(data['Timestamp'][10], peak), xytext=(data['Timestamp'][10], peak))
    # if 'dynamic' in file_path:
    #     # 画一条竖线
    #     start_time = data['Timestamp'].min().replace(hour=1, minute=0, second=0, microsecond=0)
    #     for hour in range(1, 12):
    #         vertical_line_time = start_time + timedelta(hours=hour)
    #         plt.axvline(x=vertical_line_time, color='grey', linestyle='--')

# 设置图表元素
plt.xlabel('时间')
plt.ylabel('卫星分组平均负载指数标准差')
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.xticks(rotation=45)
plt.gcf().autofmt_xdate()
plt.legend()
# plt.title('50组')

# 显示图表
plt.show()
