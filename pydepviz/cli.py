import typer
from enum import Enum
from typing import Optional
from yaspin import yaspin
from pathlib import Path

class OutputFormat(str, Enum):
    HTML = "html"
    SVG = "svg"
    PDF = "pdf"

class ExportFormat(str, Enum):
    PNG = "png"
    JPG = "jpg"
    SVG = "svg"

app = typer.Typer(
    name="dependency-analyzer",
    help="A CLI tool for analyzing and visualizing project dependencies",
    add_completion=True
)

@app.command()
def visualize(
    input_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        help="Path to the dependency file to visualize"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.HTML,
        "-f",
        "--format",
        case_sensitive=False,
        help="Output format for the visualization"
    )
) -> None:
    """
    Visualize project dependencies in various formats.
    """
    typer.echo(f"Visualizing dependencies from {input_file} in {format.value} format.")

@app.command(name="serve")
def serve(
    port: int = typer.Option(
        8000,
        "-p",
        "--port",
        min=1024,
        max=65535,
        help="The port to run the server on",
        show_default=True
    ),
    host: str = typer.Option(
        "127.0.0.1",
        "-h",
        "--host",
        help="The host interface to bind to"
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug mode"
    )
) -> None:
    """
    Start a web server for interactive dependency exploration.
    """
    typer.echo(f"Starting the web server at http://{host}:{port}", color=True)
    if debug:
        typer.echo("Debug mode enabled", color=True)

@app.command(name="export")
def export(
    input_file: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True, help="Path to the dependency file to export"),
    format: ExportFormat = typer.Option(ExportFormat.PNG, "-f", "--format", help="The format to export to (png, jpg, svg)"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-o", help="Directory to save the exported file", dir_okay=True, file_okay=False, resolve_path=True)
) -> None:
    """Export dependency graph to various formats."""
    with yaspin(text="Exporting dependencies...") as spinner:
        try:
            typer.echo(f"Exporting dependencies from {input_file} to {format.value}.")
            spinner.ok("✅ ")
        except Exception as e:
            spinner.fail("💥 ")
            raise typer.Abort() from e

@app.command(name="analyze")
def analyze(
    input_file: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, resolve_path=True, help="The input file to analyze"),
    output_file: Path = typer.Option(Path("dependency_graph.png"), "-o", "--output", help="The output file to save the graph", writable=True),
    include_dev: bool = typer.Option(False, "--include-dev", "-d", help="Include development dependencies"),
    max_depth: Optional[int] = typer.Option(None, "--max-depth", "-m", help="Maximum depth for dependency resolution", min=1)
) -> None:
    """Analyze dependencies and generate a detailed graph."""

    typer.echo(f"Analyzing dependencies from {input_file} and generating a graph at {output_file}.")
    if include_dev:
        typer.echo("Including development dependencies in analysis.")
    if max_depth:
        typer.echo(f"Limiting analysis to depth of {max_depth}.")

def version_callback(value: bool) -> None:
    """Callback to handle the --version flag."""
    if value:
        typer.echo(f"Dependency Analyzer Version 1.0.0")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show the application version and exit.", callback=version_callback, is_eager=True),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output")
) -> None:
    """ A command-line tool for analyzing and visualizing project dependencies."""
    if verbose:
        typer.echo("Verbose mode enabled")

if __name__ == "__main__":
    app()