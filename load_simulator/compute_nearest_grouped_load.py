# import numpy as np
# from skyfield.api import load, EarthSatellite
# from datetime import datetime, timedelta
# import pandas as pd
# from region_load import get_region_load
# import random
#
#
# def load_tle(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#     satellites = []
#     for i in range(0, len(lines), 3):
#         name = lines[i].strip()
#         line1 = lines[i + 1].strip()
#         line2 = lines[i + 2].strip()
#         satellite = EarthSatellite(line1, line2, name, ts)
#         satellites.append(satellite)
#     return satellites
#
# def nearst_group_satellites(tle_path, num_groups=60):
#
#
#
# if __name__ == '__main__':
#     corrected_matrix = np.zeros((30, 16), dtype=int)
#     # 填充矩阵
#     for i in range(16):
#         start_num = i * 30 + 1
#         corrected_matrix[:, i] = np.arange(start_num, start_num + 30)
#
#     # 分解矩阵为小矩形
#     sub_matrices = []
#
#     # 确定小矩形的尺寸
#     sub_matrix_height = 4
#     sub_matrix_width = 4
#
#     # 计算在每个维度上需要迭代的次数
#     for i in range(0, corrected_matrix.shape[0], sub_matrix_height):
#         for j in range(0, corrected_matrix.shape[1], sub_matrix_width):
#             # 提取子矩阵
#             sub_matrix = corrected_matrix[i:i+sub_matrix_height, j:j+sub_matrix_width]
#             # 将子矩阵转换为列表，并添加到结果列表中
#             sub_matrices.append(sub_matrix.flatten())
#     # 显示一个示例子矩阵以验证
#     print(sub_matrices[1])
#
#
#
#
