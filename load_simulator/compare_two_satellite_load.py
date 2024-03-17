import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.interpolate import make_interp_spline
import numpy as np

# 设置字体和图表属性
plt.rcParams["font.sans-serif"]=['simsun']  # 设置字体
plt.rcParams["axes.unicode_minus"]=False  # 解决负号乱码问题
plt.rcParams.update({'font.size': 16})
plt.dpi = 600

# Load the data from the CSV file
data = pd.read_csv('datas/satellite_permin_load.csv')

# Convert Timestamp to datetime and set as index
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

# Filter data for GUOWANG #1 and #10 on the specified date and time range (0:00 to 12:00)
gw1_data_interval = data[(data['Satellite'] == 'GW #1') &
                         (data.index.date == pd.to_datetime('2023-01-01').date()) &
                         (data.index.hour >= 0) & (data.index.hour < 12)]
gw2_data_interval = data[(data['Satellite'] == 'GW #2') &
                         (data.index.date == pd.to_datetime('2023-01-01').date()) &
                         (data.index.hour >= 0) & (data.index.hour < 12)]
gw13_data_interval = data[(data['Satellite'] == 'GW #13') &
                          (data.index.date == pd.to_datetime('2023-01-01').date()) &
                          (data.index.hour >= 0) & (data.index.hour < 12)]

# Convert the index to matplotlib dates for smooth plotting
gw1_dates = mdates.date2num(gw1_data_interval.index.to_pydatetime())
gw2_dates = mdates.date2num(gw2_data_interval.index.to_pydatetime())
gw10_dates = mdates.date2num(gw13_data_interval.index.to_pydatetime())

# Get smoothed data using spline interpolation
def smooth_data(x_data, y_data):
    # Create a spline of x and y
    spl = make_interp_spline(x_data, y_data, k=3)  # type: ignore
    x_smooth = np.linspace(x_data.min(), x_data.max(), 300)
    y_smooth = spl(x_smooth)
    return x_smooth, y_smooth

gw1_x_smooth, gw1_y_smooth = smooth_data(gw1_dates, gw1_data_interval['Load'].values)
gw2_x_smooth, gw2_y_smooth = smooth_data(gw2_dates, gw2_data_interval['Load'].values)
gw10_x_smooth, gw10_y_smooth = smooth_data(gw10_dates, gw13_data_interval['Load'].values)

# Set the formatter for the x-axis to display time in HH:MM format
hours_fmt = mdates.DateFormatter('%H:%M')

# Plot the smooth load data for both satellites within the specified interval
plt.figure(figsize=(14, 7))
plt.plot_date(gw1_x_smooth, gw1_y_smooth, '-', color='blue', label='Satellite #1')
plt.plot_date(gw2_x_smooth, gw2_y_smooth, '-', color='black', label='Satellite #2')
plt.plot_date(gw10_x_smooth, gw10_y_smooth, '-', color='green', label='Satellite #13')
plt.xlabel('时间(UTC)')
plt.ylabel('负载指数(L)')
plt.legend()
plt.grid(False)

# Apply the formatter
plt.gca().xaxis.set_major_formatter(hours_fmt)

# Rotate the x-axis labels for better readability
plt.gcf().autofmt_xdate()

plt.show()
