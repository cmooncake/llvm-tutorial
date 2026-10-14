#!/usr/bin/env bash
# Explicit opt-in installer for Ubuntu 24.04. Installs system packages.
set -euo pipefail
source /etc/os-release
if [[ "$ID" != ubuntu || "$VERSION_ID" != 24.04 || $(id -u) != 0 ]]; then
  echo 'Run with sudo on Ubuntu 24.04; this script installs system packages.' >&2
  exit 1
fi
apt-get update
apt-get install -y ca-certificates curl gnupg
key=$(mktemp)
trap 'rm -f -- "$key"' EXIT
curl --fail --location --retry 3 https://apt.llvm.org/llvm-snapshot.gpg.key -o "$key"
fingerprint=$(gpg --show-keys --with-colons "$key" | awk -F: '$1 == "fpr" {print $10; exit}')
if [[ "$fingerprint" != 6084F3CF814B57C1CF12EFD515CF4D18AF4F7421 ]]; then
  echo 'Unexpected LLVM signing key; inspect upstream key rotation before continuing.' >&2
  exit 1
fi
install -m 644 "$key" /usr/share/keyrings/llvm-tutorial.asc
printf '%s\n' 'deb [signed-by=/usr/share/keyrings/llvm-tutorial.asc] https://apt.llvm.org/noble/ llvm-toolchain-noble-22 main' \
  > /etc/apt/sources.list.d/llvm-tutorial.list
apt-get update
apt-get install -y build-essential cmake ninja-build python3 \
  clang-22 llvm-22 llvm-22-dev llvm-22-tools mlir-22-tools zlib1g-dev libzstd-dev
