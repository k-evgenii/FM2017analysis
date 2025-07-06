#ifndef INIT_DB_H
#define INIT_DB_H

// Function to initialize the database and execute the SQL script
int init_database(const char *db_name, const char *sql_file);

#endif // INIT_DB_H