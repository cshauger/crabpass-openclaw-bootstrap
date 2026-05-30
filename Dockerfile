# OpenClaw bot with env-based configuration
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Install rclone
RUN curl -sL https://rclone.org/install.sh | bash

# Install pip and Python libraries for Office files + Playwright
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install --break-system-packages requests openpyxl python-docx python-pptx pandas xlsxwriter playwright && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Playwright browser (chromium only to save space)
RUN playwright install chromium && playwright install-deps chromium

# Find where user 1000's home is and set up there
RUN mkdir -p /home/openclaw/.openclaw/workspace /home/openclaw/.config/rclone && \
    chown -R 1000:1000 /home/openclaw

# Copy setup files
COPY setup.py /setup.py
COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh /setup.py

# Copy rclone config for Nextcloud
COPY rclone.conf /home/openclaw/.config/rclone/rclone.conf
RUN chown 1000:1000 /home/openclaw/.config/rclone/rclone.conf

# Copy workspace files (memory, identity, etc.)
COPY *.md /home/openclaw/.openclaw/workspace/
RUN chown -R 1000:1000 /home/openclaw/.openclaw/workspace/
