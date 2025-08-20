"""Generate multiple brand taglines for a fictional eco-friendly cleaning product.

Demonstrates: basic completion call, temperature for creativity, and simple
post-processing to trim/normalize outputs.

Prerequisites: Environment variable OPENAI_API_KEY must be set.
Optional: Set OPENAI_MODEL to override default model name.
"""
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-instruct")
client = OpenAI(api_key=api_key)

PROMPT = (
    "You are a branding assistant. Generate 5 concise, punchy tagline options for an "
    "eco-friendly household cleaning spray named 'PureMist'. Each tagline should: \n"
    "1) Emphasize natural ingredients, \n"
    "2) Convey effectiveness, and \n"
    "3) Stay under 12 words.\n\n"
    "Return them as a simple numbered list."
)

response = client.completions.create(
    model=MODEL,
    prompt=PROMPT,
    temperature=0.85,   # higher creativity
    max_tokens=120,
    n=1,
)

raw_text = response.choices[0].text.strip()

# Basic normalization: split lines, strip, drop empties
lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

print("Model:", MODEL)
print("Prompt:\n" + PROMPT)
print("\nTagline Candidates:")
for line in lines:
    print(line)
