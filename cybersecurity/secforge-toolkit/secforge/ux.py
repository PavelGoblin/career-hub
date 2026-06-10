from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

con = Console()

BANNER = """
  ╔══════════════════════════════════════╗
  ║       ███████  ███████  ██████       ║
  ║       ██      ██      ██            ║
  ║       █████   █████   █████         ║
  ║       ██      ██      ██            ║
  ║       ██      ███████ ██            ║
  ║                                      ║
  ║    Security Toolkit Forge v2.0       ║
  ╚══════════════════════════════════════╝
"""


def show_logo() -> None:
    con.print(BANNER, style="bold cyan")


def picker(title: str, items: list[tuple[str, str]], prompt: str = "Choice") -> str | None:
    t = Table(box=box.ROUNDED, title=title, title_style="bold yellow")
    t.add_column("#", style="dim", width=4)
    t.add_column("Option", style="cyan")
    for i, (key, desc) in enumerate(items, 1):
        t.add_row(str(i), f"{key:<24} {desc}")
    con.print(t)
    ans = Prompt.ask(f"[bold yellow]{prompt}[/]", default="")
    if not ans:
        return None
    try:
        n = int(ans)
        if 1 <= n <= len(items):
            return items[n - 1][0]
        return None
    except ValueError:
        return ans.strip().lower()


def actions_picker(name: str) -> str | None:
    return picker(f"  {name}", [
        ("info", "Show details, description, install notes"),
        ("install", "Run installation steps for this tool"),
        ("launch", "Execute the tool command"),
        ("back", "Return to previous screen"),
    ], "Action")


def info(msg: str) -> None:
    con.print(f"[bold cyan]>[/] {msg}")


def ok(msg: str) -> None:
    con.print(f"[bold green]\u2713[/] {msg}")


def fail(msg: str) -> None:
    con.print(f"[bold red]\u2717[/] {msg}")


def heading(text: str) -> None:
    con.print(Panel(text, style="bold blue"))


def show_detail(eid: str, label: str, group: str, desc: str, url: str | None, tags: list[str], method: str) -> None:
    g = Table.grid(padding=(0, 2))
    g.add_column(style="bold yellow")
    g.add_column(style="white")
    g.add_row("ID:", eid)
    g.add_row("Name:", label)
    g.add_row("Group:", group)
    g.add_row("Desc:", desc)
    g.add_row("Method:", method)
    if url:
        g.add_row("URL:", url)
    if tags:
        g.add_row("Tags:", ", ".join(tags))
    con.print(Panel(g, title=f"[bold cyan]{label}[/]", border_style="cyan"))
