import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"]=["simsun"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
# 字号大小
plt.rcParams["font.size"] = 13

# Data to be plotted
intervals_ms = [2036, 2071, 2407, 2200, 2643, 2165, 2056, 3093, 2223, 2002]
average_interval = sum(intervals_ms) / len(intervals_ms)  # Calculating the average

# Generating a bar plot with Chinese labels and with the average line, but without axis grid lines
plt.figure(figsize=(10, 6))
plt.bar(range(1, 11), intervals_ms, color='blue')
plt.axhline(y=average_interval, color='red', linestyle='-', label=f'平均值: {average_interval:.2f} ms')
plt.xlabel('实验组编号')
plt.ylabel('恢复用时 (ms)')
plt.title('各实验组Leader节点宕机恢复用时')
plt.xticks(range(1, 11))  # Set x-ticks to group numbers
plt.legend()

# Showing the plot without grid lines
plt.show()
