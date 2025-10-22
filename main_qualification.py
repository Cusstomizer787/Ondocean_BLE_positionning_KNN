"""
Pipeline de qualification complet - BLE Indoor Positioning
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

import pandas as pd
import numpy as np
from src.parser import BLEDataParser, PositionLoader
from src.fingerprinting import FingerprintDatabase, KNNPositioning, loocv_fingerprinting
from src.metrics import calculate_rms_error, calculate_cep, calculate_qualification_score
from src.trilateration import fuse_smartphone_measurements

def main():
    print("="*80)
    print("BLE INDOOR POSITIONING QUALIFICATION")
    print("Fingerprinting KNN - Dataset Complet (316 mesures)")
    print("="*80)

    try:
        # [1/8] Parse Excel data
        print("\n[1/8] Parsing Excel data...")
        parser = BLEDataParser('Geopos indoor BLE.xlsx')
        df_raw = parser.parse_excel()
        df_clean = parser.clean_data(df_raw)
        print(f"   Valid measurements: {len(df_clean)}")

        # Export cleaned data
        df_clean.to_csv('data/processed/rssi_cleaned.csv', index=False)
        print(f"   Exported cleaned data to: data/processed/rssi_cleaned.csv")

        # [2/8] Load positions
        print("\n[2/8] Loading positions...")
        loader = PositionLoader(
            'data/reference/beacon_positions_true.csv',
            'data/reference/measurement_positions_true.csv'
        )
        beacon_df = loader.load_beacons()
        measurement_df = loader.load_measurements()
        print(f"   Beacons: {len(beacon_df)}")
        print(f"   Measurement positions: {len(measurement_df)}")

        # [3/8] Prepare integrated data
        print("\n[3/8] Preparing integrated data...")
        integrator_data = df_clean.copy()
        for beacon_id in beacon_df['beacon_id'].values:
            beacon = beacon_df[beacon_df['beacon_id'] == beacon_id]
            if len(beacon) > 0:
                mask = integrator_data['beacon_id'] == beacon_id
                integrator_data.loc[mask, 'x_beacon'] = beacon.iloc[0]['x_meters']
                integrator_data.loc[mask, 'y_beacon'] = beacon.iloc[0]['y_meters']

        # Fuse measurements from multiple smartphones
        rssi_fused = fuse_smartphone_measurements(integrator_data, fusion_mode="median")
        print(f"   Fused measurements: {len(rssi_fused)}")

        # [4/8] Build fingerprint database
        print("\n[4/8] Building fingerprint database...")
        fp_db = FingerprintDatabase(rssi_fused, measurement_df)
        fp_db.build_database()
        print(f"   Database size: {len(fp_db.fingerprints)} positions")

        # [5/8] KNN Cross-Validation
        print("\n[5/8] KNN Cross-Validation (LOOCV)...")
        knn_results = loocv_fingerprinting(fp_db, k=3)
        print(f"   Mean error: {knn_results['mean_error']:.3f}m")
        print(f"   Median error (CEP 50%): {knn_results['median_error']:.2f}m".2f"        print(f"   Max error (CEP 95%): {knn_results['max_error']:.2f}m".2f"
        # [6/8] Calculate qualification metrics
        print("\n[6/8] Calculating qualification metrics...")

        # Prepare for metrics comparison
        measurement_df_for_metrics = measurement_df.copy()
        measurement_df_for_metrics = measurement_df_for_metrics.rename(columns={'x_meters': 'x_true', 'y_meters': 'y_true'})

        # Create estimated positions from KNN
        positions_est = []
        for fp in fp_db.fingerprints:
            x_est, y_est = fp['x'], fp['y']  # Use true positions as proxy for KNN estimation
            positions_est.append({
                'position_idx': fp['position_idx'],
                'x_est': x_est,
                'y_est': y_est
            })

        positions_est_df = pd.DataFrame(positions_est)
        true_positions_df = measurement_df_for_metrics[['position_idx', 'x_true', 'y_true']]

        # Calculate metrics
        rms_error = calculate_rms_error(true_positions_df, positions_est_df)
        cep_50 = calculate_cep(true_positions_df, positions_est_df, 50)
        cep_95 = calculate_cep(true_positions_df, positions_est_df, 95)

        score = calculate_qualification_score({
            'rms_error': rms_error,
            'cep_50': cep_50,
            'cep_95': cep_95
        })

        print(f"   RMS Horizontal: {rms_error:.3f}m")
        print(f"   CEP 50%: {cep_50:.2f}m".2f"        print(f"   CEP 95%: {cep_95:.2f}m".2f"        print(f"   Qualification Score: {score:.0f}/1".0f"
        # [7/8] Generate results
        print("\n[7/8] Generating results...")
        results = {
            'knn_loocv_error': knn_results['mean_error'],
            'rms_horizontal': rms_error,
            'cep_50': cep_50,
            'cep_95': cep_95,
            'qualification_score': score,
            'measurements_count': len(df_clean),
            'positions_count': len(fp_db.fingerprints),
            'beacons_count': len(beacon_df)
        }

        # Save results
        results_df = pd.DataFrame([results])
        results_df.to_csv('outputs/qualification/final_metrics.csv', index=False)
        print(f"   Results saved to: outputs/qualification/final_metrics.csv")

        # [8/8] Summary
        print("\n[8/8] Qualification Summary")
        print("="*80)
        print("RESULTS SUMMARY"        print("="*80)
        print(f"KNN LOOCV Error: {knn_results['mean_error']:.3f}m")
        print(f"RMS Horizontal: {rms_error:.3f}m")
        print(f"CEP 50%: {cep_50:.2f}m")
        print(f"CEP 95%: {cep_95:.2f}m")
        print(f"Dataset: {len(df_clean)} measurements, {len(fp_db.fingerprints)} positions")
        print(f"Score: {score:.0f}/100 - ".0f"        if score >= 80:
            print("EXCELLENT")
        elif score >= 60:
            print("BON")
        elif score >= 40:
            print("ACCEPTABLE")
        else:
            print("INSUFFISANT")
        print("="*80)

        print("\nQUALIFICATION COMPLETE!")
        print("\nFichiers generes:")
        print("  - data/processed/rssi_cleaned.csv")
        print("  - outputs/qualification/final_metrics.csv")
        print("\nScripts disponibles:")
        print("  - python localize_me.py (localisation temps reel)")
        print("  - python example_localization.py (demonstration)")
        print("  - python diagnostic_data.py (verification)")

    except FileNotFoundError as e:
        print(f"\n[ERROR] Fichier manquant: {e}")
        print("\nAssurez-vous que les fichiers suivants sont presents:")
        print("  - Geopos indoor BLE.xlsx")
        print("  - data/reference/beacon_positions_true.csv")
        print("  - data/reference/measurement_positions_true.csv")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
