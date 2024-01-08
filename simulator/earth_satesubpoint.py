from skyfield.api import Topos, load
from skyfield.sgp4lib import EarthSatellite
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Define the TLE lines
tle_line1 = '1 00001U 23029BR  23354.90575231  .00001103  00000-0  33518-4 0  9998'
tle_line2 = '2 00001 85.00000   0.7036 0003481 299.7327   0.3331 14.94839113  1770'

# Create a satellite object using the TLE lines
satellite = EarthSatellite(tle_line1, tle_line2, 'MY SATELLITE', load.timescale())

# Timescale and time range for the pass
times = load.timescale().utc(2023, 12, 20, range(24))  # Adjust the date as necessary

# Compute satellite positions
geocentric = satellite.at(times)

# Get latitude and longitude
subpoint = geocentric.subpoint()
latitude = subpoint.latitude.degrees
longitude = subpoint.longitude.degrees

# Set up the map
plt.figure(figsize=(12, 6))
m = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c')
m.drawcoastlines()
m.drawparallels(np.arange(-90., 91., 30.), labels=[1,0,0,0])
m.drawmeridians(np.arange(-180., 181., 60.), labels=[0,0,0,1])

# Convert latitude and longitude to x and y coordinates
x, y = m(longitude, latitude)

# Plot the ground track
m.plot(x, y, 'o-', markersize=5, linewidth=1, color='red', label='MY SATELLITE')

# Add legend and title
plt.legend(loc='upper left')
plt.title('Ground Track of MY SATELLITE on 2023-12-20')

# Show the plot
plt.show()
