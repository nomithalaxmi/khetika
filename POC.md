# Proof of Concept — Khetika 🌿

## Overview

This document describes the proof-of-concept (POC) phase of Khetika, a multilingual AI-powered smart farming assistant designed for Indian farmers — particularly those in Telugu, Hindi, and English-speaking agricultural communities.

---

## Problem Statement

Indian farmers — especially smallholder farmers — face:
- Language barriers when accessing crop advisory services
- Lack of timely, practical advice on disease detection, irrigation, and pest control
- Limited access to agronomists in rural areas
- No week-by-week seasonal reminders for crop management

---

## POC Goals

| Goal | Status |
|------|--------|
| Multilingual Q&A (Telugu, Hindi, English) | ✅ Done |
| Crop photo disease diagnosis via vision AI | ✅ Done |
| Seasonal crop profile + weekly task reminders | ✅ Done |
| Query knowledge base (SQLite logging) | ✅ Done |
| Language-switch UI (whole page) | ✅ Done |

---

## Architecture (POC)

```
User (Browser)
    │
    ▼
Flask Web App (app.py)
    ├── /chat         → Gemini 1.5 Flash (text + vision)
    ├── /profile/save → SQLite (farmer profile)
    ├── /profile/weekly_task → crop_calendar.py
    └── /knowledge    → SQLite query log viewer

Database (SQLite via database.py)
    ├── queries table    (question, answer, lang, timestamp)
    ├── farmer_profiles  (session_id, crop, sowing_date, lang)
    └── alerts           (session_id, week, task, timestamp)
```

---

## AI Model Used

- **Model**: Google Gemini 1.5 Flash
- **Capabilities used**: Text generation + Vision (image understanding)
- **Prompt strategy**: System-prompted with persona (AgriBot), language detection via `langdetect`, auto-reply in detected language

---

## POC Limitations

- No user authentication (session-based only)
- Mandi price data is AI-generated (not live market feeds)
- Crop calendar covers only 5 crops (Rice, Cotton, Maize, Tomato, Wheat)
- No offline support yet

---

## Next Steps (Post-POC)

1. Live mandi price API integration (Agmarknet)
2. Weather API integration (IMD / OpenWeather)
3. SMS alerts for weekly crop tasks (Twilio/MSG91)
4. Mobile-first PWA with offline mode
5. Expand crop calendar to 20+ crops
6. User accounts with full history

---

## Validation

The POC was validated by:
- Testing multilingual responses in Telugu, Hindi, and English
- Uploading leaf images with visible disease symptoms
- Setting a crop profile and verifying correct weekly task display
- Confirming SQLite knowledge base logging per query

---

*POC built by: Nomitha laxmi .ch| IcfaiTech, Hyderabad*  
*Stack: Python · Flask · Gemini API · SQLite · Bootstrap 5*
