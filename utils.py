import math
import time
from tqdm import tqdm


def euclidean_distance(x1, z1, x2, z2):
    # 计算两点之间的欧几里得距离
    return math.sqrt((x1 - x2) ** 2 + (z1 - z2) ** 2)


def show_progress(current_iteration, total_iterations, start_time, use_progress_bar):
    # 显示进度条和时间信息
    if use_progress_bar:
        current_time = time.time()
        elapsed_time = current_time - start_time
        progress = current_iteration / total_iterations
        if progress > 0:
            time_per_step = elapsed_time / progress
            remaining_time = time_per_step * (1 - progress)
        else:
            remaining_time = float('inf')
        tqdm.write(f"进度: {progress * 100:.2f}% | 已用时间: {elapsed_time:.2f}s | 剩余时间: {remaining_time:.2f}s")
