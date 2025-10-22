# Guide de Push vers GitHub

## 📋 Prérequis

✅ **Fichiers mis à jour:**
- Positions des balises corrigées dans `data/reference/beacon_positions_true.csv`
- README.md mis à jour avec nouvelles positions
- Tous les scripts Python essentiels présents

## 🚀 Étapes de Push

### 1. Vérifier le contenu du projet

```bash
cd C:\Users\ncuss\Documents\GitHub\Ondocean_BLE_positionning_KNN
dir
```

**Fichiers essentiels à vérifier:**
- ✅ `localize_me.py` - Script principal de localisation
- ✅ `main_qualification.py` - Pipeline de qualification
- ✅ `requirements.txt` - Dépendances Python
- ✅ `README.md` - Documentation
- ✅ `src/` - Modules Python (parser, fingerprinting, etc.)
- ✅ `data/reference/` - Positions des balises et mesures
- ✅ `Geopos indoor BLE.xlsx` - Données RSSI

### 2. Initialiser Git (si pas déjà fait)

```bash
git init
```

### 3. Configurer .gitignore (déjà présent)

Le fichier `.gitignore` exclut:
- `__pycache__/`
- `*.pyc`
- `outputs/`
- `.vscode/`
- etc.

### 4. Ajouter tous les fichiers

```bash
git add .
```

### 5. Créer le commit initial

```bash
git commit -m "feat: BLE Indoor Positioning KNN system with updated beacon positions

- Fingerprinting KNN: 3.7m error (recommended)
- 5 BLE beacons with corrected positions
- 316 RSSI measurements from 3 smartphones
- Interactive localization script (localize_me.py)
- Complete qualification pipeline
- Score: 68/100 - BON"
```

### 6. Configurer le remote GitHub

```bash
git remote add origin https://github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN.git
```

### 7. Vérifier le remote

```bash
git remote -v
```

### 8. Pousser vers GitHub

```bash
git branch -M main
git push -u origin main
```

## 🔐 Authentification GitHub

Si vous utilisez un token personnel:

```bash
# Format: https://<TOKEN>@github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN.git
git remote set-url origin https://<VOTRE_TOKEN>@github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN.git
git push -u origin main
```

## ✅ Vérification Post-Push

Après le push, vérifiez sur GitHub:
1. **README.md** s'affiche correctement
2. **Positions des balises** sont à jour dans `data/reference/beacon_positions_true.csv`
3. **Scripts Python** sont présents et lisibles
4. **Structure du projet** est complète

## 📊 Nouvelles Positions des Balises

| Balise | X (m) | Y (m) | Position |
|--------|-------|-------|----------|
| 60 | -8.35 | -0.15 | Origine corridor |
| 25 | 3.47 | 2.20 | Début zone test |
| 53 | 11.43 | 3.54 | Centre corridor |
| 3 | 21.46 | 2.20 | Fin zone test |
| 38 | 25.93 | 9.70 | Extrémité corridor |

**Zone:** Corridor 34.3m × 9.9m

## 🎯 Commandes Rapides

```bash
# Tout en une fois
cd C:\Users\ncuss\Documents\GitHub\Ondocean_BLE_positionning_KNN
git init
git add .
git commit -m "feat: BLE Indoor Positioning KNN system with updated beacon positions"
git remote add origin https://github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN.git
git branch -M main
git push -u origin main
```

## 📝 Notes

- **Projet:** Mastère Spécialisé ILEMS 2025
- **Auteur:** Nicolas Cusseau
- **Version:** 2.0 - Dataset Complet (316 mesures)
- **Méthode recommandée:** Fingerprinting KNN (K=3)
- **Précision:** 3.7m d'erreur moyenne

---

**🎯 Prêt pour GitHub!**
