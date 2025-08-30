"""Automated end-to-end test exercising all CLI menu actions with assertions.

Run:
    python -m sports_hub.test_script

Exits with non-zero status if any assertion fails.
"""
import os, sys, json
import unittest

if __package__ is None:  # allow direct execution
    CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
    PARENT_DIR = os.path.dirname(CURRENT_DIR)
    if PARENT_DIR not in sys.path:
        sys.path.insert(0, PARENT_DIR)

from sports_hub.db.schema import setup
from sports_hub.db.connection import get_conn
from sports_hub.core.categories import add_category, list_categories
from sports_hub.core.teams import add_team, list_teams
from sports_hub.core.players import add_player, list_players
from sports_hub.core.memberships import assign_player_to_team, end_membership
from sports_hub.core.matches import record_match, list_matches
from sports_hub.core.reports import unique_players_per_category
from sports_hub.utils.export import export_to_csv, export_to_json

DB_NAME = "SportDB"

def reset_database():
    conn = get_conn()  # server-level connection
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    conn.commit()
    cur.close(); conn.close()

class TestWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reset_database()
        setup()

        # Categories
        cls.cat_ids = [add_category(n) for n in ["Football", "Basketball", "Tennis"]]
        # Teams
        cls.team_ids = [
            add_team("Red Warriors", cls.cat_ids[0]),
            add_team("Blue Knights", cls.cat_ids[0]),
            add_team("Golden Eagles", cls.cat_ids[1]),
            add_team("Silver Foxes", cls.cat_ids[1]),
        ]
        # Players
        cls.player_ids = [
            add_player("John Doe", "john@example.com", "1990-01-01"),
            add_player("Jane Smith", "jane@example.com", "1992-02-02"),
            add_player("Mike Brown", "mike@example.com", "1995-03-03"),
        ]
        # Memberships
        assign_player_to_team(cls.player_ids[0], cls.team_ids[0])
        assign_player_to_team(cls.player_ids[1], cls.team_ids[1])
        assign_player_to_team(cls.player_ids[2], cls.team_ids[2])
        end_membership(cls.player_ids[0])  # end one membership
        # Matches
        cls.match_ids = [
            record_match(cls.cat_ids[0], "2025-08-30", "Stadium A", "Derby", cls.team_ids[0], cls.team_ids[1], 2, 1),
            record_match(cls.cat_ids[1], "2025-08-30", "Arena B", "League", cls.team_ids[2], cls.team_ids[3], 3, 3),
        ]

    def test_categories(self):
        cats = list_categories()
        self.assertEqual(len(cats), 3)
        names = {c[1] for c in cats}
        self.assertSetEqual(names, {"Football", "Basketball", "Tennis"})

    def test_teams(self):
        teams = list_teams()
        self.assertEqual(len(teams), 4)
        # Ensure categories show up in result (3rd element is category name)
        cat_names = {t[2] for t in teams}
        self.assertTrue({"Football", "Basketball"}.issubset(cat_names))

    def test_players(self):
        players = list_players()
        self.assertEqual(len(players), 3)
        emails = {p[2] for p in players}
        self.assertIn("john@example.com", emails)

    def test_matches(self):
        matches = list_matches()
        self.assertEqual(len(matches), 2)
        # Validate teams summary contains 'WIN' or 'DRAW'
        summaries = [m[4] for m in matches]
        self.assertTrue(any("WIN" in s or "DRAW" in s for s in summaries))

    def test_unique_players_view(self):
        rows = unique_players_per_category()
        m = {r[1]: r[2] for r in rows}
        # After ending first player's membership, only second remains active in Football
        self.assertEqual(m.get("Football"), 1)

    def test_exports(self):
        cats = list_categories(); players = list_players(); teams = list_teams(); matches = list_matches(); unique = unique_players_per_category()
        datasets = [
            ("categories", cats, ["id","name","matches_played"]),
            ("players", players, ["id","full_name","email","dob"]),
            ("teams", teams, ["id","name","category"]),
            ("matches", matches, ["id","category","match_date","location","teams_summary"]),
            ("unique", unique, ["category_id","category_name","active_unique_players"]),
        ]
        for name, data, headers in datasets:
            csv_file = f"test_{name}.csv"; json_file = f"test_{name}.json"
            export_to_csv(data, csv_file, headers=headers)
            export_to_json(data, json_file, headers=headers)
            # Basic file existence & non-empty
            self.assertTrue(os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0)
            self.assertTrue(os.path.isfile(json_file) and os.path.getsize(json_file) > 0)
            # JSON loads
            with open(json_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                self.assertIsInstance(loaded, list)
                if loaded:
                    self.assertIsInstance(loaded[0], (list, dict))

if __name__ == '__main__':
    unittest.main(verbosity=2)
