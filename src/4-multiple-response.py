"""Generate multiple brand name ideas in parallel (n completions).

Uses the OpenAI Completions API with configurable parameters via env vars:
  OPENAI_MODEL  (default gpt-3.5-turbo-instruct)
  NAME_COUNT    (default 5) -> number of parallel completions (n)
  TEMP          (default 0.7)
"""
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-instruct")
N = int(os.getenv("NAME_COUNT", "5"))


def _parse_temp():
    """Return temperature as float.

    Prefers OAI_TEMP or OAI_TEMPERATURE. Falls back to 0.7. Ignores the Windows
    system TEMP path (which contains a backslash or colon)."""
    raw = os.getenv("OAI_TEMP") or os.getenv(
        "OAI_TEMPERATURE") or os.getenv("TEMP", "0.7")
    # If it looks like a Windows temp path, ignore.
    if any(ch in raw for ch in ("\\", ":", "/")) and not raw.replace('.', '', 1).isdigit():
        return 0.7
    try:
        return float(raw)
    except ValueError:
        return 0.7


TEMP = _parse_temp()

client = OpenAI(api_key=api_key)

CONTEXT = os.getenv(
    "NAME_CONTEXT", "a sustainable smart hydration tracking bottle")
PROMPT = (
    f"Suggest creative, brandable names for {CONTEXT}. "
    "Each name must be ≤3 words, globally pronounceable, avoid overused buzzwords, and feel premium."
)

response = client.completions.create(
    model=MODEL,
    prompt=PROMPT,
    temperature=TEMP,
    max_tokens=60,
    n=N,
    stop=None,
)

print(f"Model: {MODEL}  n={N}  temperature={TEMP}")
print("Prompt:\n" + PROMPT + "\n")
for idx, choice in enumerate(response.choices, 1):
    print(f"{idx}. {choice.text.strip()}")
