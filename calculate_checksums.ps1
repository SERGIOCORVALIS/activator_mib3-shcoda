# PowerShell script for calculating SHA256 checksums
# For LG MEN3 Activator

$ErrorActionPreference = "Stop"

Write-Host "=== LG MEN3 Activator - Checksum Calculation ===" -ForegroundColor Green
Write-Host ""

# File paths
$scriptPath = "Data\activator_device.script.module_20251204-1914\0\activation.sh"
$installerPath = "Data\activator_device.script.module_20251204-1914\0\installer.txt"
$mnfPath = "Meta\Normal_release_2\activator_device\script.module\1.0.0.mnf"

# Check if files exist
if (-not (Test-Path $scriptPath)) {
    Write-Host "ERROR: File $scriptPath not found!" -ForegroundColor Red
    exit 1
}

Write-Host "1. Calculating checksum for activation.sh..." -ForegroundColor Yellow

# Get file size
$fileInfo = Get-Item $scriptPath
$fileSize = $fileInfo.Length
Write-Host "   File size: $fileSize bytes" -ForegroundColor Cyan

# Calculate SHA256 hash
$hashAlgorithm = [System.Security.Cryptography.SHA256]::Create()
$fileStream = [System.IO.File]::OpenRead($scriptPath)
$hashBytes = $hashAlgorithm.ComputeHash($fileStream)
$fileStream.Close()
$hashAlgorithm.Dispose()

# Convert to hex string (lowercase)
$hashString = ($hashBytes | ForEach-Object { $_.ToString("x2") }) -join ""
Write-Host "   SHA256 hash: $hashString" -ForegroundColor Green

# CheckSumSize: 524288 (block size for verification)
$checkSumSize = 524288

Write-Host ""
Write-Host "2. Updating installer.txt..." -ForegroundColor Yellow

# Read installer.txt
$installerContent = Get-Content $installerPath -Raw -Encoding UTF8 | ConvertFrom-Json

# Update checksums
$installerContent.Scripts[0].Length = $fileSize
$installerContent.Scripts[0].CheckSum = @($hashString)
$installerContent.Scripts[0].CheckSumSize = $checkSumSize

# Remove ExtraFiles section to bypass signature verification
Write-Host "   Removing ExtraFiles section to bypass signature check..." -ForegroundColor Cyan
if ($installerContent.Scripts[0].PSObject.Properties.Name -contains 'ExtraFiles') {
    $installerContent.Scripts[0].PSObject.Properties.Remove('ExtraFiles')
}

# Save updated installer.txt
$installerJson = $installerContent | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText((Resolve-Path $installerPath).Path, $installerJson, [System.Text.Encoding]::UTF8)
Write-Host "   installer.txt updated!" -ForegroundColor Green

Write-Host ""
Write-Host "3. Calculating checksum for installer.txt..." -ForegroundColor Yellow

# Calculate hash for installer.txt
$installerInfo = Get-Item $installerPath
$installerHashAlgorithm = [System.Security.Cryptography.SHA256]::Create()
$installerFileStream = [System.IO.File]::OpenRead($installerPath)
$installerHashBytes = $installerHashAlgorithm.ComputeHash($installerFileStream)
$installerFileStream.Close()
$installerHashAlgorithm.Dispose()
$installerHashString = ($installerHashBytes | ForEach-Object { $_.ToString("x2") }) -join ""
Write-Host "   SHA256 hash installer.txt: $installerHashString" -ForegroundColor Green

Write-Host ""
Write-Host "4. Updating script.module/1.0.0.mnf..." -ForegroundColor Yellow

# Read .mnf file
$mnfContent = Get-Content $mnfPath -Raw -Encoding UTF8 | ConvertFrom-Json

# Update checksums
$mnfContent.HWIndex[0].InstallerFile = "activator_device.script.module_20251204-1914/0/installer.txt"
$mnfContent.HWIndex[0].CheckSum = @($installerHashString)
$mnfContent.HWIndex[0].CheckSumSize = $checkSumSize

# Save updated .mnf file
$mnfJson = $mnfContent | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText((Resolve-Path $mnfPath).Path, $mnfJson, [System.Text.Encoding]::UTF8)
Write-Host "   1.0.0.mnf updated!" -ForegroundColor Green

Write-Host ""
Write-Host "=== DONE ===" -ForegroundColor Green
Write-Host ""
Write-Host "Results:" -ForegroundColor Yellow
Write-Host "  - activation.sh: $hashString" -ForegroundColor Cyan
Write-Host "  - installer.txt: $installerHashString" -ForegroundColor Cyan
Write-Host "  - activation.sh size: $fileSize bytes" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Red
Write-Host "  - ExtraFiles section removed from installer.txt to bypass signature check" -ForegroundColor Yellow
Write-Host "  - If system requires signature, different approach may be needed" -ForegroundColor Yellow
Write-Host ""
