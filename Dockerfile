# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better caching)
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app
COPY . .

# Expose port used by Streamlit; DO sets $PORT dynamically
EXPOSE 8080

# Default PORT for local runs; DO will override
ENV PORT=8080

# Streamlit runtime config to bind to 0.0.0.0 and chosen PORT
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_ENABLEXSRSFPROTECTION=false \
    STREAMLIT_SERVER_PORT=$PORT \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Ensure data directory exists at runtime
RUN mkdir -p /app/data

CMD sh -c "streamlit run streamlit_app.py --server.port=${PORT} --server.address=0.0.0.0"


