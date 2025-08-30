"""
Analytics & reporting queries
"""
from sports_hub.db.connection import get_conn

def unique_players_per_category():
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("SELECT * FROM vw_unique_players_per_category ORDER BY category_id")
	results = cur.fetchall()
	cur.close()
	conn.close()
	return results
