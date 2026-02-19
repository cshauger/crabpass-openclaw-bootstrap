# OpenClaw bot with env-based configuration
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Install rclone
RUN curl -sL https://rclone.org/install.sh | bash

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
