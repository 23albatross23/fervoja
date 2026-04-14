# Contributing to fervoja

First off, thank you for considering contributing to this railway protocol messaging library! Community contributions are essential to ensure the reliability and safety of these protocol implementations.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Pull Request Process](#pull-request-process)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to **alvaro.pauner@outlook.es**.

## How Can I Contribute?

### Reporting Bugs
If you find a bug in a protocol parser or message formatter:
* Check the **Issue Tracker** to see if it has already been reported.
* If not, open a new issue. Include the specific protocol version, a sample hex dump of the message (if possible), and the expected vs. actual behavior.

### Suggesting Enhancements
New protocol support or feature requests are welcome! Please open an issue first to discuss the implementation details before writing any code.

## Development Setup

To set up the project locally:

1. **Fork** the repository and clone it to your machine.
  ```bash
  git clone [https://github.com/23albatross23/fervoja.git](https://github.com/23albatross23/fervoja.git)
  ```
2. Install the necessary dependencies:
  ```bash   
  cd fervoja
  pip install -e .[test]
  ```
3. Run the test suite to ensure your baseline is stable:
  ```bash
  pytest
  ```
## Coding Standards
Because this library handles critical infrastructure data formats, we maintain high standards for code quality:
* Safety & Validation: All parsers must perform strict bounds checking. Never assume a telegram length is correct without validating it against the protocol header.
* Documentation: Link every message class or function to its corresponding section in the protocol specification.
* Unit Testing: We require high coverage for new message formats. Include tests for both valid telegrams and "malformed" data to ensure the library fails gracefully.
* Linting: Follow the project's style guide. We use **Ruff** for linting and formatting, and **mypy** for static type checking. You can check your code by running:
  ```bash
  # Run linter and formatter check
  ruff check .
  ruff format --check .
  
  # Run type checker
  mypy .
  ```

## Pull Request Process
1. Create a new branch for your work: git checkout -b feat/new-protocol-feature.
2. Keep your commits small and focused. Use descriptive commit messages.
3. Ensure your branch is up to date with the main branch.
4. Submit your Pull Request with a clear description of the changes and link it to any relevant issues.
5. Wait for a maintainer to review your code. We may ask for changes to ensure protocol compliance.
---
Thank you for your contribution to the railway software ecosystem!
