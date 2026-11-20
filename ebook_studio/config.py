"""Where the books live, and per-series settings."""
import os
import tomllib
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
CACHE = PROJECT / ".cache"
CHROME = os.environ.get("CHROME_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


class ConfigError(Exception):
    pass


def library_root():
    """Folder that holds one sub-folder per series. EBOOK_LIBRARY overrides config.toml."""
    root = os.environ.get("EBOOK_LIBRARY")
    if not root:
        cfg = PROJECT / "config.toml"
        if not cfg.exists():
            raise ConfigError("config.toml not found; set `library` in it or export EBOOK_LIBRARY")
        root = tomllib.loads(cfg.read_text())["library"]
    root = Path(root).expanduser()
    if not root.is_dir():
        raise ConfigError(f"Library folder not found: {root}\nIs the external drive plugged in?")
    return root


def load_series(series):
    folder = library_root() / series
    if not folder.is_dir():
        raise ConfigError(f"Series folder not found: {folder}")
    toml = folder / "series.toml"
    if not toml.exists():
        raise ConfigError(f"Missing {toml}")
    meta = tomllib.loads(toml.read_text())
    return folder, meta


def find_stories(series_dir, selector):
    """Story folders look like 01-the-torn-letter. selector: 'all' or a prefix such as '01'."""
    dirs = sorted(d for d in series_dir.iterdir()
                  if d.is_dir() and not d.name.startswith(".") and (d / "story.md").exists())
    if selector == "all":
        return dirs
    hits = [d for d in dirs if d.name.startswith(selector)]
    if not hits:
        raise ConfigError(f"No story matching '{selector}' in {series_dir}")
    return hits
