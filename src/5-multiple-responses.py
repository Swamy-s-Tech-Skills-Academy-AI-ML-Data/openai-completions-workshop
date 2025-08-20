"""Use best_of to internally sample multiple completions and return the top (by logprob).

Environment variables:
    OPENAI_MODEL  (default gpt-4o-mini)
    OAI_TEMP / OAI_TEMPERATURE (preferred temperature override)
    BEST_OF       (default 5)
    MAX_TOKENS    (default 120)
    NAME_CONTEXT  (default "a privacy-focused personal finance app")

Generates ONE standout brand name for the supplied context under clear constraints.
"""
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def _parse_temp():
    raw = os.getenv("OAI_TEMP") or os.getenv(
        "OAI_TEMPERATURE") or os.getenv("TEMP", "0.7")
    if any(ch in raw for ch in ("\\", ":", "/")) and not raw.replace('.', '', 1).isdigit():
        return 0.7
    try:
        return float(raw)
    except ValueError:
        return 0.7


TEMP = _parse_temp()
BEST_OF = int(os.getenv("BEST_OF", "5"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "120"))

client = OpenAI(api_key=api_key)

CONTEXT = os.getenv("NAME_CONTEXT", "a privacy-focused personal finance app")
PROMPT = (
    f"Provide ONE standout, memorable brand name for {CONTEXT}. "
    "Constraints: 1) 1–3 words, 2) globally pronounceable, 3) no generic terms like 'Solutions', 'Services', 'Tech', 4) avoid existing famous brands, 5) avoid leading/trailing quotes. Return ONLY the name."
)

response = client.completions.create(
    model=MODEL,
    prompt=PROMPT,
    temperature=TEMP,
    max_tokens=MAX_TOKENS,
    best_of=BEST_OF,
    n=1,
    stop=None,
)

choice = response.choices[0]
print(f"Model: {MODEL}  best_of={BEST_OF}  temperature={TEMP}")
print("Prompt:\n" + PROMPT + "\n")
print("Selected Name:\n" + choice.text.strip())
