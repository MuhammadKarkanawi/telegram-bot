import subprocess
import sys
import os

script_path = os.path.join(os.getcwd(), "main.py")
bot_process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def start_bot():
    global bot_process
    if bot_process is None:
        bot_process = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return "Bot gestartet."
    else:
        return "Bot läuft bereits."

def stop_bot():
    global bot_process
    if bot_process:
        bot_process.terminate()
        bot_process = None
        return "Bot gestoppt."
    else:
        return "Bot war nicht aktiv."

def get_logs():
    if bot_process and bot_process.stdout:
        try:
            return bot_process.stdout.read().decode(errors="ignore")
        except:
            return "Fehler beim Lesen der Logs."
    return "Keine Logs verfügbar."
    
    
