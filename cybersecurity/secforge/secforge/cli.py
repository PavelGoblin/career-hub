import argparse
import sys
from typing import NoReturn

from secforge import __version__
from secforge.constants import APP_DESC
from secforge.catalog import ToolCatalog
from secforge.installer import Installer
from secforge.utils import format_table, safe_print


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="secforge",
        description=APP_DESC,
    )
    p.add_argument(
        "-v", "--version",
        action="version",
        version=f"secforge v{__version__}",
    )

    sub = p.add_subparsers(dest="command", help="Available commands")

    list_p = sub.add_parser("list", help="List categories or tools")
    list_p.add_argument(
        "category",
        nargs="?",
        default=None,
        help="Category ID to list tools under",
    )

    search_p = sub.add_parser("search", help="Search tools by name/description/tag")
    search_p.add_argument("query", help="Search term")

    info_p = sub.add_parser("info", help="Show detailed info about a tool")
    info_p.add_argument("tool_id", help="Tool identifier")

    install_p = sub.add_parser("install", help="Install a tool")
    install_p.add_argument("tool_id", help="Tool identifier")

    return p


def echo(text: str = "") -> None:
    safe_print(text)


def cmd_list(catalog: ToolCatalog, args: argparse.Namespace) -> None:
    if args.category:
        cat = catalog.get_category(args.category)
        if not cat:
            echo(f"Unknown category: {args.category}")
            sys.exit(1)
        tools = catalog.tools_by_category(args.category)
        if not tools:
            echo(f"No tools in category '{cat.name}'")
            return
        echo(f"\n  [{cat.id}]  {cat.name} — {cat.description}\n")
        rows = [[t.id, t.name, t.description[:60]] for t in tools]
        echo(format_table(rows, header=["ID", "Name", "Description"]))
    else:
        echo("\n  Categories:\n")
        rows = [[c.id, c.name, c.description[:60]] for c in catalog.list_categories()]
        echo(format_table(rows, header=["ID", "Category", "Description"]))


def cmd_search(catalog: ToolCatalog, args: argparse.Namespace) -> None:
    results = catalog.search(args.query)
    if not results:
        echo(f"No tools found matching '{args.query}'")
        return
    echo(f"\n  Found {len(results)} tool(s) for '{args.query}':\n")
    rows = [[t.id, t.name, t.category, t.description[:50]] for t in results]
    echo(format_table(rows, header=["ID", "Name", "Category", "Description"]))


def cmd_info(catalog: ToolCatalog, args: argparse.Namespace) -> None:
    tool = catalog.get_tool(args.tool_id)
    if not tool:
        echo(f"Unknown tool: {args.tool_id}")
        sys.exit(1)
    echo(f"\n  {tool.name}\n")
    echo(f"  ID:          {tool.id}")
    echo(f"  Category:    {tool.category}")
    echo(f"  Description: {tool.description}")
    if tool.homepage:
        echo(f"  Homepage:    {tool.homepage}")
    echo(f"  Install:     {tool.install_method}")
    if tool.tags:
        echo(f"  Tags:        {', '.join(tool.tags)}")


def cmd_install(catalog: ToolCatalog, args: argparse.Namespace) -> None:
    tool = catalog.get_tool(args.tool_id)
    if not tool:
        echo(f"Unknown tool: {args.tool_id}")
        sys.exit(1)
    if not tool.install_commands:
        echo(f"No install instructions for {tool.name}")
        return
    echo(f"\n  Installing {tool.name}...\n")
    installer = Installer()
    results = installer.install(tool.install_commands)
    success = 0
    failed = 0
    for cmd_str, ok in results.items():
        status = "OK" if ok else "FAILED"
        echo(f"    [{status}] {cmd_str}")
        if ok:
            success += 1
        else:
            failed += 1
    echo(f"\n  Done: {success} succeeded, {failed} failed")


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return

    catalog = ToolCatalog()

    dispatch = {
        "list": cmd_list,
        "search": cmd_search,
        "info": cmd_info,
        "install": cmd_install,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(catalog, args)


if __name__ == "__main__":
    main()
