FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

# Menjalankan aplikasi Flask dari file main.py
CMD ["python", "main.py"]
