import typer

app = typer.Typer()

@app.command()
def visualize(input_file: str, format: str = "html"):
    typer.echo(f"Visualizing dependencies from {input_file} in {format} format.")

@app.command()
def serve():
    """Start the web server to explore dependencies."""
    typer.echo("Starting the web server at http://localhost:8000")

@app.command()
def export(input_file: str, output_format: str = "png"):
    """Export dependency graph to a specific format."""
    typer.echo(f"Exporting dependencies from {input_file} to {output_format}.")

if __name__ == "__main__":
    app()
