import sqlite3
from datetime import datetime, timedelta

DB = "agribot.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Chat query log
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Farmer crop profile for seasonal memory
    c.execute('''
        CREATE TABLE IF NOT EXISTS farmer_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL UNIQUE,
            crop_name TEXT NOT NULL,
            sowing_date TEXT NOT NULL,
            language TEXT DEFAULT 'en',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Weekly task alerts log
    c.execute('''
        CREATE TABLE IF NOT EXISTS weekly_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            week_number INTEGER NOT NULL,
            task TEXT NOT NULL,
            sent_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Feature: SMS subscriptions
    c.execute('''
        CREATE TABLE IF NOT EXISTS sms_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL UNIQUE,
            phone_number TEXT NOT NULL,
            crop_name TEXT DEFAULT '',
            language TEXT DEFAULT 'en',
            active INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Feature: Mandi price cache (TTL 1 hour)
    c.execute('''
        CREATE TABLE IF NOT EXISTS mandi_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            commodity TEXT NOT NULL,
            state TEXT DEFAULT '',
            data TEXT NOT NULL,
            cached_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def log_query(question, answer, language):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO queries (question, answer, language) VALUES (?, ?, ?)",
              (question, answer, language))
    conn.commit()
    conn.close()


def get_top_queries(limit=20):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT question, answer, language, timestamp FROM queries ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows


# Farmer profile helpers
def save_farmer_profile(session_id, crop_name, sowing_date, language):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        INSERT INTO farmer_profile (session_id, crop_name, sowing_date, language)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            crop_name=excluded.crop_name,
            sowing_date=excluded.sowing_date,
            language=excluded.language
    ''', (session_id, crop_name, sowing_date, language))
    conn.commit()
    conn.close()


def get_farmer_profile(session_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT crop_name, sowing_date, language FROM farmer_profile WHERE session_id=?", (session_id,))
    row = c.fetchone()
    conn.close()
    return row


def get_all_profiles():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT session_id, crop_name, sowing_date, language FROM farmer_profile")
    rows = c.fetchall()
    conn.close()
    return rows


def log_alert(session_id, week_number, task):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO weekly_alerts (session_id, week_number, task) VALUES (?, ?, ?)",
              (session_id, week_number, task))
    conn.commit()
    conn.close()


# SMS subscription helpers
def save_sms_subscription(session_id, phone_number, crop_name, language):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        INSERT INTO sms_subscriptions (session_id, phone_number, crop_name, language)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            phone_number=excluded.phone_number,
            crop_name=excluded.crop_name,
            language=excluded.language,
            active=1
    ''', (session_id, phone_number, crop_name, language))
    conn.commit()
    conn.close()


def get_sms_subscriptions():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT session_id, phone_number, crop_name, language FROM sms_subscriptions WHERE active=1")
    rows = c.fetchall()
    conn.close()
    return rows


# Mandi cache helpers
def log_mandi_cache(commodity, state, data):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # Delete old cache for this commodity/state
    c.execute("DELETE FROM mandi_cache WHERE commodity=? AND state=?", (commodity, state))
    c.execute("INSERT INTO mandi_cache (commodity, state, data) VALUES (?, ?, ?)",
              (commodity, state, data))
    conn.commit()
    conn.close()


def get_mandi_cache(commodity, state, ttl_minutes=60):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(minutes=ttl_minutes)).strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "SELECT data FROM mandi_cache WHERE commodity=? AND state=? AND cached_at > ?",
        (commodity, state, cutoff)
    )
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
