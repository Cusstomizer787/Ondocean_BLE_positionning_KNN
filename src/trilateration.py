"""Trilateration methods for BLE positioning"""
import pandas as pd
import numpy as np
from typing import Dict

def fuse_smartphone_measurements(df: pd.DataFrame, fusion_mode: str = "median") -> pd.DataFrame:
    """Fuse measurements from multiple smartphones for same position"""
    fused_data = []

    for pos_idx in df['position_idx'].unique():
        pos_data = df[df['position_idx'] == pos_idx]

        for beacon_id in pos_data['beacon_id'].unique():
            beacon_data = pos_data[pos_data['beacon_id'] == beacon_id]

            if len(beacon_data) > 1:
                # Multiple measurements for same position-beacon
                if fusion_mode == "median":
                    fused_rssi = beacon_data['rssi_dbm'].median()
                elif fusion_mode == "mean":
                    fused_rssi = beacon_data['rssi_dbm'].mean()
                else:
                    fused_rssi = beacon_data['rssi_dbm'].iloc[0]  # First value
            else:
                fused_rssi = beacon_data['rssi_dbm'].iloc[0]

            fused_data.append({
                'position_idx': pos_idx,
                'beacon_id': beacon_id,
                'rssi_dbm': fused_rssi,
                'x_beacon': beacon_data['x_beacon'].iloc[0],
                'y_beacon': beacon_data['y_beacon'].iloc[0]
            })

    return pd.DataFrame(fused_data)

def weighted_least_squares_trilateration(distances: Dict, beacon_positions: Dict) -> tuple:
    """Weighted Least Squares trilateration"""
    # Simplified implementation
    # In practice, would implement full WLS algorithm
    return (np.nan, np.nan)  # Placeholder
