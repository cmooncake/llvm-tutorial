# Instructional Writing Guide

[简体中文](writing-guide.md) | [English](writing-guide.en.md)

Write for students with C/C++, data structures, and introductory compiler knowledge who are new to LLVM engineering. Introduce a term by stating the problem it solves, showing a minimal example, and then naming it formally.

## Chapter Development

Begin with an observable problem, establish the next conceptual model, add one variable at a time, ask for a prediction, run a tool, explain the evidence, assign a bounded exercise, diagnose common errors, and connect to the next chapter. Objectives and acceptance lists do not replace explanatory prose.

## Titles

Use stable academic subjects such as Lexical Analysis, Static Single Assignment Form, and Calling Conventions. Narrative hooks belong in the body. Use “Laboratory N,” “Programming Exercise,” and “Course Project” consistently.

## Examples and Exercises

Code is short enough to explain line by line, preceded by its purpose and followed by interpretation. Show at least one failure. Distinguish course design choices from LLVM rules. Mark unvalidated code honestly.

Exercises define context, behavior, constraints, starting guidance, and completion evidence. At least one result requires explanation rather than only an output check.

## Tone and Review

Use direct, respectful prose. Avoid “obvious,” “easy,” and “simply” for first exposure. Before publication check the opening problem, terminology, paragraph progression, expected observations, structural versus semantic correctness, evidence, and technical titles.

Organization is informed by the public compiler courses MIT 6.035, Stanford CS143, CMU 15-411/611, and Berkeley CS164; no lecture or assignment text is copied.

