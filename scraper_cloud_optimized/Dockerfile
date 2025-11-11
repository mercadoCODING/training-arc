# Use full Debian-based Python image for stable dependency resolution
FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

# Install Chrome + dependencies
RUN apt-get update && apt-get install -y wget unzip curl gnupg \
    libvulkan1 libnss3 libxss1 libgconf-2-4 libxi6 libxrandr2 \
    libxcomposite1 libxcursor1 libxdamage1 libxext6 libgbm1 \
    libgtk-3-0 libasound2 xvfb fonts-liberation xdg-utils apt-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (latest stable)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# ✅ Install ChromeDriver 142 (matching Chrome 142)
RUN CHROME_DRIVER_VERSION=142.0.6260.0 \
    && wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_DRIVER_VERSION}/linux64/chromedriver-linux64.zip" -O chromedriver.zip \
    && unzip chromedriver.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm -rf chromedriver.zip chromedriver-linux64

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

ENV PATH="/usr/bin/chromedriver:${PATH}"
ENV DISPLAY=:99

CMD ["python", "jobstreet_scraper.py"]
