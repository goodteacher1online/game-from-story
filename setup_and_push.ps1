Set-Location 'C:\Users\goodt\island-avatar-scene'

# Ensure asset directories exist
New-Item -ItemType Directory -Force -Path 'assets\models' | Out-Null
New-Item -ItemType Directory -Force -Path 'assets\hdr'    | Out-Null

Write-Host "Fetching Island model URL..." -ForegroundColor Cyan
$isoJson = Invoke-RestMethod -Uri 'https://api.poly.pizza/v1/models?search=island&license=CC0' -Method Get
$isoUrl  = $isoJson.results[0].download_url
Write-Host "Island URL: $isoUrl"
Invoke-WebRequest -Uri $isoUrl -OutFile 'assets\models\island.glb' -ErrorAction Stop

Write-Host "Fetching Avatar model URL..." -ForegroundColor Cyan
$avaJson = Invoke-RestMethod -Uri 'https://api.poly.pizza/v1/models?search=human&license=CC0' -Method Get
$avaUrl  = $avaJson.results[0].download_url
Write-Host "Avatar URL: $avaUrl"
Invoke-WebRequest -Uri $avaUrl -OutFile 'assets\models\avatar.glb' -ErrorAction Stop

Write-Host "Downloading HDRI..." -ForegroundColor Cyan
$hdrUrl = 'https://cdn.polyhaven.com/file/ph/royal_esplanade_2k.hdr'
Write-Host "HDRI URL: $hdrUrl"
Invoke-WebRequest -Uri $hdrUrl -OutFile 'assets\hdr\environment.hdr' -ErrorAction Stop

Write-Host "All assets downloaded successfully." -ForegroundColor Green

# Git init if needed
if (-not (Test-Path '.git')) {
    Write-Host "Initializing git repository..." -ForegroundColor Cyan
    git init
    git remote add origin https://github.com/goodteacher1online/island-avatar-scene.git
}

Write-Host "Staging files..." -ForegroundColor Cyan
git add .
Write-Host "Committing changes..." -ForegroundColor Cyan
git commit -m "Add CC0 island, avatar, and HDRI assets"

# Push to GitHub only (dual-push script supports -Remote)
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
& "$env:USERPROFILE\.agents\skills\git-dual-sync\scripts\dual-push.ps1" -Remote origin -Message "Add CC0 assets"
