FROM python:3.10-slim

# Arbeitsverzeichnis
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY . .

# .env wird bei Render durch Environment Variables ersetzt
ENV PYTHONUNBUFFERED=1

# Bot starten
CMD ["python", "main.py"]
