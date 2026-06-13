# Khetika 🌿 — Smart Farming Assistant

A multilingual AI-powered farming chatbot for Indian farmers.  
Built with Flask + Gemini API + SQLite.

---

## Features

1. **Multilingual Q&A** — Ask in Telugu, Hindi, Tamil, Kannada, or English
2. **Full UI Language Switch** — Entire interface switches language (not just replies)
3. **Crop Photo Diagnosis** — Upload a leaf/crop image for instant disease detection (Gemini Vision)
4. **Seasonal Memory** — Set your crop + sowing date, get week-by-week task reminders
5. **Knowledge Base** — All queries logged to SQLite at `/knowledge`
6. **Modern Responsive UI** — Works on mobile and desktop

---

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Add your Gemini API key to `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   SECRET_KEY=khetika_secret_123
   ```
   Get a free key at: https://aistudio.google.com

3. Run:
   ```
   python app.py
   ```

4. Open: http://localhost:5000

---

## Project Structure

```
khetika/
├── app.py               # Flask routes + Gemini integration
├── database.py          # SQLite helpers (queries, profiles, alerts)
├── crop_calendar.py     # Week-by-week task data for 5 crops
├── requirements.txt
├── .env
├── POC.md               # Proof of Concept document
├── CONTRIBUTING.md      # How to contribute
├── SPECKIT.md           # Full technical specification
├── USER_MANUAL.md       # End-user guide
├── AGENTS.md            # AI agent system design
├── templates/
│   ├── base.html
│   ├── chat.html        # Main chat UI — multilingual, modern
│   └── knowledge_base.html
└── static/
    └── chat.js
```

---

## Supported Languages (UI + Replies)

| Language | Code | Status |
|----------|------|--------|
| English | en | ✅ Full |
| తెలుగు (Telugu) | te | ✅ Full |
| हिंदी (Hindi) | hi | ✅ Full |
| தமிழ் (Tamil) | ta | ✅ Full |
| ಕನ್ನಡ (Kannada) | kn | ✅ Full |

---

## Supported Crops (Seasonal Memory)

Rice · Cotton · Maize · Tomato · Wheat

---

## Tech Stack

- **Backend**: Flask, Python
- **AI**: Google Gemini 1.5 Flash (text + vision)
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Vanilla JS, Google Fonts (Baloo 2 + Noto Sans Indian Scripts)

---

## Documentation

| File | Description |
|------|-------------|
| [POC.md](POC.md) | Proof of concept — goals, architecture, validation |
| [SPECKIT.md](SPECKIT.md) | Full API and technical specification |
| [USER_MANUAL.md](USER_MANUAL.md) | End-user guide with screenshots and tips |
| [AGENTS.md](AGENTS.md) | AI agent design, flows, and extension guide |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute code, crops, and translations |

---

## New Features (v2)

### 🎙️ Voice Input
Tap the microphone button to speak your question in Telugu, Hindi, Tamil, Kannada, or English. Uses the Web Speech API (Chrome/Edge supported). Auto-sends after you finish speaking.

### 💰 Real-time Mandi Prices
Live commodity prices from India's Open Government Data platform (`data.gov.in`). Search any crop (Tomato, Rice, Onion, Cotton, etc.) to see modal/min/max prices across markets. Falls back to representative sample data if API key is not configured.

**Setup:** Register at [data.gov.in](https://data.gov.in) → My Account → API Keys. Add to `.env`:
```
DATA_GOV_API_KEY=your_key_here
```

### 📱 SMS Alerts (Twilio)
Farmers subscribe with their mobile number to receive weekly crop task reminders via SMS. Supports all 5 languages.

**Setup:** [Twilio free trial](https://www.twilio.com/try-twilio) gives ~1000 SMS credits. Add to `.env`:
```
TWILIO_ACCOUNT_SID=ACxxxxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM_NUMBER=+1XXXXXXXXXX
```

**Trigger weekly SMS:** Call `POST /sms/send_weekly` with header `X-Cron-Secret: <your_cron_secret>` from a cron job or Render Cron.

### 🌤 Weather Integration
Shows real-time weather for the farmer's GPS location with farming-specific advice (spray warnings, irrigation tips, fungal disease alerts). Uses OpenWeatherMap API.

**Setup:** Free key at [openweathermap.org](https://openweathermap.org/api). Add to `.env`:
```
OPENWEATHER_API_KEY=your_key_here
```

### 📱 PWA Offline Support
Khetika is now a Progressive Web App (PWA):
- **Install to home screen** on Android/iOS/desktop
- **Offline fallback page** with farming tips when disconnected
- **Service Worker** caches assets for instant loads
- **Offline indicator** in the chat UI
- `manifest.json` with app icons and shortcuts

No setup required — works automatically.
