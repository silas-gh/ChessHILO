CREATE TABLE IF NOT EXISTS positions (
    fen VARCHAR(100) PRIMARY KEY,
    num_games INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users (
    user_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(30),
    password_hash TEXT
);

CREATE TABLE IF NOT EXISTS leaderboard (
    user_id uuid PRIMARY KEY REFERENCES users(user_id),
    score INT DEFAULT 0
);