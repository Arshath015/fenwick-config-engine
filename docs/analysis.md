# Configuration‑Driven Behaviour Analysis

The example config demonstrates two key properties of the engine:

1. **Deterministic sequencing** – Updates are applied in the exact order they
   appear before any subsequent query consumes the state. This makes the
   behaviour fully reproducible simply by reordering the list entries.
2. **Zero‑initialisation shortcut** – Supplying an ``initial`` array of zeros
   is equivalent to omitting it, but the explicit list clarifies intent and
   validates the schema.

When the config is extended with additional ``query`` entries, the runtime
cost remains linear in the number of operations because each operation is
handled in O(log n) time by the underlying Fenwick tree. No extra memory is
allocated beyond the tree itself, keeping the engine suitable for large
datasets (e.g., n > 10⁶) as long as the configuration file fits in memory.
