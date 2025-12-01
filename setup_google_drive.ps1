#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Setup rclone for Google Drive integration with GitHub/GitLab Actions

.DESCRIPTION
    This script helps you configure rclone to work with your Google Drive account.
    It will generate a token that you'll add as a secret to GitHub/GitLab.

.NOTES
    Your Google Account: s8001145@gmail.com
#>

Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║     🔧 Google Drive Setup for Ollama Models Downloader       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "`n📋 This script will help you:
1. Install rclone (if needed)
2. Configure Google Drive connection
3. Generate token for GitHub/GitLab Actions
4. Testxxxxxxxxxxction
`n" -ForegroundColor Yellow

# Step 1: Check if rclone is installed
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Step 1: Checking rclone installation..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$rcloneInstalled = $false
try {
    $version = rclone version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ rclone is already installed!" -ForegroundColor Green
        Write-Host $version[0] -ForegroundColor Gray
        $rcloneInstalled = $true
    }
} catch {
    # Not installed
}

if (-not $rcloneInstalled) {
    Write-Host "❌ rclone is not installed" -ForegroundColor Red
    Write-Host "`n📥 Installing rclone..." -ForegroundColor Yellow
    
    $installChoice = Read-Host "`nInstall rclone now? (y/n)"
    if ($installChoice -eq 'y') {
        try {
            # Try winget first
            Write-Host "Installing via winget..." -ForegroundColor Cyan
            winget install Rclone.Rclone
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ rclone installed successfully!" -ForegroundColor Green
                Write-Host "⚠️  Please restart PowerShell and run this script again." -ForegroundColor Yellow
                exit 0
            }
        } catch {
            Write-Host "❌ winget installation failed" -ForegroundColor Red
            Write-Host "`n📥 Alternative: Download manually from https://rclone.org/downloads/" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "❌ rclone is required. Please install it and run this script again." -ForegroundColor Red
        Write-Host "Download from: https://rclone.org/downloads/" -ForegroundColor Cyan
        exit 1
    }
}

# Step 2: Configure Google Drive
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Step 2: Configure Google Drive connection..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$remoteName = "gdrive-ollama"

# Check if remote already exists
$existingRemotes = rclone listremotes 2>$null
if ($existingRemotes -match "$remoteName") {
    Write-Host "⚠️  Remote '$remoteName' already exists" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to reconfigure it? (y/n)"
    if ($overwrite -ne 'y') {
        Write-Host "Using existing configuration..." -ForegroundColor Green
    } else {
        rclone config delete $remoteName 2>$null
    }
}

if (-not ($existingRemotes -match "$remoteName") -or $overwrite -eq 'y') {
    Write-Host "`n📝 Starting interactive configuration..." -ForegroundColor Yellow
    Write-Host @"

╔════════════════════════════════════════════════════════════════╗
║  INSTRUCTIONS FOR RCLONE CONFIGURATION:                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  1. When asked 'name>', type: $remoteName                      ║
║  2. When asked 'Storage>', type: drive (or number for drive)  ║
║  3. For 'client_id>', press Enter (leave blank)               ║
║  4. For 'client_secret>', press Enter (leave blank)           ║
║  5. For 'scope>', choose: 1 (Full access)                     ║
║  6. For 'service_account_file>', press Enter                  ║
║  7. For 'Edit advanced config?', type: n                      ║
║  8. For 'Use web browser?', type: y                           ║
║  9. Browser will open - login with: s8001145@gmail.com        ║
║  10. Click 'Allow' to grant access                            ║
║  11. Return to terminal and press Enter                       ║
║  12. For 'Configure as team drive?', type: n                  ║
║  13. Confirm with: y                                          ║
║  14. Then type: q (to quit)                                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

    $ready = Read-Host "Ready to start configuration? (y/n)"
    if ($ready -ne 'y') {
        Write-Host "❌ Configuration cancelled" -ForegroundColor Red
        exit 1
    }

    rclone config
}

# Step 3: Test connection
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Step 3: Testing Google Drive connection..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

Write-Host "`n🔍 Listing files in your Google Drive root..." -ForegroundColor Yellow
$testResult = rclone lsd "${remoteName}:" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Connection successful!" -ForegroundColor Green
    Write-Host "`nYour Google Drive folders:" -ForegroundColor Cyan
    Write-Host $testResult
} else {
    Write-Host "❌ Connection failed!" -ForegroundColor Red
    Write-Host $testResult -ForegroundColor Red
    exit 1
}

# Step 4: Extract token for GitHub/GitLab
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Step 4: Extracting token for GitHub/GitLab Actions..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$configPath = "$env:USERPROFILE\.config\rclone\rclone.conf"
if (-not (Test-Path $configPath)) {
    $configPath = "$env:APPDATA\rclone\rclone.conf"
}

if (Test-Path $configPath) {
    Write-Host "📄 Reading rclone config from: $configPath" -ForegroundColor Gray
    
    $config = Get-Content $configPath -Raw
    
    # Extract the full remote config
    $remoteConfig = $config -match "(?s)\[$remoteName\](.*?)(?=\n\[|\z)"
    if ($matches) {
        $remoteSection = $matches[0]
        
        # Save to file for GitHub/GitLab secrets
        $secretFile = ".\rclone_gdrive_config.txt"
        $remoteSection | Out-File -FilePath $secretFile -Encoding UTF8
        
        Write-Host "`n✅ Configuration exported!" -ForegroundColor Green
        Write-Host "📁 Saved to: $secretFile" -ForegroundColor Cyan
        
        Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
        Write-Host "║  NEXT STEPS - ADD TO GITHUB/GITLAB SECRETS:                   ║" -ForegroundColor Yellow
        Write-Host "╠════════════════════════════════════════════════════════════════╣" -ForegroundColor Yellow
        Write-Host "║                                                                ║" -ForegroundColor Yellow
        Write-Host "║  FOR GITHUB:                                                   ║" -ForegroundColor Yellow
        Write-Host "║  1. Go to: https://github.com/sumca1/ollama-downloader/       ║" -ForegroundColor Yellow
        Write-Host "║            settings/secrets/actions                            ║" -ForegroundColor Yellow
        Write-Host "║  2. Click 'New repository secret'                              ║" -ForegroundColor Yellow
        Write-Host "║  3. Name: RCLONE_CONFIG                                        ║" -ForegroundColor Yellow
        Write-Host "║  4. Value: Copy content from $secretFile  ║" -ForegroundColor Yellow
        Write-Host "║  5. Click 'Add secret'                                         ║" -ForegroundColor Yellow
        Write-Host "║                                                                ║" -ForegroundColor Yellow
        Write-Host "║  FOR GITLAB:                                                   ║" -ForegroundColor Yellow
        Write-Host "║  1. Go to: https://gitlab.com/sumca1/                          ║" -ForegroundColor Yellow
        Write-Host "║            ollama-models-downloader/-/settings/ci_cd           ║" -ForegroundColor Yellow
        Write-Host "║  2. Expand 'Variables' section                                 ║" -ForegroundColor Yellow
        Write-Host "║  3. Click 'Add variable'                                       ║" -ForegroundColor Yellow
        Write-Host "║  4. Key: RCLONE_CONFIG                                         ║" -ForegroundColor Yellow
        Write-Host "║  5. Value: Copy content from $secretFile  ║" -ForegroundColor Yellow
        Write-Host "║  6. Uncheck 'Protect variable'                                 ║" -ForegroundColor Yellow
        Write-Host "║  7. Check 'Mask variable'                                      ║" -ForegroundColor Yellow
        Write-Host "║  8. Click 'Add variable'                                       ║" -ForegroundColor Yellow
        Write-Host "║                                                                ║" -ForegroundColor Yellow
        Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
        
        Write-Host "`n📋 Opening the config file for you to copy..." -ForegroundColor Cyan
        Start-Sleep -Seconds 2
        notepad $secretFile
        
    } else {
        Write-Host "❌ Could not find remote '$remoteName' in config" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ rclone config file not found at: $configPath" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "📝 Don't forget to add the secret to GitHub/GitLab!" -ForegroundColor Yellow
Write-Host "`n🚀 After adding the secret, you can run the workflow and files will upload to your Google Drive!" -ForegroundColor Cyan
