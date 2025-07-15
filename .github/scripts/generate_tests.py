import os
import subprocess
from openai import OpenAI               # new import

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Determine which files changed in the last commit
changed_files = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
).decode().split()

for file_path in changed_files:
    # Only generate tests for non‑test .py files
    if file_path.endswith(".py") and "test" not in file_path.lower():
        with open(file_path, "r") as f:
            code_content = f.read()

        prompt = (
            "You are an AI coding assistant. Write a pytest unit test suite for "
            "the following Python code:\n'''"
            + code_content
            + "\n'''\n"
            "Ensure the tests are thorough and cover edge cases. Only output the "
            "test code, no explanation."
        )

        response = client.chat.completions.create(      # new call path
            model="gpt-4o-mini",                       # pick whatever model you use
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        test_code = response.choices[0].message.content

        if test_code.startswith("```"):
            test_code = test_code.strip("``` \npython")

        os.makedirs("tests", exist_ok=True)
        test_file = os.path.join("tests", f"test_{os.path.basename(file_path)}")
        with open(test_file, "w") as f:
            f.write(test_code.strip() + "\n")
        print(f"Generated tests for {file_path} -> {test_file}")
