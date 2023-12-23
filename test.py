from orbit_predictor.sources import get_predictor_from_tle_lines
from datetime import datetime, timedelta

# tle lines for the satellite
tle_lines = [
    "1 25544U 98067A   23073.93457080  .00016717  00000-0  10270-3 0  9155",
    "2 25544  51.6449  27.8199 0006469  52.1655  87.9193 15.49778524301557"
]

# Create a predictor for the satellite
predictor = get_predictor_from_tle_lines(tle_lines)

# Start time and end time for 24 hours period
start = datetime.utcnow()
end = start + timedelta(days=1)

# Empty lists to store the latitude and longitude
latitudes = []
longitudes = []
count = 0

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
    start += timedelta(seconds=1)
    count += 1

# Now you have lists of latitudes and longitudes for the satellite over 24 hours
# You can print them, plot them, or save them as needed
for lat, lon in zip(latitudes, longitudes):
    print(f"Latitude: {lat}, Longitude: {lon}")

print(count)
