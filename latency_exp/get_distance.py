from skyfield.api import EarthSatellite, Topos, load
from datetime import datetime, timedelta
import numpy as np

# 创建天文学数据加载器
ts = load.timescale()

# TLE 数据
tle_line1 = '1 25544U 98067A   20029.54791435  .00001264  00000-0  33266-4 0  9998'
tle_line2 = '2 25544  51.6431  21.3833 0005074  59.9664  81.5404 15.49292828209822'

# 创建卫星对象
satellite = EarthSatellite(tle_line1, tle_line2)

# 地面站坐标（纬度、经度、海拔高度）
ground_station = Topos(latitude_degrees=40.0, longitude_degrees=-80.0, elevation_m=0.0)

# 设置起始时间和计算距离的持续时间（秒）
start_time = ts.utc(2023, 1, 1, 0, 0, 0)
duration = 36000  # 计算前60秒的距离

# 初始化用于存储距离的数组
distances = []

# 遍历每个时间点
for t in range(duration):
    time = start_time + timedelta(seconds=t)
    satellite_position = satellite.at(time)
    ground_station_position = ground_station.at(time)
    # 计算地面站和卫星的笛卡尔坐标差
    diff = satellite_position.position.km - ground_station_position.position.km
    # 计算欧几里得距离
    distance = np.linalg.norm(diff)
    distances.append(distance)

# 输出结果
for i, distance in enumerate(distances, 1):
    print(f"Time: {start_time.utc_datetime() + timedelta(seconds=i-1)}, Distance: {distance} km")


