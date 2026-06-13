# Technical Plan: Crop Calendar & Weekly Task Alerts

**Spec**: specs/003-crop-calendar/spec.md
**Status**: Implemented

---

## 1. Architecture

```
crop_calendar.py
└── CROP_CALENDAR = { crop: { week: task_string } }
└── get_week_task(crop, sowing_date) → (week_number, task_string)

database.py
└── save_farmer_profile(sid, crop, sowing_date, lang)
└── get_farmer_profile(sid) → (crop, sowing_date, lang)
└── log_alert(sid, week, task)

app.py
├── POST /profile/save   → save crop + sowing date
└── GET  /profile/weekly_task → return current week's task
```

---

## 2. Database Schema

```sql
CREATE TABLE farmer_profiles (
    sid TEXT PRIMARY KEY,
    crop_name TEXT,
    sowing_date TEXT,   -- ISO format YYYY-MM-DD
    lang TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alerts_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sid TEXT,
    week INTEGER,
    task TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. Week Calculation Logic

```python
from datetime import date
weeks_since_sowing = (date.today() - sowing_date).days // 7 + 1
task = CROP_CALENDAR[crop].get(weeks_since_sowing, "No task this week")
```
