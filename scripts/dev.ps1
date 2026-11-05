# AMR Sentinel AI — Local Development Launcher (PowerShell)
param(
    [string]$Service = "all"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  AMR Sentinel AI - Local Development Environment" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

function Start-Backend {
    Write-Host "[API] Starting FastAPI on http://localhost:8000..." -ForegroundColor Green
    Set-Location "$Root"
    $env:PYTHONPATH = "services/api"
    & "$Root\.venv\Scripts\uvicorn.exe" app.main:app --host 0.0.0.0 --port 8000 --reload --app-dir services/api
}

function Start-Frontend {
    Write-Host "[Web] Starting Next.js on http://localhost:3000..." -ForegroundColor Green
    Set-Location "$Root\apps\web"
    npm run dev
}

if ($Service -eq "api") {
    Start-Backend
} elseif ($Service -eq "web") {
    Start-Frontend
} else {
    Write-Host "To run full stack locally:" -ForegroundColor Yellow
    Write-Host "  Terminal 1 (Backend):  .\scripts\dev.ps1 -Service api" -ForegroundColor White
    Write-Host "  Terminal 2 (Frontend): .\scripts\dev.ps1 -Service web" -ForegroundColor White
    Write-Host ""
    Write-Host "Starting Backend now in this terminal..." -ForegroundColor Yellow
    Start-Backend
}
