# User Manual — Khetika 🌿
### Smart Farming Assistant

---

## What is Khetika?

**Khetika** is your personal farming assistant. You can:
- Ask any farming question in **Telugu, Hindi, or English**
- **Upload a photo** of your crop/leaf to detect diseases
- Set your **crop profile** to get week-by-week reminders
- Switch the **app language** to Telugu, Hindi, Tamil, Kannada, or English

---

## Getting Started

### Step 1 — Open Khetika
Go to `http://localhost:5000` in your browser (or the hosted URL provided by your administrator).

### Step 2 — Choose Your Language
Click the **language dropdown** in the top navigation bar and select:
- 🇮🇳 **Telugu** (తెలుగు)
- 🇮🇳 **Hindi** (हिंदी)
- 🇮🇳 **Tamil** (தமிழ்)
- 🇮🇳 **Kannada** (ಕನ್ನಡ)
- 🌐 **English**

The whole page — buttons, hints, labels, and prompts — will change to your selected language.

---

## How to Chat

1. Type your question in the text box at the bottom
2. Press **Enter** or click **Send**
3. Khetika will reply in your language

**You can type in any language** — Khetika auto-detects it.

### Example Questions

| Language | Question |
|----------|----------|
| English | "What fertilizer is best for rice in sandy soil?" |
| Telugu | "నా పత్తి చేలో పురుగులు వస్తున్నాయి, ఏం చేయాలి?" |
| Hindi | "मेरी फसल की पत्तियाँ पीली हो रही हैं, कारण क्या है?" |

---

## Photo Diagnosis 📷

Upload a photo of your crop leaf or plant to detect diseases.

1. Click the **📷 Photo** button
2. Select an image from your device
3. (Optional) Type a description of the problem
4. Click **Send**

Khetika will analyze the photo and suggest a remedy.

> **Tip**: Make sure the photo is clear and well-lit. Get close to the affected leaf.

---

## Crop Profile & Weekly Tasks 🌾

Set your crop profile to get automated weekly reminders.

1. Click the **🌾 My Crop** button (bottom-right corner)
2. Select your **crop** from the dropdown
3. Enter your **sowing date**
4. Click **Save Profile**

Khetika will show you a **"This Week's Task"** card at the top of the chat — updated automatically based on how many weeks have passed since sowing.

### Supported Crops
- Rice
- Cotton
- Maize
- Tomato
- Wheat

---

## Quick Hint Chips

Below the chat, you'll see colored chips like:
- "Rice fertilizer"
- "Telugu query"
- "Soil health"

Click any chip to quickly fill the input box with a sample question.

---

## Knowledge Base

Click **Knowledge Base** in the top navigation to view:
- All questions asked through Khetika
- Answers and language of each query
- Timestamps

This helps build a local farming knowledge database over time.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No reply from Khetika | Check your internet connection |
| Photo upload not working | Use JPEG or PNG images under 5MB |
| Wrong language in reply | Type your question clearly in your language |
| Weekly task not showing | Make sure you've saved a crop profile |

---

## Privacy

- Your questions are stored locally in a SQLite database on the server
- No data is sent to third parties other than Google Gemini (for AI replies)
- Session data is stored in your browser cookie — clearing cookies resets your profile

---

*Khetika — Built for Indian Farmers 🌾*  
*Made with ❤️ by Nomitha laxmi .ch, IcfaiTech Hyderabad*
