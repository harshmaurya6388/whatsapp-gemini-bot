from flask import Flask, request
import requests
import google.generativeai as genai
import os

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("AIzaSyC1zKUh7bl1dJlvSeo6UEcYT4GF3Ca5yoQ")
WHATSAPP_TOKEN = os.getenv("EAAJP3CWZBOvgBPDGYwZCp9YRyVqiU7IKuA9xY4cI3PIQhfIEX3prnqxxRIkb2A4VR0d5vF87ZCeBsZCxqIQnZCx85ZB5ga8be29PoZAgY0RaOwUu7CNZCftMEspMfEgIF0ebNx3nSp6olm2Wyz0VC7iYsuTs50Mq0S84XGUeelh8SIuOaahuGFA6NqJGxsuGQEjHFZCyIpu15e54SNR52K9oyeLrTiHcmyZATqrLOyKpxsenw8160ZD")
VERIFY_TOKEN = os.getenv("testbot")
PHONE_NUMBER_ID = os.getenv("769157359612667")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        user_text = message["text"]["body"]
        user_number = message["from"]

        response = model.generate_content(user_text)
        reply = response.text

        url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "messaging_product": "whatsapp",
            "to": user_number,
            "type": "text",
            "text": {"body": reply}
        }
        requests.post(url, headers=headers, json=body)

    except Exception as e:
        print("Error:", e)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
