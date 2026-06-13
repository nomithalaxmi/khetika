# Feature Spec: Groq + Ollama LLM Migration

**Status**: Implemented
**Author**: Naga Gireesh Reddy
**Date**: 2026-06-07
**Spec ID**: 002

---

## 1. Problem Statement

Khetika originally used Google Gemini 1.5 Flash as its AI backend.
Gemini requires a paid API key, creates vendor lock-in, and offers no
offline fallback — making it unsuitable for rural deployment where
connectivity is limited and cost matters.

---

## 2. User Story

> As a developer deploying Khetika,
> I want to use a free, open LLM backend with an offline fallback,
> So that the app works without a paid API key and without internet.

---

## 3. Acceptance Criteria

- [x] Gemini dependency fully removed (no google-generativeai import)
- [x] Groq cloud API used as primary (free tier, OpenAI-compatible)
- [x] Ollama local used as fallback when Groq fails or key is absent
- [x] Text chat works via Groq (llama3-8b-8192)
- [x] Image/vision works via Groq (llama-3.2-11b-vision-preview)
- [x] Automatic fallback logged as warning, not an error to user
- [x] All env vars documented in .env.example
- [x] requirements.txt updated (httpx replaces google-generativeai)
- [x] Indian language responses preserved (Telugu, Hindi, Tamil, Kannada)

---

## 4. Out of Scope

- Streaming responses
- Multiple simultaneous LLM providers (A/B testing)
- Fine-tuned models

---

## 5. Open Questions

All resolved. Migration shipped.
