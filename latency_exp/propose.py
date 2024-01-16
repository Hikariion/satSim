from skyfield.api import Topos, load, EarthSatellite, utc
from datetime import timedelta
from collections import deque
import numpy as np
import json

# 读取TLE文件
file_path = 'guowang_tle.txt'  # 替换为您的TLE文件路径
# 加载Skyfield的时间和星历表
ts = load.timescale()
# Ground station coordinates (latitude, longitude)
ground_station_coords = (39.9, 116.3)  # Beijing, China

# Initialize the ground station position
ground_station = Topos(latitude_degrees=ground_station_coords[0], longitude_degrees=ground_station_coords[1])

# 每跳的链路时延
hop_latency = 3  # 单位：ms

# 解析TLE文件并创建卫星字典
def parse_tle(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    satellites = {}
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        satellite = EarthSatellite(line1, line2, name, ts)
        satellites[name] = satellite
    return satellites

# 用于获取卫星与地面某坐标之间的距离
def get_distance(satellite: EarthSatellite, ground_station, time):
    # 地面站坐标（纬度、经度、海拔高度）
    satellite_position = satellite.at(time)
    ground_station_position = ground_station.at(time)
    # 计算地面站和卫星的笛卡尔坐标差
    diff = satellite_position.position.km - ground_station_position.position.km
    # 计算欧几里得距离
    distance = np.linalg.norm(diff)
    return distance

def get_hops(satellites, source_satellite_name, target_satellite_name, ts, time):
    if source_satellite_name not in satellites or target_satellite_name not in satellites:
        return "Source or target satellite not found"

    # 初始化队列和访问过的卫星集合
    queue = deque([(source_satellite_name, 0)])
    visited = set([source_satellite_name])

    while queue:
        current_satellite_name, hops = queue.popleft()

        # 检查是否达到目标卫星
        if current_satellite_name == target_satellite_name:
            return hops

        current_satellite = satellites[current_satellite_name]
        current_satellite_position = current_satellite.at(time)

        distances = []
        for name, sat in satellites.items():
            if name not in visited:
                distance = (sat.at(time) - current_satellite_position).distance().km
                distances.append((name, distance))

        closest_satellites = sorted(distances, key=lambda x: x[1])[:4]
        for satellite_name, _ in closest_satellites:
            if satellite_name not in visited:
                queue.append((satellite_name, hops + 1))
                visited.add(satellite_name)

        return "Target satellite not reachable"



# 找出最近 n 跳的卫星集合
def calculate_distances_to_satellite(satellites, target_satellite_name, ts, time, n=1):
    target_satellite = satellites.get(target_satellite_name)
    if not target_satellite:
        return "Target satellite not found"

    # 初始化集合包含目标卫星
    current_satellites = {target_satellite_name}

    for _ in range(n):
        next_satellites = set()
        for satellite_name in current_satellites:
            satellite = satellites.get(satellite_name)
            satellite_position = satellite.at(time)

            # 计算距离并且排序
            distances = []
            for name, sat in satellites.items():
                if name != satellite_name:
                    if name != satellite_name:
                        distance = (sat.at(time) - satellite_position).distance().km
                        distances.append((name, distance))

            closest = sorted(distances, key=lambda x: x[1])[:4]
            next_satellites.update([name for name, _ in closest])

        # 更新当前卫星集合
        current_satellites = next_satellites


    return list(current_satellites)

# 获得预计时间内的满足时延约束的集合
def get_S():
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始
    end_time = start_time + timedelta(seconds=3600)

    # Load the satellites from the TLE data file
    satellites = parse_tle(file_path)

    # Calculate the closest satellite at each time step
    speed_of_light = 299792.458  # in km/s
    times = ts.linspace(start_time, end_time, 3600)

    previous_closest_satellite = None
    migrate_times = 0

    closest_distances = []

    S = []


    # TODO: 获得预计时间内的满足时延约束的集合
    for time in times:
        print(time.utc_datetime())
        min_distance = float('inf')
        current_closest_satellite = None
        for satellite in satellites.values():
            distance = get_distance(satellite, ground_station, time)
            if distance < min_distance:
                min_distance = distance
                current_closest_satellite = satellite
        if current_closest_satellite != previous_closest_satellite and previous_closest_satellite is not None:
            # get peers near cloest satellite
            # nearest_satellites = calculate_distances_to_satellite(satellites, current_closest_satellite.name, ts, time, 2)
            # print(nearest_satellites)
            migrate_times += 1  # Increment the migration count
            S.append(calculate_distances_to_satellite(satellites, current_closest_satellite.name, ts, time, 1))


        previous_closest_satellite = current_closest_satellite
        closest_distances.append(min_distance)

    print(len(S))
    # 将 S 持久化
    with open('S.json', 'w') as file:
        json.dump(S, file)


# 计算迁移路径
def get_migration_path():
    # 读 S
    S = []
    with open('S.json', 'r') as file:
        S = json.load(file)


    # 对S进行转换
    transformed_S = []
    for sublist in S:
        # print(sublist)
        transformed_sublist = []
        for item in sublist:
            # print(item)
            if '#' in item:
                number_part = item.split('#')[-1].strip()
                if number_part.isdigit():
                    transformed_sublist.append(int(number_part))
                else:
                    print(f"Warning: Found an invalid number format in '{item}'")
            else:
                print(f"Warning: No '#' found in '{item}'")
        transformed_S.append(transformed_sublist)

    print(transformed_S)

    # dp
    for s in transformed_S:
        s.sort()

    n = len(transformed_S)
    dp = [[float('inf')]*len(transformed_S[i]) for i in range(n)]
    pre = [[-1]*len(transformed_S[i]) for i in range(n)]

    for j in range(len(transformed_S[0])):
        dp[0][j] = 1

    for i in range(1, n):
        for j in range(len(transformed_S[i])):
            for k in range(len(transformed_S[i-1])):
                if transformed_S[i][j] not in transformed_S[i-1][:k+1]:
                    if dp[i-1][k]+1 < dp[i][j]:
                        dp[i][j] = dp[i-1][k]+1
                        pre[i][j] = k
                else:
                    if dp[i-1][k] < dp[i][j]:
                        dp[i][j] = dp[i-1][k]
                        pre[i][j] = k

    # Find the minimum distinct subsequence length
    min_distinct_len = min(dp[n-1])

    # Construct one of the possible distinct subsequences
    sequence = []
    min_idx = dp[n-1].index(min_distinct_len)
    sequence.append(transformed_S[n-1][min_idx])
    idx = min_idx
    for i in range(n-2, -1, -1):
        idx = pre[i+1][idx]
        sequence.append(transformed_S[i][idx])

    sequence = sequence[::-1]
    return sequence


if __name__ == '__main__':
    # get_S()
    sequence = get_migration_path()

    print(sequence)
    print(len(sequence))




