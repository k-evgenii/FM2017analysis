#!/usr/bin/env python3
"""
CSV to SQLite Database Importer (OOP Version)
Flexible script to import CSV files into SQLite database with automatic table creation
""" #just a prototype for the script, so nothing properly works yet, use as a base to set up a csv importer

import sqlite3
import csv
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re


class DatabaseManager:
    """Manages SQLite database connection and operations"""
    
    def __init__(self, db_path: str):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        
    def connect(self) -> None:
        """Establish connection to database"""
        self.connection = sqlite3.connect(str(self.db_path))
        self.cursor = self.connection.cursor()
        print(f"✓ Connected to database: {self.db_path}")
        
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.commit()
            self.connection.close()
            print("✓ Database connection closed")
            
    def execute_script(self, sql_file: Path) -> None:
        """Execute SQL script from file"""
        if not sql_file.exists():
            raise FileNotFoundError(f"SQL script not found: {sql_file}")
            
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        self.cursor.executescript(sql_script)
        self.connection.commit()
        print(f"✓ Executed SQL script: {sql_file.name}")
        
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in database"""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.cursor.execute(query, (table_name,)).fetchone()
        return result is not None
        
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get list of column names for a table"""
        query = f"PRAGMA table_info({table_name})"
        columns = self.cursor.execute(query).fetchall()
        return [col[1] for col in columns]  # col[1] is the column name
        
    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> None:
        """
        Create a new table with specified columns
        
        Args:
            table_name: Name of the table to create
            columns: List of dicts with 'name' and 'type' keys
        """
        column_defs = [f'"{col["name"]}" {col["type"]}' for col in columns]
        
        # Add an auto-increment ID if not present
        has_id = any(col['name'].lower() in ['id', f'{table_name}_id'] for col in columns)
        if not has_id:
            column_defs.insert(0, f'{table_name}_id INTEGER PRIMARY KEY AUTOINCREMENT')
            
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {',\n    '.join(column_defs)}\n);"
        
        self.cursor.execute(create_sql)
        self.connection.commit()
        print(f"✓ Created table: {table_name}")
        
    def insert_rows(self, table_name: str, columns: List[str], rows: List[List]) -> int:
        """
        Insert multiple rows into table
        
        Args:
            table_name: Name of the table
            columns: List of column names
            rows: List of row data
            
        Returns:
            Number of rows inserted
        """
        placeholders = ','.join(['?' for _ in columns])
        column_names = ','.join([f'"{col}"' for col in columns])
        
        insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        
        self.cursor.executemany(insert_sql, rows)
        self.connection.commit()
        
        return len(rows)


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
    """Main class for importing CSV data to SQLite"""
    
    MODE_AUTO = 'auto'          # Auto-detect and create/match table
    MODE_CREATE = 'create'      # Force create new table
    MODE_MATCH = 'match'        # Match existing table columns
    MODE_APPEND = 'append'      # Append to existing table
    
    def __init__(self, db_path: str, csv_path: str):
        """
        Initialize CSV importer
        
        Args:
            db_path: Path to SQLite database
            csv_path: Path to CSV file
        """
        self.db_manager = DatabaseManager(db_path)
        self.csv_analyzer = CSVAnalyzer(csv_path)
        self.table_name: Optional[str] = None
        
    def import_csv(self, 
                   table_name: str, 
                   mode: str = MODE_AUTO,
                   init_script: Optional[str] = None,
                   modify_script: Optional[str] = None) -> None:
        """
        Import CSV data to database
        
        Args:
            table_name: Name of target table
            mode: Import mode ('auto', 'create', 'match', 'append')
            init_script: Optional path to initialization SQL script
            modify_script: Optional path to modification SQL script
        """
        self.table_name = table_name
        
        print("\n" + "="*60)
        print("CSV to SQLite Import")
        print("="*60)
        print(f"CSV File: {self.csv_analyzer.csv_path}")
        print(f"Database: {self.db_manager.db_path}")
        print(f"Table: {table_name}")
        print(f"Mode: {mode}")
        print("="*60 + "\n")
        
        # Connect to database
        self.db_manager.connect()
        
        try:
            # Check if we need to initialize database
            if not self.db_manager.db_path.exists() or self.db_manager.db_path.stat().st_size == 0:
                if init_script:
                    print("Database is empty. Running initialization script...")
                    self.db_manager.execute_script(Path(init_script))
                    if modify_script:
                        print("Running modification script...")
                        self.db_manager.execute_script(Path(modify_script))
                        
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
            self.db_manager.disconnect()
            
        print("\n" + "="*60)
        print("✓ Import completed successfully!")
        print("="*60 + "\n")
        
    def _import_auto(self, csv_columns: List[Dict[str, str]]) -> None:
        """Auto mode: detect and handle appropriately"""
        if self.db_manager.table_exists(self.table_name):
            print(f"Table '{self.table_name}' exists. Checking column compatibility...")
            self._import_match(csv_columns)
        else:
            print(f"Table '{self.table_name}' does not exist. Creating new table...")
            self._import_create(csv_columns)
            
    def _import_create(self, csv_columns: List[Dict[str, str]]) -> None:
        """Create mode: create new table and import"""
        if self.db_manager.table_exists(self.table_name):
            print(f"WARNING: Table '{self.table_name}' already exists.")
            response = input("Drop and recreate? (y/N): ")
            if response.lower() == 'y':
                self.db_manager.cursor.execute(f"DROP TABLE {self.table_name}")
                self.db_manager.connection.commit()
                print(f"✓ Dropped table: {self.table_name}")
            else:
                print("Import cancelled.")
                return
                
        # Create table
        self.db_manager.create_table(self.table_name, csv_columns)
        
        # Import data
        self._insert_data(csv_columns)
        
    def _import_match(self, csv_columns: List[Dict[str, str]]) -> None:
        """Match mode: match CSV columns to existing table"""
        if not self.db_manager.table_exists(self.table_name):
            raise ValueError(f"Table '{self.table_name}' does not exist. Use 'create' or 'auto' mode.")
            
        db_columns = self.db_manager.get_table_columns(self.table_name)
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
        if not self.db_manager.table_exists(self.table_name):
            raise ValueError(f"Table '{self.table_name}' does not exist. Use 'create' or 'auto' mode.")
            
        db_columns = self.db_manager.get_table_columns(self.table_name)
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
            inserted = self.db_manager.insert_rows(self.table_name, columns_to_insert, batch)
            total_inserted += inserted
            print(f"  Progress: {total_inserted}/{len(rows)} rows")
            
        print(f"✓ Inserted {total_inserted} rows")


def main():
    """Main function with CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Import CSV data to SQLite database with flexible table handling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto mode - detect and handle appropriately
  python csv_importer.py --csv data.csv --db mydb.db --table players --mode auto
  
  # Create new table from CSV
  python csv_importer.py --csv data.csv --db mydb.db --table players --mode create
  
  # Match columns with existing table
  python csv_importer.py --csv data.csv --db mydb.db --table players --mode match
  
  # Initialize DB first, then import
  python csv_importer.py --csv data.csv --db mydb.db --table players --init initialise_db.sql --modify modify_db.sql
        """
    )
    
    parser.add_argument('--csv', required=True, help='Path to CSV file')
    parser.add_argument('--db', required=True, help='Path to SQLite database')
    parser.add_argument('--table', required=True, help='Target table name')
    parser.add_argument('--mode', 
                       choices=['auto', 'create', 'match', 'append'],
                       default='auto',
                       help='Import mode (default: auto)')
    parser.add_argument('--init', help='Path to initialization SQL script')
    parser.add_argument('--modify', help='Path to modification SQL script')
    
    args = parser.parse_args()
    
    # Create importer and run
    importer = CSVImporter(args.db, args.csv)
    importer.import_csv(
        table_name=args.table,
        mode=args.mode,
        init_script=args.init,
        modify_script=args.modify
    )


if __name__ == "__main__":
    main()
