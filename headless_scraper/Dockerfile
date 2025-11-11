# Use Python 3.10 slim base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates git\
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repo properly (no apt-key)
RUN wget -q -O /usr/share/keyrings/google-linux-signing-key.gpg https://dl.google.com/linux/linux_signing_key.pub \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set display for headless Chrome
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy scraper code into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the scraper
CMD ["python", "jobstreet_scraper.py"]
