#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Fetch published hub API contracts and write pinned, eMSP-role subsets.

Only reads files the hubs publish in public GitHub repositories (raw file URLs).
It sends nothing to a hub's QA or production API. Output files carry the source URL,
retrieval date and licence so they can be committed as spec inputs.

    uv run fetch_public_contracts.py --out specs/roaming-hubs/_sources

Sources (re-check licences before redistributing):
  OICP 2.3 EMP/CPO OpenAPI  github.com/hubject/oicp-emp-2.3-api-doc  (CC BY-SA 4.0 via hubject/oicp)
  OPCP 1.0.0 component APIs github.com/hubject/opcp                  (CC BY-SA 4.0)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

RAW = "https://raw.githubusercontent.com/hubject"
OICP = {
    "emp": f"{RAW}/oicp-emp-2.3-api-doc/master/src/openapi.yaml",
    "cpo": f"{RAW}/oicp-cpo-2.3-api-doc/master/src/openapi.yaml",
}
OPCP_BASE = f"{RAW}/opcp/main/OPCP-1.0.0/reference"
OPCP = ["rcp", "pcp", "cps", "ccp", "est", "webhooks"]
# OPCP operations an eMSP / mobility operator (MO) is allowed to call, from
# OPCP-1.0.0/docs/04_authentication.md (role table).
MO_OPS = {
    "rcp": {"getRootCert", "getAllRootCerts", "get-v1-root-ctl"},
    "pcp": {"getOEMProvCert", "lookupVehicle"},
    "cps": {"createSignedContractData", "createAndForwardSignedContractData",
            "generateSignedContractData", "put-v1-cps-signContractData", "get-cps-signer"},
    "ccp": {"addSignedContractData", "deleteSignedContractData", "lookupContract",
            "getContracts", "setDefaultContract"},
    "est": {"simpleenroll", "cacerts"},
    "webhooks": None,  # all
}
HTTP = {"get", "put", "post", "delete", "patch"}
_cache: dict[str, object] = {}


class _Loader(yaml.SafeLoader):
    """SafeLoader with YAML 1.2 booleans: only true/false, so field names like On stay strings."""


_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:bool"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
_Loader.add_implicit_resolver(
    "tag:yaml.org,2002:bool", re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"), list("tTfF")
)


def fetch(url: str) -> object:
    url = url.split("#")[0]
    if url not in _cache:
        req = urllib.request.Request(url, headers={"User-Agent": "ev-roaming-hubs/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 (public https)
            text = r.read().decode("utf-8")
        _cache[url] = json.loads(text) if url.endswith(".json") else yaml.load(text, Loader=_Loader)  # noqa: S506 (safe subclass)
    return _cache[url]


def deref(node, base: str, stack: tuple[str, ...] = ()):
    """Inline $ref (relative file refs and #/ pointers). Cycles become a stub."""
    if isinstance(node, list):
        return [deref(n, base, stack) for n in node]
    if not isinstance(node, dict):
        return node
    if "$ref" in node and isinstance(node["$ref"], str):
        ref = node["$ref"]
        target = urllib.parse.urljoin(base, ref) if not ref.startswith("#") else base + ref
        if target in stack:
            return {"description": f"recursive reference to {ref.rsplit('/', 1)[-1]}"}
        doc = fetch(target)
        frag = target.split("#", 1)[1] if "#" in target else ""
        for part in [p for p in frag.split("/") if p]:
            doc = doc[part]
        merged = deref(doc, target.split("#")[0], stack + (target,))
        extra = {k: deref(v, base, stack) for k, v in node.items() if k != "$ref"}
        return {**merged, **extra} if isinstance(merged, dict) and extra else merged
    return {k: deref(v, base, stack) for k, v in node.items()}


def provenance(url: str, licence: str) -> dict:
    return {
        "x-source": url,
        "x-retrieved": dt.date.today().isoformat(),
        "x-licence": licence,
        "x-note": "Derived subset. Hub copy is authoritative; keep attribution and share-alike.",
    }


NOTE = re.compile(r"To `(?P<dir>[A-Z]+)`.*?Implementation: `(?P<impl>[A-Z]+)`", re.S)


def annotate(item: dict, role: str) -> None:
    """Lift the "To RECEIVE / Implementation: MANDATORY" note into extension fields.

    The note is written from the point of view of the document's role, so for the EMP
    file RECEIVE means the eMSP must expose the endpoint and SEND means it calls Hubject.
    """
    for method, op in item.items():
        if method in HTTP and isinstance(op, dict):
            m = NOTE.search(op.get("description", ""))
            if m:
                op[f"x-{role}-direction"] = m["dir"]
                op[f"x-{role}-implementation"] = m["impl"]


def oicp(role: str, url: str, out: Path) -> None:
    spec = fetch(url)
    paths = {}
    for path, item in spec["paths"].items():
        paths[path] = deref(item, url)
        annotate(paths[path], role)
    doc = {
        "openapi": "3.0.0",
        "info": {"title": f"OICP 2.3 {role.upper()} (pinned subset)", "version": "2.3.0",
                 **provenance(url, "CC BY-SA 4.0")},
        "servers": spec.get("servers", []),
        "paths": paths,
    }
    dest = out / f"hubject-oicp-2.3-{role}.openapi.yaml"
    dest.write_text(yaml.safe_dump(doc, sort_keys=False, width=100, allow_unicode=True))
    print(f"wrote {dest} ({len(paths)} paths)")


def opcp(name: str, out: Path) -> None:
    url = f"{OPCP_BASE}/{name}.v1.json"
    spec = fetch(url)
    allowed = MO_OPS[name]
    paths = {}
    for path, item in spec["paths"].items():
        kept = {m: o for m, o in item.items()
                if m not in HTTP or allowed is None or o.get("operationId") in allowed}
        if any(m in HTTP for m in kept):
            paths[path] = kept
    spec["paths"] = paths
    info = spec.setdefault("info", {})
    info.update(provenance(url, "CC BY-SA 4.0"))
    info["x-role-filter"] = "mobility operator (eMSP) operations only"
    dest = out / f"hubject-opcp-{name}.mo.openapi.json"
    dest.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {dest} ({len(paths)} paths)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", choices=["oicp", "opcp"])
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    failures = 0
    jobs = []
    if args.only in (None, "oicp"):
        jobs += [lambda r=r, u=u: oicp(r, u, args.out) for r, u in OICP.items()]
    if args.only in (None, "opcp"):
        jobs += [lambda n=n: opcp(n, args.out) for n in OPCP]
    for job in jobs:
        try:
            job()
        except (urllib.error.URLError, KeyError, ValueError) as exc:
            failures += 1
            print(f"FAILED: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
