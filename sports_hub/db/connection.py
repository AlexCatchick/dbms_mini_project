"""
get_conn(), DB credentials, helper methods
"""
import mysql.connector
from mysql.connector import Error
from sports_hub.config import DB_HOST, DB_USER, DB_PASS

def get_conn(db=None):
	return mysql.connector.connect(
		host=DB_HOST, user=DB_USER, password=DB_PASS, database=db
	)
