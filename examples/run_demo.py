"""Demo script that runs the engine with the example config.

The script writes query results to ``results/demo_output.txt``.
"""

from pathlib import Path
from engine.runner import run_config

CONFIG_PATH = Path(__file__).parent.parent / "config" / "example_config.yaml"
RESULT_PATH = Path(__file__).parent / "results" / "demo_output.txt"

def demo() -> None:
    results = run_config(CONFIG_PATH)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULT_PATH.open("w", encoding="utf-8") as f:
        for left, right, value in results:
            f.write(f"query [{left}, {right}] = {value}\n")
    print(f"Demo finished, results written to {RESULT_PATH}")

if __name__ == "__main__":
    demo()
