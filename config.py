import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# 游戏配置：新增游戏只需在此添加一条记录
GAME_CONFIG = {
    '原神': {
        'default_path': r'D:\MIHOYO\Genshin Impact\Genshin Impact Game',
        'cache_subfolder': r'YuanShen_Data\webCaches',
        'url_pattern': r'https://webstatic\.mihoyo\.com.*?game_biz=hk4e_cn',
    },
    '崩坏:星穹铁道': {
        'default_path': r'D:\MIHOYO\Star Rail\Game',
        'cache_subfolder': r'StarRail_Data\webCaches',
        'url_pattern': r'https://webstatic\.mihoyo\.com.*?game_biz=hkrpg_cn',
    },
    '绝区零': {
        'default_path': r'D:\MIHOYO\ZenlessZoneZero Game',
        'cache_subfolder': r'ZenlessZoneZero_Data\webCaches',
        'url_pattern': r'https://[^\s]*?mihoyo\.com[^\s]*?getGachaLog[^\s]*?game_biz=nap_cn',
    },
}

# 用户配置文件路径（与可执行文件同目录）
CONFIG_FILE = Path(__file__).parent / 'user_config.json'


def get_default_paths() -> dict[str, str]:
    """返回所有游戏的默认路径。"""
    return {game: cfg['default_path'] for game, cfg in GAME_CONFIG.items()}


def load_user_paths() -> dict[str, str]:
    """加载用户自定义路径，不存在则返回默认路径。"""
    defaults = get_default_paths()
    if not CONFIG_FILE.exists():
        return defaults
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            saved = json.load(f)
        # 合并：已保存的覆盖默认值，新增游戏使用默认值
        for game in defaults:
            if game not in saved:
                saved[game] = defaults[game]
        return saved
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("读取用户配置失败，使用默认路径: %s", e)
        return defaults


def save_user_paths(paths: dict[str, str]) -> None:
    """保存用户自定义路径到配置文件。"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(paths, f, ensure_ascii=False, indent=2)
    except OSError as e:
        logger.error("保存用户配置失败: %s", e)
