# Inspiration

**SecForge** was inspired by **Z4nzu/hackingtool** (https://github.com/Z4nzu/hackingtool),
an excellent all-in-one hacking tool aggregator.

The **concept** (an interactive TUI catalog of security tools) is shared, but
the entire codebase is **written from scratch** with a data-driven architecture.

## Key Differences

| Aspect | Z4nzu/hackingtool | SecForge |
|--------|-------------------|----------|
| Tool definitions | Python subclasses for each tool | JSON catalog (data-driven) |
| Install logic | Inline shell per class | Modular Executor with step engine |
| Navigation | Arrow-key selectable menus | Numbered prompt-based menus |
| Code structure | Monolithic modules | db/runner/ux/launcher layers |
| Add new tool | Write a Python class | Add a JSON entry |
| Search | Menu-based filtering | Full-text across names, descs, tags |

Big thanks to **Z4nzu** and all hackingtool contributors for the inspiration.
