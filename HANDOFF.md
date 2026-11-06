# Motiva A3 handoff for Lexxie

Open this folder, follow [README.md](README.md), and sign in with a local account you create. Save one check-in so you have a record to use for the reflection page. Start from this source package or the corresponding commit once it is in the shared GitHub repository.

## 1. Add reflection and history

- `motiva/models.py` and `motiva/migrations/0001_initial.py` already define `CheckIn` and `Reflection`. `CheckIn.owner` points to the signed-in user. `Reflection.checkin` is a one-to-one field with `related_name="reflection"`. Keep that relationship so each check-in has at most one reflection.
- Add `forms_reflections.py`, `views_reflections.py`, `urls_reflections.py`, and the templates inside `motiva/templates/motiva/`. Include the URL module in `config/urls.py`. Both new views should require login.
- Add `/checkins/<int:pk>/reflect/` named `reflection_edit`. Fetch the check-in using both `pk` and `owner=request.user`. Show the saved goal and action. Require an `outcome` (`completed`, `partial`, or `not_started`) and allow optional `notes`. Load the existing reflection into the form when one exists. Save a new or updated reflection against the authorized check-in and redirect to `history_list`.
- Add `/history/` named `history_list`. List the current user's check-ins newest first, with goal, action, date, and reflection outcome when present. Show an empty state and links to `checkin_detail` and `reflection_edit`. Add a **Reflect** link on `checkin_detail.html` and a **History** link in `base.html`.
- Verify that a reflection remains after refresh, edits update the existing row, and another user cannot view or attach a reflection to someone else's record.

## 2. Write the initial AI plan

Create `README_AI.md`. Name a candidate model and explain why it fits. Describe how Django would pass the saved goal, barrier, time, ratings, and curated strategies to the model without account identifiers. Define a structured response with the strategy, action, estimated minutes, and rationale. Explain how the app validates the response and lets the user edit the suggestion before saving. Describe expected resource and cost factors, privacy, and a rule-based fallback for failed calls or invalid output.

If you run a small experiment, record the actual inputs, outputs, and limitations in `docs/ai_experiment.md`. For A3, document the status accurately. Complete model integration is an A4 task.

## 3. Push the integrated prototype

Update `README.md` with the reflection and history routes, implemented features, and AI status. Run the entire check-in, action, reflection, and history flow. Push the integrated code to the shared GitHub repository, confirm instructor access, and send Ashley the repository URL and commit. Ashley will update the roadmap statuses, verify a clean checkout, and submit the URL through Canvas.
