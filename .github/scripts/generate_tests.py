import os
import subprocess
from pathlib import Path
from openai import OpenAI                       # ⬅ new import

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Which files changed since the previous commit on this branch?
changed_files = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
    text=True,
).split()

for file_path in changed_files:
    # Only consider Python source files, ignoring tests
    if not (file_path.endswith(".py") and "test" not in file_path.lower()):
        continue

    # Read the source code
    code = Path(file_path).read_text()

    # Determine the module's dotted import path, e.g. "mypkg.mymod"
    module_path = Path(file_path).with_suffix("").as_posix().replace("/", ".")

    # Build the prompt for the AI
    prompt = (
        f"You are an AI coding assistant. Write a **pytest** unit‑test suite "
        f"for the Python module **`{module_path}`**.  "
        f"Import the code under test with `import {module_path}` or "
        f"`from {module_path} import ...` – **never** use placeholders.\n\n"
        "Here is the source:\n'''"
        + code
        + "'''\n"
        "Ensure coverage of edge cases. Output **only** the test code."
    )

    # Request the AI to generate tests
    response = client.chat.completions.create(
        model="gpt-4o-mini",                     # use your preferred model
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    test_code = response.choices[0].message.content

    # Strip ``` fences if the model included them
    if test_code.startswith("```"):
        test_code = test_code.strip("``` \npython")

    # Ensure the tests directory exists
    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)

    # Write the generated tests to a file
    dest = tests_dir / f"test_{Path(file_path).name}"
    dest.write_text(test_code.rstrip() + "\n")

    print(f"Generated tests for {file_path} → {dest}")
