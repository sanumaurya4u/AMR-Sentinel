# AMR Sentinel AI — Test & Quality Gate Runner
$ErrorActionPreference = "Stop"
$CallerLocation = Get-Location
$Root = Split-Path -Parent $PSScriptRoot

function Remove-DirectorySafely([string]$targetPath, [int]$maxAttempts = 5, [int]$baseDelayMs = 200) {
    if (-not (Test-Path -LiteralPath $targetPath)) {
        return
    }

    $lastErr = ""
    for ($i = 1; $i -le $maxAttempts; $i++) {
        $oldEAP = $ErrorActionPreference
        try {
            # Localize ErrorActionPreference to prevent native stderr 2>&1 from triggering terminating NativeCommandError
            $ErrorActionPreference = "SilentlyContinue"
            $output = & cmd.exe /c "rmdir /s /q `"$targetPath`" 2>&1"
            if ($output) {
                $lastErr = ($output | Out-String).Trim()
            }
        }
        catch {
            $lastErr = $_.Exception.Message
        }
        finally {
            $ErrorActionPreference = $oldEAP
        }

        # Check if directory has been successfully removed
        if (-not (Test-Path -LiteralPath $targetPath)) {
            # Windows NTFS handle drain: allow file table entries and handle closures to settle
            Start-Sleep -Milliseconds 500
            if (-not (Test-Path -LiteralPath $targetPath)) {
                return
            }
        }

        # Progressive backoff delay before next retry attempt
        Start-Sleep -Milliseconds ($baseDelayMs * $i)
    }

    if (Test-Path -LiteralPath $targetPath) {
        Write-Error "Failed to clean '$targetPath' after $maxAttempts attempts. Locks may be held by another process: $lastErr"
        exit 1
    }
}

try {
    Set-Location "$Root"

    # Clean stale build artifacts using native Windows cmd with retry loop to prevent handle race conditions
    Remove-DirectorySafely "$Root\apps\web\.next"
    if (Test-Path "$Root\apps\web\tsconfig.tsbuildinfo") {
        Remove-Item -Force "$Root\apps\web\tsconfig.tsbuildinfo" -ErrorAction SilentlyContinue
    }

    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "  Running Quality Gates & Automated Tests" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan

    # 1. Python Linter
    Write-Host "`n[1/4] Running Ruff linter..." -ForegroundColor Yellow
    & "$Root\.venv\Scripts\ruff.exe" check "$Root\services\api"
    if ($LASTEXITCODE -ne 0) { exit 1 }

    # 2. Python Architecture Isolation & Unit Tests
    Write-Host "`n[2/4] Running AST Isolation & Pytest Suite..." -ForegroundColor Yellow
    $env:PYTHONPATH = "$Root\services\api"
    & "$Root\.venv\Scripts\pytest.exe" "$Root\services\api\tests" -v
    if ($LASTEXITCODE -ne 0) { exit 1 }

    # 3. Web Type Check
    Write-Host "`n[3/4] Running TypeScript Strict Type-Check..." -ForegroundColor Yellow
    Set-Location "$Root\apps\web"
    npm run type-check
    if ($LASTEXITCODE -ne 0) { exit 1 }

    # Inter-gate handle drain: allow Node.js tsc process handles to release before build starts
    Start-Sleep -Milliseconds 250

    # 4. Next.js Production Build
    Write-Host "`n[4/4] Running Next.js Production Build..." -ForegroundColor Yellow
    Set-Location "$Root\apps\web"
    npm run build
    if ($LASTEXITCODE -ne 0) { exit 1 }

    Write-Host "`n==========================================================" -ForegroundColor Green
    Write-Host "  All Quality Gates Passed Successfully!" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
}
finally {
    Set-Location $CallerLocation
}
