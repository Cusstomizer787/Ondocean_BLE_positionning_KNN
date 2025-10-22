"""
EXEMPLE D'UTILISATION - Localisation BLE KNN
Demo avec mesures RSSI simulees
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import pandas as pd
import numpy as np
from src.parser import BLEDataParser, PositionLoader
from src.fingerprinting import FingerprintDatabase, KNNPositioning
from src.trilateration import fuse_smartphone_measurements

def main():
    print("="*80)
    print("EXEMPLE - LOCALISATION BLE")
    print("="*80)

    # Load reference database
    print("\nChargement de la base de reference...")
    parser = BLEDataParser('Geopos indoor BLE.xlsx')
    df_clean = parser.clean_data(parser.parse_excel())

    loader = PositionLoader(
        'data/reference/beacon_positions_true.csv',
        'data/reference/measurement_positions_true.csv'
    )
    beacon_df = loader.load_beacons()
    measurement_df = loader.load_measurements()

    # Integrate beacon positions
    integrator_data = df_clean.copy()
    for beacon_id in beacon_df['beacon_id'].values:
        beacon = beacon_df[beacon_df['beacon_id'] == beacon_id]
        if len(beacon) > 0:
            mask = integrator_data['beacon_id'] == beacon_id
            integrator_data.loc[mask, 'x_beacon'] = beacon.iloc[0]['x_meters']
            integrator_data.loc[mask, 'y_beacon'] = beacon.iloc[0]['y_meters']

    rssi_fused = fuse_smartphone_measurements(integrator_data, fusion_mode="median")

    # Build database
    fp_db = FingerprintDatabase(rssi_fused, measurement_df)
    fp_db.build_database()

    # KNN
    knn = KNNPositioning(k=3)
    knn.fit(fp_db)

    print(f"[OK] Base chargee: {len(fp_db.fingerprints)} positions")

    # EXEMPLES DE LOCALISATION
    print("\n" + "="*80)
    print("EXEMPLES DE LOCALISATION")
    print("="*80)

    examples = [
        {
            'name': 'Position debut zone (proche balise 25)',
            'rssi': {'60': 85, '25': 92, '53': 78, '3': 75, '38': 70},
            'expected': '~(12m, 1m)'
        },
        {
            'name': 'Position milieu zone (proche balise 53)',
            'rssi': {'60': 78, '25': 85, '53': 93, '3': 87, '38': 80},
            'expected': '~(22m, 1m)'
        },
        {
            'name': 'Position fin zone (proche balise 3)',
            'rssi': {'60': 72, '25': 80, '53': 85, '3': 91, '38': 88},
            'expected': '~(33m, 1m)'
        },
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   RSSI mesure: {example['rssi']}")

        # Localization
        x_est, y_est = knn.predict_weighted(example['rssi'])

        print(f"   >> Position estimee: ({x_est:.2f}m, {y_est:.2f}m)")
        print(f"   -- Attendu approximativement: {example['expected']}")

    print("\n" + "="*80)
    print("UTILISATION EN TEMPS REEL")
    print("="*80)
    print("""
Pour utiliser en temps reel avec vos propres mesures:

1. Lancez le script interactif:
   python localize_me.py

2. Entrez vos mesures RSSI pour chaque balise
   Exemple:
     Balise 60: 85
     Balise 25: 92
     Balise 53: 78
     ...

3. Le systeme vous donne votre position (X, Y) estimee

NOTES:
- Au moins 3 balises requises
- RSSI typiques: 75-95 dBm
- Precision: ~3.7m en moyenne
- Zone test: 11.7-36.9m (X), 0-1m (Y)
""")

    print("="*80)

if __name__ == "__main__":
    main()
