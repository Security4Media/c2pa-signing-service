#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"!\[[^\]]+\]\(([^)]+)\)|\[[^\]]+\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:")
SKIP_PARTS = {"archive"}


def iter_markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(
                sorted(
                    candidate
                    for candidate in path.rglob("*.md")
                    if not any(part in SKIP_PARTS for part in candidate.parts)
                )
            )
        elif path.suffix == ".md":
            files.append(path)
    return files


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]
    return target


def normalize_relative_path(raw_path: str) -> str:
    return os.path.normpath(raw_path)


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for match in LINK_RE.finditer(line):
            target = normalize_target(match.group(1) or match.group(2) or "")
            if not target or target.startswith("#") or target.startswith(SKIP_PREFIXES):
                continue

            target_path = target.split("#", 1)[0]
            if not target_path:
                continue

            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                errors.append(f"{path}:{line_no}: missing link target {target_path}")
                continue

            expected_relative = os.path.relpath(resolved, start=path.parent.resolve())
            authored_relative = normalize_relative_path(target_path)
            expected_relative = normalize_relative_path(expected_relative)
            if authored_relative != expected_relative:
                errors.append(
                    f"{path}:{line_no}: link target should be relative to {path.parent}: "
                    f"{target_path} -> {expected_relative}"
                )
    return errors


def main() -> int:
    raw_paths = [Path(arg) for arg in sys.argv[1:]]
    if not raw_paths:
        print("usage: check_internal_links.py <markdown-file-or-dir> [...]", file=sys.stderr)
        return 2

    errors: list[str] = []
    for file_path in iter_markdown_files(raw_paths):
        errors.extend(validate_file(file_path))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("internal markdown links: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
