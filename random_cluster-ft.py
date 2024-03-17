import json
import random

# 定义节点数量和群集数量
num_satellites = 480
num_clusters = 30

# 创建卫星名字列表
satellites = [f"Guowang #{i+1}" for i in range(num_satellites)]

# 随机分配卫星到不同的群集
random.shuffle(satellites)
clusters = {f"cluster-{i+1}": {"name": f"cluster-{i+1}", "satellites": []} for i in range(num_clusters)}
for i, sat in enumerate(satellites):
    cluster_name = f"cluster-{i % num_clusters + 1}"
    clusters[cluster_name]["satellites"].append({"name": sat, "satelliteId": sat})

# 构造JSON数据结构
json_data = {
    "clusters": clusters
}

# 将数据转换为JSON格式
json_output = json.dumps(json_data, indent=2)

# 保存为json文件
with open("random_cluster.json", "w") as f:
    f.write(json_output)