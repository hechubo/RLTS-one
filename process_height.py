import os
import numpy as np

def should_delete_file(file_path):
    """ 检查文件中的高度数据是否连续10个没有变化 """
    data = np.loadtxt(file_path)
    altitudes = data[:, 3]  # 高度数据在第四列

    # 检查是否有10个连续相同的高度值
    count = 1
    for i in range(1, len(altitudes)):
        if altitudes[i] == altitudes[i - 1]:
            count += 1
            if count == 10:
                return True
        else:
            count = 1
    return False

def main(directory):
    """ 遍历指定目录下的所有文件，并删除符合条件的文件 """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if should_delete_file(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

# 使用示例
main("/root/RLTS-one/TrajData/routes_clean")  # 将这里的路径替换为你的文件夹路径