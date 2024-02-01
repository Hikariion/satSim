from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from region_load import get_region_load
import random

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

if __name__ == '__main__':
    satellite_load_data_file_path = 'datas/satellite_permin_load.csv'
    satellite_load_data = pd.read_csv(satellite_load_data_file_path)
    satellite_load_data['Timestamp'] = pd.to_datetime(satellite_load_data['Timestamp'])

    # TLE File path
    tle_file_path = 'guowang_tle_suit.txt'

    # 加载时间模块
    ts = load.timescale()
    satellites = load_tle(tle_file_path)
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # Start time set to Jan 1, 2023

    matching_load_data = satellite_load_data[
        (satellite_load_data['Satellite'] == 'GW #1')  &
        (satellite_load_data['Timestamp'] == start_time.utc_datetime())
        ]

    print(matching_load_data['Load'].values[0])
