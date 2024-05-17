# 获取各个时刻星下点坐标
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
        for satellite in satellites:
            geocentric = satellite.at(current_time)
            subpoint = geocentric.subpoint()
            # 计算负载情况
            region_load = get_region_load(subpoint.latitude.degrees, subpoint.longitude.degrees, current_time.utc_datetime().hour)
            data.append({
                'Timestamp': current_time.utc_datetime(),
                'Satellite': satellite.name,
                'Latitude': subpoint.latitude.degrees,
                'Longitude': subpoint.longitude.degrees,
                # 'Load': region_load,
            })
        # data 里存储了这一时刻所有卫星的负载情况

        current_time += timedelta(minutes=1)
    return pd.DataFrame(data)

# 主程序
def main(file_path):
    satellites = load_tle(file_path)
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # 2023年0点0分0秒开始
    df = calculate_subpoints(satellites, start_time)
    return df

# 文件路径
file_path = 'guowang_tle_suit.txt'  # TLE数据文件路径
df = main(file_path)
df.to_csv('satellite_subpoints_suit.csv', index=False)
print("计算完成，结果已保存到 'satellite_subpoints.csv'")
