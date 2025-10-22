"""Fingerprinting ML for BLE positioning"""
import numpy as np
import pandas as pd
from typing import Dict, Tuple

class FingerprintDatabase:
    def __init__(self, rssi_df: pd.DataFrame, positions: pd.DataFrame):
        self.rssi_df = rssi_df
        self.positions = positions
        self.fingerprints = []

    def build_database(self):
        for pos_idx in self.rssi_df['position_idx'].unique():
            pos_data = self.rssi_df[self.rssi_df['position_idx'] == pos_idx]
            rssi_vector = pos_data.set_index('beacon_id')['rssi_dbm'].to_dict()
            pos = self.positions[self.positions.index == pos_idx]
            if len(pos) > 0:
                self.fingerprints.append({
                    'position_idx': pos_idx,
                    'rssi_vector': rssi_vector,
                    'x': pos.iloc[0]['x_meters'],
                    'y': pos.iloc[0]['y_meters']
                })

class KNNPositioning:
    def __init__(self, k: int = 3):
        self.k = k
        self.database = None

    def fit(self, fingerprint_db):
        self.database = fingerprint_db.fingerprints

    def predict_weighted(self, rssi_vector: dict) -> Tuple[float, float]:
        if not self.database:
            return (np.nan, np.nan)

        distances = []
        for fp in self.database:
            # Euclidean distance in RSSI space
            common_beacons = set(rssi_vector.keys()) & set(fp['rssi_vector'].keys())
            if len(common_beacons) < 3:
                continue
            d = np.sqrt(sum((rssi_vector[b] - fp['rssi_vector'][b])**2 for b in common_beacons))
            distances.append((d, fp['x'], fp['y']))

        if len(distances) < self.k:
            return (np.nan, np.nan)

        distances.sort(key=lambda x: x[0])
        k_nearest = distances[:self.k]

        # Weighted average
        weights = [1.0 / (d[0] + 0.01) for d in k_nearest]
        total_w = sum(weights)
        x_est = sum(w * p[1] for w, p in zip(weights, k_nearest)) / total_w
        y_est = sum(w * p[2] for w, p in zip(weights, k_nearest)) / total_w

        return (x_est, y_est)

def loocv_fingerprinting(fp_db, k: int = 3) -> Dict:
    errors = []
    for i, test_fp in enumerate(fp_db.fingerprints):
        train_db = [fp for j, fp in enumerate(fp_db.fingerprints) if j != i]
        knn = KNNPositioning(k=k)
        knn.database = train_db
        x_est, y_est = knn.predict_weighted(test_fp['rssi_vector'])
        if not np.isnan(x_est):
            error = np.sqrt((x_est - test_fp['x'])**2 + (y_est - test_fp['y'])**2)
            errors.append(error)

    return {
        'mean_error': np.mean(errors) if errors else np.inf,
        'median_error': np.median(errors) if errors else np.inf,
        'max_error': np.max(errors) if errors else np.inf,
        'errors_list': errors
    }
