# Data Model: Farmer Profile & Session Management

## farmer_profile table

| Column      | Type      | Notes                                  |
|-------------|-----------|----------------------------------------|
| id          | INTEGER PK AUTOINCREMENT | Internal row id          |
| session_id  | TEXT UNIQUE NOT NULL | Flask session ID (16 hex chars) |
| crop_name   | TEXT NOT NULL | e.g. "Paddy", "Cotton", "Maize"   |
| sowing_date | TEXT NOT NULL | ISO format: YYYY-MM-DD            |
| language    | TEXT DEFAULT 'en' | en, te, hi, ta, kn             |
| created_at  | DATETIME DEFAULT CURRENT_TIMESTAMP | Auto-set on first insert |

`session_id` is unique, so repeat saves use
`ON CONFLICT(session_id) DO UPDATE` to refresh `crop_name`, `sowing_date`,
and `language` for the existing row rather than inserting a duplicate.

---

## queries table (Knowledge Base)

| Column    | Type      | Notes                          |
|-----------|-----------|----------------------------------|
| id        | INTEGER PK AUTOINCREMENT | Auto-increment        |
| question  | TEXT NOT NULL | Farmer's question              |
| answer    | TEXT NOT NULL | Chatbot's response             |
| language  | TEXT DEFAULT 'en' | Language of the exchange   |
| timestamp | DATETIME DEFAULT CURRENT_TIMESTAMP | Auto-set    |

`get_top_queries(limit)` selects `question, answer, language, timestamp`
ordered by `id DESC`, returning the most recently asked queries for
display on the `/knowledge` page (knowledge_base.html).

---

## Session Object (Flask `session`)

| Key | Type | Notes |
|-----|------|-------|
| sid | str  | `os.urandom(8).hex()` — 16-character hex string, generated once per browser session and used as the foreign key into `farmer_profile.session_id` |

---

## Relationships

```
session["sid"]  ──── 1:1 ────  farmer_profile.session_id
```

- `queries` is independent of session — it is a global, anonymized log
  used purely to populate the shared knowledge base (no `session_id` column).
- `farmer_profile` is keyed 1:1 by `session_id`; each browser session maps
  to at most one profile row (enforced via `UNIQUE` constraint + upsert).
