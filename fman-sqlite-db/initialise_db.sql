PRAGMA foreign_keys = ON;           -- ignored by Postgres, required by SQLite
BEGIN;


CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(30) NOT NULL,
    nation_extid INT NOT NULL,
    born INT NOT NULL,
    age INT NOT NULL,
    int_caps INT NOT NULL,
    int_goals INT NOT NULL,
    u21_caps INT NOT NULL,
    u21_goals INT NOT NULL,
    height INT NOT NULL,
    "weight" INT NOT NULL,
    aerial_ability INT NOT NULL,
    command_of_area INT NOT NULL,
    communication INT NOT NULL,
    eccentricity INT NOT NULL,
    handling INT NOT NULL,
    kicking INT NOT NULL,
    one_on_ones INT NOT NULL,
    reflexes INT NOT NULL,
    rushing_out INT NOT NULL,
    tendency_to_punch INT NOT NULL,
    throwing INT NOT NULL,
    corners INT NOT NULL,
    crossing INT NOT NULL,
    dribbling INT NOT NULL,
    finishing INT NOT NULL,
    first_touch INT NOT NULL,
    free_kicks INT NOT NULL,
    heading INT NOT NULL,
    long_shots INT NOT NULL,
    long_throws INT NOT NULL,
    marking INT NOT NULL,
    passing INT NOT NULL,
    penalty_taking INT NOT NULL,
    tackling INT NOT NULL,
    technique INT NOT NULL,
    aggression INT NOT NULL,
    anticipation INT NOT NULL,
    bravery INT NOT NULL,
    composure INT NOT NULL,
    concentration INT NOT NULL,
    vision INT NOT NULL,
    decisions INT NOT NULL,
    determination INT NOT NULL,
    flair INT NOT NULL,
    leadership INT NOT NULL,
    off_the_ball INT NOT NULL,
    positioning INT NOT NULL,
    teamwork INT NOT NULL,
    work_rate INT NOT NULL,
    acceleration INT NOT NULL,
    agility INT NOT NULL,
    balance INT NOT NULL,
    jumping INT NOT NULL,
    left_foot INT NOT NULL,
    natural_fitness INT NOT NULL,
    pace INT NOT NULL,
    right_foot INT NOT NULL,
    stamina INT NOT NULL,
    strength INT NOT NULL,
    consistency INT NOT NULL,
    dirtiness INT NOT NULL,
    important_matches INT NOT NULL,
    injury_proness INT NOT NULL,
    versatility INT NOT NULL,
    adaptability INT NOT NULL,
    ambition INT NOT NULL,
    loyalty INT NOT NULL,
    pressure INT NOT NULL,
    professional INT NOT NULL,
    sportsmanship INT NOT NULL,
    temperament INT NOT NULL,
    controversy INT NOT NULL,
    goalkeeper INT NOT NULL,
    sweeper INT NOT NULL,
    striker INT NOT NULL,
    attacking_mid_central INT NOT NULL,
    attacking_mid_left INT NOT NULL,
    attacking_mid_right INT NOT NULL,
    defender_central INT NOT NULL,
    defender_left INT NOT NULL,
    defender_right INT NOT NULL,
    defensive_midfielder INT NOT NULL,
    midfield_central INT NOT NULL,
    midfield_left INT NOT NULL,
    midfield_right INT NOT NULL,
    wingback_left INT NOT NULL,
    wingback_right INT NOT NULL
);

CREATE TABLE IF NOT EXISTS teams(
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
     "name" VARCHAR(30) NOT NULL,
     nation_id INT NOT NULL,
     division VARCHAR(30) NULL,
     average_age FLOAT NULL,
     balance TEXT NULL,
     transfer_budget TEXT NULL,
     wage_budget TEXT NULL,
     training_facilities TEXT NULL,
     youth_facilities TEXT NOT NULL,
     youth_academy TEXT NOT NULL,
     youth_recruitment TEXT NULL,
     stadium_capacity INT NOT NULL,
     average_attendance INT NOT NULL,
     ability FLOAT NOT NULL,
     potential FLOAT NOT NULL
);

CREATE TABLE nations (
    nation_id INTEGER PRIMARY KEY,   -- ⬅ no AUTOINCREMENT
    "name"      VARCHAR(50) UNIQUE     -- may be NULL until you scrape names
);

CREATE TABLE IF NOT EXISTS positions(                                                                
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    position VARCHAR(5) NOT NULL,
    -- player_id and team_id are foreign keys to players and teams tables
    --A player can appear on many teams in many positions, but you should never have the same player–team–position triple twice
    PRIMARY KEY (player_id, team_id, position),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(30) NOT NULL,
    age INT NOT NULL,
    nationality VARCHAR(15) NOT NULL,
    team VARCHAR(15) NOT NULL,
    club_job VARCHAR(45) NOT NULL,
    "club_contract_type" VARCHAR(15) NOT NULL,
    wage VARCHAR(15) NOT NULL,
    "contract_expires" DATE NULL,
    "contract_signed" DATE NULL,
    judging_player_ability INT NOT NULL,
    judging_player_potential INT NOT NULL,
    manager_rating FLOAT NOT NULL,
    assistant_rating FLOAT NOT NULL,
    coach_rating FLOAT NOT NULL,
    scout_rating FLOAT NOT NULL,
    physio_rating FLOAT NOT NULL,
    strength_training INT NOT NULL,
    aerobic_training INT NOT NULL,
    gk_handling_training INT NOT NULL,
    gk_shot_stopping_training INT NOT NULL,
    tactics_training INT NOT NULL,
    "ball_control_training" INT NOT NULL,
    defending_training INT NOT NULL,
    attacking_training INT NOT NULL,
    shooting_training INT NOT NULL,
    home_rep INT NOT NULL,
    world_rep INT NOT NULL,
    current_rep INT NOT NULL
);

CREATE TABLE IF NOT EXISTS loans (
    player_id INTEGER NOT NULL,
    loaning_team_id INTEGER NOT NULL,
    receiving_team_id INTEGER NOT NULL,
    loan_expires DATE NOT NULL,
    --This blocks the same triple from appearing twice.
    --A player can be loaned out to many teams, but you should never have the same player–loaning team–receiving team triple twice
    PRIMARY KEY (player_id, loaning_team_id, receiving_team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (loaning_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (receiving_team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS contracts (
    curr_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    "name" VARCHAR(30) NOT NULL,
    age INT NOT NULL,
    nationality VARCHAR(15) NOT NULL,
    contracted_club VARCHAR(30) NOT NULL,
    wage VARCHAR(15) NOT NULL,
    "contract_expires" DATE NULL,
    "contract_signed" DATE NULL,
    "value" VARCHAR(15) NOT NULL,
    estimated_cost VARCHAR(15) NOT NULL,
    team_id INTEGER NOT NULL,
    current_ability INT NOT NULL,
    potential_ability INT NOT NULL,
    ca_remaining INT NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS peak_players (
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    --You only care that this player peaked at this club once.
    PRIMARY KEY (player_id, team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

COMMIT;







