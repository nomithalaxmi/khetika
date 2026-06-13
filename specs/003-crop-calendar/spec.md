# Feature Spec: Crop Calendar & Weekly Task Alerts

**Status**: Implemented
**Author**: Naga Gireesh Reddy
**Date**: 2026-06-07
**Spec ID**: 003

---

## 1. Problem Statement

Farmers often miss critical crop management tasks (fertilizing, irrigation,
pest scouting) because they have no structured reminder system. Missing
these tasks at the right growth stage leads to lower yields.

---

## 2. User Story

> As a farmer who sowed paddy on June 1st,
> I want to see what task I should do this week,
> So that I don't miss any critical crop management step.

---

## 3. Acceptance Criteria

- [x] Farmer can save crop name + sowing date via profile form
- [x] App calculates current week number from sowing date
- [x] Correct weekly task shown for each crop + week combination
- [x] Tasks logged to database for analytics
- [x] Profile persists across sessions (SQLite + Flask session)
- [x] Crop list: Paddy, Cotton, Groundnut, Maize, Tomato, Chilli

---

## 4. Out of Scope

- Push notifications / SMS alerts
- Multi-crop profiles per farmer
- Weather-adjusted task recommendations

---

## 5. Open Questions

- Should tasks be translated to farmer's language? (Future feature)
