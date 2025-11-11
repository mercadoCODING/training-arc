# Use full Python base image (not slim)
FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

# Install dependencies for Chrome + Chromedriver
RUN apt-get update && apt-get install -y wget unzip curl gnupg libvulkan1 libnss3 libxss1 libgconf-2-4 \
    libxi6 libxrandr2 libxcomposite1 libxcursor1 libxdamage1 libxext6 libgbm1 libgtk-3-0 libasound2 xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome (pinned to version 115 for stability)
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

# Install compatible Chromedriver (matching Chrome 115)
RUN DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_115") \
    && wget -q "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" -O chromedriver.zip \
    && unzip chromedriver.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver.zip

# Install Python requirements
RUN pip install --upgrade pip
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

ENV PATH="/usr/bin/chromedriver:${PATH}"
ENV DISPLAY=:99

CMD ["python", "jobstreet_scraper.py"]
