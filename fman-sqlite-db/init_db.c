#include "init_db.h"
#include <stdio.h>
#include <stdlib.h>

int initialize_db(const char *sql_filename, sqlite3 *db) {
    FILE *f = fopen(sql_filename, "rb");
    if (!f) {
        perror("fopen");
        return SQLITE_CANTOPEN;
    }

    // load whole file into memory
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    rewind(f);
    char *sql = malloc(sz + 1);
    if (!sql) {
        fclose(f);
        return SQLITE_NOMEM;
    }
    fread(sql, 1, sz, f);
    sql[sz] = '\0';
    fclose(f);

    char *err = NULL;
    int rc = sqlite3_exec(db, sql, NULL, NULL, &err);
    free(sql);

    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err);
        sqlite3_free(err);
    }
    return rc;
}
