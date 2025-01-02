import os
import re


def getVersion(folder):
    # 初始化一个空列表来存储文件夹名称
    folders = []
    # 遍历指定路径下的所有文件夹
    for DIR in os.listdir(folder):
        # 检查是否为文件夹
        if os.path.isdir(os.path.join(folder, DIR)):
            # 将文件夹名称添加到列表中
            folders.append(DIR)
    # 初始化最大版本号为最小可能值的列表
    max_version = [0, 0, 0, 0]
    max_folder = None
    # 找到最大版本号
    for folder in folders:
        # 使用正则表达式匹配文件夹名中的数字
        match = re.match(r'(\d+\.\d+\.\d+\.\d+)', folder)
        if match:
            # 解析版本号
            version = list(map(int, match.group(1).split('.')))
            # 比较版本号
            if version > max_version:
                max_version = version
                max_folder = folder
    return max_folder

print(getVersion(r'F:\MIHOYO\ZenlessZoneZero Game\ZenlessZoneZero_Data\webCaches'))