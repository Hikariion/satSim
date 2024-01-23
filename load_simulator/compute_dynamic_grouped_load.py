from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import pandas as pd
from region_load import get_region_load
import random

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

# def randomly_group_satellites(tle_path, num_groups=40):
#     """
#     Randomly group satellites from a TLE file into a specified number of groups.
#
#     :param tle_path: Path to the TLE file.
#     :param num_groups: Number of groups to divide the satellites into.
#     :return: Dictionary with satellite names as keys and their group as values.
#     """
#     with open(tle_path, 'r') as file:
#         lines = file.readlines()
#
#     # Extract satellite names
#     satellite_names = [line.strip() for line in lines if line.startswith('V')]
#
#     # Randomly shuffle the satellite list
#     random.shuffle(satellite_names)
#
#     # Initialize the dictionary to hold the group assignments
#     satellite_groups = {}
#     satellites_per_group = len(satellite_names) // num_groups
#
#     # Assign satellites to groups
#     for group_index in range(num_groups):
#         for satellite_index in range(satellites_per_group):
#             satellite = satellite_names[group_index * satellites_per_group + satellite_index]
#             satellite_groups[satellite] = f'Group {group_index + 1}'
#
#     return satellite_groups

# 定义函数来计算指定时刻的一小时内每个卫星的平均负载并分组
def calculate_average_loads(satellite_load_data, start_time, num_groups):
    # 确定结束时间
    end_time = start_time + timedelta(hours=1)

    # 筛选出在指定时间范围内的数据
    filtered_data = satellite_load_data[(satellite_load_data['Timestamp'] >= start_time) &
                         (satellite_load_data['Timestamp'] < end_time)]

    # 计算每个卫星的平均负载
    average_loads = filtered_data.groupby('Satellite')['Load'].mean()

    # 将卫星根据平均负载排序并分组
    sorted_satellites = average_loads.sort_values().index.tolist()
    satellites_per_group = len(sorted_satellites) // num_groups
    satellite_groups = {}
    for i in range(num_groups):
        group_satellites = sorted_satellites[i * satellites_per_group: (i + 1) * satellites_per_group]
        for satellite in group_satellites:
            satellite_groups[satellite] = f'Group {i + 1}'

    return satellite_groups

# 计算星下点坐标及负载
def calculate_subpoints(satellites, start_time, duration_hours, file_path, satellite_load_data, group_numbers):
    end_time = start_time + timedelta(hours=duration_hours)
    data = []
    current_time = start_time
    hour_counter = 0

    while current_time.utc_datetime() < end_time.utc_datetime():
        print(current_time.utc_datetime())

        # 每小时重新分组
        if hour_counter % 60 == 0:
            print("重新分组")
            satellite_groups = calculate_average_loads(satellite_load_data, current_time.utc_datetime(), group_numbers)

        group_loads = {}
        for satellite in satellites:
            geocentric = satellite.at(current_time)
            subpoint = geocentric.subpoint()
            # 计算负载情况
            region_load = get_region_load(subpoint.latitude.degrees, subpoint.longitude.degrees, current_time.utc_datetime().hour)
            group = satellite_groups.get(satellite.name, 'Unknown')
            if group not in group_loads:
                group_loads[group] = []
                group_loads[group].append(region_load)
        mean_loads = [sum(loads) / len(loads) for loads in group_loads.values() if loads]
        if mean_loads:
            # 计算这些均值的标准差
            overall_std = pd.Series(mean_loads).std()
            data.append({
                'Timestamp': current_time.utc_datetime(),
                'Overall Load STD': overall_std,
            })

        current_time += timedelta(minutes=2)
        hour_counter += 2
    return pd.DataFrame(data)

satellite_groups = {}
# 示例分组
# satellite_groups = {
#     'Satellite1': 'Group1',
#     'Satellite2': 'Group1',
#     'Satellite3': 'Group2',
#     # ... 其他卫星和它们的分组
# }

# grouped by orbit

# Call the function and get the groups
tle_file_path = 'guowang_tle.txt'


# Displaying a portion of the result for verification
list(satellite_groups.items())[:]  # Displaying first 15 items as an example

def main(file_path, num_experiments=10):
    satellites = load_tle(file_path)
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # Start time set to Jan 1, 2023

    all_data = []

    satellite_load_data_file_path = 'datas/satellite_permin_load.csv'
    satellite_load_data = pd.read_csv(satellite_load_data_file_path)
    satellite_load_data['Timestamp'] = pd.to_datetime(satellite_load_data['Timestamp'])


    # Generate new random groupings for each experiment

    # Calculate subpoint loads for the current grouping
    df = calculate_subpoints(satellites, start_time, 12, file_path, satellite_load_data, 30)
    all_data.append(df)

    # Averaging the results
    averaged_data = pd.concat(all_data).groupby(level=0).mean()

    return averaged_data

# File path
tle_file_path = 'guowang_tle_suit.txt'

# Running the experiments and getting averaged results
averaged_df = main(tle_file_path)
averaged_df.to_csv('dynamic_group_30_experiments_avg_load_12H.csv', index=False)
print("计算完成，平均结果已保存到 'dynamic_group_30_experiments_avg_load_12H.csv'")

