# Task List: Multilingual UI Language Switcher

**Plan**: specs/001-multilingual-ui/plan.md
**Status**: Complete ✅
**Author**: Naga Gireesh Reddy
**Date**: 2026-06-07

---

## Phase 1 — Setup

- [x] T01: Add Google Fonts Noto Sans Telugu/Devanagari/Tamil/Kannada *(1h)*
- [x] T02: Create `LANGS` translation object in chat.html *(2h)*

## Phase 2 — Frontend

- [x] T03: Tag all static UI strings with `data-i18n` attributes *(1h)*
- [x] T04: Implement `switchLanguage(lang)` function *(1h)*
- [x] T05: Add language dropdown to navbar *(30m)*
- [x] T06: Persist language choice in localStorage *(30m)*
- [x] T07: Auto-load saved language on page init *(30m)*

## Phase 3 — Testing & Docs

- [x] T08: Manual test all 5 languages — verify all strings update
- [x] T09: Test localStorage persistence across page reloads
- [x] T10: Update USER_MANUAL.md with language switcher instructions
- [x] T11: Update CHANGELOG.md under [Unreleased]
