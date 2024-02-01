from skyfield.api import Topos, EarthSatellite, load
from datetime import datetime, timezone, timedelta
import numpy as np

# Load the satellites from the TLE data file
tle_file_path = 'gw_tle.txt'
ts = load.timescale()
start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始
end_time = start_time + timedelta(seconds=3600)
# Calculate the closest satellite at each time step
speed_of_light = 299792.458  # in km/s

def remaining_visibility_time(observer: Topos, satellite: EarthSatellite, time: datetime) -> int:
    ts = load.timescale()
    end_time = time + timedelta(hours=2)  # 假设最多检查未来2小时内的可见性
    current_time = time
    while current_time.time() <= end_time.time():
        if not is_satellite_visible(observer, satellite, current_time):
            break
        current_time += timedelta(seconds=1)  # 每30秒检查一次
    return int((current_time - time).total_seconds())


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

def is_satellite_visible(observer: Topos, satellite: EarthSatellite, time: datetime) -> bool:
    ts = load.timescale()
    skyfield_time = ts.from_datetime(time)

    # 计算卫星相对于观察点在指定时间的位置
    difference = satellite - observer
    topocentric = difference.at(skyfield_time)

    alt, az, distance = topocentric.altaz()

    # 如果高度角（Altitude）大于45°，则可见
    return alt.degrees > 0

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

def test():
    satellites = parse_tle(tle_file_path)

    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始

    # Ground station coordinates (latitude, longitude)
    ground_station_coords = (39.9, 116.3)  # Beijing, China

    # Initialize the ground station position
    ground_station = Topos(latitude_degrees=ground_station_coords[0], longitude_degrees=ground_station_coords[1])

    visible_satellites = []

    for satellite in satellites.values():
        if(is_satellite_visible(ground_station, satellite, start_time.utc_datetime())):
            visible_satellites.append(satellite)

    for visible_satellite in visible_satellites:
        print(visible_satellite.name)
        print(remaining_visibility_time(ground_station, visible_satellite, start_time.utc_datetime()))

def main():
    satellites = parse_tle(tle_file_path)
    # Ground station coordinates (latitude, longitude)
    ground_station_coords = (39.9, 116.3)  # Beijing, China

    # Initialize the ground station position
    ground_station = Topos(latitude_degrees=ground_station_coords[0], longitude_degrees=ground_station_coords[1])

    current_satellite = None
    migrate_times = 0

    times = ts.linspace(start_time, end_time, 3600)

    switch_time = start_time

    distances = []

    for time in times:
        print(time.utc_datetime())

        if time.utc_datetime().time() >= switch_time.utc_datetime().time():
            # 迁移次数递增
            migrate_times += 1

            # 找到当前的可见卫星列表
            visible_satellites = []
            for satellite in satellites.values():
                if (is_satellite_visible(ground_station, satellite, time.utc_datetime())):
                    visible_satellites.append(satellite)
            # 获得可见时间最长的卫星
            longest_visible_time = 0
            longest_visible_satellite = None

            for visible_satellite in visible_satellites:
                visible_time = remaining_visibility_time(ground_station, visible_satellite, time.utc_datetime())
                if visible_time > longest_visible_time:
                    longest_visible_time = visible_time
                    longest_visible_satellite = visible_satellite

            # 重置切换时间
            switch_time = time + timedelta(seconds=longest_visible_time)
            # 重置当前卫星
            current_satellite = longest_visible_satellite
        # 计算当前卫星的距离
        current_distance = get_distance(current_satellite, ground_station, time)
        distances.append(current_distance)

    distance_file_path = 'datas/longest_visual_distance.npy'
    np.save(distance_file_path, distances)
    print('迁移次数：', migrate_times)

main()

#迁移次数： 6
