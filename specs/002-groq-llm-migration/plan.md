# Technical Plan: Groq + Ollama LLM Migration

**Spec**: specs/002-groq-llm-migration/spec.md
**Status**: Implemented
**Date**: 2026-06-07

---

## 1. Tech Stack Choices

| Layer   | Before              | After                        | Reason              |
|---------|---------------------|------------------------------|---------------------|
| AI SDK  | google-generativeai | httpx (raw HTTP)             | No vendor SDK needed|
| Primary | Gemini 1.5 Flash    | Groq llama3-8b-8192          | Free, fast, open    |
| Vision  | Gemini 1.5 Flash    | Groq llama-3.2-11b-vision    | Free vision support |
| Fallback| None                | Ollama (llama3 + llava)      | Fully offline       |

---

## 2. Architecture

```
app.py
├── llm_chat(messages)
│   ├── _groq_chat()      → api.groq.com/openai/v1/chat/completions
│   └── _ollama_chat()    → localhost:11434/api/chat  (fallback)
│
└── llm_vision(img, mime, prompt)
    ├── _groq_vision()    → Groq vision endpoint
    └── _ollama_vision()  → Ollama llava (fallback)
```

Message format: OpenAI standard `[{role, content}]` throughout.

---

## 3. API Changes

No route changes. Internal LLM calls only.

---

## 4. Environment Variables

```
GROQ_API_KEY          = key from console.groq.com
GROQ_MODEL            = llama3-8b-8192
GROQ_VISION_MODEL     = llama-3.2-11b-vision-preview
OLLAMA_BASE_URL       = http://localhost:11434
OLLAMA_MODEL          = llama3
OLLAMA_VISION_MODEL   = llava
```

---

## 5. Risks & Mitigations

| Risk                      | Mitigation                            |
|---------------------------|---------------------------------------|
| Groq rate limits          | Fallback to Ollama automatically      |
| Ollama not installed      | Clear error message in logs           |
| Indian language quality   | System prompt enforces language match |
