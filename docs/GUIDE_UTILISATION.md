# GUIDE D'UTILISATION - Localisation BLE Indoor

**Système de positionnement BLE par Fingerprinting KNN**
**Précision: 3.7m d'erreur moyenne**

---

## Principe de Fonctionnement

### 1. Base de Référence (Fingerprint Database)
Le système a été entraîné avec **316 mesures RSSI** collectées à **26 positions connues** (11.7-36.9m en X, Y=0m ou 1m).

Pour chaque position de référence, on a enregistré les RSSI des **5 balises BLE**:
- Balise 60 à (0.00, 0.00)m
- Balise 25 à (11.70, 2.20)m
- Balise 53 à (22.85, 3.67)m
- Balise 3 à (32.89, 2.20)m
- Balise 38 à (40.86, 9.80)m

### 2. Localisation en Temps Réel
Lorsque vous donnez vos mesures RSSI actuelles, le système:

1. **Calcule la distance** entre votre vecteur RSSI et chaque position de référence
2. **Trouve les K=3 positions** les plus proches dans l'espace RSSI
3. **Moyenne pondérée** des positions (poids = 1/distance)
4. **Retourne votre position** estimée (X, Y)

---

## Utilisation Simple

### Méthode 1: Script Interactif

```bash
python localize_me.py
```

Le script vous demande vos mesures RSSI:

```
Balise 60 - RSSI (dBm): 85
Balise 25 - RSSI (dBm): 92
Balise 53 - RSSI (dBm): 78
Balise 3 - RSSI (dBm): 75
Balise 38 - RSSI (dBm): 70

📍 POSITION ESTIMÉE:
   X = 12.45 m
   Y = 0.85 m
```

### Méthode 2: Exemple Démo

```bash
python example_localization.py
```

Montre 3 exemples de localisation avec RSSI simulés.

---

## Utilisation Avancée (Code Python)

### Intégration dans votre application

```python
from src.fingerprinting import FingerprintDatabase, KNNPositioning
import pandas as pd

# 1. Charger la base de référence (une fois au démarrage)
# ... (voir localize_me.py pour le code complet)

# 2. Initialiser KNN
knn = KNNPositioning(k=3)
knn.fit(fingerprint_database)

# 3. Mesurer RSSI en temps réel
rssi_current = {
    '60': 85.0,  # RSSI balise 60 (dBm)
    '25': 92.0,  # RSSI balise 25
    '53': 78.0,  # RSSI balise 53
    '3': 75.0,   # RSSI balise 3
    '38': 70.0   # RSSI balise 38
}

# 4. Estimer position
x_est, y_est = knn.predict_weighted(rssi_current)

print(f"Position: ({x_est:.2f}m, {y_est:.2f}m)")
```

---

## Conseils pour de Bonnes Mesures

### RSSI Typiques
- **Fort signal:** 90-95 dBm (proche de la balise)
- **Signal moyen:** 80-90 dBm (distance moyenne)
- **Signal faible:** 70-80 dBm (loin de la balise)
- **Très faible:** <70 dBm (limite de portée)

### Qualité des Mesures
1. **Stationnaire:** Ne bougez pas pendant la mesure (10-30s)
2. **Moyenne:** Faites la moyenne de plusieurs scans RSSI
3. **Minimum 3 balises:** Pour une localisation fiable
4. **Évitez obstacles:** Restez en vue des balises si possible

### Gestion des Erreurs
- Si RSSI < 60 dBm: balise probablement hors portée (skip)
- Si toutes balises faibles: vous êtes hors zone de test
- Si NaN retourné: pas assez de balises détectées

---

## Limites et Performance

### Précision Attendue
- **Moyenne:** 3.7m d'erreur (LOOCV)
- **Médiane (CEP 50%):** 10.4m
- **95% des cas (CEP 95%):** <19.8m

### Zone de Validité
- **X:** 11.7 → 36.9m (zone test)
- **Y:** 0 → 1m (2 lignes de mesure)
- **Hors zone:** Extrapolation (précision dégradée)

### Facteurs d'Erreur
- **Multi-trajets:** Réflexions sur murs/mobilier
- **Masquage:** Obstruction ligne de vue
- **RSSI drift:** Variations temporelles du signal
- **Smartphone:** Antenne BLE différente selon modèle

---

## Cas d'Usage

### ✅ Recommandé Pour
- Navigation indoor approximative (précision ~4m)
- Zone-based localization (quelle salle/zone)
- Tracking trajectoire générale
- Détection présence/mouvement

### ❌ Non Recommandé Pour
- Précision centimétrique (<1m)
- Applications critiques sécurité
- Navigation robotique précise
- Mesures métrologique

---

## Amélioration Possible

### Pour Précision <2m
1. **Plus de positions training:** 50-100 (vs 26 actuel)
2. **Dense sampling:** Espacement <1m (vs 2.1m)
3. **Weighted KNN:** Optimiser poids
4. **Features avancées:** Variance RSSI, ratios, gradients
5. **ML avancé:** Random Forest, XGBoost, Neural Networks

### Maintenance
- **Recalibration:** Tous les 1-3 mois (RSSI drift)
- **Validation:** LOOCV après chaque update
- **Monitoring:** Logger erreur en temps réel

---

## Support et Contact

**Projet:** Mastère Spécialisé ILEMS 2025
**Auteur:** Nicolas Cusseau
**Version:** 2.0 (316 mesures, 26 positions)

**Fichiers:**
- `localize_me.py` - Localisation interactive
- `example_localization.py` - Exemples démo
- `RAPPORT_FINAL_COMPARATIF.md` - Rapport technique complet

**Méthode validée:** Fingerprinting KNN (K=3)
**Score qualification:** 68/100 - BON
