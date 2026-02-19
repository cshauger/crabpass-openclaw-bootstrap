# OpenClaw bot with env-based configuration
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Create directories
RUN mkdir -p /data/.openclaw /data/.openclaw/workspace && \
    chown -R 1000:1000 /data

# Copy setup files
COPY setup.py /setup.py
COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh /setup.py

USER 1000
WORKDIR /app

ENV OPENCLAW_STATE_DIR=/data/.openclaw
ENV OPENCLAW_CONFIG_PATH=/data/.openclaw/config.json5

ENTRYPOINT ["/bootstrap.sh"]
