"""
CRUD for players
"""
from sports_hub.db.connection import get_conn
from mysql.connector import Error

def add_player(full_name, email=None, dob=None):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("INSERT INTO players(full_name, email, dob) VALUES(%s, %s, %s)", (full_name, email, dob))
	conn.commit()
	player_id = cur.lastrowid
	cur.close()
	conn.close()
	return player_id

def list_players():
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("SELECT id, full_name, email, dob FROM players ORDER BY id")
	results = cur.fetchall()
	cur.close()
	conn.close()
	return results

def get_player(player_id):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("SELECT id, full_name, email, dob FROM players WHERE id=%s", (player_id,))
	result = cur.fetchone()
	cur.close()
	conn.close()
	return result

def update_player(player_id, full_name=None, email=None, dob=None):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	fields = []
	values = []
	if full_name:
		fields.append("full_name=%s")
		values.append(full_name)
	if email:
		fields.append("email=%s")
		values.append(email)
	if dob:
		fields.append("dob=%s")
		values.append(dob)
	if not fields:
		return False
	values.append(player_id)
	sql = f"UPDATE players SET {', '.join(fields)} WHERE id=%s"
	cur.execute(sql, tuple(values))
	conn.commit()
	cur.close()
	conn.close()
	return True

def delete_player(player_id):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("DELETE FROM players WHERE id=%s", (player_id,))
	conn.commit()
	cur.close()
	conn.close()
	return True
