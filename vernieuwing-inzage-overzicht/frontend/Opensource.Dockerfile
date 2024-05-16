FROM node:20-alpine AS build

# Set the working directory
WORKDIR /app

# Copy the entire application code
COPY ./frontend /app

# Install dependencies and build the Nuxt.js application
RUN npm ci
RUN npm run build

# Use the official Node.js image for the runtime stage
FROM node:20-alpine

# Install Nginx
RUN apk add --no-cache nginx

# Copy the built Nuxt.js application from the build stage
COPY --from=build /app/.output /app/.output

# Expose the port
EXPOSE 3000

# Start the application and Nginx
CMD ["sh", "-c", "nginx -g 'daemon off;' & /usr/local/bin/node /app/.output/server/index.mjs"]