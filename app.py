from flask import Flask, render_template, request, redirect, url_for
import bot_runner
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Telegram-Nutzer-ID

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    msg = bot_runner.start_bot()
    return redirect(url_for("index", msg=msg))

@app.route("/stop", methods=["POST"])
def stop():
    msg = bot_runner.stop_bot()
    return redirect(url_for("index", msg=msg))

@app.route("/logs")
def logs():
    logs = bot_runner.get_logs()
    return f"<pre>{logs}</pre>"

@app.route("/send", methods=["POST"])
def send():
    message = request.form["message"]
    if message:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))