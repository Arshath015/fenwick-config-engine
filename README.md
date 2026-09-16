# fenwick-config-engine
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9%2B-success.svg)](https://www.python.org/downloads/)

A config‑driven Fenwick Tree utility that separates algorithmic logic from
runtime behaviour. Change queries and updates by editing a YAML/JSON file –
no code changes required.

## Table of Contents
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Theoretical Background](#theoretical-background)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Analysis Document](#analysis-document)
- [Testing](#testing)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [License](#license)

## Overview
The engine reads a declarative configuration describing a sequence of
updates and range‑sum queries. It builds a Fenwick tree, executes the operations
in order, and returns query results. This pattern enables non‑engineers to
experiment with different data‑sets and operation mixes without touching the
Python source.

## Tech Stack
- Python 3.9+
- Standard library (`argparse`, `json`, `pathlib`)
- Optional: `PyYAML` for YAML config support
- `pytest` for testing

## Architecture
```text
fenwick-config-engine/
├─ engine/
│  ├─ fenwick.py      # Core data structure
│  ├─ config.py       # Schema validation & loading
│  └─ runner.py       # Executes config against FenwickTree
├─ config/
│  └─ example_config.yaml
├─ examples/
│  ├─ run_demo.py     # Runnable demo, writes results/
│  └─ results/
├─ tests/
│  ├─ test_fenwick.py
│  └─ test_integration.py
├─ docs/
│  └─ analysis.md
└─ README.md
```

## Theoretical Background
The Fenwick Tree (or Binary Indexed Tree) is a data structure that supports
point updates and prefix‑sum queries in logarithmic time while using linear
space. It stores cumulative information in a tree implicitly represented by
an array; each index ``i`` is responsible for the range ``(i - lsb(i), i]``.

By leveraging the least‑significant bit operation (``i & -i``), both update
and query traverse only the relevant ancestors, yielding O(log n) complexity.
The structure is especially useful in competitive programming and real‑time
analytics where mutable cumulative data must be queried frequently.

In this engine the tree is wrapped in a class exposing ``update`` and
``range_sum`` methods. The config‑driven layer adds a thin orchestration layer
that can be extended to support additional operations (e.g., range updates)
without altering the core algorithm.

## Installation
```bash
git clone https://github.com/yourorg/fenwick-config-engine.git
cd fenwick-config-engine
pip install -r requirements.txt
```

## Usage
Run the provided demo:
```bash
python examples/run_demo.py
```
This reads ``config/example_config.yaml`` and writes query results to
``examples/results/demo_output.txt``.

To execute the engine with a custom config:
```bash
python -m engine.runner path/to/config.yaml path/to/output.txt
```

## API Reference
### class FenwickTree
- ``__init__(size: int, init_values: List[int] | None = None)``
- ``update(index: int, delta: int) -> None``
- ``prefix_sum(index: int) -> int``
- ``range_sum(left: int, right: int) -> int``

### function run_config(config_path: str | pathlib.Path) -> List[Tuple[int, int, int]]
Executes a configuration file and returns a list of query results.

## Analysis Document
See the detailed behaviour analysis in [docs/analysis.md](docs/analysis.md).

## Testing
```bash
pytest -q
```
The test suite covers unit tests for the Fenwick tree and integration tests
that validate the runner against a generated config.

## Limitations
- Only point updates are supported; range updates would require a
  Fenwick‑Tree‑of‑Fenwick‑Trees or a segment tree.
- Config validation is shallow; deeper type constraints (e.g., value ranges)
  are not enforced.

## Roadmap
- Add support for range‑add / point‑query operations.
- Introduce schema generation via ``pydantic`` for richer validation.
- Benchmark against NumPy cumulative‑sum for large static arrays.

## License
MIT License
