FROM python:3.13-slim

# Instala dependências de sistema para rodar PySide6 / Qt no modo gráfico (X11)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libegl1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libdbus-1-3 \
    libxkbcommon-x11-0 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando padrão
CMD ["python", "main.py"]
