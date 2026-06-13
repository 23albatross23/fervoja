# fervoja 🚆

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://www.python.org/)

**fervoja** is an open-source Python library designed for formatting and manipulating railway communication protocol messages. 

The main goal is to provide a unified and lightweight interface to work with critical industry standards without relying on heavy external dependencies.

## 🛠 Supported Protocols

Currently, the library includes support for:

* **UNISIG (BSL 3.6.0)**: Standard messaging for ETCS/ERTMS systems.
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
git clone [https://github.com/23albatross23/fervoja.git](https://github.com/23albatross23/fervoja.git)
cd fervoja
pip install -e .[test]
```

## 📊 Code coverage
<!-- coverage-start -->
| Name                                                     |    Stmts |     Miss |   Branch |   BrPart |   Cover |
|--------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: |
| fervoja/application\_layer/unisig/containers.py          |      137 |       82 |       26 |        0 |     35% |
| fervoja/application\_layer/unisig/interfaces.py          |        7 |        0 |        0 |        0 |    100% |
| fervoja/application\_layer/unisig/train2track/packets.py |       99 |        0 |        8 |        0 |    100% |
| fervoja/application\_layer/unisig/variables/names.py     |      227 |        0 |        0 |        0 |    100% |
| fervoja/application\_layer/unisig/variables/sizes.py     |       22 |        0 |        0 |        0 |    100% |
| fervoja/application\_layer/unisig/variables/variables.py |      182 |        0 |       30 |        0 |    100% |
| fervoja/foundations/abstractions.py                      |        3 |        0 |        0 |        0 |    100% |
| fervoja/foundations/containers.py                        |       89 |        0 |       28 |        0 |    100% |
| fervoja/foundations/dependencies.py                      |       11 |        0 |        2 |        0 |    100% |
| fervoja/foundations/fields.py                            |       14 |        0 |        0 |        0 |    100% |
| fervoja/foundations/logger.py                            |       40 |        3 |        8 |        1 |     92% |
| fervoja/foundations/singleton.py                         |       10 |        0 |        2 |        0 |    100% |
| fervoja/foundations/values.py                            |      227 |        0 |       58 |        0 |    100% |
| **TOTAL**                                                | **1068** |   **85** |  **162** |    **1** | **91%** |

10 empty files skipped.

<!-- coverage-end -->
## 🚂 Example
TODO