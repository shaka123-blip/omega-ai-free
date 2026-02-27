FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 libfontconfig1 libxrender1 libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/output /app/cache /app/assets && \
    chmod 777 /app/data /app/output /app/cache

ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    HF_SPACE=1

EXPOSE 7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "4", "--timeout", "300", "app:app"]
