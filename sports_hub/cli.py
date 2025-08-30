"""Command-line interface (menus)

Run one of these:
	1) From parent directory:  python -m sports_hub.cli
	2) Or directly:            python sports_hub/cli.py
This file adjusts sys.path when run directly so package imports work.
"""
import os, sys
if __package__ is None:  # executed directly
		CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
		PARENT_DIR = os.path.dirname(CURRENT_DIR)
		if PARENT_DIR not in sys.path:
				sys.path.insert(0, PARENT_DIR)
from sports_hub.db.schema import setup
from sports_hub.core.categories import add_category, list_categories
from sports_hub.core.teams import add_team, list_teams
from sports_hub.core.players import add_player, list_players
from sports_hub.core.memberships import assign_player_to_team, end_membership
from sports_hub.core.matches import record_match, list_matches
from sports_hub.core.reports import unique_players_per_category
## Authentication not required, so import removed
from sports_hub.utils.export import export_to_csv, export_to_json

def main():
	print("Setting up database & objects (first run only)…")
	setup()
	# Authentication not required
	menu = """
--- Sport Hubs CLI ---
1) Add Category
2) List Categories
3) Add Team
4) List Teams
5) Add Player
6) List Players
7) Assign Player -> Team (enforces unique active per category)
8) End Player's Active Membership
9) Record Match (two teams in same category)
10) List Matches
11) Unique Active Players per Category
12) Export Data (choose dataset & format)
0) Exit
Choice: """
	while True:
		c = input(menu).strip()
		try:
			if c == "1":
				name = input("Category name: ").strip()
				add_category(name)
				print("Category added.")
			elif c == "2":
				cats = list_categories()
				for r in cats: print(r)
			elif c == "3":
				name = input("Team name: ").strip()
				cats = list_categories()
				for r in cats: print(r)
				cat_id = int(input("Category id: "))
				add_team(name, cat_id)
				print("Team added.")
			elif c == "4":
				teams = list_teams()
				for r in teams: print(r)
			elif c == "5":
				full = input("Player full name: ").strip()
				email = input("Email (optional): ").strip() or None
				dob = input("DOB YYYY-MM-DD (optional): ").strip() or None
				add_player(full, email, dob)
				print("Player added.")
			elif c == "6":
				players = list_players()
				for r in players: print(r)
			elif c == "7":
				players = list_players()
				for r in players: print(r)
				player_id = int(input("Player id: "))
				teams = list_teams()
				for r in teams: print(r)
				team_id = int(input("Team id: "))
				if assign_player_to_team(player_id, team_id):
					print("Assigned.")
				else:
					print("Assignment failed.")
			elif c == "8":
				player_id = int(input("Player id to end active membership: "))
				affected = end_membership(player_id)
				print(f"Ended rows: {affected}")
			elif c == "9":
				cats = list_categories()
				for r in cats: print(r)
				cat_id = int(input("Category id for match: "))
				match_date = input("Match date YYYY-MM-DD: ").strip()
				location = input("Location: ").strip()
				notes = input("Notes (optional): ").strip() or None
				teams = [t for t in list_teams() if t[2] == cats[cat_id-1][1]]
				for t in teams: print(t)
				t1 = int(input("Team 1 id: "))
				t2 = int(input("Team 2 id: "))
				s1 = int(input("Team 1 score: "))
				s2 = int(input("Team 2 score: "))
				record_match(cat_id, match_date, location, notes, t1, t2, s1, s2)
				print("Match recorded.")
			elif c == "10":
				matches = list_matches()
				for r in matches: print(r)
			elif c == "11":
				report = unique_players_per_category()
				for r in report: print(r)
			elif c == "12":
				dataset = input("Dataset (categories|players|teams|matches): ").strip().lower()
				fmt = input("Format (csv|json): ").strip().lower()
				if dataset == "categories":
					data = list_categories(); headers=["id","name","matches_played"]
				elif dataset == "players":
					data = list_players(); headers=["id","full_name","email","dob"]
				elif dataset == "teams":
					data = list_teams(); headers=["id","name","category"]
				elif dataset == "matches":
					data = list_matches(); headers=["id","category","match_date","location","teams_summary"]
				else:
					print("Unknown dataset."); continue
				filename = input(f"Output filename ({fmt}): ").strip()
				if fmt == "csv":
					export_to_csv(data, filename, headers=headers)
					print(f"Exported {dataset} to {filename} with headers")
				elif fmt == "json":
					export_to_json(data, filename, headers=headers)
					print(f"Exported {dataset} to {filename} with headers")
				else:
					print("Unsupported format (use csv or json)")
			elif c == "0":
				print("Bye!"); break
			else:
				print("Invalid choice.")
		except Exception as e:
			print("Error:", e)

if __name__ == "__main__":
	main()
