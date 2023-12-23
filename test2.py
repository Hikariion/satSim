from orbit_predictor.sources import get_predictor_from_tle_lines
from datetime import datetime, timedelta
from load import region_load

def parse_tle_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    satellites = []
    for i in range(0, len(lines), 3):
        satellite = {
            'name': lines[i].strip(),
            'line1': lines[i + 1].strip(),
            'line2': lines[i + 2].strip()
        }
        satellites.append(satellite)
    print(len(satellites))
    return satellites



# 文件路径
file_path = 'tle/guowang.txt'

# 从文件中解析TLE数据
satellites = parse_tle_from_file(file_path)

# # 输出解析结果
# for sat in satellites:
#     print(sat)

satLoad = []
count = 0

for sat in satellites:
    count += 1
    print(count)
    # Create a predictor for the satellite
    predictor = get_predictor_from_tle_lines([sat['line1'], sat['line2']])

    # Start time and end time for 24 hours period
    start = datetime(2023, 1, 1, 0, 0, 0)
    end = start + timedelta(days=1)

    # Empty lists to store the latitude and longitude
    latitudes = []
    longitudes = []
    acc_load = 0

    # Iterate over each second within the 24 hours period
    while start < end:
        # Get the position of the satellite
        position = predictor.get_position(start)

        # Get the latitude and longitude
        lat = position.position_llh[0]
        lon = position.position_llh[1]

        # Append the coordinates to the lists
        latitudes.append(lat)
        longitudes.append(lon)

        # Increment the time by one second
        acc_load += region_load.get_region_load(lat, lon, start.hour)
        start += timedelta(seconds=1)

    satLoad.append(acc_load)

    # Now you have lists of latitudes and longitudes for the satellite over 24 hours
    # You can print them, plot them, or save them as needed
    # for lat, lon in zip(latitudes, longitudes):
    #     print(f"{sat['name']}, {lat}, {lon}")



filename = "satLoad.txt"



with open(filename, "w") as file:
    # 向文件写入数据
    file.write(str(satLoad))