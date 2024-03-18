import random

from skyfield.api import Topos, load, EarthSatellite, utc
from datetime import timedelta
from collections import deque
import numpy as np
import json

# 读取TLE文件
file_path = 'gw_tle.txt'  # 替换为您的TLE文件路径
# 加载Skyfield的时间和星历表
ts = load.timescale()

# Initialize the ground station position
ground_station = Topos(latitude_degrees=0, longitude_degrees=0)

# 每跳的链路时延
hop_latency = 4  # 单位：ms

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

def get_hops(satellites, source_satellite_name, target_satellite_name, time):
    if source_satellite_name not in satellites or target_satellite_name not in satellites:
        raise "Source or target satellite not found"

    if source_satellite_name == target_satellite_name:
        return 0


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

        closest_satellites = sorted(distances, key=lambda x: x[1])[:5]
        for satellite_name, _ in closest_satellites:
            if satellite_name not in visited:
                queue.append((satellite_name, hops + 1))
                visited.add(satellite_name)

    raise "Target satellite not reachable"



# 找出最近 n 跳的卫星集合
def calculate_distances_to_satellite(satellites, target_satellite_name, time, n):
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

            closest = sorted(distances, key=lambda x: x[1])[:5]
            next_satellites.update([name for name, _ in closest])

        # 更新当前卫星集合
        current_satellites = next_satellites


    return list(current_satellites)

# 获得预计时间内的满足时延约束的集合
def get_S(exp_num, hops):
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始
    end_time = start_time + timedelta(seconds=3600)

    # Load the satellites from the TLE data file
    satellites = parse_tle(file_path)

    times = ts.linspace(start_time, end_time, 3600)

    previous_closest_satellite = None


    S = []

    for time in times:
        print(time.utc_datetime())
        min_distance = float('inf')
        current_closest_satellite = None
        for satellite in satellites.values():
            distance = get_distance(satellite, ground_station, time)
            if distance < min_distance:
                min_distance = distance
                current_closest_satellite = satellite
        if current_closest_satellite != previous_closest_satellite:
            S.append(calculate_distances_to_satellite(satellites, current_closest_satellite.name, time, hops))

        previous_closest_satellite = current_closest_satellite

    print(len(S))
    # 将 S 持久化
    with open(f'datas/{exp_num}/S_{hops}hop.json', 'w') as file:
        json.dump(S, file)
    # S 作为 txt 持久化
    with open(f'datas/{exp_num}/S_{hops}hop.txt', 'w') as file:
        for s in S:
            file.write(str(s)+'\n')


# 计算迁移路径
def get_migration_path(exp_num, hops):
    # 读 S
    with open(f'datas/{exp_num}/S_{hops}hop.json', 'r') as file:
        S = json.load(file)

    # dp
    for s in S:
        s.sort()

    n = len(S)
    dp = [[float('inf')]*len(S[i]) for i in range(n)]
    pre = [[-1]*len(S[i]) for i in range(n)]

    for j in range(len(S[0])):
        dp[0][j] = 1

    for i in range(1, n):
        for j in range(len(S[i])):
            for k in range(len(S[i-1])):
                if S[i][j] not in S[i-1][:k+1]:
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
    sequence.append(S[n-1][min_idx])
    idx = min_idx
    for i in range(n-2, -1, -1):
        idx = pre[i+1][idx]
        sequence.append(S[i][idx])

    sequence = sequence[::-1]
    return sequence

def calculate_migration_times(sequence):
    cnt = 0
    current = sequence[0]
    for i in sequence:
        if i != current:
            cnt += 1
            current = i
    return cnt

#  计算时延
def get_delay(sequence):
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始
    end_time = start_time + timedelta(seconds=3600)

    # Load the satellites from the TLE data file
    satellites = parse_tle(file_path)

    # Calculate the closest satellite at each time step
    speed_of_light = 299.792458  # in km/ms
    times = ts.linspace(start_time, end_time, 3600)

    previous_closest_satellite = None

    delays = []

    # idx for service satellite
    service_satellite_idx = -1

    hops = 0

    for time in times:
        print(time.utc_datetime())
        min_distance = float('inf')

        current_closest_satellite = None

        for satellite in satellites.values():
            distance = get_distance(satellite, ground_station, time)
            if distance < min_distance:
                min_distance = distance
                current_closest_satellite = satellite
        if current_closest_satellite != previous_closest_satellite:
            service_satellite_idx += 1
            hops = get_hops(satellites, current_closest_satellite.name, sequence[service_satellite_idx], time)

        previous_closest_satellite = current_closest_satellite
        delay = min_distance * 2 / speed_of_light
        print("service_satellite_idx = ", service_satellite_idx)
        # 从 S[service_satellite_idx] 随机选一个元素
        print("hops = ", hops)
        mid_delay = hops * hop_latency
        print(delay+mid_delay)
        delays.append(delay + mid_delay)

    return delays


if __name__ == '__main__':

    hops = 1

    coords = np.load('random_coords.npy')

    exp_round = 0

    delay_times = []
    migrate_times = []

    for lat, lon in coords:
        exp_round += 1
        print(exp_round)
        ground_station = Topos(latitude_degrees=lat, longitude_degrees=lon)
        get_S(exp_round, hops)
        sequence = get_migration_path(exp_round, hops)
        times = calculate_migration_times(sequence)
        delays = get_delay(sequence)

        migrate_times.append(times)
        delay_times.append(delays)


    average_delay_times = np.mean(delay_times, axis=0)
    average_migrate_times = np.mean(migrate_times, axis=0)

    np.save(f'datas/propose_average_migrate_times_{hops}hop_4ms.npy', average_migrate_times)
    np.save(f'datas/propose_average_delay_times_{hops}hop_4ms.npy', average_delay_times)









