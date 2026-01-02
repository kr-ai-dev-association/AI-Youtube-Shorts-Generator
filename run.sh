#!/bin/bash
# Detect python version in venv
PYTHON_VERSION=$(venv/bin/python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
export LD_LIBRARY_PATH=$(find $(pwd)/venv/lib/python${PYTHON_VERSION}/site-packages/nvidia -name "lib" -type d 2>/dev/null | paste -sd ":" -)
source venv/bin/activate
python main.py "$@"
