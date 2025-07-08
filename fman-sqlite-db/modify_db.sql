PRAGMA foreign_keys = OFF;    -- Temporarily allow schema changes
BEGIN TRANSACTION;

-- ===== 1) positions =====
ALTER TABLE positions RENAME TO positions_old;

CREATE TABLE positions (
    player_id  INTEGER NOT NULL,
    team_id    INTEGER NOT NULL,
    position   VARCHAR(5) NOT NULL,
    PRIMARY KEY (player_id, team_id, position),
    FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE,
    FOREIGN KEY (team_id)
        REFERENCES teams(team_id)
        ON DELETE CASCADE
);

INSERT INTO positions (player_id, team_id, position)
SELECT player_id, team_id, position FROM positions_old;
DROP TABLE positions_old;


-- ===== 2) peak_players =====
ALTER TABLE peak_players RENAME TO peak_players_old;

CREATE TABLE peak_players (
    player_id INTEGER NOT NULL,
    team_id   INTEGER NOT NULL,
    PRIMARY KEY (player_id, team_id),
    FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE,
    FOREIGN KEY (team_id)
        REFERENCES teams(team_id)
        ON DELETE CASCADE
);

INSERT INTO peak_players (player_id, team_id)
SELECT player_id, team_id FROM peak_players_old;
DROP TABLE peak_players_old;


-- ===== 3) loans =====
ALTER TABLE loans RENAME TO loans_old;

CREATE TABLE loans (
    loan_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id         INTEGER NOT NULL,
    loaning_team_id   INTEGER NOT NULL,
    receiving_team_id INTEGER NOT NULL,
    loan_expires      DATE    NOT NULL,
    FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE,
    FOREIGN KEY (loaning_team_id)
        REFERENCES teams(team_id)
        ON DELETE CASCADE,
    FOREIGN KEY (receiving_team_id)
        REFERENCES teams(team_id)
        ON DELETE CASCADE
);

INSERT INTO loans (loan_id, player_id, loaning_team_id, receiving_team_id, loan_expires)
SELECT loan_id, player_id, loaning_team_id, receiving_team_id, loan_expires
  FROM loans_old;
DROP TABLE loans_old;


COMMIT;
PRAGMA foreign_keys = ON;     -- Turn FK enforcement (and cascades) back on
