# Basis-Image
FROM python:3.11-slim

# Systempakete installieren (für Cartopy, GEOS, PROJ etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libproj-dev \
    proj-data \
    proj-bin \
    libgeos-dev \
    libgeos-c1v5 \
    libgdal-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis
WORKDIR /app

# Requirements kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App-Code kopieren
COPY . .

# Streamlit Port
EXPOSE 8501

# Streamlit starten
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

