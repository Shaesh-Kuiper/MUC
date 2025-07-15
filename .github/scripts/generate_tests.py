# scripts/generate_tests.py
"""
Generate pytest suites for every changed Python source file
(excluding existing tests) and save them under tests/.
"""

import os
import subprocess
from pathlib import Path
from openai import OpenAI                       # ⬅ new import

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Which files changed since the previous commit on this branch?
changed_files = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
    text=True,
).split()

for file_path in changed_files:
    if not (file_path.endswith(".py") and "test" not in file_path.lower()):
        continue

    code = Path(file_path).read_text()

    prompt = (
        "You are an AI coding assistant. Write a pytest unit‑test suite for "
        "the following Python code:\n'''"
        + code
        + "'''\n"
        "Ensure the tests are thorough and cover edge cases. Only output the "
        "test code, no explanation."
    )

    response = client.chat.completions.create(   # ⬅ new call path
        model="gpt-4o-mini",                     # use your preferred model
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    test_code = response.choices[0].message.content

    # Strip ``` fences if the model included them
    if test_code.startswith("```"):
        test_code = test_code.strip("``` \npython")

    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)
    dest = tests_dir / f"test_{Path(file_path).name}"
    dest.write_text(test_code.rstrip() + "\n")
    print(f"Generated tests for {file_path} → {dest}")
