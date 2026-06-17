FROM python:3.12-slim AS builder
WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel
COPY pyproject.toml .
COPY src/ src/
RUN pip install --prefix=/install .

FROM python:3.12-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /install /usr/local
COPY pyproject.toml .
COPY src/ src/
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8030
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8030"]
