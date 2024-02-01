from skyfield.api import Topos, load, EarthSatellite
from datetime import timedelta
import numpy as np

# Function to parse TLE data from a file
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

# Ground station coordinates (latitude, longitude)
ground_station_coords = (39.9, 116.3)  # Beijing, China

# Initialize the ground station position
ground_station = Topos(latitude_degrees=ground_station_coords[0], longitude_degrees=ground_station_coords[1])

# Load timescale and initialize a time period for calculations
ts = load.timescale()
start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始
end_time = start_time + timedelta(seconds=3600)

# Load the satellites from the TLE data file
tle_file_path = 'gw_tle.txt'
satellites = parse_tle(tle_file_path)

# Calculate the closest satellite at each time step
speed_of_light = 299792.458  # in km/s
times = ts.linspace(start_time, end_time, 3600)

previous_closest_satellite = None
migrate_times  = 0

closest_distances = []
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
        migrate_times += 1  # Increment the migration count

    previous_closest_satellite = current_closest_satellite
    closest_distances.append(min_distance)

closest_distances_file_path = 'datas/closest_distances.npy'
np.save(closest_distances_file_path, closest_distances)

print('迁移次数：',migrate_times)

#迁移次数： 21


