from skyfield.api import Topos, load, EarthSatellite, utc
from datetime import timedelta
import numpy as np

# 读取TLE文件
file_path = 'guowang_tle.txt'  # 替换为您的TLE文件路径
# 加载Skyfield的时间和星历表
ts = load.timescale()
# Ground station coordinates (latitude, longitude)
ground_station_coords = (39.9, 116.3)  # Beijing, China

# Initialize the ground station position
ground_station = Topos(latitude_degrees=ground_station_coords[0], longitude_degrees=ground_station_coords[1])

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


# 计算卫星距离指定卫星的距离
def calculate_distances_to_satellite(satellites, target_satellite_name, ts, time):
    target_satellite = satellites.get(target_satellite_name)
    if not target_satellite:
        return "Target satellite not found"

    target_position = target_satellite.at(time)

    distances = []
    for name, sat in satellites.items():
        if name != target_satellite_name:
            distance = (sat.at(time) - target_position).distance().km
            distances.append((name, distance))

    return sorted(distances, key=lambda x: x[1])[:4]

def main():
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

    for time in times:
        # print(time.utc_datetime())
        min_distance = float('inf')
        current_closest_satellite = None
        for satellite in satellites.values():
            distance = get_distance(satellite, ground_station, time)
            if distance < min_distance:
                min_distance = distance
                current_closest_satellite = satellite
        if current_closest_satellite != previous_closest_satellite and previous_closest_satellite is not None:
            # get peers near cloest satellite
            nearest_satellites = calculate_distances_to_satellite(satellites, current_closest_satellite.name, ts, time)
            print(nearest_satellites)
            migrate_times += 1  # Increment the migration count

        previous_closest_satellite = current_closest_satellite
        closest_distances.append(min_distance)

if __name__ == '__main__':
    main()




