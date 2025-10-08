#!/usr/bin/env python3
"""
Abstract Database Classes
Provides abstract base classes for database operations that can be implemented
for different database backends (SQLite, MySQL, PostgreSQL, etc.)
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import sqlite3


class DatabaseConnection(ABC):
    """Abstract base class for database connections"""
    
    def __init__(self, db_path: str):
        """
        Initialize database connection
        
        Args:
            db_path: Path or connection string to database
        """
        self.db_path: str = db_path
        self.connection = None
        self.cursor = None
        
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to database"""
        pass
        
    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection"""
        pass
        
    @abstractmethod
    def execute_script(self, sql_script: str) -> None:
        """
        Execute SQL script
        
        Args:
            sql_script: SQL script content to execute
        """
        pass
        
    @abstractmethod
    def execute_query(self, query: str, params: tuple = ()) -> List[tuple]:
        """
        Execute a query and return results
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result tuples
        """
        pass
        
    @abstractmethod
    def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists in database
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists, False otherwise
        """
        pass
        
    @abstractmethod
    def get_table_columns(self, table_name: str) -> List[str]:
        """
        Get list of column names for a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column names
        """
        pass
        
    @abstractmethod
    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> None:
        """
        Create a new table with specified columns
        
        Args:
            table_name: Name of the table to create
            columns: List of dicts with 'name' and 'type' keys
        """
        pass
        
    @abstractmethod
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
        pass
        
    def commit(self) -> None:
        """Commit current transaction"""
        if self.connection:
            self.connection.commit()


class SQLiteConnection(DatabaseConnection):
    """SQLite implementation of DatabaseConnection"""
    
    def connect(self) -> None:
        """Establish connection to SQLite database"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        print(f"✓ Connected to SQLite database: {Path(self.db_path).name}")
        
    def disconnect(self) -> None:
        """Close SQLite database connection"""
        if self.connection:
            self.connection.commit()
            self.connection.close()
            print("✓ Database connection closed")
            
    def execute_script(self, sql_script: str) -> None:
        """Execute SQL script in SQLite"""
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")
        self.cursor.executescript(sql_script)
        self.connection.commit()
        
    def execute_query(self, query: str, params: tuple = ()) -> List[tuple]:
        """Execute query in SQLite"""
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.cursor.execute(query, params).fetchall()
        
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in SQLite database"""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.execute_query(query, (table_name,))
        return len(result) > 0
        
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get list of column names for a SQLite table"""
        query = f"PRAGMA table_info({table_name})"
        columns = self.execute_query(query)
        return [col[1] for col in columns]  # col[1] is the column name
        
    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> None:
        """Create a new table in SQLite"""
        column_defs = [f'"{col["name"]}" {col["type"]}' for col in columns]
        
        # Add an auto-increment ID if not present
        has_id = any(col['name'].lower() in ['id', f'{table_name}_id'] for col in columns)
        if not has_id:
            column_defs.insert(0, f'{table_name}_id INTEGER PRIMARY KEY AUTOINCREMENT')
        
        columns_str = ',\n    '.join(column_defs)
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_str}\n);"
        
        self.cursor.execute(create_sql)
        self.connection.commit()
        print(f"✓ Created table: {table_name}")
        
    def insert_rows(self, table_name: str, columns: List[str], rows: List[List]) -> int:
        """Insert multiple rows into SQLite table"""
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")
            
        placeholders = ','.join(['?' for _ in columns])
        column_names = ','.join([f'"{col}"' for col in columns])
        
        insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        
        self.cursor.executemany(insert_sql, rows)
        self.connection.commit()
        
        return len(rows)


class MySQLConnection(DatabaseConnection):
    """MySQL implementation of DatabaseConnection (placeholder for future implementation)"""
    
    def __init__(self, db_path: str, host: str = 'localhost', port: int = 3306, 
                 user: str = 'root', password: str = ''):
        """
        Initialize MySQL connection
        
        Args:
            db_path: Database name
            host: MySQL host
            port: MySQL port
            user: MySQL user
            password: MySQL password
        """
        super().__init__(db_path)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
    def connect(self) -> None:
        """Establish connection to MySQL database"""
        try:
            import mysql.connector  # type: ignore
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_path
            )
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to MySQL database: {self.db_path}")
        except ImportError:
            raise ImportError("mysql-connector-python not installed. Install with: pip install mysql-connector-python")
            
    def disconnect(self) -> None:
        """Close MySQL database connection"""
        if self.connection:
            self.connection.commit()
            self.connection.close()
            print("✓ Database connection closed")
            
    def execute_script(self, sql_script: str) -> None:
        """Execute SQL script in MySQL"""
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")
        # MySQL doesn't support executescript, so we split by semicolons
        for statement in sql_script.split(';'):
            statement = statement.strip()
            if statement:
                self.cursor.execute(statement)
        self.connection.commit()
        
    def execute_query(self, query: str, params: tuple = ()) -> List[tuple]:
        """Execute query in MySQL"""
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
        
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists in MySQL database"""
        query = "SHOW TABLES LIKE %s"
        result = self.execute_query(query, (table_name,))
        return len(result) > 0
        
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get list of column names for a MySQL table"""
        query = f"DESCRIBE {table_name}"
        columns = self.execute_query(query)
        return [col[0] for col in columns]  # col[0] is the column name
        
    def create_table(self, table_name: str, columns: List[Dict[str, str]]) -> None:
        """Create a new table in MySQL"""
        # Convert SQLite types to MySQL types
        type_mapping = {
            'INTEGER': 'INT',
            'REAL': 'FLOAT',
            'TEXT': 'TEXT',
            'DATE': 'DATE'
        }
        
        column_defs = []
        for col in columns:
            mysql_type = type_mapping.get(col['type'].upper(), col['type'])
            column_defs.append(f"`{col['name']}` {mysql_type}")
        
        # Add an auto-increment ID if not present
        has_id = any(col['name'].lower() in ['id', f'{table_name}_id'] for col in columns)
        if not has_id:
            column_defs.insert(0, f'{table_name}_id INT PRIMARY KEY AUTO_INCREMENT')
        
        columns_str = ',\n    '.join(column_defs)
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_str}\n);"
        
        self.cursor.execute(create_sql)
        self.connection.commit()
        print(f"✓ Created table: {table_name}")
        
    def insert_rows(self, table_name: str, columns: List[str], rows: List[List]) -> int:
        """Insert multiple rows into MySQL table"""
        if not self.cursor:
            raise RuntimeError("Database not connected. Call connect() first.")
            
        placeholders = ','.join(['%s' for _ in columns])  # MySQL uses %s, not ?
        column_names = ','.join([f'`{col}`' for col in columns])
        
        insert_sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        
        self.cursor.executemany(insert_sql, rows)
        self.connection.commit()
        
        return len(rows)


def create_database_connection(db_type: str, **kwargs) -> DatabaseConnection:
    """
    Factory function to create appropriate database connection
    
    Args:
        db_type: Type of database ('sqlite', 'mysql', 'postgresql')
        **kwargs: Database-specific connection parameters
        
    Returns:
        DatabaseConnection instance
        
    Examples:
        # SQLite
        conn = create_database_connection('sqlite', db_path='mydb.db')
        
        # MySQL
        conn = create_database_connection('mysql', db_path='mydb', 
                                         host='localhost', user='root', password='pass')
    """
    db_type = db_type.lower()
    
    if db_type == 'sqlite':
        return SQLiteConnection(kwargs.get('db_path', 'database.db'))
    elif db_type == 'mysql':
        return MySQLConnection(
            db_path=kwargs.get('db_path', 'database'),
            host=kwargs.get('host', 'localhost'),
            port=kwargs.get('port', 3306),
            user=kwargs.get('user', 'root'),
            password=kwargs.get('password', '')
        )
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
