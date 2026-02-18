FROM node:22-slim

# Just echo hello to test build works
RUN echo "Build test successful"

CMD ["node", "-e", "console.log('Hello from test container')"]
