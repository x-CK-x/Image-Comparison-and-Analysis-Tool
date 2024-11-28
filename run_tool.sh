#!/bin/bash

ENV_NAME="image_tool_env"
PYTHON_SCRIPT="inspect_image_tool.py"

# Activate the conda environment
echo "Activating conda environment '${ENV_NAME}'..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

# Run the Python script
echo "Running '${PYTHON_SCRIPT}'..."
python "$PYTHON_SCRIPT"
