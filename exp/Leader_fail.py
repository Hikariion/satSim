import matplotlib.pyplot as plt
import numpy as np  # 导入NumPy以便进行数学计算

plt.rcParams["font.sans-serif"] = ["simsun"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号问题
plt.rcParams["font.size"] = 13  # 字号大小

# Data to be plotted
intervals_ms_ours = [2.036, 2.071, 2.407, 2.200, 2.643, 2.165, 2.056, 3.093, 2.223, 2.002]
intervals_ms_reboot = [46.305, 42.594, 49.249, 57.360, 54.167, 46.574, 48.647, 55.052, 55.433, 53.675]

# 计算平均值
average_ms_ours = np.mean(intervals_ms_ours)
average_ms_reboot = np.mean(intervals_ms_reboot)

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))

# 设置轴标签
ax.set_xlabel('实验组编号', fontsize=15)
ax.set_ylabel('时间 (s)', fontsize=15)

# 绘制两组数据
ax.plot(range(1, 11), intervals_ms_ours, color='tab:blue', marker='o', linestyle='-', label='本文方案主节点重启集群恢复耗时')
ax.plot(range(1, 11), intervals_ms_reboot, color='tab:orange', marker='x', linestyle='-', label='中心化方案主节点重启集群恢复耗时')

# 绘制平均值线
ax.axhline(y=average_ms_ours, color='tab:blue', linestyle='--', label='本文方案平均恢复耗时')
ax.axhline(y=average_ms_reboot, color='tab:orange', linestyle='--', label='中心化方案平均恢复耗时')

# 在平均值线旁边添加数值注释
plt.annotate(f'{average_ms_ours:.2f} s', xy=(1, average_ms_ours), xytext=(1, average_ms_ours + 0.3), color='tab:blue')
plt.annotate(f'{average_ms_reboot:.2f} s', xy=(1, average_ms_reboot), xytext=(1, average_ms_reboot + 0.3), color='tab:orange')

# 设置x轴的刻度，确保实验组编号从1到10显示全
ax.set_xticks(range(1, 11))
ax.set_xticklabels([str(i) for i in range(1, 11)])

# 添加图例
ax.legend()

# 显示图形
plt.show()
