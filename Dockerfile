# OpenClaw bot with env-based configuration
FROM ghcr.io/openclaw/openclaw:latest

USER root

# Create directories
RUN mkdir -p /data/.openclaw /data/workspace && \
    chown -R 1000:1000 /data

# Copy bootstrap script
COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

USER 1000
WORKDIR /home/node

ENV OPENCLAW_STATE_DIR=/data/.openclaw
ENV OPENCLAW_WORKSPACE_DIR=/data/workspace

ENTRYPOINT ["/bootstrap.sh"]
