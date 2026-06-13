# Security Policy — Khetika

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.1.x   | ✅ Yes    |
| 1.0.x   | ⚠️ Critical fixes only |
| < 1.0   | ❌ No     |

---

## Reporting a Vulnerability

**Please do NOT open a public GitHub/GitLab issue for security vulnerabilities.**

To report a vulnerability:

1. Email: **security@khetika.example.com** (replace with real address)
2. Subject: `[SECURITY] Brief description`
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge receipt within **48 hours** and aim to resolve confirmed vulnerabilities within **14 days**.

---

## Scope

In scope:
- SQL injection in database.py
- Arbitrary file upload via /chat image endpoint
- Session hijacking / cookie issues
- API key exposure in logs or responses
- Server-Side Request Forgery (SSRF)
- Remote Code Execution

Out of scope:
- Denial of service via large file uploads (rate-limit these at the server level)
- Issues in third-party libraries (report to upstream)
- Social engineering

---

## Security Practices in Khetika

- API keys loaded from `.env` via `python-dotenv` (never hardcoded)
- `.env` excluded from version control via `.gitignore`
- `.env.example` provided with placeholder values only
- Uploaded images processed in-memory, not saved to disk
- SQLite database not exposed via any public route
- Session secret key required via environment variable

---

## Known Limitations (POC)

- No input validation on crop name / sowing date beyond empty check
- No rate limiting on `/chat` endpoint
- No authentication — all sessions are anonymous

These are planned for v2.0.
