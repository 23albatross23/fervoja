# fervoja 🚆

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://www.python.org/)

**fervoja** is an open-source Python library designed for formatting and manipulating railway communication protocol messages. 

The main goal is to provide a unified and lightweight interface to work with critical industry standards without relying on heavy external dependencies.

The library is not intended for use in safety-critical execution environments, as Python does not meet the strict determinism and certification requirements (e.g., CENELEC standards) for such systems. However, it is an incredibly powerful utility for testing and simulation. Test engineers can easily serialize edge-case or intentionally invalid messages to validate the fault tolerance of real products, while developers can use it to rapidly translate and debug messages in their toolchains.

## 🛠 Supported Protocols

Currently, the library includes support for:

* **UNISIG (BSL 3.6.0)**: Standard messaging for ETCS/ERTMS systems.
    - [x] Train To Track: done 🥳
    - [ ] Track To Train: working
    - [ ] Euroloop: planned
    - [ ] Eurobalise: planned
    - [ ] RBC to RBC: planned
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
| Name                                                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |
|---------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: |
| fervoja/application\_layer/unisig/containers.py           |      154 |       16 |       28 |        5 |     88% |
| fervoja/application\_layer/unisig/interfaces.py           |        7 |        0 |        0 |        0 |    100% |
| fervoja/application\_layer/unisig/train2track/messages.py |       86 |        0 |        2 |        0 |    100% |
| fervoja/application\_layer/unisig/train2track/packets.py  |       99 |        0 |        8 |        0 |    100% |
| fervoja/application\_layer/unisig/variables/names.py      |      227 |        0 |        0 |        0 |    100% |
| fervoja/application\_layer/unisig/variables/sizes.py      |       22 |        0 |        0 |        0 |    100% |
| fervoja/application\_layer/unisig/variables/variables.py  |      182 |        0 |       30 |        0 |    100% |
| fervoja/foundations/abstractions.py                       |        3 |        0 |        0 |        0 |    100% |
| fervoja/foundations/containers.py                         |       90 |        0 |       30 |        0 |    100% |
| fervoja/foundations/dependencies.py                       |       11 |        0 |        2 |        0 |    100% |
| fervoja/foundations/fields.py                             |       14 |        0 |        0 |        0 |    100% |
| fervoja/foundations/logger.py                             |       40 |        3 |        8 |        1 |     92% |
| fervoja/foundations/singleton.py                          |       10 |        0 |        2 |        0 |    100% |
| fervoja/foundations/values.py                             |      227 |        0 |       58 |        0 |    100% |
| **TOTAL**                                                 | **1172** |   **19** |  **168** |    **6** | **98%** |

10 empty files skipped.

<!-- coverage-end -->
## 🚂 Example

Here is how to create a message, add a packet, and serialize it to hex:

```python
from fervoja.application_layer.unisig.train2track.messages import Factory as MessageFactory
from fervoja.application_layer.unisig.train2track.packets import Factory as PacketFactory

# 1. Initialize the factories
pkt_factory = PacketFactory()
msg_factory = MessageFactory()

# 2. Get the desired message and packet
pkt_0 = pkt_factory.get(0)
msg_136 = msg_factory.get(136)

# 3. Change any field
pkt_0["NID_LRBG"] = 1234
msg_136["NID_ENGINE"] = 1234

# 4. Add the packet to the message
msg_136.add_packet(pkt_0)

# 5. View the string representation
print(msg_136)

# 6. Serialize to hex for transmission
print(msg_136.encode_hex())
```
Output:
```
{
	NID_MESSAGE : 136,
	L_MESSAGE : 24,
	T_TRAIN : 0,
	NID_ENGINE : 1234,
	{
		NID_PACKET : 0,
		L_PACKET : 114,
		Q_SCALE : 0,
		NID_LRBG : 1234,
		D_LRBG : 0,
		Q_DIRLRBG : 0,
		Q_DLRBG : 0,
		L_DOUBTOVER : 0,
		L_DOUBTUNDER : 0,
		Q_LENGTH : 0,
		V_TRAIN : 0,
		Q_DIRTRAIN : 0,
		M_MODE : 0,
		M_LEVEL : 0,
	},
	PADDING : 0000
}
8806000000000001348000E4000269000000000000000000
```
