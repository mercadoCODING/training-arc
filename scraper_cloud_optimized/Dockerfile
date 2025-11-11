# ==========================
# Base image
# ==========================
FROM python:3.11-slim

# ==========================
# Install system dependencies for Chrome + Selenium
# ==========================
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf-xlib-2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# ==========================
# Install Google Chrome (latest stable) without apt-key
# ==========================
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# ==========================
# Install Chromedriver (matches Chrome version)
# ==========================
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1) \
    && DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") \
    && wget -q "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# ==========================
# Set working directory
# ==========================
WORKDIR /app

# ==========================
# Copy scraper code
# ==========================
COPY . .

# ==========================
# Install Python dependencies
# ==========================
RUN pip install --no-cache-dir -r requirements.txt

# ==========================
# Environment variables for headless Chrome
# ==========================
ENV CHROME_BIN=/usr/bin/google-chrome
ENV DISPLAY=:99

# ==========================
# Run scraper
# ==========================
CMD ["python", "jobstreet_scraper.py"]
