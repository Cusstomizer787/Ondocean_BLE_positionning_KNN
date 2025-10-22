"""
Diagnostic: Analyser donnees parsees pour comprendre structure
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.parser import BLEDataParser, PositionLoader
import pandas as pd

def main():
    print("="*80)
    print("DIAGNOSTIC DONNEES PARSEES")
    print("="*80)

    # Parse data
    parser = BLEDataParser('Geopos indoor BLE.xlsx')
    df_raw = parser.parse_excel()
    df_clean = parser.clean_data(df_raw)

    print(f"\n1. MESURES TOTALES: {len(df_clean)}")

    print("
2. REPARTITION PAR SMARTPHONE:")
    for smartphone in df_clean['smartphone'].unique():
        count = len(df_clean[df_clean['smartphone'] == smartphone])
        print(f"   {smartphone}: {count} mesures")

    print("
3. REPARTITION PAR BALISE:")
    for beacon_id in sorted(df_clean['beacon_id'].unique()):
        count = len(df_clean[df_clean['beacon_id'] == beacon_id])
        print(f"   Balise {beacon_id}: {count} mesures")

    print("
4. POSITION CODES DETECTES:")
    position_codes = df_clean['position_code'].unique()
    print(f"   Total positions uniques: {len(position_codes)}")
    print(f"   Codes: {sorted(position_codes)}")

    print("
5. REPARTITION PAR LIGNE:")
    line1 = df_clean[df_clean['position_code'].str.startswith('1')]
    line2 = df_clean[df_clean['position_code'].str.startswith('2')]
    print(f"   Ligne 1 (codes 1X): {len(line1)} mesures")
    print(f"   Ligne 2 (codes 2X): {len(line2)} mesures")

    print("
6. VERIFICATION TEL NICOLAS (devrait etre seulement ligne 2):")
    nicolas_data = df_clean[df_clean['smartphone'].str.contains('Nicolas')]
    print(f"   Total mesures Tel Nicolas: {len(nicolas_data)}")
    if len(nicolas_data) > 0:
        nicolas_codes = nicolas_data['position_code'].unique()
        print(f"   Position codes: {sorted(nicolas_codes)}")
        nicolas_line1 = nicolas_data[nicolas_data['position_code'].str.startswith('1')]
        nicolas_line2 = nicolas_data[nicolas_data['position_code'].str.startswith('2')]
        print(f"   Ligne 1: {len(nicolas_line1)}, Ligne 2: {len(nicolas_line2)}")

    print("
7. SAMPLE DE DONNEES:")
    print(df_clean[['beacon_id', 'smartphone', 'position_code', 'rssi_dbm']].head(20).to_string())

    print("
8. RSSI PAR POSITION (moyennes):")
    rssi_by_position = df_clean.groupby('position_code')['rssi_dbm'].agg(['mean', 'count']).round(1)
    print(rssi_by_position.to_string())

    print("\n" + "="*80)
    print("DIAGNOSTIC TERMINE")
    print("="*80)

if __name__ == "__main__":
    main()
