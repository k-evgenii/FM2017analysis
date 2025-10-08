#!/usr/bin/env python3
"""
FM2017 Database Setup Script (OOP Version with Abstract Base Classes)
Initializes and modifies the database using abstract database connections
Supports SQLite, MySQL, and other databases through the DatabaseConnection interface
"""

import sys
from pathlib import Path
from typing import Optional, List
from database_abc import DatabaseConnection, create_database_connection


class DatabaseSetup:
    """Handles database initialization and setup using abstract database connection"""
    
    def __init__(self, db_connection: DatabaseConnection, script_dir: Path):
        """
        Initialize database setup manager
        
        Args:
            db_connection: DatabaseConnection instance (SQLite, MySQL, etc.)
            script_dir: Directory containing SQL scripts
        """
        self.db_connection: DatabaseConnection = db_connection
        self.script_dir: Path = script_dir
        
    def check_sql_files(self, sql_files: List[str]) -> bool:
        """
        Check if required SQL files exist
        
        Args:
            sql_files: List of SQL filenames to check
            
        Returns:
            True if all files exist, False otherwise
        """
        missing_files = []
        for sql_file in sql_files:
            file_path = self.script_dir / sql_file
            if not file_path.exists():
                missing_files.append(file_path)
                
        if missing_files:
            print("ERROR: Missing SQL files:")
            for file_path in missing_files:
                print(f"  ✗ {file_path}")
            return False
            
        return True
        
    def connect(self) -> None:
        """Establish connection to database"""
        self.db_connection.connect()
        
    def disconnect(self) -> None:
        """Close database connection"""
        self.db_connection.disconnect()
            
    def execute_sql_file(self, sql_file: str) -> None:
        """
        Read and execute an SQL file
        
        Args:
            sql_file: Name of the SQL file to execute
        """
        sql_file_path = self.script_dir / sql_file
        
        print(f"Reading {sql_file}...")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        print(f"Executing {sql_file}...")
        self.db_connection.execute_script(sql_script)
        print(f"✓ {sql_file} executed successfully")
        
    def setup(self, 
              init_script: str = "initialise_db.sql", 
              modify_script: str = "modify_db.sql",
              force: bool = False,
              db_file_path: Optional[Path] = None) -> int:
        """
        Run complete database setup
        
        Args:
            init_script: Name of initialization SQL script
            modify_script: Name of modification SQL script
            force: If True, skip confirmation for overwriting existing DB
            db_file_path: Optional path to database file (for display/deletion, SQLite only)
            
        Returns:
            0 on success, 1 on error
        """
        print("=" * 60)
        print("FM2017 Database Setup")
        print("=" * 60)
        if db_file_path:
            print(f"Database path: {db_file_path}")
        else:
            print(f"Database: {self.db_connection.db_path}")
        print("=" * 60)
        print()
        
        # Check if database file already exists (SQLite only)
        if db_file_path and db_file_path.exists() and not force:
            print(f"WARNING: Database already exists at {db_file_path}")
            response = input("Do you want to delete it and create a new one? (y/N): ")
            if response.lower() != 'y':
                print("Database setup cancelled.")
                return 0
            db_file_path.unlink()
            print("✓ Existing database deleted.")
            print()
        elif db_file_path and db_file_path.exists() and force:
            db_file_path.unlink()
            print("✓ Existing database deleted (force mode).")
            print()
            
        # Check SQL files exist
        if not self.check_sql_files([init_script, modify_script]):
            return 1
            
        try:
            # Connect to database
            self.connect()
            
            # Step 1: Initialize database
            print()
            print("Step 1: Initializing database schema...")
            print("-" * 60)
            self.execute_sql_file(init_script)
            
            # Step 2: Modify database
            print()
            print("Step 2: Applying database modifications...")
            print("-" * 60)
            self.execute_sql_file(modify_script)
            
            # Close connection
            print()
            self.disconnect()
            
            # Success message
            print()
            print("=" * 60)
            print("✓ Database setup complete!")
            print("=" * 60)
            if db_file_path:
                print(f"Database location: {db_file_path}")
                print()
                print("You can now use the database with:")
                print(f'  sqlite3 {db_file_path}')
                print(f'  python -c "import sqlite3; conn = sqlite3.connect(\'{db_file_path}\')"')
            else:
                print(f"Database: {self.db_connection.db_path}")
            print()
            
            return 0
            
        except Exception as e:
            print(f"\nERROR: Database error occurred: {e}")
            try:
                self.disconnect()
            except:
                pass
            return 1


def main():
    """Main function with CLI interface"""
    import argparse
    
    # Get script directory
    script_dir = Path(__file__).parent.absolute()
    
    parser = argparse.ArgumentParser(
        description='Initialize FM2017 database with schema and modifications',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create SQLite database with default name (fm.db)
  python setup_database.py
  
  # Create SQLite database with custom name
  python setup_database.py --db my_database.db
  
  # Force overwrite without confirmation
  python setup_database.py --force
  
  # Use MySQL instead of SQLite
  python setup_database.py --db-type mysql --db mydb --host localhost --user root --password pass
  
  # Use custom SQL scripts
  python setup_database.py --init custom_init.sql --modify custom_modify.sql
        """
    )
    
    parser.add_argument('--db', 
                       default='fm.db',
                       help='Database filename (SQLite) or database name (MySQL)')
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
    parser.add_argument('--init',
                       default='initialise_db.sql',
                       help='Initialization SQL script (default: initialise_db.sql)')
    parser.add_argument('--modify',
                       default='modify_db.sql',
                       help='Modification SQL script (default: modify_db.sql)')
    parser.add_argument('--force',
                       action='store_true',
                       help='Force overwrite existing database without confirmation')
    
    args = parser.parse_args()
    
    # Create database connection based on type
    if args.db_type == 'sqlite':
        db_path = script_dir / args.db
        db_conn = create_database_connection('sqlite', db_path=str(db_path))
    elif args.db_type == 'mysql':
        db_path = None
        db_conn = create_database_connection('mysql',
                                            db_path=args.db,
                                            host=args.host,
                                            port=args.port,
                                            user=args.user,
                                            password=args.password)
    else:
        print(f"ERROR: Unsupported database type: {args.db_type}")
        return 1
    
    # Create setup manager and run
    setup = DatabaseSetup(db_conn, script_dir)
    return setup.setup(
        init_script=args.init,
        modify_script=args.modify,
        force=args.force,
        db_file_path=db_path
    )


if __name__ == "__main__":
    sys.exit(main())
