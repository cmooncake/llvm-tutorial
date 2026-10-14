# Course Tools

[简体中文](README.md) | [English](README.en.md)

`setup-ubuntu.sh` adds the LLVM 22 apt source and installs development tools on Ubuntu 24.04 when explicitly run with sudo. It changes system packages; it is not an environment checker. See the [testing guide](../docs/testing.en.md) for CMake/CTest commands and coverage.

Course tools include environment and documentation audits and define stable CLI boundaries for IR verification, test execution, CFG export, and benchmark summaries. They never implement core compiler work on behalf of students.

```powershell
./tools/check-env.ps1
./tools/audit-docs.ps1
```

`audit-docs.ps1` checks translation pairs, language navigation, local links, and duplicate headings.

`measure.py` compares complete process times for deterministic executables, retaining raw samples, executable hashes, execution order, dispersion, and output equality checks. It does not isolate startup, JIT, or kernel time or automatically establish significance; see [research reports](../docs/project-report.en.md) for usage and limits. See the [shared labs](../docs/graduate-labs.en.md) for MLIR entry points and stage artifacts.

