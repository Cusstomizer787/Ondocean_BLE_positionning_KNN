"""
BLE Data Parser - Parse Excel RSSI measurements and integrate with positions
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict


def decode_position_hex(col_idx: int) -> str:
    """Convert Excel column index to position code (11-1D or 21-2D)

    Args:
        col_idx: Column index from Excel (0-12 for first 13, 13-25 for next 13)

    Returns:
        Position code like '11', '1A', '21', '2D'
    """
    # Map column index to hex position codes
    # Columns 2-14 in Excel (indices 0-12) map to both line 1 and line 2
    # depending on which smartphone

    if col_idx <= 12:
        # First 13 positions
        hex_suffix = hex(col_idx + 1)[2:].upper()  # 1-D
        return f"1{hex_suffix}"
    else:
        # Next 13 positions (line 2)
        hex_suffix = hex(col_idx - 12)[2:].upper()  # 1-D
        return f"2{hex_suffix}"


class BLEDataParser:
    """Parse Excel RSSI data and clean measurements"""

    def __init__(self, excel_path: str = 'Geopos indoor BLE.xlsx'):
        self.excel_path = excel_path
        self.raw_df = None

    def parse_excel(self) -> pd.DataFrame:
        """Parse Excel to structured DataFrame with position codes"""
        # Read Excel without header
        df = pd.read_excel(self.excel_path, sheet_name='Feuil1', header=None)

        # Identify beacon sections
        beacon_sections = []
        for idx, row in df.iterrows():
            if pd.notna(row[2]) and 'Balise' in str(row[2]):
                beacon_id = str(row[2]).replace('Balise ', '').strip()
                beacon_sections.append({'row': idx, 'beacon_id': beacon_id})

        # Extract RSSI measurements
        measurements = []

        for i, section in enumerate(beacon_sections):
            beacon_id = section['beacon_id']
            start_row = section['row']

            # Determine end row
            if i < len(beacon_sections) - 1:
                end_row = beacon_sections[i+1]['row']
            else:
                end_row = len(df)

            # Extract data rows for this beacon
            beacon_data = df.iloc[start_row+1:end_row]

            # Process each data row (smartphones)
            # Reset line counter for THIS beacon (each beacon section has its own line numbering)
            line_counters = {}
            current_smartphone = None  # Track current smartphone for forward-fill

            for row_idx, row in beacon_data.iterrows():
                # Forward-fill smartphone name: if col1 is empty, use previous smartphone
                if pd.notna(row[1]) and str(row[1]).strip():
                    smartphone_raw = str(row[1]).replace('Tél', 'Tel').strip()
                    if 'Tel' in smartphone_raw:
                        current_smartphone = smartphone_raw

                smartphone = current_smartphone

                if smartphone:
                    # Initialize line counter for this smartphone if not exists
                    if smartphone not in line_counters:
                        line_counters[smartphone] = 1
                    else:
                        line_counters[smartphone] += 1

                    current_line = line_counters[smartphone]

                    # Determine which geometric line based on smartphone and line number
                    # Paul: line 1 (Y=0) then line 2 (Y=1)
                    # Guillaume: line 1 (Y=0) then line 2 (Y=1)
                    # Nicolas: line 1 (Y=0) only

                    geometric_line = current_line  # Default

                    # Extract RSSI values from columns 2-14 (13 positions)
                    for col_idx in range(2, 15):
                        rssi_val = row[col_idx]

                        if pd.notna(rssi_val) and str(rssi_val) not in ['inf', 'ERR']:
                            try:
                                rssi_dbm = float(rssi_val)
                                position_idx = col_idx - 2  # 0-12

                                # Decode position code based on geometric line
                                hex_suffix = hex(position_idx + 1)[2:].upper()  # 1-D
                                position_code = f"{geometric_line}{hex_suffix}"

                                measurements.append({
                                    'beacon_id': beacon_id,
                                    'smartphone': smartphone,
                                    'position_code': position_code,
                                    'position_idx': position_idx,  # Keep for compatibility
                                    'line_number': geometric_line,
                                    'rssi_dbm': rssi_dbm,
                                    'valid': True
                                })
                            except ValueError:
                                pass

        self.raw_df = pd.DataFrame(measurements)
        return self.raw_df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and filter RSSI measurements"""
        # Filter valid measurements
        df_clean = df[df['valid'] == True].copy()

        # Remove invalid RSSI values
        df_clean = df_clean[df_clean['rssi_dbm'] != 'inf']
        df_clean = df_clean[df_clean['rssi_dbm'] != 'ERR']

        # Convert to numeric
        df_clean['rssi_dbm'] = pd.to_numeric(df_clean['rssi_dbm'])

        # Filter reasonable RSSI range
        df_clean = df_clean[(df_clean['rssi_dbm'] >= 50) & (df_clean['rssi_dbm'] <= 100)]

        return df_clean.reset_index(drop=True)


class PositionLoader:
    """Load beacon and measurement positions from CSV files"""

    def __init__(self, beacon_csv: str, measurement_csv: str):
        self.beacon_csv = beacon_csv
        self.measurement_csv = measurement_csv
        self.beacon_df = None
        self.measurement_df = None

    def load_beacons(self) -> pd.DataFrame:
        """Load beacon positions"""
        self.beacon_df = pd.read_csv(self.beacon_csv)
        return self.beacon_df

    def load_measurements(self) -> pd.DataFrame:
        """Load measurement positions"""
        self.measurement_df = pd.read_csv(self.measurement_csv)
        return self.measurement_df

    def get_beacon_position(self, beacon_id: str) -> Tuple[float, float]:
        """Get (x, y) for specific beacon"""
        beacon = self.beacon_df[self.beacon_df['beacon_id'] == beacon_id]
        if len(beacon) > 0:
            return (beacon.iloc[0]['x_meters'], beacon.iloc[0]['y_meters'])
        return (None, None)

    def get_measurement_position(self, position_code: str) -> Tuple[float, float]:
        """Get (x, y) for specific measurement position using position_code"""
        measurement = self.measurement_df[self.measurement_df['position_code'] == position_code]
        if len(measurement) > 0:
            return (measurement.iloc[0]['x_meters'], measurement.iloc[0]['y_meters'])
        return (None, None)
