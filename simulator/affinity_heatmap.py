# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
#
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
#
# # 设置字体和图表属性
# plt.rcParams["font.sans-serif"]=['simsun']  # 设置字体
# plt.rcParams["axes.unicode_minus"]=False  # 解决负号乱码问题
# plt.rcParams.update({'font.size': 14})
#
# def plot_full_affinity_matrix(file_path):
#     """
#     Plot a heatmap for the full affinity matrix stored in a CSV file.
#
#     :param file_path: Path to the CSV file containing the affinity matrix.
#     """
#     # Load the affinity matrix from the CSV file
#     affinity_matrix = pd.read_csv(file_path, header=None).values
#
#     # Plotting
#     plt.figure(figsize=(10, 8))
#     plt.imshow(affinity_matrix, cmap='hot', interpolation='nearest')
#     plt.colorbar()
#     plt.title("节点间关联度热力图")
#     plt.xlabel("卫星编号")
#     plt.ylabel("卫星编号")
#     plt.show()
#
# # Example usage:
# # plot_full_affinity_matrix('path_to_your_affinity_matrix_file.csv')
# # Replace 'path_to_your_affinity_matrix_file.csv' with the actual path to your file.
#
#
# # Example usage:
# # plot_lower_triangle_affinity_matrix('path_to_your_affinity_matrix_file.csv')
# # Replace 'path_to_your_affinity_matrix_file.csv' with the actual path to your file.
#
# filepath = 'average_affinity_matrix.csv'
# plot_full_affinity_matrix(filepath)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置字体和图表属性
plt.rcParams["font.sans-serif"]=['simsun']  # 设置字体
plt.rcParams["axes.unicode_minus"]=False  # 解决负号乱码问题
plt.rcParams.update({'font.size': 12})

# Load the CSV file to create the correlation matrix
file_path = 'average_affinity_matrix.csv'
correlation_matrix = pd.read_csv(file_path)

# Resetting the index and columns of the dataframe to represent node indices
correlation_matrix.index = range(correlation_matrix.shape[0])
correlation_matrix.columns = range(correlation_matrix.shape[1])

# Plotting the heatmap with correct labels
plt.figure(figsize=(20, 15))
sns.heatmap(correlation_matrix, cmap='coolwarm', xticklabels=50, yticklabels=50)
plt.title('卫星间周期关联度指数分布图')
plt.xlabel('卫星节点编号')
plt.ylabel('卫星节点编号')
plt.show()

