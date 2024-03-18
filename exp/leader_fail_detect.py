import numpy as np

def calculate_latency(node1, node2, hops_delay):
    x1 = node1 % 16
    if x1 == 0:
        x1 = 16
    y1 = node1 // 30
    x2 = node2 % 16
    if x2 == 0:
        x2 = 16
    y2 = node2 // 30

    col = min(abs(x1 - x2), 16 - abs(x1 - x2))
    row = min(abs(y1 - y2), 30 - abs(y1 - y2))

    return (col + row) * hops_delay

if __name__ == '__main__':
    hops_delay = 4

    # Generate 10 arrays each with 30 numbers ranging from 1 to 480
    arrays = [np.random.randint(1, 481, 30) for _ in range(10)]

    total_delay = 0

    # Calculate the average latency for each array
    for idx, array in enumerate(arrays):
        # 计算 array 里所有节点两两之间延迟的平均
        delay = 0
        count = 0
        for i in array:
            for j in array:
                if i != j:
                    count += 1
                    delay += calculate_latency(i, j, hops_delay)

        total_delay += (delay / count)

    print(total_delay / len(arrays))


