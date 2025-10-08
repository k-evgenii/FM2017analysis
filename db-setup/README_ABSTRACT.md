# Database Setup - Abstract Architecture

This folder contains database setup and CSV import scripts with an **abstract base class architecture** that supports multiple database backends (SQLite, MySQL, PostgreSQL, etc.).

## Why Abstract Classes?

This design enables:
- **Easy migration** between database types (SQLite → MySQL → PostgreSQL)
- **Code reusability** for different projects (FM2017, Polymarket trades, etc.)
- **Single codebase** supports multiple backends
- **Type-safe** with proper abstractions

## Architecture Overview

### Abstract Base Classes (`database_abc.py`)

```
DatabaseConnection (ABC)
├── SQLiteConnection
├── MySQLConnection
└── [Future: PostgreSQLConnection, etc.]
```

**`DatabaseConnection`** defines the interface:
- `connect()` / `disconnect()`
- `execute_script()` / `execute_query()`
- `table_exists()` / `get_table_columns()`
- `create_table()` / `insert_rows()`

Each database type implements these methods according to its own SQL dialect and connection requirements.

## Files

| File | Description |
|------|-------------|
| `database_abc.py` | Abstract base classes and database implementations |
| `setup_database.py` | Database initialization script (uses ABC) |
| `csv_importer.py` | CSV import tool (OOP, prototype - not yet using ABC) |
| `initialise_db.sql` | Initial schema creation |
| `modify_db.sql` | Schema modifications (adds foreign keys) |
| `setup_database.ps1` | PowerShell wrapper (legacy) |
| `setup_database.bat` | Batch wrapper (legacy) |

## Quick Start

### SQLite (Default)

```bash
# Basic setup
python setup_database.py

# Custom database name
python setup_database.py --db my_database.db

# Force overwrite without confirmation
python setup_database.py --force
```

### MySQL

```bash
# Setup MySQL database
python setup_database.py --db-type mysql --db fm2017 \
    --host localhost --user root --password mypass
```

## Detailed Usage

### 1. Setup SQLite Database

```bash
# Default (creates fm.db)
python setup_database.py

# Custom database name
python setup_database.py --db my_fm_data.db

# Use custom SQL scripts
python setup_database.py --init custom_init.sql --modify custom_modify.sql

# Force overwrite existing database
python setup_database.py --force
```

### 2. Setup MySQL Database

```bash
# Basic MySQL setup
python setup_database.py --db-type mysql --db fm2017 \
    --user root --password mypass

# MySQL with custom host/port
python setup_database.py --db-type mysql --db fm2017 \
    --host 192.168.1.100 --port 3306 \
    --user admin --password secret
```

### 3. CSV Import (Future - when integrated with ABC)

```bash
# Auto mode - smart detection
python csv_importer.py --csv players.csv --db fm.db --table players --mode auto

# Create new table from CSV
python csv_importer.py --csv data.csv --db fm.db --table my_table --mode create

# Match columns with existing table
python csv_importer.py --csv data.csv --db fm.db --table players --mode match
```

## Extending to Other Projects

### Example: Polymarket Trades Database

```python
from database_abc import create_database_connection, DatabaseSetup
from pathlib import Path

# Create connection - easily switch between SQLite/MySQL!
db_conn = create_database_connection('sqlite', db_path='polymarket.db')
# OR
db_conn = create_database_connection('mysql', 
                                    db_path='polymarket',
                                    host='localhost',
                                    user='root',
                                    password='pass')

# Setup with your own SQL scripts
script_dir = Path('./polymarket_scripts')
setup = DatabaseSetup(db_conn, script_dir)

setup.setup(
    init_script='polymarket_init.sql',
    modify_script='polymarket_modify.sql',
    force=True
)
```

### Adding New Database Backend (e.g., PostgreSQL)

```python
from database_abc import DatabaseConnection

class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL implementation"""
    
    def __init__(self, db_path: str, host: str = 'localhost', 
                 port: int = 5432, user: str = 'postgres', password: str = ''):
        super().__init__(db_path)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
    
    def connect(self) -> None:
        """Connect to PostgreSQL"""
        import psycopg2
        self.connection = psycopg2.connect(
            dbname=self.db_path,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.connection.cursor()
        print(f"✓ Connected to PostgreSQL database: {self.db_path}")
    
    # Implement all other abstract methods...
    def table_exists(self, table_name: str) -> bool:
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            )
        """
        return self.execute_query(query, (table_name,))[0][0]
    
    # ... etc.
```

Then update the factory function in `database_abc.py`:

```python
def create_database_connection(db_type: str, **kwargs) -> DatabaseConnection:
    if db_type == 'sqlite':
        return SQLiteConnection(kwargs.get('db_path', 'database.db'))
    elif db_type == 'mysql':
        return MySQLConnection(...)
    elif db_type == 'postgresql':  # ← Add this
        return PostgreSQLConnection(...)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
```

## Database Schema

### FM2017 Tables

- **`players`** - Player information and attributes (60+ columns)
- **`teams`** - Team data
- **`nations`** - National teams  
- **`positions`** - Player positions (with foreign keys)
- **`peak_players`** - Players at peak performance
- **`loans`** - Loan transactions

See `initialise_db.sql` for full schema details.

## Dependencies

### Required (Built-in)
- `sqlite3` - SQLite database
- `pathlib` - Path handling
- `typing` - Type hints
- `csv` - CSV handling
- `abc` - Abstract base classes

### Optional
- `mysql-connector-python` - For MySQL support
  ```bash
  pip install mysql-connector-python
  ```
- `psycopg2` - For PostgreSQL support
  ```bash
  pip install psycopg2-binary
  ```

## Design Patterns Used

| Pattern | Where | Why |
|---------|-------|-----|
| **Abstract Factory** | `create_database_connection()` | Create database connections without knowing concrete class |
| **Strategy** | `DatabaseConnection` implementations | Interchangeable database backends |
| **Template Method** | `DatabaseSetup.setup()` | Define skeleton of setup process |
| **Dependency Injection** | `DatabaseSetup.__init__()` | Loose coupling, easy testing |

## Best Practices

- **Type Hints** - Full type annotations (`Optional[str]`, `List[Dict]`, etc.)  
- **Docstrings** - Every class and method documented  
- **Error Handling** - Proper exception handling and cleanup  
- **SOLID Principles**:
- **S**ingle Responsibility - Each class has one purpose
- **O**pen/Closed - Open for extension, closed for modification
- **L**iskov Substitution - All `DatabaseConnection` implementations are interchangeable
- **I**nterface Segregation - Clean, focused interfaces
- **D**ependency Inversion - Depend on `DatabaseConnection` abstraction

## Future Enhancements

- [ ] Integrate `csv_importer.py` with abstract classes
- [ ] Add PostgreSQL support
- [ ] Add MongoDB/NoSQL support
- [ ] Implement connection pooling
- [ ] Add transaction management
- [ ] Create database migration tool
- [ ] Add data validation layer
- [ ] Implement ORM-style query builder
- [ ] Add async database support

## Contributing

When adding new database support:

1. Create new class inheriting from `DatabaseConnection`
2. Implement all abstract methods
3. Handle database-specific SQL dialect differences
4. Add type mappings (e.g., SQLite `INTEGER` → MySQL `INT`)
5. Update factory function in `database_abc.py`
6. Add usage examples to this README
7. Test with sample data

## Example: Complete Workflow

```bash
# 1. Setup SQLite database
python setup_database.py --db fm2017.db

# 2. Verify database created
ls -la fm2017.db

# 3. Query database
sqlite3 fm2017.db "SELECT name FROM sqlite_master WHERE type='table';"

# 4. Later: Switch to MySQL (same code!)
python setup_database.py --db-type mysql --db fm2017 \
    --host localhost --user root --password mypass
```

## Related Documentation

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)
- [Python ABC Module](https://docs.python.org/3/library/abc.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## License

See repository root LICENSE file.

---

**Questions or Issues?** Open an issue in the repository!
