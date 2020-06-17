DROP TABLE IF EXISTS stats;

CREATE TABLE stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_name TEXT NOT NULL,
  points REAL NOT NULL,
  rebounds REAL NOT NULL,
  points_per_game REAL
);

INSERT INTO stats (player_name, points, rebounds, points_per_game) VALUES ("Kyrie", 5, 2, 5.2);

INSERT INTO stats (player_name, points, rebounds) VALUES ("Lonzo Ball", 5, 2);