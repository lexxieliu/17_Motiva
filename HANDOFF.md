# Motiva A3 handoff for Ashley

**Repository:** <https://github.com/lexxieliu/17_Motiva>

**Final A3 code commit:** `8034cc7` (reflection, history, AI plan). Later commits on `main` update documentation only. Ashley's handoff commit is `f9050bb`.

## Run

Follow [README.md](README.md) on a fresh checkout: create a virtual environment, install requirements, run `migrate`, create a local user with `createsuperuser`, and start `runserver`. No AI API key or other configuration is needed.

## Completed

- Ashley: project setup, `CheckIn` and `Reflection` models and migration, sign-in/sign-out, check-in with validation, rule-based action, editable action page, product scope.
- Lexxie: reflection page (`/checkins/<id>/reflect/`, `reflection_edit`), history page with goal search (`/history/`, `history_list`), **Reflect** link on the action page, **History** navigation link, `README.md`, and `README_AI.md` (AI plan; status: proposed).

## Known issues

- AI suggestions are not integrated; the rule-based mapping is the only suggestion source.
- No `docs/ai_experiment.md`: no AI experiment was run.
- Timer, account settings, public registration, deployment, and automated tests are not included.

## Remaining for Ashley

The integrated source was verified in a fresh environment on November 8, 2026. The roadmap, product scope, and `docs/a3_checks.md` now reflect the completed A3 workflow. Twenty-five route-level checks passed. The remaining submission step is to submit the repository URL on Canvas by November 9, 11:59 PM.

