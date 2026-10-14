# Research Reports and Experimental Records

[简体中文](project-report.md) | [English](project-report.en.md)

The final report answers one concrete question rather than listing implementation dates. Aim for 6–8 pages plus appendices containing long IR, complete commands, and raw measurements. Negative results can be valuable if readers can determine what the evidence supports.

## Proposal

M1 uses 1–2 pages to state the hypothesis, baseline, compiler intervention, correctness strategy, and results that would refute the hypothesis. Identify a runnable slice achievable within two weeks and a fallback without GPU or external-service requirements.

“Can conservative range analysis reduce dynamic bounds checks on four loop families while preserving traps?” is measurable. “Build a powerful optimizer” is not. After scope freeze, explain how new language features serve the original question or move them to future work.

## Method and correctness

Describe source rules, analysis domain, transfer functions, convergence, and transformation preconditions. MLIR projects identify legal operations, type conversion, materialization, and residual operations at each stage. Separate conservative implementation approximations from language semantics.

Provide a case that must transform, one that may transform, and one that must not. Discuss oracle independence: two backends sharing a front end cannot expose every shared front-end error. Random testing, verification, and formal validation have different limits; naming a tool does not replace an argument.

## Evaluation design

Include at least three explainable workloads and one expected not to benefit. Reduce input sizes if resources are limited, not the set of inconvenient results. Record input sources, seed, size, compiler options, commit, SDK version, CPU, system, and measurement date.

Check correctness before timing. Separate compilation/optimization, startup or JIT, and steady-state kernels. Use at least three warmups and twenty measured runs per configuration, alternating or randomizing order. Long experiments may use fewer runs with an explicit uncertainty discussion. Retain all valid samples rather than deleting slow ones. Report medians, dispersion, and per-workload regressions.

Define speedup as baseline time divided by candidate time for the same workload; above one favors the candidate. A geometric mean may summarize workload ratios, but do not average unrelated absolute timings. Small or noisy samples support limited observations, not unsubstantiated significance claims.

Perform an ablation: disable your pass, remove an analysis component, disable a schedule feature, or compare with a fixed conservative policy. An ablation permitting incorrect transformations does not belong in the performance average. Report correctness failures separately with their cause.

## Report order

The repository provides `tools/measure.py` as a starting point for deterministic executables:

```sh
python3 tools/measure.py --baseline build/base --candidate build/candidate \
  --arg=100000 --runs 20 --warmups 3 \
  --context "commit=<sha>; LLVM=22.1.8; flags=<flags>; workload=<name>" \
  --output build/timing.json
```

It checks stdout/stderr on every run, aborts on failures/mismatches, and saves commands, executable hashes, and all samples. Measurements include process startup, not kernel-only or JIT steady-state time. Timing checks do not replace language correctness tests.

1. Question, hypothesis, contribution: distinguish your work from existing infrastructure.
2. Semantics and method: preconditions, implementation boundaries, correctness argument.
3. Experimental setup: baselines, workloads, environment, metrics, statistics.
4. Results: individual outcomes, ablation, negative findings, interpretation.
5. Threats to validity: shared front ends, size, target, caching, compiler versions.
6. Conclusions and reproduction: claims limited to actual evidence.

Append build/run commands, logs, raw JSON/text data, dependency versions, citations, and contributions. Plots or best times alone are insufficient. A reproducer should distinguish build failure, wrong execution, and different performance.

## Defense and peer reproduction

Each team presents for fifteen minutes with ten minutes of questions. Demonstrate a valid input, counterexample, intermediate representation, and result with a baseline. Do not spend the session rerunning a full benchmark. Instructors ask each member to explain a cross-module boundary.

Another team reproduces one conclusion using the supplied commands, recording environment differences, failed steps, and assistance. Authors respond in the final report. Reproduction failure is an engineering observation, not immediate evidence that the reproducer lacks skill.

## Method reference

[Cornell CS 6120](https://www.cs.cornell.edu/courses/cs6120/2019fa/project/) combines implementation, empirical evaluation, and design review. Our sample counts, page limit, and metrics are teaching conventions, not guarantees of publication readiness or statistical significance.
