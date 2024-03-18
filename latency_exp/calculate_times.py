import numpy as np

# min dist
min_dist_array = np.load('datas/minDist_migrate_times_list_avg.npy')
print(min_dist_array)
# 32.4

# longest visual time
longest_visual_array = np.load('datas/longest_visual_migrate_times_list_avg.npy')
print(np.mean(longest_visual_array))
# 5.6


# propose
propose_array_2hop = np.load('datas/propose_average_migrate_times_2hop_4ms.npy')
print(np.mean(propose_array_2hop))
# 16.4

propose_array_1hop = np.load('datas/propose_average_migrate_times_1hop_4ms.npy')
print(np.mean(propose_array_1hop))
# 18.0