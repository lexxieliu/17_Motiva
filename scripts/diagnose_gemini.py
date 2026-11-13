"""Find which part of the Gemini request is slow. Run from the project folder:

    python scripts/diagnose_gemini.py [model ...]

Prints only status and timings, never the API key.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from google import genai
from google.genai import types

from motiva.ai_suggestions import RESPONSE_SCHEMA, SYSTEM_INSTRUCTION

key = os.environ.get("GEMINI_API_KEY", "")
model = os.environ.get("GEMINI_MODEL", "")
print(f"key loaded: {bool(key)} (length {len(key)}), model: {model}")

client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=30_000))

# 1. Is the key valid, and which Flash models can it use?
try:
    names = [m.name for m in client.models.list() if "flash" in m.name]
    print("key OK. flash models available:", ", ".join(n.replace("models/", "") for n in names[:15]))
except Exception as e:
    print("KEY/LIST FAILED:", type(e).__name__, str(e)[:300])
    sys.exit(1)

prompt = json.dumps({"goal": "Review chapter 4 for my chemistry midterm", "barrier": "Unsure where to start",
                     "available_minutes": 25, "confidence_1_to_5": 2, "importance_1_to_5": 5, "demand_1_to_5": 4})


def trial(label, **cfg):
    start = time.perf_counter()
    try:
        r = client.models.generate_content(model=label.split(":")[0], contents=prompt, config=types.GenerateContentConfig(**cfg))
        ms = int((time.perf_counter() - start) * 1000)
        u = r.usage_metadata
        print(f"[OK  ] {label}: {ms} ms, thoughts={getattr(u, 'thoughts_token_count', None)}, "
              f"output={getattr(u, 'candidates_token_count', None)} -> {(r.text or '')[:80]!r}")
    except Exception as e:
        ms = int((time.perf_counter() - start) * 1000)
        print(f"[FAIL] {label}: {ms} ms, {type(e).__name__}: {str(e)[:150]}")


low = types.ThinkingConfig(thinking_level="low")
candidates = sys.argv[1:] or ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-flash-lite-latest"]
for model in candidates:
    trial(f"{model}: JSON + schema, thinking low (what the app sends)", max_output_tokens=2048, thinking_config=low,
          response_mime_type="application/json", response_schema=RESPONSE_SCHEMA, system_instruction=SYSTEM_INSTRUCTION)
