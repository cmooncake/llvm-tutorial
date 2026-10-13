$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$markdown = Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.md' |
  Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' }
$errors = [System.Collections.Generic.List[string]]::new()

foreach ($file in $markdown) {
  $relative = [IO.Path]::GetRelativePath($root, $file.FullName)
  $isEnglish = $file.Name.EndsWith('.en.md')

  if ($isEnglish) {
    $baseName = $file.Name.Substring(0, $file.Name.Length - 6) + '.md'
    $pair = Join-Path $file.DirectoryName $baseName
  } elseif ($file.Name -eq 'README.md') {
    $pair = Join-Path $file.DirectoryName 'README.en.md'
  } else {
    $pair = Join-Path $file.DirectoryName ($file.BaseName + '.en.md')
  }

  if (-not (Test-Path -LiteralPath $pair)) {
    $errors.Add("missing translation pair: $relative")
  }

  $content = Get-Content -LiteralPath $file.FullName -Raw -Encoding utf8
  if ($content -notmatch '\[简体中文\]' -or $content -notmatch '\[English\]') {
    $errors.Add("missing language navigation: $relative")
  }

  $headings = [regex]::Matches($content, '(?m)^#{1,6}\s+(.+?)\s*$') |
    ForEach-Object { $_.Groups[1].Value.Trim().ToLowerInvariant() }
  $duplicates = $headings | Group-Object | Where-Object { $_.Count -gt 1 }
  foreach ($duplicate in $duplicates) {
    $errors.Add("duplicate heading '$($duplicate.Name)': $relative")
  }

  if (-not $isEnglish -and (Test-Path -LiteralPath $pair)) {
    $englishContent = Get-Content -LiteralPath $pair -Raw -Encoding utf8
    $numbered = @([regex]::Matches($content, '(?m)^##\s+(\d+(?:\.\d+)*)\b') |
      ForEach-Object { $_.Groups[1].Value })
    $englishNumbered = @([regex]::Matches($englishContent, '(?m)^##\s+(\d+(?:\.\d+)*)\b') |
      ForEach-Object { $_.Groups[1].Value })
    $difference = Compare-Object $numbered $englishNumbered
    if ($difference) {
      $errors.Add("numbered heading mismatch: $relative")
    }
  }

  foreach ($match in [regex]::Matches($content, '\[[^\]]+\]\(([^)]+)\)')) {
    $target = $match.Groups[1].Value
    if ($target -match '^(https?://|mailto:|#)') { continue }
    $pathPart = ($target -split '#', 2)[0]
    if ([string]::IsNullOrWhiteSpace($pathPart)) { continue }
    $resolved = [IO.Path]::GetFullPath((Join-Path $file.DirectoryName $pathPart))
    if (-not (Test-Path -LiteralPath $resolved)) {
      $errors.Add("broken local link '$target': $relative")
    }
  }
}

if ($errors.Count -gt 0) {
  $errors | Sort-Object -Unique | ForEach-Object { Write-Error $_ }
  exit 1
}

Write-Host "Documentation audit passed: $($markdown.Count) Markdown files checked."

