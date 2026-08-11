# obraz bazowy: lekki Python 3.12
FROM python:3.12-slim

# biblioteki systemowe wymagane przez opencv-python
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) torch CPU (osobna warstwa = lepszy cache; demo bez GPU)
RUN pip install --no-cache-dir torch torchvision \
        --index-url https://download.pytorch.org/whl/cpu

# 2) reszta zaleznosci
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) kod + wagi modelu (na koncu — zmieniaja sie najczesciej)
COPY vision/ ./vision/
COPY yolov8n.pt ./

# domyslne ustawienia w kontenerze (nadpiszesz przez -e przy docker run)
ENV VIDEO_SOURCE=/app/sample.mp4 \
    DEVICE=cpu \
    WEB_HOST=0.0.0.0

EXPOSE 5000
CMD ["python", "-m", "vision.dashboard", "--no-modbus"]