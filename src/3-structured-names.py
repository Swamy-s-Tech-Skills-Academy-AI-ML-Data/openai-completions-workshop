"""Generate structured brand name ideas with optional JSON output.

Demonstrates: single completion, deterministic temperature, optional JSON formatting.
Environment:
    OPENAI_MODEL   -> override model (default gpt-3.5-turbo-instruct)
    OUTPUT_FORMAT  -> 'text' (default) or 'json'
    NAME_CONTEXT   -> business / product context (default: eco-friendly smart home cleaning device)

Set OUTPUT_FORMAT=json to request a JSON array; otherwise returns a numbered list.
"""
import os
import json
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-instruct")
OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "text").lower()  # 'text' or 'json'
client = OpenAI(api_key=api_key)

CONTEXT = os.getenv(
    "NAME_CONTEXT", "an eco-friendly smart home cleaning device brand")

BASE_PROMPT = (
    f"Generate five distinct, concise, brandable names for {CONTEXT}. "
    "Each name must: 1) be original (avoid tired clichés), 2) be pronounceable globally, "
    "3) contain at most 3 words, and 4) avoid generic terms like 'Solution(s)' or 'Service(s)'."
)

if OUTPUT_FORMAT == "json":
    full_prompt = (
        BASE_PROMPT +
        "\nReturn ONLY a compact JSON array of strings (no keys, no extra text)."
    )
else:
    full_prompt = (
        BASE_PROMPT +
        "\nReturn as a clean numbered list (1-5) without extra commentary."
    )

response = client.completions.create(
    model=MODEL,
    prompt=full_prompt,
    temperature=0.5,   # lower for more deterministic naming
    max_tokens=150,
    n=1,
)

text = response.choices[0].text.strip()

print(f"Model: {MODEL}")
print(f"Format requested: {OUTPUT_FORMAT}")
print("Prompt:\n" + full_prompt + "\n")

if OUTPUT_FORMAT == "json":
    # Attempt to parse JSON; if it fails just print raw.
    try:
        ideas = json.loads(text)
        if isinstance(ideas, list):
            print("Parsed JSON ideas:")
            for i, name in enumerate(ideas, 1):
                print(f"{i}. {name}")
        else:
            print("Unexpected JSON structure, raw text:\n" + text)
    except json.JSONDecodeError:
        print("Failed to parse JSON; raw text follows:\n" + text)
else:
    print("Name Ideas:\n" + text)
