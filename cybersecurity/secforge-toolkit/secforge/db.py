from __future__ import annotations

import json
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Group:
    gid: str
    label: str
    desc: str


@dataclass
class Entry:
    eid: str
    label: str
    group: str
    desc: str
    method: str = "auto"
    steps: list[str] = field(default_factory=list)
    cmd: str | None = None
    url: str | None = None
    tags: list[str] = field(default_factory=list)


def _read_json(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class Catalog:
    def __init__(self, base: Path) -> None:
        gs = _read_json(base / "groups.json")
        es = _read_json(base / "entries.json")
        self.groups: list[Group] = [Group(**g) for g in gs]
        self.entries: list[Entry] = [Entry(**e) for e in es]
        self._by_eid: dict[str, Entry] = {e.eid: e for e in self.entries}
        self._by_group: dict[str, list[Entry]] = {}
        for e in self.entries:
            self._by_group.setdefault(e.group, []).append(e)

    def get_group(self, gid: str) -> Group | None:
        for g in self.groups:
            if g.gid == gid:
                return g
        return None

    def group_entries(self, gid: str) -> list[Entry]:
        return self._by_group.get(gid, [])

    def get_entry(self, eid: str) -> Entry | None:
        return self._by_eid.get(eid)

    def search(self, term: str) -> list[Entry]:
        t = term.lower()
        return [
            e
            for e in self.entries
            if any(t in v.lower() for v in (e.eid, e.label, e.desc, e.group))
            or any(t in tag.lower() for tag in e.tags)
        ]
