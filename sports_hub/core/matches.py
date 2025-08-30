"""
Record & list matches
"""
from sports_hub.db.connection import get_conn
from mysql.connector import Error

def record_match(sport_category_id, match_date, location, notes, team1_id, team2_id, score1, score2):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("""INSERT INTO matches_history(sport_category_id, match_date, location, notes) VALUES(%s, %s, %s, %s)""", (sport_category_id, match_date, location, notes))
	match_id = cur.lastrowid
	r1 = 'DRAW' if score1 == score2 else ('WIN' if score1 > score2 else 'LOSS')
	r2 = 'DRAW' if score1 == score2 else ('LOSS' if score1 > score2 else 'WIN')
	cur.execute("INSERT INTO match_teams(match_id, team_id, score, result) VALUES(%s, %s, %s, %s)", (match_id, team1_id, score1, r1))
	cur.execute("INSERT INTO match_teams(match_id, team_id, score, result) VALUES(%s, %s, %s, %s)", (match_id, team2_id, score2, r2))
	# Manually increment matches_played (triggers removed)
	cur.execute("UPDATE sports_categories SET matches_played = matches_played + 1 WHERE id=%s", (sport_category_id,))
	conn.commit()
	cur.close()
	conn.close()
	return match_id

def list_matches():
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("""SELECT m.id, sc.name AS category, m.match_date, m.location, GROUP_CONCAT(CONCAT(t.name,'(',mt.score,') ',mt.result) ORDER BY mt.score DESC SEPARATOR ' vs ') FROM matches_history m JOIN sports_categories sc ON sc.id=m.sport_category_id JOIN match_teams mt ON mt.match_id=m.id JOIN teams t ON t.id=mt.team_id GROUP BY m.id, sc.name, m.match_date, m.location ORDER BY m.id DESC""")
	results = cur.fetchall()
	cur.close()
	conn.close()
	return results
