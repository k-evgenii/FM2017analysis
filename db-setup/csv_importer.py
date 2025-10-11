#!/usr/bin/env python3
"""
CSV to Database Importer (OOP Version with Abstract Base Classes)
Flexible script to import CSV files into any database with automatic table creation
Supports SQLite, MySQL, PostgreSQL, etc. through DatabaseConnection interface
"""

import csv
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re
from database_abc import DatabaseConnection, create_database_connection
import importlib.util
import sys



class CSVAnalyzer:
    """Analyzes CSV files and determines column types"""
    
    def __init__(self, csv_path: str):
        """
        Initialize CSV analyzer
        
        Args:
            csv_path: Path to CSV file
        """
        self.csv_path = Path(csv_path)
        self.headers: List[str] = []
        self.sample_data: List[List] = []
        
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
            
    def analyze(self, sample_size: int = 100) -> List[Dict[str, str]]:
        """
        Analyze CSV and determine column types
        
        Args:
            sample_size: Number of rows to sample for type detection
            
        Returns:
            List of column definitions with name and type
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.headers = next(reader)
            
            # Read sample data
            for i, row in enumerate(reader):
                if i >= sample_size:
                    break
                self.sample_data.append(row)
                
        print(f"✓ Analyzed CSV: {self.csv_path.name}")
        print(f"  - Columns: {len(self.headers)}")
        print(f"  - Sample rows: {len(self.sample_data)}")
        
        # Determine column types
        columns = []
        for idx, header in enumerate(self.headers):
            col_type = self._infer_column_type(idx)
            columns.append({
                'name': self._sanitize_column_name(header),
                'type': col_type
            })
            
        return columns
        
    def _sanitize_column_name(self, name: str) -> str:
        """Sanitize column name for SQL"""
        # Replace spaces and special chars with underscores
        name = re.sub(r'[^\w]', '_', name)
        # Remove leading/trailing underscores
        name = name.strip('_')
        # Convert to lowercase
        name = name.lower()
        return name
        
    def _infer_column_type(self, col_idx: int) -> str:
        """Infer SQL type for a column based on sample data"""
        if col_idx >= len(self.headers):
            return 'TEXT'
            
        # Collect non-empty values
        values = [row[col_idx] for row in self.sample_data if col_idx < len(row) and row[col_idx].strip()]
        
        if not values:
            return 'TEXT'
            
        # Check if all are integers
        if all(self._is_integer(v) for v in values):
            return 'INTEGER'
            
        # Check if all are floats
        if all(self._is_float(v) for v in values):
            return 'REAL'
            
        # Check if all are dates
        if all(self._is_date(v) for v in values):
            return 'DATE'
            
        # Default to TEXT
        return 'TEXT'
        
    @staticmethod
    def _is_integer(value: str) -> bool:
        """Check if value is an integer"""
        try:
            int(value)
            return '.' not in value
        except ValueError:
            return False
            
    @staticmethod
    def _is_float(value: str) -> bool:
        """Check if value is a float"""
        try:
            float(value)
            return True
        except ValueError:
            return False
            
    @staticmethod
    def _is_date(value: str) -> bool:
        """Check if value is a date"""
        date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d']
        for fmt in date_formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue
        return False
        
    def read_all_data(self) -> Tuple[List[str], List[List]]:
        """
        Read all data from CSV
        
        Returns:
            Tuple of (headers, rows)
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
            
        return headers, rows


class CSVImporter:
    """Main class for importing CSV data to any database using DatabaseConnection"""
    
    MODE_AUTO = 'auto'          # Auto-detect and create/match table
    MODE_CREATE = 'create'      # Force create new table
    MODE_MATCH = 'match'        # Match existing table columns
    MODE_APPEND = 'append'      # Append to existing table
    
    def __init__(self, db_connection: DatabaseConnection, csv_path: str, table_name: str):
        """
        Initialize CSV importer
        
        Args:
            db_connection: DatabaseConnection instance (SQLite, MySQL, etc.)
            csv_path: Path to CSV file
            table_name: Name of target table
        """
        self.db_connection: DatabaseConnection = db_connection
        self.csv_analyzer = CSVAnalyzer(csv_path)
        self.table_name: str = table_name
        
    def import_csv(self, 
                   mode: str = MODE_AUTO,
                   init_script: Optional[str] = None,
                   modify_script: Optional[str] = None) -> None:
        """
        Import CSV data to database
        
        Args:
            mode: Import mode ('auto', 'create', 'match', 'append')
            init_script: Optional path to initialization SQL script
            modify_script: Optional path to modification SQL script
        """
        print("\n" + "="*60)
        print("CSV to Database Import")
        print("="*60)
        print(f"CSV File: {self.csv_analyzer.csv_path}")
        print(f"Database: {self.db_connection.db_path}")
        print(f"Table: {self.table_name}")
        print(f"Mode: {mode}")
        print("="*60 + "\n")
        
        # Connect to database
        self.db_connection.connect()
        
        try:
            # Check if we need to initialize database (SQLite only)
            db_path = Path(self.db_connection.db_path)
            if db_path.exists() and (not db_path.stat().st_size or db_path.stat().st_size == 0):
                if init_script:
                    print("Database is empty. Running initialization script...")
                    with open(init_script, 'r', encoding='utf-8') as f:
                        sql_script = f.read()
                    self.db_connection.execute_script(sql_script)
                    if modify_script:
                        print("Running modification script...")
                        with open(modify_script, 'r', encoding='utf-8') as f:
                            sql_script = f.read()
                        self.db_connection.execute_script(sql_script)
                        
            # Analyze CSV
            csv_columns = self.csv_analyzer.analyze()
            
            # Handle different modes
            if mode == self.MODE_AUTO:
                self._import_auto(csv_columns)
            elif mode == self.MODE_CREATE:
                self._import_create(csv_columns)
            elif mode == self.MODE_MATCH:
                self._import_match(csv_columns)
            elif mode == self.MODE_APPEND:
                self._import_append(csv_columns)
            else:
                raise ValueError(f"Unknown mode: {mode}")
                
        finally:
            self.db_connection.disconnect()
            
        print("\n" + "="*60)
        print("✓ Import completed successfully!")
        print("="*60 + "\n")
        
    def _import_auto(self, csv_columns: List[Dict[str, str]]) -> None:
        """Auto mode: detect and handle appropriately"""
        if self.db_connection.table_exists(self.table_name):
            print(f"Table '{self.table_name}' exists. Checking column compatibility...")
            self._import_match(csv_columns)
        else:
            print(f"Table '{self.table_name}' does not exist. Creating new table...")
            self._import_create(csv_columns)
            
    def _import_create(self, csv_columns: List[Dict[str, str]]) -> None:
        """Create mode: create new table and import"""
        if self.db_connection.table_exists(self.table_name):
            print(f"WARNING: Table '{self.table_name}' already exists.")
            response = input("Drop and recreate? (y/N): ")
            if response.lower() == 'y':
                # Use execute_query to drop table
                drop_query = f"DROP TABLE {self.table_name}"
                self.db_connection.execute_query(drop_query)
                self.db_connection.commit()
                print(f"✓ Dropped table: {self.table_name}")
            else:
                print("Import cancelled.")
                return
                
        # Create table
        self.db_connection.create_table(self.table_name, csv_columns)
        
        # Import data
        self._insert_data(csv_columns)
        
    def _import_match(self, csv_columns: List[Dict[str, str]]) -> None:
        """Match mode: match CSV columns to existing table"""
        if not self.db_connection.table_exists(self.table_name):
            raise ValueError(f"Table '{self.table_name}' does not exist. Use 'create' or 'auto' mode.")
            
        db_columns = self.db_connection.get_table_columns(self.table_name)
        csv_col_names = [col['name'] for col in csv_columns]
        
        # Find matching columns
        matched_columns = []
        for csv_col in csv_col_names:
            if csv_col in db_columns:
                matched_columns.append(csv_col)
                
        if not matched_columns:
            raise ValueError("No matching columns found between CSV and database table")
            
        print(f"\nMatched columns ({len(matched_columns)}/{len(csv_col_names)}):")
        for col in matched_columns:
            print(f"  ✓ {col}")
            
        unmatched = [col for col in csv_col_names if col not in matched_columns]
        if unmatched:
            print(f"\nUnmatched columns ({len(unmatched)}):")
            for col in unmatched:
                print(f"  ✗ {col}")
                
        # Import only matched columns
        self._insert_data(csv_columns, matched_columns)
        
    def _import_append(self, csv_columns: List[Dict[str, str]]) -> None:
        """Append mode: append to existing table (all columns must match)"""
        if not self.db_connection.table_exists(self.table_name):
            raise ValueError(f"Table '{self.table_name}' does not exist. Use 'create' or 'auto' mode.")
            
        db_columns = self.db_connection.get_table_columns(self.table_name)
        csv_col_names = [col['name'] for col in csv_columns]
        
        # Check if all CSV columns exist in DB
        missing = [col for col in csv_col_names if col not in db_columns]
        if missing:
            raise ValueError(f"CSV has columns not in table: {', '.join(missing)}")
            
        self._insert_data(csv_columns)
        
    def _insert_data(self, 
                     csv_columns: List[Dict[str, str]], 
                     column_filter: Optional[List[str]] = None) -> None:
        """
        Insert data from CSV into table
        
        Args:
            csv_columns: CSV column definitions
            column_filter: Optional list of column names to include
        """
        # Read all CSV data
        headers, rows = self.csv_analyzer.read_all_data()
        
        # Sanitize headers
        sanitized_headers = [self.csv_analyzer._sanitize_column_name(h) for h in headers]
        
        # Filter columns if needed
        if column_filter:
            # Get indices of columns to include
            col_indices = [i for i, h in enumerate(sanitized_headers) if h in column_filter]
            columns_to_insert = [sanitized_headers[i] for i in col_indices]
            
            # Filter row data
            filtered_rows = []
            for row in rows:
                filtered_row = [row[i] if i < len(row) else '' for i in col_indices]
                filtered_rows.append(filtered_row)
            rows = filtered_rows
        else:
            columns_to_insert = sanitized_headers
            
        print(f"\nInserting {len(rows)} rows into '{self.table_name}'...")
        
        # Insert data in batches
        batch_size = 1000
        total_inserted = 0
        
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            inserted = self.db_connection.insert_rows(self.table_name, columns_to_insert, batch)
            total_inserted += inserted
            print(f"  Progress: {total_inserted}/{len(rows)} rows")
            
        print(f"✓ Inserted {total_inserted} rows")

    def categorical_variable_import(self,
                                    csv_column: str,
                                    variable_description: str,
                                    target_table: str,
                                    csv_uid_column: Optional[str] = None) -> None:
        """
        Import categorical variable from CSV into a target table using a mapping.

        Args:
            csv_column: Column name in the CSV that contains the categorical text (e.g. PositionsDesc)
            variable_description: Path to a Python script that produces a mapping dict OR will be ignored and mapping generated from CSV
            target_table: Table name in DB to insert rows into (e.g. 'positions')
            csv_uid_column: Optional CSV column that contains an external player id (e.g. 'UID'). If omitted, will try to match by Name.
        """
        # Load or generate mapping dict from variable_description
        mapping = {}
        var_path = Path(variable_description)
        if var_path.exists():
            try:
                spec = importlib.util.spec_from_file_location("var_desc", str(var_path))
                if spec is None or spec.loader is None:
                    raise ImportError("Could not load spec from variable description file")
                mod = importlib.util.module_from_spec(spec)
                sys.modules["var_desc"] = mod
                spec.loader.exec_module(mod)  # type: ignore
                # look for common names
                if hasattr(mod, 'pos_map1'):
                    mapping = getattr(mod, 'pos_map1')
                elif hasattr(mod, 'pos_map'):
                    mapping = getattr(mod, 'pos_map')
                elif hasattr(mod, 'get_mapping'):
                    mapping = getattr(mod, 'get_mapping')()
                else:
                    print("Variable description script didn't expose a mapping; will infer from CSV")
                    mapping = {}
            except Exception as e:
                print(f"Failed to load variable description: {e}; will infer mapping from CSV")
                mapping = {}
        else:
            print("Variable description file not found; inferring mapping from CSV")

        # Read CSV and extract the two columns we need
        headers, rows = self.csv_analyzer.read_all_data()
        sanitized_headers = [self.csv_analyzer._sanitize_column_name(h) for h in headers]

        # Determine indices
        try:
            col_idx = sanitized_headers.index(self.csv_analyzer._sanitize_column_name(csv_column))
        except ValueError:
            raise ValueError(f"CSV column not found: {csv_column}")

        uid_idx = None
        if csv_uid_column:
            if self.csv_analyzer._sanitize_column_name(csv_uid_column) in sanitized_headers:
                uid_idx = sanitized_headers.index(self.csv_analyzer._sanitize_column_name(csv_uid_column))
        else:
            # try common names
            for candidate in ['uid', 'player_id', 'playerid', 'id', 'name']:
                if candidate in sanitized_headers:
                    uid_idx = sanitized_headers.index(candidate)
                    break

        # If mapping is empty, infer mapping from CSV column values
        if not mapping:
            unique_positions = set()
            for row in rows:
                cell = row[col_idx] if col_idx < len(row) else ''
                if not cell:
                    continue
                for combination in str(cell).split('/'):
                    for token in combination.split():
                        unique_positions.add(token)
            mapping = {pos: idx+1 for idx, pos in enumerate(sorted(unique_positions))}
            print(f"Inferred mapping with {len(mapping)} categories")

        # Connect to DB and prepare lookups
        self.db_connection.connect()
        try:
            # discover players table columns to choose lookup strategy
            player_cols = self.db_connection.get_table_columns('players') if self.db_connection.table_exists('players') else []

            batch_size = 1000
            batch: List[List] = []
            seen = set()
            total_inserted = 0

            for ridx, row in enumerate(rows, start=1):
                cell = row[col_idx] if col_idx < len(row) else ''
                if not cell:
                    continue

                # resolve player_id
                player_id = None
                if uid_idx is not None and uid_idx < len(row):
                    uid_val = row[uid_idx]
                    candidates = [c for c in player_cols if 'uid' in c.lower() or 'ext' in c.lower() or c.lower() == 'player_id']
                    if candidates:
                        candidate = candidates[0]
                        q = f"SELECT player_id FROM players WHERE {candidate} = ? LIMIT 1"
                        res = self.db_connection.execute_query(q, (uid_val,))
                        if res:
                            player_id = res[0][0]

                if player_id is None:
                    name_idx = None
                    if 'name' in sanitized_headers:
                        name_idx = sanitized_headers.index('name')
                    if name_idx is not None and name_idx < len(row):
                        name_val = row[name_idx]
                        q = "SELECT player_id FROM players WHERE name = ? LIMIT 1"
                        res = self.db_connection.execute_query(q, (name_val,))
                        if res:
                            player_id = res[0][0]

                if player_id is None:
                    continue

                # split cell into tokens and prepare inserts
                for combination in str(cell).split('/'):
                    for token in combination.split():
                        token = token.strip()
                        if not token:
                            continue
                        mapped = mapping.get(token)
                        if mapped is None:
                            continue
                        position_value = str(mapped)
                        team_id = 0
                        key = (player_id, team_id, position_value)
                        if key in seen:
                            continue

                        # check database to avoid duplicates
                        q = "SELECT 1 FROM {tbl} WHERE player_id = ? AND team_id = ? AND position = ?".format(tbl=target_table)
                        exists = self.db_connection.execute_query(q, (player_id, team_id, position_value))
                        if exists:
                            seen.add(key)
                            continue

                        seen.add(key)
                        batch.append([player_id, team_id, position_value])

                        # flush batch
                        if len(batch) >= batch_size:
                            inserted = self.db_connection.insert_rows(target_table, ['player_id', 'team_id', 'position'], batch)
                            total_inserted += inserted
                            print(f"  Progress: inserted {total_inserted} rows (processed {ridx}/{len(rows)})")
                            batch.clear()

            # final flush
            if batch:
                inserted = self.db_connection.insert_rows(target_table, ['player_id', 'team_id', 'position'], batch)
                total_inserted += inserted

            if total_inserted:
                print(f"Inserted {total_inserted} categorical rows into {target_table}")
            else:
                print("No categorical rows to insert")

        finally:
            self.db_connection.disconnect()


def main():
    """Main function with CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Import CSV data to database with flexible table handling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # SQLite - Auto mode
  python csv_importer.py --csv data.csv --db mydb.db --table players --mode auto
  
  # SQLite - Create new table from CSV
  python csv_importer.py --csv data.csv --db mydb.db --table players --mode create
  
  # SQLite - Match columns with existing table
  python csv_importer.py --csv data.csv --db mydb.db --table players --mode match
  
  # MySQL - Import to MySQL database
  python csv_importer.py --csv data.csv --db-type mysql --db mydb --table players \\
      --host localhost --user root --password mypass
  
  # Initialize DB first, then import
  python csv_importer.py --csv data.csv --db mydb.db --table players \\
      --init initialise_db.sql --modify modify_db.sql
        """
    )
    
    parser.add_argument('--csv', required=True, help='Path to CSV file')
    parser.add_argument('--db', required=True, help='Database name/path')
    parser.add_argument('--db-type',
                       choices=['sqlite', 'mysql'],
                       default='sqlite',
                       help='Database type (default: sqlite)')
    parser.add_argument('--host',
                       default='localhost',
                       help='Database host (for MySQL, default: localhost)')
    parser.add_argument('--port',
                       type=int,
                       default=3306,
                       help='Database port (for MySQL, default: 3306)')
    parser.add_argument('--user',
                       default='root',
                       help='Database user (for MySQL, default: root)')
    parser.add_argument('--password',
                       default='',
                       help='Database password (for MySQL)')
    parser.add_argument('--table', required=True, help='Target table name')
    parser.add_argument('--mode', 
                       choices=['auto', 'create', 'match', 'append'],
                       default='auto',
                       help='Import mode (default: auto)')
    parser.add_argument('--init', help='Path to initialization SQL script')
    parser.add_argument('--modify', help='Path to modification SQL script')
    
    args = parser.parse_args()
    
    # Create database connection based on type
    if args.db_type == 'sqlite':
        db_conn = create_database_connection('sqlite', db_path=args.db)
    elif args.db_type == 'mysql':
        db_conn = create_database_connection('mysql',
                                            db_path=args.db,
                                            host=args.host,
                                            port=args.port,
                                            user=args.user,
                                            password=args.password)
    else:
        print(f"ERROR: Unsupported database type: {args.db_type}")
        return 1
    
    # Create importer and run
    importer = CSVImporter(db_conn, args.csv, args.table)
    importer.import_csv(
        mode=args.mode,
        init_script=args.init,
        modify_script=args.modify
    )


if __name__ == "__main__":
    main()
