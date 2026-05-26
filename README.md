# cod8a

cod8a pronounced codetta, is a code documentation and visualization tool for **Python** and **.NET** projects.

## Installation

### Prerequisites

- **[Python 3.9+](https://www.python.org/downloads/)** (Required for all projects)
- **[Poetry](https://python-poetry.org/docs/#installation)** (Required for all projects)
- **[.NET 10.0 SDK](https://dotnet.microsoft.com/download/dotnet/10.0)** (Required **only** if you intend to analyze C#/.NET projects)

### Setup

1. **Fork** the repository on GitHub.
2. **Clone** your fork:

```bash
git clone https://github.com/yourusername/cod8a.git
cd cod8a
```

3. **Install** Python dependencies:

```bash
poetry install
```

4. **Optional**: Ensure .NET 10.0 is installed (if documenting C#)

```bash
dotnet --version
```

## Usage

The tool uses a CLI interface to analyze code and generate visualizations.

### UML Diagrams

Generate Mermaid-compatible diagrams (Class, Sequence, Flowchart):

```bash
# General syntax
cod8a uml -p <path_to_source> -d <diagram_type>

# Generate a class diagram (default)
cod8a uml -p src/my_project

# Generate a sequence diagram
cod8a uml -p src/my_file.py -d sequence

# Generate a flowchart
cod8a uml -p src/my_logic -d flow
```

#### Diagram Type Options:
- **Class:** `class`, `c`
- **Sequence:** `sequence`, `seq`, `s`
- **Flowchart:** `flowchart`, `flow`, `f`

### CLI Options

- `-p, --path`: Path to the file or directory to analyze.
- `-d, --diagram`: Type of diagram to generate (default: `class`).
- `-o, --output`: Output file path (saves as `.mmd`).
- `--json`: Output the raw analysis in JSON format.

### Documentation (In development)

*Note: This feature is currently in development.*

Generate Markdown documentation from code structure:

```bash
# Not yet implemented
cod8a doc -p path/to/source
```

## Features

- **Mermaid Integration:** Generates high-quality Mermaid.js diagrams for visualization.
  - **Supported Diagrams:** Class, Sequence, and Flowchart diagrams.
- **C# Support:** Uses a Roslyn-based analyzer targeting **.NET 10.0** to extract deep structural information.
- **Python Support:** Uses AST-based parsing for Python files.
- **Markdown Documentation (TODO):** Detailed markdown generation for code documentation is currently in development.

