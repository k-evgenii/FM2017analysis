# Database Setup Scripts

This folder contains scripts to set up the FM2017 SQLite database.

## Files

- `initialise_db.sql` - Creates the initial database schema with all tables
- `modify_db.sql` - Modifies the database schema (adds foreign keys and constraints)
- `setup_database.ps1` - PowerShell script to execute both SQL files
- `setup_database.bat` - Batch script to execute both SQL files (alternative)

## Prerequisites

You need SQLite3 installed and available in your PATH.

### Installing SQLite on Windows:

1. Download the SQLite tools from: https://www.sqlite.org/download.html
   - Look for "sqlite-tools-win32-x86-*.zip"
2. Extract the zip file
3. Add the extracted folder to your system PATH, or copy `sqlite3.exe` to this folder

## Usage

### Using PowerShell (Recommended):

```powershell
# Run from this directory
.\setup_database.ps1

# Or specify a custom database name/path
.\setup_database.ps1 -DatabasePath "my_custom.db"
```

### Using Batch File:

```cmd
# Run from this directory
setup_database.bat

# Or specify a custom database name
setup_database.bat my_custom.db
```

### Manual Execution:

If you prefer to run the SQL files manually:

```bash
# Initialize the database
sqlite3 fm.db ".read initialise_db.sql"

# Apply modifications
sqlite3 fm.db ".read modify_db.sql"
```

## What the Scripts Do

1. **Check Prerequisites**: Verify that SQLite3 is installed
2. **Handle Existing Database**: Prompt to delete if database already exists
3. **Initialize Schema**: Execute `initialise_db.sql` to create all tables
4. **Apply Modifications**: Execute `modify_db.sql` to add foreign keys and constraints
5. **Confirm Success**: Display summary and database location

## Output

The scripts will create a file named `fm.db` (or your custom name) in this directory containing the fully initialized database.

## Troubleshooting

- **"sqlite3 is not installed"**: Install SQLite and add it to your PATH
- **"Permission denied"**: Run the script with appropriate permissions
- **"File not found"**: Ensure you're running the script from the `db-setup` directory
