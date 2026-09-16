"""Configuration handling for the Fenwick engine.

The engine reads a JSON or YAML file that describes a sequence of
operations (updates and queries). The schema is deliberately simple so
that non‑technical users can tweak behavior without touching code.
"""

from __future__ import annotations

import json
import pathlib
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

CONFIG_SCHEMA = {
    "size": int,
    "initial": list,
    "operations": list,
}


def load_config(path: str | pathlib.Path) -> Dict[str, Any]:
    """Load and validate a configuration file.

    Supported formats: .json, .yaml, .yml
    The function raises ``ValueError`` if required keys are missing or have
    incorrect types.
    """
    path = pathlib.Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Config file {path} does not exist")

    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise ImportError("PyYAML is required to read YAML configs")
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
    elif path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    else:
        raise ValueError("Unsupported config file extension")

    # Basic schema validation
    for key, typ in CONFIG_SCHEMA.items():
        if key not in raw:
            raise ValueError(f"Missing required config key: {key}")
        if not isinstance(raw[key], typ):
            raise ValueError(f"Config key '{key}' must be of type {typ.__name__}")

    # Validate operations structure
    for op in raw["operations"]:
        if not isinstance(op, dict) or "type" not in op:
            raise ValueError("Each operation must be a dict with a 'type' field")
        if op["type"] == "update":
            if not all(k in op for k in ("index", "delta")):
                raise ValueError("Update operation requires 'index' and 'delta'")
        elif op["type"] == "query":
            if not all(k in op for k in ("left", "right")):
                raise ValueError("Query operation requires 'left' and 'right'")
        else:
            raise ValueError(f"Unsupported operation type: {op['type']}")

    return raw
