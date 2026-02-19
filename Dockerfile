# OpenClaw bot with env-based configuration
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Find where user 1000's home is and set up there
RUN mkdir -p /home/openclaw/.openclaw/workspace && \
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
