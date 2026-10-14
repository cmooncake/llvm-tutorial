$ErrorActionPreference = 'Stop'

$required = @('clang', 'llvm-config', 'opt', 'llc', 'lli', 'llvm-as', 'llvm-dis', 'llvm-link', 'FileCheck', 'cmake', 'ninja', 'python')
$failed = $false

foreach ($name in $required) {
  $command = Get-Command $name -ErrorAction SilentlyContinue
  if (-not $command) {
    Write-Host "[missing] $name" -ForegroundColor Red
    $failed = $true
    continue
  }

  $output = & $name --version 2>&1
  if ($LASTEXITCODE -ne 0) {
    Write-Host "[failed] $name - $output" -ForegroundColor Red
    $failed = $true
    continue
  }
  $firstLine = $output | Select-Object -First 1
  Write-Host "[ok] $name - $firstLine" -ForegroundColor Green
}

if ($failed) {
  Write-Error 'LLVM tutorial environment is incomplete. See chapters/00-toolchain/README.md.'
}

