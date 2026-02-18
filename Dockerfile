FROM node:22-bookworm

# Install pnpm
RUN corepack enable

WORKDIR /app

# Clone OpenClaw and build
RUN git clone --depth 1 https://github.com/openclaw/openclaw.git . && \
    pnpm install --frozen-lockfile && \
    OPENCLAW_A2UI_SKIP_MISSING=1 pnpm build

# Copy bootstrap script
COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

ENV NODE_ENV=production
USER node

ENTRYPOINT ["/bootstrap.sh"]
