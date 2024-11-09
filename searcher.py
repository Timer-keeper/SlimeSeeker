from utils import euclidean_distance


def is_valid_slime_block(slime_obj, block_x, block_z):
    # 检查一个方块是否可以生成史莱姆
    return slime_obj.check(slime_obj.seed, block_x, block_z)


def count_slime_blocks_in_range(slime_obj, center_x, center_z, min_radius, max_radius):
    if not isinstance(center_x, int) or not isinstance(center_z, int):
        raise TypeError("center_x and center_z must be integers")
    if not isinstance(min_radius, int) or not isinstance(max_radius, int):
        raise TypeError("min_radius and max_radius must be integers")
    if min_radius < 0 or max_radius < 0 or min_radius >= max_radius:
        raise ValueError("min_radius and max_radius must be non-negative and min_radius < max_radius")
    # 计算指定范围内的史莱姆方块数量
    count = 0
    # 计算 chunk 范围
    start_chunk_x = (center_x - max_radius) // 16
    end_chunk_x = (center_x + max_radius + 15) // 16
    start_chunk_z = (center_z - max_radius) // 16
    end_chunk_z = (center_z + max_radius + 15) // 16
    distances = {}
    for chunk_x in range(start_chunk_x, end_chunk_x):
        for chunk_z in range(start_chunk_z, end_chunk_z):
            # 计算 chunk 内部的边界
            start_block_x = max(chunk_x * 16, center_x - max_radius)
            end_block_x = min((chunk_x + 1) * 16, center_x + max_radius + 1)
            start_block_z = max(chunk_z * 16, center_z - max_radius)
            end_block_z = min((chunk_z + 1) * 16, center_z + max_radius + 1)
            for block_x in range(start_block_x, end_block_x):
                for block_z in range(start_block_z, end_block_z):
                    key = (block_x, block_z)
                    if key not in distances:
                        distances[key] = euclidean_distance(center_x, center_z, block_x, block_z)
                    distance = distances[key]
                    if min_radius <= distance < max_radius and is_valid_slime_block(slime_obj, block_x, block_z):
                        count += 1
    return count
