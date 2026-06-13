# Contributing to Khetika 🌿

Thank you for your interest in contributing to **Khetika** — a multilingual AI farming assistant built for Indian farmers!

---

## How to Contribute

### 1. Fork & Clone

```bash
git clone https://github.com/your-username/khetika.git
cd khetika
```

### 2. Set Up Environment

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

### 3. Run Locally

```bash
python app.py
# Open http://localhost:5000
```

---

## Types of Contributions Welcome

| Type | Examples |
|------|----------|
| 🌾 **Crop Data** | Add new crops to `crop_calendar.py` |
| 🌐 **Translations** | Add UI strings for new languages |
| 🐛 **Bug Fixes** | Fix issues from the GitHub issue tracker |
| ✨ **Features** | New routes in `app.py`, new UI components |
| 📖 **Docs** | Improve README, POC, or this guide |

---

## Adding a New Crop

Edit `crop_calendar.py` and follow the existing format:

```python
"yourcrop": {
    1: "Week 1 task description",
    2: "Week 2 task description",
    # ... up to week 20+
}
```

Then add the crop to the list in `README.md`.

---

## Adding a New Language

1. Add translations to the `i18n` object in `chat.html`
2. Add the language to the language-switcher dropdown
3. Test all UI strings display correctly

---

## Code Style

- Python: Follow PEP 8. Use descriptive variable names.
- HTML/CSS: Use Bootstrap 5 utility classes where possible.
- JS: Vanilla JS only (no jQuery). Use `async/await` for fetch.
- Commit messages: Use present tense — `Add Telugu FAQ hints`, not `Added`.

---

## Pull Request Checklist

- [ ] Code runs without errors (`python app.py`)
- [ ] New features are tested manually
- [ ] Docs updated if needed (README / POC / USER_MANUAL)
- [ ] No hardcoded API keys in code
- [ ] Descriptive PR title and description

---

## Reporting Bugs

Open a GitHub issue with:
- Steps to reproduce
- Expected vs actual behavior
- Browser + OS info
- Screenshot if UI-related

---

## Code of Conduct

Be respectful and constructive. This project is built to help farmers — keep that mission at the center of every contribution.

---

*Questions? Open an issue or reach out to the maintainer.*
