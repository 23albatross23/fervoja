# railPy 🚆

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://www.python.org/)

**railPy** is an open-source Python library designed for formatting and manipulating railway communication protocol messages. 

The main goal is to provide a unified and lightweight interface to work with critical industry standards without relying on heavy external dependencies.

## 🛠 Supported Protocols

Currently, the library includes support for:

* **UNISIG**: Standard messaging for ETCS/ERTMS systems.
    - Train To Track: working
    - Track To Train: planned
    - Euroloop: planned
    - Eurobalise: planned
    - RBC to RBC: planned
* **EULYNX**: Protocol for controlling and monitoring trackside objects.
    - Planned.
* **RaSTA** (Rail Safe Transport Application): A secure transport layer for railway applications.
    - Planned.

## 🚀 Key Features

* **Zero External Dependencies**: Pure Python implementation to maximize compatibility and ease of integration.
* **Lightweight**: Optimized for environments requiring high efficiency and low overhead.
* **Single-threaded**: Deterministic execution, ideal for real-time system integration or simulators.
* **Comprehensive Testing**: Full coverage guaranteed via `pytest` and `coveragepy`.

## 📦 Installation

To install the library in development mode and enable the testing environment:

```bash
git clone [https://github.com/23albatross23/railPy.git](https://github.com/23albatross23/railPy.git)
cd railPy
pip install -e .[test]
```

## 📊 Code coverage
<!-- coverage-start -->
| Name                               |    Stmts |     Miss |   Branch |   BrPart |    Cover |
|----------------------------------- | -------: | -------: | -------: | -------: | -------: |
| railpy/foundations/abstractions.py |        3 |        0 |        0 |        0 |     100% |
| railpy/foundations/containers.py   |       51 |        0 |       16 |        0 |     100% |
| railpy/foundations/dependencies.py |       11 |        0 |        2 |        0 |     100% |
| railpy/foundations/fields.py       |       13 |        0 |        0 |        0 |     100% |
| railpy/foundations/values.py       |      101 |        0 |       22 |        0 |     100% |
| **TOTAL**                          |  **179** |    **0** |   **40** |    **0** | **100%** |

9 empty files skipped.

<!-- coverage-end -->
## 🚂 Example
TODO