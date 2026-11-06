# Motiva

Motiva helps college students turn a learning goal and its immediate barrier into one manageable next action. This A3 handoff includes the Django foundation, sign-in, and the database-backed check-in and editable action plan. Both application models and their initial migration are included. Lexxie owns the reflection and history pages and the initial AI plan.

## Run locally

Open a terminal in the folder containing `manage.py`. The handoff was checked with Python 3.12 and Django 5.2.18.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows PowerShell, use `.venv\Scripts\Activate.ps1` to activate the environment. Create your own local username and password when prompted. Sign in at <http://127.0.0.1:8000/>. SQLite creates the local database when you run migrations.

| Route | Purpose |
| --- | --- |
| `/` | Open the check-in flow |
| `/accounts/login/` | Sign in |
| `/checkins/new/` | Save a goal, barrier, ratings, and available minutes |
| `/checkins/<id>/` | Review the saved check-in and edit its action |
| `/accounts/logout/` | Sign out using the navigation button |

Try a goal such as “Start my chemistry review,” choose “Unsure where to start,” enter three ratings from 1 to 5, and enter 15 minutes. Save the check-in, revise the suggested action, and refresh to confirm the edit persisted. Suggestions in this build come from a short rule-based mapping. The local workflow runs without an AI service or API key.

See [HANDOFF.md](HANDOFF.md) for the extension steps, [product scope](docs/product_scope.md) for the A3 product update, and [roadmap](docs/roadmap.md) for responsibilities and targets. The settings are for local development. Deployment configuration belongs to the A4 milestone.
