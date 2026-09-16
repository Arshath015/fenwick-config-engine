"""Engine runner that executes a config against the Fenwick tree.

The runner isolates side‑effects: it returns a list of results from query
operations while applying updates in order.
"""

from __future__ import annotations

import pathlib
from typing import List, Tuple, Dict, Any

from .fenwick import FenwickTree
from .config import load_config


def run_config(config_path: str | pathlib.Path) -> List[Tuple[int, int, int]]:
    """Execute operations defined in *config_path*.

    Returns
    -------
    List[Tuple[int, int, int]]
        Each tuple corresponds to a query operation ``(left, right, result)``
        in the order they appear in the config.
    """
    cfg = load_config(config_path)
    ft = FenwickTree(cfg["size"], cfg["initial"])
    results: List[Tuple[int, int, int]] = []

    for op in cfg["operations"]:
        if op["type"] == "update":
            ft.update(op["index"], op["delta"])
        else:  # query
            left, right = op["left"], op["right"]
            res = ft.range_sum(left, right)
            results.append((left, right, res))
    return results


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Run Fenwick engine with a config file")
    parser.add_argument("config", type=str, help="Path to YAML or JSON config")
    parser.add_argument("output", type=str, help="Path to write query results (txt)")
    args = parser.parse_args()

    results = run_config(args.config)
    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for left, right, val in results:
            line = f"query [{left}, {right}] = {val}\n"
            f.write(line)
    print(f"Wrote {len(results)} results to {out_path}")


if __name__ == "__main__":
    main()
