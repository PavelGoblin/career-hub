from __future__ import annotations

import sys
from pathlib import Path

from secforge import __version__
from secforge.db import Catalog
from secforge.runner import Executor, os_name, pkg_manager
from secforge.ux import (
    con, show_logo, picker, actions_picker,
    show_detail, info, ok, fail,
)

BASE = Path(__file__).resolve().parent.parent / "catalog"


def _about(cat: Catalog) -> None:
    lines = [
        f"SecForge v{__version__}",
        f"OS:        {os_name()}",
        f"Kernel:    {sys.platform}",
        f"Python:    {sys.version.split()[0]}",
        f"PM:        {pkg_manager() or 'N/A'}",
        f"Groups:    {len(cat.groups)}",
        f"Entries:   {len(cat.entries)}",
        "",
        "Concept inspired by Z4nzu/hackingtool",
        "Code built from scratch — PavelGoblin 2026",
    ]
    from rich.panel import Panel
    con.print(Panel("\n".join(lines), title="About", border_style="cyan"))


def _group_loop(cat: Catalog, exec: Executor, gid: str) -> None:
    grp = cat.get_group(gid)
    if not grp:
        fail(f"Unknown group '{gid}'")
        return
    entries = cat.group_entries(gid)
    if not entries:
        info(f"Nothing in '{grp.label}' yet")
        return
    while True:
        items = [(e.eid, e.desc) for e in entries] + [("back", "Main menu")]
        sel = picker(f"  {grp.label}", items, "Tool #")
        if sel is None or sel == "back":
            return
        _entry_loop(cat, exec, sel)


def _entry_loop(cat: Catalog, exec: Executor, eid: str) -> None:
    ent = cat.get_entry(eid)
    if not ent:
        fail(f"Unknown '{eid}'")
        return
    while True:
        act = actions_picker(ent.label)
        if act is None or act == "back":
            return
        if act == "info":
            show_detail(ent.eid, ent.label, ent.group, ent.desc, ent.url, ent.tags, ent.method)
            con.input("\n[dim]Enter[/]")
        elif act == "install":
            _install(exec, ent)
            con.input("\n[dim]Enter[/]")
        elif act == "launch":
            _launch(ent)
            con.input("\n[dim]Enter[/]")


def _install(exec: Executor, ent) -> None:
    if not ent.steps:
        info(f"No automated steps for '{ent.label}'")
        if ent.url:
            info(f"See {ent.url}")
        return
    info(f"Installing {ent.label}...")
    results = exec.run_steps(ent.steps)
    good = sum(1 for v in results.values() if v)
    bad = sum(1 for v in results.values() if not v)
    for step, success in results.items():
        (ok if success else fail)(step)
    info(f"Done: {good} ok, {bad} failed")


def _launch(ent) -> None:
    if not ent.cmd:
        info(f"No launch command for '{ent.label}'")
        return
    info(f"Starting {ent.label}...")
    code = Executor.launch(ent.cmd)
    if code != 0:
        fail(f"Exit code: {code}")


def _search_loop(cat: Catalog, exec: Executor) -> None:
    q = con.input("[bold yellow]Search:[/] ").strip()
    if not q:
        return
    results = cat.search(q)
    if not results:
        info(f"No hits for '{q}'")
        return
    info(f"{len(results)} result(s)")
    while True:
        items = [(e.eid, f"[{e.group}] {e.desc[:50]}") for e in results] + [("back", "Main menu")]
        sel = picker("  RESULTS", items, "Tool #")
        if sel is None or sel == "back":
            return
        _entry_loop(cat, exec, sel)


def main() -> None:
    try:
        cat = Catalog(BASE)
        exec = Executor()
        while True:
            show_logo()
            items = [(g.gid, g.desc) for g in cat.groups]
            items += [
                ("_search", "Search all entries"),
                ("_about", "About this tool"),
                ("_quit", "Exit"),
            ]
            sel = picker("  CATEGORIES", items, "# or command")
            if sel is None:
                continue
            if sel == "_quit":
                info("Bye.")
                break
            if sel == "_about":
                _about(cat)
                con.input("\n[dim]Enter[/]")
                continue
            if sel == "_search":
                _search_loop(cat, exec)
                continue
            _group_loop(cat, exec, sel)
    except KeyboardInterrupt:
        info("\nInterrupted.")
        sys.exit(0)
