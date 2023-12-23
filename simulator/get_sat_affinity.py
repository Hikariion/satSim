from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import pandas as pd
from region_load import get_region_load
import numpy as np

# 加载时间模块
ts = load.timescale()

# 读取并解析TLE数据
def load_tle(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    satellites = []
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        satellite = EarthSatellite(line1, line2, name, ts)
        satellites.append(satellite)
    return satellites


# 计算星下点坐标以及负载
def calculate_subpoints(satellites, start_time, duration_hours=24):
    end_time = start_time + timedelta(hours=duration_hours)
    data = []
    current_time = start_time
    while current_time.utc_datetime() < end_time.utc_datetime():
        print(current_time.utc_datetime())
        for satellite in satellites:
            geocentric = satellite.at(current_time)
            subpoint = geocentric.subpoint()
            # 计算负载情况
            region_load = get_region_load(subpoint.latitude.degrees, subpoint.longitude.degrees, current_time.utc_datetime().hour)
            data.append({
                'Timestamp': current_time.utc_datetime(),
                'Satellite': satellite.name,
                # 'Latitude': subpoint.latitude.degrees,
                # 'Longitude': subpoint.longitude.degrees,
                'Load': region_load,
            })
        # data 里存储了这一时刻所有卫星的负载情况
        # 计算这一时刻各卫星之间的亲和度
        current_time += timedelta(minutes=1)
    return pd.DataFrame(data)

def calculate_affinity_matrix(load_values):
    load_array = np.array(load_values)
    difference_matrix = np.abs(load_array.reshape(-1, 1) - load_array)
    max_diff = np.max(difference_matrix) if np.max(difference_matrix) > 0 else 1
    affinity_matrix = difference_matrix / max_diff
    return affinity_matrix

# 计算亲和度矩阵
def calculate_affinity(load_df):
    time_points = load_df['Timestamp'].unique()
    affinity_matrices = []

    for time_point in time_points:
        print(time_point)
        # 同一时刻所有卫星的load
        loads = load_df[load_df['Timestamp'] == time_point]['Load'].tolist()

        affinity_matrix = calculate_affinity_matrix(loads)
        affinity_matrices.append(affinity_matrix)

    return np.mean(affinity_matrices, axis=0)

# 从文件读取卫星负载数据
def load_satellite_loads(file_path):
    return pd.read_csv(file_path)

# 主程序
def main(file_path):
    load_df = load_satellite_loads(file_path)
    # 计算亲和度矩阵
    average_affinity_matrix = calculate_affinity(load_df)

    # 保存数据
    # load_df.to_csv('satellite_loads.csv', index=False)
    np.savetxt('average_affinity_matrix.csv', average_affinity_matrix, delimiter=',', fmt='%f')

    print("Data saved to 'average_affinity_matrix.csv'.")


# 文件路径
file_path = 'satellite_permin_load.csv'  # TLE数据文件路径
main(file_path)

