# Docker-in-Docker Python Project

A high-performance Python development environment with VS Code optimizations, GitHub Actions Runner, and NVIDIA GPU support.

## Features

- Optimized VS Code development container setup
- NVIDIA CUDA GPU passthrough for accelerated computing
- GitHub Actions Runner for local CI/CD testing
- Modern Python project structure and tooling
- Clean architecture with modular design
- Comprehensive test suite

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

3. **Development Container**
   - When VS Code opens, it will prompt to "Reopen in Container"
   - Click "Reopen in Container" to build and start the development environment
   - The container setup process will handle all dependencies automatically

4. **Running GitHub Actions Locally**
   ```bash
   # Set up GitHub runner (only needed once)
   ~/setup-github-runner.sh
   
   # Run a GitHub workflow locally using act
   act -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-latest
   ```

5. **Running the Application**
   ```bash
   # Run the web server
   python -m dind_python_project run-server
   
   # Process data with CPU
   python -m dind_python_project process-data input.json output.json
   
   # Process data with GPU (if available)
   python -m dind_python_project process-data input.json output.json --gpu
   ```

## Project Structure

```
.
├── .devcontainer/            # VS Code development container configuration
├── .github/                  # GitHub Actions workflows
├── src/                      # Source code
│   └── dind_python_project/  # Main package
│       ├── api/              # Web API components
│       ├── core/             # Core business logic
│       ├── cli.py            # Command-line interface
│       └── config.py         # Configuration handling
├── tests/                    # Test suite
│   ├── api/                  # API tests
│   └── core/                 # Core logic tests
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── pyproject.toml            # Project metadata and dependencies
└── README.md                 # This file
```

## Development Tools

- **Code Quality**: black, isort, flake8, mypy
- **Testing**: pytest, pytest-cov
- **Git Hooks**: pre-commit
- **Automation**: GitHub Actions

## Using GPU Acceleration

The development container automatically configures NVIDIA GPU passthrough if available. To use GPU acceleration in your code, install the optional CUDA dependencies:

```bash
pip install -e ".[cuda]"
```

Then use the `--gpu` flag with the CLI commands or set `USE_GPU=true` in your environment variables.