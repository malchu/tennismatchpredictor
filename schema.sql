DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    player1 TEXT NOT NULL,
    player2 TEXT NOT NULL,
    chance INTEGER NOT NULL,
    winner TEXT NOT NULL
);