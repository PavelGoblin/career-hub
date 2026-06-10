from pathlib import Path
from secforge.db import Catalog

BASE = Path(__file__).resolve().parent.parent / "catalog"


def test_catalog_loaded():
    c = Catalog(BASE)
    assert len(c.groups) > 0
    assert len(c.entries) > 0


def test_get_group():
    c = Catalog(BASE)
    g = c.get_group("scanning")
    assert g is not None
    assert g.label == "Network Scanning"


def test_get_entry():
    c = Catalog(BASE)
    e = c.get_entry("nmap")
    assert e is not None
    assert e.label == "Nmap"


def test_missing_group():
    c = Catalog(BASE)
    assert c.get_group("nope") is None


def test_missing_entry():
    c = Catalog(BASE)
    assert c.get_entry("nope") is None


def test_group_entries():
    c = Catalog(BASE)
    es = c.group_entries("utils")
    assert len(es) > 0
    assert all(e.group == "utils" for e in es)


def test_entry_by_category():
    c = Catalog(BASE)
    es = c.group_entries("scanning")
    found = [e for e in es if e.eid == "nmap"]
    assert len(found) == 1


def test_search():
    c = Catalog(BASE)
    r = c.search("nmap")
    assert len(r) > 0
    assert any(e.eid == "nmap" for e in r)


def test_search_no_result():
    c = Catalog(BASE)
    assert c.search("zzzdoesnotexist") == []


def test_json_valid():
    import json
    for fn in ("groups.json", "entries.json"):
        with open(BASE / fn, encoding="utf-8") as f:
            json.load(f)
