# LLVM Tutorial Versions and Lab Environments

[简体中文](environment-research.md) | [English](environment-research.en.md)

Research date: 2026-10-13. Explicit upstream requirements and our own decisions are distinguished below. A course year is not evidence of its LLVM version.

## Upstream comparison

| Material | Version and environment evidence | Lesson for this course |
|---|---|---|
| [Kaleidoscope 22.1.0](https://releases.llvm.org/22.1.0/docs/tutorial/index.html) | Release-specific documentation exists; the [live tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/) is not frozen | Match APIs to release documentation; a small tutorial's engineering shortcuts are not a capstone architecture |
| [llvm-tutor](https://github.com/banach-space/llvm-tutor#development-environment) | The opened README specifies LLVM 23, C++17, CMake ≥ 3.20, and reports testing on Ubuntu 23.04 / macOS 11.7; it uses lit/FileCheck | Adopt independent plugins, tests, and CI, not the rolling environment; upstream claims are not our validation |
| [CMU 15-411 Spring 2024 Lab 6](https://www.cs.cmu.edu/~janh/courses/411/24/labs/lab6llvm.pdf) | Refers to Andrew Linux machines and requires LLVM/native backends, regression tests, and a report; no major version is specified in this assignment | Learn stable compiler interfaces and experimental evaluation; do not invent a CMU version pin |
| [Cornell CS 6120 Spring 2025 Lesson 7](https://www.cs.cornell.edu/courses/cs6120/2025sp/lesson/7/) | Requires LLVM/CMake, illustrates Homebrew, and warns against Xcode's LLVM; no version is pinned | Distinguish the system compiler from a full SDK; reconcile old video commands with corrected text |
| [MLIR Getting Started](https://mlir.llvm.org/getting_started/) / [Toy](https://mlir.llvm.org/docs/Tutorials/Toy/) | Build MLIR from llvm-project with examples/assertions and run `check-mlir`; web commands do not check out a release | Supply a fixed tag; do not require a full source build before the first lab |

Search snippets returned LLVM 22 for llvm-tutor, while opening its README returned 23. Search results are not lockfiles. Semester/release pages provide fixed context; main branches and live documentation can change.

## Choosing the course environment

The course needs one reproducible environment, not the highest version number. LLVM 22.1 has release documentation; [apt.llvm.org](https://apt.llvm.org/) provides the Noble `llvm-toolchain-noble-22` repository. Ubuntu 24.04 works across Linux, WSL2, and GitHub Actions, reducing ABI, library, linker, and shell differences.

Install development packages for foundational labs so students can focus on IR and passes. Source builds become useful when modifying LLVM, enabling assertions, or building course dialects. This is a teaching tradeoff, not a claim that other platforms are unsuitable.

Our installer uses a dedicated apt source with `signed-by` and checks the signing key fingerprint, rather than copying old global `apt-key` commands. A release-line pin does not freeze patches; see the [version policy](version-policy.en.md) for the pre-semester image-freezing requirement.

## Source environment for the MLIR elective

This is a preparation path with a fixed tag, not a validated course MLIR lab. Run it in a separate directory with Git, CMake, Ninja, a C++ toolchain, and Python installed. The basic environment does not require CUDA:

```sh
git clone --depth 1 --branch llvmorg-22.1.0 https://github.com/llvm/llvm-project.git
cmake -S llvm-project/llvm -B llvm-project/build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_PROJECTS="clang;mlir" \
  -DLLVM_TARGETS_TO_BUILD=Native \
  -DLLVM_BUILD_EXAMPLES=ON \
  -DLLVM_ENABLE_ASSERTIONS=ON
cmake --build llvm-project/build --target check-mlir --parallel 2
```

This tag is an explicit version example, not a claim about the latest patch. Build more targets or the full tree when other Clang/LLVM tools are needed. `check-mlir` validates upstream MLIR, not the unimplemented Mini dialect. Add NVPTX/AMDGPU, drivers, and runtimes for GPU work; select parallelism according to available memory.

## Test organization

The [LLVM Testing Guide](https://llvm.org/docs/TestingGuide.html) distinguishes regression tests, unit tests, and the test suite; [FileCheck](https://llvm.org/docs/CommandGuide/FileCheck.html) matches IR structure. This repository currently uses CTest scheduling, a Python standard-library driver, and FileCheck, without a separate lit dependency. Introduce shared lit configuration when MiniLang/MLIR have substantial `RUN:` collections, rather than treating directives without a runner as automated tests.

Text checks do not replace behavior checks. The suite also executes functions with `lli`, checks expected behavior before and after optimization, and requires invalid IR to fail verification. See the [testing guide](testing.en.md) for coverage.
