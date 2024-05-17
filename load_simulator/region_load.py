from typing import Tuple, Dict

# 地理密度信息
region_load = [
    65, 10, 10, 10, 10, 10, 80, 80, 45, 45, 30, 10,
    30, 80, 350, 350, 340, 80, 130, 520, 250, 300, 460, 530, 50,
    10, 15, 300, 460, 50, 100, 200, 120, 160, 400, 220, 40,
    15, 10, 10, 150, 150, 10, 60, 60, 20, 60, 160, 45,
    10, 10, 10, 80, 50, 10, 30, 15, 10, 20, 60, 35,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
]

# 动态流量信息
flu_rate = [0.08, 0.06, 0.06, 0.06, 0.06, 0.14, 0.35, 0.45, 0.9, 1.18, 1.1, 0.91, 0.73, 0.65, 0.72, 0.80, 0.74,
            0.45, 0.28, 0.15, 0.16, 0.18, 0.15, 0.1]

# 纬度
latitude_mapping: Dict[Tuple, int] = {}
# 经度
longitude_mapping: Dict[Tuple, int] = {}

latitude_mapping = {
    (60, 90): 0,
    (30, 60): 1,
    (0, 30): 2,
    (-30, 0): 3,
    (-60, -30): 4,
    (-90, -60): 5
}

longitude_mapping = {
    (-180, -150): 0,
    (-150, -120): 1,
    (-120, -90): 2,
    (-90, -60): 3,
    (-60, -30): 4,
    (-30, 0): 5,
    (0, 30): 6,
    (30, 60): 7,
    (60, 90): 8,
    (90, 120): 9,
    (120, 150): 10,
    (150, 180): 0
}

def get_region_load(latitude, longitude, hour):
    lat_index = None
    long_index = None

    # 查找纬度索引
    for lat_range, index in latitude_mapping.items():
        if lat_range[0] <= latitude < lat_range[1]:
            lat_index = index
            break

    # 查找经度索引
    for long_range, index in longitude_mapping.items():
        if long_range[0] <= longitude < long_range[1]:
            long_index = index
            break

    if lat_index is not None and long_index is not None:
        # 计算region_load的索引
        region_index = lat_index * 12 + long_index
        rate = getFluRate(hour, longitude)
        return region_load[region_index] * rate
    else:
        return None

# def get_hour_from_seconds(seconds):
#     """
#     Given the number of seconds elapsed in a day, return the corresponding hour.
#     Hours are counted from 0 to 23.
#     """
#     # Since there are 3600 seconds in an hour, divide the total seconds by 3600
#     hour = seconds // 3600
#     return hour

def getFluRate(hour, long):
    # 要转化为当地时间
    timezone_offset = int(round(long / 15.0))
    hour = (hour + timezone_offset) % 24
    return flu_rate[hour]






