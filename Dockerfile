FROM python:3.14-slim

WORKDIR /cinema_backend

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./

RUN pip install --upgrade pip
RUN pip install uv
RUN uv pip install --system .

COPY . .

EXPOSE 8000