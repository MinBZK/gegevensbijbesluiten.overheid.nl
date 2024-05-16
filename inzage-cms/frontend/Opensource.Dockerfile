FROM node:20-alpine

WORKDIR /app

# Copy source code
COPY ./frontend /app

# Install dependencies
RUN npm ci

# Expose port
EXPOSE 8080

# Start the application
CMD ["npm", "run", "serve"]