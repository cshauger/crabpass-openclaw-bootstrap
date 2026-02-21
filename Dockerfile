# OpenClaw bot with env-based configuration
# Pin to specific version for new model support
FROM ghcr.io/openclaw/openclaw:2026.2.3

USER root

# Install rclone
RUN curl -sL https://rclone.org/install.sh | bash

# Install pip and Python libraries for Office files
RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install --break-system-packages openpyxl python-docx python-pptx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Find where user 1000's home is and set up there
RUN mkdir -p /home/openclaw/.openclaw/workspace /home/openclaw/.config/rclone && \
    chown -R 1000:1000 /home/openclaw

# Copy setup files
COPY setup.py /setup.py
COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh /setup.py

USER 1000
WORKDIR /app

# Point to the correct location
ENV HOME=/home/openclaw
ENV OPENCLAW_STATE_DIR=/home/openclaw/.openclaw
ENV OPENCLAW_CONFIG_PATH=/home/openclaw/.openclaw/config.json5

ENTRYPOINT ["/bootstrap.sh"]
