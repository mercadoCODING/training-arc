FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repo properly (no apt-key)
RUN wget -q -O /usr/share/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:99

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "jobstreet_scraper.py"]

