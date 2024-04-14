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

if __name__ == '__main__':
    tle_file_path = 'gw_tle.txt'
    ts = load.timescale()
    satellites = parse_tle(tle_file_path)
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)
    end_time = start_time + timedelta(seconds=3600)

    total_migrate_times_lists = []
    total_closest_distances_lists = []

    coords = np.load('random_coords.npy')

    exp_round = 0

    for lat, lon in coords:
        exp_round += 1
        print(f'exp times {exp_round}')

        ground_station = Topos(latitude_degrees=lat, longitude_degrees=lon)

        start_time = ts.utc(2023, 1, 1, 0, 0, 0)
        end_time = start_time + timedelta(seconds=3600)
        times = ts.linspace(start_time, end_time, 3600)

        migrate_times = 0
        closest_distances = []

        previous_closest_satellite = None

        for time in times:
            print(time.utc_datetime())
            min_distance = float('inf')
            current_closest_satellite = None
            for satellite in satellites.values():
                distance = get_distance(satellite, ground_station, time)
                if distance < min_distance:
                    current_closest_satellite = satellite
            if current_closest_satellite != previous_closest_satellite:
                migrate_times += 1  # Increment the migration count

            previous_closest_satellite = current_closest_satellite
            closest_distances.append(min_distance)

        total_migrate_times_lists.append(migrate_times)
        total_closest_distances_lists.append(closest_distances)

    average_distance = np.mean(total_closest_distances_lists, axis=0)
    average_migrate_times = np.mean(total_migrate_times_lists, axis=0)

    # 保存迁移次数列表和平均距离到文件
    print(total_migrate_times_lists)
    print(average_migrate_times)
    np.save('datas/minDist_migrate_times_list_avg.npy', average_migrate_times)
    np.save('datas/minDist_average_distance.npy', average_distance)


