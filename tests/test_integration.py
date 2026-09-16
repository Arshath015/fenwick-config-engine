import pathlib
import json
import pytest
from engine.runner import run_config

@pytest.fixture
def tmp_config(tmp_path: pathlib.Path) -> pathlib.Path:
    cfg = {
        "size": 4,
        "initial": [0, 0, 0, 0],
        "operations": [
            {"type": "update", "index": 0, "delta": 4},
            {"type": "update", "index": 2, "delta": 7},
            {"type": "query", "left": 0, "right": 2},
            {"type": "query", "left": 1, "right": 3},
        ],
    }
    p = tmp_path / "cfg.json"
    p.write_text(json.dumps(cfg), encoding="utf-8")
    return p

def test_runner_returns_correct_results(tmp_config: pathlib.Path):
    results = run_config(tmp_config)
    assert results == [(0, 2, 11), (1, 3, 7)]
