FROM python:3.10-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    fonts-liberation \
    xdg-utils \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libindicator7 \
    libasound2 \
    libgbm-dev \
    libxshmfence1 \
    libxrandr2 \
    libxdamage1 \
    libxi6 \
    libxcomposite1 \
    libxcursor1 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN LATEST=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -q https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Set display port to avoid crashes
ENV DISPLAY=:99

# Copy project files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your script
CMD ["python", "jobstreet_scraper.py"]
