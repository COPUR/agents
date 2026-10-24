#!/usr/bin/env python3
"""Build traceability.csv for a roaming-hub spec bundle and report gaps.

Reads specs/<hub>/spec.md requirement blocks ("### RH-..."), acceptance/*.feature tags
("@RH-..."), and tasks.md lines that cite requirements. Task lines may use short IDs
("AUTH-001"), ranges ("AUTH-001..004") or area wildcards ("REG-*").

    python3 build_traceability.py specs/roaming-hubs
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REQ_HEAD = re.compile(r"^### (RH-([A-Z]+)-([A-Z]+)-(\d{3}))\s*$")
META = re.compile(r"^- (source|confidence|priority|contract|verify): (.*)$")
TAG = re.compile(r"@(RH-[A-Z]+-[A-Z]+-\d{3})")
TASK = re.compile(r"^- (T-[A-Z]+-\d+) \| [^|]+\| ([^|]+)\|")
SHORT = re.compile(r"\b([A-Z]+)-(\d{3})(?:\.\.(\d{3}))?\b|\b([A-Z]+)-\*")
COLUMNS = ["requirement_id", "hub", "area", "priority", "confidence", "source_url",
           "contract", "acceptance", "task", "status"]


def parse_spec(path: Path) -> list[dict]:
    reqs, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = REQ_HEAD.match(line)
        if m:
            cur = {"requirement_id": m[1], "hub": m[2], "area": m[3]}
            reqs.append(cur)
            continue
        if cur is not None:
            mm = META.match(line)
            if mm:
                cur[mm[1]] = mm[2].strip()
            elif line.startswith("## "):
                cur = None
    return reqs


def expand(hub: str, text: str, known: set[str]) -> set[str]:
    out: set[str] = set()
    for m in SHORT.finditer(text):
        if m[4]:
            out |= {r for r in known if r.startswith(f"RH-{hub}-{m[4]}-")}
            continue
        lo = int(m[2])
        hi = int(m[3]) if m[3] else lo
        out |= {f"RH-{hub}-{m[1]}-{n:03d}" for n in range(lo, hi + 1)} & known
    return out


def main(root: Path) -> int:
    rows = []
    for spec in sorted(root.glob("*/spec.md")):
        hub_dir = spec.parent
        reqs = parse_spec(spec)
        known = {r["requirement_id"] for r in reqs}
        hub = reqs[0]["hub"] if reqs else hub_dir.name.upper()
        tests: dict[str, list[str]] = {}
        for feat in sorted(hub_dir.glob("acceptance/*.feature")):
            for tag in TAG.findall(feat.read_text(encoding="utf-8")):
                tests.setdefault(tag, [])
                if feat.name not in tests[tag]:
                    tests[tag].append(feat.name)
        tasks: dict[str, list[str]] = {}
        tasks_md = hub_dir / "tasks.md"
        if tasks_md.exists():
            for line in tasks_md.read_text(encoding="utf-8").splitlines():
                m = TASK.match(line)
                if m:
                    for rid in expand(hub, m[2], known):
                        tasks.setdefault(rid, []).append(m[1])
        for r in reqs:
            rid = r["requirement_id"]
            acc = ";".join(tests.get(rid, []))
            tsk = ";".join(tasks.get(rid, []))
            conf = r.get("confidence", "")
            status = "blocked" if conf.startswith("unknown") else ("gap" if not (acc and tsk) else "ready")
            rows.append({
                "requirement_id": rid, "hub": r["hub"], "area": r["area"],
                "priority": r.get("priority", ""), "confidence": conf,
                "source_url": r.get("source", ""), "contract": r.get("contract", ""),
                "acceptance": acc, "task": tsk, "status": status,
            })
        orphans = sorted(set(tests) - known)
        if orphans:
            print(f"{hub_dir.name}: acceptance tags with no requirement: {', '.join(orphans)}")
    out = root / "traceability.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    gaps = [r for r in rows if r["status"] == "gap"]
    print(f"wrote {out}: {len(rows)} requirements, "
          f"{sum(r['status'] == 'ready' for r in rows)} ready, {len(gaps)} gaps, "
          f"{sum(r['status'] == 'blocked' for r in rows)} blocked")
    for r in gaps:
        missing = [c for c in ("acceptance", "task") if not r[c]]
        print(f"  gap {r['requirement_id']} ({r['priority']}): no {' or '.join(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("specs/roaming-hubs")))
