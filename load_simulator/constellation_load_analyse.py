import pandas as pd
import matplotlib.pyplot as plt

# 设置字体和图表属性
plt.rcParams["font.sans-serif"]=['simsun']  # 设置字体
plt.rcParams["axes.unicode_minus"]=False  # 解决负号乱码问题
plt.rcParams.update({'font.size': 16})
plt.dpi = 600

# Load the dataset
df = pd.read_csv('datas/satellite_permin_load.csv')

# Filter the data for the specified timestamp
df_filtered = df[df['Timestamp'] == '2023-01-01 03:00:00+00:00']

# Extract numerical IDs for satellites
df_filtered['Satellite_ID'] = df_filtered['Satellite'].str.extract('(\d+)').astype(int)

plt.figure(figsize=(12, 7))
# Plot using the numerical ID instead of the full satellite name
plt.scatter(df_filtered['Satellite_ID'], df_filtered['Load'], marker='x', color='blue')
plt.xlabel('卫星编号')
plt.ylabel('负载指数（L）')

# Adjust x-axis to potentially display every 50th ID, based on the range of your data
max_id = df_filtered['Satellite_ID'].max()
plt.xticks(range(0, max_id + 1, 50))  # Adjust the range and step as needed

plt.grid(False)  # Turned grid on for better readability, adjust as needed
plt.tight_layout()
plt.show()
