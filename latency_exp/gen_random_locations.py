import numpy as np
import random


def generate_and_save_coords(file_path):
    coords = []
    for _ in range(3):  # 生成10个随机坐标
        latitude = random.uniform(-90, 90)
        longitude = random.uniform(-180, 180)
        coords.append((latitude, longitude))

    np.save(file_path, np.array(coords))


coords_file_path = 'random_coords.npy'
generate_and_save_coords(coords_file_path)
print(f"Generated coordinates have been saved to {coords_file_path}.")