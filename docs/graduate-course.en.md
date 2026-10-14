# Graduate Course in LLVM and MLIR Compiler Engineering

[简体中文](graduate-course.md) | [English](graduate-course.en.md)

This course asks how source semantics enter an intermediate representation, under what conditions optimizations preserve them, and how multiple representation levels support domain optimization. Students begin without LLVM engineering experience, build an executable compiler core, and investigate one transformation or lowering strategy over a semester.

The schedule spans 16 weeks, with two 90-minute discussions, a 60-minute lab clinic, and an estimated 8–12 hours of independent work per week. Teams of two are recommended. Individual projects reduce the workload set, not correctness requirements. Prerequisites are C++, data structures, introductory compiler construction, and computer architecture; this is not an introductory programming course.

## Scope

Required topics include LLVM IR, SSA, dataflow analysis, pass engineering, source lowering, optimization correctness, experimental methods, MLIR operations/regions/conversion, and CPU bufferization. Everyone completes the shared MLIR lab. Custom dialects, Transform schedules, GPUs, and advanced JIT systems are project specializations.

To reserve time for optimization and MLIR, common acceptance uses the [MiniLang Scalar core](language-profile.en.md): integers, booleans, functions, lexical scope, mutable bindings, conditions, and loops. Arrays, strings, closures, and complete debug information are no longer simultaneous requirements for every team. Projects choosing them must first specify their semantics rather than rely on undefined runtime helpers. This scope decision does not remove diagnostics, tests, or runtime errors.

Chapter numbers identify topics, not weeks. Chapters 00–10 are interleaved in the first half; chapters 11 and 14–18 form the optimization and multilevel-IR sequence. See [release readiness](release-readiness.en.md) for the actual state of notes, assignments, and implementations.

## Observable learning outcomes

| ID | Independent student task | Evidence |
|---|---|---|
| O1 | Construct valid SSA for branches/loops and explain dominance | L1 IR, phi argument, counterexample |
| O2 | State optimization preconditions, handling flags, effects, and invalidation | L2 correctness argument and non-transformable inputs |
| O3 | Turn language rules into front-end/back-end contracts | L3/L4 diagnostics, execution, ABI tests |
| O4 | Design staged MLIR lowering and localize conversion failures | L5 intermediate IR and legality argument |
| O5 | Distinguish performance changes, noise, and semantic errors | Raw data, baseline, ablation, limitations |
| O6 | Enable independent reproduction and defend technical decisions | Reproduction exercise and individual defense |

## Sixteen-week schedule

Exit checks are formative, not separate graded submissions. See [assignments](assignments.en.md) for precise contracts.

| Week | Discussion and reading | Lab and exit check | Due |
|---:|---|---|---|
| 1 | Compilation stages and observable behavior; 00–01 | L0 environment; explain what a verifier cannot prove | Environment record |
| 2 | SSA, dominance, loops; 02 | Diamond/loop phi construction and edge semantics | L1 |
| 3 | C++ APIs, ownership, Pass Manager; 03–04 | Generator/counting pass; explain `all()`/`none()` | Begin L2 |
| 4 | Dataflow fixed points and local optimization legality; 04, 11 | Refute an unsafe rule with a counterexample | L2 |
| 5 | Language contracts and front-end interfaces; 05–07 | Locations, recovery, symbol tables; discussion 1 | Begin L3 |
| 6 | Typing and reachable returns; 07–08 | Front-end acceptance; review research questions | L3, M1 proposal |
| 7 | CFG lowering, memory, ABI; 08–09 | Short circuit/traps, call order, an incorrect GEP | Begin L4 |
| 8 | JIT/AOT and diagnostics; 10, 12 | One reliable execution path; lli is not your own ORC JIT | L4 |
| 9 | Loop optimization, aliasing, poison; 11 | Correct baseline; discussion 2 | M2 executable baseline |
| 10 | MLIR regions and dialects; 14, 16 | L5 SCF → CF → LLVM; track lost information | Begin L5 |
| 11 | Conversion and bufferization; 15–17 | Live old-tensor counterexample; discussion 3 | L5 |
| 12 | Custom dialect or optimization-analysis specialization | Midterm demo, cross-machine reproduction, failure clinic | M3 interim results |
| 13 | Transform schedules and experimental design; 18 | Parameter space and ablation; discussion 4 | Freeze evaluation plan |
| 14 | Research experiments and interpretation | TA raw-data review; reproduce, do not add core features | Report draft |
| 15 | Artifact review and individual defense | Clean build, negative inputs, limitations, module boundaries | Code freeze |
| 16 | Research reports and peer review | 15-minute presentation, 10-minute questions; reproduce another team | M4 final package |

Do not expand the common language after week 6. Teams without an executable baseline in week 9 stop adding features and reconnect the smallest end-to-end program. Instructors narrow the research question rather than take over implementation at the end.

## Running a class meeting

A 90-minute discussion begins with a falsifiable question, such as whether two functions returning zero are interchangeable. Allow five minutes for individual judgments and fifteen for counterexamples. Introduce the definitions needed to justify those judgments, spend twenty-five minutes deriving IR or analysis results, twenty reading an implementation, and ten on an individual exit response. Use the remaining time for clarification rather than more terminology.

The second meeting works from experimental results. A student presents a minimal failure, states the input and expected behavior, and identifies the failing phase. Before editing their IR, ask which language rule or verifier invariant is violated. If that is unclear, return to semantics instead of trying more pass orders.

The clinic addresses environment and integration issues, not replacement lectures. TAs record problem categories, reproduction commands, and time to resolution. When the same environment issue affects three teams, fix the shared script and publish an erratum rather than making everyone debug it separately.

## Discussion questions and instructor answers

Use these formatively; assess the same ideas on different assignment inputs.

| Week | Question | Essential answer |
|---:|---|---|
| 1 | Does successful IR verification establish source correctness | It checks IR invariants, not equivalence to source semantics |
| 2 | Does a phi use belong to the merge block or an incoming edge | Incoming values are edge-associated; ordinary-instruction reasoning is insufficient |
| 3 | Can a Value outlive the Context supporting its Module | LLVM objects depend on Context-owned resources; their lifetimes are not independent |
| 4 | Does unchanged CFG justify preserving every analysis | No; preserve precisely or invalidate conservatively |
| 5 | Should lexing reject the positive magnitude in `-2147483648` | Not prematurely; separate magnitude tokenization from unary-minus validation |
| 6 | How does a returning branch merge with a value-producing branch | The returning branch has no reachable merge edge and supplies no phi incoming |
| 7 | Can both sides of `false && trap_call()` execute before a select | No; effects and traps make evaluation order observable |
| 8 | Does invoking lli demonstrate your own ORC implementation | No; identify the boundary between generated IR and the external executor |
| 9 | Can a potentially dividing-by-zero expression move outside an if | Only with a speculation-safety argument; new paths may otherwise fail |
| 10 | Is LLVM dialect already an LLVM IR file | No; translation and final verification remain |
| 11 | Can a tensor update overwrite a buffer when the old value remains live | Conflict/alias analysis may require a copy; bufferization is not lifetime management |
| 12 | Does a verified custom op necessarily have a lowering | No; parsing, semantic verification, and conversion legality are distinct contracts |
| 13 | Does the fastest single tile-size measurement identify the best schedule | No; repeat, control order, vary workloads, and check correctness |
| 14 | Does a geometric mean of 1.1× mean every workload improved | No; show individual results and regressions |
| 15 | May a hidden test introduce an unpublished language rule | No; hide inputs, not the specification |
| 16 | Can a project with no speedup earn a strong grade | Yes, with a sound question, correct implementation, rigorous evaluation, and justified conclusions |

## Reading discussions

Teams rotate as discussion leaders. Others submit a one-page memo identifying one technical claim, its assumptions, and an experiment that could refute it. A summary of the abstract is insufficient. Four discussions address LLVM semantics, optimization validation, multilevel IR, and tensor memory management. Assign one core reading and one implementation excerpt, not an entire project's documentation.

- LLVM semantics: [LLVM 22.1 LangRef](https://releases.llvm.org/22.1.0/docs/LangRef.html), focusing on `phi`, `sdiv`, `nsw`, and poison.
- Validation: [Alive2 paper and author materials](https://web.ist.utl.pt/nuno.lopes/pubs.php?id=alive2-pldi21), discussing its scope, loop limitations, and complementarity with testing; solver setup is not a prerequisite for the first lab.
- Multilevel IR: [MLIR paper](https://arxiv.org/abs/2002.11054), relating its motivation to information lost in a concrete lowering.
- Memory: [One-Shot Bufferization](https://mlir.llvm.org/docs/Bufferization/), explaining copies when old tensor values remain live and separating allocation from deallocation.

## Research project boundaries

All teams use the same executable language core; the research increment answers one question. LLVM projects may study local value numbering, a safe LICM subset, range-analysis-assisted check elimination, or pass ordering. MLIR projects may study a domain operation's verifier, two lowering strategies, bufferization copies, or two Transform schedules. Include a baseline without the proposed transformation; do not attribute existing standard optimizations to your contribution.

M1 states the question, hypothesis, minimum implementation, baseline, and fallback. M2 supplies an executable baseline and a non-transformable case. M3 supplies preliminary correctness results, raw measurements, and a narrowed plan. M4 supplies code, reproduction instructions, a report, and individual contributions. See the [report template](project-report.en.md) and [assessment](assessment.en.md).

## Instructor responsibilities before launch

Students are not release testers for the teaching package. Instructors first run every assigned lab on a clean image and align reference code, public tests, and grading interfaces. Public reference code cannot later become secret. If teaching with public references, assess new semantic variants, tests, and explanations instead of pretending answers are inaccessible.

Do not assign unfinished assets as ready-to-use coursework. [Release readiness](release-readiness.en.md) lists blockers and units suitable for a pilot. Complete notes, complete code, and a completed teaching pilot are different maturity levels.

## Teaching design references

The proposal, progress-report, final-report, and design-review sequence draws on [CMU 15-745](https://www.cs.cmu.edu/afs/cs/academic/class/15745-f25/www/projects.html) and [Cornell CS 6120](https://www.cs.cornell.edu/courses/cs6120/2019fa/project/). Weeks, weights, and language scope are this course's design, not a reproduction of either university's course.
