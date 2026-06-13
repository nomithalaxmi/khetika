# Agents — Khetika AI System Design 🤖

> This document describes the AI agent architecture behind Khetika and how to extend it.

---

## Current Agent: AgriBot

Khetika uses a **single-agent, multi-modal** architecture powered by Google Gemini 1.5 Flash.

### Agent Identity

```
Name:     AgriBot
Role:     Agricultural assistant for Indian farmers
Model:    gemini-1.5-flash
Modality: Text + Vision (image understanding)
Memory:   Short-term (last 10 turns, session-scoped)
```

### System Prompt

```
You are AgriBot, an agricultural assistant for Indian farmers.
Answer farming questions clearly and practically.
Topics: crop diseases, fertilizers, irrigation, pest control,
        soil health, weather, mandi prices.
If the user writes in Telugu, reply in Telugu.
If the user writes in Hindi, reply in Hindi.
Otherwise reply in English.
Keep answers short (3-5 lines max). Be friendly and practical.
```

---

## Agent Capabilities

| Capability | Implementation |
|------------|---------------|
| **Multilingual Q&A** | langdetect → Gemini prompt |
| **Vision / Disease Detection** | Base64 image → Gemini vision |
| **Seasonal Reminders** | crop_calendar.py (rule-based lookup) |
| **Language-Aware Response** | System prompt instruction |
| **Conversation Memory** | Session-stored history (10 turns) |

---

## Agent Flow (Text)

```
User types question
        │
        ▼
langdetect() → detect language (en/te/hi/...)
        │
        ▼
Build messages[] with:
  - system prompt (role/persona)
  - last 10 history turns
  - current user message
        │
        ▼
gemini.generate_content(messages)
        │
        ▼
Return reply + detected lang
        │
        ▼
Log to SQLite (queries table)
```

---

## Agent Flow (Vision)

```
User uploads image (+ optional text)
        │
        ▼
Read image bytes → base64 encode
        │
        ▼
Build prompt:
  - system prompt + user question
  - mime_type + base64 data (Gemini multimodal format)
        │
        ▼
vision_model.generate_content([image_dict, prompt_text])
        │
        ▼
Return diagnosis + remedy
```

---

## Proposed Multi-Agent Extension

For future versions, Khetika can be extended into a **multi-agent pipeline**:

```
┌─────────────────────────────────────────────────────┐
│                   Router Agent                      │
│  Classifies intent: Q&A / Disease / Weather / Price │
└──────────────┬──────────────────────┬───────────────┘
               │                      │
        ┌──────▼──────┐        ┌──────▼──────┐
        │  AgriBot     │        │  VisionBot  │
        │ (text Q&A)   │        │ (diagnosis) │
        └──────┬──────┘        └──────┬──────┘
               │                      │
        ┌──────▼──────┐        ┌──────▼──────┐
        │  WeatherBot  │        │  MandiBot   │
        │ (IMD/OpenW.) │        │ (live price)│
        └─────────────┘        └─────────────┘
```

---

## Extending the Agent

### Add a New Persona / Domain

In `app.py`, modify `SYSTEM_PROMPT`:

```python
SYSTEM_PROMPT = """
You are AgriBot, an agricultural assistant...
# Add: Also answer questions about government farming schemes (PM-KISAN, etc.)
"""
```

### Add a Tool-Calling Agent (Future)

When Google Gemini supports function calling in this SDK version:

```python
tools = [
    {"name": "get_weather", "description": "Get current weather for a location"},
    {"name": "get_mandi_price", "description": "Get today's crop price from market"},
]
response = model.generate_content(messages, tools=tools)
```

### Add Memory Persistence

Replace session-based history with SQLite:
```python
# Store per session_id in DB instead of session cookie
save_history(session_id, user_msg, bot_reply)
history = load_history(session_id, limit=10)
```

---

## Safety & Guardrails

- Gemini has built-in safety filters for harmful content
- No medical/veterinary advice — redirected to agricultural domain only
- Language detection prevents mismatched-language replies
- Session isolation — each farmer's profile is separate

---

## Performance Notes

- Gemini 1.5 Flash: average response ~1–2 seconds
- Vision inference: ~2–4 seconds (base64 encoding adds overhead)
- SQLite logging: < 5ms per query
- Crop calendar lookup: O(1) dictionary access

---

*AGENTS.md v1.0 — Khetika Smart Farming Assistant*
