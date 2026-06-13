# Feature Spec: Farmer Profile & Session Management

**Status**: Implemented
**Author**: Naga Gireesh Reddy
**Date**: 2026-06-07
**Spec ID**: 004

---

## 1. Problem Statement

Each chat session was stateless — the app had no memory of who the
farmer was, what crop they grew, or what language they preferred.
This forced farmers to repeat context in every conversation.

---

## 2. User Story

> As a returning farmer,
> I want the app to remember my crop and language preference,
> So that I don't have to re-enter it every time I open the app.

---

## 3. Acceptance Criteria

- [x] Unique session ID generated per browser session
- [x] Farmer profile (crop, sowing date, language) saved to SQLite
- [x] Profile loaded on page open and pre-filled in form
- [x] Last 10 chat messages remembered within a session
- [x] Knowledge base shows top 30 most-asked queries

---

## 4. Out of Scope

- User login / password authentication
- Cross-device profile sync
- Multiple profiles per device

---

## 5. Open Questions

- Should session ID persist across browser restarts? (Currently: No)
