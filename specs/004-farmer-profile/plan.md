# Technical Plan: Farmer Profile & Session Management

**Spec**: specs/004-farmer-profile/spec.md
**Status**: Implemented

---

## 1. Architecture

```
database.py
├── init_db()                 → creates farmer_profile, queries, weekly_alerts tables
├── save_farmer_profile(session_id, crop_name, sowing_date, language)
├── get_farmer_profile(session_id) → (crop_name, sowing_date, language)
├── get_all_profiles()        → admin view of all stored profiles
├── log_query(question, answer, language)
└── get_top_queries(limit)    → recent/most-asked queries for knowledge base

app.py
├── session["sid"]            → os.urandom(8).hex(), generated on first visit
├── GET  /                     → load profile via get_farmer_profile(sid), pre-fill form
├── POST /profile/save         → persist crop, sowing date, language
└── GET  /knowledge             → render knowledge_base.html with get_top_queries()

templates/
├── base.html          → shared layout, loads profile data into JS context
├── chat.html           → chat UI pre-filled with stored profile (crop/lang)
└── knowledge_base.html → top queries list
```

---

## 2. Session Lifecycle

```python
import os

if "sid" not in session:
    session["sid"] = os.urandom(8).hex()
```

- `sid` is generated once per browser session and stored in the Flask session cookie.
- On every page load, `get_farmer_profile(sid)` is called to check for an existing profile.
- If found, crop name, sowing date, and language are pre-filled into the chat form.
- If not found, the farmer is prompted to set up their profile on first use.

---

## 3. Database Schema

```sql
CREATE TABLE IF NOT EXISTS farmer_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    crop_name TEXT NOT NULL,
    sowing_date TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    language TEXT DEFAULT 'en',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

`farmer_profile.session_id` is `UNIQUE`, so `save_farmer_profile()` uses
`ON CONFLICT(session_id) DO UPDATE` to upsert crop, sowing date, and
language whenever the farmer updates their profile.

---

## 4. Knowledge Base (Top Queries)

```python
def get_top_queries(limit=20):
    # Returns the most recent logged queries, newest first
    SELECT question, answer, language, timestamp
    FROM queries ORDER BY id DESC LIMIT ?
```

Every chat exchange is logged via `log_query()`. The `/knowledge` route
renders the most recent entries (limit configurable, spec target: top 30)
so farmers can browse commonly-asked questions without re-typing them.

---

## 5. Out of Scope (per spec)

- No login/password auth — identity is tied to the session cookie only.
- No cross-device sync — `session_id` is local to one browser.
- No multi-profile support per device — one `farmer_profile` row per `session_id`.

---

## 6. Testing Strategy

- Verify `session["sid"]` persists across page reloads within the same browser session.
- Verify `save_farmer_profile()` upserts correctly on repeat calls with the same `session_id`.
- Verify `/knowledge` returns the expected number/order of top queries.
