# OpenAI Completions Workshop

_A focused, completions-only workshop: parameter control, quality vs cost, and reusable abstractions._

This repository contains customized, vendor-neutral OpenAI API demo materials written to emphasize:

- Pure OpenAI (no Azure-specific client usage)
- Modern `openai` Python SDK patterns (v1+)
- Consolidated notebook-driven flow
- Live exploration of parameters: temperature, max_tokens, n, streaming
- Good practices: environment variables, token awareness, simple retry wrapper

## Structure

```text
openai-completions-workshop/
  README.md                          # This file
  notebooks/
    openai_completions_workshop.ipynb    # Legacy / original workshop notebook
    text_generation_with_completions.ipynb # 14 end-to-end text generation use cases (new)
  src/                               # Stand‑alone script samples (see section below)
  requirements.txt                   # Generated after first pip install freeze
  .python-version                    # (Optional) Python toolchain pin
  .copilot/                          # Copilot guidance config
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

## Notebooks

### 1. `openai_completions_workshop.ipynb`

Original 45‑minute, parameter‑oriented flow (model listing, parameter sweeps, streaming, penalties, token budgeting, retry helper intro).

### 2. `text_generation_with_completions.ipynb`

Feature-style showcase of **14 concrete text generation use cases** implemented with a shared resilient helper (`get_completion`) featuring:

- Environment‑driven configuration (`OPENAI_MODEL`, `OAI_TEMP` / `OAI_TEMPERATURE`, `OAI_MAX_TOKENS`)
- Lightweight retry (RateLimitError / APIError) with exponential backoff + jitter
- Dataclass result wrapper (text, tokens, retries)
- Deterministic vs creative temperature tuning per task

Use Cases Covered:

1. Summarization  
2. Sentiment Classification  
3. Multilingual Generation + Translation  
4. Semantic Interpretation of Idiom  
5. Factual Recall / Explanatory Response  
6. Code Generation & Explanation (delimiter parsing)  
7. Conversational Agent (FAQ Assistant with tiny in‑memory KB)  
8. Style Transfer / Tone Adaptation  
9. Data‑to‑Text Generation (tabular → narrative + aggregate insight)  
10. Creative Writing (multi‑style variants + optional title)  
11. Question Generation (tiered cognitive levels + numbering cleanup)  
12. Entity Extraction with Explanation (typed bullet list)  
13. Paraphrasing / Rewriting (multi‑constraint variants)  
14. Email / Document Drafting (structured sections + variant)

Each cell is intentionally self‑contained to minimize cross‑cell coupling and highlight prompt patterns.

## Sample Scripts (`src/`)

Seven focused Python scripts demonstrating core completion patterns. Each uses the `OPENAI_API_KEY` environment variable (and optional overrides noted). Run from the repo root or `code/` directory after activating your virtual env.

| Script | Purpose | Key Args / Env Vars |
|--------|---------|---------------------|
| `1-list-openai-models.py` | Lists available models (prints basic metadata + IDs) | `OPENAI_MODEL` (optional display override) |
| `2-brand-taglines.py` | Generates 5 numbered taglines for a product ("PureMist" eco cleaner example) | `OPENAI_MODEL` |
| `3-structured-names.py` | Produces 5 brand names (numbered or JSON) | `OUTPUT_FORMAT` (`text`/`json`), `NAME_CONTEXT` |
| `4-multiple-response.py` | Parallel n completions for multiple name variants | `NAME_COUNT`, `OAI_TEMP` / `OAI_TEMPERATURE`, `NAME_CONTEXT` |
| `5-multiple-responses.py` | Uses `best_of` to internally sample & return a single top name | `BEST_OF`, `MAX_TOKENS`, `OAI_TEMP`, `NAME_CONTEXT` |
| `6-stream.py` | Streams three names + taglines structure token-by-token | `NAME_CONTEXT`, `OAI_TEMP`, `MAX_TOKENS` |
| `7-tokenizer.py` | Token counting helper (model-aware) for prompts | `OPENAI_MODEL`; CLI arg or `file:prompts.txt` |

### Quick Run Examples (PowerShell)

```powershell
# 1. List models
py src/1-list-openai-models.py

# 2. Taglines (override model)
$env:OPENAI_MODEL='gpt-4o-mini'; py src/2-brand-taglines.py

# 3. Structured names as JSON
$env:OUTPUT_FORMAT='json'; $env:NAME_CONTEXT='a biodegradable travel accessory brand'; py src/3-structured-names.py

# 4. Multiple parallel name candidates
$env:NAME_CONTEXT='an AI meeting summarizer'; $env:NAME_COUNT='4'; $env:OAI_TEMP='0.8'; py src/4-multiple-response.py

# 5. best_of single winner
$env:NAME_CONTEXT='a privacy-focused personal finance app'; $env:BEST_OF='6'; py src/5-multiple-responses.py

# 6. Streaming structured output
$env:NAME_CONTEXT='an AI-powered personal language coach'; py src/6-stream.py

# 7. Token counting
py src/7-tokenizer.py "Summarize quarterly revenue drivers succinctly."
py src/7-tokenizer.py file:my_prompts.txt
```

### Common Environment Variables

- `OPENAI_API_KEY` (required) – your API key
- `OPENAI_MODEL` – default model (falls back to `gpt-4o-mini` if unset)
- `OAI_TEMP` / `OAI_TEMPERATURE` – preferred temperature override (scripts avoid clashing with system `TEMP`)
- `NAME_CONTEXT` – swaps in different product/service contexts
- `OUTPUT_FORMAT` – `json` or `text` (script 3)
- `BEST_OF`, `NAME_COUNT`, `MAX_TOKENS` – sampling / control parameters

### Suggested Progression

1 → 2 → 3 introduces basic prompting, structure & format control.
4 vs 5 compares explicit parallel sampling (`n`) to internal `best_of` ranking.
6 shows streaming for long outputs.
7 helps you budget tokens before sending prompts.

## Customization Notes

- All outputs intentionally not cached—run live for authentic behavior.
- Safe for public demo: avoid sensitive or ambiguous prompts.

## Extending & Ideas

Planned / easy wins:

- Add automated evaluation harness (LLM rubric or regex assertions) for select prompts
- Cost estimation helper (tokens × price) + per‑use case tally
- Structured JSON output examples (e.g., schema extraction) with validation
- Retrieval augmentation stub (swap in vector lookup for FAQ)
- Batch prompt runner for grid searching temperature / max_tokens combinations
- Streaming variants for selected creative tasks

## Completions-Only Toolkit (Optional Add‑On)

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

### Next Toolkit Ideas

- Grid search (temperature × top_p) exporter
- Cost per 1K tokens annotation in output
- Stop sequence library for structured extraction
- JSON schema enforcement (retry on invalid parse)

---
_Prepared automatically by session asset generator._
