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
    if not file_path.startswith('propose_delay'):
        delays = np.array(loaded_distances) * 2 / speed_of_light * 1000
    else:
        delays = np.array(loaded_distances)

    # 对时延进行排序以计算CDF
    sorted_delays = np.sort(delays)
    cdf = np.arange(1, len(sorted_delays) + 1) / len(sorted_delays)

    plt.plot(sorted_delays, cdf, label=label)  # 绘制CDF曲线

    line_color = plt.gca().get_lines()[-1].get_color()
    # # p60分位点
    # idx_50 = np.searchsorted(cdf, 0.5)
    # plt.axvline(sorted_delays[idx_50], color=line_color, linestyle='--', ymax=cdf[idx_50])
    # plt.annotate('50%:{:.2f}'.format(sorted_delays[idx_50]), xy=(sorted_delays[idx_50], cdf[idx_50]), xytext=(sorted_delays[idx_50]+0.05, cdf[idx_50]-0.03))
    # plt.plot([sorted_delays[idx_50]], [cdf[idx_50]], 'o', color=line_color)
    # p80分位点
    idx_80 = np.searchsorted(cdf, 0.8)
    plt.axvline(sorted_delays[idx_80], color=line_color, linestyle=':', ymax=cdf[idx_80] - 0.03)
    plt.annotate('80%:{:.2f}'.format(sorted_delays[idx_80]), xy=(sorted_delays[idx_80], cdf[idx_80]), xytext=(sorted_delays[idx_80]+0.05, cdf[idx_80]-0.03))
    plt.plot([sorted_delays[idx_80]], [cdf[idx_80]], 'o', color=line_color)
    # p99分位点
    idx_99 = np.searchsorted(cdf, 0.99)
    plt.axvline(sorted_delays[idx_99], color=line_color, linestyle=':', ymax=cdf[idx_99] - 0.03)
    plt.annotate('99%:{:.2f}'.format(sorted_delays[idx_99]), xy=(sorted_delays[idx_99], cdf[idx_99]), xytext=(sorted_delays[idx_99]-0.03, cdf[idx_99]-0.03))
    plt.plot([sorted_delays[idx_99]], [cdf[idx_99]], 'o', color=line_color)



# 绘制CDF图
plt.figure(figsize=(10, 6))

# 绘制 closest_distances 的CDF Nearest Distance First
plot_cdf('closest_distances.npy', 'Nearest Distance First')

# 绘制 longest_visual_distance 的CDF Longest Visibility First
plot_cdf('longest_visual_distance.npy', 'Longest Visibility First')

# 绘制 propose_delay 的CDP
plot_cdf('propose_delay.npy', 'Proposed-1-hop')
# 绘制 propose_delay 的CDP
plot_cdf('propose_delay_2hop.npy', 'Proposed-2-hop')

plt.title('卫星计算时延的累积分布函数 (CDF)')
plt.xlabel('时延(ms)')
plt.ylabel('CDF')
plt.grid(False)
plt.legend()
plt.show()