#!/bin/bash
set -e

# Load environment variables from .env file if it exists
if [ -f "/app/.env" ]; then
    echo "Loading environment variables from .env file"
    export $(grep -v '^#' /app/.env | xargs)
fi

# Function to check for GitHub token and repository from env vars
function check_env_vars() {
    if [ -z "$GITHUB_PERSONAL_TOKEN" ]; then
        echo "Error: GITHUB_PERSONAL_TOKEN environment variable is not set."
        echo "Please add it to your .env file or set it in the Terminal with: export GITHUB_PERSONAL_TOKEN=your_token"
        exit 1
    fi

    if [ -z "$GITHUB_REPOSITORY" ]; then
        echo "Error: GITHUB_REPOSITORY environment variable is not set."
        echo "Please add it to your .env file or set it in the Terminal with: export GITHUB_REPOSITORY=owner/repo"
        exit 1
    fi
}

# Function to download and install the runner
function setup_runner() {
    cd ~/actions-runner

    # Check if runner is already installed
    if [ -f ".runner" ]; then
        echo "Runner is already installed. Checking for updates..."
        
        # Get the latest runner version
        GITHUB_RUNNER_VERSION=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | jq -r '.tag_name[1:]')
        CURRENT_VERSION=$(cat .runner | grep -oP 'Version=\K[0-9.]+')
        
        if [ "$CURRENT_VERSION" != "$GITHUB_RUNNER_VERSION" ]; then
            echo "Updating runner from $CURRENT_VERSION to $GITHUB_RUNNER_VERSION..."
            clean_and_install
        else
            echo "Runner is up to date. Version: $CURRENT_VERSION"
        fi
    else
        clean_and_install
    fi
}

# Function to clean existing runner and install a new one
function clean_and_install() {
    # Clean any existing installation
    rm -rf ~/actions-runner/*

    # Get the latest runner version
    GITHUB_RUNNER_VERSION=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | jq -r '.tag_name[1:]')
    
    # Determine machine architecture
    ARCH=$(uname -m)
    if [ "$ARCH" == "x86_64" ]; then
        RUNNER_ARCH="x64"
    elif [ "$ARCH" == "aarch64" ] || [ "$ARCH" == "arm64" ]; then
        RUNNER_ARCH="arm64"
    else
        echo "Unsupported architecture: $ARCH"
        exit 1
    fi
    
    # Download the runner package
    echo "Downloading runner version $GITHUB_RUNNER_VERSION for $RUNNER_ARCH..."
    RUNNER_PACKAGE="actions-runner-linux-${RUNNER_ARCH}-${GITHUB_RUNNER_VERSION}.tar.gz"
    RUNNER_URL="https://github.com/actions/runner/releases/download/v${GITHUB_RUNNER_VERSION}/${RUNNER_PACKAGE}"
    
    curl -o "${RUNNER_PACKAGE}" -L "${RUNNER_URL}"
    tar xzf "${RUNNER_PACKAGE}"
    rm "${RUNNER_PACKAGE}"
    
    # Configure the runner
    echo "Configuring the runner..."
    
    # Get a registration token
    REG_TOKEN=$(curl -s -X POST \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Authorization: token ${GITHUB_PERSONAL_TOKEN}" \
        "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/runners/registration-token" \
        | jq -r '.token')
    
    if [ "$REG_TOKEN" == "null" ]; then
        echo "Failed to get registration token. Check your personal token and repository."
        exit 1
    fi
    
    # Configure the runner with auto removal when the container stops
    ./config.sh --url "https://github.com/${GITHUB_REPOSITORY}" \
                --token "${REG_TOKEN}" \
                --name "$(hostname)-runner" \
                --work "_work" \
                --labels "self-hosted,Linux,${RUNNER_ARCH}" \
                --unattended \
                --replace \
                --ephemeral
}

# Function to run the runner
function run_runner() {
    echo "Starting runner in the background..."
    cd ~/actions-runner
    nohup ./run.sh > runner.log 2>&1 &
    echo "Runner started. Logs are in ~/actions-runner/runner.log"
    echo "Runner process ID: $!"
}

# Main script execution
echo "GitHub Actions Runner Setup"
echo "==========================="

check_env_vars
setup_runner
run_runner

echo "==========================="
echo "Runner setup complete!"
echo "You can use 'act' to run GitHub Actions workflows locally."
echo "Example: cd /app && act -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest"