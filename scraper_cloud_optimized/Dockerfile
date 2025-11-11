# ===========================
# Base Image
# ===========================
FROM python:3.11-slim

# ===========================
# Environment Variables
# ===========================
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CHROME_DRIVER_VERSION=116.0.5845.96

# ===========================
# Install Dependencies
# ===========================
RUN apt-get update && apt-get install -y \
        wget \
        unzip \
        curl \
        gnupg \
        ca-certificates \
        fonts-liberation \
        libappindicator3-1 \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libcups2 \
        libdbus-1-3 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        libxcomposite1 \
        libxdamage1 \
        libxrandr2 \
        xdg-utils \
        libgtk-3-0 \
        libgbm1 \
        mesa-utils \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# ===========================
# Install Google Chrome
# ===========================
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# ===========================
# Install Chromedriver
# ===========================
RUN wget -q "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# ===========================
# Set working directory
# ===========================
WORKDIR /app

# Copy scraper code
COPY scraper_cloud_optimized/ /app/

# Install Python dependencies
COPY scraper_cloud_optimized/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# ===========================
# Entrypoint
# ===========================
CMD ["python", "jobstreet_scraper.py"]
