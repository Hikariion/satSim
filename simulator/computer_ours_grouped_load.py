from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import pandas as pd
from region_load import get_region_load

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


# 计算星下点坐标
def calculate_subpoints(satellites, start_time, duration_hours=24):
    end_time = start_time + timedelta(hours=duration_hours)
    data = []
    current_time = start_time
    while current_time.utc_datetime() < end_time.utc_datetime():
        print(current_time.utc_datetime())
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

        current_time += timedelta(minutes=10)
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
def ours_group_satellites(grouped_path, num_groups=40, group_size=12):
    df = pd.read_csv(grouped_path)

    # Convert the DataFrame to a dictionary with the required format
    satellite_groups = {f"{row['Node']}": f"{row['Cluster']}" for _, row in df.iterrows()}

    return satellite_groups

# Call the function and get the groups
tle_file_path = 'guowang_tle.txt'
groupedn_file_path = 'node_cluster_50_assignments_affinity.csv'
satellite_groups = ours_group_satellites(groupedn_file_path)
# print(satellite_groups)

# Displaying a portion of the result for verification
list(satellite_groups.items())[:]  # Displaying first 15 items as an example

def main(file_path):
    satellites = load_tle(tle_file_path)
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始
    df = calculate_subpoints(satellites, start_time)
    return df
# 文件路径
df = main(tle_file_path)
df.to_csv('satellite_ours_group_50_load.csv', index=False)
print("计算完成，结果已保存到 'satellite_ours_group_50_load.csv'")
