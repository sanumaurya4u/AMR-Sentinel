# AMR Sentinel AI — Test & Quality Gate Runner
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Running Quality Gates & Automated Tests" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Python Linter
Write-Host "`n[1/4] Running Ruff linter..." -ForegroundColor Yellow
& "$Root\.venv\Scripts\ruff.exe" check "$Root\services\api"
if ($LASTEXITCODE -ne 0) { exit 1 }

# 2. Python Architecture Isolation & Unit Tests
Write-Host "`n[2/4] Running AST Isolation & Pytest Suite..." -ForegroundColor Yellow
$env:PYTHONPATH = "services/api"
& "$Root\.venv\Scripts\pytest.exe" "$Root\services\api\tests" -v
if ($LASTEXITCODE -ne 0) { exit 1 }

# 3. Web Type Check
Write-Host "`n[3/4] Running TypeScript Strict Type-Check..." -ForegroundColor Yellow
Set-Location "$Root\apps\web"
npm run type-check
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  All Quality Gates Passed Successfully!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
