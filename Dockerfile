FROM python:3.9-slim

# Working directory
WORKDIR /app

# Copying all files to the container
COPY . /app

# Install required packages for installation and build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Installing Node.js (LTS version) and npm
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm && \
    rm -rf /var/lib/apt/lists/*

# Installing g++ (required for compiling C++ code)
RUN apt-get update && \
    apt-get install -y g++ && \
    rm -rf /var/lib/apt/lists/*

# Installing Java (for Java-based code execution)
RUN apt-get update && \
    apt-get install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

# Exposing the port Flask runs on
EXPOSE 5000

# Setting environment variables for Flask
ENV FLASK_APP=app.py

# Running the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
