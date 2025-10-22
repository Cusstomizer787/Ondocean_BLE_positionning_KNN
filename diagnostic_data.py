"""
Diagnostic: Analyser données parsées pour comprendre structure
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.parser import BLEDataParser, PositionLoader
import pandas as pd

print("="*80)
print("DIAGNOSTIC DONNEES PARSEES")
print("="*80)

# Parse data
parser = BLEDataParser('Geopos indoor BLE.xlsx')
df_raw = parser.parse_excel()
print(f"\nColonnes du DataFrame: {df_raw.columns.tolist()}")
print(f"Premières lignes:\n{df_raw.head()}")
df_clean = parser.clean_data(df_raw)

print(f"\n1. MESURES TOTALES: {len(df_clean)}")

print(f"\n2. REPARTITION PAR SMARTPHONE:")
for smartphone in df_clean['smartphone'].unique():
    count = len(df_clean[df_clean['smartphone'] == smartphone])
    print(f"   {smartphone}: {count} mesures")

print(f"\n3. REPARTITION PAR BALISE:")
for beacon_id in sorted(df_clean['beacon_id'].unique()):
    count = len(df_clean[df_clean['beacon_id'] == beacon_id])
    print(f"   Balise {beacon_id}: {count} mesures")

print(f"\n4. POSITION CODES DETECTES:")
position_codes = df_clean['position_code'].unique()
print(f"   Total positions uniques: {len(position_codes)}")
print(f"   Codes: {sorted(position_codes)}")

print(f"\n5. REPARTITION PAR LIGNE:")
line1 = df_clean[df_clean['position_code'].str.startswith('1')]
line2 = df_clean[df_clean['position_code'].str.startswith('2')]
print(f"   Ligne 1 (codes 1X): {len(line1)} mesures")
print(f"   Ligne 2 (codes 2X): {len(line2)} mesures")

print(f"\n6. VERIFICATION TEL NICOLAS (devrait être seulement ligne 2):")
tel_nicolas = df_clean[df_clean['smartphone'].str.contains('Nicolas', na=False)]
print(f"   Total mesures Tel Nicolas: {len(tel_nicolas)}")
if len(tel_nicolas) > 0:
    codes_nicolas = sorted(tel_nicolas['position_code'].unique())
    print(f"   Position codes: {codes_nicolas}")
    line1_nicolas = tel_nicolas[tel_nicolas['position_code'].str.startswith('1')]
    line2_nicolas = tel_nicolas[tel_nicolas['position_code'].str.startswith('2')]
    print(f"   Ligne 1: {len(line1_nicolas)}, Ligne 2: {len(line2_nicolas)}")

print(f"\n7. SAMPLE DE DONNEES:")
print(df_clean[['beacon_id', 'smartphone', 'position_code', 'rssi_dbm']].head(20))

print(f"\n8. RSSI PAR POSITION (moyennes):")
rssi_by_pos = df_clean.groupby('position_code')['rssi_dbm'].agg(['mean', 'count'])
print(rssi_by_pos)

print("\n" + "="*80)
print("DIAGNOSTIC TERMINE")
print("="*80)
