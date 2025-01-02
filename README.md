# PyDepViz

**PyDepViz** is a Python-native dependency graph visualizer designed to simplify the process of analyzing and managing dependencies in Python projects. It provides a detailed, interactive view of your project's dependencies, identifies conflicts, and offers tools to resolve them effectively.

## Features

### Initial Scope
1. **Dependency Parsing**
   - Reads dependencies from files like `requirements.txt`, `pyproject.toml`, `setup.py`, and `Pipfile.lock`.
   - Identifies direct and transitive dependencies.

2. **Interactive Visualization**
   - Displays an interactive dependency graph using HTML, CSS, and JavaScript.
   - Allows zooming, panning, and node-click interactions to view metadata (e.g., version, license, maintainers).

3. **Conflict Detection**
   - Highlights version conflicts and incompatible dependencies.

4. **Vulnerability Scanning**
   - Integrates with APIs like Snyk or PyUp to detect known vulnerabilities.

5. **Export Options**
   - Exports dependency graphs as images (PNG, SVG) and generates summary reports in Markdown or HTML.

### Advanced Features (Future Enhancements)
1. **Environment Comparison**
   - Compare dependencies across different environments or projects.
   - Highlight mismatches between declared and installed versions.

2. **Impact Analysis**
   - Visualize how changes to a dependency propagate throughout the project.

3. **Metrics**
   - Analyze dependencies based on size, popularity, or update frequency.
   - Highlight critical dependencies with many downstream dependents.

4. **Conflict Resolution**
   - Propose and optionally apply fixes for version conflicts.

5. **Web Interface**
   - A real-time, web-based dashboard for exploring dependencies.

## Architecture

### Core Components
1. **Dependency Parser**
   - Reads and parses dependency files into a structured format.

2. **Graph Builder**
   - Converts parsed dependencies into a graph model (JSON format).

3. **Visualization Engine**
   - Renders the graph in the browser using D3.js or similar libraries.

4. **Analyzer**
   - Detects issues like version conflicts, outdated packages, and vulnerabilities.

5. **Export Engine**
   - Outputs graphs and reports for offline use.

6. **Interface**
   - CLI for quick commands and a web interface for in-depth exploration.

## Tech Stack

### Backend
- **Python Libraries**: `networkx`, `pipdeptree`, `click`, `fastapi`.
- **API Integration**: Snyk API, PyUp Safety, NVD for vulnerability data.

### Frontend
- **Visualization Libraries**: D3.js, Cytoscape.js, or Vis.js.
- **Web Stack**: HTML, CSS, and JavaScript.

### Data Format
- **Graph JSON Structure**:
  ```json
  {
    "nodes": [
      { "id": "package_a", "label": "Package A", "group": "direct" },
      { "id": "package_b", "label": "Package B", "group": "transitive" }
    ],
    "edges": [
      { "from": "package_a", "to": "package_b" }
    ]
  }
  ```

## Installation
```bash
pip install pydepviz
```

## Usage
### CLI
```bash
pydepviz visualize requirements.txt
```

### Web Interface
Run the web server:
```bash
pydepviz serve
```
Access the visualization in your browser at `http://localhost:8000`.

### Exporting
```bash
pydepviz export requirements.txt --format png
```

## Development
### Getting Started
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pydepviz.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python -m pydepviz
   ```

### Testing
Run the test suite:
```bash
pytest
```

## Roadmap
- [ ] Implement core dependency parsing.
- [ ] Develop the JSON graph format.
- [ ] Integrate D3.js for interactive visualization.
- [ ] Add conflict detection and resolution tools.
- [ ] Integrate vulnerability scanning with external APIs.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for bug fixes, features, or documentation updates.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

**PyDepViz** aims to be the go-to tool for Python developers to manage and visualize dependencies effectively. Start your journey with PyDepViz today!