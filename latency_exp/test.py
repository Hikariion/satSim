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

    return alt.degrees > 45

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

if __name__ == '__main__':
    satellites = parse_tle(tle_file_path)

    current_time = ts.now()

    observer = Topos(latitude_degrees=39.9, longitude_degrees=118.3)

    for satellite in satellites.values():
        difference = satellite - observer
        topocentric = difference.at(current_time)
        alt, az, distance = topocentric.altaz()
        print(alt.degrees)





