---
name: mermaid
description: Generate Mermaid diagrams (class, sequence, flowchart) from source code by extracting JSON structure using cod8a CLI and generating the diagrams. Use this skill to visualize code architecture, extract structural data, and export diagrams as PDF.
---

# Mermaid Tools

This skill enables the generation of Mermaid diagrams (Class, Sequence, Flowchart) by extracting the code structure as JSON using the `cod8a` CLI and then writing the Mermaid code based on specific diagram guidelines. The agent is responsible for converting the extracted structural data into the correct Mermaid format.

## Workflow

1. **Extract Data**: Use the `cod8a` CLI to parse the code and output the structure in JSON format.
   - Analyze a file: `poetry run cod8a uml -f <path_to_file> --json`
   - Analyze a project: `python -m src.cod8a.cli uml -p <path_to_project> --json`

2. **Load Guidelines**: Based on the requested diagram, refer to the corresponding reference file for generation rules:
   - **Class Diagram**: Convert the json result from the `struct` to a mermaid code, then generate a class diagram following the instructions in: [references/class_diagram.md](references/class_diagram.md)
   - **Sequence Diagram**: Read [references/sequence_diagram.md](references/sequence_diagram.md)
   - **Flowchart**: Read [references/flowchart.md](references/flowchart.md)

3. **Generate Diagram**: As the agent, read the JSON output from step 1 and apply the rules from step 2 to write the complete Mermaid code. Save the resulting Mermaid code to a temporary `.mmd` file (e.g., `docs/diagram.mmd`).

4. **Export to PDF**: If the user requests a PDF, use the Mermaid CLI (`mmdc`) to convert the generated `.mmd` file to PDF:
   ```bash
   # Ensure the docs directory exists
   mkdir -p docs
   # Convert to PDF
   mmdc -i docs/diagram.mmd -o docs/diagram.pdf
   ```