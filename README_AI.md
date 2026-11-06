# Motiva AI plan

**Status: Proposed.** No model has been experimented with or integrated in A3. The current build uses the rule-based mapping in `motiva/views_checkins.py`. Model integration is an A4 task.

## Candidate model

**Claude Haiku 5.5** (`claude-haiku-5-5`) through the Anthropic Messages API.

Why it fits:

- The task is short, structured text generation: one feasible next step from a small check-in. It does not need a large model or fine-tuning.
- A small hosted model keeps per-request cost and response time low for an interactive form.
- It follows instructions and returns JSON that Django can parse and validate.
- A hosted API needs no GPU, model weights, or model server in the Django deployment.

## Input

Django builds the prompt from the saved `CheckIn` only:

| Field | Source |
| --- | --- |
| goal | `CheckIn.goal` |
| barrier | `CheckIn.barrier` (readable label) |
| available_minutes | `CheckIn.available_minutes` |
| confidence, importance, demand | `CheckIn` ratings (1–5) |
| strategies | Curated strategy list (starting from the five rule-based strategies; Ashley maintains the content) |

No account identifiers are sent: no user ID, username, email, or check-in ID.

## Output

The model must return one JSON object:

```json
{
  "strategy": "start",
  "action": "Open the Chapter 4 slides and write three notes on reaction rates.",
  "estimated_minutes": 15,
  "rationale": "A single source and a fixed number of notes make it easy to begin."
}
```

The user reviews and edits the suggestion before saving it as `next_action`.

## Django workflow

1. The user submits a valid check-in. Django saves the `CheckIn`.
2. A service function, `motiva/ai_suggestions.py: suggest_action(checkin)`, builds the prompt and calls the model with a timeout.
3. Django parses and validates the response:
   - valid JSON with all four fields present and non-empty;
   - `strategy` is in the curated list;
   - `estimated_minutes` is an integer from 1 to `available_minutes`;
   - `action` is within a length limit.
4. The action page (`checkin_detail`) shows the suggestion, labeled as AI-generated, in the editable action field.
5. The user edits if needed and saves. Only the user's saved text is stored in `next_action`.

**Fallback:** if the API key is missing, the call times out or fails, or the output fails validation, the check-in is still saved and the page shows the labeled rule-based suggestion. The fallback keeps the workflow usable. It is not the AI feature.

The API key is read from an environment variable (`ANTHROPIC_API_KEY`) and is never committed.

## Resources, latency, and cost

- One API request per check-in. No local GPU or model files.
- Cost depends on the number of check-ins and tokens per request: the system prompt, strategy list, and check-in (a few hundred input tokens) plus a short JSON response (about 100 output tokens).
- Latency depends on the network round trip and output length. The request blocks the redirect after a check-in, so it needs a timeout, after which the fallback is used.
- Keeping the prompt and output short limits both cost and latency.

## Privacy

- Only the fields listed above are sent. No account identifiers.
- The goal is free text and may contain personal details. The interface should tell users that the goal is sent to an external AI service.
- Prompts and raw model responses are not stored or logged by the app.
- Data handling on the provider side follows the provider's API terms.

## Limitations

- Suggestions may be generic, off-topic, or poorly matched to the barrier.
- `estimated_minutes` is the model's guess, not a measured duration.
- Output varies between calls for the same input.
- Goal text could contain instructions aimed at the model. Validation limits what can reach the page, but cannot judge whether an action is useful.
- The feature depends on an external service, network access, and an API key.
- Motiva suggests study steps. It is not counseling or mental-health support.
