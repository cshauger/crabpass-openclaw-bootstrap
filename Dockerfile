# Stage 1: Build
FROM node:22-bookworm AS builder

RUN corepack enable
WORKDIR /app

RUN git clone --depth 1 https://github.com/openclaw/openclaw.git . && \
    pnpm install --frozen-lockfile && \
    OPENCLAW_A2UI_SKIP_MISSING=1 pnpm build && \
    pnpm prune --prod

# Stage 2: Runtime (slim)
FROM node:22-slim

WORKDIR /app

# Copy only production files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

ENV NODE_ENV=production

CMD ["/bootstrap.sh"]
