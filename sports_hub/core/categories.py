"""
CRUD for sports categories
"""
from sports_hub.db.connection import get_conn
from mysql.connector import Error

def add_category(name):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("INSERT INTO sports_categories(name) VALUES(%s)", (name,))
	conn.commit()
	category_id = cur.lastrowid
	cur.close()
	conn.close()
	return category_id

def list_categories():
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("SELECT id, name, matches_played FROM sports_categories ORDER BY id")
	results = cur.fetchall()
	cur.close()
	conn.close()
	return results

def get_category(category_id):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("SELECT id, name, matches_played FROM sports_categories WHERE id=%s", (category_id,))
	result = cur.fetchone()
	cur.close()
	conn.close()
	return result

def update_category(category_id, name=None):
	if not name:
		return False
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("UPDATE sports_categories SET name=%s WHERE id=%s", (name, category_id))
	conn.commit()
	cur.close()
	conn.close()
	return True

def delete_category(category_id):
	conn = get_conn("SportDB")
	cur = conn.cursor()
	cur.execute("DELETE FROM sports_categories WHERE id=%s", (category_id,))
	conn.commit()
	cur.close()
	conn.close()
	return True
