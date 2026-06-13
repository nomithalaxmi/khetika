# Technical Plan: Multilingual UI Language Switcher

**Spec**: specs/001-multilingual-ui/spec.md
**Status**: Implemented
**Author**: Naga Gireesh Reddy
**Date**: 2026-06-07

---

## 1. Tech Stack Choices

| Layer    | Choice                        | Reason                          |
|----------|------------------------------|---------------------------------|
| Frontend | Vanilla JS i18n object       | No build step, zero dependencies|
| Fonts    | Google Fonts Noto Sans       | Best Indian script coverage     |
| Storage  | localStorage                 | Persists across page reloads    |
| Backend  | No changes needed            | Translation is fully client-side|

---

## 2. Architecture

```
chat.html
└── LANGS = { en: {...}, te: {...}, hi: {...}, ta: {...}, kn: {...} }
    └── switchLanguage(lang)
        ├── updates all [data-i18n] elements
        ├── updates hint chips
        ├── updates placeholders
        └── saves to localStorage('khetika_lang')
```

On page load: read `khetika_lang` from localStorage, call switchLanguage.

---

## 3. API Changes

None. Translation is 100% client-side.

---

## 4. Database Changes

None.

---

## 5. UI Changes

- Navbar: language dropdown (EN 🇮🇳 / తె / हि / த / ಕ)
- All static strings tagged with `data-i18n="key"`
- Hint chips re-rendered on language switch
- Placeholder text updated dynamically

---

## 6. Risks & Mitigations

| Risk                              | Mitigation                         |
|-----------------------------------|------------------------------------|
| Font not loading (offline)        | Fallback to system sans-serif      |
| Missing translation key           | Fall back to English string        |
| localStorage not available        | Graceful degradation to English    |
