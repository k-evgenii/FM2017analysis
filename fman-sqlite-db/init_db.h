#ifndef INIT_DB_H
#define INIT_DB_H

#include <sqlite3.h>

/**
 * Reads the given SQL file and executes it on `db`.
 * Returns SQLITE_OK on success, or an SQLite error code.
 */
int initialize_db(const char *sql_filename, sqlite3 *db);

#endif /* INIT_DB_H */
