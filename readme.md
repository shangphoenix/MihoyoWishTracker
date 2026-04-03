# MihoyoWishTracker

米哈游抽卡链接获取工具，支持从游戏本地缓存中自动提取抽卡记录链接，提取后自动复制到剪贴板，方便导入第三方抽卡分析工具。

## 支持的游戏

| 游戏 | 标识 |
| --- | --- |
| 原神 | hk4e_cn |
| 崩坏：星穹铁道 | hkrpg_cn |
| 绝区零 | nap_cn |

## 功能特性

- 自动读取游戏缓存文件，提取抽卡历史链接
- 支持自定义游戏安装路径，自动保存配置
- 提取成功后自动复制链接到剪贴板
- 简洁的图形界面，操作简单

## 使用方法

### 直接下载

前往 [Releases](https://github.com/shangphoenix/MihoyoWishTracker/releases) 页面下载最新的 `MihoyoWishTracker.exe`，双击运行即可。

### 从源码运行

```bash
git clone https://github.com/shangphoenix/MihoyoWishTracker.git
cd MihoyoWishTracker
pip install -r requirements.txt
python wishTracker.py
```

## 从源码构建

```bash
python -m PyInstaller --onefile --windowed --icon=MiHoYo_Logo.ico --name=MihoyoWishTracker wishTracker.py --clean --hidden-import=config --hidden-import=core
```

构建产物位于 `dist/MihoyoWishTracker.exe`。

## 项目结构

```
MihoyoWishTracker/
├── wishTracker.py      # 主程序入口，Tkinter GUI
├── config.py           # 游戏配置与用户路径管理
├── core.py             # 缓存文件解析与链接提取核心逻辑
├── MiHoYo_Logo.ico     # 应用图标
├── requirements.txt    # Python 依赖
└── user_config.json    # 用户自定义路径（运行时生成）
```

## License

[MIT](LICENSE)
