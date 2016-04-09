-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.

SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
  AND pid <> pg_backend_pid();




DROP DATABASE if exists tournament;
CREATE DATABASE tournament;
\c tournament
CREATE TABLE Players (name text NOT NULL, id serial primary key);

CREATE TABLE Matches (
			id serial PRIMARY KEY,
			winner integer REFERENCES players(id) ON DELETE CASCADE,
			loser integer REFERENCES players(id) ON DELETE CASCADE
			CHECK (winner <> loser)
			);
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE VIEW num_wins AS (SELECT Players.id, Players.name, COUNT(Matches.winner = Players.id) AS wins
 FROM Players LEFT JOIN Matches ON Players.id=Matches.winner GROUP BY Players.id);

CREATE VIEW num_loses AS (SELECT Players.id, Players.name, COUNT(Matches.loser = Players.id) AS loses
 FROM Players LEFT JOIN Matches ON Players.id=Matches.loser  GROUP BY Players.id);

CREATE VIEW num_matches AS (SELECT num_wins.id, num_wins.name, num_wins.wins AS wins, num_wins.wins + num_loses.loses AS games
 FROM num_wins LEFT JOIN num_loses ON num_wins.id=num_loses.id ORDER BY wins);

-- select * from Players;
-- select * from Matches;
-- select * from num_wins;
-- select * from num_loses;
-- select * from num_matches;