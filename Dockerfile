# OpenClaw bot with env-based configuration
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Install unzip first (needed for rclone), then rclone
RUN apt-get update && apt-get install -y unzip && \
    curl -sL https://rclone.org/install.sh | bash && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip, Python libraries, and Playwright dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2 libpango-1.0-0 libcairo2 && \
    pip3 install --break-system-packages openpyxl python-docx python-pptx pandas xlsxwriter playwright && \
    playwright install chromium && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Find where user 1000's home is and set up there
RUN mkdir -p /home/openclaw/.openclaw/workspace /home/openclaw/.config/rclone && \
    chown -R 1000:1000 /home/openclaw

# Copy setup files
COPY setup.py /setup.py
COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh /setup.py

# Copy workspace files (memory, identity, etc.)
COPY *.md /home/openclaw/.openclaw/workspace/
RUN chown -R 1000:1000 /home/openclaw/.openclaw/workspace/

USER 1000
WORKDIR /app

# Point to the correct location
ENV HOME=/home/openclaw
ENV OPENCLAW_STATE_DIR=/home/openclaw/.openclaw
ENV OPENCLAW_CONFIG_PATH=/home/openclaw/.openclaw/config.json5

ENTRYPOINT ["/bootstrap.sh"]
