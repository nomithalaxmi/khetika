# Khetika — Project Constitution
## Spec-Kit v2.0 (updated post Groq migration)

This constitution defines the core principles, design rules, and
non-negotiable constraints for the Khetika project.
All feature specs must be consistent with this document.

---

## 1. Mission

Khetika's mission is to make agricultural knowledge accessible to every
Indian farmer, in their own language, through a simple chat interface.
Every design decision must serve that mission.

---

## 2. Core Principles

### P1 — Language First
The UI must be fully usable in Telugu, Hindi, Tamil, and Kannada — not
just English. AI replies must match the user's input language.

### P2 — Farmer-Centric Simplicity
The interface must be usable by someone with basic smartphone literacy.
No jargon. No complex menus. One tap to ask a question.

### P3 — Practical Answers
AI responses should be actionable within 3–5 lines. No lengthy academic
explanations. A farmer reading on a low-end Android phone must be able
to act on the answer immediately.

### P4 — Local-First Data
All query logging happens locally (SQLite). No farmer data is sent to
third parties beyond the AI inference call.

### P5 — Zero Friction Setup
The app must run with a single command (`python app.py`) after
`pip install -r requirements.txt`. No Docker required for development.

### P6 — Open Source LLM Priority
Prefer open, free, or low-cost LLM backends. Avoid vendor lock-in to
any single proprietary AI provider.

---

## 3. Architecture Rules

- Backend  : Flask (Python 3.11+). No FastAPI, no Django.
- AI       : Groq cloud (primary) + Ollama local (fallback). No Gemini.
  - Text model  : llama3-8b-8192 via Groq (free tier)
  - Vision model: llama-3.2-11b-vision-preview via Groq
  - Fallback    : Ollama (llama3 + llava) for fully offline use
- Database : SQLite for POC. PostgreSQL allowed for production.
- Frontend : Bootstrap 5 + Vanilla JS. No React, no Vue.
- Fonts    : Baloo 2 + Noto Sans Indian Scripts. No system fonts.
- HTTP     : httpx (sync). No requests, no aiohttp.

---

## 4. Feature Acceptance Criteria

A feature is complete when:
1. It works in all 5 supported languages (en, te, hi, ta, kn)
2. It is tested (unit test in `tests/`)
3. It is documented (USER_MANUAL.md updated if user-facing)
4. It passes all CI checks (lint, format, type_check, security, test)
5. CHANGELOG.md is updated under [Unreleased]
6. Its spec folder has spec.md + plan.md + tasks.md all marked done

---

## 5. Non-Goals (POC Scope)

- Real-time market prices (no live API yet)
- User authentication or accounts
- Offline / PWA support
- Native mobile app
- RTL language support (Urdu, Arabic)

---

## 6. Quality Thresholds

| Metric           | Threshold        |
|------------------|------------------|
| Test coverage    | ≥ 60%            |
| Pylint score     | ≥ 7.0            |
| Bandit severity  | No HIGH issues   |
| Ruff violations  | 0                |

---

## 7. LLM Provider Policy

| Provider | Role     | Cost      | Notes                        |
|----------|----------|-----------|------------------------------|
| Groq     | Primary  | Free tier | Fast, OpenAI-compatible API  |
| Ollama   | Fallback | Free      | Local, fully offline         |

Never hardcode API keys. Always read from environment variables.
Always implement Groq → Ollama fallback in every LLM call.
