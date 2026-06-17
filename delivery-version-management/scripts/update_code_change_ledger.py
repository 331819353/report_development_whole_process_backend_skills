#!/usr/bin/env python3
"""Create/read/append per-code-file change ledgers.

The default ledger path is:
<code-file-directory>/__change_logs__/<code-file-name>.changes.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import os
import re
from pathlib import Path
from textwrap import dedent


CODE_EXTENSIONS = {
    ".css",
    ".go",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".less",
    ".mjs",
    ".py",
    ".scss",
    ".sql",
    ".ts",
    ".tsx",
    ".vue",
    ".yaml",
    ".yml",
}


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def default_version() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().strftime("v%Y%m%d-%H%M%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_count(text: str) -> int:
    if not text:
        return 0
    return len(text.splitlines())


def resolve_code_path(root: Path, file_arg: str) -> Path:
    code_path = Path(file_arg).expanduser()
    if not code_path.is_absolute():
        code_path = root / code_path
    code_path = code_path.resolve()

    if not code_path.exists():
        raise SystemExit(f"[code-ledger] code file not found: {code_path}")
    if not code_path.is_file():
        raise SystemExit(f"[code-ledger] not a file: {code_path}")
    if code_path.suffix and code_path.suffix not in CODE_EXTENSIONS:
        print(f"[code-ledger] warning: {code_path.suffix} is not in the default code extension list")
    return code_path


def ledger_path_for(code_path: Path) -> Path:
    return code_path.parent / "__change_logs__" / f"{code_path.name}.changes.md"


def snapshot_dir_for(code_path: Path) -> Path:
    return ledger_path_for(code_path).parent / ".snapshots"


def before_snapshot_paths(code_path: Path) -> tuple[Path, Path]:
    snapshot_dir = snapshot_dir_for(code_path)
    stem = f"{code_path.name}.before"
    return snapshot_dir / f"{stem}.txt", snapshot_dir / f"{stem}.json"


def patch_dir_for(code_path: Path) -> Path:
    return ledger_path_for(code_path).parent / "patches"


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def create_ledger_if_missing(code_path: Path, root: Path, purpose: str, actor: str) -> Path:
    ledger_path = ledger_path_for(code_path)
    if ledger_path.exists():
        return ledger_path

    source_text = read_text(code_path)
    code_rel = rel(code_path, root)
    ledger_rel = rel(ledger_path, root)
    timestamp = now_stamp()
    purpose_value = purpose or "TBD: describe what this file owns before the next handoff."
    actor_value = actor or "codex"

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(
        dedent(
            f"""\
            # Code Change Ledger: {code_rel}

            - Code file: `{code_rel}`
            - Ledger file: `{ledger_rel}`
            - Purpose: {purpose_value}
            - Primary features: TBD
            - Last reviewed before edit: {timestamp} / baseline / {actor_value}
            - Ledger rule: read this file before editing the code file; append a version entry after every scoped change.

            ## Functional Inventory

            | Feature ID | Feature / Behavior | Main Code Range | Inputs | Outputs | Notes |
            | --- | --- | --- | --- | --- | --- |
            | FEAT-TBD | TBD | TBD | TBD | TBD | Created from current file baseline. |

            ## Version Entries

            ### baseline - {timestamp}

            - Change ID: baseline
            - Actor: {actor_value}
            - Change type: baseline
            - Summary: Initial ledger created from existing file before a code change.
            - Modified functionality: none
            - Code ranges: full file, {line_count(source_text)} lines
            - Modified content: none
            - Affected contracts: none
            - Verification: sha256 `{file_sha256(code_path)}`
            - Rollback note: use VCS history or previous release bundle if available.
            - Related files: none
            - Follow-up: fill purpose, feature inventory, and stable code ranges during the next functional change.
            """
        ),
        encoding="utf-8",
    )
    return ledger_path


def write_before_snapshot(code_path: Path, root: Path, actor: str) -> tuple[Path, Path]:
    source_text = read_text(code_path)
    snapshot_path, meta_path = before_snapshot_paths(code_path)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(source_text, encoding="utf-8")
    meta_path.write_text(
        json.dumps(
            {
                "codeFile": rel(code_path, root),
                "capturedAt": now_stamp(),
                "actor": actor or "codex",
                "lines": line_count(source_text),
                "sha256": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return snapshot_path, meta_path


def read_before_snapshot(code_path: Path, root: Path, allow_missing: bool) -> tuple[str, dict[str, object]]:
    snapshot_path, meta_path = before_snapshot_paths(code_path)

    if not snapshot_path.exists() or not meta_path.exists():
        if allow_missing:
            return "", {
                "codeFile": rel(code_path, root),
                "capturedAt": "missing",
                "lines": 0,
                "sha256": "missing",
            }
        raise SystemExit(
            "[code-ledger] missing pre-edit snapshot; run --stage before before editing "
            "or pass --allow-missing-before with an exact external VCS/release reference"
        )

    return read_text(snapshot_path), json.loads(read_text(meta_path))


def build_unified_diff(before_text: str, after_text: str, code_rel: str) -> str:
    diff_lines = difflib.unified_diff(
        before_text.splitlines(),
        after_text.splitlines(),
        fromfile=f"a/{code_rel}",
        tofile=f"b/{code_rel}",
        lineterm="",
    )
    diff_text = "\n".join(diff_lines)
    return f"{diff_text}\n" if diff_text else ""


def infer_ranges_from_diff(diff_text: str) -> str:
    ranges = []
    for match in re.finditer(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", diff_text):
        old_start = int(match.group(1))
        old_count = int(match.group(2) or "1")
        new_start = int(match.group(3))
        new_count = int(match.group(4) or "1")
        old_end = old_start + max(old_count, 1) - 1
        new_end = new_start + max(new_count, 1) - 1
        ranges.append(f"L{new_start}-L{new_end} (was L{old_start}-L{old_end})")
    return ", ".join(ranges)


def diff_evidence(
    args: argparse.Namespace,
    code_path: Path,
    root: Path,
    before_text: str,
    after_text: str,
    version: str,
) -> tuple[str, str]:
    if before_text == after_text:
        return "No text diff: before snapshot and after file are identical.", "none"

    code_rel = rel(code_path, root)
    diff_text = build_unified_diff(before_text, after_text, code_rel)
    diff_lines = diff_text.splitlines()

    if len(diff_lines) <= args.max_inline_diff_lines:
        evidence = f"inline unified diff:\n\n```diff\n{diff_text.rstrip()}\n```"
        return evidence, infer_ranges_from_diff(diff_text)

    patch_dir = patch_dir_for(code_path)
    patch_dir.mkdir(parents=True, exist_ok=True)
    safe_version = re.sub(r"[^A-Za-z0-9_.-]+", "-", version).strip("-") or "change"
    patch_path = patch_dir / f"{safe_version}-{code_path.name}.diff"
    patch_path.write_text(diff_text, encoding="utf-8")
    evidence = (
        f"sidecar patch `{rel(patch_path, root)}` "
        f"({len(diff_lines)} diff lines, sha256 `{file_sha256(patch_path)}`)"
    )
    return evidence, infer_ranges_from_diff(diff_text)


def format_markdown_field(value: str) -> str:
    if "\n" not in value:
        return value
    return "\n" + "\n".join(f"  {line}" if line else "" for line in value.splitlines())


def append_after_entry(args: argparse.Namespace, code_path: Path, root: Path, ledger_path: Path) -> None:
    summary = args.summary.strip()
    if not summary:
        raise SystemExit("[code-ledger] --summary is required for --stage after")

    source_text = read_text(code_path)
    before_text, before_meta = read_before_snapshot(code_path, root, args.allow_missing_before)
    version = args.version.strip() or default_version()
    timestamp = now_stamp()
    change_evidence, inferred_ranges = diff_evidence(args, code_path, root, before_text, source_text, version)
    code_ranges = args.ranges or inferred_ranges or "TBD: add stable anchors or line ranges after formatting"
    entry = f"""

### {version} - {timestamp}

- Change ID: {args.change_id or "ad-hoc"}
- Actor: {args.actor or "codex"}
- Change type: {args.change_type}
- Summary: {summary}
- Modified functionality: {args.features or "TBD"}
- Code ranges: {code_ranges}
- Modified content: {args.modified_content or "TBD"}
- Affected contracts: {args.affected_contracts or "none"}
- Verification: {args.verification or "not run: verification not provided"}
- Rollback note: {args.rollback or "revert this file and the related files listed below together if needed"}
- Related files: {args.related_files or "none"}
- Before snapshot: {before_meta.get("lines", "unknown")} lines, sha256 `{before_meta.get("sha256", "unknown")}`, captured `{before_meta.get("capturedAt", "unknown")}`
- After snapshot: {line_count(source_text)} lines, sha256 `{file_sha256(code_path)}`
- Change evidence: {format_markdown_field(change_evidence)}
- Follow-up: {args.follow_up or "none"}
"""
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def main() -> None:
    parser = argparse.ArgumentParser(description="Maintain per-code-file change ledger markdown.")
    parser.add_argument("--file", required=True, help="Code file path, relative to --root or absolute.")
    parser.add_argument("--root", default=os.getcwd(), help="Project root. Defaults to current directory.")
    parser.add_argument("--stage", choices=("before", "after"), required=True)
    parser.add_argument("--purpose", default="")
    parser.add_argument("--version", default="")
    parser.add_argument("--change-id", default="")
    parser.add_argument("--actor", default="codex")
    parser.add_argument("--change-type", default="update")
    parser.add_argument("--summary", default="")
    parser.add_argument("--features", default="")
    parser.add_argument("--ranges", default="")
    parser.add_argument("--modified-content", default="")
    parser.add_argument("--affected-contracts", default="")
    parser.add_argument("--verification", default="")
    parser.add_argument("--rollback", default="")
    parser.add_argument("--related-files", default="")
    parser.add_argument("--follow-up", default="")
    parser.add_argument("--allow-missing-before", action="store_true")
    parser.add_argument("--max-inline-diff-lines", type=int, default=400)
    parser.add_argument("--show-lines", type=int, default=160, help="Lines to print during --stage before.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    code_path = resolve_code_path(root, args.file)
    ledger_path = create_ledger_if_missing(code_path, root, args.purpose, args.actor)

    if args.stage == "before":
        snapshot_path, meta_path = write_before_snapshot(code_path, root, args.actor)
        ledger_text = read_text(ledger_path)
        lines = ledger_text.splitlines()
        preview = "\n".join(lines[-args.show_lines :])
        print(f"[code-ledger] read before edit: {rel(ledger_path, root)}")
        print(f"[code-ledger] captured before snapshot: {rel(snapshot_path, root)}")
        print(f"[code-ledger] captured before metadata: {rel(meta_path, root)}")
        print(preview)
        return

    append_after_entry(args, code_path, root, ledger_path)
    print(f"[code-ledger] appended after edit: {rel(ledger_path, root)}")


if __name__ == "__main__":
    main()
