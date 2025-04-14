from flask import Flask, render_template, request, redirect, url_for
import bot_runner
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    bot_runner.start_bot()
    return redirect(url_for("index"))

@app.route("/stop", methods=["POST"])
def stop():
    bot_runner.stop_bot()
    return redirect(url_for("index"))

@app.route("/logs")
def logs():
    logs = bot_runner.get_logs()
    return f"<pre>{logs}</pre>"

@app.route("/send", methods=["POST"])
def send():
    message = request.form["message"]
    if message:
        if message.strip() == "/meme":
            meme = requests.get("https://meme-api.com/gimme").json()
            meme_url = meme["url"]
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            requests.post(url, data={"chat_id": CHAT_ID, "photo": meme_url})
        elif message.strip() == "/random":
            antworten = ["Ja!", "Nein!", "Vielleicht...", "Frag später nochmal!", "Auf jeden Fall!"]
            antwort = random.choice(antworten)
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": CHAT_ID, "text": antwort})
        else:
            # Standardtext senden
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
