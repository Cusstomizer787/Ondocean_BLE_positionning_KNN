# BLE Indoor Positioning - Fingerprinting KNN

**Système de localisation BLE indoor par Machine Learning**  
**Précision: 3.7m d'erreur moyenne | Score: 68/100 - BON**

![KNN Localization](https://img.shields.io/badge/KNN-3.7m%20error-brightgreen)
![BLE Beacons](https://img.shields.io/badge/5%20Beacons-26%20Positions-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

---

## 🎯 Utilisation Rapide

### Localisation en Temps Réel
```bash
python localize_me.py
```

### Qualification Complète
```bash
python main_qualification.py
```

### Exemples Démo
```bash
python example_localization.py
```

---

## 📊 Résultats

| Méthode | Erreur Moyenne | Performance |
|---------|----------------|-------------|
| **Fingerprinting KNN** | **3.7m** | ⭐⭐⭐ Recommandé |
| Trilatération WLS | 12.7m | ⚠️ Sous-optimal |

**Dataset:** 316 mesures RSSI, 3 smartphones, 5 balises BLE  
**Zone:** Corridor 34.3m × 9.9m, 26 positions test

---

## 🚀 Installation

```bash
# Clone le repository
git clone https://github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN.git
cd Ondocean_BLE_positionning_KNN

# Installe les dépendances
pip install -r requirements.txt

# Lance la qualification complète
python main_qualification.py
```

---

## 🏗️ Structure du Projet

```
Ondocean_BLE_positionning_KNN/
├── 📄 README.md                    # Documentation principale
├── 📋 localize_me.py              # 🎯 Localisation temps réel
├── 🔬 main_qualification.py       # Pipeline qualification
├── 📝 example_localization.py     # Exemples démo
├── 📊 diagnostic_data.py          # Validation dataset
├── ⚙️ requirements.txt            # Dépendances Python
├── 📁 src/                        # Modules Python
│   ├── parser.py                  # Parse Excel + forward-fill
│   ├── fingerprinting.py         # KNN ML (recommandé)
│   ├── trilateration.py          # WLS (sous-optimal)
│   ├── path_loss.py              # ITU Indoor (inadapté)
│   └── metrics.py                # RMS/CEP/Score
├── 📁 data/                       # Données de référence
│   ├── reference/
│   │   ├── beacon_positions_true.csv        # 5 balises
│   │   └── measurement_positions_true.csv   # 26 positions
│   └── processed/
│       └── rssi_cleaned.csv                 # 316 mesures
├── 📁 outputs/                    # Résultats
│   └── qualification/
│       └── final_metrics.csv
└── 📁 docs/                       # Documentation
    ├── RAPPORT_FINAL_COMPARATIF.md
    └── GUIDE_UTILISATION.md
```

---

## 🎓 Description du Système

### Principe de Fonctionnement

Le système utilise le **Fingerprinting KNN (K-Nearest Neighbors)** pour localiser un utilisateur dans un environnement indoor basé sur les signaux BLE de 5 balises.

1. **Phase d'entraînement:** Collecte de 316 mesures RSSI à 26 positions connues
2. **Base de référence:** Chaque position = empreinte RSSI des 5 balises
3. **Localisation temps réel:** Trouve les 3 positions les plus similaires (K=3)
4. **Estimation:** Moyenne pondérée des positions candidates

### Configuration Balises
| Balise | X (m) | Y (m) | Position |
|--------|-------|-------|----------|
| 60 | -8.35 | -0.15 | Origine corridor |
| 25 | 3.47 | 2.20 | Début zone test |
| 53 | 11.43 | 3.54 | Centre corridor |
| 3 | 21.46 | 2.20 | Fin zone test |
| 38 | 25.93 | 9.70 | Extrémité corridor |

**Zone de test:** Corridor 34.3m × 9.9m

---

## 💡 Utilisation

### 1. Localisation Interactive
```bash
python localize_me.py
```
Entrez vos mesures RSSI pour chaque balise et obtenez votre position.

### 2. Code Python
```python
from src.fingerprinting import KNNPositioning

# Charger le modèle
knn = KNNPositioning(k=3)
# ... (voir localize_me.py pour code complet)

# Mesurer RSSI
rssi = {'60': 85, '25': 92, '53': 78, '3': 75, '38': 70}

# Localiser
x, y = knn.predict_weighted(rssi)
print(f"Position: ({x:.2f}m, {y:.2f}m)")
```

### 3. Validation
```bash
python diagnostic_data.py  # Vérifier les 316 mesures
```

---

## 📈 Performance

### Métriques de Qualification
- **KNN LOOCV Error:** 3.694m (méthode optimale)
- **CEP 50%:** 10.41m
- **CEP 95%:** 19.76m
- **Score Qualification:** 68/100 - BON

### Comparaison Méthodes
| Version | Dataset | KNN Error | Score |
|---------|---------|-----------|-------|
| V1 | 128 mesures | 4.4m | 58/100 |
| V2 | 128 mesures | 7.3m | 58/100 |
| **V3** | **316 mesures** | **3.7m** | **68/100** |

---

## 🔧 Configuration Requise

- **Python:** 3.8+
- **Dépendances:** pandas, numpy, scipy, openpyxl, pyyaml, matplotlib
- **Données:** Inclues dans le repository
- **Hardware:** Compatible avec n'importe quel récepteur BLE

---

## 📚 Documentation

- **[GUIDE_UTILISATION.md](docs/GUIDE_UTILISATION.md)** - Guide utilisateur complet
- **[RAPPORT_FINAL_COMPARATIF.md](docs/RAPPORT_FINAL_COMPARATIF.md)** - Rapport technique détaillé

---

## 🎯 Cas d'Usage

### ✅ Recommandé Pour
- Navigation indoor approximative
- Détection de zone/pièce
- Tracking trajectoire
- Validation positionnement BLE

### ❌ Non Adapté Pour
- Précision centimétrique (<1m)
- Applications critiques sécurité
- Navigation robotique haute précision

---

## 🔬 Contexte Projet

**Projet:** Mastère Spécialisé ILEMS 2025 - Qualification BLE Indoor  
**Auteur:** Nicolas Cusseau  
**Date:** Octobre 2025  
**Version:** 2.0 - Dataset Complet

---

## 📞 Support

Pour toute question sur l'utilisation ou l'implémentation, consultez:
1. **GUIDE_UTILISATION.md** - Mode d'emploi détaillé
2. **localize_me.py** - Code source commenté
3. **Issues GitHub** - Questions et support

---

**Projet validé ✅** - Framework BLE indoor positioning opérationnel  
**Méthode recommandée:** Fingerprinting KNN (K=3)  
**Précision:** 3.7m d'erreur moyenne

---

## 📞 Push vers GitHub

```bash
# 1. Aller dans le répertoire
cd C:\Users\ncuss\Documents\GitHub\Ondocean_BLE_positionning_KNN

# 2. Initialiser Git (si pas déjà fait)
git init
git add .
git commit -m "Initial commit: BLE Indoor Positioning KNN system"

# 3. Configurer le remote (remplacer par votre token)
git remote add origin https://github.com/Cusstomizer787/Ondocean_BLE_positionning_KNN.git

# 4. Pousser vers GitHub
git branch -M main
git push -u origin main
```

## 🔧 Tests

```bash
# Vérifier le dataset
python diagnostic_data.py

# Lancer la qualification complète
python main_qualification.py

# Tester les exemples
python example_localization.py

# Localisation interactive
python localize_me.py
```

## 📚 Documentation

- **[README.md](README.md)** - Documentation principale
- **[docs/GUIDE_UTILISATION.md](docs/GUIDE_UTILISATION.md)** - Guide utilisateur
- **[docs/RAPPORT_FINAL_COMPARATIF.md](docs/RAPPORT_FINAL_COMPARATIF.md)** - Rapport technique

---

**Projet:** Mastère Spécialisé ILEMS 2025 - BLE Indoor Positioning Qualification
**Auteur:** Nicolas Cusseau
**Version:** 2.0 - Dataset Complet (316 mesures)
**Licence:** MIT

**🎯 Prêt pour GitHub!**
