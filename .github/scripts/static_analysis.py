#!/usr/bin/env python3
"""
Run language‑appropriate static‑analysis / linting on files changed
in the last commit on this branch.

Supported languages ↔ tool mapping
  • *.py    → flake8
  • *.js    → eslint
  • *.c/*.​h → cppcheck
  • *.cpp   → cppcheck
  • *.java  → checkstyle   (uses the bundled Google style rules)
Exit‑code is **non‑zero** if *any* tool reports problems.
"""
from __future__ import annotations
import os
import subprocess
from pathlib import Path
from shutil import which

ROOT = Path(__file__).resolve().parents[2]          # repo root
CHANGED_FILES = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
    text=True,
).split()

# --------------------------------------------------------------------------- #
# Map file‑extensions to (tool‑name, command‑list)
# --------------------------------------------------------------------------- #
TOOLS: dict[str, tuple[str, list[str]]] = {
    ".py":  ("flake8",  ["flake8"]),
    ".js":  ("eslint",  ["eslint", "--max-warnings=0"]),
    ".c":   ("cppcheck", ["cppcheck", "--enable=all", "--error-exitcode=1"]),
    ".h":   ("cppcheck", ["cppcheck", "--enable=all", "--error-exitcode=1"]),
    ".cpp": ("cppcheck", ["cppcheck", "--enable=all", "--error-exitcode=1"]),
    ".java":("checkstyle",
             ["checkstyle", "-c", "/google_checks.xml"]),   # default rules
}

def ensure_tool(cmd: list[str]) -> bool:
    """Return True if the command's executable is available on PATH."""
    return which(cmd[0]) is not None

def main() -> None:
    relevant: dict[str, list[Path]] = {}
    for f in CHANGED_FILES:
        ext = Path(f).suffix
        if ext in TOOLS:
            relevant.setdefault(ext, []).append(Path(f))

    if not relevant:
        print("No files needing static analysis changed – skipping.")
        return

    failures: list[str] = []
    for ext, files in relevant.items():
        name, cmd = TOOLS[ext]
        if not ensure_tool(cmd):
            print(f"::warning:: {name} not installed – skipping {ext} files.")
            continue

        print(f"▶ Running {name} on {len(files)} file(s)…")
        for file in files:
            # Each tool processes one file at a time; easier to pinpoint errors
            proc = subprocess.run(cmd + [str(ROOT / file)])
            if proc.returncode != 0:
                failures.append(str(file))

    if failures:
        joined = ", ".join(failures)
        raise SystemExit(f"{len(failures)} file(s) failed static analysis: {joined}")

if __name__ == "__main__":
    main()
