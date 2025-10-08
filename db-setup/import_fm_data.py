#!/usr/bin/env python3
"""
Import FM2017 dataset into database
Quick script to import fbmandataset.csv into the players table
"""

from pathlib import Path
from database_abc import create_database_connection
from csv_importer import CSVImporter


def main():
    """Import FM dataset into database"""
    
    # Paths
    script_dir = Path(__file__).parent
    original_csv = script_dir.parent / "fman_initial_Dat_Analysis_test" / "fbmandataset.csv"
    processed_csv = script_dir.parent / "fman_initial_Dat_Analysis_test" / "fbmandataset_processed.csv"
    db_path = script_dir / "fm.db"
    
    # Check if we need to preprocess
    if not processed_csv.exists() or original_csv.stat().st_mtime > processed_csv.stat().st_mtime:
        print("Preprocessing CSV to match database schema...")
        from preprocess_csv import preprocess_csv
        preprocess_csv(str(original_csv), str(processed_csv))
    
    csv_path = processed_csv
    
    # Verify CSV exists
    if not csv_path.exists():
        print(f"ERROR: CSV file not found: {csv_path}")
        return 1
    
    print("="*60)
    print("FM2017 Dataset Import")
    print("="*60)
    print(f"CSV: {csv_path}")
    print(f"Database: {db_path}")
    print("="*60 + "\n")
    
    # Create database connection
    db_conn = create_database_connection('sqlite', db_path=str(db_path))
    
    # Create importer
    importer = CSVImporter(db_conn, str(csv_path), 'players')
    
    # Import with match mode (will match columns with existing table)
    importer.import_csv(
        mode='match'
    )
    
    print("\n✓ FM2017 dataset successfully imported!")
    print(f"✓ Database: {db_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())
