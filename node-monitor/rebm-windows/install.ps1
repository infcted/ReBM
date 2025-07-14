# ReBM Windows Monitor Installer

Write-Host "Installing ReBM Windows Monitor..." -ForegroundColor Cyan

# Ensure running as Administrator
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator."
    exit 1
}

# Create directory
$targetDir = "C:\ReBM"
if (-not (Test-Path $targetDir)) {
    New-Item -Path $targetDir -ItemType Directory | Out-Null
}

# Copy files
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Copy-Item "$scriptPath\node_monitor.py" $targetDir -Force

# Install Python requests if needed
try {
    python -c "import requests" 2>$null
} catch {
    Write-Host "Installing requests module..."
    pip install requests
}

# Download and install NSSM if not present
$nssmPath = "$targetDir\nssm.exe"
if (-not (Test-Path $nssmPath)) {
    Write-Host "Downloading NSSM..."
    Invoke-WebRequest -Uri "https://nssm.cc/release/nssm-2.24.zip" -OutFile "$targetDir\nssm.zip"
    Expand-Archive "$targetDir\nssm.zip" -DestinationPath $targetDir -Force
    $nssmExe = Get-ChildItem -Path $targetDir -Recurse -Filter nssm.exe | Select-Object -First 1
    if ($nssmExe) {
        Copy-Item $nssmExe.FullName $nssmPath -Force
    }
    Remove-Item "$targetDir\nssm.zip" -Force
}

# Set up the service using NSSM
$serviceName = "ReBMWindowsMonitor"
$pythonExe = (Get-Command python).Source
$serviceDisplayName = "ReBM Windows Monitor"

# Remove existing service if present
& $nssmPath remove $serviceName confirm

# Install service
& $nssmPath install $serviceName $pythonExe "$targetDir\node_monitor.py"
& $nssmPath set $serviceName DisplayName "$serviceDisplayName"
& $nssmPath set $serviceName Start SERVICE_AUTO_START
& $nssmPath set $serviceName AppDirectory $targetDir
& $nssmPath set $serviceName AppEnvironmentExtra "REBM_API_URL=http://localhost:8000" "NODE_NAME=$env:COMPUTERNAME" "CHECK_INTERVAL_SECONDS=300"

# Start the service
Start-Service $serviceName

Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "Service status: $(Get-Service $serviceName).Status"
Write-Host ""
Write-Host "Commands:" -ForegroundColor Yellow
Write-Host "  Get-Service -Name '$serviceName'" -ForegroundColor Yellow
Write-Host "  Restart-Service -Name '$serviceName'" -ForegroundColor Yellow
Write-Host "  Stop-Service -Name '$serviceName'" -ForegroundColor Yellow 