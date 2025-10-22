# Script PowerShell pour pousser le projet vers GitHub
# Projet: Ondocean BLE Positioning KNN
# Auteur: Nicolas Cusseau - ILEMS 2025

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BLE Indoor Positioning KNN - GitHub Push" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si on est dans le bon répertoire
$currentDir = Get-Location
Write-Host "[1/8] Répertoire actuel: $currentDir" -ForegroundColor Yellow

# Vérifier les fichiers essentiels
Write-Host "[2/8] Vérification des fichiers essentiels..." -ForegroundColor Yellow
$essentialFiles = @(
    "localize_me.py",
    "main_qualification.py",
    "requirements.txt",
    "README.md",
    "data\reference\beacon_positions_true.csv"
)

$allFilesPresent = $true
foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MANQUANT!" -ForegroundColor Red
        $allFilesPresent = $false
    }
}

if (-not $allFilesPresent) {
    Write-Host "`n❌ Fichiers manquants! Arrêt du script." -ForegroundColor Red
    exit 1
}

# Initialiser Git si nécessaire
Write-Host "`n[3/8] Initialisation Git..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "  ✓ Repository Git initialisé" -ForegroundColor Green
} else {
    Write-Host "  ✓ Repository Git déjà initialisé" -ForegroundColor Green
}

# Ajouter tous les fichiers
Write-Host "`n[4/8] Ajout des fichiers..." -ForegroundColor Yellow
git add .
Write-Host "  ✓ Fichiers ajoutés" -ForegroundColor Green

# Créer le commit
Write-Host "`n[5/8] Création du commit..." -ForegroundColor Yellow
$commitMessage = @"
feat: BLE Indoor Positioning KNN system with updated beacon positions

- Fingerprinting KNN: 3.7m error (recommended)
- 5 BLE beacons with corrected positions:
  * Balise 60: (-8.35, -0.15) m
  * Balise 25: (3.47, 2.20) m
  * Balise 53: (11.43, 3.54) m
  * Balise 3: (21.46, 2.20) m
  * Balise 38: (25.93, 9.70) m
- 316 RSSI measurements from 3 smartphones
- Interactive localization script (localize_me.py)
- Complete qualification pipeline
- Score: 68/100 - BON
- Zone: Corridor 34.3m × 9.9m
"@

git commit -m $commitMessage
Write-Host "  ✓ Commit créé" -ForegroundColor Green

# Configurer le remote
Write-Host "`n[6/8] Configuration du remote GitHub..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN.git"

# Vérifier si le remote existe déjà
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "  ℹ Remote 'origin' existe déjà: $existingRemote" -ForegroundColor Cyan
    Write-Host "  Voulez-vous le remplacer? (O/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "O" -or $response -eq "o") {
        git remote remove origin
        git remote add origin $remoteUrl
        Write-Host "  ✓ Remote mis à jour" -ForegroundColor Green
    }
} else {
    git remote add origin $remoteUrl
    Write-Host "  ✓ Remote configuré: $remoteUrl" -ForegroundColor Green
}

# Vérifier le remote
Write-Host "`n[7/8] Vérification du remote..." -ForegroundColor Yellow
git remote -v

# Pousser vers GitHub
Write-Host "`n[8/8] Push vers GitHub..." -ForegroundColor Yellow
Write-Host "  ⚠️ Assurez-vous d'avoir configuré votre authentification GitHub!" -ForegroundColor Yellow
Write-Host "  Appuyez sur Entrée pour continuer ou Ctrl+C pour annuler..." -ForegroundColor Cyan
Read-Host

git branch -M main
git push -u origin main

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  ✅ Push terminé avec succès!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nVérifiez votre repository: https://github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN" -ForegroundColor Cyan
Write-Host ""
