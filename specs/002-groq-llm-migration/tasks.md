# Task List: Groq + Ollama LLM Migration

**Status**: Complete ✅
**Date**: 2026-06-07

---

## Phase 1 — Remove Gemini

- [x] T01: Remove `google-generativeai` from requirements.txt *(15m)*
- [x] T02: Add `httpx` to requirements.txt *(5m)*
- [x] T03: Remove all `genai` imports from app.py *(15m)*

## Phase 2 — Groq Integration

- [x] T04: Implement `_groq_chat()` using httpx POST *(1h)*
- [x] T05: Implement `_groq_vision()` with base64 image support *(1h)*
- [x] T06: Implement `llm_chat()` dispatcher with try/except *(30m)*
- [x] T07: Implement `llm_vision()` dispatcher with try/except *(30m)*

## Phase 3 — Ollama Fallback

- [x] T08: Implement `_ollama_chat()` *(45m)*
- [x] T09: Implement `_ollama_vision()` using llava *(45m)*

## Phase 4 — Config & Docs

- [x] T10: Update .env.example with all new variables *(15m)*
- [x] T11: Update constitution.md — change AI stack from Gemini to Groq *(15m)*
- [x] T12: Update CHANGELOG.md *(10m)*
- [x] T13: Update README.md setup instructions *(20m)*

## Phase 5 — Testing

- [x] T14: Test text chat in all 5 languages with Groq
- [x] T15: Test image upload with Groq vision
- [x] T16: Test fallback to Ollama (by unsetting GROQ_API_KEY)
