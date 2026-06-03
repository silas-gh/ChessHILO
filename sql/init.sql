CREATE TABLE positions (
    fen VARCHAR(100) PRIMARY KEY,
    num_games INT DEFAULT 0
);

CREATE TABLE users (
    user_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(30)
);

CREATE TABLE leaderboard (
    user_id uuid PRIMARY KEY REFERENCES users(user_id),
    score INT DEFAULT 0
);