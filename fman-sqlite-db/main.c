#include <stdio.h>
#include <stdlib.h>
#include "init_db.h"

int main() {
    const char *db_name = "football_manager.db";
    const char *sql_file = "initialise_db.sql";

    // Initialize the database
    if (init_database(db_name, sql_file) != 0) {
        fprintf(stderr, "Failed to initialize the database\n");
        return 1;
    }

    printf("Database initialized successfully\n");
    return 0; // Success
}