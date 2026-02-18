FROM node:22-bookworm

RUN corepack enable

WORKDIR /app

# Clone and build OpenClaw
RUN git clone --depth 1 https://github.com/openclaw/openclaw.git . && \
    pnpm install --frozen-lockfile && \
    OPENCLAW_A2UI_SKIP_MISSING=1 pnpm build

COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

ENV NODE_ENV=production

# Run as root to avoid permission issues during testing
CMD ["/bootstrap.sh"]
