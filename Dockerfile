# ==========================================
# Stage 1: Build & Compile Dependencies
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Install system utilities required to compile C++ extensions (needed for prophet/xgboost)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker's build cache layers
COPY requirements.txt .

# Install dependencies into a local user directory
RUN pip install --no-cache-dir --user -r requirements.txt


# ==========================================
# Stage 2: Minimalist Production Runtime
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy the pre-compiled Python packages from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy your internal application source directories
COPY ./src ./src

# Set environment variables so Python can locate the installed packages and directories
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Expose Streamlit's default networking port
EXPOSE 8501

# The execution command that fires up your application dashboard
ENTRYPOINT ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
