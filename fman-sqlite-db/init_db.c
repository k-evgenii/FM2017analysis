#include <stdio.h>
#include <stdlib.h>
#include <sqlite3.h>
#include "init_db.h"

// Function to load SQL script from a file
static char *load_sql_from_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        perror("Failed to open SQL file");
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *sql = malloc(length + 1);
    if (!sql) {
        perror("Failed to allocate memory for SQL");
        fclose(file);
        return NULL;
    }

    fread(sql, 1, length, file);
    sql[length] = '\0';
    fclose(file);

    return sql;
}

// Function to initialize the database and execute the SQL script
int init_database(const char *db_name, const char *sql_file) {
    sqlite3 *db;
    char *errMsg = 0;
    int rc;

    // Open or create the database file
    rc = sqlite3_open(db_name, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Can't open or create database: %s\n", sqlite3_errmsg(db));
        return 1; // Exit with error
    }
    printf("Database '%s' created or opened successfully\n", db_name);

    // Load SQL script from file
    char *sql_script = load_sql_from_file(sql_file);
    if (!sql_script) {
        sqlite3_close(db);
        return 1; // Exit with error
    }

    // Enable foreign key support
    rc = sqlite3_exec(db, "PRAGMA foreign_keys = ON;", NULL, NULL, &errMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to enable foreign key support: %s\n", errMsg);
        sqlite3_free(errMsg);
        free(sql_script);
        sqlite3_close(db);
        return 1; // Exit with error
    }

    // Execute SQL script
    rc = sqlite3_exec(db, sql_script, NULL, NULL, &errMsg);
    free(sql_script);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", errMsg);
        sqlite3_free(errMsg);
        sqlite3_close(db);
        return 1; // Exit with error
    }

    printf("Database schema initialized successfully\n");
    sqlite3_close(db);
    return 0; // Success
}