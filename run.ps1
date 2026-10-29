# Vaultwise launcher (Windows PowerShell 5.1+).
# Usage from the project folder:   .\run.bat          (or: powershell -ExecutionPolicy Bypass -File .\run.ps1)
# Options:  -Port 8001   use another port        -NoBrowser   do not open the browser
param([int]$Port = 8000, [switch]$NoBrowser)

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
$Url = "http://127.0.0.1:$Port"
$OllamaUrl = "http://127.0.0.1:11434"
$RequiredModels = @("llama3.2:3b", "nomic-embed-text")
$OptionalModels = @("llama3.1:8b")   # used for summaries; without it summaries use llama3.2:3b

function Step($msg) { Write-Host "  > $msg" -ForegroundColor Cyan }
function Ok($msg)   { Write-Host "    $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "    $msg" -ForegroundColor Yellow }
function Fail($msg) { Write-Host "    $msg" -ForegroundColor Red; exit 1 }

function Test-Url($u) {
    try { Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 3 | Out-Null; return $true } catch { return $false }
}

Write-Host ""
Write-Host "  Vaultwise - private answers from your company documents" -ForegroundColor White
Write-Host ""

# 1. Already running? Just open it.
if (Test-Url "$Url/health") {
    Ok "Vaultwise is already running at $Url"
    if (-not $NoBrowser) { Start-Process $Url }
    exit 0
}

# 2. Python
Step "Checking Python"
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { Fail "Python was not found. Install Python 3.10+ from https://www.python.org and tick 'Add to PATH'." }
Ok (& python --version)

# 3. Python packages (installed once)
Step "Checking Python packages"
& python -c "import fastapi, uvicorn, multipart, rank_bm25, numpy, scipy, yaml, docx, requests" 2>$null
if ($LASTEXITCODE -ne 0) {
    Warn "Installing required packages (first run only)..."
    & python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { Fail "pip install failed. Run: python -m pip install -r requirements.txt" }
}
Ok "Packages ready"

# 4. Ollama (the local AI engine)
Step "Checking the local AI engine (Ollama)"
if (-not (Test-Url "$OllamaUrl/api/tags")) {
    $ollama = Get-Command ollama -ErrorAction SilentlyContinue
    if (-not $ollama) { Fail "Ollama is not installed. Install it from https://ollama.com/download, then run this again." }
    Warn "Ollama is not running - starting it..."
    Start-Process -FilePath $ollama.Source -ArgumentList "serve" -WindowStyle Hidden
    $t = 0
    while (-not (Test-Url "$OllamaUrl/api/tags") -and $t -lt 30) { Start-Sleep -Seconds 1; $t++ }
    if (-not (Test-Url "$OllamaUrl/api/tags")) { Fail "Ollama did not start. Open the Ollama app from the Start menu and try again." }
}
Ok "Ollama is running on this computer"

# 5. Models (downloaded once; needs internet only the first time)
Step "Checking AI models"
$tags = (Invoke-WebRequest -Uri "$OllamaUrl/api/tags" -UseBasicParsing).Content | ConvertFrom-Json
$have = @($tags.models | ForEach-Object { $_.name })
foreach ($m in $RequiredModels) {
    $found = $have | Where-Object { $_ -eq $m -or $_ -eq "$m`:latest" }
    if (-not $found) {
        Warn "Downloading $m (first run only, needs internet)..."
        & ollama pull $m
        if ($LASTEXITCODE -ne 0) { Fail "Could not download $m. Check your internet connection and run: ollama pull $m" }
    }
}
foreach ($m in $OptionalModels) {
    if (-not ($have | Where-Object { $_ -eq $m })) {
        Warn "Optional model $m is not installed: summaries will use llama3.2:3b (run 'ollama pull $m' for more accurate summaries)."
    }
}
Ok "Models ready"

# 6. Port
$busy = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($busy) { Fail "Port $Port is used by another program. Run: .\run.bat -Port 8001" }

# 7. Open the browser as soon as the server answers (in a small hidden helper)
if (-not $NoBrowser) {
    $opener = "for(`$i=0;`$i -lt 180;`$i++){try{Invoke-WebRequest -Uri '$Url/health' -UseBasicParsing -TimeoutSec 2|Out-Null;Start-Process '$Url';break}catch{Start-Sleep -Seconds 1}}"
    Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile", "-Command", $opener
}

# 8. Start Vaultwise (stays in this window; press Ctrl+C to stop)
Write-Host ""
Ok "Starting Vaultwise at $Url  (only this computer can open it)"
Write-Host "    Keep this window open while you use Vaultwise. Press Ctrl+C to stop." -ForegroundColor Gray
Write-Host ""
& python -m uvicorn vaultwise.api:app --app-dir src --host 127.0.0.1 --port $Port
