"""
Database schema setup (DDL, triggers, views)
"""
from sports_hub.db.connection import get_conn
from mysql.connector import Error

DDL_STATEMENTS = [
	"CREATE DATABASE IF NOT EXISTS SportDB",
	"USE SportDB",
	"""CREATE TABLE IF NOT EXISTS sports_categories (
		id INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE,
		matches_played INT NOT NULL DEFAULT 0,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	) ENGINE=InnoDB""",
	"""CREATE TABLE IF NOT EXISTS teams (
		id INT AUTO_INCREMENT PRIMARY KEY,
		name VARCHAR(100) NOT NULL,
		sport_category_id INT NOT NULL,
		UNIQUE KEY uq_team (name, sport_category_id),
		FOREIGN KEY (sport_category_id) REFERENCES sports_categories(id)
			ON UPDATE CASCADE ON DELETE RESTRICT
	) ENGINE=InnoDB""",
	"""CREATE TABLE IF NOT EXISTS players (
		id INT AUTO_INCREMENT PRIMARY KEY,
		full_name VARCHAR(150) NOT NULL,
		email VARCHAR(150) UNIQUE,
		dob DATE NULL
	) ENGINE=InnoDB""",
	"""CREATE TABLE IF NOT EXISTS player_team_memberships (
		id INT AUTO_INCREMENT PRIMARY KEY,
		player_id INT NOT NULL,
		team_id INT NOT NULL,
		sport_category_id INT NOT NULL,
		start_date DATE NOT NULL DEFAULT (CURRENT_DATE),
		end_date DATE NULL,
		membership_active TINYINT(1) AS (CASE WHEN end_date IS NULL THEN 1 ELSE 0 END) STORED,
		UNIQUE KEY uq_active_cat (player_id, sport_category_id, membership_active),
		UNIQUE KEY uq_player_team_unique (player_id, team_id, start_date),
		FOREIGN KEY (player_id) REFERENCES players(id)
			ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY (team_id) REFERENCES teams(id)
			ON UPDATE CASCADE ON DELETE RESTRICT,
		FOREIGN KEY (sport_category_id) REFERENCES sports_categories(id)
			ON UPDATE CASCADE ON DELETE RESTRICT
	) ENGINE=InnoDB""",
	"""CREATE TABLE IF NOT EXISTS matches_history (
		id INT AUTO_INCREMENT PRIMARY KEY,
		sport_category_id INT NOT NULL,
		match_date DATE NOT NULL,
		location VARCHAR(150),
		notes VARCHAR(500),
		FOREIGN KEY (sport_category_id) REFERENCES sports_categories(id)
			ON UPDATE CASCADE ON DELETE RESTRICT
	) ENGINE=InnoDB""",
	"""CREATE TABLE IF NOT EXISTS match_teams (
		match_id INT NOT NULL,
		team_id INT NOT NULL,
		score INT DEFAULT 0,
		result ENUM('WIN','LOSS','DRAW') DEFAULT NULL,
		PRIMARY KEY (match_id, team_id),
		FOREIGN KEY (match_id) REFERENCES matches_history(id)
			ON UPDATE CASCADE ON DELETE CASCADE,
		FOREIGN KEY (team_id) REFERENCES teams(id)
			ON UPDATE CASCADE ON DELETE RESTRICT
	) ENGINE=InnoDB""",
	# View (drop first for idempotency)
	"DROP VIEW IF EXISTS vw_unique_players_per_category",
	"""CREATE VIEW vw_unique_players_per_category AS
		SELECT sc.id AS category_id, sc.name AS category_name,
			   COUNT(DISTINCT ptm.player_id) AS active_unique_players
		FROM sports_categories sc
		LEFT JOIN player_team_memberships ptm
		  ON ptm.sport_category_id = sc.id AND ptm.end_date IS NULL
		GROUP BY sc.id, sc.name"""
]

def setup():
	conn = get_conn()
	cur = conn.cursor()
	for stmt in DDL_STATEMENTS:
		try:
			cur.execute(stmt)
		except Error as e:
			print("DDL error:", e)
	conn.commit()
	cur.close()
	conn.close()
