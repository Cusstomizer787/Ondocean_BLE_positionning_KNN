"""
Localisation en temps réel avec Fingerprinting KNN
Usage: Donnez vos mesures RSSI, obtenez votre position (x, y)
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.parser import BLEDataParser, PositionLoader
from src.fingerprinting import FingerprintDatabase, KNNPositioning
from src.trilateration import fuse_smartphone_measurements

def main():
    print("="*80)
    print("LOCALISATION BLE TEMPS RÉEL - Fingerprinting KNN")
    print("="*80)

    # 1. Charger la base de référence (fingerprint database)
    print("\n[1/3] Chargement de la base de référence...")

    try:
        # Parse Excel data
        parser = BLEDataParser('Geopos indoor BLE.xlsx')
        df_raw = parser.parse_excel()
        df_clean = parser.clean_data(df_raw)

        # Load positions
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

        # Fuse measurements from multiple smartphones (median)
        rssi_fused = fuse_smartphone_measurements(integrator_data, fusion_mode="median")

        # Build fingerprint database
        fp_db = FingerprintDatabase(rssi_fused, measurement_df)
        fp_db.build_database()

        print(f"   [OK] Base chargee: {len(fp_db.fingerprints)} positions de reference")
        print(f"   [OK] Balises disponibles: {sorted(rssi_fused['beacon_id'].unique())}")

        # 2. Initialize KNN
        knn = KNNPositioning(k=3)
        knn.fit(fp_db)

        print("\n[2/3] Modele KNN pret (K=3)")

        # 3. Interactive localization
        print("\n[3/3] LOCALISATION EN TEMPS REEL")
        print("="*80)
        print("\nEntrez vos mesures RSSI pour chaque balise:")
        print("Format: RSSI en dBm (valeurs typiques: 75-95)")
        print("Tapez 'quit' pour quitter\n")

        while True:
            print("-"*80)
            print("NOUVELLE MESURE:")

            # Collect RSSI for each beacon
            rssi_vector = {}

            beacon_ids = sorted(rssi_fused['beacon_id'].unique())
            for beacon_id in beacon_ids:
                while True:
                    try:
                        rssi_input = input(f"  Balise {beacon_id} - RSSI (dBm) [ou 'skip']: ")

                        if rssi_input.lower() == 'quit':
                            print("\nFin de la localisation. Au revoir!")
                            sys.exit(0)

                        if rssi_input.lower() == 'skip':
                            break

                        rssi_val = float(rssi_input)

                        if rssi_val < 50 or rssi_val > 100:
                            print(f"    [WARN] Valeur inhabituelle ({rssi_val} dBm). Continuez? (o/n)")
                            confirm = input("    ")
                            if confirm.lower() != 'o':
                                continue

                        rssi_vector[beacon_id] = rssi_val
                        break

                    except ValueError:
                        print("    [ERROR] Entrez un nombre valide")

            if len(rssi_vector) < 3:
                print("\n[ERROR] Au moins 3 balises requises pour la localisation")
                continue

            # KNN localization
            x_est, y_est = knn.predict_weighted(rssi_vector)

            if np.isnan(x_est):
                print("\n[ERROR] Localisation impossible (pas assez de donnees)")
                continue

            # Display result
            print("\n" + "="*80)
            print("📍 POSITION ESTIMEE:")
            print(f"   X = {x_est:.2f".2f"")
            print(f"   Y = {y_est:.2f".2f"")
            print("="*80)

            # Context information
            print("
Contexte:")
            print("  • Corridor: 0-40.86m (X) × 0-9.80m (Y)"            print("  • Zone test: 11.7-36.9m (X)"            print("  • Lignes: Y=0m (plus loin) et Y=1m (plus pres)")

            if 11.7 <= x_est <= 36.9:
                print("  • ✅ Dans la zone de test"            else:
                print("  • ⚠️ Hors zone de test (extrapolation)"            if y_est < 0.5:
                print("  • Ligne 1 (Y~0m, plus loin des balises)"            elif y_est < 1.5:
                print("  • Ligne 2 (Y~1m, plus pres des balises)"            else:
                print("  • ⚠️ Y inhabituellement eleve"
            print()

    except FileNotFoundError as e:
        print(f"\n[ERROR] Fichier manquant: {e}")
        print("\nAssurez-vous que les fichiers suivants sont presents:")
        print("  - Geopos indoor BLE.xlsx")
        print("  - data/reference/beacon_positions_true.csv")
        print("  - data/reference/measurement_positions_true.csv")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Erreur lors du chargement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
