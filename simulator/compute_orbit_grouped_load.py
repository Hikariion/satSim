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


# 首先，我们将480颗卫星展开成一个按照卫星顺序排列的数组
# 然后，我们将这个数组切分成若干个3x4的长方形

def reshape_and_slice_satellites(tle_path, num_columns=3, num_rows=4):
    """
    Reshape satellite names into an array and slice it into several 3x4 rectangles.

    :param tle_path: Path to the TLE file.
    :param num_columns: Number of columns in each rectangle (width).
    :param num_rows: Number of rows in each rectangle (height).
    :return: List of rectangles, each containing 12 satellite names.
    """
    with open(tle_path, 'r') as file:
        lines = file.readlines()

    # Extract satellite names
    satellite_names = [line.strip() for line in lines if line.startswith('V')]

    # Ensure we have the correct total number of satellites
    if len(satellite_names) != 480:
        raise ValueError("The number of satellites does not match the expected total of 480.")

    # Reshape the list into an array with columns representing satellites in order
    satellites_array = [satellite_names[i:i + 12] for i in range(0, len(satellite_names), 12)]

    # Slice the array into 3x4 rectangles
    rectangles = []
    for column_group in range(0, len(satellites_array), num_columns):
        for row in range(num_rows):
            rectangle = []
            for column in range(num_columns):
                satellite_index = column_group + column
                if satellite_index < len(satellites_array):
                    rectangle.append(satellites_array[satellite_index][row])
            rectangles.append(rectangle)

    return rectangles



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
def group_orbit_satellites(tle_path, num_groups=40, group_size=12):
    """
    Function to group satellites from a TLE file into specified number of groups.

    :param tle_path: Path to the TLE file.
    :param num_groups: Number of groups to divide the satellites into.
    :param group_size: Number of satellites in each group.
    :return: Dictionary with satellite names as keys and their group as values.
    """
    # Read TLE file
    with open(tle_path, 'r') as file:
        lines = file.readlines()

    # Initialize group dictionary
    satellite_groups = {}
    for i in range(num_groups):
        for j in range(group_size):
            satellite_index = i * group_size * 3 + j * 3
            if satellite_index < len(lines):
                satellite_name = lines[satellite_index].strip()
                group_name = f'Group {i+1}'
                satellite_groups[satellite_name] = group_name

    return satellite_groups

# Call the function and get the groups
tle_file_path = 'guowang_tle.txt'
satellite_groups = group_orbit_satellites(tle_file_path)

# Displaying a portion of the result for verification
list(satellite_groups.items())[:]  # Displaying first 15 items as an example

def main(file_path):
    satellites = load_tle(tle_file_path)
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始
    df = calculate_subpoints(satellites, start_time)
    return df
# 文件路径
df = main(tle_file_path)
df.to_csv('satellite_orbit_group_load.csv', index=False)
print("计算完成，结果已保存到 'satellite_orbit_group_load.csv'")
