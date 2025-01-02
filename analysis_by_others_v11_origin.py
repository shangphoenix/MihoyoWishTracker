import json
import os
import re
import sys
import win32api
import win32con
import win32file
import pyperclip
import tkinter as tk
from tkinter import filedialog

config_file_path = '抽卡链接获取配置文件.json'
folder1, folder2 = '', ''


# 初始化
def initialize():
    global folder1, folder2, config_file_path
    text.insert('1.0', '若位置错误，请选择YuanShen.exe或StarRail.exe所在文件夹重新定位(将生成配置文件保存选择的位置)')
    # 如果配置文件存在，则读取配置文件内容，否则使用默认地址
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
            folder1 = config_data.get('folder1', '')
            folder2 = config_data.get('folder2', '')
    else:
        folder1 = os.path.join(getInstallPath(), r'games\Genshin Impact Game')
        folder2 = os.path.join(getInstallPath(), r'games\Star Rail Game')


# 单选框更新文本框
def selectOption():
    if option.get() == '原神':
        global folder1
        label.config(text=folder1)
    elif option.get() == '崩坏:星穹铁道':
        global folder2
        label.config(text=folder2)


# 选择游戏位置文本框和更新配置文件
def selectFolder():
    global folder1, folder2, config_file_path
    if option.get() == '原神':
        folder1 = filedialog.askdirectory()
        label.config(text=folder1)
    elif option.get() == '崩坏:星穹铁道':
        folder2 = filedialog.askdirectory()
        label.config(text=folder2)
    # 写入配置文件
    with open(config_file_path, 'w') as config_file:
        config_data = {
            "folder1": folder1,
            "folder2": folder2
        }
        json.dump(config_data, config_file, indent=4)


# 恢复默认位置更新文本框和配置文件
def resetFolder():
    global folder1, folder2, config_file_path
    if option.get() == '原神':
        folder1 = os.path.join(getInstallPath(), r'games\Genshin Impact Game')
        label.config(text=folder1)
    elif option.get() == '崩坏:星穹铁道':
        folder2 = os.path.join(getInstallPath(), r'games\Star Rail Game')
        label.config(text=folder2)
    # 如果配置文件存在，则写入配置文件
    if os.path.exists(config_file_path):
        with open(config_file_path, 'w') as config_file:
            config_data = {
                "folder1": folder1,
                "folder2": folder2
            }
            json.dump(config_data, config_file, indent=4)


# 获取抽卡链接更新文本框
def getLink():
    try:
        if option.get() == '原神':
            global folder1
            folder = os.path.join(folder1, r'YuanShen_Data\webCaches')
            folder = os.path.join(folder, getVersion(folder), r'Cache\Cache_Data')
            start_str = 'https://webstatic.mihoyo.com'
            end_str = 'game_biz=hk4e_cn'
            result = f'{option.get()}抽卡链接(已复制到剪贴板):{getString(folder, start_str, end_str)}'
            text.delete('1.0', tk.END)
            text.insert('1.0', result)
        elif option.get() == '崩坏:星穹铁道':
            global folder2
            folder = os.path.join(folder2, r'StarRail_Data\webCaches')
            folder = os.path.join(folder, getVersion(folder), r'Cache\Cache_Data')
            start_str = 'https://webstatic.mihoyo.com'
            end_str = 'plat_type=pc'
            result = f'{option.get()}抽卡链接(已复制到剪贴板):{getString(folder, start_str, end_str)}'
            text.delete('1.0', tk.END)
            text.insert('1.0', result)
    except Exception as e:
        raise e


# 注册表获取米哈游启动器安装位置
def getInstallPath():
    try:
        registry = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HYP_1_1_cn'
        # 打开注册表
        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, registry, False, win32con.KEY_READ)
        # 读取安装路径
        value = win32api.RegQueryValueEx(key, 'InstallPath')[0]
        # 关闭注册表
        win32api.RegCloseKey(key)
        return value
    except FileNotFoundError:
        text.delete('1.0', tk.END)
        text.insert('1.0',
                    '未找到米哈游启动器，请选择YuanShen.exe或StarRail.exe所在文件夹重新定位(将生成配置文件保存选择的位置)')
    except Exception as e:
        raise e


# 获取游戏目录中最新的版本号
def getVersion(folder):
    try:
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
    except FileNotFoundError:
        text.delete('1.0', tk.END)
        text.insert('1.0', '位置错误，请检查位置是否正确')
    except Exception as e:
        raise e


# 获取抽卡连接
def getString(folder, start_str, end_str):
    try:
        # 文件地址及复制地址
        copy_folder = os.path.join(folder, 'data_2')
        copy_folder_new = os.path.join(folder, 'data_2_copy')
        # 复制文件
        win32file.CopyFile(copy_folder, copy_folder_new, True)
        # 打开复制文件
        with open(copy_folder_new, 'r', encoding='ISO-8859-1') as file:
            content = file.read()
        # 查找以start_str开头，end_str结尾的字符串
        matches = re.findall(f'{start_str}.*?{end_str}', content)
        # 删除复制文件
        os.remove(copy_folder_new)
        # 将找到的字符串复制到剪贴板
        pyperclip.copy(matches[-1])
        return matches[-1]
    except Exception as e:
        raise e


# 创建主窗口
root = tk.Tk()
root.title('米哈游抽卡链接获取V1.1 by彩虹糖')
root.iconbitmap(os.path.join(sys._MEIPASS, 'image.ico'))
root.geometry('480x520')

# 创建第一行的框架用于放置单选框
frame1 = tk.Frame(root)
frame1.pack(pady=(10, 0))

# 创建单选框
options = ['原神', '崩坏:星穹铁道','绝区零']
option = tk.StringVar(value=' ')
for idx, opt in enumerate(options):
    radiobutton = tk.Radiobutton(frame1, text=opt, variable=option, value=opt, command=lambda: selectOption())
    radiobutton.pack(side=tk.LEFT, padx=10)

# 创建第二行的框架用于放置按钮
frame2 = tk.Frame(root)
frame2.pack(pady=(10, 0))

button1 = tk.Button(frame2, text='选择游戏位置', command=selectFolder)
button1.pack(side=tk.LEFT, padx=10)
button2 = tk.Button(frame2, text='恢复默认位置', command=resetFolder)
button2.pack(side=tk.LEFT, padx=10)
button3 = tk.Button(frame2, text='获取抽卡链接', command=getLink)
button3.pack(side=tk.LEFT, padx=10)

# 创建第三行的框架用于放置文件夹路径标签
frame3 = tk.Frame(root)
frame3.pack(pady=(10, 0))

label = tk.Label(frame3, text='未选择游戏')
label.pack()

# 创建第四行的框架用于放置结果Text组件
frame4 = tk.Frame(root)
frame4.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

text = tk.Text(frame4, wrap=tk.WORD)
text.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, padx=10)

# 初始化
initialize()

# 运行主循环
root.mainloop()
