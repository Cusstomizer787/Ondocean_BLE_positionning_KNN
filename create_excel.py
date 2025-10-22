#!/usr/bin/env python3
"""
Script to create the missing Excel file for the GitHub distribution
"""
import pandas as pd
import numpy as np
import os

def create_excel_file():
    """Create Geopos indoor BLE.xlsx with sample data structure"""

    # Create sample data structure similar to the original Excel
    # Based on the parsing logic in parser.py

    # Create empty DataFrame with appropriate dimensions
    # Original file has 42 rows and 15 columns based on diagnostic

    rows = []

    # Beacon 38 section (rows 3-10 in original)
    rows.append(['', '', 'Balise 38', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['Tel Paul', '', 90, 88, 92, 90, 92, 91, 93, 90, 92, 88, 90, 85, 90])  # Line 1
    rows.append(['', '', 95, '', 88, 92, 90, 91, 90, 88, 90, 80, 85, 87, 87])  # Line 2
    rows.append(['Tel Guillaume', '', 79, 77, 83, 89, 93, 96, 97, 95, 94, 92, 90, 88, 86])  # Line 1
    rows.append(['', '', 85, 87, 89, 91, 93, 95, 94, 92, 90, 88, 86, 84, 82])  # Line 2
    rows.append(['Tel Nicolas', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])  # Line 1 (empty)
    rows.append(['', '', 88, 90, 92, 94, 91, 89, 87, 85, 83, 81, 79, 77, 75])  # Line 2

    # Beacon 3 section (rows 11-18)
    rows.append(['', '', 'Balise 3', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['Tel Paul', '', 85, 83, 87, 89, 91, 88, 86, 84, 82, 80, 78, 76, 74])
    rows.append(['', '', 80, 82, 84, 86, 88, 85, 83, 81, 79, 77, 75, 73, 71])
    rows.append(['Tel Guillaume', '', 82, 84, 86, 88, 90, 87, 85, 83, 81, 79, 77, 75, 73])
    rows.append(['', '', 77, 79, 81, 83, 85, 82, 80, 78, 76, 74, 72, 70, 68])
    rows.append(['Tel Nicolas', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['', '', 75, 77, 79, 81, 83, 80, 78, 76, 74, 72, 70, 68, 66])

    # Beacon 53 section (rows 19-26)
    rows.append(['', '', 'Balise 53', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['Tel Paul', '', 80, 82, 84, 86, 83, 81, 79, 77, 75, 73, 71, 69, 67])
    rows.append(['', '', 75, 77, 79, 81, 78, 76, 74, 72, 70, 68, 66, 64, 62])
    rows.append(['Tel Guillaume', '', 78, 80, 82, 84, 81, 79, 77, 75, 73, 71, 69, 67, 65])
    rows.append(['', '', 73, 75, 77, 79, 76, 74, 72, 70, 68, 66, 64, 62, 60])
    rows.append(['Tel Nicolas', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['', '', 70, 72, 74, 76, 73, 71, 69, 67, 65, 63, 61, 59, 57])

    # Beacon 25 section (rows 27-34)
    rows.append(['', '', 'Balise 25', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['Tel Paul', '', 88, 90, 87, 85, 83, 81, 79, 77, 75, 73, 71, 69, 67])
    rows.append(['', '', 83, 85, 82, 80, 78, 76, 74, 72, 70, 68, 66, 64, 62])
    rows.append(['Tel Guillaume', '', 85, 87, 84, 82, 80, 78, 76, 74, 72, 70, 68, 66, 64])
    rows.append(['', '', 80, 82, 79, 77, 75, 73, 71, 69, 67, 65, 63, 61, 59])
    rows.append(['Tel Nicolas', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['', '', 78, 80, 77, 75, 73, 71, 69, 67, 65, 63, 61, 59, 57])

    # Beacon 60 section (rows 35-42)
    rows.append(['', '', 'Balise 60', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['Tel Paul', '', 92, 90, 88, 86, 84, 82, 80, 78, 76, 74, 72, 70, 68])
    rows.append(['', '', 87, 85, 83, 81, 79, 77, 75, 73, 71, 69, 67, 65, 63])
    rows.append(['Tel Guillaume', '', 89, 87, 85, 83, 81, 79, 77, 75, 73, 71, 69, 67, 65])
    rows.append(['', '', 84, 82, 80, 78, 76, 74, 72, 70, 68, 66, 64, 62, 60])
    rows.append(['Tel Nicolas', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
    rows.append(['', '', 82, 80, 78, 76, 74, 72, 70, 68, 66, 64, 62, 60, 58])

    # Create DataFrame
    df = pd.DataFrame(rows)

    # Save to Excel
    output_file = 'Geopos indoor BLE.xlsx'
    df.to_excel(output_file, sheet_name='Feuil1', header=False, index=False)

    print(f"✅ Excel file created: {output_file}")
    print(f"   Shape: {df.shape}")
    print(f"   File size: {os.path.getsize(output_file)} bytes")

    # Verify structure
    print("\n📊 Excel structure verification:")
    for idx, row in df.iterrows():
        if pd.notna(row[2]) and 'Balise' in str(row[2]):
            beacon_id = str(row[2]).replace('Balise ', '').strip()
            print(f"   Beacon {beacon_id} at row {idx}")

    return True

if __name__ == "__main__":
    print("🔧 Creating Geopos indoor BLE.xlsx for GitHub distribution...")
    create_excel_file()
    print("\n✅ Excel file ready for GitHub!")
    print("💡 Note: This is a sample file. Replace with original if available.")
