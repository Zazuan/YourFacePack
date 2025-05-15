FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender-dev \
    libboost-all-dev \
    libatlas-base-dev \
    libdlib-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "bot.py"]
