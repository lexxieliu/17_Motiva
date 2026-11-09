# Motiva

Motiva helps college students turn a learning goal and its immediate barrier into one manageable next action, then reflect on how it went. This is the A3 local prototype, built with Django and SQLite.

## Implemented features

- Sign-in and sign-out with Django's built-in accounts. Personal pages require sign-in.
- **Check-in:** enter a goal, a barrier, confidence, importance, and demand ratings (1–5), and available minutes (1–180). Invalid input shows errors and saves nothing.
- **Action planning:** a valid check-in is saved with a rule-based suggested action, which the user can edit and save.
- **Reflection:** record whether the action was completed, partly completed, or not started, with optional notes. Each check-in has one reflection; later edits update it.
- **History:** the user's own check-ins, newest first, with goal, action, date, and outcome or "No reflection yet". Includes a goal search.
- Each user can see and change only their own records.

## Run locally

Requires Python 3.12 or later. Open a terminal in the folder containing `manage.py`.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

- **Dependencies:** listed in `requirements.txt` (Django 5.2.18).
- **Database:** `migrate` creates a local SQLite file, `db.sqlite3`, which is not committed.
- **Local user:** `createsuperuser` prompts for a username and password of your choice. Public registration is not included.
- **Configuration:** none required. `DJANGO_SECRET_KEY` can be set as an environment variable; otherwise a local development key is used. No AI API key is needed.

Open <http://127.0.0.1:8000/> and sign in.

## Main routes

| Route | Name | Purpose |
| --- | --- | --- |
| `/` | | Redirects to a new check-in |
| `/accounts/login/` | `login` | Sign in |
| `/accounts/logout/` | `logout` | Sign out (navigation button) |
| `/checkins/new/` | `checkin_create` | Save a check-in |
| `/checkins/<id>/` | `checkin_detail` | View the check-in and edit its action |
| `/checkins/<id>/reflect/` | `reflection_edit` | Save or update the reflection |
| `/history/` | `history_list` | View and search past check-ins |

## AI status

**Proposed, not integrated.** Suggested actions come from a rule-based mapping by barrier. The planned model-assisted suggestion is described in [README_AI.md](README_AI.md). No AI experiment was run for A3.

## Known gaps

- Model-based suggestions, the work-session timer, account settings, and public registration are planned for A4.
- Settings are for local development only (`DEBUG = True`). The app is not deployed.
- No automated tests are included yet.

## A3 submission materials

Team 17 consists of Ashley Zhou and Lexxie Liu. The A3 materials are in this repository.

- [Product scope update](docs/product_scope.md)
- [AI technical plan](README_AI.md)
- [Development progress and roadmap](docs/roadmap.md)
- [Integrated prototype verification](docs/a3_checks.md)

Submit the repository URL through Canvas by November 9, 2026 at 11:59 PM.

See [HANDOFF.md](HANDOFF.md) for the handoff status.

