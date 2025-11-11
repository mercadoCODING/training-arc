# Use full Debian-based Python image for stable dependency resolution
FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

# Install all Chrome dependencies
RUN apt-get update && apt-get install -y wget unzip curl gnupg \
    libvulkan1 libnss3 libxss1 libgconf-2-4 \
    libxi6 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxext6 libgbm1 libgtk-3-0 \
    libasound2 xvfb fonts-liberation xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (pinned for compatibility)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Install compatible ChromeDriver (v115)
RUN DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_115") \
    && wget -q "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" -O chromedriver.zip \
    && unzip chromedriver.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver.zip

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Headless Chrome environment
ENV PATH="/usr/bin/chromedriver:${PATH}"
ENV DISPLAY=:99

CMD ["python", "jobstreet_scraper.py"]
