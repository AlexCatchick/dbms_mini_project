"""
CRUD for teams
"""
from sports_hub.db.connection import get_conn
from mysql.connector import Error

def add_team(name, sport_category_id):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("INSERT INTO teams(name, sport_category_id) VALUES(%s, %s)", (name, sport_category_id))
	conn.commit()
	team_id = cur.lastrowid
	cur.close()
	conn.close()
	return team_id

def list_teams():
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("SELECT t.id, t.name, sc.name AS category FROM teams t JOIN sports_categories sc ON sc.id=t.sport_category_id ORDER BY t.id")
	results = cur.fetchall()
	cur.close()
	conn.close()
	return results

def get_team(team_id):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("SELECT id, name, sport_category_id FROM teams WHERE id=%s", (team_id,))
	result = cur.fetchone()
	cur.close()
	conn.close()
	return result

def update_team(team_id, name=None, sport_category_id=None):
	fields = []
	values = []
	if name:
		fields.append("name=%s")
		values.append(name)
	if sport_category_id:
		fields.append("sport_category_id=%s")
		values.append(sport_category_id)
	if not fields:
		return False
	values.append(team_id)
	sql = f"UPDATE teams SET {', '.join(fields)} WHERE id=%s"
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute(sql, tuple(values))
	conn.commit()
	cur.close()
	conn.close()
	return True

def delete_team(team_id):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("DELETE FROM teams WHERE id=%s", (team_id,))
	conn.commit()
	cur.close()
	conn.close()
	return True
