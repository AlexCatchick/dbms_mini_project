<div align="center">

# Sports Hub CLI
CLI-based sports management system for categories, teams, players, memberships & matches on a local MySQL instance. Clean modular architecture, data exports, and automated end‑to‑end tests.

</div>


## 1. Overview
Original single-file prototype evolved into a maintainable, testable package:
* Clear separation (schema / CRUD / reporting / exports / interface).
* Removed brittle MySQL `DELIMITER` trigger blocks; replaced with explicit Python logic (incrementing `matches_played`, resolving category on membership assignment).
* Consistent CSV & JSON exports with headers and type coercion.
* Automated `unittest` workflow validates full lifecycle.

## 2. Features
| Domain | Capabilities |
|--------|--------------|
| Categories | Create, list, match count tracking |
| Teams | Create, list (with category) |
| Players | Create, list, update/delete helpers (in modules) |
| Memberships | Assign player→team, end active membership, unique active per category enforced by schema uniqueness (player, category, active) |
| Matches | Record match (2 teams same category), auto WIN/LOSS/DRAW, increments category count |
| Reporting | View `vw_unique_players_per_category` for active unique player counts |
| Export | Any dataset (categories, players, teams, matches, unique view) to CSV/JSON with headers |
| Testing | Full end-to-end workflow assertions & export verification |

## 3. Project Structure
```
project/
  requirements.txt
  README.md
  sports_hub/
    __init__.py
    cli.py                 # Interactive menu (option 12 unified export)
    config.py              # DB credentials (local MySQL)
    db/
      __init__.py
      connection.py        # get_conn()
      schema.py            # Ordered DDL + view (no triggers)
      seed_data.py         # (placeholder)
    core/
      __init__.py
      categories.py        # Category CRUD
      teams.py             # Team CRUD
      players.py           # Player CRUD
      memberships.py       # Assign + end membership (manual category resolution)
      matches.py           # Match record/list + manual matches_played increment
      reports.py           # Unique players view access
    utils/
      __init__.py
      export.py            # Uniform CSV/JSON export helpers
    test_script.py         # unittest workflow (drops & rebuilds DB)
```

## 4. Data Model
Tables (simplified):
```
sports_categories(id, name UNIQUE, matches_played, created_at)
teams(id, name, sport_category_id FK, UNIQUE(name, sport_category_id))
players(id, full_name, email UNIQUE, dob)
player_team_memberships(id, player_id FK, team_id FK, sport_category_id, start_date, end_date, membership_active (generated),
    UNIQUE(player_id, sport_category_id, membership_active))
matches_history(id, sport_category_id FK, match_date, location, notes)
match_teams(match_id FK, team_id FK, score, result ENUM, PK(match_id, team_id))
VIEW vw_unique_players_per_category(category_id, category_name, active_unique_players)
```
No triggers; logic moved to Python for portability and clearer error handling.

## 5. Installation
Prerequisites: Python 3.11+ (13 OK) & running local MySQL with user matching `config.py`.

```
pip install -r requirements.txt
```
Adjust `sports_hub/config.py` if needed.

## 6. Running the CLI
From `new_project/` parent of the package:
```
python -m sports_hub.cli
```
Alternative (direct):
```
python sports_hub/cli.py
```
Menu Options:
1 Add Category
2 List Categories
3 Add Team
4 List Teams
5 Add Player
6 List Players
7 Assign Player -> Team
8 End Player's Active Membership
9 Record Match
10 List Matches
11 Unique Active Players per Category
12 Export Data (choose dataset & format)
0 Exit

## 7. Exporting Data
Option 12 prompts:
1. Dataset: `categories|players|teams|matches`
2. Format: `csv|json`
3. Output filename

Headers always included. JSON exports become list of objects; dates/coercibles converted to strings.

Programmatic example:
```python
from sports_hub.core.categories import list_categories
from sports_hub.utils.export import export_to_json
cats = list_categories()
export_to_json(cats, "cats.json", headers=["id","name","matches_played"])
```

## 8. Tests
Run full workflow tests (drops & recreates DB):
```
python -m sports_hub.test_script
```
Assertions cover:
* Row counts & names
* Team category joins
* Membership activity changes
* Match creation + results summary
* Unique players view logic
* CSV/JSON export file existence & validity

Exit code != 0 indicates failure (CI friendly).

## 9. Implementation Details
* `schema.py` uses an ordered list (`DDL_STATEMENTS`) for idempotent setup.
* `memberships.assign_player_to_team` queries category directly; no trigger.
* `matches.record_match` updates `matches_played` explicitly.
* `export.py` normalizes row tuples to dicts when headers supplied; handles dates & decimals.
* CLI adds path bootstrap for direct execution.

## 10. Security & Config
Credentials are plain-text for local dev only. For production consider:
* Environment variables (`os.getenv`) or `.env` loader
* Least-privilege DB user

## 11. Extensibility Roadmap
| Area | Enhancement Ideas |
|------|-------------------|
| Logging | Add `logging` module with rotating file handler |
| Error Handling | Wrap DB ops in context managers & retries where sensible |
| Transactions | Group multi-statement operations (match + updates) in explicit transactions |
| Packaging | Add `pyproject.toml` for installation as editable package |
| Seeding | Implement `seed_data.py` with sample fixtures |
| Stats | Aggregated team/player performance queries |
| CLI UX | Input validation & colored output |
| Migrations | Separate SQL migration scripts (e.g., Alembic) |
| Testing | Split unit vs integration; mock DB for unit logic |

## 12. Troubleshooting
| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: sports_hub` | Ran CLI from inside package | Run from parent or use `python -m sports_hub.cli` |
| DDL errors (old triggers) | Old schema file cached | Pull latest `schema.py`, drop DB, re-run tests |
| Empty JSON export | Missing headers earlier | Headers now mandatory in CLI; provide when calling programmatically |

## 13. License / Usage
Educational example. Adapt freely (add appropriate license text if distributing).

---
**Summary:** Sports Hub CLI delivers a modular, test-backed sports management system with reliable DB setup and flexible exports—clean foundation for future extensions.
