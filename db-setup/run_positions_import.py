#!/usr/bin/env python3
"""
Run categorical import for Positions from the FM CSV into the positions table.
Usage (PowerShell):
    python .\\db-setup\\run_positions_import.py

This script expects the repository root structure unchanged and will:
 - read fman_initial_Dat_Analysis_test/fbmandataset.csv
 - use fman_initial_Dat_Analysis_test/positions_separater.py for mapping (if present)
 - insert rows into db-setup/fm.db positions table

Make a DB backup if you want to be cautious before running.
"""
from pathlib import Path
from database_abc import create_database_connection
from csv_importer import CSVImporter


def main():
    repo_root = Path(__file__).parent.parent
    csv_path = repo_root / 'fman_initial_Dat_Analysis_test' / 'fbmandataset.csv'
    var_script = repo_root / 'fman_initial_Dat_Analysis_test' / 'positions_separater.py'
    db_path = Path(__file__).parent / 'fm.db'

    if not csv_path.exists():
        print(f"ERROR: CSV not found: {csv_path}")
        return 1
    if not db_path.exists():
        print(f"ERROR: Database not found: {db_path}")
        return 1

    print("Running positions categorical import")
    print(f" CSV: {csv_path}")
    print(f" Var script: {var_script}")
    print(f" DB: {db_path}\n")

    db_conn = create_database_connection('sqlite', db_path=str(db_path))
    importer = CSVImporter(db_conn, str(csv_path), 'positions')

    # This will parse PositionsDesc column, use mapping from positions_separater.py when available
    importer.categorical_variable_import('PositionsDesc', str(var_script), 'positions', csv_uid_column='UID')

    print('\nDone.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
