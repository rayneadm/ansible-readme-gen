FROM python:3.12-slim

# system deps
RUN apt-get update && apt-get install -y \
    tree \
    ansible \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/generate_readme.py .

ENTRYPOINT ["python", "/app/generate_readme.py"]
