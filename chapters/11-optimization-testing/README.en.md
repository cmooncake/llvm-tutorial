# Chapter 11: Optimization and Compiler Testing

[简体中文](README.md) | [English](README.en.md)

> Estimated time: 6–9 hours. This chapter replaces “it runs” with evidence for semantics and measurements for optimization.

An optimization is correct only when it preserves every behavior observable under the language specification. Shorter IR is not necessarily faster, and a faster benchmark does not prove semantic equivalence for all programs. Correctness testing and performance experiments therefore remain separate.

## 11.1 Pass Pipelines

Use PassBuilder for standard `O0`, `O1`, and `O2` pipelines with target analysis information. Record custom extension points and expose the effective pipeline in logs.

Run the verifier after custom transformations. Treat overflow flags, poison, undefined behavior, aliasing, and side effects conservatively; C or C++ intuition does not replace the LLVM Language Reference.

## 11.2 Test Layers

Unit tests cover local lexer, parser, and semantic rules. lit/FileCheck regression tests inspect important IR and diagnostic structure. End-to-end tests observe program behavior. Differential tests compare JIT against AOT or optimized against unoptimized execution. Fuzzing searches for crashes, hangs, and phase disagreement.

FileCheck asserts important relationships rather than complete output. Diagnostic tests assert codes, spans, and parameters. Every regression first receives a failing test.

## 11.3 Performance Experiments

Use interpretable microbenchmarks and separate warm-up, JIT time, execution time, and linking. Report hardware, operating system, compiler version, pipeline, sample count, and statistical method. Observe at least two of run time, code size, and compile time.

## 11.4 Dataflow Analysis: Establish Facts Before Transforming

Calling a pass is not a graduate-level explanation of optimization. First implement a read-only analysis and state its flow direction, merge operator, and termination argument.

For liveness on non-SSA three-address code, `USE[B]` contains variables read before their first definition in B; `DEF[B]` contains variables defined in B. This is a backward may analysis:

```text
OUT[B] = union(IN[S] for S in successors(B))
IN[B]  = USE[B] union (OUT[B] - DEF[B])
```

Initialize sets to empty, with empty OUT at exits. Requeue predecessors only when IN changes. A finite variable universe and monotone growth ensure termination; one backward sweep need not solve a loop. Students record the changing sets, not just the final answer.

Use a diamond whose left arm defines `x = a + 1`, right arm defines `x = b + 1`, and merge returns x. Merge IN is `{x}`; the arm IN sets are `{a}` and `{b}`. Add a back edge and explain which update revisits a previously processed block.

In SSA, phi operands are edge uses, not ordinary successor-block uses. For each outgoing edge, subtract successor phi definitions from successor IN and add only that edge's phi operands, then union across edges. Otherwise a value from the other arm becomes incorrectly live on this path. Print analysis results first; discuss invalidation when adding a transformation.

## 11.5 Legality: Invariance Is Not Sufficient

Consider a divisor defined outside the following region but possibly zero:

```llvm
entry:
  br i1 %take, label %work, label %exit
work:
  %q = sdiv i32 42, %d
  br label %exit
exit:
  %r = phi i32 [ 0, %entry ], [ %q, %work ]
  ret i32 %r
```

With `%take=false, %d=0`, the original returns zero. Hoisting division into entry introduces UB on a previously defined path, despite valid IR structure. A zero-trip loop gives the analogous LICM counterexample. Do not demand a particular crash from executing the invalid transformation; check its forbidden placement and explain the semantic counterexample.

For each candidate, justify operand availability, additional execution, trapping/UB, memory interference, and dominance of uses. An invariant address does not establish an invariant load; unknown calls are not assumed effect-free. A student safe subset may handle only unflagged integer `add/sub/mul`, excluding memory, division, calls, and floating point. Do not call this complete LICM.

Distinguish wrapping arithmetic, `nsw` poison, and immediate UB. Scalar wrapping addition does not license `nsw`; poison production does not necessarily trap at that instruction. Consult the [LLVM 22 LangRef](https://releases.llvm.org/22.1.0/docs/LangRef.html).

## 11.6 Levels of Correctness Evidence

Submit preconditions and a semantic argument, minimal positive and forbidden cases, boundary values, and differential results. Random samples extend coverage; they do not establish a universal proof.

[Alive2](https://web.ist.utl.pt/nuno.lopes/pubs.php?id=alive2-pldi21) is an optional research tool. Distinguish success, counterexample, timeout, and unsupported input. Bounded loop reasoning does not prove arbitrary iteration counts. Students should derive a counterexample before discussing tool scope; solver installation is not the principal learning objective.

## Laboratory 11: Optimization Equivalence and Benchmarking

Build an `O0`/`O2` differential runner and benchmark one standard or custom optimization. Generate small well-typed random expression programs and compare output and traps before and after optimization.

Temporarily inject one unsound transformation on an experiment branch, demonstrate that the suite detects it, and then remove it. Keep correctness conclusions separate from performance conclusions.

## Submission

- reproducible and printable pass pipelines;
- unit, regression, end-to-end, and differential test entry points;
- a minimized regression test;
- raw benchmark data and analysis; and
- an optimization correctness argument.

## References

- [LLVM Testing Infrastructure Guide](https://llvm.org/docs/TestingGuide.html)
- [FileCheck](https://llvm.org/docs/CommandGuide/FileCheck.html)
- [Using the New Pass Manager](https://llvm.org/docs/NewPassManager.html)

