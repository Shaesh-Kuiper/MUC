#!/usr/bin/env python
"""
Generate test cases for a PR using OpenAI and commit them.

Usage:
  python generate_tests.py --pr_number 12 --repo owner/repo
"""
import argparse
import os
import subprocess
import textwrap
import json
import pathlib
from github import Github
import openai

SYSTEM_PROMPT = """\
You are an expert software engineer.
Given the diff of a pull request and the project's README,
create unit tests that thoroughly verify the new or changed behaviour.
Respond ONLY with valid code blocks for each file, using the repository's
preferred test framework and directory layout.
Provide filenames in comments like:  # file: tests/test_feature.py
Aim for at least the coverage target provided by the user.
"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pr_number", required=True, type=int)
    p.add_argument("--repo", required=True)
    args = p.parse_args()

    gh = Github(os.environ["GH_TOKEN"])
    repo = gh.get_repo(args.repo)
    pr = repo.get_pull(args.pr_number)

    # -------- 1. Build context --------
    readme = repo.get_readme().decoded_content.decode()
    diff_chunks = []
    for f in pr.get_files():
        if f.status in ("added", "modified"):
            diff_chunks.append(f.patch)

    # Join diff chunks outside of f-string to avoid backslashes in expressions
    diff_text = "\n".join(diff_chunks)
    min_cov = os.environ.get("MIN_COVERAGE", "80")

    prompt = textwrap.dedent("""
    README.md:
    ```markdown
    {}
    ```

    Pull-Request diff:
    ```diff
    {}
    ```

    Required minimum coverage: {}%
    """.format(readme, diff_text, min_cov)).strip()

    # -------- 2. Call OpenAI --------
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    code_blocks = extract_code_blocks(response.choices[0].message.content)

    # -------- 3. Write files --------
    for fname, code in code_blocks.items():
        out_path = pathlib.Path(fname)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(code, encoding="utf-8")


def extract_code_blocks(text):
    """
    Parse markdown-style ``` blocks with an optional '# file: ...' hint.
    Returns {filename: source}
    """
    import re
    blocks = re.findall(r"```[^`]*?```", text, flags=re.S)
    files = {}
    for b in blocks:
        header, body = b.split("\n", 1)
        body = body.rsplit("```", 1)[0]  # trim closing
        hint = re.search(r"#\s*file:\s*(.+)", body)
        if hint:
            fname = hint.group(1).strip()
            code = body.split(hint.group(0), 1)[1].lstrip("\n")
            files[fname] = code
    return files


if __name__ == "__main__":
    main()
