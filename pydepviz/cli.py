import typer
from yaspin import yaspin

app = typer.Typer()

@app.command()
def visualize(
    input_file: str, 
    format: str = "html"
):
    """Visualize dependencies in a specific format."""
    typer.echo(f"Visualizing dependencies from {input_file} in {format} format.")

@app.command()
def serve():
    """Start the web server to explore dependencies."""
    typer.echo("Starting the web server at http://localhost:8000")

@app.command()
def export(
    input_file: str,
    format: str = typer.Option("png","-f", "--format", help="The format to export to.")
):
    """Export dependency graph to a specific format."""
    spinner = yaspin()
    spinner.start()
    typer.echo(f"Exporting dependencies from {input_file} to {format}.")
    spinner.stop()

if __name__ == "__main__":
    app()