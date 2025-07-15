#!/usr/bin/env python
"""
Generate test cases for a PR using OpenAI and commit them.

Usage:
  python generate_tests.py --pr_number 12 --repo owner/repo
"""
import argparse
import os
import textwrap
import pathlib

from github import Github
from openai import OpenAI  # v1.x client

SYSTEM_PROMPT = """\
You are an expert software engineer.
Given the diff of a pull request and the project's README,
create unit tests that thoroughly verify the new or changed behaviour.
Respond ONLY with valid code blocks for each file, using the repository's
preferred test framework and directory layout.
Provide filenames in comments like:  # file: tests/test_feature.py
Aim for at least the coverage target provided by the user.
"""


def extract_code_blocks(text: str) -> dict[str, str]:
    """
    Parse markdown-style ``` blocks with an optional '# file: ...' hint.
    Returns a mapping {filename: code}.
    """
    import re
    blocks = re.findall(r"```[^`]*?```", text, flags=re.S)
    files: dict[str, str] = {}
    for b in blocks:
        # split off the opening ``` line and the trailing ```
        header, body = b.split("\n", 1)
        body = body.rsplit("```", 1)[0]
        # look for a "# file: path" hint
        hint = re.search(r"#\s*file:\s*(.+)", body)
        if not hint:
            continue
        fname = hint.group(1).strip()
        # strip the hint line itself, leaving just the code
        code = body.split(hint.group(0), 1)[1].lstrip("\n")
        files[fname] = code
    return files


def main():
    parser = argparse.ArgumentParser(description="Generate tests for a PR")
    parser.add_argument(
        "--pr_number", required=True, type=int, help="Pull request number"
    )
    parser.add_argument(
        "--repo", required=True, help="GitHub repo in owner/repo format"
    )
    args = parser.parse_args()

    # GitHub setup
    gh = Github(os.environ["GH_TOKEN"])
    repo = gh.get_repo(args.repo)
    pr = repo.get_pull(args.pr_number)

    # Build context
    readme = repo.get_readme().decoded_content.decode()
    diff_chunks: list[str] = []
    for f in pr.get_files():
        if f.status in ("added", "modified"):
            diff_chunks.append(f.patch)
    diff_text = "\n".join(diff_chunks)
    min_cov = os.environ.get("MIN_COVERAGE", "80")

    prompt = textwrap.dedent(f"""
        README.md:
        ```markdown
        {readme}
        ```

        Pull-Request diff:
        ```diff
        {diff_text}
        ```

        Required minimum coverage: {min_cov}%
    """).strip()

    # OpenAI call (new v1.x client)
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    # Extract and write files
    code_blocks = extract_code_blocks(response.choices[0].message.content)
    for fname, code in code_blocks.items():
        out_path = pathlib.Path(fname)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(code, encoding="utf-8")
        print(f"Wrote {fname}")


if __name__ == "__main__":
    main()
