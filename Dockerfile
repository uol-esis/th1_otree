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

# Create a virtual environment
RUN python -m venv /venv

# Ensure pip is up-to-date inside venv
RUN /venv/bin/pip install --upgrade pip

# Install Python deps into the venv
COPY requirements-docker.txt .
RUN /venv/bin/pip install --no-cache-dir -r requirements-docker.txt


# =========================
# Stage 2: Final runtime
# =========================
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m otree

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /venv /venv

# Ensure /app is owned by otree user and is writable
USER root
RUN chown -R otree:otree /app

USER otree

# Ensure the venv is used for all Python/Pip commands
ENV PATH="/venv/bin:$PATH"

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run oTree server
CMD ["otree", "prodserver", "0.0.0.0:8000"]
