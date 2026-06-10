from secforge.catalog import ToolCatalog


def test_catalog_loads():
    cat = ToolCatalog()
    assert len(cat.tools) > 0
    assert len(cat.categories) > 0


def test_get_tool():
    cat = ToolCatalog()
    t = cat.get_tool("nmap")
    assert t is not None
    assert t.name == "Nmap"
    assert t.id == "nmap"


def test_get_unknown_tool():
    cat = ToolCatalog()
    assert cat.get_tool("nonexistent") is None


def test_tools_by_category():
    cat = ToolCatalog()
    tools = cat.tools_by_category("scanning")
    assert len(tools) > 0
    for t in tools:
        assert t.category == "scanning"


def test_search():
    cat = ToolCatalog()
    results = cat.search("nmap")
    assert len(results) > 0
    assert any(t.id == "nmap" for t in results)


def test_search_no_results():
    cat = ToolCatalog()
    results = cat.search("xyznonexistent12345")
    assert len(results) == 0


def test_list_categories():
    cat = ToolCatalog()
    cats = cat.list_categories()
    assert len(cats) > 0
    assert any(c.id == "scanning" for c in cats)
