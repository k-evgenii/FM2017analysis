#include <stdio.h>
#include <sqlite3.h>
#include "init_db.h" // Include the header file

int init_database(const char *db_name) {
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

    // Create SQL tables




    
const char *createPlayersTableSQL = R"(
CREATE TABLE IF NOT EXISTS players (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(30) NOT NULL,
    NATIONID INT NOT NULL,
    BORN INT NOT NULL,
    AGE INT NOT NULL,
    INTCAPS INT NOT NULL,
    INTGOALS INT NOT NULL,
    U21CAPS INT NOT NULL,
    U21GOALS INT NOT NULL,
    HEIGHT INT NOT NULL,
    WEIGHT INT NOT NULL,
    AERIALABILITY INT NOT NULL,
    COMMANDOFAREA INT NOT NULL,
    COMMUNICATION INT NOT NULL,
    ECCENTRICITY INT NOT NULL,
    HANDLING INT NOT NULL,
    KICKING INT NOT NULL,
    ONEONONES INT NOT NULL,
    REFLEXES INT NOT NULL,
    RUSHINGOUT INT NOT NULL,
    TENDENCYTOPUNCH INT NOT NULL,
    THROWING INT NOT NULL,
    CORNERS INT NOT NULL,
    CROSSING INT NOT NULL,
    DRIBBLING INT NOT NULL,
    FINISHING INT NOT NULL,
    FIRSTTOUCH INT NOT NULL,
    FREEKICKS INT NOT NULL,
    HEADING INT NOT NULL,
    LONGSHOTS INT NOT NULL,
    LONGTHROWS INT NOT NULL,
    MARKING INT NOT NULL,
    PASSING INT NOT NULL,
    PENALTYTAKING INT NOT NULL,
    TACKLING INT NOT NULL,
    TECHNIQUE INT NOT NULL,
    AGGRESSION INT NOT NULL,
    ANTICIPATION INT NOT NULL,
    BRAVERY INT NOT NULL,
    COMPOSURE INT NOT NULL,
    CONCENTRATION INT NOT NULL,
    VISION INT NOT NULL,
    DECISIONS INT NOT NULL,
    DETERMINATION INT NOT NULL,
    FLAIR INT NOT NULL,
    LEADERSHIP INT NOT NULL,
    OFFTHEBALL INT NOT NULL,
    POSITIONING INT NOT NULL,
    TEAMWORK INT NOT NULL,
    WORKRATE INT NOT NULL,
    ACCELERATION INT NOT NULL,
    AGILITY INT NOT NULL,
    BALANCE INT NOT NULL,
    JUMPING INT NOT NULL,
    LEFTFOOT INT NOT NULL,
    NATURALFITNESS INT NOT NULL,
    PACE INT NOT NULL,
    RIGHTFOOT INT NOT NULL,
    STAMINA INT NOT NULL,
    STRENGTH INT NOT NULL,
    CONSISTENCY INT NOT NULL,
    DIRTINESS INT NOT NULL,
    IMPORTANTMATCHES INT NOT NULL,
    INJURYPRONESS INT NOT NULL,
    VERSATILITY INT NOT NULL,
    ADAPTABILITY INT NOT NULL,
    AMBITION INT NOT NULL,
    LOYALTY INT NOT NULL,
    PRESSURE INT NOT NULL,
    PROFESSIONAL INT NOT NULL,
    SPORTSMANSHIP INT NOT NULL,
    TEMPERAMENT INT NOT NULL,
    CONTROVERSY INT NOT NULL,
    GOALKEEPER INT NOT NULL,
    SWEEPER INT NOT NULL,
    STRIKER INT NOT NULL,
    ATTACKINGMIDCENTRAL INT NOT NULL,
    ATTACKINGMIDLEFT INT NOT NULL,
    ATTACKINGMIDRIGHT INT NOT NULL,
    DEFENDERCENTRAL INT NOT NULL,
    DEFENDERLEFT INT NOT NULL,
    DEFENDERRIGHT INT NOT NULL,
    DEFENSIVEMIDFIELDER INT NOT NULL,
    MIDFIELDCENTRAL INT NOT NULL,
    MIDFIELDLEFT INT NOT NULL,
    MIDFIELDRIGHT INT NOT NULL,
    WINGBACKLEFT INT NOT NULL,
    WINGBACKRIGHT INT NOT NULL
);
)";

const char *createPositionsTableSQL =  R"(
CREATE TABLE IF NOT EXISTS positions(                                                                
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY (team_id) REFERENCES team_table(team_id),
    Position VARCHAR(5) NOT NULL,
    Team VARCHAR(30) NOT NULL,
);
)";

const char *createTeamsTableSQL = 
"CREATE TABLE IF NOT EXISTS teams("
                                                                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                                "NAME VARCHAR(30) NOT NULL,"
                                                                "NATIONID INT NOT NULL,"
                                                                "DIVISION VARCHAR(30) NULL,"
                                                                "AVERAGE AGE FLOAT NULL,"
                                                                "BALANCE TEXT NULL,"
                                                                "TRANSFER BUDGET TEXT NULL,"
                                                                "WAGE BUDGET TEXT NULL,"
                                                                "TRAINING FACILITIES TEXT NULL,"
                                                                "YOUTH FACILITIES TEXT NOT NULL,"
                                                                "YOUTH ACADEMY TEXT NOT NULL,"
                                                                "YOUTH RECRUITMENT TEXT NULL,"
                                                                "STADIUM CAPACITY INT NOT NULL,"
                                                                "AVERAGE ATTENDANCE INT NOT NULL,"
                                                                "ABILITY FLOAT NOT NULL,"
                                                                "POTENTIAL FLOAT NOT NULL,
                                                                );";

const char *createStaffTableSQL = "CREATE TABLE IF NOT EXISTS staff("
                                                                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                                "NAME VARCHAR(30) NOT NULL,"
                                                                "AGE INT NOT NULL,"
                                                                "NATIONALITY VARCHAR(15) NOT NULL,"
                                                                "TEAM VARCHAR(15) NOT NULL,"
                                                                "CLUB JOB VARCHAR(45) NOT NULL,"
                                                                "CLUB CONTRACT TYPE VARCHAR(15) NOT NULL,"
                                                                "WAGE VARCHAR(15) NOT NULL,"
                                                                "CONTRACT EXPIRES DATE NULL,"
                                                                "CONTRACT SIGNED DATE NULL,"
                                                                "JUDGING PLAYER ABILITY INT NOT NULL,"
                                                                "JUDGING PLAYER POTENTIAL INT NOT NULL,"
                                                                "MANAGER RATING FLOAT NOT NULL,"
                                                                "ASSISTANT RATING FLOAT NOT NULL,"
                                                                "COACH RATING FLOAT NOT NULL,"
                                                                "SCOUT RATING FLOAT NOT NULL,"
                                                                "PHYSIO RATING FLOAT NOT NULL,"
                                                                "STRENGTH TRAINING INT NOT NULL,"
                                                                "AEROBIC TRAINING INT NOT NULL,"
                                                                "GK HANDLING TRAINING INT NOT NULL,"
                                                                "GK SHOT STOPPING TRAINING INT NOT NULL,"
                                                                "TACTICS TRAINING INT NOT NULL,"
                                                                "BALL CONTROL TRAINING INT NOT NULL,"
                                                                "DEFENDING TRAINING INT NOT NULL,"
                                                                "ATTACKING TRAINING INT NOT NULL,"
                                                                "SHOOTING TRAINING INT NOT NULL,"
                                                                "HOME REP INT NOT NULL,"
                                                                "WORLD REP INT NOT NULL,"
                                                                "CURRENT REP INT NOT NULL,
                                                                );";    
 
                                                                
const char *createStaffTableSQL = "CREATE TABLE IF NOT EXISTS Loaned_Out_Players("
                                                                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                                "PLAYER ID ,"
                                                                "TEAM ID ,"
                                                                "NAME VARCHAR(30) NOT NULL,"
                                                                "LOAN TEAM ID INT NOT NULL,"
                                                                "LOAN EXPIRES DATE NOT NULL,""
                                                                );";    

const char *createStaffTableSQL = "CREATE TABLE IF NOT EXISTS Current_Players("
                                                                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                                "PLAYER ID ,"
                                                                "NAME VARCHAR(30) NOT NULL,"
                                                                "AGE INT NOT NULL,"
                                                                "NATIONALITY VARCHAR(15) NOT NULL,"
                                                                "CONTRACTED CLUB VARCHAR(30) NOT NULL,"
                                                                "WAGE VARCHAR(15) NOT NULL,"
                                                                "CONTRACT EXPIRES DATE NULL,"
                                                                "CONTRACT SIGNED DATE NULL,"
                                                                "VALUE VARCHAR(15) NOT NULL,"
                                                                "ESTIMATED COST VARCHAR(15) NOT NULL,"
                                                                "TEAM ID ,"
                                                                "CURRENT ABILITY INT NOT NULL,"
                                                                "POTENTIAL ABILITY INT NOT NULL,"
                                                                "CA REMAINING INT NOT NULL,
                                                                );";        

                                                                
const char *createStaffTableSQL = "CREATE TABLE IF NOT EXISTS Peak_Players("
                                                                "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                                                                "PLAYER ID ,"
                                                                "TEAM ID ,
                                                                );";                                                                    

    rc = sqlite3_exec(db, createTableSQL, NULL, NULL, &errMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", errMsg);
        sqlite3_free(errMsg);
        sqlite3_close(db);
        return 1; // Exit with error
    }
    printf("Table 'PERSON' created successfully\n");

    // Close the database connection
    sqlite3_close(db);
    printf("Database connection closed\n");
    return 0; // Success
}