from __future__ import annotations

import shutil
import subprocess
import platform


def os_name() -> str:
    return platform.system().lower()


def pkg_manager() -> str | None:
    pairs = [
        ("apt-get", "apt"),
        ("dnf", "dnf"),
        ("yum", "yum"),
        ("pacman", "pacman"),
        ("brew", "brew"),
        ("choco.exe", "choco"),
    ]
    for exe, name in pairs:
        if shutil.which(exe):
            return name
    return None


def _exec(args: list[str]) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(args, capture_output=True, text=True)
    except Exception:
        return None


def _stream(args: list[str]) -> int:
    try:
        return subprocess.run(args).returncode
    except Exception:
        return -1


class Executor:
    def run_steps(self, steps: list[str]) -> dict[str, bool]:
        out: dict[str, bool] = {}
        for raw in steps:
            parts = raw.strip().split()
            if not parts:
                continue
            if shutil.which(parts[0]) is None:
                out[raw] = False
                continue
            r = _exec(parts)
            out[raw] = r is not None and r.returncode == 0
        return out

    @staticmethod
    def launch(cmd_str: str) -> int:
        return _stream(cmd_str.strip().split())

    @staticmethod
    def system_install(pkg: str) -> list[str]:
        pm = pkg_manager()
        tbl = {
            "apt": f"apt-get install -y {pkg}",
            "dnf": f"dnf install -y {pkg}",
            "yum": f"yum install -y {pkg}",
            "pacman": f"pacman -S --noconfirm {pkg}",
            "brew": f"brew install {pkg}",
            "choco": f"choco install -y {pkg}",
        }
        c = tbl.get(pm)
        return [c] if c else [f"echo 'unsupported: install {pkg} manually'"]

    @staticmethod
    def pip_install(pkg: str) -> list[str]:
        return [f"pip install {pkg}"]

    @staticmethod
    def git_clone(url: str, dst: str | None = None) -> list[str]:
        if dst:
            return [f"git clone {url} {dst}"]
        return [f"git clone {url}"]
