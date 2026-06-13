import os
import base64
import httpx
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from langdetect import detect
from database import (init_db, log_query, get_top_queries,
                      save_farmer_profile, get_farmer_profile, get_all_profiles, log_alert,
                      save_sms_subscription, get_sms_subscriptions, log_mandi_cache, get_mandi_cache)
from crop_calendar import get_week_task, CROP_CALENDAR

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "agribot_dev_secret")

# ─── LLM backend configuration ───────────────────────────────────────────────
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL  = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL     = os.getenv("GROQ_MODEL", "llama3-8b-8192")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "llama3")

# ─── Feature: SMS Alerts (Twilio) ────────────────────────────────────────────
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN  = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")

# ─── Feature: Weather (OpenWeatherMap) ───────────────────────────────────────
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# ─── Feature: Mandi Prices (data.gov.in) ─────────────────────────────────────
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY", "")
MANDI_API_URL    = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

SYSTEM_PROMPT = """
You are AgriBot, an agricultural assistant for Indian farmers.
Answer farming questions clearly and practically.
Topics: crop diseases, fertilizers, irrigation, pest control, soil health, weather, mandi prices.
If the user writes in Telugu, reply in Telugu.
If the user writes in Hindi, reply in Hindi.
Otherwise reply in English.
Keep answers short (3-5 lines max). Be friendly and practical.
"""

init_db()

# ─── LLM helpers ─────────────────────────────────────────────────────────────

def _groq_chat(messages: list[dict]) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
    }
    resp = httpx.post(GROQ_BASE_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _ollama_chat(messages: list[dict]) -> str:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
    }
    resp = httpx.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def llm_chat(messages: list[dict]) -> str:
    if GROQ_API_KEY:
        try:
            return _groq_chat(messages)
        except Exception as exc:
            app.logger.warning("Groq failed (%s), falling back to Ollama.", exc)
    return _ollama_chat(messages)


def _groq_vision(image_b64: str, mime_type: str, prompt: str) -> str:
    vision_model = os.getenv("GROQ_VISION_MODEL", "llama-3.2-11b-vision-preview")
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{image_b64}"},
                },
                {"type": "text", "text": SYSTEM_PROMPT + "\n\nFarmer's question: " + prompt},
            ],
        }
    ]
    payload = {
        "model": vision_model,
        "messages": messages,
        "max_tokens": 512,
    }
    resp = httpx.post(GROQ_BASE_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _ollama_vision(image_b64: str, mime_type: str, prompt: str) -> str:
    vision_model = os.getenv("OLLAMA_VISION_MODEL", "llava")
    url = f"{OLLAMA_BASE_URL}/api/chat"
    messages = [
        {
            "role": "user",
            "content": SYSTEM_PROMPT + "\n\nFarmer's question: " + prompt,
            "images": [image_b64],
        }
    ]
    payload = {"model": vision_model, "messages": messages, "stream": False}
    resp = httpx.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def llm_vision(image_b64: str, mime_type: str, prompt: str) -> str:
    if GROQ_API_KEY:
        try:
            return _groq_vision(image_b64, mime_type, prompt)
        except Exception as exc:
            app.logger.warning("Groq vision failed (%s), falling back to Ollama.", exc)
    return _ollama_vision(image_b64, mime_type, prompt)


def detect_lang(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"


LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
}


def build_messages(history: list[dict], user_msg: str, reply_lang: str = None) -> list[dict]:
    system_prompt = SYSTEM_PROMPT
    if reply_lang and reply_lang in LANGUAGE_NAMES:
        system_prompt += (
            f"\n\nIMPORTANT: Always reply in {LANGUAGE_NAMES[reply_lang]}, "
            f"regardless of the language used in earlier messages."
        )
    msgs = [{"role": "system", "content": system_prompt}]
    for h in history:
        msgs.append({"role": "user",      "content": h["user"]})
        msgs.append({"role": "assistant", "content": h["bot"]})
    msgs.append({"role": "user", "content": user_msg})
    return msgs


# ─── routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if "sid" not in session:
        session["sid"] = os.urandom(8).hex()
    session.setdefault("history", [])
    profile = get_farmer_profile(session["sid"])
    return render_template("chat.html", profile=profile, crops=sorted(CROP_CALENDAR.keys()))


@app.route("/offline")
def offline():
    return render_template("offline.html")


# ── Feature 1: multimodal chat (text + optional image) ──────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    user_msg   = request.form.get("message", "").strip()
    image_file = request.files.get("image")
    ui_lang    = request.form.get("ui_lang", "").strip().lower()

    if not user_msg and not image_file:
        return jsonify({"error": "Empty message"}), 400

    lang    = detect_lang(user_msg) if user_msg else "en"
    history = session.get("history", [])
    # ui_lang (explicit user selection) takes priority over auto-detected lang
    reply_lang = ui_lang if ui_lang in LANGUAGE_NAMES else lang

    try:
        if image_file:
            img_bytes = image_file.read()
            img_b64   = base64.b64encode(img_bytes).decode()
            mime_type = image_file.content_type or "image/jpeg"

            prompt_text = (
                user_msg if user_msg
                else "Identify any crop disease, pest, or problem visible in this image. "
                     "Give a practical remedy for an Indian farmer."
            )
            if reply_lang in LANGUAGE_NAMES:
                prompt_text += f"\n\nReply in {LANGUAGE_NAMES[reply_lang]}."
            bot_reply = llm_vision(img_b64, mime_type, prompt_text)

        else:
            messages  = build_messages(history, user_msg, reply_lang)
            bot_reply = llm_chat(messages)
    except Exception as exc:
        app.logger.error("Chat LLM call failed: %s", exc)
        return jsonify({"error": "LLM unavailable. Please configure GROQ_API_KEY or run Ollama locally."}), 503

    history.append({"user": user_msg or "[photo uploaded]", "bot": bot_reply})
    session["history"] = history[-10:]
    log_query(user_msg or "[photo]", bot_reply, lang)

    return jsonify({"reply": bot_reply, "lang": lang})


# ── Feature 2: save farmer profile ──────────────────────────────────────────
@app.route("/profile/save", methods=["POST"])
def save_profile():
    data        = request.json
    crop_name   = data.get("crop_name", "").strip()
    sowing_date = data.get("sowing_date", "").strip()

    if not crop_name or not sowing_date:
        return jsonify({"error": "Missing crop or date"}), 400

    sid  = session.get("sid", os.urandom(8).hex())
    lang = session.get("lang", "en")
    save_farmer_profile(sid, crop_name, sowing_date, lang)

    week, task = get_week_task(crop_name, sowing_date)
    return jsonify({"week": week, "task": task, "crop": crop_name})


# ── Feature 2: get this week's task ─────────────────────────────────────────
@app.route("/profile/weekly_task")
def weekly_task():
    sid     = session.get("sid")
    profile = get_farmer_profile(sid) if sid else None
    if not profile:
        return jsonify({"task": None})

    crop_name, sowing_date, lang = profile
    week, task = get_week_task(crop_name, sowing_date)

    if task:
        log_alert(sid, week, task)

    return jsonify({
        "crop": crop_name,
        "sowing_date": sowing_date,
        "week": week,
        "task": task,
    })


# ── Feature 3: Real-time Mandi Prices ────────────────────────────────────────
@app.route("/mandi")
def mandi_prices():
    commodity = request.args.get("commodity", "Tomato").strip()
    state     = request.args.get("state", "").strip()

    # Check cache first (1 hour TTL)
    cached = get_mandi_cache(commodity, state)
    if cached:
        return jsonify({"source": "cache", "data": json.loads(cached)})

    try:
        params = {
            "api-key": DATA_GOV_API_KEY,
            "format": "json",
            "filters[commodity]": commodity,
            "limit": 20,
        }
        if state:
            params["filters[state]"] = state

        resp = httpx.get(MANDI_API_URL, params=params, timeout=6)
        resp.raise_for_status()
        result = resp.json()

        records = result.get("records", [])
        if not records:
            app.logger.warning("Mandi API returned no records. Full response: %s", result)
            # Fallback: return sample data if API key not configured
            records = get_sample_mandi_data(commodity)
            return jsonify({"source": "sample", "data": records, "note": "Live data unavailable. Configure DATA_GOV_API_KEY for real prices."})

        # Cache the result
        log_mandi_cache(commodity, state, json.dumps(records))
        return jsonify({"source": "live", "data": records})

    except Exception as e:
        app.logger.warning("Mandi API failed: %s", e)
        # Return sample data as fallback
        records = get_sample_mandi_data(commodity)
        return jsonify({"source": "sample", "data": records, "note": "Live data unavailable. Configure DATA_GOV_API_KEY for real prices."})


def get_sample_mandi_data(commodity):
    """Sample mandi data when API is unavailable."""
    base_prices = {
        "Tomato": (1200, 1800, 1500),
        "Onion": (800, 1200, 1000),
        "Potato": (600, 900, 750),
        "Rice": (1800, 2200, 2000),
        "Wheat": (2000, 2400, 2200),
        "Cotton": (6000, 7000, 6500),
        "Maize": (1400, 1800, 1600),
        "Soybean": (3800, 4200, 4000),
    }
    lo, hi, modal = base_prices.get(commodity, (500, 1000, 750))
    return [
        {"market": "Hyderabad", "state": "Telangana", "commodity": commodity,
         "min_price": str(lo), "max_price": str(hi), "modal_price": str(modal),
         "arrival_date": datetime.now().strftime("%d/%m/%Y")},
        {"market": "Warangal", "state": "Telangana", "commodity": commodity,
         "min_price": str(int(lo * 0.95)), "max_price": str(int(hi * 0.95)), "modal_price": str(int(modal * 0.95)),
         "arrival_date": datetime.now().strftime("%d/%m/%Y")},
        {"market": "Kurnool", "state": "Andhra Pradesh", "commodity": commodity,
         "min_price": str(int(lo * 1.05)), "max_price": str(int(hi * 1.05)), "modal_price": str(int(modal * 1.05)),
         "arrival_date": datetime.now().strftime("%d/%m/%Y")},
    ]


# ── Feature 4: Weather Integration ───────────────────────────────────────────
@app.route("/weather")
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    city = request.args.get("city", "Hyderabad")

    try:
        if lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={OPENWEATHER_API_KEY}&units=metric"

        if not OPENWEATHER_API_KEY:
            raise ValueError("No API key")

        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        weather_info = {
            "city": data.get("name", city),
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s to km/h
            "rainfall": data.get("rain", {}).get("1h", 0),
            "advice": get_farming_weather_advice(data),
        }
        return jsonify({"source": "live", "weather": weather_info})

    except Exception as e:
        app.logger.warning("Weather API failed: %s", e)
        # Sample weather data
        return jsonify({
            "source": "sample",
            "weather": {
                "city": city,
                "temp": 32,
                "feels_like": 36,
                "humidity": 65,
                "description": "Partly Cloudy",
                "icon": "02d",
                "wind_speed": 12.5,
                "rainfall": 0,
                "advice": "Good day for field work. Consider irrigating in the evening to reduce evaporation."
            },
            "note": "Configure OPENWEATHER_API_KEY for real weather data."
        })


def get_farming_weather_advice(data):
    """Generate farming advice based on weather conditions."""
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"] * 3.6
    rain = data.get("rain", {}).get("1h", 0)
    weather_id = data["weather"][0]["id"]

    if rain > 5:
        return "Heavy rainfall expected. Avoid pesticide spraying. Check field drainage to prevent waterlogging."
    elif rain > 0:
        return "Light rain — delay irrigation. Good time to apply urea as it will dissolve quickly."
    elif temp > 38:
        return "Very hot day. Irrigate crops in early morning or late evening. Avoid spraying chemicals."
    elif temp < 15:
        return "Cool weather. Watch for fungal diseases in humid conditions. Ideal for sowing rabi crops."
    elif humidity > 80:
        return "High humidity — risk of fungal diseases. Monitor crops closely and ensure good air circulation."
    elif wind > 30:
        return "Strong winds. Avoid spraying pesticides or fertilizers today as drift will waste chemicals."
    else:
        return "Pleasant farming conditions. Good day for field work, spraying, or transplanting seedlings."


# ── Feature 5: SMS Alerts via Twilio ─────────────────────────────────────────
@app.route("/sms/subscribe", methods=["POST"])
def sms_subscribe():
    data  = request.json
    phone = data.get("phone", "").strip()
    crop  = data.get("crop", "").strip()
    lang  = data.get("lang", "en").strip()

    if not phone or len(phone) < 10:
        return jsonify({"error": "Invalid phone number"}), 400

    # Normalize Indian phone numbers
    if not phone.startswith("+"):
        phone = "+91" + phone.lstrip("0")

    sid = session.get("sid", os.urandom(8).hex())
    save_sms_subscription(sid, phone, crop, lang)

    # Send welcome SMS
    welcome = send_sms(phone, f"🌾 Khetika: Welcome! You'll receive weekly farming tips for {crop.title()}. Reply STOP to unsubscribe.")
    return jsonify({"success": True, "phone": phone, "sms_sent": welcome})


@app.route("/sms/send_weekly", methods=["POST"])
def send_weekly_sms():
    """Trigger weekly SMS alerts to all subscribers (call from cron/scheduler)."""
    if request.headers.get("X-Cron-Secret") != os.getenv("CRON_SECRET", ""):
        return jsonify({"error": "Unauthorized"}), 403

    subs = get_sms_subscriptions()
    sent = 0
    for sid, phone, crop, lang in subs:
        profile = get_farmer_profile(sid)
        if profile:
            crop_name, sowing_date, _ = profile
            week, task = get_week_task(crop_name, sowing_date)
            if task:
                msg = f"🌾 Khetika Week {week} — {crop_name.title()}: {task}"
                if send_sms(phone, msg):
                    sent += 1

    return jsonify({"sent": sent, "total": len(subs)})


def send_sms(to_number: str, message: str) -> bool:
    """Send SMS via Twilio."""
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER):
        app.logger.info("SMS not configured. Would send to %s: %s", to_number, message)
        return False

    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
        resp = httpx.post(url,
            data={"To": to_number, "From": TWILIO_FROM_NUMBER, "Body": message},
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            timeout=10
        )
        resp.raise_for_status()
        return True
    except Exception as e:
        app.logger.warning("SMS send failed: %s", e)
        return False


# ── Knowledge base ───────────────────────────────────────────────────────────
@app.route("/knowledge")
def knowledge():
    rows = get_top_queries(30)
    return render_template("knowledge_base.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
