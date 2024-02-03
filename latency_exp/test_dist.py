from skyfield.api import load, EarthSatellite
import numpy as np

# Function to parse TLE file and return satellites
def parse_tle(file_path):
    satellites = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        satellite = EarthSatellite(line1, line2, name)
        satellites[name] = satellite
    return satellites

# Load TLE data
tle_file_path = 'gw_tle.txt'  # Update this to your TLE file path
satellites = parse_tle(tle_file_path)

# Assuming we have at least two satellites in the file
if len(satellites) >= 2:
    ts = load.timescale()
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)
    end_time = ts.utc(2023, 1, 1, 1, 0, 0)
    times = ts.linspace(start_time, end_time, 3600)  # 3600 time steps for an hour

    first_satellite = satellites['V GUOWANG #1']
    second_satellite = satellites['V GUOWANG #2']

    print(first_satellite)
    print(second_satellite)

    distances = [np.linalg.norm(first_satellite.at(time).position.km - second_satellite.at(time).position.km) for time in times]

    average_distance = np.mean(distances)
    print(f"Average distance: {average_distance} km")
