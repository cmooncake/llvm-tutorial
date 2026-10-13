$ErrorActionPreference = 'Stop'

$required = @('clang', 'llvm-config', 'opt', 'llc', 'lli', 'cmake', 'ninja')
$failed = $false

foreach ($name in $required) {
  $command = Get-Command $name -ErrorAction SilentlyContinue
  if (-not $command) {
    Write-Host "[missing] $name" -ForegroundColor Red
    $failed = $true
    continue
  }

  $firstLine = (& $name --version 2>&1 | Select-Object -First 1)
  Write-Host "[ok] $name - $firstLine" -ForegroundColor Green
}

if ($failed) {
  Write-Error 'LLVM tutorial environment is incomplete. See chapters/00-toolchain/README.md.'
}

