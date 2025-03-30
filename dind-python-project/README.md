# Docker-in-Docker Python Project

A high-performance Python development environment with VS Code optimizations, GitHub Actions Runner, and NVIDIA GPU support.

## Features

- Optimized VS Code development container setup
- NVIDIA CUDA GPU passthrough for accelerated computing
- GitHub Actions Runner for local CI/CD testing
- Modern Python project structure and tooling
- Clean architecture with modular design
- Comprehensive test suite
- Centralized configuration using `.env` file

## Quick Start

1. **Prerequisites**
   - VS Code with Remote Development extension
   - Docker Desktop with NVIDIA Container Toolkit (for GPU support)
   - Git

2. **Setup**

   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/dind-python-project.git
   cd dind-python-project
   
   # Copy the environment template and update values
   cp .env.template .env
   # Edit .env with your GitHub token and repository
   
   # Open in VS Code
   code .
   ```

3. **Configuration**

   The project uses a `.env` file as the single source of truth for all configuration. This file contains environment variables that configure all aspects of the application. Edit the `.env` file to customize your settings:

   ```properties
   # GitHub Actions runner settings
   GITHUB_PERSONAL_TOKEN=your_personal_access_token_here
   GITHUB_REPOSITORY=your_username/your_repository

   # Python settings
   DEBUG=false
   ENV=development
   LOG_LEVEL=INFO
   USE_GPU=true

   # Flask settings
   FLASK_APP=dind_python_project.api.app:create_app()
   FLASK_ENV=development
   
   # Other settings
   PROJECT_NAME=dind-python-project
   VERSION=0.1.0
   ```

4. **Development Container**
   - When VS Code opens, it will prompt to "Reopen in Container"
   - Click "Reopen in Container" to build and start the development environment
   - The container setup process will handle all dependencies automatically
   - The `.env` file will be loaded automatically in the container

5. **Running GitHub Actions Locally**

   ```bash
   # Set up GitHub runner (only needed once)
   ~/setup-github-runner.sh
   
   # Run a GitHub workflow locally using act
   act -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest
   ```

6. **Running the Application**

   ```bash
   # Run the web server
   python -m dind_python_project run-server
   
   # Process data with CPU
   python -m dind_python_project process-data input.json output.json
   
   # Process data with GPU (if available)
   python -m dind_python_project process-data input.json output.json --gpu
   
   # Display current configuration from .env file
   python -m dind_python_project config
   ```

## Development Tools

- **Code Quality**: black, isort, flake8, mypy
- **Testing**: pytest, pytest-cov
- **Git Hooks**: pre-commit
- **Automation**: GitHub Actions
- **Configuration**: python-dotenv for .env file management

## Using GPU Acceleration

The development container automatically configures NVIDIA GPU passthrough if available. To use GPU acceleration in your code, install the optional CUDA dependencies:

```bash
pip install -e ".[cuda]"
```

Then use the `--gpu` flag with the CLI commands or set `USE_GPU=true` in your `.env` file.

## Using .env for Configuration

The project uses the `python-dotenv` package to load environment variables from a `.env` file. This ensures a single source of truth for all configuration settings. The configuration is loaded automatically by the application at startup.

To view the current configuration derived from your `.env` file:

```bash
python -m dind_python_project config
```

### Configuration Precedence

1. Command-line arguments (highest priority)
2. Environment variables set in the shell
3. Variables in the `.env` file
4. Default values in the code (lowest priority)
