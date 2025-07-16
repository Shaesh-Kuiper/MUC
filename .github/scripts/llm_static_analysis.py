#!/usr/bin/env python3
"""
Ask an OpenAI chat model which static‑analysis command to run for every file
touched in the last commit, then run those commands.

The model must reply with **valid JSON** in the form:

{
  "<relative/path/to/file>": ["<executable>", "arg1", ...],
  ...
}

Only these tools are allowed:
  flake8          (Python)
  eslint          (JS/TS)
  cppcheck        (C/C++/Headers)
  checkstyle      (Java, Google rules)
Any file whose command array is empty will be skipped.

Exit‑status is non‑zero if any command returns non‑zero.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # set by the workflow

REPO_ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def changed_files() -> list[str]:
    out = subprocess.check_output(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"], text=True
    )
    return [line.strip() for line in out.splitlines() if line.strip()]


def ask_llm(files: list[str]) -> dict[str, list[str]]:
    """Return {file: cmd_list} chosen by the LLM."""
    system_prompt = (
        "You are a CI assistant helping to run static‑analysis.\n"
        "Choose exactly one appropriate tool for each file from the list below "
        "and respond with STRICT JSON (no markdown) mapping each path to the "
        "full command array **without** the file path itself:\n\n"
        " • flake8          ← Python (*.py)\n"
        " • eslint --max-warnings=0 ← JS/TS (*.js, *.ts)\n"
        " • cppcheck --enable=all --error-exitcode=1 ← C/C++ (*.c, *.h, *.cpp)\n"
        " • checkstyle -c /google_checks.xml ← Java (*.java)\n\n"
        "If no tool applies, map the file to an empty list []."
    )
    user_prompt = "Files changed:\n" + "\n".join(files)

    resp = openai.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    content = resp.choices[0].message.content
    try:
        data: dict[str, list[str]] = json.loads(content)
    except json.JSONDecodeError as err:
        raise RuntimeError(f"LLM did not return valid JSON:\n{content}") from err
    return data


def run_commands(mapping: dict[str, list[str]]) -> list[str]:
    failures: list[str] = []

    for rel_path, cmd_list in mapping.items():
        if not cmd_list:
            continue  # explicitly skipped
        full_cmd = cmd_list + [rel_path]  # file path is final argument
        print("▶", *full_cmd)
        proc = subprocess.run(full_cmd, cwd=REPO_ROOT)
        if proc.returncode != 0:
            failures.append(rel_path)
    return failures


def main() -> None:
    files = changed_files()
    if not files:
        print("No files changed — skipping static analysis.")
        return

    mapping = ask_llm(files)
    failures = run_commands(mapping)

    if failures:
        joined = ", ".join(failures)
        raise SystemExit(f"{len(failures)} file(s) failed static analysis: {joined}")


if __name__ == "__main__":
    main()
