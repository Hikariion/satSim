import numpy as np

# min dist
min_dist_array = np.load('datas/minDist_migrate_times_list_avg.npy')
print(min_dist_array)
# 28.6

# longest visual time
longest_visual_array = np.load('datas/longest_visual_migrate_times_list_avg.npy')
print(np.mean(longest_visual_array))
# 5.3


# propose
propose_array = np.load('datas/propose_average_migrate_times_2hop_3ms.npy')
print(np.mean(propose_array))
# 20.7