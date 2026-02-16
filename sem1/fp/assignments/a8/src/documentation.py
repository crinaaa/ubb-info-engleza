
"""
Generate HTML documentation for functions.py using pdoc.

"""

import pdoc
from pathlib import Path

modules = [
    "src.repository.memory_repo",
    "src.repository.text_file_repo",
    "src.repository.binary_file_repo",
]

output_dir = Path("docs")

pdoc.pdoc(*modules, output_directory=output_dir)

print("Documentation has been generated.")