from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from region_load import get_region_load
import random
import argparse

# 遗传算法参数
num_individuals = 100  # 种群大小
num_generations = 100  # 代数
mutation_rate = 0.05   # 变异率
num_groups = 0        # 分组总数


# 读取并解析TLE数据
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


# 初始化种群
def generate_initial_population(size, num_satellites):
    population = []
    for _ in range(size):
        # 生成 0 ~ num_groups - 1 的随机序列
        individual = np.arange(num_satellites)
        # 随机打乱这个序列，以确保个体的多样性
        np.random.shuffle(individual)
        individual %= num_groups  # 确保平均分配到各个组
        # 将处理后的个体（卫星分组）添加到 population 列表中
        population.append(individual)
    return np.array(population)


# 适应度函数
def calculate_fitness(individual, average_loads):
    satellite_names = [f'GW #{i + 1}' for i in range(480)]
    satellite_groups = {}

    for satellite_name, group in zip(satellite_names, individual):
        satellite_groups[satellite_name] = f'Group {group + 1}'

    # 计算各分组的平均负载
    group_loads = {}
    for satellite, group in satellite_groups.items():
        if group not in group_loads:
            group_loads[group] = []
        if satellite in average_loads:
            group_loads[group].append(average_loads[satellite])

    # 计算各分组平均负载的标准差
    group_average_loads = [np.mean(loads) for loads in group_loads.values() if loads]
    std_dev = np.std(group_average_loads)

    return std_dev


# 交叉操作
def crossover(parent1, parent2):
    # 确保交叉后每个组中的卫星数量不变
    child1, child2 = parent1.copy(), parent2.copy()
    crossover_point = random.randint(0, len(parent1) - 1)
    for i in range(crossover_point, len(parent1)):
        # 在 child1 中查找与 parent2[i] 相同值的位置并交换
        idx1 = np.where(child1 == parent2[i])[0][0]
        child1[i], child1[idx1] = child1[idx1], child1[i]
        # 在 child2 中查找与 parent1[i] 相同值的位置并交换
        idx2 = np.where(child2 == parent1[i])[0][0]
        child2[i], child2[idx2] = child2[idx2], child2[i]
    return child1, child2


# 变异操作
def mutation(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            swap_with = random.randint(0, len(individual) - 1)
            individual[i], individual[swap_with] = individual[swap_with], individual[i]


# 遗传算法主函数
def genetic_algorithm(average_loads):
    num_satellites = len(average_loads)
    population = generate_initial_population(num_individuals, num_satellites)
    best_fitness = float('-inf')  # 初始化为负无穷，确保任何适应度值都比它大
    best_individual = None  # 用于存储遇到的最佳个体

    for generation in range(num_generations):
        fitnesses = np.array([calculate_fitness(individual, average_loads) for individual in population])

        # 检查并更新最佳适应度值及其对应的个体
        current_best_fitness = np.max(fitnesses)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[np.argmax(fitnesses)].copy()  # 复制当前最佳个体

        # 选择
        selected_indices = np.argsort(fitnesses)[-num_individuals:]  # 选择适应度最高的个体
        population = population[selected_indices]

        # 交叉和变异
        next_generation = []
        for i in range(0, len(population), 2):
            parent1, parent2 = population[i], population[min(i + 1, len(population) - 1)]
            child1, child2 = crossover(parent1, parent2)
            mutation(child1)
            mutation(child2)
            next_generation.extend([child1, child2])
        population = np.array(next_generation)[:num_individuals]

        # 可以打印当前代的最佳适应度值等信息
        # print(f'Generation {generation + 1}:')
        # print(f'Best fitness: {best_fitness}')  # 打印整个过程中遇到的最佳适应度
        # print(f'Best grouping: {best_individual}')  # 显示整个过程中遇到的最佳个体

    # 返回整个运行过程中的最佳个体
    print(f'Global Best fitness: {best_fitness}')
    return best_individual

# 定义函数来计算指定时刻的一小时内每个卫星的平均负载并分组
def calculate_genetics_loads(satellite_load_data, start_time):
    # 确定结束时间
    end_time = start_time + timedelta(minutes=10)

    # 筛选出在指定时间范围内的数据
    filtered_data = satellite_load_data[(satellite_load_data['Timestamp'] >= start_time) &
                         (satellite_load_data['Timestamp'] < end_time)]

    # 计算每个卫星的平均负载
    average_loads = filtered_data.groupby('Satellite')['Load'].mean()


    # 使用遗传算法进行分组
    best_grouping = genetic_algorithm(average_loads)

    satellite_names = [f'GW #{i+1}' for i in range(480)]

    # print(best_grouping)

    satellite_groups = {}

    # 根据遗传算法的结果分配卫星到分组
    for satellite_name, group in zip(satellite_names, best_grouping):
        satellite_groups[satellite_name] = f'Group {group + 1}'


    # 计算各分组的平均负载
    group_loads = {}
    for satellite, group in satellite_groups.items():
        if group not in group_loads:
            group_loads[group] = []
        if satellite in average_loads:
            group_loads[group].append(average_loads[satellite])

    # 计算各分组平均负载的标准差
    group_average_loads = [np.mean(loads) for loads in group_loads.values() if loads]
    std_dev = np.std(group_average_loads)

    # print(f'fitness: {calculate_fitness(best_grouping, average_loads)}')
    # print(f'genetics_groups: {std_dev}')

    return satellite_groups


# 计算星下点坐标及负载
def calculate_subpoints(satellites, start_time, duration_hours, satellite_load_data):
    end_time = start_time + timedelta(hours=duration_hours)
    data = []
    current_time = start_time
    hour_counter = 0
    satellite_groups = {}

    while current_time.utc_datetime() < end_time.utc_datetime():
        print(current_time.utc_datetime())

        # 每小时重新分组
        if hour_counter % 10 == 0:
            print("重新分组")
            satellite_groups = calculate_genetics_loads(satellite_load_data, current_time.utc_datetime())

        group_loads = {f'Group {i + 1}': [] for i in range(num_groups)}  # 初始化每组的负载列表
        for satellite in satellites:
            geocentric = satellite.at(current_time)
            subpoint = geocentric.subpoint()
            # 计算负载情况
            region_load = get_region_load(subpoint.latitude.degrees, subpoint.longitude.degrees, current_time.utc_datetime().hour)
            group = satellite_groups[satellite.name]
            group_loads[group].append(region_load)

        # print(group_loads)
        mean_loads = [np.mean(loads) for loads in group_loads.values() if loads]
        # print(f'mean_loads: {mean_loads}')
        if mean_loads:
            # 计算这些均值的标准差
            overall_std = np.std(mean_loads)
            print(f'overall_std: {overall_std}')
            data.append({
                'Timestamp': current_time.utc_datetime(),
                'Overall Load STD': overall_std,
            })

        current_time += timedelta(minutes=2)
        hour_counter += 2
    return pd.DataFrame(data)

# 示例分组
# satellite_groups = {
#     'Satellite1': 'Group1',
#     'Satellite2': 'Group1',
#     'Satellite3': 'Group2',
#     # ... 其他卫星和它们的分组
# }

# grouped by orbit

# Call the function and get the groups
tle_file_path = 'guowang_tle_suit.txt'

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('nums_of_groups', type=int, help='Number of groups to divide satellites into')
    # Parse arguments
    args = parser.parse_args()

    # Use the nums_of_groups from the parsed arguments
    num_groups = args.nums_of_groups

    # TLE File path
    tle_file_path = 'guowang_tle_suit.txt'

    # 加载时间模块
    ts = load.timescale()
    satellites = load_tle(tle_file_path)
    start_time = ts.utc(2023, 1, 1, 0, 0, 0)  # Start time set to Jan 1, 2023

    all_data = []

    satellite_load_data_file_path = 'datas/satellite_permin_load.csv'
    satellite_load_data = pd.read_csv(satellite_load_data_file_path)
    satellite_load_data['Timestamp'] = pd.to_datetime(satellite_load_data['Timestamp'])

    df = calculate_subpoints(satellites, start_time, 12, satellite_load_data)

    output_filename = f'datas/dynamic_genetics_{num_groups}_experiments_avg_load_12H.csv'
    df.to_csv(output_filename, index=False)
    print(f'计算完成，平均结果已保存到 {output_filename}')



