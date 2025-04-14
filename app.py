# Flask importieren, um die Web-Anwendung zu erstellen
from flask import Flask, render_template, request, redirect, url_for
# Bot-Funktionen aus einer externen Datei importieren
import bot_runner
# System- und Netzwerkoperationen
import os
import requests
# Für Zufallsgenerierung von Antworten
import random

# Flask-Anwendung initialisieren
app = Flask(__name__)

# API-Schlüssel und Umgebungsvariablen laden
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Token für den Telegram-Bot
CHAT_ID = os.getenv("CHAT_ID")  # Chat-ID, an die Nachrichten gesendet werden
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # API-Schlüssel für Wetterinformationen

# Die Startseite der Webanwendung (Route "/")
@app.route("/")
def index():
    return render_template("index.html")  # Gibt die HTML-Vorlage für die Index-Seite zurück

# Route für den Start des Bots (POST-Request)
@app.route("/start", methods=["POST"])
def start():
    bot_runner.start_bot()  # Startet den Bot (bot_runner ist eine externe Datei)
    return redirect(url_for("index"))  # Leitet zurück zur Index-Seite

# Route für das Stoppen des Bots (POST-Request)
@app.route("/stop", methods=["POST"])
def stop():
    bot_runner.stop_bot()  # Stoppt den Bot
    return redirect(url_for("index"))  # Leitet zurück zur Index-Seite

# Route für das Abrufen von Logs des Bots
@app.route("/logs")
def logs():
    logs = bot_runner.get_logs()  # Holt sich die Logs aus dem Bot-Runner
    return f"<pre>{logs}</pre>"  # Gibt die Logs in einem formatierten HTML-Tag aus

# Route zum Senden von Nachrichten (POST-Request)
@app.route("/send", methods=["POST"])
def send():
    # Die Nachricht aus dem Formular extrahieren
    message = request.form["message"].strip()
    # Telegram API URLs für das Senden von Nachrichten und Bildern
    url_send = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    url_photo = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    if message:  # Wenn eine Nachricht vorhanden ist
        # Wenn die Nachricht "/meme" ist, ein zufälliges Meme holen
        if message == "/meme":
            meme = requests.get("https://meme-api.com/gimme").json()  # Holen eines Memes von einer API
            meme_url = meme["url"]  # URL des Memes extrahieren
            requests.post(url_photo, data={"chat_id": CHAT_ID, "photo": meme_url})  # Meme über Telegram senden

        # Wenn die Nachricht "/random" ist, eine zufällige Antwort auswählen
        elif message == "/random":
            antworten = ["Ja!", "Nein!", "Vielleicht...", "Frag später nochmal!", "Auf jeden Fall!"]
            antwort = random.choice(antworten)  # Zufällige Antwort wählen
            requests.post(url_send, data={"chat_id": CHAT_ID, "text": antwort})  # Antwort über Telegram senden

        # Wenn die Nachricht "/weather" ist, das Wetter abfragen
        elif message == "/weather":
            city = "Dortmund"  # Die Stadt für die Wetterabfrage festlegen
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"  # URL für Wetter-API
            response = requests.get(weather_url).json()  # Wetterdaten abrufen

            if response.get("cod") == 200:  # Wenn die Anfrage erfolgreich war
                temp = response["main"]["temp"]  # Temperatur extrahieren
                desc = response["weather"][0]["description"]  # Wetterbeschreibung extrahieren
                text = f"🌤 Das Wetter in {city}: {temp}°C, {desc}"  # Text für das Wetter
            else:
                text = "⚠ Stadt nicht gefunden!"  # Fehlertext, wenn die Stadt nicht gefunden wird

            requests.post(url_send, data={"chat_id": CHAT_ID, "text": text})  # Wetter über Telegram senden

        # Wenn die Nachricht "/start" ist, eine Begrüßung senden
        elif message == "/start":
            text = "Hallo! Ich bin dein Telegram-Bot. Wie kann ich helfen?"  # Begrüßungsnachricht
            requests.post(url_send, data={"chat_id": CHAT_ID, "text": text})  # Nachricht über Telegram senden

        else:
            # Standardtext senden, wenn keine der speziellen Nachrichten eingegeben wurde
            requests.post(url_send, data={"chat_id": CHAT_ID, "text": message})

    return redirect(url_for("index"))  # Nach dem Senden der Nachricht zur Index-Seite zurückkehren

# Die Anwendung wird gestartet, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))  # Flask-App auf Port 8080 oder einem Umgebungsport starten
