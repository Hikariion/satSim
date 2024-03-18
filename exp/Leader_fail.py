import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["simsun"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号问题
plt.rcParams["font.size"] = 13  # 字号大小

# Data to be plotted
intervals_ms_ours = [2.036, 2.071, 2.407, 2.200, 2.643, 2.165, 2.056, 3.093, 2.223, 2.002]
intervals_ms_reboot = [122.6, 123.4, 124.1, 125.3, 123.2, 124.5, 123.7, 123.8, 123.6, 123.9]
average_interval = sum(intervals_ms_ours) / len(intervals_ms_ours)  # 计算平均值

# 创建图形和双轴
fig, ax1 = plt.subplots(figsize=(10, 6))

# 设置主轴
ax1.set_xlabel('实验组编号')
ax1.set_ylabel('恢复用时 (s)', color='tab:blue')
ax1.plot(range(1, 11), intervals_ms_ours, color='tab:blue', marker='o', linestyle='-', label='恢复用时')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 克隆轴用于双轴
ax2 = ax1.twinx()
ax2.set_ylabel('中心化方案中心节点重启耗时 (s)', color='tab:green')  # 设置副轴
ax2.plot(range(1, 11), intervals_ms_reboot, color='tab:blue', marker='o', linestyle='-', label='恢复用时')
ax2.tick_params(axis='y', labelcolor='tab:green')

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left')


# 显示图形
plt.show()
