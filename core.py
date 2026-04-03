import re
import shutil
import logging
import tempfile
from pathlib import Path

from config import GAME_CONFIG

logger = logging.getLogger(__name__)


def get_latest_version(cache_folder: Path) -> str | None:
    """在缓存目录中找到最新版本号的子目录。"""
    if not cache_folder.is_dir():
        return None

    max_version = [0, 0, 0, 0]
    max_folder = None

    for entry in cache_folder.iterdir():
        if not entry.is_dir():
            continue
        match = re.match(r'(\d+\.\d+\.\d+\.\d+)', entry.name)
        if match:
            version = list(map(int, match.group(1).split('.')))
            if version > max_version:
                max_version = version
                max_folder = entry.name

    return max_folder


def parse_cache_file(data_file: Path, url_pattern: str) -> str | None:
    """从缓存文件中提取抽卡链接，返回最后一个匹配的 URL。"""
    if not data_file.exists():
        return None

    # 使用系统临时目录，避免污染游戏缓存目录
    with tempfile.NamedTemporaryFile(delete=False, suffix='_data_2') as tmp:
        tmp_path = Path(tmp.name)

    try:
        shutil.copy2(data_file, tmp_path)
        with open(tmp_path, 'r', encoding='ISO-8859-1') as f:
            content = f.read()

        matches = re.findall(url_pattern, content)
        return matches[-1] if matches else None
    finally:
        tmp_path.unlink(missing_ok=True)


def extract_wish_link(game: str, game_path: str) -> str:
    """
    提取指定游戏的抽卡链接。

    Returns:
        成功时返回抽卡链接 URL，失败时返回错误描述字符串（以"错误:"开头）。
    """
    if game not in GAME_CONFIG:
        return "错误: 未知的游戏选项"

    cfg = GAME_CONFIG[game]
    folder = Path(game_path)

    if not folder.exists():
        return f"错误: {game} 路径不存在，请检查设置"

    cache_folder = folder / cfg['cache_subfolder']
    if not cache_folder.exists():
        return f"错误: 缓存目录不存在: {cache_folder}"

    version = get_latest_version(cache_folder)
    if not version:
        return f"错误: {game} 缓存文件夹中未找到版本目录"

    data_file = cache_folder / version / 'Cache' / 'Cache_Data' / 'data_2'
    if not data_file.exists():
        return f"错误: 缓存文件 data_2 不存在"

    try:
        link = parse_cache_file(data_file, cfg['url_pattern'])
    except PermissionError:
        return f"错误: 缓存文件被占用，请关闭游戏后重试"
    except OSError as e:
        logger.exception("读取缓存文件失败")
        return f"错误: 读取缓存文件失败: {e}"

    if link is None:
        return "错误: 未找到抽卡链接，请先在游戏内打开抽卡历史记录"

    return link
