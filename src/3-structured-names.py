"""Generate structured pet salon name ideas with optional JSON output.

Demonstrates: single completion, deterministic temperature, optional JSON formatting.
Set OUTPUT_FORMAT=json to request a JSON array; defaults to numbered text list.
"""
import os
import json
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "text").lower()  # 'text' or 'json'
client = OpenAI(api_key=api_key)

BASE_PROMPT = (
    "Suggest five creative, brandable names for a new pet salon. "
    "Each name should evoke: professional care, friendliness, and personalized service."
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
