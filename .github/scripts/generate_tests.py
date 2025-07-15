# scripts/generate_tests.py
import os, subprocess, openai

# Load OpenAI API key from environment (set via GitHub Secret)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Determine which files have changed in the last commit (for push workflows)
changed_files = subprocess.check_output(
    ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
).decode().split()

for file_path in changed_files:
    # Only generate tests for Python source files (skip if file is a test or non-py)
    if file_path.endswith(".py") and "test" not in file_path.lower():
        with open(file_path, "r") as f:
            code_content = f.read()
        # Construct prompt for OpenAI (instruct to only output test code)
        prompt = (
            "You are an AI coding assistant. Write a pytest unit test suite for the following Python code:\n"
            + "'''\n" + code_content + "\n'''\n"
            + "Ensure the tests are thorough and cover edge cases. Only output the test code, no explanation."
        )
        # Call OpenAI API (using a ChatCompletion or Completion endpoint)
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",  # or "gpt-3.5-turbo" if GPT-4 is unavailable
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        test_code = response['choices'][0]['message']['content']
        # Remove markdown fences if present (the AI might include ```python ... ``` in response)
        if test_code.startswith("```"):
            test_code = test_code.strip("``` \npython")
        # Save the generated test code to a new file under tests/ directory
        test_dir = "tests"
        os.makedirs(test_dir, exist_ok=True)
        test_file_path = os.path.join(test_dir, f"test_{os.path.basename(file_path)}")
        with open(test_file_path, "w") as f:
            f.write(test_code.strip() + "\n")
        print(f"Generated tests for {file_path} -> {test_file_path}")
