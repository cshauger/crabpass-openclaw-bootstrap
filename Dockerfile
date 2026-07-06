# OpenClaw bot with env-based configuration
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Install rclone
RUN curl -sL https://rclone.org/install.sh | bash

# Install system dependencies for Playwright first
RUN apt-get update && apt-get install -y \
    python3-pip \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages including Playwright
RUN pip3 install --break-system-packages requests openpyxl python-docx python-pptx pandas xlsxwriter playwright

# Install Chromium browser for Playwright
RUN playwright install chromium

# Setup directories
RUN mkdir -p /home/openclaw/.openclaw/workspace /home/openclaw/.config/rclone && \
    chown -R 1000:1000 /home/openclaw

COPY setup.py /setup.py
COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh /setup.py

COPY rclone.conf /home/openclaw/.config/rclone/rclone.conf
RUN chown 1000:1000 /home/openclaw/.config/rclone/rclone.conf

COPY *.md /home/openclaw/.openclaw/workspace/
RUN chown -R 1000:1000 /home/openclaw/.openclaw/workspace/
