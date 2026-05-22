---
name: cod8a-uml
description: Generate Mermaid diagrams (class, sequence, flowchart) from source code by extracting JSON structure using cod8a CLI.
---

# cod8a-uml Skill

This skill uses the `cod8a` CLI to extract code structure into a JSON format and then generates a Mermaid diagram based on the user's request.

## Workflow

1.  **Understand the Request:** Determine the target file or project and the requested diagram type (flowchart, class, or sequence).
2.  **Generate JSON:** Run the `cod8a` CLI to generate the JSON representation of the code structure. Use the `-t` flag to specify the diagram type:
    ```bash
    poetry run cod8a uml -f <path_to_file> -t <flowchart|class|sequence> --json
    # OR for a project
    poetry run cod8a uml -p <path_to_project> -t <flowchart|class|sequence> --json
    ```
    *(Note: Ensure you are in the correct directory or provide absolute paths).*
3.  **Select Diagram Skill:** Based on the type specified by the `-t` flag, follow the specific instructions in the corresponding sub-skill file to convert the JSON to Mermaid code:
    *   **Class Diagram (`-t class`):** Refer to `mermaid/class.md`
    *   **Flowchart (`-t flowchart`):** Refer to `mermaid/flowchart.md`
    *   **Sequence Diagram (`-t sequence`):** Refer to `mermaid/sequence.md`
4.  **Output Diagram:** Present the generated Mermaid code to the user or save it to a file as requested.
