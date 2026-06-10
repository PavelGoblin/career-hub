import json
import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def detect_os() -> str:
    if sys.platform.startswith("linux"):
        return "linux"
    if sys.platform == "darwin":
        return "macos"
    if sys.platform == "win32":
        return "windows"
    return "unknown"


def detect_package_manager() -> str | None:
    managers = [
        ("apt", "apt-get"),
        ("dnf", "dnf"),
        ("yum", "yum"),
        ("pacman", "pacman"),
        ("brew", "brew"),
        ("choco", "choco.exe"),
    ]
    for name, bin_name in managers:
        if shutil.which(bin_name):
            return name
    return None


def run_command(cmd: list[str], capture: bool = False) -> subprocess.CompletedProcess:
    kwargs: dict[str, Any] = {}
    if capture:
        kwargs["capture_output"] = True
        kwargs["text"] = True
    return subprocess.run(cmd, **kwargs)


def format_table(rows: list[list[str]], header: list[str] | None = None) -> str:
    cols = len(rows[0]) if rows else 0
    if not cols:
        return ""
    widths = [0] * cols
    all_rows = ([header] if header else []) + rows
    for row in all_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    sep = "+" + "+".join("-" * w for w in widths) + "+"
    lines = [sep]
    if header:
        lines.append("|" + "|".join(h.center(widths[i]) for i, h in enumerate(header)) + "|")
        lines.append(sep)
    for row in rows:
        lines.append("|" + "|".join(cell.ljust(widths[i]) for i, cell in enumerate(row)) + "|")
    lines.append(sep)
    return "\n".join(lines)
