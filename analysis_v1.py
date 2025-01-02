import os
import re
import win32api
import win32con
import win32file
import pyperclip
import tkinter as tk
from tkinter import filedialog

folder1 = r'F:\MIHOYO\Genshin Impact\Genshin Impact Game'
folder2 = r'F:\MIHOYO\Star Rail\Game'
folder3 = r'F:\MIHOYO\ZenlessZoneZero Game'


def select_folder():
    folder = filedialog.askdirectory()
    if select_option.get() == '原神':
        global folder1
        folder1 = folder
    elif select_option.get() == '崩坏:星穹铁道':
        global folder2
        folder2 = folder
    elif select_option.get() == '绝区零':
        global folder3
        folder3 = folder
    update_folder_label()


def reset_folder():
    if select_option.get() == '原神':
        global folder1
        folder1 = os.path.join(getInstallPath(), r'Genshin Impact\Genshin Impact Game')
    elif select_option.get() == '崩坏:星穹铁道':
        global folder2
        folder2 = os.path.join(getInstallPath(), r'games\Star Rail Game')
    elif select_option.get() == '绝区零':
        global folder3
        folder3 = os.path.join(getInstallPath(), r'games\ZenlessZoneZero Game')
    update_folder_label()


def update_folder_label():
    if select_option.get() == '原神':
        global folder1
        if folder1 == '':
            folder1 = os.path.join(getInstallPath(), r'games\Genshin Impact Game')
        folder_label.config(text=folder1)
    elif select_option.get() == '崩坏:星穹铁道':
        global folder2
        if folder2 == '':
            folder2 = os.path.join(getInstallPath(), r'games\Star Rail Game')
        folder_label.config(text=folder2)
    elif select_option.get() == '绝区零':
        global folder3
        if folder3 == '':
            folder3 = os.path.join(getInstallPath(), r'games\ZenlessZoneZero Game')
        folder_label.config(text=folder3)


def getInstallPath():
    return 'F:\\MIHOYO'


def update_result_text():
    result = getLink()
    result_text.delete('1.0', tk.END)
    result_text.insert('1.0', result)


def getLink():
    global folder1, folder2, folder3
    if select_option.get() == '原神':
        folder = os.path.join(folder1, r'YuanShen_Data\webCaches')
        folder = os.path.join(folder, getVersion(folder), r'Cache\Cache_Data')
        print(folder)
        start_str = 'https://webstatic.mihoyo.com'
        end_str = 'game_biz=hk4e_cn'
    elif select_option.get() == '崩坏:星穹铁道':
        folder = os.path.join(folder2, r'StarRail_Data\webCaches')
        folder = os.path.join(folder, getVersion(folder), r'Cache\Cache_Data')
        print(folder)
        start_str = 'https://webstatic.mihoyo.com'
        end_str = 'plat_type=pc'
    elif select_option.get() == '绝区零':
        folder = os.path.join(folder3, r'ZenlessZoneZero_Data\webCaches')
        folder = os.path.join(folder, getVersion(folder), r'Cache\Cache_Data')
        print(folder)
        start_str = 'https://public-operation-nap.mihoyo.com'
        end_str = 'game_biz=nap_cn'
    else:
        return f'未选择'
    return f'{select_option.get()}抽卡链接(已复制到剪贴板):{getString(folder, start_str, end_str)}'


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
    print(max_folder)
    return max_folder


def getString(folder, start_str, end_str):
    # 复制地址
    copy_folder = os.path.join(folder, 'data_2')
    copy_folder_new = os.path.join(folder, 'data_2_copy')
    # 复制文件
    win32file.CopyFile(copy_folder, copy_folder_new, True)
    # 打开复制后的文件
    with open(copy_folder_new, 'r', encoding='ISO-8859-1') as file:
        content = file.read()
    # 查找以start_str开头，end_str结尾的字符串
    matches = re.findall(f'{start_str}.*?{end_str}', content)
    # 删除文件
    os.remove(copy_folder_new)
    # 将找到的字符串复制到剪贴板
    pyperclip.copy(matches[-1])
    print(matches[-1])
    return matches[-1]


# 创建主窗口
root = tk.Tk()
root.title('原神/崩坏:星穹铁道抽卡链接获取V1.0 by彩虹糖')

options = ['原神', '崩坏:星穹铁道', '绝区零']
select_option = tk.StringVar(value=' ')

# 创建第一行的框架用于放置单选框
frame1 = tk.Frame(root)
frame1.pack(pady=10)

# 创建单选框
for idx, option in enumerate(options):
    radio_button = tk.Radiobutton(frame1, text=option, variable=select_option, value=option,
                                  command=lambda opt=option: update_folder_label())
    radio_button.pack(side=tk.LEFT, padx=(0, 10))

# 创建第二行的框架用于放置按钮
frame2 = tk.Frame(root)
frame2.pack(pady=10)

browse_button = tk.Button(frame2, text='选择游戏位置', command=select_folder)
browse_button.pack(side=tk.LEFT, padx=(0, 10))
browse_button = tk.Button(frame2, text='恢复默认位置', command=reset_folder)
browse_button.pack(side=tk.LEFT, padx=(0, 10))
process_button = tk.Button(frame2, text='获取抽卡链接', command=update_result_text)
process_button.pack(side=tk.LEFT, padx=(0, 10))

# 创建第三行的框架用于放置文件夹路径标签
frame3 = tk.Frame(root)
frame3.pack(pady=10)

folder_label = tk.Label(frame3, text='未选择')
folder_label.pack(pady=10)

# 创建第四行的框架用于放置结果Text组件
frame4 = tk.Frame(root)
frame4.pack(pady=10, fill=tk.BOTH, expand=True)

result_text = tk.Text(frame4, height=20, wrap=tk.WORD)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_text.insert('1.0', '如若位置错误，请选择YuanShen.exe或StarRail.exe所在的文件夹进行重新定位!')

# 运行主循环
root.mainloop()
