#include <stdio.h>
#include "init_db.h" // Include the header file

int main() {
    const char *db_name = "reaction_storage.db";

    // Initialize the database
    if (init_database(db_name) != 0) {
        fprintf(stderr, "Failed to initialize the database\n");
        return 1;
    }

    return 0; // Success
}