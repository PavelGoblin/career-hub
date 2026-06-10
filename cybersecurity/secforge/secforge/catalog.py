from typing import Any

from secforge.constants import TOOLS_CATALOG, CATEGORIES_CATALOG
from secforge.utils import load_json


class ToolEntry:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.category: str = data["category"]
        self.description: str = data.get("description", "")
        self.install_method: str = data.get("install_method", "manual")
        self.install_commands: list[str] = data.get("install_commands", [])
        self.run_command: str | None = data.get("run_command")
        self.homepage: str | None = data.get("homepage")
        self.tags: list[str] = data.get("tags", [])

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"


class CategoryEntry:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.icon: str = data.get("icon", "🔧")
        self.description: str = data.get("description", "")

    def __str__(self) -> str:
        return f"{self.icon} {self.name}"


class ToolCatalog:
    def __init__(self) -> None:
        self.tools: list[ToolEntry] = [ToolEntry(t) for t in load_json(TOOLS_CATALOG)]
        self.categories: list[CategoryEntry] = [
            CategoryEntry(c) for c in load_json(CATEGORIES_CATALOG)
        ]
        self._by_id: dict[str, ToolEntry] = {t.id: t for t in self.tools}
        self._by_category: dict[str, list[ToolEntry]] = {}
        for t in self.tools:
            self._by_category.setdefault(t.category, []).append(t)

    def get_tool(self, tool_id: str) -> ToolEntry | None:
        return self._by_id.get(tool_id)

    def get_category(self, cat_id: str) -> CategoryEntry | None:
        for c in self.categories:
            if c.id == cat_id:
                return c
        return None

    def list_categories(self) -> list[CategoryEntry]:
        return self.categories

    def tools_by_category(self, cat_id: str) -> list[ToolEntry]:
        return self._by_category.get(cat_id, [])

    def search(self, query: str) -> list[ToolEntry]:
        q = query.lower()
        results = []
        for t in self.tools:
            if any(
                q in field.lower()
                for field in [t.name, t.description, t.category, t.id]
            ):
                results.append(t)
            elif any(q in tag.lower() for tag in t.tags):
                results.append(t)
        return results
