#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List


TYPE_PATTERNS = [
    ("requirement", re.compile(r"需求|requirement|prd", re.I)),
    ("prototype", re.compile(r"原型|prototype|demo|mock", re.I)),
    ("data-model", re.compile(r"数据模型|data[-_ ]?model|model", re.I)),
    ("api", re.compile(r"api|接口|swagger|openapi", re.I)),
    ("backend", re.compile(r"backend|后端|service|server", re.I)),
    ("frontend", re.compile(r"frontend|前端|页面|ui", re.I)),
    ("test", re.compile(r"test|测试|qa|evidence|defect", re.I)),
    ("release", re.compile(r"release|上线|发布|版本", re.I)),
]

VERSION_PATTERN = re.compile(r"(?:^|[-_ ])(v\d+(?:\.\d+){0,2})(?:$|[-_ .])", re.I)


def infer_type(path: Path) -> str:
    text = str(path)
    for artifact_type, pattern in TYPE_PATTERNS:
        if pattern.search(text):
            return artifact_type
    return "other"


def infer_version(path: Path, default_version: str) -> str:
    match = VERSION_PATTERN.search(path.name)
    if match:
        return match.group(1).lower()
    return default_version


def collect_files(root: Path, default_version: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    ignored_dirs = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.name.startswith(".DS_Store"):
            continue
        artifact_type = infer_type(path)
        version = infer_version(path, default_version)
        rows.append(
            {
                "artifact_id": f"{artifact_type}-{len(rows) + 1:03d}",
                "type": artifact_type,
                "name": path.name,
                "version": version,
                "path": str(path),
                "status": "draft",
            }
        )
    return rows


def render_markdown(rows: List[Dict[str, str]], release_version: str) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Delivery Index",
        "",
        f"- Generated at: {generated_at}",
        f"- Release version: {release_version}",
        "",
        "## Artifact Index",
        "",
        "| Artifact ID | Type | Name | Version | Path/source | Owner | Status | Upstream version | Downstream version | Change IDs | Evidence | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {artifact_id} | {type} | {name} | {version} | {path} |  | {status} |  |  |  |  |  |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Version Chain",
            "",
            "| Release version | Requirement | Prototype | Data model | API docs | Backend | Frontend | Test matrix/report | Automation | Status |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            f"| {release_version} |  |  |  |  |  |  |  |  | draft |",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a first-pass delivery artifact index.")
    parser.add_argument("root", help="Artifact root directory to scan.")
    parser.add_argument("--out", default="DELIVERY_INDEX.md", help="Output Markdown file.")
    parser.add_argument("--version", default="release-v1.0", help="Release bundle version.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(root)
    rows = collect_files(root, args.version)
    out = Path(args.out).expanduser().resolve()
    out.write_text(render_markdown(rows, args.version), encoding="utf-8")
    print(f"Wrote {out} with {len(rows)} artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
