from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import random
import requests
import os
from dotenv import load_dotenv

# .env Variablen laden
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Definiere die erlaubte Gruppen-ID (ersetze mit deiner tatsächlichen Gruppen-ID)
ALLOWED_GROUP_ID = -123456789  # Beispiel: Ersetze dies mit deiner Gruppen-ID

# Initialisiere die Bot-App
app = Application.builder().token(BOT_TOKEN).build()

# Funktion zur Überprüfung der Gruppen-ID
def is_allowed_group(update: Update) -> bool:
    return update.effective_chat.id == ALLOWED_GROUP_ID

# Befehle
async def start(update: Update, context: CallbackContext):
    if is_allowed_group(update):
        await update.message.reply_text("Hallo! Ich bin dein Telegram-Bot. Wie kann ich helfen?")
    else:
        await update.message.reply_text("⚠ Dieser Bot ist nicht in dieser Gruppe aktiv!")

async def help(update: Update, context: CallbackContext):
    if is_allowed_group(update):
        await update.message.reply_text("Ich bin dein Bot! Verfügbare Befehle:\n/start\n/help\n/random\n/weather\n/meme")
    else:
        await update.message.reply_text("⚠ Dieser Bot ist nicht in dieser Gruppe aktiv!")

async def echo(update: Update, context: CallbackContext):
    if is_allowed_group(update) and update.message.text and not update.message.text.startswith("/"):
        await update.message.reply_text(update.message.text)

async def random_response(update: Update, context: CallbackContext):
    if is_allowed_group(update):
        antworten = ["Ja!", "Nein!", "Vielleicht...", "Frag später nochmal!", "Auf jeden Fall!"]
        await update.message.reply_text(random.choice(antworten))

async def weather(update: Update, context: CallbackContext):
    if is_allowed_group(update):
        city = "Dortmund"  # Optional: Benutzer-Eingabe einbauen
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&;appid={WEATHER_API_KEY}&;units=metric"
        response = requests.get(url).json()

        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            await update.message.reply_text(f"🌤 Das Wetter in {city}: {temp}°C, {desc}")
        else:
            await update.message.reply_text("⚠ Stadt nicht gefunden!")

async def meme(update: Update, context: CallbackContext):
    if is_allowed_group(update):
        url = "https://meme-api.com/gimme"
        response = requests.get(url).json()
        meme_url = response["url"]
        await update.message.reply_photo(meme_url)

async def get_chat_id(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Die Chat-ID ist: {chat_id}")
    
# Handler hinzufügen
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("random", random_response))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("meme", meme))
app.add_handler(CommandHandler("get_chat_id", get_chat_id))
app.add_handler(MessageHandler(filters.TEXT &; ~filters.COMMAND, echo))

# Bot starten
if __name__ == "__main__":
    print("Bot läuft...")
    app.run_polling()
