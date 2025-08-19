# OpenAI Completions Workshop

_A focused, completions-only workshop: parameter control, quality vs cost, and reusable abstractions._

This folder contains customized, vendor-neutral OpenAI API demo materials rewritten to emphasize:

- Pure OpenAI (no Azure-specific client usage)
- Modern `openai` Python SDK patterns (v1+)
- Consolidated notebook-driven flow
- Live exploration of parameters: temperature, max_tokens, n, streaming
- Good practices: environment variables, token awareness, simple retry wrapper

## Structure

```text
openai-completions-workshop/
  ReadMe.md              # This file
  notebooks/
    openai_demo.ipynb  # Main 45‑minute session notebook
```

## Prerequisites

- Python 3.11+
- `pip install openai tiktoken python-dotenv` (plus any extras you add)
- Environment variable: `OPENAI_API_KEY`

Optionally create a local `.env` file:

```text
OPENAI_API_KEY=sk-...your key...
```

## 🔹 Installation & Setup

Steps (PowerShell on Windows shown; bash/zsh equivalents in comments):

```powershell
# 1. Verify tooling
python --version
pip --version

py -0p # To check installed Python versions (3.11+ required)

# 2. Create & activate virtual environment (force Python 3.12)
pip install virtualenv
py -3.12 -m venv .venv                  # Ensures the venv uses Python 3.12
. .venv/Scripts/Activate.ps1            # (bash/zsh: source .venv/bin/activate)

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. First install (Bootstrap alternative if no requirements.txt yet):
pip install openai tiktoken python-dotenv
pip freeze > requirements.txt

# 5. Install dependencies if requirements.txt exists
pip install -r requirements.txt         # If the file exists (preferred)

# 6. Provide your API key (either set env var or create .env)
setx OPENAI_API_KEY "sk-..."            # (bash/zsh: export OPENAI_API_KEY="sk-...")
# Then restart the shell so setx takes effect.
```

Optional version pinning: add a `.python-version` file at repo root (used by pyenv / some IDEs). Example:

```text
3.12
```

## Notebook Outline

1. Setup & sanity check
2. Model inventory & capability introspection
3. Baseline completion (simple naming prompt)
4. Prompt refinement & structure
5. Multiple candidates (n) + temperature sweep
6. Token counting & prompt compression
7. Presence / frequency penalties (style steering)
8. Streaming responses (incremental tokens)
9. Helper wrapper & retries
10. Recap & next steps

## Customization Notes

- All outputs intentionally not cached—run live for authentic behavior.
- Safe for public demo: avoid sensitive or ambiguous prompts.

## Extending

- Add function calling examples
- Insert evaluation harness cell (e.g., simple rubric scoring)
- Add cost estimation utility

## Completions-Only Toolkit (Added)

Lightweight abstraction for the dedicated completions session.

### Files

```text
session/
  completions_service.py          # Core service + retries
  requirements.txt                # Minimal deps
  tests/
    test_completions_service.py   # Mocked unit tests
```

### Install & Test (PowerShell)

```powershell
cd session
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
pytest -q
```

### Quick Run

```powershell
setx OPENAI_API_KEY "sk-..."  # restart shell
python completions_service.py
```

### Programmatic Use

```python
from completions_service import CompletionService
svc = CompletionService()
res = svc.safe_generate("List three benefits of clean code.")
print(res[0].text)
```

### Design Highlights

- Deferred client creation (import safety without key)
- Retry with exponential backoff (RateLimit / APIError)
- Normalized result dataclass (latency, tokens, finish_reason)
- Simple to extend with cost estimator or logging hooks

### Next Ideas

- Grid search (temperature × top_p) exporter
- Cost per 1K tokens annotation in output
- Stop sequence library for structured extraction

---
_Prepared automatically by session asset generator._
