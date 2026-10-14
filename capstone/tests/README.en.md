# Capstone Tests

[简体中文](README.md) | [English](README.en.md)

`cases.json` supplies 29 public Scalar inputs and expected results. `run.py` invokes a student compiler's check/run commands, checking streams, statuses, codes, and selected exact locations. A missing compiler is an error, not a skip.

```sh
python3 capstone/tests/run.py --compiler /absolute/path/minilang --stage check --report build/frontend.json
python3 capstone/tests/run.py --compiler /absolute/path/minilang --stage run --report build/acceptance.json
```

Check mode validates only the front end. Run mode first checks every input, then executes valid programs. Each invocation has a 15-second timeout; failures are collected and produce exit 1. The runner does not yet verify emit-ir, JIT/AOT differential behavior, or all spans, so 29/29 is not full language conformance.

The Scalar C runtime is in `../runtime/`. There is no complete reference compiler yet; program expectations require cross-validation on reference and independent implementations before launch. Hidden tests hide inputs, not language rules.
