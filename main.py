import time

from Slime_Logic import Slime
from searcher import count_slime_blocks_in_range
from utils import show_progress


def get_user_input():
    try:
        seed = int(input("请输入世界种子: "))
        center_x = int(input("请输入中心点的 X 坐标 (1-16): "))
        center_z = int(input("请输入中心点的 Z 坐标 (1-16): "))
        search_range = int(input("请输入搜寻范围 (以区块为单位): "))
        use_progress_bar = input("是否启用进度条 (y/n): ").strip().lower() == 'y'
        if not (1 <= center_x <= 16) or not (1 <= center_z <= 16):
            raise ValueError("中心点的 X 和 Z 坐标必须在 1 到 16 之间。")
        if search_range <= 0:
            raise ValueError("搜寻范围必须大于 0。")
        return seed, center_x, center_z, search_range, use_progress_bar
    except ValueError as e:
        print(f"无效输入：{e}")
        return None


def main():
    print("SlimeSeeker alpha")
    user_input = get_user_input()
    if user_input is None:
        return
    seed, center_x, center_z, search_range, use_progress_bar = user_input
    # 固定最小半径和最大半径
    min_radius = 24
    max_radius = 128
    # 创建 slime 实例
    my_slime = Slime()
    my_slime.seed = seed
    # 打开文件准备写入
    with open("slime_count.txt", "w") as file:
        start_time = time.time()  # 记录开始时间
        # 计算总迭代次数
        total_iterations = (2 * search_range + 1) ** 2
        # 遍历四个方向的位置
        for dx in range(-search_range, search_range + 1):
            for dz in range(-search_range, search_range + 1):
                current_x = center_x + dx * 16
                current_z = center_z + dz * 16
                count = count_slime_blocks_in_range(my_slime, current_x, current_z, min_radius, max_radius)
                # 将当前位置的史莱姆方块数量输出到文件
                file.write(
                    f"在 ({current_x}, {current_z}) 为中心，半径 {min_radius} 到 {max_radius} 范围内，共有 {count} 个史莱姆方块。\n")
                # 显示进度条和时间信息
                current_iteration = (dx + search_range) * (2 * search_range + 1) + (dz + search_range)
                show_progress(current_iteration, total_iterations, start_time, use_progress_bar)
        end_time = time.time()  # 记录结束时间
        total_time = end_time - start_time
        print(f"计算完成，结果已保存到 'slime_count.txt' 文件中。")
        print(f"总耗时: {total_time:.2f} 秒。")


if __name__ == "__main__":
    main()
