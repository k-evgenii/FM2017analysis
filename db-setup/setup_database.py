#!/usr/bin/env python3
"""
FM2017 Database Setup Script
Initializes and modifies the SQLite database using Python's built-in sqlite3 module
"""

import sqlite3
import os
import sys
from pathlib import Path


def execute_sql_file(cursor, sql_file_path):
    """Read and execute an SQL file"""
    print(f"Reading {sql_file_path}...")
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    print(f"Executing {sql_file_path}...")
    cursor.executescript(sql_script)
    print(f"✓ {sql_file_path} executed successfully")


def main():
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    
    # Database name (can be overridden by command line argument)
    db_name = sys.argv[1] if len(sys.argv) > 1 else "fm.db"
    db_path = script_dir / db_name
    
    print("=" * 50)
    print("FM2017 Database Setup")
    print("=" * 50)
    print()
    print(f"Database path: {db_path}")
    print()
    
    # Check if database already exists
    if db_path.exists():
        print(f"WARNING: Database already exists at {db_path}")
        response = input("Do you want to delete it and create a new one? (y/N): ")
        if response.lower() != 'y':
            print("Database setup cancelled.")
            return 0
        db_path.unlink()
        print("Existing database deleted.")
        print()
    
    # SQL files
    init_sql = script_dir / "initialise_db.sql"
    modify_sql = script_dir / "modify_db.sql"
    
    # Check if SQL files exist
    if not init_sql.exists():
        print(f"ERROR: {init_sql} not found!")
        return 1
    if not modify_sql.exists():
        print(f"ERROR: {modify_sql} not found!")
        return 1
    
    try:
        # Connect to database (creates it if it doesn't exist)
        print("Connecting to database...")
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Step 1: Initialize database
        print()
        print("Step 1: Initializing database schema...")
        print("-" * 50)
        execute_sql_file(cursor, init_sql)
        conn.commit()
        
        # Step 2: Modify database
        print()
        print("Step 2: Applying database modifications...")
        print("-" * 50)
        execute_sql_file(cursor, modify_sql)
        conn.commit()
        
        # Close connection
        conn.close()
        
        # Success message
        print()
        print("=" * 50)
        print("✓ Database setup complete!")
        print("=" * 50)
        print(f"Database location: {db_path}")
        print()
        print("You can now use the database with:")
        print(f'  python -c "import sqlite3; conn = sqlite3.connect(\'{db_path}\'); ..."')
        print()
        
        return 0
        
    except sqlite3.Error as e:
        print(f"\nERROR: SQLite error occurred: {e}")
        return 1
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
