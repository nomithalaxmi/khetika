# Research: LLM Backend Options for Indian Language Support

**Date**: 2026-06-07

---

## Options Evaluated

| Provider  | Cost       | Indian Lang | Vision | Offline | Decision  |
|-----------|------------|-------------|--------|---------|-----------|
| Gemini    | Paid       | Good        | Yes    | No      | ❌ Removed |
| Groq      | Free tier  | Good        | Yes    | No      | ✅ Primary |
| Ollama    | Free       | Good        | llava  | Yes     | ✅ Fallback|
| OpenAI    | Paid       | Good        | Yes    | No      | ❌ Too costly|
| Hugging Face| Free     | Variable    | Some   | No      | ❌ Complex |

## Why Groq

- Free tier with generous limits (14,400 req/day on llama3-8b)
- OpenAI-compatible API — easy to migrate
- llama3-8b handles Telugu, Hindi, Tamil, Kannada well
- Vision support via llama-3.2-11b-vision-preview
- Fast inference (< 1s typical response)

## Why Ollama as Fallback

- Fully offline — critical for rural areas with poor connectivity
- Free forever, no API key needed
- llava model handles crop disease image analysis
- Runs on modest hardware (8GB RAM sufficient for llama3)
