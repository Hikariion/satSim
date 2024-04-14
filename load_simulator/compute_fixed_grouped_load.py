from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import pandas as pd
from region_load import get_region_load
import numpy as np

satellite_groups = {}

# 16
def split_array_into_2x15_blocks(array):
    blocks = []
    for i in range(0, array.shape[0], 2):  # 从0开始，每次增加2
        block = np.vstack((array[i, :15], array[i+1, :15]))  # 上半块
        blocks.append(block)
    for i in range(0, array.shape[0], 2):
        block = np.vstack((array[i, 15:], array[i+1, 15:]))
        blocks.append(block)
    return blocks


# 20
def split_array_into_vertical_3x8_blocks(array):
    blocks = []
    for col_start in range(0, array.shape[1], 3):  # 从0开始，每次增加3列
        block = array[:8, col_start:col_start + 3]  # 获取3列，8行的块
        blocks.append(block)
    for col_start in range(0, array.shape[1], 3):
        block = array[8:, col_start:col_start + 3]
        blocks.append(block)
    return blocks

# 25
def split_array_into_6x3_blocks(array):
    blocks = []
    for col_start in range(0, array.shape[1], 6):
        block = array[:3, col_start:col_start + 6]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
            block = array[3:6, col_start:col_start+6]
            blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
            block = array[6:9, col_start:col_start+6]
            blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
            block = array[9:12, col_start:col_start+6]
            blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
            block = array[12:, col_start:col_start+6]
            blocks.append(block)
    return blocks

# 30
def split_array_into_8x2_blocks(array):
    blocks = []
    for col_start in range(0, array.shape[1], 2):
        block = array[:8, col_start:col_start + 2]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 2):
        block = array[8:, col_start:col_start + 2]
        blocks.append(block)
    return blocks

# 35
def split_array_into_6x2_blocks(array):
    blocks = []
    for col_start in range(0, array.shape[1], 6):
        block = array[:2, col_start:col_start + 6]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
        block = array[2:4, col_start:col_start + 6]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
        block = array[4:6, col_start:col_start + 6]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
        block = array[6:8, col_start:col_start + 6]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
        block = array[8:10, col_start:col_start + 6]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
        block = array[10:12, col_start:col_start + 6]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 6):
        block = array[12:, col_start:col_start + 6]
        blocks.append(block)
    return blocks

# 40
def split_array_into_vertical_3x4_blocks(array):
    blocks = []
    for col_start in range(0, array.shape[1], 3):
        block = array[:4, col_start:col_start + 3]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 3):
        block = array[4:8, col_start:col_start + 3]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 3):
        block = array[8:12, col_start:col_start + 3]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 3):
        block = array[12:16, col_start:col_start + 3]
        blocks.append(block)
    return blocks

# 45
def split_array_into_2x5_blocks(array):
    blocks = []
    for col_start in range(0, array.shape[1], 2):
        block = array[:5, col_start:col_start + 2]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 2):
        block = array[5:10, col_start:col_start + 2]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 2):
        block = array[10:, col_start:col_start + 2]
        blocks.append(block)
    return blocks

# 50
def split_array_into_3x3_blocks(array):
    blocks = []
    for col_start in range(0, array.shape[1], 3):
        block = array[:3, col_start:col_start + 3]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 3):
        block = array[3:6, col_start:col_start + 3]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 3):
        block = array[6:9, col_start:col_start + 3]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 3):
        block = array[9:12, col_start:col_start + 3]
        blocks.append(block)
    for col_start in range(0, array.shape[1], 3):
        block = array[12:, col_start:col_start + 3]
        blocks.append(block)
    return blocks


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


def calculate_subpoints(satellites, start_time, duration_hours=12):
    end_time = start_time + timedelta(hours=duration_hours)
    data = []
    current_time = start_time
    while current_time.utc_datetime() < end_time.utc_datetime():
        print(current_time.utc_datetime())
        group_loads = {}
        for satellite in satellites:
            geocentric = satellite.at(current_time)
            subpoint = geocentric.subpoint()
            # 计算负载情况
            region_load = get_region_load(subpoint.latitude.degrees, subpoint.longitude.degrees, current_time.utc_datetime().hour)
            group = satellite_groups.get(satellite.name, 'Unknown')
            if group not in group_loads:
                group_loads[group] = []
                group_loads[group].append(region_load)
        mean_loads = [sum(loads) / len(loads) for loads in group_loads.values() if loads]
        if mean_loads:
            # 计算这些均值的标准差
            overall_std = np.std(mean_loads)
            data.append({
                'Timestamp': current_time.utc_datetime(),
                'Overall Load STD': overall_std,
            })

        current_time += timedelta(minutes=2)
    return pd.DataFrame(data)


def fixed_group_satellites(tle_path, blocks):
    with open(tle_path, 'r') as file:
        lines = file.readlines()

    satellite_groups = {}

    for i, block in enumerate(blocks):
        for id_list in block:
            for id in id_list:
                satellite_groups[f'GW #{id}'] = f'Group {i+1}'

    return satellite_groups

if __name__ == '__main__':
    array = np.arange(1, 481).reshape(16, 30, order='F')
    # 再次调用函数来分割数组
    blocks = split_array_into_3x3_blocks(array)

    # 显示第一组以确认
    # first_block_corrected = blocks_2x15[10]

    # print(first_block_corrected)
    # print(len(blocks))

    tle_file_path = 'guowang_tle_suit.txt'
    ts = load.timescale()

    satellites = load_tle(tle_file_path)
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)

    satellite_groups = fixed_group_satellites(tle_file_path, blocks)
    #
    # # print(satellite_groups)
    #
    df = calculate_subpoints(satellites, start_time)
    df.to_csv('datas/fixed_group_50_experiments_avg_load_12H.csv', index=False)
    print("计算完成，平均结果已保存到 'datas/fixed_group_50_experiments_avg_load_12H.csv'")