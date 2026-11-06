# A3 handoff checks

The following checks passed on November 6, 2026 in a fresh copy with a new SQLite database, Python 3.12, and the dependency versions in `requirements.txt`. The checks exercised Django's HTTP routes with CSRF enforcement.

| Check | Observed result |
| --- | --- |
| Initial migrations and Django system check | Migrations applied to a clean database. System check reported no issues. The models and migrations agree. |
| Sign-in and sign-out | A local user could sign in and sign out. Signed-out visits to personal pages redirected to login. |
| Check-in validation | Blank goal, invalid minutes, invalid rating, and invalid barrier were rejected without creating a record. A POST without a CSRF token was rejected. |
| Check-in persistence | A valid check-in created a record owned by the signed-in user and displayed the expected rule-based suggestion. |
| Action editing | A revised action persisted after a fresh request. A blank edit displayed an error and preserved the saved action. |
| Account isolation | A second user could neither read nor edit the first user's action page. |
| Reflection relationship | A reflection saved via the ORM was available through the linked check-in. |

After Lexxie integrates reflection and history, verify the full workflow again from a clean checkout. Add the actual results for reflection creation and editing, empty history, and cross-account history and reflection access. Record AI experiment results separately if an experiment is run.
