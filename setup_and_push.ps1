Set-Location 'C:\Users\goodt\game-from-story'

# Ensure asset directories exist
New-Item -ItemType Directory -Force -Path 'assets\models' | Out-Null
New-Item -ItemType Directory -Force -Path 'assets\hdr'    | Out-Null

Write-Host "Downloading Island model..." -ForegroundColor Cyan
$isoUrl = 'https://raw.githubusercontent.com/greenMakaroni/three-floating-island/master/src/components/Landing/island.glb'
Write-Host "Island URL: $isoUrl"
if (-not (Test-Path 'assets\models\island.glb') -or (Get-Item 'assets\models\island.glb').Length -eq 0) {
    Invoke-WebRequest -Uri $isoUrl -OutFile 'assets\models\island.glb' -ErrorAction Stop
}

Write-Host "Downloading Avatar model..." -ForegroundColor Cyan
$avaUrl = 'https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/models/gltf/Xbot.glb'
Write-Host "Avatar URL: $avaUrl"
if (-not (Test-Path 'assets\models\avatar.glb') -or (Get-Item 'assets\models\avatar.glb').Length -eq 0) {
    Invoke-WebRequest -Uri $avaUrl -OutFile 'assets\models\avatar.glb' -ErrorAction Stop
}

Write-Host "Downloading HDRI..." -ForegroundColor Cyan
$hdrUrl = 'https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/royal_esplanade_1k.hdr'
Write-Host "HDRI URL: $hdrUrl"
if (-not (Test-Path 'assets\hdr\environment.hdr') -or (Get-Item 'assets\hdr\environment.hdr').Length -eq 0) {
    Invoke-WebRequest -Uri $hdrUrl -OutFile 'assets\hdr\environment.hdr' -ErrorAction Stop
}

Write-Host "All assets downloaded successfully." -ForegroundColor Green

# Git init if needed
if (-not (Test-Path '.git')) {
    Write-Host "Initializing git repository..." -ForegroundColor Cyan
    git init
    git branch -M main
    git remote add origin https://github.com/goodteacher1online/game-from-story.git
}

Write-Host "Staging files..." -ForegroundColor Cyan
git add .

Write-Host "Pushing via dual-push.ps1..." -ForegroundColor Cyan
& "$env:USERPROFILE\.agents\skills\git-dual-sync\scripts\dual-push.ps1" -Remote origin -Branch main -Message "Add CC0 island, avatar, and HDRI assets"
