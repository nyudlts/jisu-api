# Base Image
FROM node:21

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Enable pnpm
RUN corepack enable

WORKDIR /usr/app

# install dependencies
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

# Install Python dependencies (if any)
RUN pip3 install --break-system-packages --user requests
RUN pip3 install --break-system-packages --user pysolr
RUN pip3 install --break-system-packages --user ebooklib
RUN pip3 install --break-system-packages --user beautifulsoup4

# RUN sudo apt install pipx 
# sudo apt install python3-requests

COPY ./ ./

EXPOSE 3001

# Default command
CMD ["pnpm", "start"]