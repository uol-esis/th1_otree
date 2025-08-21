# =========================
# Stage 1: Build dependencies
# =========================
FROM python:3.11-slim AS builder

# Install system deps needed for psycopg2, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements-docker.txt .
RUN pip install --user --no-cache-dir -r requirements-docker.txt


# =========================
# Stage 2: Final runtime
# =========================
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m otree
USER otree

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/otree/.local
ENV PATH=/home/otree/.local/bin:$PATH

# Copy project files
COPY . .


# Expose port
EXPOSE 8000

# Run oTree server
CMD ["otree", "prodserver", "0.0.0.0:8000"]
