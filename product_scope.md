# Motiva A3 product scope

## Problem and audience

College students sometimes know what they need to study but struggle to start. A task can feel too demanding, difficult to begin, or disconnected from a goal they care about. Motiva helps a student identify the immediate barrier and choose a concrete next step that fits the time they have. It is designed for college students working independently on coursework, exam preparation, or academic projects.

## Three planned core features

1. **Motivation check-in and action planning.** Enter one goal, select a barrier, rate confidence, importance, and perceived demand, and report available time. The prototype saves the check-in and opens a page where the student can revise and save a suggested action. Sign-in keeps the workflow tied to the student's account.
2. **Model-assisted suggestions.** Use the saved check-in and a curated set of strategies to suggest one feasible action. The student can edit the suggestion before saving. The current Django build uses a transparent rule-based mapping. The model-based feature and its validation and fallback behavior are planned for the next milestone.
3. **Reflection and learning history.** Record whether an action was completed, partly completed, or not started, with an optional note. Review previous actions and reflections to decide what to try again. The reflection form saves or updates one reflection per check-in. The history page displays the signed-in user's records newest first and supports goal search.

## Changes since A2

The A2 project idea and wireframes describe a full loop from check-in to strategy selection, work session, reflection, and history. A3 concentrates on a runnable database-backed flow and an initial AI plan. The editable action and baseline suggestion share one page in this build. The timer, account settings, and fuller interface remain on the A4 roadmap. The model-assisted feature extends the original rule-based strategy design. The rule-based suggestions also provide a fallback for the planned model integration.

