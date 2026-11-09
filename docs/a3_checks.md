# A3 integrated prototype verification

Reviewed on November 8, 2026 against source commit `cf0d8f996eecc90ce6f49a34bec128088d8c5928`.

The review used a fresh source copy, a new virtual environment, and a new SQLite database. Dependencies from requirements.txt installed successfully. The environment was Python 3.12.10, Django 5.2.18, asgiref 3.12.1, and sqlparse 0.6.0.

The machine's default Python certificate configuration initially prevented pip from reaching PyPI. Installing with the operating system certificate bundle resolved it while retaining certificate verification. This environment-specific command was used:

```sh
python -m pip install --cert /etc/ssl/cert.pem -r requirements.txt
```

Database migrations and Django system checks passed. Twenty-five route-level checks passed using Django's HTTP test client with CSRF enforcement. The checks used temporary local accounts and exercised rendered templates and database state.

| Area | Actual result |
| --- | --- |
| Setup | Fresh migrations applied. Django reported no system-check issues. Model definitions matched committed migrations. |
| Login and navigation | Root led to check-in. Sign-in and POST sign-out worked. Signed-out visits to personal pages redirected to login. |
| Validation | Blank goal, out-of-range ratings and minutes, and unknown barriers produced form errors and created no record. A missing CSRF token was rejected. |
| Check-in and action | A valid check-in was saved to the signed-in user. Its detail page and Reflect link rendered. Action edits persisted across requests. Blank edits preserved the existing action. |
| Reflection | A missing outcome was rejected. A partial outcome and notes saved and redirected to history. Later edits updated the same reflection row. |
| History | A new user saw the empty state. Saved records and outcomes displayed. Case-insensitive goal search and the no-results state worked. |
| Authorization | A second user could neither read nor update another user's action or reflection. History excluded the other user's records. Unauthorized requests preserved existing data. |
| Text handling | User-entered HTML was escaped in action and history pages. |

AI feasibility was reviewed from README_AI.md. The model is proposed. Model calls, AI output quality, and AI latency have not been tested. A4 evaluation will collect those results.

These checks verify the local Django routes and database workflow. Visual browser inspection and public deployment were outside this verification.

