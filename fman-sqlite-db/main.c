#include <stdio.h>
#include <sqlite3.h>
#include "init_db.h"

int main(void) {
    sqlite3 *db;
    int rc = sqlite3_open("fm.db", &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        return rc;
    }

    // Ensure foreign-key constraints
    sqlite3_exec(db,
        "PRAGMA foreign_keys = ON;",
        NULL, NULL, NULL);

    // Initialize schema (creates tables IF NOT EXISTS, commits at end)
    rc = initialize_db("initialise_db.sql", db);
    if (rc != SQLITE_OK) {
        sqlite3_close(db);
        return rc;
    }

    // --- at this point your DB is ready ---
    printf("Database initialized and ready to go!\n");

    sqlite3_close(db);
    return 0;
}
