"""Command-line interface for the application."""

import click

from dind_python_project.api.app import create_app
from dind_python_project.config import AppConfig
from dind_python_project.core.processor import DataProcessor


@click.group()
def cli() -> None:
    """Command-line interface for dind-python-project."""
    pass


@cli.command(name="run-server")
@click.option("--host", default="0.0.0.0", help="Server host")
@click.option("--port", default=5000, help="Server port")
@click.option("--debug", is_flag=True, help="Enable debug mode")
def run_server(host: str, port: int, debug: bool) -> None:
    """Run the Flask web server."""
    config = AppConfig(debug=debug)
    app = create_app(config)
    click.echo(f"Starting server on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)


@cli.command(name="process-data")
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option("--gpu", is_flag=True, help="Use GPU acceleration if available")
def process_data(input_file: str, output_file: str, gpu: bool) -> None:
    """Process data from INPUT_FILE and save results to OUTPUT_FILE."""
    processor = DataProcessor(use_gpu=gpu)
    click.echo(f"Processing {input_file} {'with GPU' if gpu else 'with CPU'}")
    result = processor.process_file(input_file)
    processor.save_results(result, output_file)
    click.echo(f"Results saved to {output_file}")


def main() -> None:
    """Entry point for the CLI application."""
    cli()