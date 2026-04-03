import logging
import threading
import tkinter as tk
from tkinter import filedialog

import pyperclip

from config import GAME_CONFIG, load_user_paths, save_user_paths
from core import extract_wish_link

# 打包命令
# pyinstaller --onefile --windowed --icon=MiHoYo_Logo.ico --name=MihoyoWishTracker wishTracker.py --clean --hidden-import=config --hidden-import=core
# 不依赖PATH的打包命令
# python -m PyInstaller --onefile --windowed --icon=MiHoYo_Logo.ico --name=MihoyoWishTracker wishTracker.py --clean --hidden-import=config --hidden-import=core

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('wishTracker.log', encoding='utf-8'),
    ],
)
logger = logging.getLogger(__name__)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('原神/崩坏:星穹铁道/绝区零 抽卡链接获取工具')
        self.root.minsize(500, 300)

        self.games = list(GAME_CONFIG.keys())
        self.current_paths = load_user_paths()
        self.select_option = tk.StringVar(value=self.games[0])

        self._build_ui()

    def _build_ui(self):
        # 游戏选择
        frame1 = tk.Frame(self.root)
        frame1.pack(pady=10)
        for game in self.games:
            rb = tk.Radiobutton(
                frame1, text=game,
                variable=self.select_option, value=game,
                command=self._update_folder_label,
            )
            rb.pack(side=tk.LEFT, padx=10)

        # 操作按钮
        frame2 = tk.Frame(self.root)
        frame2.pack(pady=10)

        tk.Button(frame2, text='选择游戏路径', command=self._select_folder).pack(side=tk.LEFT, padx=10)
        tk.Button(frame2, text='恢复默认路径', command=self._reset_folder).pack(side=tk.LEFT, padx=10)
        self.fetch_button = tk.Button(frame2, text='获取抽卡链接', command=self._fetch_link)
        self.fetch_button.pack(side=tk.LEFT, padx=10)

        # 路径显示
        frame3 = tk.Frame(self.root)
        frame3.pack(pady=10)
        self.folder_label = tk.Label(frame3, text=self.current_paths.get(self.games[0], '未选择'))
        self.folder_label.pack(pady=10)

        # 结果输出
        frame4 = tk.Frame(self.root)
        frame4.pack(pady=10, fill=tk.BOTH, expand=True)
        self.result_text = tk.Text(frame4, height=20, wrap=tk.WORD)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.result_text.insert('1.0', '如路径有误，请选择正确的游戏路径或恢复默认路径。')

    def _current_game(self) -> str:
        return self.select_option.get()

    def _select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            game = self._current_game()
            self.current_paths[game] = folder
            save_user_paths(self.current_paths)
            self._update_folder_label()

    def _reset_folder(self):
        game = self._current_game()
        self.current_paths[game] = GAME_CONFIG[game]['default_path']
        save_user_paths(self.current_paths)
        self._update_folder_label()

    def _update_folder_label(self):
        game = self._current_game()
        self.folder_label.config(text=self.current_paths.get(game, '未选择'))

    def _fetch_link(self):
        """在后台线程中提取抽卡链接，避免 UI 假死。"""
        game = self._current_game()
        folder = self.current_paths.get(game, '')

        self.fetch_button.config(state=tk.DISABLED, text='获取中...')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', f'正在获取 {game} 的抽卡链接，请稍候...')

        def _worker():
            result = extract_wish_link(game, folder)
            self.root.after(0, lambda: self._on_fetch_done(game, result))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_fetch_done(self, game: str, result: str):
        self.fetch_button.config(state=tk.NORMAL, text='获取抽卡链接')
        self.result_text.delete('1.0', tk.END)

        if result.startswith('错误:'):
            self.result_text.insert('1.0', f'{game}: {result}')
            logger.warning("%s: %s", game, result)
        else:
            pyperclip.copy(result)
            self.result_text.insert('1.0', f'{game} 抽卡链接(已复制到剪贴板):\n{result}')
            logger.info("%s: 成功获取抽卡链接", game)


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()
