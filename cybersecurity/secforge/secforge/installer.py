import subprocess
from secforge.utils import detect_package_manager, run_command


class Installer:
    def __init__(self) -> None:
        self.pkg_manager = detect_package_manager()

    def install(self, commands: list[str]) -> dict[str, bool]:
        results = {}
        for cmd in commands:
            parts = cmd.strip().split()
            if not parts:
                continue
            try:
                proc = run_command(parts)
                success = proc.returncode == 0
                results[cmd] = success
            except FileNotFoundError:
                results[cmd] = False
        return results

    @staticmethod
    def system_package(package: str) -> list[str]:
        pm = detect_package_manager()
        if not pm:
            return [f"echo 'No package manager found; install {package} manually'"]
        cmd_map = {
            "apt": f"sudo apt-get install -y {package}",
            "dnf": f"sudo dnf install -y {package}",
            "yum": f"sudo yum install -y {package}",
            "pacman": f"sudo pacman -S --noconfirm {package}",
            "brew": f"brew install {package}",
            "choco": f"choco install -y {package}",
        }
        return [cmd_map.get(pm, f"echo 'unsupported: install {package} manually'")]

    @staticmethod
    def pip(package: str) -> list[str]:
        return [f"pip install {package}"]

    @staticmethod
    def git_clone(repo: str, target: str | None = None) -> list[str]:
        if target:
            return [f"git clone {repo} {target}"]
        return [f"git clone {repo}"]

    @staticmethod
    def cargo(package: str) -> list[str]:
        return [f"cargo install {package}"]
