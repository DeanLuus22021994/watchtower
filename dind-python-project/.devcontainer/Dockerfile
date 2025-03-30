FROM nvidia/cuda:12.4.0-cudnn9-devel-ubuntu22.04 AS base

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set locale and timezone in one layer
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC

# Install system dependencies - grouped to reduce layers
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl wget build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl \
    libpq-dev python3-dev ca-certificates apt-transport-https \
    gnupg lsb-release software-properties-common jq unzip ssh \
    sudo vim && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    # Install Docker CLI
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    # Clean up to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and setup Python environment in one layer
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ENV PYENV_ROOT /opt/pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    # Install pyenv and latest Python
    curl -s -S -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash && \
    pyenv install $(pyenv install --list | grep -v - | grep -v a | grep -v b | grep -v rc | tail -1) && \
    pyenv global $(pyenv versions --bare | tail -1) && \
    pyenv rehash && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    # Install Poetry
    curl -sSL https://install.python-poetry.org | python3 - && \
    echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc && \
    echo 'export PATH="/home/vscode/.local/bin:$PATH"' >> /home/vscode/.bashrc && \
    # Install common Python tools
    pip install --no-cache-dir mypy black flake8 isort pytest pytest-cov pre-commit pip-tools && \
    # Install act for GitHub Actions local testing
    curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | bash && \
    # Setup actions runner directories
    mkdir -p /opt/actions-runner /home/$USERNAME/actions-runner && \
    chown -R $USERNAME:$USERNAME /opt/actions-runner /home/$USERNAME/actions-runner

# Switch to non-root user
USER $USERNAME
WORKDIR /home/$USERNAME

# Script to set up and start GitHub Actions runner
COPY .devcontainer/setup-github-runner.sh /home/$USERNAME/setup-github-runner.sh
RUN sudo chmod +x /home/$USERNAME/setup-github-runner.sh

# Set working directory
WORKDIR /app

# For dev containers, we need Python packages in user site-packages
ENV PATH="/home/vscode/.local/bin:${PATH}"

# Set CI/CD_PYTHON_PATH for better compatibility in CI/CD environments
ENV CI_PYTHON_PATH="/opt/pyenv/shims/python"