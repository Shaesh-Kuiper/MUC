name: CI – Generate & Run Unit Tests

on:
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # 1. Check out the PR’s code
      - name: Checkout code
        uses: actions/checkout@v3

      # 2. Set up Python
      - name: Set up Python 3.x
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      # 3. Set up Java (Temurin JDK 17)
      - name: Set up Java 17
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '17'

      # 4. Install Python deps and pytest
      - name: Install Python dependencies & pytest
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest

      # 5. Generate unit tests for every changed file
      - name: Generate unit tests
        run: |
          mkdir -p tests/generated
          for file in $(git diff --name-only origin/main...HEAD); do
            python scripts/generate_tests.py README.md "$file" tests/generated
          done

      # 6a. Run Python tests
      - name: Run Python tests
        run: python -m pytest --maxfail=1 --disable-warnings -q

      # 6b. Run Java tests (Maven or Gradle if detected)
      - name: Run Java tests
        run: |
          if [ -f pom.xml ]; then
            mvn test -q
          elif [ -f build.gradle ] || [ -f build.gradle.kts ]; then
            ./gradlew test --quiet
          else
            echo "No Java build file found; skipping Java tests."
          fi
