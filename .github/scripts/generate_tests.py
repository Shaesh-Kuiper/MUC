import sys
# from your_module import generate_tests  # <- your function
import argparse
import os
import sys

try:
    # Use the new OpenAI client interface for openai>=1.0.0
    from openai import OpenAI
except ImportError:
    sys.exit(
        """Missing dependency `openai`. Install with `pip install openai`.\n"
        "Ensure you're on openai>=1.0.0 or pin to openai==0.28.* if you prefer the legacy API."""
    )


def read_file(path: str) -> str:
    """Read and return the contents of a text file."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_tests(readme_path: str, file_path: str, model: str = 'gpt-4.1-mini') -> str:
    """
    Read the README and updated file, merge them into a prompt,
    and call the OpenAI API to generate unit tests.
    Returns the generated test code as a string.
    """
    readme_content = read_file(readme_path)
    file_content = read_file(file_path)

    # prompt = (
    #     "You are an expert developer who writes thorough unit tests.\n"
    #     "Below is the repository README followed by the content of an updated file. "
    #     "Write a complete set of compatible pytest tests for the updated file. "
    #     "If the file is not testable, output a placeholder test that always passes.\nreturn the test alone and nothing extra"
    #     f"\n\nRepository README:\n{readme_content}\n\n"
    #     f"Updated File ({os.path.basename(file_path)}):\n{file_content}\n"
    # )

    prompt = (
        "You are an expert developer who writes thorough unit tests.\n"
        "Below is the repository README followed by the content of an updated file that is to be uploade to github. "
        "Write a complete set of compatible unit tests for the updated file.\nNOTE if its not a type of file that u cannot write a test, then give an arbitary test that will always pass (like in css edits)\nu must output thr test alone not a single extra word, like in the format used for in CICD pipeline \n\n "
        f"Repository README:\n{readme_content}\n\n"
        f"Updated File Content ({os.path.basename(file_path)}):\n{file_content}\n"
    )

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise EnvironmentError("Environment variable OPENAI_API_KEY is not set.")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for generating unit tests."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()







readme_path = sys.argv[1]
source_path = sys.argv[2]
out_dir     = sys.argv[3]

tests_code = generate_tests(readme_path, source_path)
# e.g. write to tests/generated/test_<module>.py
module_name = source_path.rstrip('.py').replace('/', '_')
with open(f"{out_dir}/test_{module_name}.py", 'w') as f:
    f.write(tests_code)
