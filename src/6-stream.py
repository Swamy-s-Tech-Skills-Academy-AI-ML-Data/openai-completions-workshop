"""Stream a longer completion token-by-token.

Environment variables:
    OPENAI_MODEL (default gpt-3.5-turbo-instruct)
    OAI_TEMP / OAI_TEMPERATURE / TEMP (temperature precedence, default 0.8)
    MAX_TOKENS (default 400)
    NAME_CONTEXT (default "an AI-powered personal language coach")
"""
import os
import sys
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-instruct")


def _parse_temp():
    raw = os.getenv("OAI_TEMP") or os.getenv(
        "OAI_TEMPERATURE") or os.getenv("TEMP", "0.8")
    if any(ch in raw for ch in ("\\", ":", "/")) and not raw.replace('.', '', 1).isdigit():
        return 0.8
    try:
        return float(raw)
    except ValueError:
        return 0.8


TEMP = _parse_temp()
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "400"))

client = OpenAI(api_key=api_key)

CONTEXT = os.getenv("NAME_CONTEXT", "an AI-powered personal language coach")
PROMPT = (
    f"Generate three distinct premium brand names AND for each a two-sentence tagline for {CONTEXT}. "
    "Requirements: 1) Names 1–3 words, 2) Taglines highlight differentiation & value, "
    "3) Avoid generic buzzwords, 4) No numbered list. Format exactly as:\n\n"
    "Name: <Name 1>\nTagline: <Tagline 1>\n\nName: <Name 2>\nTagline: <Tagline 2>\n\nName: <Name 3>\nTagline: <Tagline 3>"
)

print(f"Model: {MODEL}  temperature={TEMP}  streaming...\n")
buffer = []
for chunk in client.completions.create(
        model=MODEL,
        prompt=PROMPT,
        temperature=TEMP,
        max_tokens=MAX_TOKENS,
        n=1,
        stream=True,
        stop=None):
    for choice in chunk.choices:
        text = getattr(choice, 'text', '')
        if text:
            buffer.append(text)
            sys.stdout.write(text)
            sys.stdout.flush()

print("\n\n---\nDone. Total characters streamed:", sum(len(t) for t in buffer))
