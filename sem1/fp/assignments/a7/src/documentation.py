"""
Generate HTML documentation for functions.py using pdoc.

"""

import pdoc
from pathlib import Path


module_path = Path("functions.py")

#output folder
output_dir = Path("docs")

# generate the documentation
pdoc.pdoc(module_path, output_directory=output_dir)

print("Documentation has been generated.")
