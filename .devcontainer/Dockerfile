FROM mcr.microsoft.com/devcontainers/python:3.13-bookworm

# Install .NET 10 SDK
# Using the dotnet-install script for flexibility with versions
RUN apt-get update && apt-get install -y wget \
    && wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
    && chmod +x dotnet-install.sh \
    && ./dotnet-install.sh --channel 10.0 --install-dir /usr/local/share/dotnet \
    && ln -s /usr/local/share/dotnet/dotnet /usr/local/bin/dotnet \
    && rm dotnet-install.sh

# Install Poetry for the vscode user
USER vscode
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/home/vscode/.local/bin:$PATH"

# Configure Poetry to create virtualenvs in the project folder
RUN /home/vscode/.local/bin/poetry config virtualenvs.in-project true

WORKDIR /workspaces/cod8a
