# We don't want to start from scratch.
# That is why we tell node here to use the current node image as base.
FROM node:14

# Create an application directory
RUN mkdir -p /app

# The /app directory should act as the main application directory
WORKDIR /app

# Copy the app package and package-lock.json file
COPY package.json /app/package.json

# Install node packages
RUN npm install





