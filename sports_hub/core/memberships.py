"""
Assign/remove players to teams
"""
from sports_hub.db.connection import get_conn
from mysql.connector import Error

def assign_player_to_team(player_id, team_id):
	"""Assign player to team. Looks up team's sport_category_id (triggers removed)."""
	conn = get_conn("SportDB")
	cur = conn.cursor()
	try:
		cur.execute("SELECT sport_category_id FROM teams WHERE id=%s", (team_id,))
		row = cur.fetchone()
		if not row:
			cur.close(); conn.close(); return False
		cat_id = row[0]
		cur.execute("""INSERT INTO player_team_memberships(player_id, team_id, sport_category_id) VALUES(%s, %s, %s)""", (player_id, team_id, cat_id))
		conn.commit()
		result = True
	except Error:
		result = False
	cur.close()
	conn.close()
	return result

def end_membership(player_id):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("""UPDATE player_team_memberships SET end_date=CURRENT_DATE WHERE player_id=%s AND end_date IS NULL""", (player_id,))
	conn.commit()
	affected = cur.rowcount
	cur.close()
	conn.close()
	return affected
