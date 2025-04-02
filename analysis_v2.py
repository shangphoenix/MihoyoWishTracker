import os
import re
import win32file
import pyperclip
import tkinter as tk
from tkinter import filedialog

# 打包命令
# pyinstaller --onefile --windowed --icon=MiHoYo_Logo.ico --name=MihoyoWishTracker analysis_v2.py --clean
# test

# 默认安装路径
DEFAULT_PATHS = {
    '原神': r'F:\MIHOYO\Genshin Impact\Genshin Impact Game',
    '崩坏:星穹铁道': r'F:\MIHOYO\Star Rail\Game',
    '绝区零': r'F:\MIHOYO\ZenlessZoneZero Game'
}

# 当前游戏路径
current_paths = DEFAULT_PATHS.copy()


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        current_paths[select_option.get()] = folder
    update_folder_label()


def reset_folder():
    game = select_option.get()
    current_paths[game] = DEFAULT_PATHS[game]
    update_folder_label()


def update_folder_label():
    game = select_option.get()
    folder_label.config(text=current_paths.get(game, '未选择'))


def get_install_path():
    return r'F:\MIHOYO'


def update_result_text():
    result = get_link()
    result_text.delete('1.0', tk.END)
    result_text.insert('1.0', result)


def get_link():
    game = select_option.get()
    folder = current_paths.get(game)

    if not folder or not os.path.exists(folder):
        return f"{game} 路径不存在，请检查设置"

    try:
        if game == '原神':
            cache_folder = os.path.join(folder, r'YuanShen_Data\webCaches')
            start_str = 'https://webstatic.mihoyo.com'
            end_str = 'game_biz=hk4e_cn'
        elif game == '崩坏:星穹铁道':
            cache_folder = os.path.join(folder, r'StarRail_Data\webCaches')
            start_str = 'https://webstatic.mihoyo.com'
            end_str = ' '
        elif game == '绝区零':
            cache_folder = os.path.join(folder, r'ZenlessZoneZero_Data\webCaches')
            start_str = 'https://public-operation-nap.mihoyo.com'
            end_str = 'game_biz=nap_cn'
        else:
            return "未选择游戏"

        version_folder = get_version(cache_folder)
        if not version_folder:
            return f"{game} 缓存文件夹版本不存在"

        data_folder = os.path.join(cache_folder, version_folder, 'Cache\Cache_Data')
        return f"{game} 抽卡链接(已复制到剪贴板): {get_string(data_folder, start_str, end_str)}"

    except Exception as e:
        return f"{game} 获取抽卡链接失败: {e}"


def get_version(folder):
    try:
        folders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
        max_version = [0, 0, 0, 0]
        max_folder = None

        for dir_name in folders:
            match = re.match(r'(\d+\.\d+\.\d+\.\d+)', dir_name)
            if match:
                version = list(map(int, match.group(1).split('.')))
                if version > max_version:
                    max_version = version
                    max_folder = dir_name

        return max_folder
    except Exception as e:
        print(f"版本解析失败: {e}")
        return None


def get_string(folder, start_str, end_str):
    try:
        data_file = os.path.join(folder, 'data_2')
        copy_file = os.path.join(folder, 'data_2_copy')

        if not os.path.exists(data_file):
            return "缓存文件 data_2 不存在"

        win32file.CopyFile(data_file, copy_file, True)

        with open(copy_file, 'r', encoding='ISO-8859-1') as file:
            content = file.read()

        matches = re.findall(f'{start_str}.*?{end_str}', content)

        os.remove(copy_file)

        if matches:
            pyperclip.copy(matches[-1])
            return matches[-1]
        else:
            return "未找到抽卡链接"

    except Exception as e:
        return f"解析缓存文件失败: {e}"


# 创建主窗口
root = tk.Tk()
root.title('原神/崩坏:星穹铁道/绝区零 抽卡链接获取工具')

# 游戏选项
options = ['原神', '崩坏:星穹铁道', '绝区零']
select_option = tk.StringVar(value='原神')

# 创建单选框
frame1 = tk.Frame(root)
frame1.pack(pady=10)

for option in options:
    radio_button = tk.Radiobutton(frame1, text=option, variable=select_option, value=option,
                                  command=update_folder_label)
    radio_button.pack(side=tk.LEFT, padx=10)

# 创建操作按钮
frame2 = tk.Frame(root)
frame2.pack(pady=10)

browse_button = tk.Button(frame2, text='选择游戏路径', command=select_folder)
browse_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(frame2, text='恢复默认路径', command=reset_folder)
reset_button.pack(side=tk.LEFT, padx=10)

process_button = tk.Button(frame2, text='获取抽卡链接', command=update_result_text)
process_button.pack(side=tk.LEFT, padx=10)

# 文件夹路径显示
frame3 = tk.Frame(root)
frame3.pack(pady=10)

folder_label = tk.Label(frame3, text=current_paths['原神'])
folder_label.pack(pady=10)

# 输出结果框
frame4 = tk.Frame(root)
frame4.pack(pady=10, fill=tk.BOTH, expand=True)

result_text = tk.Text(frame4, height=20, wrap=tk.WORD)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

result_text.insert('1.0', '如路径有误，请选择正确的游戏路径或恢复默认路径。')

# 运行主循环
root.mainloop()
