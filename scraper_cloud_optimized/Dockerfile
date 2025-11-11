# Use a prebuilt Selenium + Chrome image
FROM selenium/standalone-chrome:115.0

# Set working directory
WORKDIR /app

# Copy your scraper code into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Set environment variables for headless Chrome
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

# Default command to run your scraper
CMD ["python", "jobstreet_scraper.py"]
