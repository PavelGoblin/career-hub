import json
from pathlib import Path
from secforge.constants import CATALOG_DIR


def test_catalog_files_exist():
    assert (CATALOG_DIR / "tools.json").exists()
    assert (CATALOG_DIR / "categories.json").exists()


def test_tools_json_valid():
    with open(CATALOG_DIR / "tools.json") as f:
        tools = json.load(f)
    assert isinstance(tools, list)
    assert len(tools) > 0
    for t in tools:
        assert "id" in t
        assert "name" in t
        assert "category" in t
        assert "description" in t


def test_categories_json_valid():
    with open(CATALOG_DIR / "categories.json", encoding="utf-8") as f:
        cats = json.load(f)
    assert isinstance(cats, list)
    assert len(cats) > 0
    for c in cats:
        assert "id" in c
        assert "name" in c


def test_tool_category_references():
    with open(CATALOG_DIR / "tools.json", encoding="utf-8") as f:
        tools = json.load(f)
    with open(CATALOG_DIR / "categories.json", encoding="utf-8") as f:
        cats = json.load(f)
    cat_ids = {c["id"] for c in cats}
    for t in tools:
        assert t["category"] in cat_ids, f"Tool {t['id']} references unknown category {t['category']}"
