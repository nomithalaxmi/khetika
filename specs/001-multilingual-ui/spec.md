# Feature Spec: Multilingual UI Language Switcher

**Status**: Implemented
**Author**: Naga Gireesh Reddy
**Date**: 2026-06-07
**Spec ID**: 001

---

## 1. Problem Statement

Farmers using Khetika could only type in their language and get replies
in their language, but the entire UI (buttons, hints, labels,
placeholders) remained in English — creating friction for non-English
users in Telugu, Hindi, Tamil, and Kannada speaking regions.

---

## 2. User Story

> As a Telugu-speaking farmer,
> I want to switch the entire app interface to Telugu,
> So that I can use Khetika without needing to read English.

---

## 3. Acceptance Criteria

- [x] Language dropdown in navbar switches entire UI instantly
- [x] All hint chips shown in selected language
- [x] All button labels, placeholders, modal text translated
- [x] Welcome message shown in selected language
- [x] Language preference persisted via localStorage
- [x] Supported: English, Telugu, Hindi, Tamil, Kannada
- [x] Noto Sans Indian Scripts loaded for correct font rendering
- [x] Works on mobile (responsive layout preserved)

---

## 4. Out of Scope

- Machine-translation of AI responses (Groq/Ollama handles natively)
- RTL language support (Urdu, Arabic)
- Odia, Bengali, Malayalam (planned for future)

---

## 5. Open Questions

All resolved. Feature shipped.
