# Multi-stage build for smaller footprint
FROM python:3.9-slim as builder

WORKDIR /app

# Install system dependencies (needed for scapy/pcap)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

WORKDIR /app

# Install runtime libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap0.8 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY . .

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Create log directory
RUN mkdir -p logs

ENTRYPOINT ["python3", "src/main.py"]
CMD ["--help"]
