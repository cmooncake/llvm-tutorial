#!/usr/bin/env sh
set -eu

failed=0
for name in clang llvm-config opt llc lli llvm-as llvm-dis llvm-link FileCheck cmake ninja python3; do
  if command -v "$name" >/dev/null 2>&1; then
    if output=$("$name" --version 2>&1); then
      version=$(printf '%s\n' "$output" | sed -n '1p')
      printf '[ok] %s - %s\n' "$name" "$version"
    else
      printf '[failed] %s: %s\n' "$name" "$output" >&2
      failed=1
    fi
  else
    printf '[missing] %s\n' "$name" >&2
    failed=1
  fi
done

if [ "$failed" -ne 0 ]; then
  printf '%s\n' 'LLVM tutorial environment is incomplete. See chapters/00-toolchain/README.md.' >&2
  exit 1
fi

