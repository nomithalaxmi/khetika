# Changelog

All notable changes to Khetika are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Planned
- Live mandi price API (Agmarknet integration)
- Weather API (IMD / OpenWeather)
- SMS alerts via Twilio/MSG91
- PWA with offline support
- Expanded crop calendar (20+ crops)
- User accounts with full history

---

## [1.1.0] — 2026-06-07

### Added
- Full UI language switcher: Telugu, Hindi, Tamil, Kannada, English
- Language preference persisted via localStorage
- Noto Sans Indian Scripts fonts for correct script rendering
- 4 new documentation files: POC.md, CONTRIBUTING.md, USER_MANUAL.md, AGENTS.md
- Repository health files: .gitignore, .editorconfig, CHANGELOG.md, SECURITY.md, CODE_OF_CONDUCT.md, .env.example, Dockerfile, .dockerignore
- CI/CD pipeline (.gitlab-ci.yml) with test, lint, format, type_check, coverage jobs
- Pre-commit hooks configuration
- Ruff, Mypy, Bandit, Pylint, Flake8, Vulture, Pyupgrade tooling
- Pytest test suite with coverage reporting
- Spec-Kit (.specify/) with constitution.md and feature spec templates
- AGENTS.md: multi-agent architecture design

### Changed
- Redesigned chat.html: modern 2-column layout, animated bubbles, auto-resize textarea
- Redesigned knowledge_base.html: modern table with hover states
- README.md updated with full documentation table

### Fixed
- Session history now capped at 10 turns to prevent context bloat

---

## [1.0.0] — 2026-05-20

### Added
- Initial release of Khetika smart farming assistant
- Multilingual Q&A via Google Gemini 1.5 Flash (text)
- Crop photo disease diagnosis (Gemini Vision)
- Farmer crop profile with weekly task reminders
- Crop calendar for Rice, Cotton, Maize, Tomato, Wheat
- SQLite knowledge base logging all queries
- Flask web app with Bootstrap 5 UI
- Session-based farmer profiles

---

[Unreleased]: https://gitlab.com/your-username/khetika/compare/v1.1.0...HEAD
[1.1.0]: https://gitlab.com/your-username/khetika/compare/v1.0.0...v1.1.0
[1.0.0]: https://gitlab.com/your-username/khetika/releases/tag/v1.0.0
