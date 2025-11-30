FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# main code 
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app

# env variables
ENV PYTHONUNBUFFERED=1
ENV OPENAI_CHAT_MODEL=gpt-4.1-mini
ENV OPENAI_AUDIO_MODEL=gpt-4o-transcribe

# fast api port
EXPOSE 8000

# unicorn server 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


