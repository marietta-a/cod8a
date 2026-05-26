# Use Python 3.13 as the base image
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1

# Install system dependencies and .NET 10.0 SDK
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    ca-certificates \
    && wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
    && chmod +x dotnet-install.sh \
    && ./dotnet-install.sh --channel 10.0 --install-dir /usr/local/share/dotnet \
    && ln -s /usr/local/share/dotnet/dotnet /usr/local/bin/dotnet \
    && rm dotnet-install.sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set workspace
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY src/ ./src/

# Install dependencies
RUN poetry install --only main

# Build the .NET analyzer
RUN dotnet build src/cod8a/dotnet/CodeAnalysis/CodeAnalyzer.csproj

# Set the entrypoint
ENTRYPOINT ["poetry", "run", "cod8a"]
CMD ["--help"]
