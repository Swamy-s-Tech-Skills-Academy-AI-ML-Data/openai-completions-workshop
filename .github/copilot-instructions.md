# Copilot Instructions for openai-completions-workshop

These guidelines help generate consistent, safe, and maintainable suggestions.

## Project Summary

A focused set of OpenAI Completions API examples + a workshop notebook. Emphasis: vendor-neutral usage, environment-based configuration, token awareness, retries, and streaming.

## Tech Stack & Conventions

- Language: Python 3.12
- Style: PEP8, f-strings, type hints where helpful (avoid over-annotation)
- API: `openai` Python SDK (v1+ `OpenAI` client)
- Env vars: `OPENAI_API_KEY`, optional overrides (`OPENAI_MODEL`, `OAI_TEMP`, `NAME_CONTEXT`, etc.)
- Scripts live in `src/` and are single-file runnable examples.

## Patterns to Follow

1. Always read API key from `OPENAI_API_KEY` (never hardcode).
2. Prefer passing `api_key=` when constructing `OpenAI`; avoid global monkeypatching.
3. Provide small helper functions for repeated logic (e.g., temperature parsing) instead of duplicating blocks across files.
4. Keep examples minimal—avoid adding heavy abstractions unless requested.
5. Use streaming (`stream=True`) only when demonstrating incremental output; otherwise, default to simple calls.
6. When adding new examples, include a short docstring summarizing purpose + env vars.
7. For token work, use `tiktoken` with model-aware encoding fallback to `cl100k_base`.

## Anti-Patterns (Avoid)

- Hardcoding secrets or writing `.env` values into code.
- Adding unrelated frameworks (Flask/FastAPI) unless explicitly requested.
- Switching to Chat Completions API in these examples (stick to legacy `completions` focus for workshop scope unless scope changes).
- Overly clever one-liners that reduce readability.
- Introducing breaking changes to existing sample filenames without updating `README.md`.

## Error Handling & Retries

- For examples showing resilience, catch `RateLimitError` and `APIError`; exponential backoff: `sleep = base ** attempt + random()`.
- Keep retry count small (≤3) in samples.

## Naming & Files

- New sample scripts: prefix with incremental number + hyphen + short-kebab description (e.g., `8-cost-estimator.py`).
- Helper/shared utilities (if introduced) go under `src/utils/` with clear function names.

## Documentation Updates

- When adding a new script, update the Samples table in `README.md`.
- If adding new env vars, append them under "Common Environment Variables".

## Testing (Future Scope)

- If tests are added, prefer `pytest` and lightweight mocks (no external calls in CI).

## Security & Safety

- No PII or sensitive data in prompts.
- Ensure outputs are neutral; avoid domain-specific brand claims unless context provided.

## Example Skeleton for a New Script

```python
"""Short description (what it demonstrates).

Environment variables:
  OPENAI_MODEL (default gpt-4o-mini)
  OAI_TEMP (optional) – temperature override
"""
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not set.")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TEMP = float(os.getenv("OAI_TEMP", "0.7"))
client = OpenAI(api_key=api_key)

PROMPT = "<describe task succinctly>"
resp = client.completions.create(model=MODEL, prompt=PROMPT, max_tokens=120, temperature=TEMP)
print(resp.choices[0].text.strip())
```

## If Unsure

Provide a conservative, minimal suggestion; add a `TODO:` comment where a decision needs confirmation.

---

Generated guidance to keep AI suggestions aligned with project goals.
