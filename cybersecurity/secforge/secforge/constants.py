import os
from pathlib import Path

APP_NAME = "secforge"
APP_VERSION = "1.0.0"
APP_DESC = "A modular cybersecurity toolkit manager — inspired by Z4nzu/hackingtool"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = PROJECT_ROOT / "catalog"
TOOLS_CATALOG = CATALOG_DIR / "tools.json"
CATEGORIES_CATALOG = CATALOG_DIR / "categories.json"

HOME_DIR = Path.home()
CONFIG_DIR = HOME_DIR / ".config" / APP_NAME
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
INSTALL_DIR = CONFIG_DIR / "installed"

SUPPORTED_PKG_MANAGERS = ["apt", "yum", "dnf", "pacman", "brew", "choco"]
