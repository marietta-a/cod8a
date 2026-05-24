# cod8a

Marietta's own code documentation and visualization tool for .NET and Python projects.

## Installation

```bash
poetry install
```

## Usage

### UML Diagrams

Generate Mermaid class diagrams:

```bash
# Analyze a specific file
cod8a uml -f path/to/file(s)
```

### Documentation

Generate Markdown documentation:

```bash
# Using cod8a doc command
cod8a doc -p path/to/file(s)

```

## Features

- Supports C# (.NET) using a Roslyn-based analyzer.
- Supports Python using AST.
- Generates Mermaid UML diagrams.
- Generates Markdown documentation.
