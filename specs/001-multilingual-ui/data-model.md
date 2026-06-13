# Data Model: Multilingual UI

No database changes. All translation data lives in client-side JS.

## Translation Object Structure

```javascript
const LANGS = {
  en: {
    appSubtitle: "Smart Farming Assistant",
    inputPlaceholder: "Ask your farming question here...",
    sendBtn: "Send",
    quickPrompts: "Quick Prompts",
    hints: ["Crop disease", "Fertilizer tips", "Pest control", ...]
  },
  te: { /* Telugu strings */ },
  hi: { /* Hindi strings */ },
  ta: { /* Tamil strings */ },
  kn: { /* Kannada strings */ }
}
```

## localStorage Schema

| Key            | Type   | Values              |
|----------------|--------|---------------------|
| khetika_lang   | string | en, te, hi, ta, kn  |
