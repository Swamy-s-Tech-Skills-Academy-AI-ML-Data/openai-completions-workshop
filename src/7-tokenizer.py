"""Token counting helper using tiktoken with model-aware encoding.

Usage examples:
  python 7-tokenizer.py                          # uses built-in sample texts
  python 7-tokenizer.py "Some prompt here"       # single arg
  python 7-tokenizer.py file:my_prompts.txt      # each line becomes an entry

Environment variable (optional):
  OPENAI_MODEL  -> attempts model-specific encoding; falls back to cl100k_base

Outputs per text: index, token count, first 60 chars, then a summary total.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable, List

import tiktoken


def pick_encoding(model: str | None):
    if model:
        try:
            return tiktoken.encoding_for_model(model)
        except Exception:
            pass  # fall through to default
    return tiktoken.get_encoding("cl100k_base")


def tokenize(text: str, encoding) -> List[int]:
    return encoding.encode(text)


def iter_inputs(argv: List[str]) -> Iterable[str]:
    if len(argv) <= 1:
        # default sample prompts
        yield "Suggest three concise pet salon taglines emphasizing friendly personalized care."
        yield "Purr Purrs Meow Purr purr purrs meow"
        return

    arg = " ".join(argv[1:])
    if arg.startswith("file:"):
        path = Path(arg.split("file:", 1)[1])
        if not path.exists():
            raise FileNotFoundError(path)
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                yield line
    else:
        yield arg


def main():
    model = os.getenv("OPENAI_MODEL")
    encoding = pick_encoding(model)
    print(f"Encoding: {encoding.name} (model hint: {model or 'None'})\n")

    total_tokens = 0
    rows = []
    for idx, text in enumerate(iter_inputs(sys.argv), 1):
        token_ids = tokenize(text, encoding)
        count = len(token_ids)
        total_tokens += count
        snippet = text.replace("\n", "\\n")[:60]
        rows.append((idx, count, snippet, token_ids))

    for idx, count, snippet, token_ids in rows:
        print(f"{idx:>2}. tokens={count:>4} | {snippet}")
        print(
            f"    ids={token_ids[:20]}{'...' if len(token_ids) > 20 else ''}")

    print("\nSummary:")
    print(f"  Text entries: {len(rows)}")
    print(f"  Total tokens: {total_tokens}")


if __name__ == "__main__":
    main()
