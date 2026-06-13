# Data Model: Crop Calendar

## farmer_profiles table

| Column      | Type    | Notes                    |
|-------------|---------|--------------------------|
| sid         | TEXT PK | Flask session ID (8 hex) |
| crop_name   | TEXT    | e.g. "Paddy", "Cotton"   |
| sowing_date | TEXT    | ISO: YYYY-MM-DD          |
| lang        | TEXT    | en, te, hi, ta, kn       |
| updated_at  | TIMESTAMP | Auto-set               |

## alerts_log table

| Column    | Type    | Notes              |
|-----------|---------|--------------------|
| id        | INT PK  | Auto-increment     |
| sid       | TEXT    | FK → farmer_profiles|
| week      | INT     | Week number (1–16) |
| task      | TEXT    | Task description   |
| logged_at | TIMESTAMP | Auto-set         |

## CROP_CALENDAR structure

```python
CROP_CALENDAR = {
  "Paddy": {
    1: "Nursery preparation and seed treatment",
    2: "Transplanting seedlings",
    ...
    16: "Harvest preparation"
  },
  "Cotton": { ... },
  ...
}
```
