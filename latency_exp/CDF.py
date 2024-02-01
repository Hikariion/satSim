import numpy as np
import matplotlib.pyplot as plt

# 设置字体和图表属性
plt.rcParams["font.sans-serif"] = ['simsun']  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号乱码问题
plt.rcParams.update({'font.size': 14})

def plot_cdf(file_path, label):
    loaded_distances = np.load(file_path)
    speed_of_light = 299792.458  # in km/s

    # 计算时延
    if not file_path.startswith('datas/propose_delay'):
        delays = np.array(loaded_distances) * 2 / speed_of_light * 1000
    else:
        delays = np.array(loaded_distances)

    # 对时延进行排序以计算CDF
    sorted_delays = np.sort(delays)
    cdf = np.arange(1, len(sorted_delays) + 1) / len(sorted_delays)

    plt.plot(sorted_delays, cdf, label=label)  # 绘制CDF曲线

    line_color = plt.gca().get_lines()[-1].get_color()
    # # p50分位点
    idx_50 = np.searchsorted(cdf, 0.5)
    plt.axvline(sorted_delays[idx_50], color=line_color, linestyle='--', ymax=cdf[idx_50])
    if file_path == 'propose_delay_2hop.npy':
        plt.annotate('50%:{:.2f}'.format(sorted_delays[idx_50]), xy=(sorted_delays[idx_50], cdf[idx_50]), xytext=(sorted_delays[idx_50]-0.8, cdf[idx_50]+0.03))
    else:
        plt.annotate('50%:{:.2f}'.format(sorted_delays[idx_50]), xy=(sorted_delays[idx_50], cdf[idx_50]),xytext=(sorted_delays[idx_50] + 0.05, cdf[idx_50] - 0.03))
    plt.plot([sorted_delays[idx_50]], [cdf[idx_50]], 'o', color=line_color)
    # p90分位点
    idx_90 = np.searchsorted(cdf, 0.9)
    plt.axvline(sorted_delays[idx_90], color=line_color, linestyle=':', ymax=cdf[idx_90] - 0.03)
    plt.annotate('90%:{:.2f}'.format(sorted_delays[idx_90]), xy=(sorted_delays[idx_90], cdf[idx_90]), xytext=(sorted_delays[idx_90]+0.05, cdf[idx_90]-0.03))
    plt.plot([sorted_delays[idx_90]], [cdf[idx_90]], 'o', color=line_color)
    # p99分位点
    idx_99 = np.searchsorted(cdf, 0.99)
    plt.axvline(sorted_delays[idx_99], color=line_color, linestyle=':', ymax=cdf[idx_99] - 0.03)
    plt.annotate('99%:{:.2f}'.format(sorted_delays[idx_99]), xy=(sorted_delays[idx_99], cdf[idx_99]), xytext=(sorted_delays[idx_99]-0.03, cdf[idx_99]-0.03))
    plt.plot([sorted_delays[idx_99]], [cdf[idx_99]], 'o', color=line_color)



# 绘制CDF图
plt.figure(figsize=(10, 6))

# 绘制 closest_distances 的CDF Nearest Distance First
plot_cdf('datas/closest_distances.npy', 'Nearest Distance First')

# 绘制 longest_visual_distance 的CDF Longest Visibility First
plot_cdf('datas/longest_visual_distance.npy', 'Longest Visibility First')

# # 绘制 propose_delay 的CDP
# plot_cdf('propose_delay.npy', 'LCMPS 10ms Constraint')
# 绘制 propose_delay 的CDP
plot_cdf('datas/propose_delay_2hop.npy', 'LCMPS 15ms Constraint')

# plt.title('卫星计算时延的累积分布函数 (CDF)')
plt.xlabel('时延(ms)')
plt.ylabel('CDF')
plt.grid(False)
plt.legend()
plt.show()